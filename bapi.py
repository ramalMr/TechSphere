import binance.client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import json

def load_config(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def print_error(error):
    if isinstance(error, BinanceAPIException):
        print(f"Binance API xətası: {error}")
    elif isinstance(error, BinanceOrderException):
        print(f"Əmr xətası: {error}")
    else:
        print(f"Xəta: {error}")

def print_orders(orders):
    if orders:
        print("Bütün əmrlər:")
        for order in orders:
            print(order)
    else:
        print("Heç bir əmri tapılmadı.")

def print_funding_wallet(wallet):
    if wallet:
        print("Fon cüzdanı vəziyyəti:")
        for asset, value in wallet.items():
            print(f"{asset}: {value}")
    else:
        print("Fon cüzdanı məlumatı yoxdur.")

def main():
    config = load_config('config.json')
    api_key = config['api_key']
    api_secret = config['api_secret']

    client = binance.client.Client(api_key, api_secret)

    try:
        sell_order = client.create_order(
            symbol='FDUSDUSDT',
            side=binance.enums.SIDE_SELL,
            type=binance.enums.ORDER_TYPE_LIMIT,
            timeInForce=binance.enums.TIME_IN_FORCE_GTC,
            quantity=10,
            price=1.0
        )
        print(f"Limit satış əmri yaradıldı: {sell_order}")
    except Exception as e:
        print_error(e)


    try:
        # Əmri ləğv etməyə çalışın
        cancel_order = client.cancel_order(
            symbol='FDUSDUSDT',
            orderId=sell_order['orderId']
        )
        print(f"Əmr ləğv edildi: {cancel_order}")
    except Exception as e:
        print_error(e)

    try:
        # Tək bir əmri alın
        order = client.get_order(
            symbol='FDUSDUSDT',
            orderId=sell_order['orderId']
        )
        print(f"Əmr detalları: {order}")
    except Exception as e:
        print_error(e)

    try:
        # Bütün əmrləri alın
        all_orders = client.get_all_orders(symbol='FDUSDUSDT')
        print_orders(all_orders)
    except Exception as e:
        print_error(e)

    try:
        # Aktiv balansını alın
        balance = client.get_asset_balance(asset='FDUSD')
        print(f"FDUSD balansı: {balance}")
    except Exception as e:
        print_error(e)

    try:
        # Fon cüzdanı vəziyyətini alın
        funding_wallet = client.funding_wallet()
        print_funding_wallet(funding_wallet)
    except Exception as e:
        print_error(e)

    try:
        # Simvol ticker məlumatlarını alın
        ticker = client.get_symbol_ticker(symbol='FDUSDUSDT')
        print("FDUSDUSDT ticker məlumatları:")
        for key, value in ticker.items():
            print(f"{key}: {value}")
    except Exception as e:
        print_error(e)

    try:
        # Toplu əməliyyatları alın
        trades = client.get_aggregate_trades(symbol='FDUSDUSDT', limit=10)
        print("Son 10 əməliyyat:")
        for trade in trades:
            print(trade)
    except Exception as e:
        print_error(e)

    try:
        # Şam çubuğu məlumatlarını alın
        klines = client.get_klines(
            symbol='FDUSDUSDT',
            interval=binance.enums.KLINE_INTERVAL_1MINUTE,
            limit=10
        )
        print("Son 10 dəqiqəlik şam çubuqları:")
        for kline in klines:
            print(kline)
    except Exception as e:
        print_error(e)

    try:
        # Birja məlumatlarını və filtrləri alın
        exchange_info = client.get_exchange_info()
        print("Birja məlumatları və filtrlər:")
        for info in exchange_info:
            print(info)
    except Exception as e:
        print_error(e)

    # Yeni xüsusiyyətlər və qəsdən səhvlər əlavə edək

    # Qəsdən minimal notional qaydasını pozmaq
    try:
        # Minimum 5 dollardan aşağı bir əmr yaratmaq
        small_order = client.create_order(
            symbol='FDUSDUSDT',
            side=binance.enums.SIDE_BUY,
            type=binance.enums.ORDER_TYPE_LIMIT,
            timeInForce=binance.enums.TIME_IN_FORCE_GTC,
            quantity=0.1,  # Çox az miqdar
            price=1.0
        )
        print(f"Kiçik əmr yaradıldı: {small_order}")
    except Exception as e:
        print_error(e)

    # Qəsdən base və quote precision qaydalarını pozmaq
    try:
        # Bəzi precision qaydalarını pozmaq
        precision_order = client.create_order(
            symbol='FDUSDUSDT',
            side=binance.enums.SIDE_BUY,
            type=binance.enums.ORDER_TYPE_LIMIT,
            timeInForce=binance.enums.TIME_IN_FORCE_GTC,
            quantity=10.123456,  # Çox dəqiq miqdar
            price=1.000123  # Çox dəqiq qiymət
        )
        print(f"Precision qaydalarını pozan əmr yaradıldı: {precision_order}")
    except Exception as e:
        print_error(e)
if __name__ == "__main__":
    main()