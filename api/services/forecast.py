import os
import requests


class ForecastService:
    @classmethod
    def get_forecast(cls, latlng, hourly=False):
        payload = {
            'current_temp': '',
            'conditions': '',
            'success': True,
        }
        if latlng and 'success' in latlng and latlng['success']:
            res = requests.get(
                'https://api.openweathermap.org'
                '/data/2.5/onecall'
                f"?appid={os.getenv('OPENWEATHER_API', 'bad openweather api key')}"
                f"&lat={latlng['lat']}"
                f"&lon={latlng['lng']}"
                f"&exclude=minutely,alerts,daily"
                f"&units=imperial"
            )
            if res.status_code == 200:
                data = res.json()
                forecast = data['current']
                payload['current_temp'] = f"{forecast['temp']}F"
                payload['conditions'] = forecast['weather'][0]['description']
                if hourly:
                    payload['hourly'] = data['hourly']
            else:
                raise requests.RequestException  # pragma: no cover
        else:
            payload['success'] = False

        return payload
