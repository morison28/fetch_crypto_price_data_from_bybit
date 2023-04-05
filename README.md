## fetch_crypto_data_from_bybit
- bybitから各種約定データを取得し，pickleファイルに保存するスクリプト
- ⚠ ローソク足は未リファクタリング(いつかやる)



### usage
#### fetch executions data
こんな感じで使う
```
python3 fetch_executions_from_bybit.py --symbol BTCUSDT --start_date 2023-01-01 --end_date 2023-01-02 --save_dir save_dir/
```
#### generate candle sticks
```
python generate_candles <symbol> <start_date> <end_date> <period>

ex)
python generate_candles BTCUSD 2021-01-01 2021-01-07 1H
```

period

```
D: 毎日
B: 毎営業日（月曜 - 金曜）
W: 毎週（日曜始まり）
M: 月末ごと
SM: 15日と月末ごと
Q: 四半期末ごと
AまたはY: 年末ごと

H: 毎時
Tまたはmin: 毎分
S: 毎秒
Lまたはms: 毎ミリ秒
Uまたはus: 毎マイクロ秒
N: 毎ナノ秒
```
参考:https://note.nkmk.me/python-pandas-time-series-freq/


### symbols
list of available symbols

```
AAVEUSDT/
ADAUSDT/
ALGOUSDT/
ALICEUSDT/
ATOMUSDT/
AVAXUSDT/
AXSUSDT/
BCHUSDT/
BITUSD/
BITUSDT/
BNBUSDT/
BTCUSD/
BTCUSDT/
BTCUSDU21/
BTCUSDZ21/
C98USDT/
CELRUSDT/
CHRUSDT/
CHZUSDT/
COMPUSDT/
CRVUSDT/
DASHUSDT/
DOGEUSDT/
DOTUSD/
DOTUSDT/
DYDXUSDT/
ENJUSDT/
ENSUSDT/
EOSUSD/
EOSUSDT/
ETCUSDT/
ETHUSD/
ETHUSDT/
ETHUSDU21/
ETHUSDZ21/
FILUSDT/
FTMUSDT/
FTTUSDT/
GALAUSDT/
HBARUSDT/
ICPUSDT/
IOSTUSDT/
IOTXUSDT/
KEEPUSDT/
KSMUSDT/
LINKUSDT/
LRCUSDT/
LTCUSDT/
LUNAUSDT/
MANAUSDT/
MATICUSDT/
NEARUSDT/
OMGUSDT/
ONEUSDT/
SANDUSDT/
SHIB1000USDT/
SLPUSDT/
SOLUSDT/
SRMUSDT/
SUSHIUSDT/
THETAUSDT/
TRXUSDT/
UNIUSDT/
VETUSDT/
WOOUSDT/
XEMUSDT/
XLMUSDT/
XRPUSD/
XRPUSDT/
XTZUSDT/
```