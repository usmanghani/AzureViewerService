from praytimes import PrayTimes

p = PrayTimes('Karachi')
p.setMethod('Karachi')
p.adjust({'asr':'Hanafi'})

import datetime
times = p.getTimes(datetime.date.today(), (47.6097, -122.3331), -8, True)

from pprint import pprint

pprint(times)
