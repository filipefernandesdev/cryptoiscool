from flask import Blueprint, render_template, request
from binance.spot import Spot
from datetime import datetime, timedelta
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

    # Price History - 2-week - daily
    priceHistory = (client.klines(symbol, "1d", limit=14))
    priceHistory_open = []
    priceHistory_high = []
    priceHistory_low = []
    priceHistory_close = []

    for day in priceHistory:
        priceHistory_open.append(float(day[1]))
        priceHistory_high.append(float(day[2]))
        priceHistory_low.append(float(day[3]))
        priceHistory_close.append(float(day[4]))

    # Date
    dateList = []
    for i in range(1, 15):
        currentDate = datetime.today() - timedelta(days=i)
        formattedDate = currentDate.strftime('%d-%m-%Y')
        dateList.append(formattedDate)

    return render_template("prices.html", baseAsset=baseAsset, quoteAsset=quoteAsset, symbol=symbol, price=price, price24h=price24h, priceHistory_open=priceHistory_open, priceHistory_high=priceHistory_high, priceHistory_low=priceHistory_low, priceHistory_close=priceHistory_close, dateList=dateList)
