from enum import Enum
from pydantic import Field
from pydantic.dataclasses import dataclass
import datetime


class RaceTrac(Enum):
    HOKKAIDO = 1
    HAKODATE = 2
    FUKUSHIMA = 3
    NIGATA = 4
    TOKYO = 5
    NAKAYAMA = 6
    CHUKYO = 7
    KYOTO = 8
    HANSHIN = 9
    KOKURA = 10


@dataclass
class Race:
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
