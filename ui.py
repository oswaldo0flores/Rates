# HW5 - Rates     Oswaldo Flores
"""
Handles user input and output.

The run method will be use in the main module to run the program. The
print exchange currency method will use methods from the object module
to get an exchange rate amount and will print that exchange amount.
The print loads methods will tell the user how many countries are loaded
in when the application starts. The user country method will get a string
from the user. The validated user country method is to validate the user
string to determine if the program should stop or if the user enter a
country's name. The user amount will get a string from the user.
The validated user amount will determine if the user enter a number and
if the number is greater than the minimum.

STANDARD_EMTPY_LIST: The list contains zero values.
"""
from object import Countries, SingleCountry

STANDARD_EMTPY_LIST = 0


def run() -> None:
    """
    To run the application.

    The main module will use this method to run the application. The application needs to start
    with a countries count greater than zero. Loading in the countries will be handled by
    the database module. Putting the data into a list will be handled by the objects class.
    The database will handle the connection if no connection is made, this application should end.
    Another way to end this application is if the user enter the word stop. Casing should not matter.
    Once the user successfully enter a country's name, get their amount.
    :return: Close the application by the user or by an error.
    """
    countries_count = Countries.get_countries_count()
    if countries_count is not None:
        print_loads(countries_count)
        countries = Countries()
        countries.load_countries(countries_count)
        if len(countries) > STANDARD_EMTPY_LIST:
            while True:
                country = validated_user_country(countries)
                if country.upper() == 'STOP':
                    return
                else:
                    amount = validated_user_amount()
                    print_exchange_currency(amount, country)
        else:
            print('An error has occur.')
            return
    else:
        print('An error has occur.')
        return


def print_exchange_currency(amount: float, country: str) -> None:
    """
    To print the exchange rate.

    To print the exchange rate with the given amount and with the given country.
    Calculating the new exchange rate, getting the country currency description,
    and getting the date of exchange will be in the object module. The print statement
    should contain the original amount, the new exchange rate amount with the type of currency,
    and the date of the exchange rate.

    :param amount: User's amount in USD.
    :type amount: float
    :param country: The name of a chosen country.
    :type country: str
    """
    single_country = SingleCountry()
    single_country.load_single_country(country)
    country_currency_desc = single_country.get_country_currency_desc()
    date = single_country.get_record_date()
    amount_with_rate = single_country.calculate_exchange_rate(amount)
    print(f'{amount} USD is {amount_with_rate:.2f} {country_currency_desc}', end=' ')
    print(f'as of {date}')
    print()


def print_loads(countries_count: int or None) -> None:
    """
    To print how many countries are loaded in.

    To print how many countries are loaded in once the applications starts.
    The reason why countries count can have a None type is because if the
    API fails to connection in the database module, it will return a None
    type.

    :param countries_count: The number of countries loaded in.
    :type countries_count: int or None
    """
    print('Load Countries...')
    print(f'{countries_count} countries found')


def user_country(prompt: str = 'Enter the country name (STOP to quit) > ') -> str:
    """
    To get a country's name.

    To get an unvalidated country's name from the user. No data validation should
    have here.

    :param prompt: Prompt the user for a country's name.
    :type prompt: str
    :return: An unvalidated string that might be a country's name.
    """
    return input(prompt)


def validated_user_country(countries: Countries,
                           stop: str = 'STOP', prompt: str = 'Enter the country name (STOP to quit) > ') -> str:
    """
    To validate user unvalidated string.

    To validate user unvalidated string to make sure it's a country's name. The
    user must enter stop or a country's name in order to move on from this method. The
    casing should not matter at all.

    :param countries: An object that can act as a list of countries.
    :type countries: Countries
    :param stop: The word STOP.
    :type stop: str
    :param prompt: Prompt the user for a country's name.
    :type prompt: str
    :return: A country's name or the word STOP to end the application.
    """
    is_input_unvalidated = True
    while is_input_unvalidated:
        country = user_country(prompt)
        if country.upper() == stop:
            return country
        for a_country in countries:
            if country.lower() == a_country.lower():
                return a_country
        else:
            print('Country not found, try again')


def user_amount(prompt: str = 'Enter the amount of exchange > ') -> str:
    """
    An unvalidated user amount.

    An unvalidated user amount from the user. No data validation should
    happen here.

    :param prompt: Prompt the user for an amount.
    :type prompt: str
    :return: An unvalidated amount from the user.
    """
    return input(prompt)


def validated_user_amount(prompt: str = 'Enter the amount of exchange > ', minimum: float = 0.0) -> float:
    """
    To validate user amount.

    To validate user amount with the given minimum. Make sure the amount is
    a float data type and is greater than the given minimum. The user need to enter
    a valid amount to move on from this method.

    :param prompt: Prompt the user for an amount.
    :type prompt: str
    :param minimum: Minimum amount the user can enter.
    :type minimum: float
    :return: The validated amount.
    """
    while True:
        amount = user_amount(prompt)
        try:
            if float(amount):
                if float(amount) > minimum:
                    return float(amount)
        except:
            amount = user_amount(prompt)
