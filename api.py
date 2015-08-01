import webapp2
import json
import envirohook
from datetime import date

# Required for Earth Engine authentication
import config

from utils import paths
paths.fix_path()

TODAY = date.today().strftime("%Y-%m-%d")


class WaterHandler(webapp2.RequestHandler):
    def get(self):

        # headers
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'

        # parameters
        coords = json.loads(self.request.get('coords'))
        viewer = bool(self.request.get('viewer', False))
        dt = self.request.get('date', TODAY)

        # response
        res = json.dumps(envirohook.water_service(coords, dt, viewer))
        self.response.write(res)


class WaterSeriesHandler(webapp2.RequestHandler):
    def get(self):

        # headers
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'

        # parameters
        coords = json.loads(self.request.get('coords'))
        viewer = bool(self.request.get('viewer', False))
        end = self.request.get('end', TODAY)
        begin = self.request.get('begin', '2012-01-01')

        # response
        series = envirohook.water_series_service(coords, begin, end, viewer)
        res = json.dumps(series)
        self.response.write(res)


class DeforestationHandler(webapp2.RequestHandler):
    def get(self):

        # headers
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'

        # parameters
        coords = json.loads(self.request.get('coords'))
        begin = self.request.get('begin', '2005-12-15')
        end = self.request.get('end', TODAY)

        # response
        res = json.dumps(envirohook.deforestation_service(coords, begin, end,))
        self.response.write(res)


class VegetationHandler(webapp2.RequestHandler):
    def get(self):
        # headers
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json'

        # parameters
        coords = json.loads(self.request.get('coords'))
        end = self.request.get('end', TODAY)
        begin = self.request.get('begin', '2012-01-01')

        # response
        series = envirohook.vegetation_service(coords, begin, end)
        res = json.dumps(series)
        self.response.write(res)


handlers = webapp2.WSGIApplication([
    ('/water', WaterHandler),
    ('/water/series', WaterSeriesHandler),
    ('/deforestation', DeforestationHandler),
    ('/vegetation/series', VegetationHandler)
], debug=True)
