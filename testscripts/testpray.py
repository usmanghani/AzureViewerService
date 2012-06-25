from praytimes import PrayTimes

p = PrayTimes('Karachi')
p.setMethod('Karachi')
p.adjust({'asr':'Hanafi'})

import datetime
times = p.getTimes(datetime.date.today(), (47.6097, -122.3331), -8, True)

from pprint import pprint

pprint(times)

from lxml import objectify
from lxml import etree
from requests import get


r = get('http://www.earthtools.org/timezone/47.6097/-122.3331')

root = objectify.fromstring(r.text.encode('ascii'))

# root = objectify.fromstring(
# '''<?xml version="1.0" encoding="ISO-8859-1" ?>
# <timezone xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.earthtools.org/timezone-1.1.xsd">
# <version>1.1</version>
# <location>
# <latitude>47.6097</latitude>
# <longitude>-122.3331</longitude>
# </location>
# <offset>-8</offset>
# <suffix>U</suffix>
# <localtime>24 Jun 2012 23:10:46</localtime>
# <isotime>2012-06-24 23:10:46 -0800</isotime>
# <utctime>2012-06-25 07:10:46</utctime>
# <dst>Unknown</dst>
# </timezone>'''
# )

pprint(root.offset)
pprint(root.dst)

