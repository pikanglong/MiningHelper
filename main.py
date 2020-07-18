import sys
import time
import ccxt

log_file = open('./log.txt', 'a+')

exchange = ccxt.huobipro()
exchange.apiKey = 'APIKEY'
exchange.secret = 'SECRET'

symbol = 'ZEC/USDT'
base_coin = symbol.split('/')[-1]
trade_coin = symbol.split('/')[0]

print('The script started successfully.')

while True:
    balance = exchange.fetch_balance()['total']
    base_coin_amount = float(balance[base_coin])
    trade_coin_amount = float(balance[trade_coin])
    print('{} | {:.8f}{} | {:.8f}{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), base_coin_amount, base_coin, trade_coin_amount, trade_coin), file=log_file, flush=True)

    ticker = exchange.fetch_ticker(symbol)

    if trade_coin_amount > 0.001 and trade_coin_amount * ticker['bid'] > 5:
        for i in range(5):
            try:
                order_info = exchange.create_market_sell_order(symbol, trade_coin_amount)
                print('success:', order_info, file=log_file, flush=True)
                break
            except Exception as e:
                print('failed:', e, file=log_file, flush=True)
                time.sleep(1)

    time.sleep(10)
