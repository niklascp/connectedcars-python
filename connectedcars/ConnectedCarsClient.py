from datetime import datetime

import asyncio
import aiohttp
from aiohttp.hdrs import ACCEPT, CONTENT_TYPE, AUTHORIZATION, USER_AGENT

import json

import logging

from .constants import *
from .models import Vehicle

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
        self.retry = 0

    async def async_refresh_token(self, session):
        try:
            headers = {
                ACCEPT: 'application/json',
                CONTENT_TYPE: 'application/json',
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
            self.logger.exception("While refreshing token")
            raise

    async def async_query(self, query):
        """Execute the GraphQL query and return results as python dictionary. This also handles auth and token refresh."""
        try:
            async with aiohttp.ClientSession() as session:
                if self.token is None:
                    await self.async_refresh_token(session)

                while self.retry < 2:

                    headers = {
                        ACCEPT: 'application/json',
                        CONTENT_TYPE: 'application/json',
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

                        if response.status == 401:
                            self.logger.debug(await response.text())
                            await self.async_refresh_token(session)
                            self.retry = self.retry + 1
                            continue
                        else:
                            response_data = await response.json(encoding = 'utf-8')
                            self.retry = 0
                            return response_data
        except:
            self.logger.exception("While executing query")
            raise
    
    async def async_vehicles_overview(self):    
        response = await self.async_query(QUERY_VEHICLE_OVERVIEW)
        return [
            Vehicle.create_from_dict(vehicle_data['vehicle'])
            for vehicle_data in response['data']['viewer']['vehicles']
        ]

    def query(self, query):
        """Fetch the latest observations for a given weather station or location."""
        return asyncio.get_event_loop().run_until_complete(self.async_query(query))

    def vehicles_overview(self):
        """Fetch the latest observations for a given weather station or location."""
        return asyncio.get_event_loop().run_until_complete(self.async_vehicles_overview())
