import ee


def surface_water(coords, year):

    loc = "L7_TOA_1YEAR/%s" % year

    weights = {
        "b(0)": 0.2626,
        "b(1)": 0.2141,
        "b(2)": 0.0926,
        "b(3)": 0.0656,
        "b(4)": -0.7629,
        "b(6)": -0.5388
    }

    exp = '+'.join(['%s*%s' % (k, v) for k, v in weights.items()])
    poly = ee.Geometry.Polygon(*coords)
    img = ee.Image(loc).clip(poly)
    water = img.expression(exp)
    threshold_exp = "(b(0) > 4) ? 1 : 0"
    binary = water.expression(threshold_exp)

    area = binary.reduceRegion(
        ee.Reducer.mean(),
        poly,
        30,
        None,
        None,
        True
    ).getInfo()

    ct = binary.mask(binary).connectedPixelCount(200, )
    x = ct.clip(poly).reduceToVectors(
        ee.Reducer.countEvery(),
        poly,
        500,
        "polygon",
        True,
        "label",
        None,
        None,
        False,
        500000
    )
    res = dict(area=area, geom=x.getInfo())
    return res
