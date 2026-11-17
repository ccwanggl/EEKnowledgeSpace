/*
 * ESP8266 交互式 Web 控制台 Demo
 * ------------------------------------------
 * 功能：
 *   1. STA 模式连接路由器，启动 Web 服务器（端口 80）
 *   2. 浏览器打开网页 → 实时开关 LED（GPIO2 内置 LED）
 *   3. 每 2 秒刷新 ADC 电压 / WiFi 信号强度
 *   4. mDNS：访问 http://esp8266-demo.local 免记 IP
 *
 * 硬件：ESP-12F 模组的通用开发板（Taobao TYPE-C 版，CH340 转串口）
 *
 * 【Arduino IDE 设置】
 *   首选板型：NodeMCU 1.0 (ESP-12E Module)   ← ESP-12F 与 ESP-12E 引脚兼容
 *   若上传失败改选：Generic ESP8266 Module
 *                  Flash Mode: DIO / Flash Size: 4MB(32Mb)
 *   USB 驱动：设备管理器出现 CH340/CH341 串口即装好了（Win10+ 一般免驱）
 *   烧录方式：这类板子有自动下载电路，直接点"上传"即可，无需按按钮；
 *             若卡在 "connecting...."，按住板上的 FLASH 键再复位，或
 *             按住 FLASH 键点上传，出现 connecting 后松开。
 *
 * 【板载 LED】ESP-12F 模组的蓝色灯在 GPIO2，低电平点亮。
 *             烧录后启动时会先闪 3 下——若灯不闪，把下面 LED_PIN 改成 16 再试。
 */

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

// ============ 1. 修改为你的路由器 ============
const char* WIFI_SSID = "YourWiFi_SSID";
const char* WIFI_PASS = "YourWiFi_Password";

ESP8266WebServer server(80);
const int LED_PIN = 2;                 // 内置 LED
bool ledOn = false;                    // true = 灯亮（GPIO2 低电平点亮）

// ============ 2. 网页（烧录进 Flash，无需外置文件） ============
const char INDEX_HTML[] PROGMEM = R"rawliteral(<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ESP8266 控制台</title>
<style>
  body{font-family:system-ui;background:#0f172a;color:#e2e8f0;
       max-width:520px;margin:0 auto;padding:24px}
  h1{font-size:20px} .card{background:#1e293b;border-radius:12px;
       padding:20px;margin:16px 0}
  #led{width:64px;height:64px;border-radius:50%;margin:0 auto 12px;
       background:#334155;transition:.15s}
  #led.on{background:#facc15;box-shadow:0 0 32px #facc1555}
  button{width:100%;padding:14px;font-size:16px;border:none;
       border-radius:10px;background:#3b82f6;color:#fff;cursor:pointer}
  button:active{transform:scale(.97)}
  .row{display:flex;justify-content:space-between;padding:8px 0;
       border-bottom:1px solid #334155}
  .val{font-variant-numeric:tabular-nums;color:#38bdf8}
  #bar{height:8px;background:#334155;border-radius:4px;overflow:hidden}
  #bar i{display:block;height:100%;width:50%;background:#22c55e}
</style>
</head>
<body>
<h1>🎛️ ESP8266 Web 控制台</h1>

<div class="card" style="text-align:center">
  <div id="led"></div>
  <button onclick="toggle()">切换 LED</button>
</div>

<div class="card">
  <div class="row"><span>ADC 原始值</span><span class="val" id="adc">--</span></div>
  <div class="row"><span>电压（A0）</span><span class="val" id="volt">--</span></div>
  <div class="row"><span>WiFi 信号</span><span class="val" id="rssi">--</span></div>
  <div class="row"><span>IP 地址</span><span class="val" id="ip">--</span></div>
  <div id="bar" style="margin-top:12px"><i id="barfill"></i></div>
</div>

<script>
// 开关 LED：写操作，立即返回最新状态
function toggle(){
  fetch('/api/led?on=' + (ledState?0:1), {method:'POST'})
    .then(r=>r.json()).then(apply);
}
// 轮询状态：每 2 秒一次（GET 幂等，轻量）
setInterval(poll, 2000);
function poll(){ fetch('/api/status').then(r=>r.json()).then(apply); }
let ledState = false;
function apply(d){
  ledState = d.led;
  document.getElementById('led').className = d.led ? 'on' : '';
  document.getElementById('adc').textContent  = d.adc;
  document.getElementById('volt').textContent   = d.volt.toFixed(3) + ' V';
  document.getElementById('rssi').textContent   = d.rssi + ' dBm';
  document.getElementById('ip').textContent     = d.ip;
  document.getElementById('barfill').style.width =
      Math.min(100, Math.max(0, (d.rssi+90)/50*100)) + '%';
}
poll();
</script>
</body></html>)rawliteral";

// ============ 3. API：状态查询 / LED 控制 ============
void handleStatus() {
  int raw = analogRead(A0);
  String json = "{";
  json += "\"led\":"  + String(ledOn ? 1 : 0);
  json += ",\"adc\":" + String(raw);
  json += ",\"volt\":" + String(raw * 3.3 / 1023.0);   // NodeMCU A0 已带分压
  json += ",\"rssi\":" + String(WiFi.RSSI());
  json += ",\"ip\":\"" + WiFi.localIP().toString() + "\"";
  json += "}";
  server.send(200, "application/json", json);
}

void handleLed() {
  if (server.hasArg("on")) {
    ledOn = (server.arg("on") == "1");
    digitalWrite(LED_PIN, ledOn ? LOW : HIGH);   // 低电平点亮
  }
  handleStatus();
}

// ============ 4. 启动流程 ============
void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);                 // 初始熄灭

  // 上电自检：LED 闪 3 下（约 1.5s），确认引脚选对了
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, LOW);  delay(150);
    digitalWrite(LED_PIN, HIGH); delay(350);
  }

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.printf("\n连接 WiFi: %s ", WIFI_SSID);
  while (WiFi.status() != WL_CONNECTED) {
    delay(400); Serial.print('.');
  }
  Serial.printf("\n已连接，IP = %s\n", WiFi.localIP().toString().c_str());

  server.on("/",        HTTP_GET,  []() {
    server.send_P(200, "text/html", INDEX_HTML);
  });
  server.on("/api/status", HTTP_GET,  handleStatus);
  server.on("/api/led",    HTTP_POST, handleLed);
  server.begin();
  Serial.println("HTTP 服务器已启动 (端口 80)");

  if (MDNS.begin("esp8266-demo")) {
    Serial.println("mDNS: http://esp8266-demo.local");
  }
}

void loop() {
  server.handleClient();
  MDNS.update();
}
