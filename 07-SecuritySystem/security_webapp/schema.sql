DROP TABLE IF EXISTS sensors;
CREATE TABLE sensors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  location TEXT,
  description TEXT,
  mqtt_topic TEXT NOT NULL,
  trigger_text TEXT NOT NULL,
  CHECK(name <> ''), CHECK(mqtt_topic <> ''), CHECK(trigger_text <> '')
);

DROP TABLE IF EXISTS events;
CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sensor_id INTEGER DEFAULT -1 REFERENCES sensors(id) ON DELETE SET DEFAULT,
  'type' TEXT NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  CHECK('type' <> '')
);

DROP TABLE IF EXISTS alarms;
CREATE TABLE alarms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  alert_when TEXT NOT NULL,
  description TEXT,
  email TEXT NOT NULL,
  CHECK(name <> ''), CHECK(alert_when <> ''), CHECK(email <> '')
);

DROP TABLE IF EXISTS alarm_has_sensor;
CREATE TABLE alarm_has_sensor (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  alarm_id INTEGER REFERENCES alarms(id) ON DELETE CASCADE,
  sensor_id INTEGER REFERENCES sensors(id) ON DELETE CASCADE
);
