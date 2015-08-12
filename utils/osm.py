from utils import paths
paths.fix_path()

import json
import numpy as np
from google.appengine.api import urlfetch


def osm_bounds(ymin, xmin, ymax, xmax):
    str_bounds = map(str, [ymin, xmin, ymax, xmax])
    return ','.join(str_bounds)


def harvest_ways(bounds, residential=True, timeout=250):
    # Accepts a bounding box (a formatted item from sample_features) and
    # returns all ways within the bounds

    # Construct URL
    if residential is True:
        geom = 'way[building=residential](%s);' % bounds
    else:
        print "NO"
        geom = 'way[building](%s);' % bounds

    base = 'http://overpass-api.de/api/interpreter'
    prefix = '[out:json][timeout:%s];' % timeout
    suffix = 'out%20geom;>;out%20skel%20qt;'
    url = base + '?data=' + prefix + geom + suffix

    # request data from overpass api
    try:
        data = json.loads(urlfetch.fetch(url=url).content)
        # print data
    except ValueError:
        return []

    def _ways(elem):
        try:
            return (elem['type'] == 'way')
        except Exception:
            return False
    return filter(_ways, data['elements'])


def process_ways(ways):
    def _process(w):
        lat = np.mean([g['lat'] for g in w['geometry']])
        lon = np.mean([g['lon'] for g in w['geometry']])
        return {'lon': lon, 'lat': lat}

    return [_process(w) for w in ways]


def grab(bbox_dict, residential_bool):
    bounds = osm_bounds(
        bbox_dict['ymin'],
        bbox_dict['xmin'],
        bbox_dict['ymax'],
        bbox_dict['xmax']
    )
    ways = harvest_ways(bounds, residential=residential_bool)
    res = process_ways(ways)
    return {'residential': residential_bool, 'results': res, 'count': len(res)}
