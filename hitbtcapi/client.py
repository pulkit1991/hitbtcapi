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


def handle_response(response):
    if response.status_code != 200:
        raise api_response_error(response)
    return response.json()


class Client(object):
    BASE_API_URI = 'https://api.hitbtc.com/api/2/'

    def __init__(self,key,secret,base_api_uri=None):
        if not key:
            raise ValueError("Missing API 'key'")
        if not secret:
            raise ValueError("Missing API 'secret'")
        self._key = key
        self._secret = secret
        self.BASE_API_URI = check_uri_security(base_api_uri or self.BASE_API_URI)
        self._build_session()

    def _build_session(self):
        self._session = requests.session()
        self._session.auth = (self._key, self._secret)

    def _create_api_uri(self,*dirs):
        return self.BASE_API_URI +'/'.join(imap(quote,dirs))

    # helper function
    def _request(self,method,*dirs,**kwargs):
        uri = self._create_api_uri(*dirs)
        return getattr(self._session,method)(uri,**kwargs)

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
        if not all(req_p in params for req_p in req_params):
            raise ParameterRequiredError('Missing required parameter(s) %s' % req_params)

    # --------------------
    #   PUBLIC API
    # --------------------
    def get_currencies(self,**params):
        response = self._get('public','currency',params=params)
        return handle_response(response)

    def get_currency(self,currency,**params):
        response = self._get('public','currency',currency,params=params)
        return handle_response(response)

    def get_symbols(self,**params):
        response = self._get('public','symbol',params=params)
        return handle_response(response)

    def get_symbol(self,symbol,**params):
        response = self._get('public','symbol',symbol,params=params)
        return handle_response(response)

    def get_tickers(self,**params):
        response = self._get('public','ticker',params=params)
        return handle_response(response)

    def get_ticker(self,symbol,**params):
        response = self._get('public','ticker',symbol,params=params)
        return handle_response(response)

    def get_trades(self,symbol,**params):
        response = self._get('public','trades',symbol,params=params)
        return handle_response(response)

    def get_orderbook(self,symbol,**params):
        response = self._get('public','orderbook',symbol,params=params)
        return handle_response(response)

    def get_candles(self,symbol,**params):
        response = self._get('public','candles',symbol,params=params)
        return handle_response(response)


    # --------------------
    #   TRADING API
    # --------------------
    def get_trading_balance(self,**params):
        response = self._get('trading','balance',params=params)
        return handle_response(response)

    def get_active_orders(self,**params):
        response = self._get('order',params=params)
        return handle_response(response)

    def get_active_order(self,clientOrderId,**params):
        response = self._get('order',clientOrderId,params=params)
        return handle_response(response)

    def create_order(self,**params):
        required = ['symbol','side','quantity','price']
        self._check_req_params(required,params)
        response = self._post('order',data=params)
        return handle_response(response)

    def update_order(self,clientOrderId,**params):
        required = ['symbol','side','quantity','price','timeInForce']
        self._check_req_params(required,params)
        response = self._put('order',clientOrderId,data=params)
        return handle_response(response)

    def cancel_open_orders(self,**params):
        response = self._delete('order',data=params)
        return handle_response(response)

    def cancel_order(self,clientOrderId,**params):
        response = self._delete('order',clientOrderId,data=params)
        return handle_response(response)

    def cancel_replace_order(self,clientOrderId,**params):
        required = ['quantity','requestClientId']
        self._check_req_params(required,params)
        response = self._patch('order',clientOrderId,data=params)
        return handle_response(response)

    def get_trading_fee(self,symbol,**params):
        response = self._get('trading','fee',symbol,params=params)
        return handle_response(response)


    # ----------------------
    #   TRADE HISTORY API
    # -----------------------
    def get_order_history(self,**params):
        response = self._get('history','order',params=params)
        return handle_response(response)

    def get_trade_history(self,**params):
        response = self._get('history','trades',params=params)
        return handle_response(response)

    def get_trades_by_orderid(self,orderId,**params):
        response = self._get('history','order',orderId,'trades',params=params)
        return handle_response(response)


    # --------------------
    #   ACCOUNT API
    # --------------------
    def get_account_balance(self,**params):
        response = self._get('account','balance',params=params)
        return handle_response(response)

    def get_deposit_address(self,currency,**params):
        response = self._get('account','crypto','address',currency,params=params)
        return handle_response(response)

    def add_deposit_address(self,currency,**params):
        response = self._post('account','crypto','address',currency,data=params)
        return handle_response(response)

    def withdraw(self,**params):
        required = ['currency','amount','address']
        self._check_req_params(required,params)
        response = self._post('account','crypto','withdraw',data=params)
        return handle_response(response)

    def commit_withdrawal(self,withdrawalId,**params):
        response = self._put('account','crypto','withdraw',withdrawalId,data=params)
        return handle_response(response)

    def rollback_withdrawal(self,withdrawalId,**params):
        response = self._delete('account','crypto','withdraw',withdrawalId,data=params)
        return handle_response(response)

    def transfer_to_trading(self,**params):
        required = ['currency','amount','type']
        self._check_req_params(required,params)
        response = self._post('account','transfer',data=params)
        return handle_response(response)

    def get_account_transactions(self,**params):
        response = self._get('account','transactions',params=params)
        return handle_response(response)

    def get_account_transaction(self,transactionId,**params):
        response = self._get('account','transactions',transactionId,params=params)
        return handle_response(response)
