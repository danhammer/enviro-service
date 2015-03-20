import random
from utils import buildings
from utils import utils
from utils import water


def cars(coords, date, viewer=True):
    bbox = utils.bounding_box(coords)
    n = random.randint(3, 30)
    i = 0
    car_coords = []
    while i < n:
        pt = utils.gen_point(bbox)
        if utils.in_polygon(pt, coords) is True:
            car_coords.append(pt)
            i += 1

    return dict(
        results=[utils.to_point(x, y) for x, y in car_coords],
        count=len(car_coords),
        date=date,
        polygon=utils.to_poly(coords, viewer=viewer)
    )


def change(coords, date, viewer=True):
    s = random.uniform(0.1, 0.9)
    change_poly = utils.scale_poly(coords, scale=s)
    bbox = utils.bounding_box(change_poly)
    n = random.randint(3, 30)
    i = 0
    kp_coords = []
    while i < n:
        pt = utils.gen_point(bbox)
        if utils.in_polygon(pt, change_poly) is True:
            kp_coords.append(pt)
            i += 1
    return dict(
        area=s,
        date=date,
        change_poly=utils.to_poly(change_poly, viewer=False),
        poly=utils.to_poly(coords, viewer=viewer),
        count=len(kp_coords),
        results=[utils.to_point(x, y) for x, y in kp_coords]
    )


def water_service(coords, date, viewer=True):
    # s = random.uniform(0.1, 0.9)
    # change_poly = utils.scale_poly(coords, scale=s)
    # return dict(
    #     area=s,
    #     date=date,
    #     change_poly=utils.to_poly(change_poly, viewer=False),
    #     poly=utils.to_poly(coords, viewer=viewer)
    # )
    poly = utils.to_poly(coords, viewer=viewer)
    year = int(date.split("-")[0])
    area = water.surface_water(poly['geometry']['coordinates'], year)
    return dict(
        area=area,
        date=date,
        poly=poly
    )


def deforestation(coords, begin, end, viewer=True):
    s = random.uniform(0.1, 0.9)
    change_poly = utils.scale_poly(coords, scale=s)
    return dict(
        area=s,
        begin=begin,
        end=end,
        change_poly=utils.to_poly(change_poly, viewer=False),
        poly=utils.to_poly(coords, viewer=viewer)
    )


def building_service(coords, date, viewer=True):
    res = buildings.harvest(coords)
    return dict(
        date=date,
        poly=utils.to_poly(coords, viewer=viewer),
        count=len(res),
        buildings=res
    )

