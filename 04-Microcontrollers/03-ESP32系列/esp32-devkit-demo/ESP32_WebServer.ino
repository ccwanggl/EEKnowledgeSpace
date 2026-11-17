/*
 * ESP32 交互式 Web 控制台 Demo
 * ------------------------------------------
 * 功能：
 *   1. STA 模式连接路由器，启动 Web 服务器（端口 80）
 *   2. 浏览器打开网页 → 实时开关 LED（GPIO2 板载蓝灯）
 *   3. 每 2 秒刷新 ADC 电压 / WiFi 信号强度 / 芯片温度
 *   4. mDNS：访问 http://esp32-devkit.local 免记 IP
 *
 * 硬件：通用 ESP32 DevKit（ESP32-WROOM-32 模组，
 *       USB 转串口 CP2102 / CH340 / CH9102，MICRO 或 TYPE-C 口）
 *
 * 【Arduino IDE 设置】
 *   板型：ESP32 Dev Module（espressif 官方 esp32 by Espressif Systems ≥ 2.x/3.x）
 *   USB 驱动：按板上实际桥接芯片装
 *     - CP2102 → Silicon Labs CP210x VCP 驱动
 *     - CH340  → Win10+ 一般免驱，设备管理器出现 COM 口即可
 *     - CH9102 → 沁恒 CH343/CH9102 驱动（设备管理器若显示"未知设备"必装）
 *   烧录方式：自动下载电路，直接点"上传"即可；
 *             若卡在 "Connecting...."，按住 BOOT 键点上传，
 *             出现 Connecting 后松开 BOOT。
 *
 * 【板载 LED】GPIO2 蓝色灯，低电平点亮。
 *             烧录后启动时会先闪 3 下确认引脚正确。
 *
 * 【与 ESP8266 版的差异】
 *   WiFi 库     ESP8266WiFi.h      → WiFi.h
 *   Web 库      ESP8266WebServer.h → WebServer.h
 *   mDNS 库     ESP8266mDNS.h      → ESPmDNS.h（注意 loop 里不需要 MDNS.update()）
 *   ADC        单通道 10bit       → 多通道 12bit（本例用 GPIO34，仅输入脚）
 *   ADC 电压   需外部分压换算     → 默认 12dB 衰减，约 0~3.3V 满量程
 */

#include <WiFi.h>
#include <WebServer.h>
#include <ESPmDNS.h>

// ============ 1. 修改为你的路由器 ============
const char* WIFI_SSID = "YourWiFi_SSID";
const char* WIFI_PASS = "YourWiFi_Password";

WebServer server(80);
const int LED_PIN = 2;                 // 内置 LED
const int ADC_PIN = 34;                // GPIO34：仅输入，ADC1_CH6，安全又好用
bool ledOn = false;                    // true = 灯亮（GPIO2 低电平点亮）

// ============ 2. 网页（烧录进 Flash，无需外置文件） ============
const char INDEX_HTML[] PROGMEM = R"rawliteral(<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ESP32 控制台</title>
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
<h1>🎛️ ESP32 Web 控制台</h1>

<div class="card" style="text-align:center">
  <div id="led"></div>
  <button onclick="toggle()">切换 LED</button>
</div>

<div class="card">
  <div class="row"><span>ADC 原始值</span><span class="val" id="adc">--</span></div>
  <div class="row"><span>电压（GPIO34）</span><span class="val" id="volt">--</span></div>
  <div class="row"><span>WiFi 信号</span><span class="val" id="rssi">--</span></div>
  <div class="row"><span>芯片温度</span><span class="val" id="temp">--</span></div>
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
  document.getElementById('volt').textContent = d.volt.toFixed(3) + ' V';
  document.getElementById('rssi').textContent = d.rssi + ' dBm';
  document.getElementById('temp').textContent = d.temp.toFixed(1) + ' ℃';
  document.getElementById('ip').textContent   = d.ip;
  document.getElementById('barfill').style.width =
      Math.min(100, Math.max(0, (d.rssi+90)/50*100)) + '%';
}
poll();
</script>
</body></html>)rawliteral";

// ============ 3. API：状态查询 / LED 控制 ============
void handleStatus() {
  int raw = analogRead(ADC_PIN);
  String json = "{";
  json += "\"led\":"  + String(ledOn ? 1 : 0);
  json += ",\"adc\":" + String(raw);
  json += ",\"volt\":" + String(raw * 3.3 / 4095.0);   // 12bit 满量程 3.3V
  json += ",\"rssi\":" + String(WiFi.RSSI());
  json += ",\"temp\":" + String(temperatureRead(), 1);    // 片上温度传感器
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
  analogReadResolution(12);                    // ADC 12bit（0~4095）
  analogSetPinAttenuation(ADC_PIN, ADC_11db);  // 衰减到约 0~3.3V 量程

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

  if (MDNS.begin("esp32-devkit")) {
    Serial.println("mDNS: http://esp32-devkit.local");
  }
}

void loop() {
  server.handleClient();
}
