from enum import Enum
from pydantic import Field
from pydantic.dataclasses import dataclass
import datetime


class RaceTrac(Enum):
    """競馬場に対応するモデル

        東京競馬場・阪神競馬場など
        全10場が個々のオブジェクトに対応

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
        """ 文字列からRaceTracオブジェクトを生成する

        Args:
            race_track_name (str): 競馬場の名前

        Returns:
            RaceTrac: 
        """
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
    """ 必要最低限の属性のみを保持したレースの基底モデル """
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
    CLOUD = 1
    FINE = 2
    RAIY = 3
    LIGHT_RAIN = 4
    LIGHT_SNOW = 5
    SNOW = 6


class WeatherFactory:
    @staticmethod
    def create(weather_name: str) -> Weather:
        """ 文字列からWeatherオブジェクトを生成する

        Args:
            weather_name (str): 曇 | 晴 | 雨 | 小雨 | 小雪 | 雪

        Returns:
            Weather: 
        """
        NAMES_INDEXED_BY_MARK_STR = {
            '曇': 'CLOUD',
            '晴': 'FINE',
            '雨': 'RAINY',
            '小雨': 'LIGHT_RAIN',
            '小雪': 'LIGHT_SNOW',
            '雪': 'SNOW',
        }
        return Weather[NAMES_INDEXED_BY_MARK_STR[weather_name]]


class TrackDirection(Enum):
    LEFT = 1
    RIGHT = 2


class TrackDirectionFactory:
    @staticmethod
    def create(track_direction_name: str) -> TrackDirection:
        """文字列からTrackDirectionオブジェクトを生成する

        Args:
            track_direction_name (str): 右 | 左

        Returns:
            TrackDirection: 
        """
        NAMES_INDEXED_BY_MARK_STR = {
            '左': 'LEFT',
            '右': 'RIGHT',
        }
        return TrackDirection[NAMES_INDEXED_BY_MARK_STR[track_direction_name]]


class TrackKind(Enum):
    GRASS = 1
    DIRT = 2
    JUMP = 3


class TrackKindFactory:
    @staticmethod
    def create(track_kind_name: str) -> TrackKind:
        """文字列からTrackKindオブジェクトを生成する

        Args:
            track_kind_name (str): 芝 | ダート　｜ 障害　

        Returns:
            TrackKind: 
        """
        NAMES_INDEXED_BY_MARK_STR = {
            '芝': 'GRASS',
            'ダート': 'DIRT',
            '障害': 'JUMP',
        }
        return TrackKind[NAMES_INDEXED_BY_MARK_STR[track_kind_name]]


class TrackSurface(Enum):
    GOOD_TO_FIRM = 1  # 馬場が芝だと "GOOD_TO_FIRM"で、ダートだと"Standard"らしいが前者で統一
    GOOD = 2
    YIELDING = 3  # これもダートだと "Muddy" らしいが芝の用語だけを使う
    SOFT = 4  # 同じくダートだと "Sloppy" らしいが芝の用語だけを使う


class TrackSurfaceFactory:
    @staticmethod
    def create(track_surface_name: str) -> TrackSurface:
        """文字列からTrackSurfaceオブジェクトを生成する

        Args:
            track_surface_name (str): 良 | 稍重 | 重 | 不良　

        Returns:
            TrackSurface: 
        """
        NAMES_INDEXED_BY_MARK_STR = {
            '良': 'GOOD_TO_FIRM',
            '稍重': 'GOOD',
            '重': 'YIELDING',
            '不良': 'SOFT',
        }
        return TrackSurface[NAMES_INDEXED_BY_MARK_STR[track_surface_name]]


class Gender(Enum):
    MALE = 1
    FEMALE = 2
