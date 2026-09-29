// csi_tx: the transmitter "S" / 送信機「S」
//
// Sends a small ESP-NOW broadcast packet 100 times per second on Wi-Fi channel 11.
// The receiver (csi_rx) measures CSI from these packets.
// No router and no password are needed.
// ESP-NOW で 1 秒に 100 回、小さなパケットを送るだけのプログラム。ルーターもパスワードも不要。
//
// LED (GPIO2, if your board has one): blinks once per second while sending.
// Board: "ESP32 Dev Module" (Arduino IDE, "esp32 by Espressif Systems").

#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h>

// ---- settings (must match csi_rx) / 設定（受信機と同じにする） ----
const uint8_t WIFI_CHANNEL = 11;          // Wi-Fi channel (1-13 in Japan)
const uint32_t SEND_INTERVAL_MS = 10;     // 10 ms = 100 packets per second
const uint32_t MAGIC = 0x4B495343;        // "CSIK": marks packets from this project
const uint8_t LED_PIN = 2;                // built-in LED on many ESP32 boards
const uint32_t PACKETS_PER_BLINK = 100;   // blink once every 100 packets (1 s)
const uint32_t BLINK_MS = 60;             // how long the LED stays on
const uint32_t SERIAL_BAUD = 115200;      // for messages to the PC

const uint8_t BROADCAST[6] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

// What we send. The receiver checks "magic" to know the packet is ours.
struct __attribute__((packed)) Payload {
  uint32_t magic;
  uint32_t seq;  // counts up: 0, 1, 2, ...
};

uint32_t seq = 0;
uint32_t nextSendMs = 0;
uint32_t ledOffMs = 0;
uint32_t sendErrors = 0;

// Stop here and keep blinking fast if setup fails, printing why.
void fail(const char *what, esp_err_t err) {
  pinMode(LED_PIN, OUTPUT);
  while (true) {
    Serial.printf("# ERROR %s failed: %s\n", what, esp_err_to_name(err));
    for (int i = 0; i < 20; i++) {
      digitalWrite(LED_PIN, i % 2);
      delay(50);
    }
  }
}

void check(esp_err_t err, const char *what) {
  if (err != ESP_OK) fail(what, err);
}

void setup() {
  Serial.begin(SERIAL_BAUD);
  pinMode(LED_PIN, OUTPUT);

  WiFi.mode(WIFI_STA);  // turn Wi-Fi on without joining any network
  WiFi.disconnect();
  check(esp_wifi_set_ps(WIFI_PS_NONE), "power save off");
  check(esp_wifi_set_country_code("JP", false), "country code");
  check(esp_wifi_set_promiscuous(true), "promiscuous on");  // needed to change channel freely
  check(esp_wifi_set_channel(WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE), "set channel");
  check(esp_wifi_set_promiscuous(false), "promiscuous off");

  // Fixed 802.11n rate so the receiver gets the full CSI (and it does not change)
  check(esp_wifi_config_espnow_rate(WIFI_IF_STA, WIFI_PHY_RATE_MCS0_LGI), "set rate");
  check(esp_now_init(), "esp_now_init");

  esp_now_peer_info_t peer = {};
  memcpy(peer.peer_addr, BROADCAST, 6);
  peer.channel = WIFI_CHANNEL;
  peer.encrypt = false;
  check(esp_now_add_peer(&peer), "add peer");

  Serial.printf("# csi_tx ready: channel %u, %lu packets per second\n", WIFI_CHANNEL,
                (unsigned long)(1000 / SEND_INTERVAL_MS));
}

void loop() {
  const uint32_t now = millis();
  if ((int32_t)(now - nextSendMs) >= 0) {
    nextSendMs += SEND_INTERVAL_MS;
    if ((int32_t)(now - nextSendMs) > (int32_t)(10 * SEND_INTERVAL_MS)) {
      nextSendMs = now + SEND_INTERVAL_MS;  // we fell far behind; start again from now
    }
    Payload p = {MAGIC, seq};
    if (esp_now_send(BROADCAST, reinterpret_cast<const uint8_t *>(&p), sizeof(p)) != ESP_OK) {
      sendErrors++;
    }
    if (seq % PACKETS_PER_BLINK == 0) {
      digitalWrite(LED_PIN, HIGH);
      ledOffMs = now + BLINK_MS;
      Serial.printf("# sent %lu packets, %lu errors\n", (unsigned long)seq,
                    (unsigned long)sendErrors);
    }
    seq++;
  }
  if (ledOffMs != 0 && (int32_t)(now - ledOffMs) >= 0) {
    digitalWrite(LED_PIN, LOW);
    ledOffMs = 0;
  }
}
