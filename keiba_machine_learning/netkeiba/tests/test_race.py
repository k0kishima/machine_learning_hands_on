from keiba_machine_learning.models import RaceTrac
from keiba_machine_learning.netkeiba.models import Race


def test_identifier():
    race = Race(year=2020, race_track=RaceTrac.HOKKAIDO,
                series_number=1, day_number=1, race_number=1)
    assert race.id == 202001010101
