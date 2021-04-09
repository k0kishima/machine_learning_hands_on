from enum import Enum
from pydantic import Field
from pydantic.dataclasses import dataclass
import datetime


class RaceTrac(Enum):
    """競馬場に対応するモデル

        東京競馬場・阪神競馬場など
        全10場が個々のオブジェクトに対応

    Args:
        Enum (Emum): Enumを継承
    """
    SAPPORO = 1
    HAKODATE = 2
    FUKUSHIMA = 3
    NIGATA = 4
    TOKYO = 5
    NAKAYAMA = 6
    CHUKYO = 7
    KYOTO = 8
    HANSHIN = 9
    KOKURA = 10


class RaceTracFactory:
    @staticmethod
    def create(race_track_name: str) -> RaceTrac:
        NAMES_INDEXED_BY_MARK_STR = {
            '札幌': 'SAPPORO',
            '函館': 'HAKODATE',
            '福島': 'FUKUSHIMA',
            '新潟': 'NIGATA',
            '東京': 'TOKYO',
            '中山': 'NAKAYAMA',
            '中京': 'CHUKYO',
            '京都': 'KYOTO',
            '阪神': 'HANSHIN',
            '小倉': 'KOKURA',
        }
        return RaceTrac[NAMES_INDEXED_BY_MARK_STR[race_track_name]]


@dataclass
class Race:
    """レースのモデル

        必要最低限の属性のみを保持したレースの基底モデル

    """
    # ブラウザURL直打ちして2着以下も取得できた年を暫定的に指定
    # 1985年はページ自体は閲覧できるが1着しか見れない（ログインすれば見れる旨は記載されていた）
    OLDEST_READABLE_YEAR = 1986

    # 2020年東京競馬場を基準にURL直打ちして確認したところ5までしかなかった
    # バッファ取って以下の値とした
    MAX_SERIES_NUMBER = 7

    # 上記と同様
    # 9日目まではあったがバッファを取って以下の値に
    MAX_DAY_NUMBER = 10

    MAX_RACE_NUMBER = 12

    race_track: RaceTrac
    year: int = Field(ge=OLDEST_READABLE_YEAR, le=datetime.date.today().year)
    series_number: int = Field(ge=1, le=MAX_SERIES_NUMBER)
    day_number: int = Field(ge=1, le=MAX_DAY_NUMBER)
    race_number: int = Field(ge=1, le=MAX_RACE_NUMBER)


class Weather(Enum):
    """天候に対応するモデル

        曇 | 晴 | 雨 | 小雨 | 小雪 | 雪

    Args:
        Enum (Emum): Enumを継承
    """
    CLOUDY = 1
    SUNNY = 2
    RAINY = 3
    LIGHT_RAIN = 4
    LIGHT_SNOWY = 5
    SNOWY = 6


class TrackDirection(Enum):
    """右回りか左回りかを保持するモデル

    Args:
        Enum (Emum): Enumを継承
    """
    LEFT = 1
    RIGHT = 2


class TrackKind(Enum):
    """競走種別に対応するモデル

        芝 | ダート　｜ 障害　

    Args:
        Enum (Emum): Enumを継承
    """
    GRASS = 1
    DIRT = 2
    JUMP = 3


class TrackSurface(Enum):
    """馬場状態に対応するモデル

        良　稍重　重　不良　

    Args:
        Enum (Emum): Enumを継承
    """
    GOOD_TO_FIRM = 1
    GOOD = 2
    YIELDING = 3
    SOFT = 4
