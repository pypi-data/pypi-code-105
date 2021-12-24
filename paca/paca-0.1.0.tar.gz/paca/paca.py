#!/usr/bin/env python 

import argparse
import textwrap
from sys import argv

import alpaca_trade_api as alpaca
from colorama import init, Fore, Style

def run():
    init()

    parser = argparse.ArgumentParser(
        prog='paca',
        description='Check asset status using Alpaca Broker API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
            Examples

            > paca AAPL
            Class: us_equity
            Easy-to-Borrow: True
            Exchange: NASDAQ
            Fractionable: True
            ID: b0b6dd9d-8b9b-48a9-ba46-b9d54906e415
            Marginable: True
            Name: Apple Inc. Common Stock
            Shortable: True
            Status: active
            Symbol: AAPL
            Tradable: True

            > paca -est DNUT
            Easy-to-Borrow: False
            Shortable: False
            Tradable: True
            ''')
    )
    parser.add_argument('ASSET', type=str.upper, help='Ticker of asset to check')
    #parser.add_argument('ASSET', type=str.upper, help='Ticker of asset(s) to check')
    parser.add_argument('-a', '--asset-class', help='Class of asset: us_equity or crypto', action='store_true')
    parser.add_argument('-e', '--easy-to-borrow', help='Easy-to-Borrow or Hard-to-Borrow status', action='store_true')
    parser.add_argument('-ex', '--exchange', help='Exchange asset is available on', action='store_true')
    parser.add_argument('-f', '--fractionable', help='Fractionable status', action='store_true')
    parser.add_argument('-i', '--id', help='ID of asset', action='store_true')
    parser.add_argument('-m', '--marginable', help='Marginable status', action='store_true')
    parser.add_argument('-n', '--name', help='Full name of asset', action='store_true')
    parser.add_argument('-s', '--shortable', help='Shortable status', action='store_true')
    parser.add_argument('-st', '--status', help='Status of asset: active or inactive', action='store_true')
    parser.add_argument('-sy', '--symbol', help='Symbol/ticker', action='store_true')
    parser.add_argument('-t', '--tradable', help='Tradable status', action='store_true')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.0')
    args = parser.parse_args()

    api = alpaca.REST()

    #if (len(args.ASSET) > 1):
    #    assets = api.list_assets(args.ASSET)
    #else:
    #    asset = api.get_asset(args.ASSET)

    asset = api.get_asset(args.ASSET)

    #if (args.raw):
    #    print(asset)
    #elif (args.no_color):

    if len(argv) == 2:
        asset_class = getattr(asset, 'class')
        print('Class: {}'.format(asset_class))
        print('Easy-to-Borrow: ' + Fore.GREEN + '{}'.format(asset.easy_to_borrow) + Fore.RESET) if asset.easy_to_borrow else print('Easy-to-Borrow: ' + Fore.RED + '{}'.format(asset.easy_to_borrow) + Fore.RESET)
        print('Exchange: {}'.format(asset.exchange))
        print('Fractionable: ' + Fore.GREEN + '{}'.format(asset.fractionable) + Fore.RESET) if asset.fractionable else print('Fractionable: ' + Fore.RED + '{}'.format(asset.fractionable) + Fore.RESET)
        print('ID: {}'.format(asset.id))
        print('Marginable: ' + Fore.GREEN + '{}'.format(asset.marginable) + Fore.RESET) if asset.marginable else print('Marginable: ' + Fore.RED + '{}'.format(asset.marginable) + Fore.RESET)
        print('Name: {}'.format(asset.name))
        print('Shortable: ' + Fore.GREEN + '{}'.format(asset.shortable) + Fore.RESET) if asset.shortable else print('Shortable: ' + Fore.RED + '{}'.format(asset.shortable) + Fore.RESET)
        print('Status: ' + Fore.GREEN + '{}'.format(asset.status) + Fore.RESET) if asset.status else print('Status: ' + Fore.RED + '{}'.format(asset.status) + Fore.RESET)
        print('Symbol: {}'.format(asset.symbol))
        print('Tradable: ' + Fore.GREEN + '{}'.format(asset.tradable) + Fore.RESET) if asset.tradable else print('Tradable: ' + Fore.RED + '{}'.format(asset.tradable) + Fore.RESET)
    else:
        if args.asset_class:
            asset_class = getattr(asset, 'class')
            print('Class: {}'.format(asset_class))
        if args.easy_to_borrow:
            print('Easy-to-Borrow: ' + Fore.GREEN + '{}'.format(asset.easy_to_borrow) + Fore.RESET) if asset.easy_to_borrow else print('Easy-to-Borrow: ' + Fore.RED + '{}'.format(asset.easy_to_borrow) + Fore.RESET)
        if args.exchange:
            print('Exchange: {}'.format(asset.exchange))
        if args.fractionable:
            print('Fractionable: ' + Fore.GREEN + '{}'.format(asset.fractionable) + Fore.RESET) if asset.fractionable else print('Fractionable: ' + Fore.RED + '{}'.format(asset.fractionable) + Fore.RESET)
        if args.id:
            print('ID: {}'.format(asset.id))
        if args.marginable:
            print('Marginable: ' + Fore.GREEN + '{}'.format(asset.marginable) + Fore.RESET) if asset.marginable else print('Marginable: ' + Fore.RED + '{}'.format(asset.marginable) + Fore.RESET)
        if args.name:
            print('Name: {}'.format(asset.name))
        if args.shortable:
            print('Shortable: ' + Fore.GREEN + '{}'.format(asset.shortable) + Fore.RESET) if asset.shortable else print('Shortable: ' + Fore.RED + '{}'.format(asset.shortable) + Fore.RESET)
        if args.status:
            print('Status: ' + Fore.GREEN + '{}'.format(asset.status) + Fore.RESET) if asset.status else print('Status: ' + Fore.RED + '{}'.format(asset.status) + Fore.RESET)
        if args.symbol:
            print('Symbol: {}'.format(asset.symbol))
        if args.tradable:
            print('Tradable: ' + Fore.GREEN + '{}'.format(asset.tradable) + Fore.RESET) if asset.tradable else print('Tradable: ' + Fore.RED + '{}'.format(asset.tradable) + Fore.RESET)

if __name__ == '__main__':
    run()
