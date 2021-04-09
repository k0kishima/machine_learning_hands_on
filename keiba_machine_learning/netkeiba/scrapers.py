import re
from datetime import datetime
from typing import IO, TypedDict
from bs4 import BeautifulSoup
from keiba_machine_learning.models import RaceTrac, TrackKind, TrackDirection, TrackSurface, Weather, RaceTracFactory, TrackKindFactory, TrackDirectionFactory, TrackSurfaceFactory, WeatherFactory, Gender

# NOTE: バージョニングは必要に応じて行う
# 例えばスクレイピング先がリニューアルされてDOMががらりと変わってしまったらこのスクリプトは使えなくなる
# その場合、コード自体は残しておいてリニューアルされたサイトに対応するものは新しいバージョンで実装を行う
# その際に名前空間も切る
# (YAGNIの原則に則って今の段階では作らない)


class RaceInformation(TypedDict):
    """レース情報をスクレイピングした結果として返すべき dict の構造を定義するクラス"""
    title: str
    race_track: RaceTrac
    track_kind: TrackKind
    track_direction: TrackDirection
    race_distance_by_meter: int
    track_surface: TrackSurface
    weather: Weather
    race_number: int
    starts_at: datetime


class RaceRecord(TypedDict):
    """レース結果の1行として返すべき dict の構造を定義するクラス

    各々の着に対応

    例えば以下のページだと9頭立てなので1〜9着まであり、各々の着にこのdictが対応する
    https://db.netkeiba.com/race/201901010101

    > 1 1 1 ゴルコンダ 牡2 54 ルメール 1:48.3 ** 1-1-1-1 36.5 1.4 1 518(-16) [東]木村哲也 サンデーレーシング 500.0

    上記のようなレース結果の表の1行を保持するデータ構造
    ※ 全項目を保持するわけではない
    """
    # TODO 重要指標である「着差」を入れる
    # アタマ、クビ、ハナ、n馬身など競馬特有の尺度をどう保持するのが適切なのかは一考する必要がある
    order_of_placing: int  # 着順
    bracket_number: int  # 枠番
    horse_number: int  # 馬番
    horse_id: int
    horse_name: str
    horse_age: int
    horse_gender: Gender
    impost: float  # 斤量
    jockey_id: int
    jockey_name: str
    race_time: float  # タイム
    win_betting_ratio: float  # 単勝倍率
    favorite_order: int  # 人気
    horse_weight: float  # 馬体重
    weight_change: float  # 体重変化


class RaceInformationScraper:
    @staticmethod
    def scrape(file: IO) -> RaceInformation:
        """
        Args:
            file (IO): netkeibaのレース結果ページのHTMLファイルを想定している

        Returns:
            RaceInformation: スクレイピング結果を返す
        """
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
