import yfinance as yf
import pandas as pd
from datetime import date
from IPython.display import display


'''Mock Stock portfolio, complete with a P/L statement in Python
Pretend to buy and sell stock with real stock data; while recording your transaction histories and presenting that information to a user in the form of a P&L statement.
• Able to get real time stock data - Allows you to mock buy/sell stock using tickers and share amount
• Saves your P & L data between running your program (For beginners, I suggest using pandas.DataFrame.to_csv or sqlite3)
• Creates a decent P & L with the columns DATE, TICKER, PRICE, SHARES, BALANCE
• Program runs smoothly (doesn't crash, output is aesthetically pleasant to look at)
• Comments within code, code is well structured and easy to look at
• Methods used in Script are contained within a Class'''



class Portfolio:
    def __init__(self, name):
    
        
            
        #name portfolio
        self.name = name
        #available cash/buying power
        self.cash = 0
        #value of investments
        self.investing = 0
        #balance = (cash+investments) with investments initially 0
        self.balance = 0
#        #make data frame with correct cols
        self.df = pd.DataFrame(columns= ["DATE", "TICKER", "PRICE", "SHARES", "BALANCE", "CASH", "BUY/SELL"])

    
    def stock_info(self,stock):
        #get info about a stock
        company = yf.Ticker(stock)
        long_name = company.info['longName']
        print(company.history(period="1wk"))
        market_price = company.info['regularMarketPrice']
        print('Company: ', long_name)
        print('Current Market Price: $', market_price)
        shares = int(self.cash/market_price)
#        print('Your Balance (Cash and Investments): $', self.balance)
        print('Your Cash Available: $', self.cash)
        print('Amount of shares you can purchase: ', shares)
        print('Shares Outstanding: ', self.get_num_shares(stock))
        return (company, market_price)
    
    def get_num_shares(self, ticker):
        #get all the purchases and sells of a stock
        if(not self.df.empty):
            df_ticker = self.df.loc[self.df["TICKER"] == ticker]
            if(not df_ticker.empty):
                df_buys = df_ticker.loc[df_ticker["BUY/SELL"] == "BUY"]
                df_sells = df_ticker.loc[df_ticker["BUY/SELL"] == "SELL"]
                
                shares_bought = df_buys["SHARES"].sum(skipna = True)
                shares_sold = df_sells["SHARES"].sum(skipna = True)
                
                
                return (shares_bought-shares_sold)
        else:
            return 0
    
    def buy(self, ticker):
        #buy a stock
        company, price = self.stock_info(ticker)
        while True:
            try:
                input_shares = int(input("\nHow many shares would you like to buy? "))
            except ValueError:
               print("Please enter a valid number (no commas or non-numeric input)")
               continue
            shares = input_shares
            break
        deduct = shares*price
        if(self.cash < deduct):
            print("You do not have enough money to conduct that trade")
            return
        else:
            #deduct cost from portfolio cash
            self.cash-= deduct
            #output from function
            self.investing = self.investments() + deduct
            print("Investing: ", self.investing)
            #balance
            self.balance = self.cash+self.investing
            # dd/mm/YY
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            #write row to the dataframe
            self.df.loc[len(self.df.index)] = [d1, ticker, price, shares, self.balance, self.cash, "BUY"]
            display(self.df)
            print(f"BOUGHT ${deduct} of {ticker}")
    
    
    
    def sell(self, ticker):
        #sell a stock
        company, price = self.stock_info(ticker)
        
        while True:
            try:
                input_shares = int(input("\nHow many shares would you like to sell? "))
            except ValueError:
               print("Please enter a valid number (no commas or non-numeric input)")
               continue
            shares = input_shares
            break
        
        augend = shares*price
        shares_available = self.get_num_shares(ticker)
        if(shares_available < shares):
            print("You do not have that many shares")
            return
        else:
            #add to portfolio balance
            self.cash+= augend
            #output from function
            
            self.investing = self.investments() - augend
            print("Investing: ", self.investing)
            #balance
            self.balance = self.cash+self.investing
            # dd/mm/YY
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            self.df.loc[len(self.df.index)] = [d1, ticker, price, shares, self.balance, self.cash, "SELL"]
            display(self.df)
            print(f"SOLD ${augend} of {ticker}")
    
    
    def investments(self):
        #amount investing
        if(not self.df.empty):
            investingpool_value = 0
            for index, row in self.df.iterrows():
                tic = row["TICKER"]
                if(self.get_num_shares(tic) < 1):
                    #if we don't hold any of that stock anymore no need to include it
                    pass
                else:
                    #we do have shares of that stock
                    #need to calculate the current value of the stock so find new proice
                    company = yf.Ticker(tic)
                    new_price = company.info['regularMarketPrice']
                    if(row["BUY/SELL"] == "BUY"):
                        #multiply new price by amount we bought at earlier date
                        investingpool_value+= new_price*row["SHARES"]
                    if(row["BUY/SELL"] == "SELL"):
                        investingpool_value-= new_price*row["SHARES"]
            return investingpool_value
        else:
            return 0
            
        
        
    
