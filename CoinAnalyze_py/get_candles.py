
#비동기적으로 티커를 업데이트 하는 함수
#이정도로 복잡해지는 거면 차라리 스레드가 좋지 않을까?
import asyncio
import pyupbit
import pandas as pd
        
class GetCoinCandle:

    def get(self,name,interval,count):
        
        rawDf=pyupbit.get_ohlcv(ticker=name,count=count,interval=interval)
        print(rawDf)
        rawDf["close_yesterday"] = rawDf["close"].shift(1)
        rawDf.loc[0,"close_yesterday"]=rawDf.loc[0,"open"]
        rawDf["rage_high"] = (rawDf["high"]-rawDf["close_yesterday"])/rawDf["close_yesterday"]
        rawDf["rage_low"] = (rawDf["low"]-rawDf["close_yesterday"])/rawDf["close_yesterday"]
        rawDf["rage_close"] = (rawDf["close"]-rawDf["close_yesterday"])/rawDf["close_yesterday"]
        rawDf.drop(["volume","value"],axis=1,inplace=True)

        rawDf.to_pickle(path="Coindata\\{0}.pkl".format(name))
        return rawDf


    #200개 이하의 캔들 조회시 사용
    async def start(self,interval,count):
        ticker_list=pd.DataFrame(pyupbit.get_tickers(fiat="KRW", is_details=True))
        ticker_list=ticker_list["market"]
        num=1
        for a in ticker_list:
            print(a)
            self.get(a,interval,count)
            num+=1
            if num%8==0:
                await asyncio.sleep(10)


        self.ranking=self.ranking.sort_values(ascending=False)
        

    def show_me(self):
        for i, j in self.coinCandleList.items():
            print("\n\n",i,"\n",j)

        print(self.ranking)


if __name__=="__main__":
    crg = GetCoinCandle()
    asyncio.run(crg.start(interval="day",count=1000))
    crg.show_me()
    # crg.start_not_async(interval="minute240",count=1300,path=".\\coindata_min240")
    # crg.show_me()
    # crg.start_not_async(interval="minute60",count=1300,path=".\\coindata_min60")
    #crg.show_me()
    # crg.start_not_async(interval="minute3",count=1300,path=".\\coindata_min3")
    # crg.show_me()