#include <Wire.h>

#define ADXL345_ADDR 0x53

// 2kHz = 500マイクロ秒
const unsigned long INTERVAL_US = 500;
unsigned long prev_us = 0;

// 送信パケット構造体（計9バイト）
// ヘッダ 2バイト + int16_t (2バイト × 3軸) + フッタ 1バイト
struct __attribute__((packed)) AccelPacket {
    uint8_t header1; // 0xAA
    uint8_t header2; // 0x55
    int16_t x;
    int16_t y;
    int16_t z;
    uint8_t tail;    // 0x0A ('\n')
};

AccelPacket packet;

void writeRegister(uint8_t reg, uint8_t val) {
    Wire.beginTransmission(ADXL345_ADDR);
    Wire.write(reg);
    Wire.write(val);
    Wire.endTransmission();
}

void setup() {
    // 500,000 bps（2kHzバイナリ転送に十分な帯域）
    Serial.begin(500000);

    Wire.begin();
    Wire.setClock(400000); // 400kHz Fast Mode

    // パケット固定値の初期化
    packet.header1 = 0xAA;
    packet.header2 = 0x55;
    packet.tail = 0x0A;

    // 1. スタンバイ解除・測定モード開始 (POWER_CTL)
    writeRegister(0x2D, 0x08);

    // 2. 出力データレートを 3200Hz に設定 (BW_RATE: 0x0F = 3200Hz)
    writeRegister(0x2C, 0x0F);

    // 3. レンジ・分解能設定 (DATA_FORMAT: フル分解能, ±16g, 4mg/LSB)
    writeRegister(0x31, 0x0B);

    prev_us = micros();
}

void loop() {
    unsigned long current_us = micros();

    // 500μs (2kHz) 周期で実行
    if (current_us - prev_us >= INTERVAL_US) {
        prev_us += INTERVAL_US;

        // X, Y, Z 軸（計6バイト）のバーストリード
        Wire.beginTransmission(ADXL345_ADDR);
        Wire.write(0x32); // DATAX0
        Wire.endTransmission(false);

        Wire.requestFrom((uint8_t)ADXL345_ADDR, (uint8_t)6);
        if (Wire.available() >= 6) {
            packet.x = (int16_t)(Wire.read() | (Wire.read() << 8));
            packet.y = (int16_t)(Wire.read() | (Wire.read() << 8));
            packet.z = (int16_t)(Wire.read() | (Wire.read() << 8));

            // バイナリ一括送信（9バイト）
            Serial.write((uint8_t*)&packet, sizeof(AccelPacket));
        }
    }
}