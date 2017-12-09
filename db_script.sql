CREATE TABLE    calendar(
  id            INTEGER PRIMARY KEY, 
  keylink       VARCHAR(16)
);
CREATE TABLE    event(
  id		INTEGER PRIMARY KEY,
  keylink       VARCHAR(16),
  name          VARCHAR(255), 
  color         VARCHAR(8),
  start         DATETIME,
  end           DATETIME
);
