"""netkeibaからダウンロードしたHTMLからpandasのDataFrameを生成するスクリプト

    Examples:
        ※ 実行時はパスを通すこと
        ※ 事前にファイルが用意されていること(`./download_race_pages.py` が実行済みであること)
        ※ 以下はコマンドライン上にて

        source venv/bin/activate
        export PYTHONPATH=".:$PYTHONPATH"
        python scripts/netkeiba/create_race_result_data_frame.py
"""

import os
from tqdm import tqdm
import pandas as pd

from keiba_machine_learning.netkeiba.constants import RACE_DATA_DIR, ENCODING_OF_WEB_PAGE
from keiba_machine_learning.netkeiba.scrapers import RaceInformationScraper, RaceResultScraper, DataNotFound, IncompatibleDataDetected

race_records = []
for file_name in tqdm(os.listdir(RACE_DATA_DIR)):
    file_path = os.path.normpath(os.path.join(RACE_DATA_DIR, file_name))

    with open(file_path, mode="r", encoding=ENCODING_OF_WEB_PAGE) as file:
        try:
            race_id, _ = file_name.split('.')
            race_id = int(race_id)
        except ValueError:
            continue

        try:
            race_information = RaceInformationScraper.scrape(file)
            file.seek(0)

            rows = [{
                'race_id': race_id,
                'race_track': race_information['race_track'].value,
                'track_kind': race_information['track_kind'].value,
                'track_direction': race_information['track_direction'].value,
                'race_distance_by_meter': race_information['race_distance_by_meter'],
                'track_surface': race_information['track_surface'].value,
                'weather': race_information['weather'].value,
                'race_number': race_information['race_number'],
                'starts_at': race_information['starts_at'],
                'order_of_placing': race_record['order_of_placing'],
                'bracket_number': race_record['bracket_number'],
                'horse_number': race_record['horse_number'],
                'horse_id': race_record['horse_id'],
                'horse_name': race_record['horse_name'],
                'horse_age': race_record['horse_age'],
                'horse_gender': race_record['horse_gender'].value,
                'impost': race_record['impost'],
                'jockey_id': race_record['jockey_id'],
                'jockey_name': race_record['jockey_name'],
                'race_time': race_record['race_time'],
                'win_betting_ratio': race_record['win_betting_ratio'],
                'favorite_order': race_record['favorite_order'],
                'horse_weight': race_record['horse_weight'],
                'weight_change': race_record['weight_change'],
            } for race_record in RaceResultScraper.scrape(file)]

            race_records.extend(rows)
        except DataNotFound:
            pass
        except IncompatibleDataDetected:
            pass
        except Exception as e:
            print(f"race_id: {race_id} can't parse.")
            raise e


df = pd.DataFrame([], columns=race_records[0].keys())
df = pd.concat([df, pd.DataFrame.from_dict(race_records)])
df.to_pickle(os.path.normpath(os.path.join(
    RACE_DATA_DIR, 'race_results_data_frame.pickle')))
