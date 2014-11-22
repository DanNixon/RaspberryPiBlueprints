DROP TABLE IF EXISTS weather_history;
CREATE TABLE weather_history (
  id INTEGER primary KEY AUTOINCREMENT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  wind_direction TEX NOT NULL,
  average_wind_speed REAL NOT NULL,
  peak_wind_speed REAL NOT NULL,
  rain_frequency REAL NOT NULL,
  light_level REAL NOT NULL,
  temperature REAL NOT NULL,
  humidity REAL NOT NULL,
  pressure REAL NOT NULL
);
