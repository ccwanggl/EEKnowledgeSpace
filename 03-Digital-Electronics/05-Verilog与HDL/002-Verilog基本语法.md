---
tags: [fpga, verilog, hdl, digital]
date-created: 2026-06-15
---

# Verilog 基本语法

## 模块定义
```verilog
module adder(
    input  [3:0] a, b,
    input        cin,
    output [3:0] sum,
    output       cout
);
    assign {cout, sum} = a + b + cin;
endmodule
```

### 数据类型
- `wire`：导线，组合逻辑输出，必须持续驱动
- `reg`：寄存器，时序逻辑输出（不一定对应物理寄存器！）
- `input/output/inout`：端口方向
- `[N:0]`：位宽，如 `[7:0]` 表示 8 位

### 数字表示
- `4'b1010`：4 位二进制
- `8'hFF`：8 位十六进制
- `16'd255`：16 位十进制
- `1'b0`、`1'b1`、`1'bz`（高阻）、`1'bx`（未知）

### 运算符
- 算术：`+`、`-`、`*`、`/`、`%`
- 位运算：`&`、`|`、`^`、`~`
- 逻辑：`&&`、`||`、`!`
- 比较：`==`、`!=`、`>`、`<`、`>=`、`<=`
- 移位：`<<`、`>>`
- 拼接：`{a, b}`、`{4{a}}`（复制 4 次）
- 条件：`condition ? true_val : false_val`

---

