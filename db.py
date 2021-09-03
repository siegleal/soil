import sqlite3 as sl
import pandas

def create_db():
  con = sl.connect('test.db')
  with con:
    con.execute("""
      CREATE TABLE IF NOT EXISTS soil (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        moisture INTEGER,
        temp REAL,
        plant TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    """)

def insert(temp, moisture, plant):
  con = sl.connect('test.db')
  with con:
    cur = con.cursor()
    cur.execute(f'INSERT INTO soil(moisture, temp, plant) VALUES({moisture}, {temp}, "{plant}")')

def read_plant(plant_name: str = None, limit: int = None):
  con = sl.connect('test.db')
  select = f'SELECT temp, moisture, plant, DATETIME(timestamp, "localtime") as timestamp  FROM soil'
  if plant_name:
    select = select + f' WHERE plant = "{plant_name}"'
  select = select + " ORDER BY timestamp"
  if limit:
    select = select + f' LIMIT {limit}'

  print(f'Select statement: {select}')

  with con:
    cur = con.cursor()
    cur.execute(select)
    rows = cur.fetchall()
    return rows

def get_plant_names():
    con = sl.connect('test.db')
    with con:
        statement = 'SELECT DISTINCT plant from soil;'
        cur = con.cursor()
        cur.execute(statement)
        names = cur.fetchall()
        names_list = [d[0] for d in names]
        print(names_list)
        return names_list

def get_last_24hours(plant: str):
  con = sl.connect('test.db')
  with con:
    cur = con.cursor()
    cur.execute(f'SELECT temp, moisture, DATETIME(timestamp, "localtime") as local_timestamp FROM soil WHERE plant = "{plant}" AND local_timestamp >= DATETIME("now", "-1 days")', con)
    return cur.fetchall()


def get_moisture_sma(plant: str):
  con = sl.connect('test.db')
  with con:
    dataframe = pandas.read_sql_query(f'SELECT moisture, DATETIME(timestamp, "localtime") as timestamp FROM soil WHERE plant = "{plant}"', con)
    dataframe['sma'] = dataframe.rolling(6, center= True, axis = 0, min_periods=1).mean()
    return_values = [{"sma": row.sma, "timestamp": row.timestamp} for index, row in dataframe.iterrows()]
    return return_values

if __name__ == '__main__':
  create_db()
