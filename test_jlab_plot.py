import plotly as plotly
import pandas as pd
import requests
from Jlab.plot import (
    plot_tw_stock_treemap,
)

if __name__ == "__main__":
    url = "http://202.182.118.167:7777/taiwan_stock_price"
    params = {"date": ""}
    response = requests.get(url, params=params)

    if response.json()["data"] is not None:
        df = pd.DataFrame.from_dict(response.json()["data"], orient="index")
        df = df.sort_index()
        fig = plot_tw_stock_treemap(df)
        plotly.offline.plot(fig, filename="/var/www/html/twstock_treemap.html")
