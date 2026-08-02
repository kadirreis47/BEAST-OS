
CREATE TABLE foods(
id TEXT PRIMARY KEY,
name TEXT NOT NULL,
category TEXT,
calories REAL,
protein REAL,
carbohydrate REAL,
fat REAL,
fiber REAL
);

CREATE TABLE recipes(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
calories REAL,
protein REAL
);
