import webapp2
import json
import dummy
import config
from datetime import date

from utils import paths
paths.fix_path()

TODAY = date.today().strftime("%Y-%m-%d")


class DummyCarHandler(webapp2.RequestHandler):
    def get(self):
        """
        """
        # headers
        self.response.headers['Content-Type'] = 'application/json'

        # parameters
        coords = json.loads(self.request.get('coords'))
        viewer = bool(self.request.get('viewer', False))
        dt = self.request.get('date', TODAY)

        # response
        self.response.write(json.dumps(dummy.cars(coords, dt, viewer)))


class DummyChangeHandler(webapp2.RequestHandler):
    def get(self):
        """
        """
        # headers
        self.response.headers['Content-Type'] = 'application/json'

        # parameters
        coords = json.loads(self.request.get('coords'))
        viewer = bool(self.request.get('viewer', False))
        dt = self.request.get('date', TODAY)

        # response
        self.response.write(json.dumps(dummy.change(coords, dt, viewer)))


class DummyWaterHandler(webapp2.RequestHandler):
    def get(self):
        """
        """
        # headers
        self.response.headers['Content-Type'] = 'application/json'

        # parameters
        coords = json.loads(self.request.get('coords'))
        viewer = bool(self.request.get('viewer', False))
        dt = self.request.get('date', TODAY)

        # response
        res = json.dumps(dummy.water_service(coords, dt, viewer))
        self.response.write(res)


class DummyDeforestationHandler(webapp2.RequestHandler):
    def get(self):
        """
        """
        # headers
        self.response.headers['Content-Type'] = 'application/json'

        # parameters
        coords = json.loads(self.request.get('coords'))
        viewer = bool(self.request.get('viewer', False))
        begin = self.request.get('begin', '2005-12-15')
        end = self.request.get('end', TODAY)

        # response
        res = json.dumps(dummy.deforestation(coords, begin, end, viewer))
        self.response.write(res)


class DummyBuildingsHandler(webapp2.RequestHandler):
    def get(self):
        """
        """
        # headers
        self.response.headers['Content-Type'] = 'application/json'

        # parameters
        coords = json.loads(self.request.get('coords'))
        viewer = bool(self.request.get('viewer', False))
        dt = self.request.get('end', TODAY)

        # response
        res = json.dumps(dummy.building_service(coords, dt, viewer))
        self.response.write(res)


handlers = webapp2.WSGIApplication([
    ('/api/dummy/cars', DummyCarHandler),
    ('/api/dummy/change', DummyChangeHandler),
    ('/api/dummy/water', DummyWaterHandler),
    ('/api/dummy/buildings', DummyBuildingsHandler),
    ('/api/dummy/deforestation', DummyDeforestationHandler)
], debug=True)
