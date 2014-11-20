/*
 * Maplin Weather Instrument Driver
 */

#define SERIAL_BAUD 115200

const uint8_t windSpeedHalfRevolutionsThreshold = 10;
const uint16_t windDirectionLevels[] = {930, 830, 735, 390, 75, 135, 235, 560};
const uint16_t windDirectionTolerance = 50;

volatile bool rainFlag = false;
volatile uint16_t windSpeedHalfRevolutions = 0;
uint16_t windSpeedStartTime = 0;
uint8_t lastWindDirection = 0;

void setup()
{
  Serial.begin(SERIAL_BAUD);

  pinMode(2, INPUT_PULLUP);
  attachInterrupt(0, rainTrigger, FALLING);

  pinMode(3, INPUT_PULLUP);
  attachInterrupt(1, windSpeedTrigger, FALLING);

  windSpeedStartTime = millis();
}

void loop()
{
  if(rainFlag)
  {
    Serial.println("RAIN_DETECT;");

    rainFlag = false;
  }

  if(windSpeedHalfRevolutions > windSpeedHalfRevolutionsThreshold)
  {
    uint16_t deltaT = millis() - windSpeedStartTime;
    float windSpeedRPM = 30000.0 / ((deltaT / (float)windSpeedHalfRevolutionsThreshold));
    windSpeedStartTime = millis();
    windSpeedHalfRevolutions = 0;

    Serial.print("WIND_SPEED:RPM:");
    Serial.print(windSpeedRPM);
    Serial.println(";");
  }

  uint16_t wind_direction_reading = analogRead(0);
  int8_t windDirection = -1;
  for(int i = 0; i < 8; i++)
  {
    uint16_t rangeMin = windDirectionLevels[i] - windDirectionTolerance;
    uint16_t rangeMax = windDirectionLevels[i] + windDirectionTolerance;

    if(rangeMin < wind_direction_reading && rangeMax > wind_direction_reading)
    {
      windDirection = i;
      break;
    }
  }

  if(lastWindDirection != windDirection && windDirection != -1)
  {
    lastWindDirection = windDirection;

    Serial.print("WIND_DIRECTION:ARB:");
    Serial.print(windDirection);
    Serial.println(";");
  }
}

void rainTrigger()
{
  rainFlag = true;
}

void windSpeedTrigger()
{
  windSpeedHalfRevolutions++;
}
