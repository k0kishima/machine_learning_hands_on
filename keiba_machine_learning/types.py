from datetime import datetime
from typing import TypedDict
from keiba_machine_learning.models import RaceTrac, TrackKind, TrackDirection, TrackSurface, Weather, HorseGender


class RaceInformation(TypedDict):
    """レース情報をスクレイピングした結果として返すべき dict の構造を定義するクラス"""
    title: str
    race_track: RaceTrac
    track_kind: TrackKind
    track_direction: TrackDirection
    race_distance_by_meter: int
    track_surface: TrackSurface
    weather: Weather
    race_number: int
    starts_at: datetime


class RaceRecord(TypedDict):
    """レース結果の1行として返すべき dict の構造を定義するクラス

    各々の着に対応

    例えば以下のページだと9頭立てなので1〜9着まであり、各々の着にこのdictが対応する
    https://db.netkeiba.com/race/201901010101

    > 1 1 1 ゴルコンダ 牡2 54 ルメール 1:48.3 ** 1-1-1-1 36.5 1.4 1 518(-16) [東]木村哲也 サンデーレーシング 500.0

    上記のようなレース結果の表の1行を保持するデータ構造
    ※ 全項目を保持するわけではない
    """
    # TODO 重要指標である「着差」を入れる
    # アタマ、クビ、ハナ、n馬身など競馬特有の尺度をどう保持するのが適切なのかは一考する必要がある
    order_of_placing: int  # 着順
    bracket_number: int  # 枠番
    horse_number: int  # 馬番
    horse_id: int
    horse_name: str
    horse_age: int
    horse_gender: HorseGender
    impost: float  # 斤量
    jockey_id: str  # ※ "05203"のような0埋めで5桁が大半だが引退した騎手だと"z0004"みたいな変則的な書式も存在している
    jockey_name: str
    race_time: float  # タイム
    win_betting_ratio: float  # 単勝倍率
    favorite_order: int  # 人気
    horse_weight: float  # 馬体重
    weight_change: float  # 体重変化
