import os
from datetime import datetime
from keiba_machine_learning.models import RaceTrac, TrackKind, TrackDirection, TrackSurface, Weather
from keiba_machine_learning.netkeiba.scrapers import RaceInformationScraper
from keiba_machine_learning.netkeiba.constants import ENCODING_OF_WEB_PAGE

base_path = os.path.dirname(os.path.abspath(__file__))


def test_to_scrape_race_information():
    file_path = os.path.normpath(os.path.join(
        base_path, "./fixtures/201901010101.html"))

    with open(file_path, mode="r", encoding=ENCODING_OF_WEB_PAGE) as file:
        expect_data = {
            'title': '2歳未勝利',
            'race_track': RaceTrac.SAPPORO,
            'track_kind': TrackKind.GRASS,
            'track_direction': TrackDirection.RIGHT,
            'race_distance_by_meter': 1800,
            'track_surface': TrackSurface.GOOD_TO_FIRM,
            'weather': Weather.CLOUD,
            'race_number': 1,
            'starts_at': datetime(2019, 7, 27, 9, 50),
        }
        assert RaceInformationScraper.scrape(file) == expect_data
