#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>

#define SERIAL_BAUD 115200

RF24 radio(9, 10);
RF24Network network(radio);

const uint16_t CHANNEL = 90;
const uint16_t THIS_NODE_ADDR = 00;

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

void loop(void)
{
  network.update();

  while(network.available())
  {
    RF24NetworkHeader header;
    payload_t payload;
    network.read(header,&payload,sizeof(payload));

    Serial.print(payload.topic);
    Serial.print(":");
    Serial.println(payload.state);
  }
}
