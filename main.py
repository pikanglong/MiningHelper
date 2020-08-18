import ccxt
import json
import time
import logging
import requests
import configparser

logging.basicConfig(filename='main.log', format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

cp = configparser.ConfigParser()
cp.read('main.conf')

huobi_apikey = cp.get('huobi', 'apiKey')
huobi_secret = cp.get('huobi', 'secret')

okex_apikey = cp.get('okex', 'apiKey')
okex_secret = cp.get('okex', 'secret')
okex_password = cp.get('okex', 'password')

sckey = cp.get('serverchan', 'sckey')

api = 'https://sc.ftqq.com/' + sckey + '.send'

huobi = ccxt.huobipro({
    'apiKey': huobi_apikey,
    'secret': huobi_secret,
    'proxies': {
        'http': 'http://localhost:33066',
        'https': 'http://localhost:33066',
    },
})

okex = ccxt.okex({
    'apiKey': okex_apikey,
    'secret': okex_secret,
    'password': okex_password,
    'proxies': {
        'http': 'http://localhost:33066',
        'https': 'http://localhost:33066',
    },
})

def send_message(api, title, content):
    data = {
        'text': title,
        'desp': content
    }
    requests.post(api, data = data)

def sell(exchange, symbol, trade_coin_amount):
    for i in range(5):
        try:
            order_info = exchange.create_market_sell_order(symbol, trade_coin_amount)
            logging.info('success: %s', order_info)
            print('success:', order_info)
            send_message(api, '出售成功', json.dumps(order_info))
            break
        except Exception as e:
            logging.error('failed: %s', e)
            print('failed:', e)
            time.sleep(1)

def solve(exchange, trade_coin, base_coin):
    symbol = trade_coin + '/' + base_coin
    try:
        balance = exchange.fetch_balance()['total']
        base_coin_amount = float(balance[base_coin])
        if trade_coin in balance:
            trade_coin_amount = float(balance[trade_coin])
        else:
            trade_coin_amount = float(0.0)
        logging.info('current account value: %.8f%s %.8f%s', base_coin_amount, base_coin, trade_coin_amount, trade_coin)
        
        ticker = exchange.fetch_ticker(symbol)

        if exchange == huobi and trade_coin_amount > 0.001 and trade_coin_amount * ticker['bid'] > 5:
            sell(exchange, symbol, trade_coin_amount)

        if exchange == okex and trade_coin_amount > 0.01:
            sell(exchange, symbol, trade_coin_amount)

    except Exception as e:
        logging.error('%s', e)
        print(e)

print('Script started...')
while True:
    solve(huobi, 'ZEC', 'USDT')
    solve(okex, 'BCH', 'USDT')
    time.sleep(10)
