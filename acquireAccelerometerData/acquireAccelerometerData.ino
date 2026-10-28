#include <Wire.h>
#include "MMA7660.h"

MMA7660 accelemeter;

// 100Hz = 10,000μs (10ms)
// 120Hz = 8,300μs
const unsigned long INTERVAL_US = 8700;
unsigned long prev_us = 0;

void setup() {
    Serial.begin(115200);

    Wire.begin();
    Wire.setClock(400000); // 400kHz

    accelemeter.init();
    accelemeter.setMode(MMA7660_STAND_BY);
    accelemeter.setSampleRate(AUTO_SLEEP_120); // センサ更新は120Hz
    accelemeter.setMode(MMA7660_ACTIVE);

    prev_us = micros();
}

void loop() {
    unsigned long current_us = micros();

    // 10ms経過するごとに1回だけ取得・送信
    if (current_us - prev_us >= INTERVAL_US) {
        prev_us += INTERVAL_US;

        float ax, ay, az;
        accelemeter.getAcceleration(&ax, &ay, &az);

        Serial.print(ax, 3);
        Serial.print(',');
        Serial.print(ay, 3);
        Serial.print(',');
        Serial.println(az, 3);
    }
}