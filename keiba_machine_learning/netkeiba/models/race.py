from typing import IO
from keiba_machine_learning.models.race import Race as Base
from keiba_machine_learning.netkeiba.constants import DATABASE_PAGE_BASE_URL


class Race(Base):
    def __hash__(self) -> int:
        return int(f'{self.year}{self.race_track.value:02d}{self.series_number:02d}{self.day_number:02d}{self.race_number:02d}')

    @property
    def id(self) -> int:
        return self.__hash__()

    @property
    def url(self) -> str:
        return '/'.join([str(url_parts)
                         for url_parts in [DATABASE_PAGE_BASE_URL, "race", self.id]])
