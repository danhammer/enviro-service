from utils import utils
from utils import water
from utils import vegetation
from utils import deforestation


def water_service(coords, date, viewer=False):
    poly = utils.to_poly(coords, viewer=viewer)
    year = int(date.split("-")[0])
    res = water.surface_water(poly['geometry']['coordinates'], year)

    return dict(
        area=res['area'],
        result=res['geom'],
        date=date,
        poly=poly
    )


def water_series_service(coords, begin, end, viewer=False):
    poly = utils.to_poly(coords, viewer=viewer)
    res = water.water_series(poly['geometry']['coordinates'], begin, end)

    return dict(
        count=len(res),
        result=res,
        begin=begin,
        end=end,
        poly=poly
    )


def deforestation_service(coords, begin, end, viewer=False):
    res = deforestation.grab(coords, begin, end)
    poly = utils.to_poly(coords, viewer=viewer)
    return dict(
        begin=begin,
        end=end,
        poly=poly,
        area=res
    )


def vegetation_service(coords, begin, end, viewer=False):
    res = vegetation.grab(coords, begin, end)
    poly = utils.to_poly(coords, viewer=viewer)
    return dict(
        count=len(res),
        results=res,
        poly=poly,
        begin=begin,
        end=end
    )
