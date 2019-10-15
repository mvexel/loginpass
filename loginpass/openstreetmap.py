"""
    loginpass.twitter
    ~~~~~~~~~~~~~~~~~

    Loginpass Backend of OpenStreetMap (https://openstreetmap.org).

    Useful Links:

    - Create App: https://apps.twitter.com/
    - API documentation: https://developer.twitter.com/

    :copyright: (c) 2018 by Hsiaoming Yang
    :license: BSD, see LICENSE for more details.
"""
from ._core import UserInfo, OAuthBackend
import xml.etree.ElementTree as ET

class OpenStreetMap(OAuthBackend):
    OAUTH_TYPE = '1.0'
    OAUTH_NAME = 'openstreetmap'
    OAUTH_CONFIG = {
        'api_base_url': 'https://www.openstreetmap.org/api/0.6',
        'request_token_url': 'https://www.openstreetmap.org/oauth/request_token',
        'access_token_url': 'https://www.openstreetmap.org/oauth/access_token',
        'authorize_url': 'https://www.openstreetmap.org/oauth/authorize',
    }

    def profile(self):
        url = 'user/details'
        resp = self.get(url)
        resp.raise_for_status()
        data = resp.text
        root = ET.fromstring(data)
        user = root.find("user")
        attrib = user.attrib
        params = {
            'osmid': attrib['id'],
            'display_name': attrib['display_name'],
        }
        username = params['display_name']
        if username:
            params['profile'] = 'https://openstreetmap.org/user/{}'.format(username)
        return UserInfo(params)
