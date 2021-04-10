import re
from datetime import datetime
from typing import IO, List
from bs4 import BeautifulSoup
from keiba_machine_learning.models import RaceTracFactory, TrackKindFactory, TrackDirectionFactory, TrackSurfaceFactory, WeatherFactory, HorseGenderFactory, TrackSurface
from keiba_machine_learning.types import RaceInformation, RaceRecord

# NOTE: バージョニングは必要に応じて行う
# 例えばスクレイピング先がリニューアルされてDOMががらりと変わってしまったらこのスクリプトは使えなくなる
# その場合、コード自体は残しておいてリニューアルされたサイトに対応するものは新しいバージョンで実装を行う
# その際に名前空間も切る
# (YAGNIの原則に則って今の段階では作らない)


class DataNotFound(Exception):
    pass


class IncompatibleDataDetected(Exception):
    pass


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

        # netkeiba側の仕様でレースデータが存在しないページにアクセスしても404をHTTPステータスコードとしてレスポンスしないので、
        # データが存在しない掲載されていないファイルが渡ってくることも想定してここでデータがない場合の制御をする
        race_result_table = soup.find('table', attrs={'summary': 'レース結果'})
        if race_result_table is None:
            raise DataNotFound

        title_element = soup.select_one(
            '#main > div > div > div > diary_snap > div > div > dl > dd > h1')
        text_under_the_title = soup.select_one(
            '#main > div > div > div > diary_snap > div > div > dl > dd > p > diary_snap_cut > span').get_text()
        race_number_element = soup.select_one(
            '#main > div > div > div > diary_snap > div > div > dl > dt')

        if s := re.search(r'(\d{4})m', text_under_the_title):
            race_distance_by_meter = int(s.group(1))
        else:
            raise ValueError("can't parse race distance.")

        if s := re.search(r'\d+', race_number_element.get_text()):
            race_number = int(s.group())
        else:
            raise ValueError("can't parse race number.")

        race_track_name = soup.select_one(
            '#main > div > div > div > ul > li > a.active').get_text()

        track_kind_mark = text_under_the_title[0]
        if track_kind_mark == '障':
            raise IncompatibleDataDetected

        track_direction_mark = text_under_the_title[1]
        if track_direction_mark == '直':
            raise IncompatibleDataDetected

        if s := re.search(r'天候 : (\w+)', text_under_the_title):
            weather_mark = s.group(1)
        else:
            raise ValueError("can't parse weather.")

        return {
            'title': title_element.get_text(),
            'race_track': RaceTracFactory.create(race_track_name),
            'track_kind': TrackKindFactory.create(track_kind_mark),
            'track_direction': TrackDirectionFactory.create(track_direction_mark),
            'race_distance_by_meter': race_distance_by_meter,
            'track_surface': TrackSurfaceParser.parse(text_under_the_title),
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
        race_result_table = soup.find('table', attrs={'summary': 'レース結果'})
        if race_result_table is None:
            raise DataNotFound
        race_result_table_rows = race_result_table.find_all('tr')

        race_records = []

        # 最初の要素は項目行(header)なのでスキップ
        for row in race_result_table_rows[1:]:
            cells = row.find_all('td')

            order_of_placing = int(cells[0].get_text())
            bracket_number = int(cells[1].get_text())
            horse_number = int(cells[2].get_text())

            if s := re.search(r'horse/(\d+)', cells[3].find('a')['href']):
                horse_id = int(s.group(1))
            else:
                raise ValueError("can't parse horse id.")

            horse_name = cells[3].get_text().strip()
            horse_age = int(cells[4].get_text()[1])
            horse_gender = HorseGenderFactory.create(cells[4].get_text()[0])
            impost = float(cells[5].get_text())

            if s := re.search(r'jockey/(\d+)', cells[6].find('a')['href']):
                jockey_id = s.group(1)
            else:
                raise ValueError("can't parse jockey id.")

            jockey_name = cells[6].get_text().strip()

            if f := re.findall(r'^(\d{1}):(\d{2})\.(\d{1})', cells[7].get_text()):
                minute, second, split_second = [
                    int(time_data) for time_data in f[0]]
                race_time = (minute * 60) + second + (split_second * 0.1)
            else:
                raise ValueError("can't parse jockey id.")

            win_betting_ratio = float(cells[12].get_text())
            favorite_order = int(cells[13].get_text())

            if f := re.findall(r'(\d{3})\(([+-]?\d{1,2})\)', cells[14].get_text()):
                horse_weight, weight_change = [
                    int(weight_data) for weight_data in f[0]]
            else:
                raise ValueError("can't parse weight data.")

            race_record: RaceRecord = {
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


class TrackSurfaceParser:
    @staticmethod
    def parse(text: str) -> TrackSurface:
        """
        Args:
            text (str): レース情報のテキスト

            例:
            ダ左1200m / 天候 : 曇 / ダート : 良 / 発走 : 13:10

        Returns:
            TrackSurface
        """
        if s := re.search(r'(芝|ダート) : (\w+)', text):
            return TrackSurfaceFactory.create(s.group(2))
        else:
            raise ValueError("can't parse track surface.")
