from datetime import datetime

import asyncio
import aiohttp
from aiohttp.hdrs import USER_AGENT, AUTHORIZATION

import json

import logging

from .constants import *

class ConnectedCarsClient(object):
    """Python wrapper for the ConnectedCars REST API.

    Note that it is based on trial and error, there is very little
    official documentation about this API yet, so use at your own risk.
    """

    def __init__(self, username, password):
        """Initialize the class.
        """
        self.username = username
        self.password = password
        self.logger = logging.getLogger(__name__)
        self.token = None

    async def async_refresh_token(self, session):
        try:
            headers = {
                USER_AGENT: '{}/{}'.format('connectedcars-python', '0.1.0'),
            }

            data = {
                'email': self.username,
                'password': self.password
            }

            async with session.post(AUTH_URL,
                                    headers = headers,
                                    json = data,
                                    timeout = API_TIMEOUT) as response:
                self.logger.debug("Request '%s' finished with status code %s", response.url, response.status)
                response_data = await response.json(encoding = 'utf-8')
                self.token = response_data['token']

        except:
            self.logger.exception("While refreshing token.")
            raise

    async def async_query(self, query):
        """Execute the GraphQL query and return results as python dictionary. This also handles auth and token refresh."""
        try:
            async with aiohttp.ClientSession() as session:
                if self.token is None:
                    await self.async_refresh_token(session)

                headers = {
                    USER_AGENT: '{}/{}'.format('connectedcars-python', '0.1.0'),
                    AUTHORIZATION: 'Bearer {}'.format(self.token),
                }
            
                data = {
                    'query': query 
                }

                async with session.post(API_URL,
                                        headers = headers,
                                        json = data,
                                        timeout = API_TIMEOUT) as response:
                    self.logger.debug("Request '%s' finished with status code %s", response.url, response.status)
                    response_data = await response.json(encoding = 'utf-8')
                    return response_data
        except:
            self.logger.exception("While fetching observations")


    def query(self, query):
        """Fetch the latest observations for a given weather station or location."""
        return asyncio.get_event_loop().run_until_complete(self.async_query(query))
