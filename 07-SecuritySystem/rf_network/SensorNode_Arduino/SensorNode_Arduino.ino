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
// This node address, ensure this is valid for your network topology
const uint16_t THIS_NODE_ADDR = 02;

/**
 * The data that is sent in a single RF message.
 */
struct payload_t
{
  char topic[10];
  uint8_t state;
};

/**
 * Configuration data for a signle sensor on a node.
 */
struct sensor_t
{
  char topic[10];
  uint8_t pin;
  uint8_t active_low;
  uint8_t pull_up;
};

// Number of sensors on this node
const uint8_t NUM_SENSORS = 3;

// Configuration for this node's sensors
sensor_t sensors[NUM_SENSORS] =
{
  {"s1", 2, 1, 1},
  {"s2", 3, 0, 1},
  {"s3", 4, 1, 1}
};

// Array to hold the last recorded values for each sensor
uint8_t last_sensor_states[NUM_SENSORS];

void setup(void)
{
  // Start the serial port
  Serial.begin(SERIAL_BAUD);

  // Start the RF node and network
  SPI.begin();
  radio.begin();
  network.begin(CHANNEL, THIS_NODE_ADDR);

  // Setup the sensor IO
  for(uint8_t i = 0; i < NUM_SENSORS; i++)
  {
    uint8_t pin = sensors[i].pin;
    if(sensors[i].pull_up)
      pinMode(pin, INPUT_PULLUP);
    else
      pinMode(pin, INPUT);

    last_sensor_states[i] = 0;
  }
}

void loop()
{
  // Pump the network
  network.update();

  // Check sensor states
  for(uint8_t i = 0; i < NUM_SENSORS; i++)
  {
    // Get a reading
    uint8_t state = digitalRead(sensors[i].pin);

    // If the state has changed
    if(state != last_sensor_states[i])
    {
      // Record the new reading
      last_sensor_states[i] = state;

      // Invert it if signal is active low
      if(sensors[i].active_low)
        state = !state;

      // Build an RF packet payload
      payload_t payload;
      memcpy(payload.topic, sensors[i].topic, 10);
      payload.state = state;
      RF24NetworkHeader header(BASE_NODE_ADDR);

      // And send it
      bool ok = network.write(header, &payload, sizeof(payload));

      // If it failed to send then give a warning on serial port
      if(!ok)
        Serial.println("RF transmit failed.");
    }
  }
}
