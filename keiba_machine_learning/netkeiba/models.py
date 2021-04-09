import os
from typing import IO
from keiba_machine_learning.models import Race as Base
from keiba_machine_learning.netkeiba.constants import DATABASE_PAGE_BASE_URL, RACE_DATA_DIR, ENCODING_OF_WEB_PAGE


class Race(Base):
    def __hash__(self) -> int:
        return int(f'{self.year}{self.race_track.value:02d}{self.series_number:02d}{self.day_number:02d}{self.race_number:02d}')

    @property
    def id(self) -> int:
        return self.__hash__()

    @property
    def url(self) -> str:
        """
        以下のようなnetkeibaでのレース結果ページを返す
        https://db.netkeiba.com/race/201901010101

        Returns:
            str: netkeibaでのレース結果ページのURL
        """
        return '/'.join([str(url_parts)
                         for url_parts in [DATABASE_PAGE_BASE_URL, "race", self.id]])

    @property
    def file_path(self) -> str:
        return os.path.join(RACE_DATA_DIR, f'{self.id}.html')

    @property
    def file(self) -> IO:
        return open(self.file_path, mode='r', encoding=ENCODING_OF_WEB_PAGE)
