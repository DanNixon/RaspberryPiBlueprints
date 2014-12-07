#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>

#define SERIAL_BAUD 115200

// RF drivers
RF24 radio(9, 10);
RF24Network network(radio);

// RF channel, change this to get best coverage and reliability
const uint16_t CHANNEL = 90;
// Base node address, do not change this
const uint16_t BASE_NODE_ADDR = 00;

/**
 * The data that is sent in a single RF message.
 */
struct payload_t
{
  char topic[10];
  uint8_t state;
};

void setup(void)
{
  // Start the serial port
  Serial.begin(SERIAL_BAUD);

  // Start the RF node and network
  SPI.begin();
  radio.begin();
  network.begin(CHANNEL, BASE_NODE_ADDR);
}

void loop(void)
{
  // Pump the network
  network.update();

  // Check for new messages
  while(network.available())
  {
    // Get the new message
    RF24NetworkHeader header;
    payload_t payload;
    network.read(header, &payload, sizeof(payload));

    // Print it to serial port
    Serial.print(payload.topic);
    Serial.print(":");
    Serial.print(payload.state);
    Serial.println(";");
  }
}
