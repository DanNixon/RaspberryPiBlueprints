#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>
#include <printf.h>

#define SERIAL_BAUD 115200

// RF drivers
RF24 radio(9, 10);
RF24Network network(radio);

// RF channel, change this to get best coverage and reliability
const uint16_t CHANNEL = 90;
// Base node address, do not change this
const uint16_t BASE_NODE_ADDR = 00;

void setup(void)
{
  // Start the serial port
  printf_begin();
  Serial.begin(SERIAL_BAUD);

  // Start the RF node and network
  SPI.begin();
  radio.begin();
  network.begin(CHANNEL, BASE_NODE_ADDR);

  // Print some debug info
  radio.printDetails();
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
    char payload[14];
    network.read(header, payload, sizeof(payload));

    // Print it to serial port
    Serial.println(payload);
  }
}
