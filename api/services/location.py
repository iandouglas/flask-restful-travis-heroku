import os
import time

import bleach
import inflect
import requests

from api import db
from api.database.models import City


class LocationService:
    @classmethod
    def get_latlng(cls, city, state):
        payload = {
            'lat': float(-90),
            'lng': float(-180),
            'success': True,
            'id': 0
        }
        good_city = None
        good_state = None
        if city:
            good_city = bleach.clean(city.strip())
        else:
            payload['error'] = 'city is required'
            payload['success'] = False
            return payload
        if state:
            good_state = bleach.clean(state.strip())
        else:
            payload['error'] = 'state is required'
            payload['success'] = False
            return payload
        if len(state) != 2:
            payload['error'] = 'state length must be 2 characters'
            payload['success'] = False
            return payload

        city_chk = db.session.query(City).filter_by(
            name=good_city, state=good_state).one_or_none()

        if city_chk is not None:
            payload['lat'] = city_chk.lat
            payload['lng'] = city_chk.lng
            payload['id'] = city_chk.id
            return payload

        res = requests.get(
            'http://www.mapquestapi.com'
            '/geocoding/v1/address'
            f"?key={os.getenv('MAPQUEST_API', 'bad mapquest api key')}"
            f'&location={city},{state}'
        )
        if res.status_code == 200:
            latlng = res.json()['results'][0]['locations'][0]['displayLatLng']
            payload['lat'] = latlng['lat']
            payload['lng'] = latlng['lng']

            city_chk = City(
                name=good_city, state=good_state,
                lat=latlng['lat'], lng=latlng['lng']
            )
            city_chk.insert()
            payload['id'] = city_chk.id

            return payload

        else:
            raise requests.RequestException  # pragma: no cover

    @classmethod
    def route_distance_time(cls, start_city, end_city):
        res = requests.get(
            'http://www.mapquestapi.com'
            '/directions/v2/route'
            f"?key={os.getenv('MAPQUEST_API', 'bad mapquest api key')}"
            f'&from={start_city.city_state()}'
            f'&to={end_city.city_state()}'
        )
        if res.status_code == 200:
            p = inflect.engine()
            route = res.json()['route']
            if 'formattedTime' in route:
                bits = [int(b) for b in route['formattedTime'].split(':')]
                eta = []
                if bits[0] > 0:
                    eta.append(f'{bits[0]} {p.plural("hour", bits[0])}')
                if bits[1] > 0:
                    eta.append(f'{bits[1]} {p.plural("minute", bits[1])}')
                return {
                    'string': ', '.join(eta),
                    'seconds': route['time']
                }

            return {'string': 'impossible route'}
