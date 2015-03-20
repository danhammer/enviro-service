import paths
paths.fix_path()

from geojson import Feature, Polygon
import json
import re


def _osm_prefix(out='json', timeout=25):
    """Generate the OSM prefix with reasonable defaults. Supports no timeout
    by supplying None to this function wrapper."""
    if timeout is not None:
        return '[out:%s][timeout:%s];' % (out, timeout)
    else:
        return '[out:%s];' % out


def _osm_component(geotype, lat, lon, search_pairs, buf=20):
    """Returns the part of the OSM query that filters the type and search
    filters.
    Args:
        geotype: 'node', 'way', or 'relation'
        kv_pairs: {'note': Walmart, 'landuse': Industrial}
    """
    nearby = '(around:%s,%s,%s)' % (float(buf), lat, lon)
    if search_pairs == {}:
        query = geotype + nearby + ';'
    else:
        fields = ['["%s"~"%s"]' % (k, v) for k, v in search_pairs.items()]
        field_str = ''.join(fields)
        query = geotype + field_str + nearby + ';'

    return query + 'out geom;'


def fetch_overpass(base, payload={}):
    """Accepts a base URL and a payload for a GET request to the overpass API,
    which accepts a strange and very rigid format."""
    if payload == {}:
        url = base
    else:
        param_list = ["%s=%s" % (k, v) for k, v in payload.items()]
        url = re.sub(" ", "%20", base + '?' + '&'.join(param_list))

    try:
        from google.appengine.api import urlfetch
        res = urlfetch.fetch(url).content
        return json.loads(res)
    except ImportError:
        import requests
        res = requests.get(url)
        return res.json()


def poly_query(coords, timeout=250):
    """Returns the part of the OSM query that grabs all elements of the
    supplied geotype within the given bounding box polygon.
    """
    prefix = "[out:json][timeout:%s];" % timeout
    coords_str = ' '.join(["%s %s" % (y, x) for x, y in coords])
    geom = 'way(poly:"%s");' % coords_str
    suffix = "out geom;>;out skel qt;"
    return prefix + geom + suffix


def _building(way):
    """Accepts an OSM way and returns true if the way represents a polygon,
    rather than a point or line."""
    try:
        # If there are duplicate coordinates, then the geometry is closed
        # (read: it is a polygon)
        coords = [(g['lon'], g['lat']) for g in way['geometry']
                  if g is not None]
        seen = set()
        uniq = []
        for x in coords:
            if x not in seen:
                uniq.append(x)
                seen.add(x)

        building = 'building' in way['tags'].keys()

        if len(uniq) != len(coords):
            return building
        else:
            return False

    except (KeyError or TypeError):
        # If there is no `geometry` key then it is likely a node, but
        # certainly not a polygon
        return False


def way_to_geojson(way_poly, bbox=None):
    """Accepts a polygon that remains formatted as an OSM way and converts it
    into a geojson feature."""
    coords = []

    if bbox is not None:
        # Clip the OSM geojsons to the extent of the bounding box, rather than
        # completing the features despite the bounding box
        for g in way_poly['geometry']:
            if g['lon'] < bbox['xmin']:
                x = bbox['xmin']
            elif g['lon'] > bbox['xmax']:
                x = bbox['xmax']
            else:
                x = g['lon']

            if g['lat'] < bbox['ymin']:
                y = bbox['ymin']
            elif g['lat'] > bbox['ymax']:
                y = bbox['ymax']
            else:
                y = g['lat']

            coords.append([x, y])

    else:
        coords = [(g['lon'], g['lat']) for g in way_poly['geometry']]

    try:
        tags = way_poly['tags']
    except KeyError:
        tags = None

    x = Feature(geometry=Polygon(coords), properties=tags, id=way_poly['id'])
    return dict(x)


def harvest(coords):
    """Harvest building for the supplied bounding box and resolution. TODO:
    Ensure that the resolution is the correct way to do this, given that the
    resolution may be different for the x- and y-directions.
    """
    base = 'http://overpass-api.de/api/interpreter'
    params = {'data': poly_query(coords)}
    data = fetch_overpass(base, payload=params)
    polys = filter(_building, data['elements'])
    return [way_to_geojson(p) for p in polys]
