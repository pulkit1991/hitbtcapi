# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import requests
import warnings

from .utils import check_uri_security
from .compat import quote
from .compat import imap
from .errors import api_response_error,ParameterRequiredError


class Client(object):
    """ API Client for the HitBTC REST API.
    Entry point for making requests to the HitBTC REST API.

    Provides helper methods for common API endpoints, as well as niceties around response handling.

    Any errors will be raised as exceptions. These exceptions will always be subclasses of `hitbtc.error.APIError`. HTTP-related errors will also be subclasses of `requests.HTTPError`.

    Full API docs, including descriptions of each API and its parameters, are available here: https://api.hitbtc.com/
    """

    BASE_API_URI = 'https://api.hitbtc.com/api/2/' #v2

    def __init__(self,key,secret,base_api_uri=None):
        if not key:
            raise ValueError("Missing API 'key'")
        if not secret:
            raise ValueError("Missing API 'secret'")
        self._key = key
        self._secret = secret
        # Allow passing in a different API base and warn if it is insecure.
        self.BASE_API_URI = check_uri_security(base_api_uri or self.BASE_API_URI)
        # Set up a requests session for interacting with the API.
        self._build_session()

    def _build_session(self):
        """
        Internal helper for creating a requests `session` with the correct authentication handling.
        """
        self._session = requests.session()
        self._session.auth = (self._key, self._secret)

    def _create_api_uri(self,*dirs):
        """
        Internal helper for creating fully qualified endpoint URIs.
        """
        return self.BASE_API_URI +'/'.join(imap(quote,dirs))

    def _request(self,method,*dirs,**kwargs):
        """
        Internal helper for creating HTTP requests to the HitBTC API. Returns the HTTP response.
        """
        uri = self._create_api_uri(*dirs)
        return getattr(self._session,method)(uri,**kwargs)

    def _handle_response(self,response):
        """
        Internal helper for handling API responses from the HitBTC server. Raises the appropriate exceptions when response is not 200; otherwise, returns the response.
        """
        if response.status_code != 200:
            raise api_response_error(response)
        return response.json()


    def _get(self,*dirs,**kwargs):
        return self._request('get',*dirs,**kwargs)

    def _post(self,*dirs,**kwargs):
        return self._request('post',*dirs,**kwargs)

    def _put(self,*dirs,**kwargs):
        return self._request('put',*dirs,**kwargs)

    def _delete(self,*dirs,**kwargs):
        return self._request('delete',*dirs,**kwargs)

    def _patch(self,*dirs,**kwargs):
        return self._request('patch',*dirs,**kwargs)

    def _check_req_params(self,req_params,params):
        """
        Internal helper to check if all required parameters for the method have been provided. Raises ParameterRequiredError if any of the required parameters is missing.
        """
        if not all(req_p in params for req_p in req_params):
            raise ParameterRequiredError('Missing required parameter(s) %s' % req_params)

    # --------------------
    #   PUBLIC API
    # --------------------
    def get_currencies(self,**params):
        response = self._get('public','currency',params=params)
        return self._handle_response(response)

    def get_currency(self,currency,**params):
        response = self._get('public','currency',currency,params=params)
        return self._handle_response(response)

    def get_symbols(self,**params):
        response = self._get('public','symbol',params=params)
        return self._handle_response(response)

    def get_symbol(self,symbol,**params):
        response = self._get('public','symbol',symbol,params=params)
        return self._handle_response(response)

    def get_tickers(self,**params):
        response = self._get('public','ticker',params=params)
        return self._handle_response(response)

    def get_ticker(self,symbol,**params):
        response = self._get('public','ticker',symbol,params=params)
        return self._handle_response(response)

    def get_trades(self,symbol,**params):
        response = self._get('public','trades',symbol,params=params)
        return self._handle_response(response)

    def get_orderbook(self,symbol,**params):
        response = self._get('public','orderbook',symbol,params=params)
        return self._handle_response(response)

    def get_candles(self,symbol,**params):
        response = self._get('public','candles',symbol,params=params)
        return self._handle_response(response)


    # --------------------
    #   TRADING API
    # --------------------
    def get_trading_balance(self,**params):
        response = self._get('trading','balance',params=params)
        return self._handle_response(response)

    def get_active_orders(self,**params):
        response = self._get('order',params=params)
        return self._handle_response(response)

    def get_active_order(self,clientOrderId,**params):
        response = self._get('order',clientOrderId,params=params)
        return self._handle_response(response)

    def create_order(self,**params):
        # required parameters for creating a new order
        required = ['symbol','side','quantity','price']
        self._check_req_params(required,params)
        response = self._post('order',data=params)
        return self._handle_response(response)

    def update_order(self,clientOrderId,**params):
        # required parameters for updating an order
        required = ['symbol','side','quantity','price','timeInForce']
        self._check_req_params(required,params)
        response = self._put('order',clientOrderId,data=params)
        return self._handle_response(response)

    def cancel_open_orders(self,**params):
        response = self._delete('order',data=params)
        return self._handle_response(response)

    def cancel_order(self,clientOrderId,**params):
        response = self._delete('order',clientOrderId,data=params)
        return self._handle_response(response)

    def cancel_replace_order(self,clientOrderId,**params):
        # required parameters for cancel replace order
        required = ['quantity','requestClientId']
        self._check_req_params(required,params)
        response = self._patch('order',clientOrderId,data=params)
        return self._handle_response(response)

    def get_trading_fee(self,symbol,**params):
        response = self._get('trading','fee',symbol,params=params)
        return self._handle_response(response)


    # ----------------------
    #   TRADE HISTORY API
    # -----------------------
    def get_order_history(self,**params):
        response = self._get('history','order',params=params)
        return self._handle_response(response)

    def get_trade_history(self,**params):
        response = self._get('history','trades',params=params)
        return self._handle_response(response)

    def get_trades_by_orderid(self,orderId,**params):
        response = self._get('history','order',orderId,'trades',params=params)
        return self._handle_response(response)


    # --------------------
    #   ACCOUNT API
    # --------------------
    def get_account_balance(self,**params):
        response = self._get('account','balance',params=params)
        return self._handle_response(response)

    def get_deposit_address(self,currency,**params):
        response = self._get('account','crypto','address',currency,params=params)
        return self._handle_response(response)

    def add_deposit_address(self,currency,**params):
        response = self._post('account','crypto','address',currency,data=params)
        return self._handle_response(response)

    def withdraw(self,**params):
        # required parameters for withdrawing cryptocurrency
        required = ['currency','amount','address']
        self._check_req_params(required,params)
        response = self._post('account','crypto','withdraw',data=params)
        return self._handle_response(response)

    def commit_withdrawal(self,withdrawalId,**params):
        response = self._put('account','crypto','withdraw',withdrawalId,data=params)
        return self._handle_response(response)

    def rollback_withdrawal(self,withdrawalId,**params):
        response = self._delete('account','crypto','withdraw',withdrawalId,data=params)
        return self._handle_response(response)

    def transfer_to_trading(self,**params):
        # required parameters to transfer between account and trading
        required = ['currency','amount','type']
        self._check_req_params(required,params)
        response = self._post('account','transfer',data=params)
        return self._handle_response(response)

    def get_account_transactions(self,**params):
        response = self._get('account','transactions',params=params)
        return self._handle_response(response)

    def get_account_transaction(self,transactionId,**params):
        response = self._get('account','transactions',transactionId,params=params)
        return self._handle_response(response)
