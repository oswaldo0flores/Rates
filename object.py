# HW5 - Rates     Oswaldo Flores
"""
To handle a single country and a list of countries.

The SingleCountry represents a single country. The class contains an init to
initialize the class, a str to set what the user is allowed to see, a method
to get country currency description, a method to get the exchange rate, a method
to get a record date, a method to calculate exchange rate with is this class
exchange rate to a given value, and a method to load in a single country from
the database module.
The Countries represent a list of country names only. The class contains an init to
initialize the class, a len to get the length of the list, an iter to iterate over the list,
a str to set what the data should look like to the user, a contains to find a country with a
given value, a get countries to get the whole list, get countries count to get how many countries
should be in the list, and a load countries method to load in a list of countries from the database
module.

COUNTRY_CURRENCY_DESC_INDEX: The index where country currency desc is located in.
EXCHANGE_RATE_INDEX: The index where exchange rate is located in.
RECORD_DATE_INDEX: The index where record date is located in.
"""
from database import GetApiFacade
from dataclasses import dataclass, field


@dataclass
class SingleCountry:
    __country_currency_desc: str
    __exchange_rate: float
    __record_date: str
    COUNTRY_CURRENCY_DESC_INDEX = 0
    EXCHANGE_RATE_INDEX = 1
    RECORD_DATE_INDEX = 2

    def __init__(self, country_currency_desc: str = '', exchange_rate: float = 0.0,
                 record_date: str = '') -> None:
        """
        To initialize the class.

        To initialize the class with a given country currency desc, exchange rate, and
        a record date. I assume the data is valid because data validation should not happen
        here. All three fields in this class can have a default value of an empty string or
        a zero.

        :param country_currency_desc: The currency of a country.
        :type country_currency_desc: str
        :param exchange_rate: The exchange rate for a country's currency.
        :type exchange_rate: float
        :param record_date: The date of the exchange rate.
        :type record_date: str
        """
        self.__country_currency_desc = country_currency_desc
        self.__exchange_rate = exchange_rate
        self.__record_date = record_date

    def __str__(self) -> str:
        """
        To display what data the user is allowed to see.

        To display what data the user is allowed to see if the user decides to print out the object
        of this class. This method also formats the data to make it more readable.

        :return: The formatted data that is display to the user.
        """
        return f'{self.__country_currency_desc}, {self.__exchange_rate}, {self.__record_date}'

    def get_country_currency_desc(self) -> str:
        """
        To get country currency desc.

        To get country currency desc. It can contain an empty string or a country currency.

        :return: An empty string or a country currency.
        """
        return self.__country_currency_desc

    def get_exchange_rate(self) -> float:
        """
        To get the exchange rate.

        To get the exchange rate of a currency. It can contain a rate of 0.0 or a country's
        exchange rate.

        :return: A rate of 0.0 or a country's exchange rate.
        """
        return self.__exchange_rate

    def get_record_date(self) -> str:
        """
        To get the record date.

        To get the record date of the exchange rate. It can contain an empty string
        or a date of the exchange rate.

        :return: An empty string or a date.
        """
        return self.__record_date

    def calculate_exchange_rate(self, value: float or int) -> float or int:
        """
        To calculate the exchange rate.

        To calculate the exchange rate with a given value. Validating the value
        should not happen here, it should happen in the ui module. Multiply the
        value with this class exchange rate to get this class country's currency
        amount.

        :param value: The amount of currency in USD.
        :type value: float or int
        :return: This class country's currency amount.
        """
        return value * self.__exchange_rate

    def load_single_country(self, country_name: str) -> None:
        """
        To load in a single country.

        To load in a single country from the database module. Since the database module can
        return a None type in case of an error, do not set the fields because it has default
        values already. If the data is not None, I assume the data I am getting is valid because
        data validation should not happen here.

        :param country_name: The name of a country.
        :type country_name: str
        """
        country = GetApiFacade.get_single_country(country_name)
        if country is not None:
            self.__country_currency_desc = country[self.COUNTRY_CURRENCY_DESC_INDEX]
            self.__exchange_rate = country[self.EXCHANGE_RATE_INDEX]
            self.__record_date = country[self.RECORD_DATE_INDEX]


@dataclass
class Countries:
    __countries: list = field(default_factory=list)

    def __init__(self) -> None:
        """
        To initialize this class.

        To initialize this class with an empty list. This class should have a mutable list because
        at the start of this application I do not know how many countries I am getting.
        """
        self.__countries = []

    def __len__(self) -> int:
        """
        To get the length of the list.

        To get the length of the list.

        :return: Length of the list.
        """
        return len(self.__countries)

    def __iter__(self):
        """
        To iterate over the list.

        To iterate over the list. Yields every country name in the list.

        :yield: A country name.
        """
        for country in self.__countries:
            yield country

    def __str__(self) -> str:
        """
        To display what data the user is allowed to see.

        To display what data the user is allowed to see. This method can
        also format the data to make it more readable.

        :return: The formatted data that is display to the user.
        """
        return '\n'.join(map(str, self.__countries))

    def __contains__(self, country: str) -> str:
        """
        To find a country.

        To find a country if it exists within the list.

        :param country: The name of a country.
        :type country: str
        :return: The name of the country that exists within the list.
        """
        if country in self.__countries:
            return country

    def get_countries(self) -> list:
        """
        To get the list of countries.

        To get the list of countries. This list can be empty or contains a list
        of country's names.

        :return: An empty list or a list of country's names.
        """
        return self.__countries

    @staticmethod
    def get_countries_count() -> float:
        """
        To get a countries count.

        To get a countries count. This method communicates with the database module.

        :return: A countries count.
        """
        return GetApiFacade.get_countries_count()

    def load_countries(self, countries_count: float) -> None:
        """
        To load countries in.

        To load in countries from the database module. Since an error can appear in the database
        module, the database module can return None data type. This means this class list will be
        empty if an error occurs. If no error occurs put the countries names into the list. The
        countries count will determine how many countries to get in the database module.

        :param countries_count: The countries count.
        :type countries_count: float
        """
        countries = GetApiFacade.get_countries(countries_count)
        if countries is not None:
            self.__countries.clear()
            self.__countries.extend(countries)
