DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  walletaddress TEXT UNIQUE NOT NULL,
  minimumbalance INTEGER DEFAULT 0 NOT NULL,
  maximumbalance INTEGER DEFAULT 5000 NOT NULL,
  factor float DEFAULT 2.0
);