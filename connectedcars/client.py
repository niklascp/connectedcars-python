from datetime import datetime

from typing import List

import asyncio
import aiohttp
from aiohttp.hdrs import ACCEPT, CONTENT_TYPE, AUTHORIZATION, USER_AGENT

import json

import logging

from .constants import *
from .models import *
from .exceptions import *

class ConnectedCarsClient(object):
    """Python wrapper for the ConnectedCars REST API.

    Note that it is based on trial and error, there is very little
    official documentation about this API yet, so use at your own risk.
    """

    def __init__(self, username, password, namespace):
        """Initialize the class.
        """
        self.username = username
        self.password = password
        self.namespace = namespace
        self.logger = logging.getLogger(__name__)
        self.token = None
        self.retry = 0

    async def async_refresh_token(self, session, timeout = API_DEFAULT_TIMEOUT):
        """Refresh client token."""
        try:
            headers = {
                ACCEPT: 'application/json',
                CONTENT_TYPE: 'application/json',
                USER_AGENT: '{}/{}'.format('connectedcars-python', '0.1.1'),
                HEADER_NAMESPACE: self.namespace
            }

            data = {
                'email': self.username,
                'password': self.password
            }

            async with session.post(AUTH_URL,
                                    headers = headers,
                                    json = data,
                                    timeout = timeout) as response:
                self.logger.debug("Request '%s' finished with status code %s", response.url, response.status)

                if response.status == 200:
                    response_data = await response.json(encoding = 'utf-8')
                    self.token = response_data['token']
                else:
                    raise ConnectedCarsException("Unexpected response: '{}'".format(await response.text()))
                    
        except Exception as e:
            self.logger.exception("While refreshing token")
            raise ConnectedCarsException from e

    async def async_query(self, query, timeout = API_DEFAULT_TIMEOUT):
        """Execute the GraphQL query and return results as python dictionary. This also handles auth and token refresh."""
        try:
            async with aiohttp.ClientSession() as session:
                if self.token is None:
                    await self.async_refresh_token(session)

                while self.retry < 2:

                    headers = {
                        ACCEPT: 'application/json',
                        CONTENT_TYPE: 'application/json',
                        USER_AGENT: '{}/{}'.format('connectedcars-python', '0.1.2'),
                        HEADER_NAMESPACE: self.namespace,
                        AUTHORIZATION: 'Bearer {}'.format(self.token)
                    }
                
                    data = {
                        'query': query 
                    }
    
                    async with session.post(API_URL,
                                            headers = headers,
                                            json = data,
                                            timeout = timeout) as response:
                        self.logger.debug("Request '%s' finished with status code %s", response.url, response.status)

                        if response.status == 401:
                            self.logger.debug(await response.text())
                            await self.async_refresh_token(session)
                            self.retry = self.retry + 1
                            continue
                        elif response.status == 200:
                            response_data = await response.json(encoding = 'utf-8')
                            self.retry = 0
                            return response_data
                        else:
                            raise ConnectedCarsException("Unexpected response: '{}'".format(await response.text()))
        except Exception as e:
            self.logger.exception("While executing query")
            raise ConnectedCarsException from e
    
    async def async_vehicles_overview(self, timeout = API_DEFAULT_TIMEOUT) -> List[Vehicle]:    
        response = await self.async_query(QUERY_VEHICLE_OVERVIEW, timeout)
        try:
            return [
                Vehicle.create_from_dict(vehicle_data['vehicle'])
                for vehicle_data in response['data']['viewer']['vehicles']
            ]
        except KeyError as e:
            raise ConnectedCarsInvalidResponse from e

    def query(self, query, timeout = API_DEFAULT_TIMEOUT):
        """Fetch the latest observations for a given weather station or location."""
        return asyncio.get_event_loop().run_until_complete(self.async_query(query, timeout))

    def vehicles_overview(self, timeout = API_DEFAULT_TIMEOUT) -> List[Vehicle]:
        """Fetch the latest observations for a given weather station or location."""
        return asyncio.get_event_loop().run_until_complete(self.async_vehicles_overview(timeout))
