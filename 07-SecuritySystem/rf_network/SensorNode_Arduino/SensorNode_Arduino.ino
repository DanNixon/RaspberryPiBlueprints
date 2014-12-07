#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>

#define SERIAL_BAUD 115200

RF24 radio(9, 10);
RF24Network network(radio);

const uint16_t CHANNEL = 90;
const uint16_t THIS_NODE_ADDR = 01;
const uint16_t BASE_NODE_ADDR = 00;

struct payload_t
{
  char topic[10];
  uint8_t state;
};

void setup(void)
{
  Serial.begin(SERIAL_BAUD);

  SPI.begin();
  radio.begin();
  network.begin(CHANNEL, THIS_NODE_ADDR);
}

//TODO: Temp
unsigned long last_sent;
uint8_t last_state = 0;

void loop()
{
  network.update();

  unsigned long now = millis();
  if(now - last_sent >= 2000)
  {
    last_sent = now;
    last_state = !last_state;

    Serial.print("Sending...");

    payload_t payload = { "test_s1", last_state };

    RF24NetworkHeader header(BASE_NODE_ADDR);
    bool ok = network.write(header, &payload, sizeof(payload));

    if (ok)
      Serial.println("ok.");
    else
      Serial.println("failed.");
  }
}
