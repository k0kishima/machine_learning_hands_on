import re
from datetime import datetime
from typing import IO, List, TypedDict
from bs4 import BeautifulSoup
from keiba_machine_learning.models import RaceTrac, TrackKind, TrackDirection, TrackSurface, Weather, RaceTracFactory, TrackKindFactory, TrackDirectionFactory, TrackSurfaceFactory, WeatherFactory, HorseGender, HorseGenderFactory

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
    horse_gender: HorseGender
    impost: float  # 斤量
    jockey_id: str  # ※ "05203"のような0埋めで5桁が大半だが引退した騎手だと"z0004"みたいな変則的な書式も存在している
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
            file (IO): netkeibaのレース結果ページのHTMLファイル

        Returns:
            RaceInformation
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


class RaceResultScraper:
    @staticmethod
    def scrape(file: IO) -> List[RaceRecord]:
        """
        Args:
            file (IO): netkeibaのレース結果ページのHTMLファイル

        Returns:
            List[RaceRecord]
        """
        soup = BeautifulSoup(file, 'html.parser')
        race_result_table_rows = soup.find(
            'table', attrs={'summary': 'レース結果'}).find_all('tr')

        race_records = []

        # 最初の要素は項目行(header)なのでスキップ
        for row in race_result_table_rows[1:]:
            cells = row.find_all('td')
            order_of_placing = int(cells[0].get_text())
            bracket_number = int(cells[1].get_text())
            horse_number = int(cells[2].get_text())
            horse_id = int(
                re.search(r'horse/(\d+)', cells[3].find('a')['href']).group(1))
            horse_name = cells[3].get_text().strip()
            horse_age = int(cells[4].get_text()[1])
            horse_gender = HorseGenderFactory.create(cells[4].get_text()[0])
            impost = int(cells[5].get_text())
            jockey_id = re.search(
                r'jockey/(\d+)', cells[6].find('a')['href']).group(1)
            jockey_name = cells[6].get_text().strip()

            minute, second, split_second = re.findall(
                r'^(\d{1}):(\d{2})\.(\d{1})', cells[7].get_text())[0]
            race_time = (int(minute) * 60) + (int(second)) + \
                (int(split_second) * 0.1)

            win_betting_ratio = float(cells[12].get_text())
            favorite_order = int(cells[13].get_text())

            horse_weight, weight_change = [int(weight_data) for weight_data in re.findall(
                r'(\d{3})\(([+-]?\d{1,2})\)', cells[14].get_text())[0]]

            race_record = {
                'order_of_placing': order_of_placing,
                'bracket_number': bracket_number,
                'horse_number': horse_number,
                'horse_id': horse_id,
                'horse_name': horse_name,
                'horse_age': horse_age,
                'horse_gender': horse_gender,
                'impost': impost,
                'jockey_id': jockey_id,
                'jockey_name': jockey_name,
                'race_time': race_time,
                'win_betting_ratio': win_betting_ratio,
                'favorite_order': favorite_order,
                'horse_weight': horse_weight,
                'weight_change': weight_change,
            }
            race_records.append(race_record)

        return race_records
