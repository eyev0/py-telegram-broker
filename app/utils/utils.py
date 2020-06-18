import pendulum
from pendulum.tz.timezone import Timezone

clock = pendulum.datetime(2020, 1, 1, tz=Timezone("Europe/Moscow"))
