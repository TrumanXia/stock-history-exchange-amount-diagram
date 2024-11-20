from mootdx.quotes import Quotes
from mootdx import consts
from mootdx.reader import Reader
client = Quotes.factory(market='std')
print(client.quotes(symbol=["880008"]))
# print(client.quotes(symbol=["399001"]))


# client = Quotes.factory(market='std')
# print(client.stock_count(market=consts.MARKET_SH))

# client = Quotes.factory(market='ext')
# print(client.markets())

# reader = Reader.factory(market='std', tdxdir='D:/投资/犀利PRO/TDX_XiliPro_7.633.806')
# # 读取日线数据
# print(reader.daily(symbol='600036'))