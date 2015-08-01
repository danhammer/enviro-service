import urllib
import json
from google.appengine.api import urlfetch


def grab(coords, begin, end, dataname="forma-alerts"):
    BASE = "http://gfw-apis.appspot.com/forest-change/%s" % dataname

    geojson = json.dumps(
        dict(type="Polygon", coordinates=[coords])
    )

    form_fields = urllib.urlencode({
        "period": "%s,%s" % (begin, end),
        "geojson": geojson
    })

    res = urlfetch.fetch(url=BASE + "?" + form_fields).content
    value = json.loads(res)["value"]
    return value

