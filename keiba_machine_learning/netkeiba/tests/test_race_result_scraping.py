import pytest
import os

from keiba_machine_learning.models import HorseGender
from keiba_machine_learning.netkeiba.scrapers import RaceResultScraper, DataNotFound
from keiba_machine_learning.netkeiba.constants import ENCODING_OF_WEB_PAGE

base_path = os.path.dirname(os.path.abspath(__file__))


def test_to_scrape_general_race_result():
    file_path = os.path.normpath(os.path.join(
        base_path, "./fixtures/201901010101.html"))

    with open(file_path, mode="r", encoding=ENCODING_OF_WEB_PAGE) as file:
        expect_data = [
            {
                'order_of_placing': 1,
                'bracket_number': 1,
                'horse_number': 1,
                'horse_id': 2017105318,
                'horse_name': 'ゴルコンダ',
                'horse_age': 2,
                'horse_gender': HorseGender.MALE,
                'impost': 54,
                'jockey_id': '05339',
                'jockey_name': 'ルメール',
                'race_time': 108.3,
                'win_betting_ratio': 1.4,
                'favorite_order': 1,
                'horse_weight': 518,
                'weight_change': -16,
            },
            {
                'order_of_placing': 2,
                'bracket_number': 3,
                'horse_number': 3,
                'horse_id': 2017104612,
                'horse_name': 'プントファイヤー',
                'horse_age': 2,
                'horse_gender': HorseGender.MALE,
                'impost': 54,
                'jockey_id': '05203',
                'jockey_name': '岩田康誠',
                'race_time': 110.1,
                'win_betting_ratio': 3.5,
                'favorite_order': 2,
                'horse_weight': 496,
                'weight_change': -8,
            },
            {
                'order_of_placing': 3,
                'bracket_number': 4,
                'horse_number': 4,
                'horse_id': 2017103879,
                'horse_name': 'ラグリマスネグラス',
                'horse_age': 2,
                'horse_gender': HorseGender.MALE,
                'impost': 51,
                'jockey_id': '01180',
                'jockey_name': '団野大成',
                'race_time': 110.9,
                'win_betting_ratio': 46.6,
                'favorite_order': 6,
                'horse_weight': 546,
                'weight_change': 6,
            },
            {
                'order_of_placing': 4,
                'bracket_number': 8,
                'horse_number': 9,
                'horse_id': 2017106259,
                'horse_name': 'キタノコドウ',
                'horse_age': 2,
                'horse_gender': HorseGender.MALE,
                'impost': 51,
                'jockey_id': '01179',
                'jockey_name': '菅原明良',
                'race_time': 111.5,
                'win_betting_ratio': 56.8,
                'favorite_order': 7,
                'horse_weight': 458,
                'weight_change': -8,
            },
            {
                'order_of_placing': 5,
                'bracket_number': 5,
                'horse_number': 5,
                'horse_id': 2017104140,
                'horse_name': 'ネモフィラブルー',
                'horse_age': 2,
                'horse_gender': HorseGender.MALE,
                'impost': 54,
                'jockey_id': '01062',
                'jockey_name': '川島信二',
                'race_time': 111.7,
                'win_betting_ratio': 140.3,
                'favorite_order': 9,
                'horse_weight': 436,
                'weight_change': 0,
            },
            {
                'order_of_placing': 6,
                'bracket_number': 8,
                'horse_number': 8,
                'horse_id': 2017101930,
                'horse_name': 'マイネルラクスマン',
                'horse_age': 2,
                'horse_gender': HorseGender.MALE,
                'impost': 54,
                'jockey_id': '01091',
                'jockey_name': '丹内祐次',
                'race_time': 112.1,
                'win_betting_ratio': 9.7,
                'favorite_order': 3,
                'horse_weight': 480,
                'weight_change': 8,
            },
            {
                'order_of_placing': 7,
                'bracket_number': 2,
                'horse_number': 2,
                'horse_id': 2017100184,
                'horse_name': 'サンモンテベロ',
                'horse_age': 2,
                'horse_gender': HorseGender.FEMALE,
                'impost': 54,
                'jockey_id': '01109',
                'jockey_name': '黛弘人',
                'race_time': 112.5,
                'win_betting_ratio': 114.7,
                'favorite_order': 8,
                'horse_weight': 450,
                'weight_change': 2,
            },
            {
                'order_of_placing': 8,
                'bracket_number': 7,
                'horse_number': 7,
                'horse_id': 2017102953,
                'horse_name': 'エスカレーション',
                'horse_age': 2,
                'horse_gender': HorseGender.FEMALE,
                'impost': 54,
                'jockey_id': '01093',
                'jockey_name': '藤岡佑介',
                'race_time': 112.5,
                'win_betting_ratio': 26.1,
                'favorite_order': 5,
                'horse_weight': 448,
                'weight_change': -4,
            },
            {
                'order_of_placing': 9,
                'bracket_number': 6,
                'horse_number': 6,
                'horse_id': 2017102421,
                'horse_name': 'セイウンジュリア',
                'horse_age': 2,
                'horse_gender': HorseGender.FEMALE,
                'impost': 54,
                'jockey_id': '01032',
                'jockey_name': '池添謙一',
                'race_time': 112.6,
                'win_betting_ratio': 16.4,
                'favorite_order': 4,
                'horse_weight': 470,
                'weight_change': 0,
            },
        ]
        assert RaceResultScraper.scrape(file) == expect_data


def test_to_scrape_empty_page():
    file_path = os.path.normpath(os.path.join(
        base_path, "./fixtures/empty_page.html"))

    with open(file_path, mode="r", encoding=ENCODING_OF_WEB_PAGE) as file:
        with pytest.raises(DataNotFound):
            assert RaceResultScraper.scrape(file)
