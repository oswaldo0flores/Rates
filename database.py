# HW5 - Rates     Oswaldo Flores
"""
This module will handle the CRUD operations.

The TreasuryReportingRatesOfExchangeApiFacade class will be an abstract class with static methods.
The class will represent an API Facade for the Treasury Reporting Rates of Exchange. The get method
will get data in json (key value pair). If any error occurs a None type will replace the json.
The GetApiFacade class is a TreasuryReportingRatesOfExchangeApiFacade. The GetApiFacade class
will represent the GET in an Api. This class contains methods for getting the countries count,
country names, and a single country information. All of those methods can have errors so a None type
is return if an error occur.

BASE_URL: The base URL in an API operation.
END_POINT: The end part of the URL.
DATE: The date we get our information from.
FORMAT: How the data will be formatted.
COUNTRY_FIELD: Data to get during an API GET operations. I should get country.
COUNTRY_CURRENCY_DESC_FIELD: Data to get during an API GET operations. I should get country currency description.
EXCHANGE_RATE_FIELD: Data to get during an API GET operations. I should get the exchange rate.
COUNTRY_FILTER: Data to filter during any API operations. I should filter a country.
RECORD_DATE_FIELD: Data to get during an API GET operations. I should get a record date.
COUNTRY_KEY: Key part for a key value pair. The key is country.
META_KEY: Key part for a key value pair. The key is meta.
TOTAL_COUNT_KEY: Key part for a key value pair. The key is total-count.
DATA_KEY: Key part for a key value pair. The key is data.
COUNTRY_CURRENCY_DESC_KEY: Key part for a key value pair. The key is country_currency_desc.
EXCHANGE_RATE_KEY: Key part for a key value pair. The key is exchange_rate.
"""
import json
import requests

from abc import ABC


class TreasuryReportingRatesOfExchangeApiFacade(ABC):
    BASE_URL = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/'

    @staticmethod
    def get(end_point: str, params: dict) -> json or None:
        """
        To get data using an API.

        To get data using an Api. The data will be in a json format because it is easier
        to maintain the data. The end point and parameters will determine which data to get
        from the Api. The Api site can go down at any time, so I need to make sure I can make a
        request data from the site. If any error message shows up, I need to catch those error message
        and return None. The None will tell the other modules that something went wrong with the Api.

        :param end_point: End part of the url. The url connects to another computer software.
        :type end_point: str
        :param params: Parameters of the end point. Will determine which data I will get.
        :type params: dict
        :return: None if an error occur. Json if requesting data was successful.
        """
        url = f'{TreasuryReportingRatesOfExchangeApiFacade.BASE_URL}{end_point}'
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None


class GetApiFacade(TreasuryReportingRatesOfExchangeApiFacade):
    END_POINT = 'v1/accounting/od/rates_of_exchange'
    DATE = 'record_date:eq:2022-12-31'
    FORMAT = 'json'
    COUNTRY_FIELD = 'country'
    COUNTRY_CURRENCY_DESC_FIELD = 'country_currency_desc'
    EXCHANGE_RATE_FIELD = 'exchange_rate'
    COUNTRY_FILTER = 'country:eq:'
    RECORD_DATE_FIELD = 'record_date'
    COUNTRY_KEY = 'country'
    META_KEY = 'meta'
    TOTAL_COUNT_KEY = 'total-count'
    DATA_KEY = 'data'
    COUNTRY_CURRENCY_DESC_KEY = 'country_currency_desc'
    EXCHANGE_RATE_KEY = 'exchange_rate'

    @staticmethod
    def get_countries_count() -> None or int:
        """
        To get the countries count.

        To get the countries count. This method will use this class end point and this method
        params to call the get method in the parent class. The get method can return json or None.
        If the get method returns None, just get the None instead of the countries count. If no error
        occur, the get method in the parent class will return a json (key value pair). Using the keys
        that is given from the Api documentation, get the countries count.

        :return: None if an error occurs. Countries count if no error occur.
        """
        params = {
            'fields': GetApiFacade.COUNTRY_FIELD,
            'filter': GetApiFacade.DATE,
            'format': GetApiFacade.FORMAT
        }
        response = TreasuryReportingRatesOfExchangeApiFacade.get(GetApiFacade.END_POINT, params)
        if response is None:
            return response
        else:
            return response[GetApiFacade.META_KEY][GetApiFacade.TOTAL_COUNT_KEY]

    @staticmethod
    def get_countries(countries_count: int) -> None or list:
        """
        To get a list of country names.

        To get a list of country names with a given countries count. This method will use this class
        end point and this method params to call the get method in the parent class. The get method
        can return json or None. If the get method returns None, just get the None value because an
        error occur. If the get method returns json, iterator over the json to get the country names.
        Use the keys from the Api documentation to get the correct data. The countries count will
        determine how many countries to get.

        :param countries_count: Number of countries to get.
        :type countries_count: int
        :return: None if an error occur. List if no error occur.
        """
        params = {
            'fields': GetApiFacade.COUNTRY_FIELD,
            'page[size]': countries_count,
            'filter': GetApiFacade.DATE
        }
        response = TreasuryReportingRatesOfExchangeApiFacade.get(GetApiFacade.END_POINT, params)
        if response is None:
            return response
        else:
            countries = []
            for period in response[GetApiFacade.DATA_KEY]:
                countries.append(period[GetApiFacade.COUNTRY_KEY])
            return countries

    @staticmethod
    def get_single_country(country_name: str) -> None or list:
        """
        To get a single country data.

        To get a single country data with a given country name. This method will use this class
        end point and this method params to call the get method in the parent class. The get method
        can return json or None. If the get method return None, just get the None value because an
        error has occurred when connecting to the site. If the get method return a json, the connection
        was successful, and I have data to get. Iterate over the json to get a country's data. Use the
        keys from the Api documentation to get the correct data. I already know the country name is
        valid because data validation happen in the ui module.

        :param country_name: A country's name.
        :type country_name: str
        :return: None if an error occur. List of a single country's data if no error occur.
        """
        params = {
            'fields': f'{GetApiFacade.COUNTRY_CURRENCY_DESC_FIELD},{GetApiFacade.EXCHANGE_RATE_FIELD},'
                      f'{GetApiFacade.RECORD_DATE_FIELD}',
            'filter': f'{GetApiFacade.COUNTRY_FILTER}{country_name},{GetApiFacade.DATE}'
        }
        response = TreasuryReportingRatesOfExchangeApiFacade.get(GetApiFacade.END_POINT, params)
        if response is None:
            return response
        else:
            country_currency = ''
            exchange_rate = 0.0
            record_date = ''
            for period in response['data']:
                country_currency = period['country_currency_desc']
                exchange_rate = float(period['exchange_rate'])
                record_date = period['record_date']
            return [country_currency, exchange_rate, record_date]
