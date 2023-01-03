from flask import Blueprint, render_template, request
from binance.spot import Spot
# import requests # Import API
views = Blueprint(__name__, "views")


@views.route("/")
def index():
    return render_template("index.html")


@views.route("/crypto/prices")
def get_prices():
    # Query Parameters
    args = request.args
    baseAsset = args.get("base")
    if baseAsset == None:
        baseAsset = "BTC"
    quoteAsset = args.get("quote")
    if quoteAsset == None:
        quoteAsset = "USDT"

    # Symbol
    symbol = baseAsset + quoteAsset

    # Binance Library
    client = Spot()

    # Current Price
    price = float((client.ticker_price(symbol))["price"])

    # Price 24 hours (%)
    price24h = float((client.ticker_24hr(symbol))["priceChangePercent"])

    # Price 2 weeks - Select only 2nd week
    price2w = (client.klines(symbol, "1w", limit=2))[1]

    return render_template("prices.html", baseAsset=baseAsset, quoteAsset=quoteAsset, symbol=symbol, price=price, price24h=price24h, price2w=price2w)
