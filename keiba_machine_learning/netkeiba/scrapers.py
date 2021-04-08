import re
from datetime import datetime
from typing import IO, TypedDict
from bs4 import BeautifulSoup
from keiba_machine_learning.models import RaceTrac, TrackKind, TrackDirection, TrackSurface, Weather, RaceTracFactory, TrackKindFactory, TrackDirectionFactory, TrackSurfaceFactory, WeatherFactory

# NOTE: バージョニングは必要に応じて行う
# 例えばスクレイピング先がリニューアルされてDOMががらりと変わってしまったらこのスクリプトは使えなくなる
# その場合、コード自体は残しておいてリニューアルされたサイトに対応するものは新しいバージョンで実装を行う
# その際に名前空間も切る
# (YAGNIの原則に則って今の段階では作らない)


class RaceInformation(TypedDict):
    title: str
    race_track: RaceTrac
    track_kind: TrackKind
    track_direction: TrackDirection
    race_distance_by_meter: int
    track_surface: TrackSurface
    weather: Weather
    race_number: int
    starts_at: datetime


class RaceInformationScraper:
    @staticmethod
    def scrape(file: IO) -> RaceInformation:
        soup = BeautifulSoup(file, 'html.parser')

        title_element = soup.select_one(
            '#main > div > div > div > diary_snap > div > div > dl > dd > h1')
        text_under_the_title = soup.select_one(
            '#main > div > div > div > diary_snap > div > div > dl > dd > p > diary_snap_cut > span').get_text()
        race_number_element = soup.select_one(
            '#main > div > div > div > diary_snap > div > div > dl > dt')

        race_distance_by_meter = int(
            re.search(r'(\d{4})m', text_under_the_title).group(1))
        race_number = int(
            re.search(r'\d+', race_number_element.get_text()).group())
        race_track_name = soup.select_one(
            '#main > div > div > div > ul > li > a.active').get_text()
        track_kind_mark = text_under_the_title[0]
        track_direction_mark = text_under_the_title[1]
        track_surface_mark = re.search(
            r'{} : (\w+)'.format(track_kind_mark), text_under_the_title).group(1)
        weather_mark = re.search(r'天候 : (\w+)', text_under_the_title).group(1)

        return {
            'title': title_element.get_text(),
            'race_track': RaceTracFactory.create(race_track_name),
            'track_kind': TrackKindFactory.create(track_kind_mark),
            'track_direction': TrackDirectionFactory.create(track_direction_mark),
            'race_distance_by_meter': race_distance_by_meter,
            'track_surface': TrackSurfaceFactory.create(track_surface_mark),
            'weather': WeatherFactory.create(weather_mark),
            'race_number': race_number,
            'starts_at': datetime(2019, 7, 27, 9, 50),
        }
