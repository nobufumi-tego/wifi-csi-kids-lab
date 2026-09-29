// csi_rx: the receiver "R" / 受信機「R」
//
// Listens on Wi-Fi channel 11 for packets from csi_tx and prints the CSI of each
// one as a text line over USB (921600 bits per second):
//
//   CSI,<time_us>,<rssi_dbm>,<amp sc-28>,...,<amp sc-1>,<amp sc1>,...,<amp sc28>
//
// "amp" = amplitude (size) of the wave on each subcarrier. Lines starting with "#"
// are messages for people. On the PC run:  uv run csi-lab capture --label empty
// 送信機のパケットを受けるたびに、56 本のサブキャリアの振幅を 1 行で PC に送る。
//
// LED (GPIO2, if your board has one): blinks once per second while receiving.
// Board: "ESP32 Dev Module" (Arduino IDE, "esp32 by Espressif Systems").

#include <WiFi.h>
#include <esp_arduino_version.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include <math.h>

// ---- settings (must match csi_tx) / 設定（送信機と同じにする） ----
const uint8_t WIFI_CHANNEL = 11;
const uint32_t MAGIC = 0x4B495343;       // "CSIK"
const uint32_t SERIAL_BAUD = 921600;     // 100 lines/s x ~300 characters needs a fast link
const uint8_t LED_PIN = 2;
const uint32_t LINES_PER_BLINK = 100;
const uint32_t BLINK_MS = 60;
const uint32_t STATUS_EVERY_MS = 5000;   // print a status message this often

// CSI layout from the ESP32: LLTF (64 subcarriers) then HT-LTF (64 subcarriers),
// each subcarrier = 2 bytes (imaginary, real). We use HT-LTF.
const int SUBCARRIERS_PER_LTF = 64;
const int BYTES_PER_SUBCARRIER = 2;
const int LTF_BYTES = SUBCARRIERS_PER_LTF * BYTES_PER_SUBCARRIER;  // 128
const int MAX_INDEX = 28;  // keep subcarriers -28..-1 and 1..28 (56 in total)
const int QUEUE_LENGTH = 32;

struct CsiRecord {
  uint32_t time_us;
  int8_t rssi_dbm;
  int8_t buf[LTF_BYTES];
};

QueueHandle_t queue;
uint8_t txMac[6];
volatile bool txKnown = false;   // becomes true after the first packet from csi_tx
volatile uint32_t dropped = 0;   // records lost because the queue was full
volatile uint32_t others = 0;    // CSI from other devices (ignored)
uint32_t printed = 0;
uint32_t ledOffMs = 0;
uint32_t lastStatusMs = 0;

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

// Called by ESP-NOW for each received packet: remember who csi_tx is.
void rememberSender(const uint8_t *mac, const uint8_t *data, int len) {
  if (txKnown || len < (int)sizeof(uint32_t)) return;
  uint32_t magic;
  memcpy(&magic, data, sizeof(magic));
  if (magic != MAGIC) return;
  memcpy(txMac, mac, 6);
  txKnown = true;
}

// Called by Wi-Fi for each packet's CSI. Keep it short: copy and hand over.
void onCsi(void *ctx, wifi_csi_info_t *info) {
  if (!info || !info->buf || !txKnown) return;
  if (memcmp(info->mac, txMac, 6) != 0) {
    others++;
    return;
  }
  if (info->len < 2 * LTF_BYTES) return;  // no HT-LTF part (not an 802.11n packet)
  CsiRecord rec;
  rec.time_us = info->rx_ctrl.timestamp;
  rec.rssi_dbm = info->rx_ctrl.rssi;
  memcpy(rec.buf, info->buf + LTF_BYTES, LTF_BYTES);
  if (xQueueSend(queue, &rec, 0) != pdTRUE) dropped++;
}

// Position in the ESP32 buffer for subcarrier k: 0..31 first, then -32..-1.
int positionOf(int k) { return k >= 0 ? k : k + SUBCARRIERS_PER_LTF; }

void printRecord(const CsiRecord &rec) {
  static char line[700];
  int n = snprintf(line, sizeof(line), "CSI,%lu,%d", (unsigned long)rec.time_us, rec.rssi_dbm);
  for (int k = -MAX_INDEX; k <= MAX_INDEX; k++) {
    if (k == 0) continue;  // the center subcarrier carries nothing
    const int p = positionOf(k) * BYTES_PER_SUBCARRIER;
    const float im = rec.buf[p];
    const float re = rec.buf[p + 1];
    n += snprintf(line + n, sizeof(line) - n, ",%.1f", sqrtf(re * re + im * im));
  }
  line[n++] = '\n';
  Serial.write(reinterpret_cast<const uint8_t *>(line), n);
}

void setup() {
  Serial.begin(SERIAL_BAUD);
  pinMode(LED_PIN, OUTPUT);
  queue = xQueueCreate(QUEUE_LENGTH, sizeof(CsiRecord));
  if (queue == nullptr) fail("queue", ESP_ERR_NO_MEM);

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  check(esp_wifi_set_ps(WIFI_PS_NONE), "power save off");
  check(esp_wifi_set_country_code("JP", false), "country code");
  check(esp_wifi_set_promiscuous(true), "promiscuous on");
  check(esp_wifi_set_channel(WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE), "set channel");

  wifi_csi_config_t csi = {};
  csi.lltf_en = true;
  csi.htltf_en = true;
  csi.stbc_htltf2_en = false;
  csi.ltf_merge_en = false;       // keep LLTF and HT-LTF separate
  csi.channel_filter_en = false;  // do not smooth neighboring subcarriers
  csi.manu_scale = false;         // automatic scaling (see "automatic gain" in the lessons)
  csi.shift = 0;
  check(esp_wifi_set_csi_config(&csi), "csi config");
  check(esp_wifi_set_csi_rx_cb(onCsi, nullptr), "csi callback");
  check(esp_wifi_set_csi(true), "csi on");

  check(esp_now_init(), "esp_now_init");
  // The callback's form changed in Arduino-ESP32 version 3, so we write both.
  // (Written as lambdas so the Arduino IDE does not mix up the two versions.)
#if ESP_ARDUINO_VERSION_MAJOR >= 3
  check(esp_now_register_recv_cb([](const esp_now_recv_info_t *info, const uint8_t *data,
                                    int len) { rememberSender(info->src_addr, data, len); }),
        "receive callback");
#else
  check(esp_now_register_recv_cb([](const uint8_t *mac, const uint8_t *data, int len) {
          rememberSender(mac, data, len);
        }),
        "receive callback");
#endif

  Serial.printf("# csi_rx ready: channel %u, waiting for csi_tx...\n", WIFI_CHANNEL);
}

void loop() {
  CsiRecord rec;
  if (xQueueReceive(queue, &rec, pdMS_TO_TICKS(100)) == pdTRUE) {
    printRecord(rec);
    printed++;
    if (printed % LINES_PER_BLINK == 0) {
      digitalWrite(LED_PIN, HIGH);
      ledOffMs = millis() + BLINK_MS;
    }
  }
  const uint32_t now = millis();
  if (ledOffMs != 0 && (int32_t)(now - ledOffMs) >= 0) {
    digitalWrite(LED_PIN, LOW);
    ledOffMs = 0;
  }
  if (now - lastStatusMs >= STATUS_EVERY_MS) {
    lastStatusMs = now;
    if (!txKnown) {
      Serial.println("# still waiting for csi_tx (is it powered on? same channel?)");
    } else {
      Serial.printf("# printed %lu, dropped %lu, other devices %lu\n", (unsigned long)printed,
                    (unsigned long)dropped, (unsigned long)others);
    }
  }
}
