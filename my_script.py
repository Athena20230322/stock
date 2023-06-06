import sys
from finlab.backtest import sim
from finlab import data

df = data.get('security_categories')
# 排除金融股
category_range = [ind for ind in list(set(df['category'])) if '金融' not in ind]

with data.universe(market='TSE_OTC',category=category_range):
    close = data.get("price:收盤價")
    high = data.get("price:最高價")
    low = data.get("price:最低價")
    vol = data.get("price:成交股數")

    # 收盤價近5日至少有1日創收盤價近120日創新
    condition1 = (close == close.rolling(120).max()).sustain(5,1)
    # 近60日股價高低區間在30%內
    condition2 = (1 - low.rolling(60).min()/high.rolling(60).max()) < 0.3
    # 收盤價低於整體市場分級的40%
    condition3 = close <= close.quantile_row(0.4)
    # 收盤價低於25元
    condition4 = close <= 25
    # 5日均大於100張
    condition5 = vol.average(5) > 100*1000

    # 交集所有條件
    position = condition1 & condition2 & condition3 & condition4 & condition5

    # 最後再挑選前5低價的標地
    position = close * (position.astype(int))
    position = position[position > 0].is_smallest(5)

    # 每月底產生訊號、隔月第一個交易日進場、開盤價進出、每檔標的持有部位上限為20%、設定交易手續費折扣
    report = sim(position, resample="M", name="低價股策略", upload=True, stop_loss=0.05, trade_at_price='open',position_limit=1/5, fee_ratio=1.425/1000*0.3, mae_mfe_window=40)
