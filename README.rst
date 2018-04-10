hitbtcapi
===================

REST API Client for HitBTC

|logo|

.. |logo| image:: https://upload.wikimedia.org/wikipedia/en/9/9f/HitBTC_logo.png

Features
=========

- Convenient methods for making API calls using keyword arguments

    - Automatic classification into form-data or query parameters
    - Automatic packing into JSON

- Near 100% test coverage.
- Tab-completable methods and attributes when using `IPython <http://ipython.org/>`_.


Installation
=============

``hitbtcapi`` is available on `PYPI <https://pypi.python.org/pypi>`_. Install with ``pip``:

.. code:: bash

    $ pip install hitbtcapi

or with ``easy_install``:

.. code:: bash

    $ easy_install hitbtcapi

The library is currently tested against Python versions 2.7 and 3.4+.

API Reference
===============

The official documentation can be found on the `HitBTC API reference page <https://api.hitbtc.com/>`_. You can also `explore the API <https://api.hitbtc.com/api/2/explore/>`_ using Swagger UI.


Prerequisites
===============

The first thing you need to do is to `Sign Up with HitBTC <https://hitbtc.com/signupapp>`_.

Next, you need to obtain an **API Key** and an **API Secret**. If you're writing code for your own HitBTC account, you can create API keys on `HitBTC API Settings <https://hitbtc.com/settings/api-keys>`_ page. You can create multiple API keys with different permissions for your applications.

NOTE: Make sure to enable appropriate permissions for the API key (some require email confirmation).

Getting started
=================

Create a ``Client`` object for interacting with the API:

.. code:: python

    from hitbtcapi.client import Client

    api_key = 'your api key'
    api_secret = 'your api secret'

    client = Client(api_key,api_secret)

Error handling
--------------
All errors occurring during interaction with the API will be raised as exceptions. These exceptions will be subclasses of ``hitbtcapi.errors.HitBTCError``. When the error involves an API request and/or response, the error will be a subclass of ``hitbtcapi.errors.APIError``, and include more information about the failed interaction. For full details of error responses, please refer to the `relevant API documentation <https://api.hitbtc.com/#error-response>`_.

+-------------------------+----------------------+
|          Error          |    HTTP Status code  |
+=========================+======================+
| InvalidRequestError     |          400         |
+-------------------------+----------------------+
| AuthenticationError     |          401         |
+-------------------------+----------------------+
| TwoFactorRequiredError  |          402         |
+-------------------------+----------------------+
| InvalidScopeError       |          403         |
+-------------------------+----------------------+
| NotFoundError           |          404         |
+-------------------------+----------------------+
| ValidationError         |          422         |
+-------------------------+----------------------+
| RateLimitExceededError  |          429         |
+-------------------------+----------------------+
| InternalServerError     |          500         |
+-------------------------+----------------------+
| ServiceUnavailableError |          503         |
+-------------------------+----------------------+
| GatewayTimeoutError     |          504         |
+-------------------------+----------------------+

Usage
-------
I've done my best to make the code clean, commented, and understandable; however it may not be exhaustive. For more details, please refer to the `HitBTC API official documentation <https://api.hitbtc.com/>`_ or the `API Explorer <https://api.hitbtc.com/api/2/explore/>`_.

**IN SHORT**

- **Use args for URI paths**
- **Use kwargs for formData or query parameters**


**Public API (Market Data)**

Get available currencies, tokens, ICO etc.

.. code:: python

    client.get_currencies()
    client.get_currency('BTC')


Get currency symbols (currency pairs) traded on HitBTC exchange.

.. code:: python

    client.get_symbols()
    client.get_symbol('ETHBTC')


Get ticker information

.. code:: python

    client.get_tickers()
    client.get_ticker('ETHBTC')


Get trades for a specific symbol

.. code:: python

    client.get_trades('ETHBTC')
    client.get_trades('ETHBTC',sort='ASC',limit=10)

    # Caution: from is a python keyword,
    # so cannot be used as a keyword argument to a function,
    # need to use dict instead
    import datetime
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    params = {
        'from': today.isoformat(),
        'to': yesterday.isoformat()
    }
    client.get_trades('ETHBTC',sort='ASC',limit=10,**params)


Get orderbook (electronic list of buy and sell orders) for a specific symbol, organized by price level

.. code:: python

    client.get_orderbook('ETHBTC')
    client.get_orderbook('ETHBTC',limit=10)


Get candles for a specific symbol (used for `OHLC <https://en.wikipedia.org/wiki/Open-high-low-close_chart>`_)

.. code:: python

    client.get_candles('ETHBTC')
    client.get_candles('ETHBTC', limit=10, period='H1')


**Trading**

Get trading balance for your account

.. code:: python

    client.get_trading_balance()


Get a list of active orders or a specific active order

.. code:: python

    client.get_active_orders()
    client.get_active_orders(symbol='ETHBTC')

    client.get_active_order('840450210')
    client.get_active_order('840450210', wait=30000)


Create a new order

.. code:: python

    client.create_order(symbol='ETHBTC',side='buy',quantity='0.063',price='0.046016') # required parameters
    client.create_order(symbol='ETHBTC',side='buy',quantity='0.063',price='0.046016', type='stopLimit', stopPrice='0.073')


Update an existing order

.. code:: python

    client.update_order('840450210',symbol='ETHBTC',side='buy',quantity='0.063',price='0.046016',timeInForce='GDC')


Cancel all open orders or a specific open order

.. code:: python

    client.cancel_open_orders()
    client.cancel_open_orders(symbol='ETHBTC')

    client.cancel_order('840450210')


Get personal trading commission rate

.. code:: python

    client.get_trading_fee('ETHBTC')


**Trading History**

Get order history

.. code:: python

    client.get_order_history()
    client.get_order_history(symbol='ETHBTC',limit=10)

    # Caution: from is a python keyword,
    # so cannot be used as a keyword argument to a function,
    # need to use dict instead
    import datetime
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    params = {
        'from': today.isoformat(),
        'to': yesterday.isoformat()
    }
    client.get_order_history(symbol='ETHBTC',limit=10,**params)

Get trade history

.. code:: python

    client.get_trade_history()
    client.get_trade_history(symbol='ETHBTC',limit=10)

    # Caution: from is a python keyword,
    # so cannot be used as a keyword argument to a function,
    # need to use dict instead
    import datetime
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    params = {
        'from': today.isoformat(),
        'to': yesterday.isoformat()
    }
    client.get_trade_history(symbol='ETHBTC',limit=10,**params)


Get trades by order

.. code:: python

    client.get_trades_by_orderid('840450210')

**Account Information**

Get account balance

.. code:: python

    client.get_account_balance()

Get deposit address for the cryptocurrency

.. code:: python

    client.get_deposit_address('BTC')

Add deposit address for the cryptocurrency

.. code:: python

    client.add_deposit_address('BTC')

Withdraw cryptocurrency

.. code:: python

    client.withdraw('BTC', amount='0.01', address='sOmE-cuRR-encY-addR-essH') # required parameters
    client.withdraw('BTC', amount='0.01', address='sOmE-cuRR-encY-addR-essH', networkFee='0.0003', includeFee=True, autoCommit=False)


Commit cryptocurrency withdrawal

.. code:: python

    client.commit_withdrawal('d2ce578f-647d-4fa0-b1aa-4a27e5ee597b')

Rollback cryptocurrency withdrawal

.. code:: python

    client.rollback_withdrawal('d2ce578f-647d-4fa0-b1aa-4a27e5ee597b')

Transfer money between trading and account

.. code:: python

    client.transfer_to_trading(currency='BTC',amount='0.023',type='bankToExchange')

Get all transactions or by id

.. code:: python

    client.get_account_transactions()
    client.get_account_transactions(currency='BTC',sort='ASC',limit=10)

    # Caution: from is a python keyword,
    # so cannot be used as a keyword argument to a function,
    # need to use dict instead
    import datetime
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    params = {
        'from': today.isoformat(),
        'to': yesterday.isoformat()
    }
    client.get_trade_history(currency='BTC',sort='ASC',limit=10,**params)

    client.get_account_transaction('d2ce578f-647d-4fa0-b1aa-4a27e5ee597b')


Testing / Contributing
=======================
Any contribution is welcome! The process is simple:

* Fork this repo
* Make your changes
* Run the tests (for multiple versions: preferred)
* Submit a pull request.


Testing for your current python version
------------------------------------------

Tests are run via `nosetest <https://nose.readthedocs.io/en/latest/>`_. To run the tests, clone the repository and then:

.. code:: bash

    # Install the required dependencies
    $ pip install -r requirements.txt
    $ pip install -r test-requirements.txt

    # Run the tests
    $ make tests


If you'd also like to generate an HTML coverage report (useful for figuring out which lines of code are actually being tested), make sure the requirements are installed and then run:

.. code:: bash

    $ make coverage


Testing for multiple python versions
------------------------------------------

I am using `tox <http://tox.readthedocs.io/en/latest/install.html>`_ to run the test suite against multiple versions of Python. Tox requires the appropriate Python interpreters to run the tests in different environments. I would recommend using `pyenv <https://github.com/pyenv/pyenv#installation>`_ for this.


However, the process is a little unintuitive because ``tox`` does not seem to work with multiple versions of python (installed via ``pyenv``) when inside a ``pyenv`` virtual environment. So, first deactivate your pyenv virtual environment:

.. code:: bash

    $ (hitbtcapi-venv) pyenv deactivate


and then install `tox` with pip or easy_install:

.. code:: bash

    $ pip install tox # or
    $ easy_install tox


Install python versions which you want to test:

.. code:: bash

    $ pyenv install 2.7.14
    $ pyenv install 3.5.0
    $ pyenv install 3.6.0

and so forth. Now, in your project directory:

.. code:: bash

    # all versions which are in tox.ini file
    $ pyenv local 2.7.14 3.5.0 3.6.0

    # run the tests for all the above versions
    $ tox


License
=========

This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgements
=================

- `HitBTC REST API example <https://github.com/hitbtc-com/hitbtc-api/blob/master/example_rest.py>`_
