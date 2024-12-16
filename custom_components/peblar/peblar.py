"""Peblar class"""

import json

import requests


class Peblar:
    def __init__(self, token, address, requestGetTimeout=None):
        self.token = token
        self.address = address
        self._requestGetTimeout = requestGetTimeout
        self.baseUrl = "http://" + self.address + "/api/wlac/v1/"
        self.headers = {
            "Content-type": "application/json",
            "Authorization": f"{self.token}",
        }

    @property
    def requestGetTimeout(self):
        return self._requestGetTimeout

    def authenticate(self):
        try:
            response = requests.get(
                f"{self.baseUrl}system",
                headers=self.headers,
                timeout=self._requestGetTimeout,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise (err)

    def getChargerData(self):
        try:
            response = requests.get(
                f"{self.baseUrl}system",
                headers=self.headers,
                timeout=self._requestGetTimeout,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise (err)
        result1 = json.loads(response.text)
        try:
            response = requests.get(
                f"{self.baseUrl}meter",
                headers=self.headers,
                timeout=self._requestGetTimeout,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise (err)
        result2 = json.loads(response.text)
        try:
            response = requests.get(
                f"{self.baseUrl}evinterface",
                headers=self.headers,
                timeout=self._requestGetTimeout,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise (err)
        result3 = json.loads(response.text)
        return result1 | result2 | result3

    def setMaxChargingCurrent(self, newMaxChargingCurrentValue):
        try:
            response = requests.patch(
                f"{self.baseUrl}evinterface",
                headers=self.headers,
                data=f'{{ "ChargeCurrentLimit": {newMaxChargingCurrentValue}}}',
                timeout=self._requestGetTimeout,
            )
        except requests.exceptions.HTTPError as err:
            raise (err)
        return json.loads(response.text)
