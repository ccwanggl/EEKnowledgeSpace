---
tags: [ethernet, tcp-ip, network, embedded, lwip, socket]
date-created: 2026-09-12
date-updated: 2026-09-12
aliases: [Socket编程, TCP echo服务端, 阻塞与非阻塞socket, 心跳重连, htons]
---

# Socket 编程与并发模型

Socket 层把连接的建立、收发与关闭抽象成文件描述符式的调用序列，代价是引入按连接划分的状态与缓冲。在 RTOS 上写 socket 代码，真正决定系统能否稳定运行的不是 API 用法，而是阻塞语义、并发模型与超时策略这三项选择。

## 1. 阻塞与非阻塞在 RTOS 任务中的差异

阻塞 socket 的 `accept`/`recv`/`send` 会挂起当前任务直到条件满足，任务在等待期间让出 CPU，写法直观但一个任务只能服务于一个流程。非阻塞 socket 立即返回，未就绪时返回 `-1` 并置 `errno` 为 `EAGAIN`/`EWOULDBLOCK`，需要配合 `select`/`poll` 或轮询使用。

在 RTOS 中的实际差异：

- 阻塞调用会因对端长时间无数据而永久占住任务，若该任务的优先级较高且与其他任务共享资源，容易形成优先级反转或看门狗超时；
- 非阻塞调用必须自行处理"部分读写"：`recv` 返回的字节数可能小于请求值，`send` 返回的字节数也可能小于待发长度，必须循环直到发完或无法继续；
- lwIP 的 socket 默认继承其 netconn 的接收超时，实际默认值与是否启用 `LWIP_SO_RCVTIMEO` 相关，**以所用版本 API 为准**；
- 在 `NO_SYS=1` 的裸机配置下没有 socket 层，只有 RAW 回调，不能用本节的写法。

推荐组合是：接收路径用阻塞 socket 放在独立任务中（由内核负责挂起），发送路径用非阻塞或带超时的写法，避免发送阻塞拖死接收任务。

## 2. 最小 TCP echo 服务端与客户端流程

服务端：`socket` → `bind` → `listen` → `accept` → `recv`/`send` 循环 → `close`。客户端：`socket` → 可选 `bind` → `connect` → `send`/`recv` 循环 → `close`。

```c
/* 服务端骨架（lwIP socket 风格，以所用版本 API 为准） */
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <lwip/sockets.h>

int srv = socket(AF_INET, SOCK_STREAM, 0);
struct sockaddr_in addr;
memset(&addr, 0, sizeof(addr));
addr.sin_family = AF_INET;
addr.sin_addr.s_addr = htonl(INADDR_ANY);   /* 监听所有本地地址 */
addr.sin_port = htons(7000);
bind(srv, (struct sockaddr *)&addr, sizeof(addr));
listen(srv, 2);                              /* backlog：排队等待 accept 的连接数 */

for (;;) {
    struct sockaddr_in peer;
    socklen_t len = sizeof(peer);
    int cli = accept(srv, (struct sockaddr *)&peer, &len);
    if (cli < 0) continue;                   /* 例如 EAGAIN 或资源不足 */

    char buf[512];
    for (;;) {
        int n = recv(cli, buf, sizeof(buf), 0);
        if (n == 0) break;                   /* 对端正常关闭 */
        if (n < 0) break;                    /* 出错，errno 区分原因 */
        int off = 0;
        while (off < n) {                    /* send 可能只发一部分 */
            int w = send(cli, buf + off, n - off, 0);
            if (w <= 0) break;
            off += w;
        }
    }
    close(cli);
}
```

`bind` 的地址用 `htonl(INADDR_ANY)` 表示接受任意本地地址；只绑定端口而不指定地址在多网口设备上的行为需要确认。`listen` 的 backlog 在 lwIP 中对应 `MEMP_NUM_TCP_PCB` 可承受的排队长度，取值超过连接池容量没有意义。

客户端的关键差异是 `connect` 可能返回 `EINPROGRESS`（非阻塞）或直接失败；连接建立后同样要处理 `recv` 返回 0 表示对端关闭，返回负值表示错误。

## 3. 多连接处理的三种模型

| 模型 | RAM 开销 | 复杂度 | 适用场景 |
|---|---|---|---|
| 一线程一连接 | 每连接一个任务栈（通常 1~4 KB）+ PCB + 收发缓冲 | 低，写法直观 | 连接数少（≤5）、逻辑复杂 |
| 单线程 select/poll 事件循环 | 无额外任务栈，但需描述符集合与每连接状态缓冲 | 中，需状态机 | 连接数中等（10~50）、报文短 |
| 回调式 RAW API | 只保留 PCB 与 pbuf | 高，回调嵌套与状态管理难 | 连接数多、资源极紧或无 OS |

一线程一连接的主要风险是任务数随连接数增长，`MEMP_NUM_TCP_PCB` 和堆都会先于 CPU 成为瓶颈；连接异常未清理会导致任务与 PCB 双双泄漏。select 事件循环用单任务处理全部连接，缺点是任一连接的处理代码变长就会拖慢其他连接，且必须严格避免在循环中阻塞。RAW 回调在中断或协议栈上下文中执行，回调里做耗时运算会直接造成丢包。

`select` 的第一个参数（最大描述符加一）在 lwIP 中通常被忽略，但为了可移植性仍应正确填写；`fd_set` 的大小受 `LWIP_SOCKET` 相关宏限制，可监控的描述符数量有上限，超出后 `select` 无法感知。

## 4. 超时与错误处理语义

- `EAGAIN`/`EWOULDBLOCK`：非阻塞操作当前无法完成，不是错误，应稍后重试；两者在多数实现中是同一个值，不能假设可区分；
- `SO_RCVTIMEO`：为 `recv` 设置超时，超时后返回 `-1` 且 `errno` 为 `EAGAIN` 或 `EWOULDBLOCK`，需要 `LWIP_SO_RCVTIMEO` 支持；`SO_SNDTIMEO` 的支持情况更受限，**以所用版本 API 为准**；
- `recv` 返回 0：对端已有序关闭，本端应完成剩余发送并 `close`；
- `recv` 返回负值：连接被复位（`ECONNRESET`）、超时、或被信号中断，处理方式各不相同，不能一律重试；
- `send` 返回负值且 `errno` 为 `EPIPE`/`ECONNRESET`：对端已断开，继续写入会反复失败；
- 向已关闭的对端发送时，若开启 `SO_LINGER` 且超时为 0，`close` 会发送 RST 而非正常挥手，可能丢失对端尚未读取的数据。

应用层超时不应只依赖 TCP 重传：重传耗尽可能需要数十秒到数分钟。工程做法是在 `recv` 上加短超时或用心跳任务统一判定，再主动 `close`。

## 5. 心跳与重连策略

心跳报文应满足三条：内容固定且短、能被对端明确回应、间隔小于路径上所有中间设备的空闲超时。常见形式是应用层 PING/PONG 或协议内建机制（MQTT 的 Keep Alive，见 [[05-Communication/06-以太网与TCP-IP/005-嵌入式网络应用协议|嵌入式网络应用协议]]）。

重连策略采用指数退避并设上限，例如 1 s、2 s、4 s、8 s、上限 30~60 s，避免服务器故障时大量设备同时重连造成冲击。重连前应关闭旧 socket 并释放资源，重复 `socket` 而不 `close` 是 PCB 泄漏的常见来源。若设备有非易失配置，应记录断线次数用于现场诊断。

## 6. 字节序与结构体布局

网络字节序为大端。所有超过一个字节的协议字段在写入报文前都要转换：

- `htons`/`ntohs` 用于 16 位（端口、长度、类型）；
- `htonl`/`ntohl` 用于 32 位（IPv4 地址、序列号、事务标识）；
- IP 地址在 `struct in_addr` 中按网络字节序存储，用字符串转换时用 `inet_addr`/`inet_pton` 而不要手工拼接；
- 单字节字段（如 MQTT 的报文类型与标志、Modbus 的功能码）无需转换。

结构体不能直接强转成报文字节流：编译器会插入填充字节导致布局与协议不一致。必须打包时使用 `__attribute__((packed))` 或 `#pragma pack(1)`，但打包结构访问未对齐成员在部分架构上会触发异常或性能下降，更稳妥的做法是按字段逐个序列化到字节数组。跨平台协议实现中，位域（bitfield）的字节序与分配方向由编译器决定，禁止用于报文布局。

Modbus TCP 的 MBAP 头、MQTT 的可变长度字段等具体打包格式见 [[05-Communication/06-以太网与TCP-IP/005-嵌入式网络应用协议|嵌入式网络应用协议]]；底层缓冲与连接池配置见 [[05-Communication/06-以太网与TCP-IP/003-lwIP移植与配置|lwIP 移植与配置]]。
