# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six
import unittest2
import json
import re
import warnings
import httpretty as hp

from hitbtcapi import errors
from hitbtcapi.client import Client

# Hide all warning output.
warnings.showwarning = lambda *a, **k: None

# Dummy API key values for use in tests
api_key = 'fakeapikey'
api_secret = 'fakeapisecret'

mock_items = {'key1': 'val1', 'key2': 'val2'}
mock_items_send = {'s1':'v1', 's2':'v2', 's3': 0}
mock_collection = [mock_items, mock_items]


class TestClient(unittest2.TestCase):
    def test_key_and_secret_required(self):
        with self.assertRaises(ValueError):
            Client(None,api_secret)
        with self.assertRaises(ValueError):
            Client(api_key,None)

    @hp.activate
    def test_auth_succeeds_with_string_unicode_and_bytes(self):
        mock_response = {'body':'{}',
                         'status':200}
        # String
        api_key = 'fakekey'
        api_secret = 'fakesecret'
        self.assertIsInstance(api_key, six.string_types)
        self.assertIsInstance(api_secret, six.string_types)

        client = Client(api_key, api_secret)
        hp.register_uri(hp.GET,re.compile('.*test$'),**mock_response)
        self.assertEqual(client._get('test').status_code,200)

        # Unicode
        api_key = u'fakekey'
        api_secret = u'fakesecret'
        self.assertIsInstance(api_key, six.text_type)
        self.assertIsInstance(api_secret, six.text_type)

        client = Client(api_key, api_secret)
        hp.register_uri(hp.GET,re.compile('.*test$'),**mock_response)
        self.assertEqual(client._get('test').status_code,200)

        # Bytes
        api_key = api_key.encode('utf-8')
        api_secret = api_secret.encode('utf-8')
        self.assertIsInstance(api_key, six.binary_type)
        self.assertIsInstance(api_secret, six.binary_type)

        client = Client(api_key, api_secret)
        hp.register_uri(hp.GET,re.compile('.*test$'),**mock_response)
        self.assertEqual(client._get('test').status_code,200)

    @hp.activate
    def test_base_api_uri_used_instead_of_default(self):
        # Requests to the default BASE_API_URI will noticeably fail by raising an AssertionError. Requests to the new URL will respond HTTP 200.
        new_base_api_uri = 'https://api.hitbtc.com/api/new/'
        # If any error is raised by the server, the test suite will never exit when using Python 3. This strange technique is used to raise the errors outside of the mocked server environment.
        errors_in_server = []
        def mock_response(request,uri,headers):
            try:
                self.assertEqual(uri,new_base_api_uri)
            except AssertionError as e:
                errors_in_server.append(e)
            return 200,headers,'{}'

        hp.register_uri(hp.GET,Client.BASE_API_URI,mock_response)
        hp.register_uri(hp.GET,new_base_api_uri,mock_response)

        client = Client(api_key,api_secret) # default BASE_API_URI
        client_new = Client(api_key,api_secret,new_base_api_uri)

        self.assertEqual(client_new._get().status_code,200)
        with self.assertRaises(AssertionError):
            client._get()
            if errors_in_server:
                raise errors_in_server.pop()

    @hp.activate
    def test_http_base_api_uri_issues_uri_security_warning(self):
        insecure_url = 'http://api.hitbtc.com/api/1/'
        with self.assertWarns(UserWarning):
            client = Client(api_key,api_secret,insecure_url)
            # check if response is OK even with insecure_url
            mock_response = {'body':'{}',
                             'status':200}
            hp.register_uri(hp.GET,insecure_url,**mock_response)
            self.assertEqual(client._get().status_code,200)


    @hp.activate
    def test_200_response_handling(self):
        # check if 200 response returns a json decoded response
        client = Client(api_key, api_secret)
        mock_response = {'body':json.dumps(mock_items),
                         'status':200}
        hp.register_uri(hp.GET,re.compile('.*test$'),**mock_response)
        response = client._get('test')
        self.assertEqual(client._handle_response(response),mock_items)

    @hp.activate
    def test_error_response_handling(self):
        client = Client(api_key, api_secret)
        # check if appropriate error is raised depending on status code
        # AND if error data is in response, it is used
        error_body = {'error': {'id': 0,
                                'message': 'fake error message',
                                'description': 'fake error description'}}
        for ecode,eclass in six.iteritems(errors._status_code_to_class):
            mock_response = {'body':json.dumps(error_body),
                             'status':ecode}
            hp.register_uri(hp.GET,re.compile('.*'+str(ecode)+'$'),**mock_response)
            with self.assertRaises(eclass):
                e = client._handle_response(client._get(str(ecode)))
                self.assertEqual(e.error_msg,'fake error message')
                self.assertEqual(e.error_desc,'fake error description')

        # check if appropriate error raised even with no error message in body or if content-type is not text/json
        for ecode,eclass in six.iteritems(errors._status_code_to_class):
            mock_response = {'status':ecode,
                             'content_type':'text/plain'}
            hp.register_uri(hp.GET,re.compile('.*'+str(ecode)+'$'),**mock_response)
            with self.assertRaises(eclass):
                client._handle_response(client._get(str(ecode)))

        # check if status code is unrecognized, generic APIError is raised
        mock_response = {'status':418}
        hp.register_uri(hp.GET,re.compile('.*test$'),**mock_response)
        with self.assertRaises(errors.APIError):
            client._handle_response(client._get('test'))

    @hp.activate
    def test_request_helper_automatically_encodes_data(self):
        client = Client(api_key, api_secret)
        def mock_response(request,uri,headers):
            self.assertIsInstance(request.body, six.binary_type)
            return 200, headers, '{}'
        hp.register_uri(hp.POST,re.compile('.*test$'),mock_response)
        self.assertEqual(client._post('test',data=mock_items).status_code,200)

    # --------------------
    #   TEST PUBLIC API
    # --------------------
    @hp.activate
    def test_get_symbols(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*public/symbol$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_symbols(),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_symbol(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.GET,re.compile('.*'+'public/symbol/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_symbol('foo'),mock_items)
        hp.reset()

    @hp.activate
    def test_get_currencies(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*public/currency$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_currencies(),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_currency(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.GET,re.compile('.*'+'public/currency/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_currency('foo'),mock_items)
        hp.reset()

    @hp.activate
    def test_get_tickers(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*public/ticker$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_tickers(),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_ticker(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.GET,re.compile('.*public/ticker/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_ticker('foo'),mock_items)
        hp.reset()

    @hp.activate
    def test_get_trades(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*public/trades/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_trades('foo'),mock_collection)
        self.assertEqual(client.get_trades('foo',**mock_items_send),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_orderbook(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.GET,re.compile('.*public/orderbook/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_orderbook('foo'),mock_items)
        self.assertEqual(client.get_orderbook('foo',**mock_items_send),mock_items)
        hp.reset()

    @hp.activate
    def test_get_candles(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.GET,re.compile('.*public/candles/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_candles('foo'),mock_items)
        self.assertEqual(client.get_candles('foo',**mock_items_send),mock_items)
        hp.reset()

    # --------------------
    #   TEST TRADING API
    # --------------------
    @hp.activate
    def test_get_active_orders(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*order$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_active_orders(),mock_collection)
        self.assertEqual(client.get_active_orders(**mock_items_send),mock_collection)
        hp.reset()

    @hp.activate
    def test_create_order(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*order$'),**mock_response)
        client = Client(api_key,api_secret)
        required_params = {'symbol':'foo','side':'sell','quantity':'1.0','price':'1.0'}
        send_params = {}
        while required_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.create_order(**send_params)
            for key in required_params:
                send_params[key] = required_params.pop(key)
                break
        self.assertEqual(client.create_order(**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_cancel_open_orders(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.DELETE,re.compile('.*order$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.cancel_open_orders(),mock_items)
        self.assertEqual(client.cancel_open_orders(**mock_items_send),mock_items)
        hp.reset()

    @hp.activate
    def test_get_active_order(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.GET,re.compile('.*order/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_active_order('foo'),mock_items)
        self.assertEqual(client.get_active_order('foo',**mock_items_send),mock_items)
        hp.reset()

    @hp.activate
    def test_update_order(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.PUT,re.compile('.*order/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        required_params = {'symbol':'foo','side':'sell','quantity':'1.0','price':'1.0','timeInForce':'GTC'}
        send_params = {}
        while required_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.update_order('foo',**send_params)
            for key in required_params:
                send_params[key] = required_params.pop(key)
                break
        self.assertEqual(client.update_order('foo',**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_cancel_order(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.DELETE,re.compile('.*order/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.cancel_order('foo'),mock_items)
        hp.reset()

    @hp.activate
    def test_cancel_replace_order(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.PATCH,re.compile('.*order/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        required_params = {'quantity':'1.0','requestClientId':'bar'}
        send_params = {}
        while required_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.cancel_replace_order('foo',**send_params)
            for key in required_params:
                send_params[key] = required_params.pop(key)
                break
        self.assertEqual(client.cancel_replace_order('foo',**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_get_trading_balance(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.GET,re.compile('.*trading/balance$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_trading_balance(),mock_items)
        hp.reset()

    @hp.activate
    def test_get_trading_fee(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.GET,re.compile('.*trading/fee/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_trading_fee('foo'),mock_items)
        hp.reset()

    # ----------------------
    #  TEST TRADE HISTORY API
    # -----------------------
    @hp.activate
    def test_get_trade_history(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*history/trades$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_trade_history(),mock_collection)
        self.assertEqual(client.get_trade_history(**mock_items_send),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_order_history(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*history/order$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_order_history(),mock_collection)
        self.assertEqual(client.get_order_history(**mock_items_send),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_trades_by_order_id(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*history/order/foo/trades$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_trades_by_orderid('foo'),mock_collection)
        hp.reset()

    # --------------------
    #   TEST ACCOUNT API
    # --------------------
    @hp.activate
    def test_get_account_balance(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*account/balance$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_account_balance(),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_account_transactions(self):
        mock_response = {'body':json.dumps(mock_collection)}
        hp.register_uri(hp.GET,re.compile('.*account/transactions$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_account_transactions(),mock_collection)
        self.assertEqual(client.get_account_transactions(**mock_items_send),mock_collection)
        hp.reset()

    @hp.activate
    def test_get_account_transaction(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.GET,re.compile('.*account/transactions/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_account_transaction('foo'),mock_items)
        hp.reset()

    @hp.activate
    def test_withdraw(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*account/crypto/withdraw$'),**mock_response)
        client = Client(api_key,api_secret)
        required_params = {'currency':'foo','amount':'1.0','address':'someAddress123'}
        send_params = {}
        while required_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.withdraw(**send_params)
            for key in required_params:
                send_params[key] = required_params.pop(key)
                break
        self.assertEqual(client.withdraw(**send_params),mock_items)
        hp.reset()

    @hp.activate
    def test_commit_withdrawal(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.PUT,re.compile('.*account/crypto/withdraw/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.commit_withdrawal('foo'),mock_items)
        hp.reset()

    @hp.activate
    def test_rollback_withdrawal(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.DELETE,re.compile('.*account/crypto/withdraw/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.rollback_withdrawal('foo'),mock_items)
        hp.reset()

    @hp.activate
    def test_get_deposit_address(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.GET,re.compile('.*account/crypto/address/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.get_deposit_address('foo'),mock_items)
        hp.reset()

    @hp.activate
    def test_add_deposit_address(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*account/crypto/address/foo$'),**mock_response)
        client = Client(api_key,api_secret)
        self.assertEqual(client.add_deposit_address('foo'),mock_items)
        hp.reset()

    @hp.activate
    def test_transfer_to_trading(self):
        mock_response = {'body':json.dumps(mock_items)}
        hp.register_uri(hp.POST,re.compile('.*account/transfer$'),**mock_response)
        client = Client(api_key,api_secret)
        required_params = {'currency':'foo','amount':'1.0','type':'limit'}
        send_params = {}
        while required_params:
            with self.assertRaises(errors.ParameterRequiredError):
                client.transfer_to_trading(**send_params)
            for key in required_params:
                send_params[key] = required_params.pop(key)
                break
        self.assertEqual(client.transfer_to_trading(**send_params),mock_items)
        hp.reset()
