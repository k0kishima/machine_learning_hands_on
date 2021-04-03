import os
import time
import urllib.request
from tqdm import tqdm

from keiba_machine_learning.netkeiba.constants import RACE_DATA_DIR
from keiba_machine_learning.models.race import RaceTrac
from keiba_machine_learning.netkeiba.models.race import Race


os.makedirs(RACE_DATA_DIR, exist_ok=True)

YEAR = 2019

races = []
for race_track in RaceTrac:
    for series_number in range(1, Race.MAX_SERIES_NUMBER + 1):
        for day_number in range(1, Race.MAX_DAY_NUMBER + 1):
            for race_number in range(1, Race.MAX_RACE_NUMBER + 1):
                races.append(Race(year=YEAR, race_track=race_track,
                                  series_number=series_number, day_number=day_number, race_number=race_number))

for race in tqdm(races):
    if os.path.exists(race.file_path):
        continue
    else:
        urllib.request.urlretrieve(race.url, race.file_path)
        time.sleep(1)
