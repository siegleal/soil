import db
from soil import Soil
import schedule
import time
import sys

soil = Soil()
plant_name = 'unknown'

def job():
  moisture, temp = soil.read()
  print(f'Writing {round(temp, 2)}, {moisture}')
  db.insert(temp, moisture, plant_name)


if __name__ == "__main__":
  plant_name = sys.argv[1]
  schedule.every(10).minutes.do(job)
  while True:
    schedule.run_pending()
    time.sleep(1)
