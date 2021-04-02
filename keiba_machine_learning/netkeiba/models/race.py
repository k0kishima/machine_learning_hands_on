from keiba_machine_learning import models


class Race(models.race.Race):
    def __hash__(self) -> int:
        return int(f'{self.year}{self.race_track.value:02d}{self.series_number:02d}{self.day_number:02d}{self.race_number:02d}')

    @property
    def id(self) -> int:
        return self.__hash__()
