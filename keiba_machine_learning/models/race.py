from enum import Enum
from pydantic import Field
from pydantic.dataclasses import dataclass
import datetime

# ブラウザURL直打ちして2着以下も取得できた年を暫定的に指定
# 1985年はページ自体は閲覧できるが1着しか見れない（ログインすれば見れる旨は記載されていた）
OLDEST_READABLE_YEAR = 1986

# 2020年東京競馬場を基準にURL直打ちして確認したところ5までしかなかった
# バッファ取って以下の値とした
MAX_SERIES_NUMBER = 7

# 上記と同様
# 9日目まではあったがバッファを取って以下の値に
MAX_DAY_NUMBER = 12

MAX_RACE_NUMBER = 12


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
    race_track: RaceTrac
    year: int = Field(ge=OLDEST_READABLE_YEAR, le=datetime.date.today().year)
    series_number: int = Field(ge=1, le=MAX_SERIES_NUMBER)
    day_number: int = Field(ge=1, le=MAX_DAY_NUMBER)
    race_number: int = Field(ge=1, le=MAX_RACE_NUMBER)

    def __hash__(self) -> int:
        return int(f'{self.year}{self.race_track.value:02d}{self.series_number:02d}{self.day_number:02d}{self.race_number:02d}')

    @property
    def id(self) -> int:
        return self.__hash__()
