"""netkeibaからレースファイルをダウンロードするスクリプト

    例えば以下のURLのようなものがレースファイルである
    https://db.netkeiba.com/race/201901010101

    このスクリプトでは指定された年のレースのファイルを全てダウンロードする

    netkeiba側の仕様でレースデータが存在しないページにアクセスしても404をHTTPステータスコードとしてレスポンスしないので、
    ここでは内容を気にせず保存を行う
    (データが存在しないことによる異常の処理はパーサーの責務とする)


    Args:
        year (int): コマンドライン引数としてダウンロード対象とするレースが開催された年を指定する

    Examples:
        ※ 実行時はパスを通すこと
        ※ 以下はコマンドライン上にて

        source venv/bin/activate
        export PYTHONPATH=".:$PYTHONPATH"
        python scripts/netkeiba/download_race_pages.py 2019
"""
import os
import time
import sys
import urllib.request
from tqdm import tqdm

from keiba_machine_learning.netkeiba.constants import RACE_DATA_DIR
from keiba_machine_learning.models.race import RaceTrac
from keiba_machine_learning.netkeiba.models.race import Race


os.makedirs(RACE_DATA_DIR, exist_ok=True)

args = sys.argv
YEAR = int(args[1])

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
