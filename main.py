import os
import stocker
import yfinance as yf
import pandas as pd
from datetime import date
from IPython.display import display


def trade():
    new = False
    print("This code runs on yahoo's yfinance api which does not have a complete record of all stocks. It is possible that a stock you enter will not be available to trade.\n")
    
    print("Rules: 1) Everytime you run this code you must conduct at least one trade. This is so that any cash infusions in a session are saved to the csv file. 2) If you must open the csv files do so with a non invasive editor like vim (don't use Numbers) 3)Code is case sensitive\n")
    dir = os.chdir(os.path.join(".", "csvs"))
    files = os.listdir(dir)
    files = [os.path.splitext(file)[0] for file in files]
    files = [el for el in files if (".DS_Store" not in el)]
    print("Portfolios: ",files)
    while True:
        c = input("Would you like to create new portfolio or use an existing one? To create a portfolio write create and then [portfolio_name]. To use an existing one just press enter\n")
        if ("create" in c):
            name = c.split()[1]
            files.append(name)
            new = True
            break
        elif not c: #means emty string
            break
        else:
            print("Sorry, that was not a valid entry \n ")
            continue
    
    while True:
        p = input("\nWhich portfolio would you like to open and begin trading in?\n")
        if(p not in files):
            print("Please enter a valid portfolio name ")
            continue
        else:
            break
    port = stocker.Portfolio(p)
    #creating new portfolio
    if(new):
        #redundancy
        port.df = pd.DataFrame(columns= ["DATE", "TICKER", "PRICE", "SHARES", "BALANCE", "CASH", "BUY/SELL"])
        #seed portfolio
        while True:
            try:
                inp_cash = int(input("\nPlease enter how much cash you want to deposit into your new portfolio (ex. 500 without $)\n"))
            except ValueError:
                print("Sorry, you did not enter a number ")
                continue
            port.cash = inp_cash
            break
        
    else:
        port.df = pd.read_csv(os.path.join(p+".csv"), index_col=[0])
        print("successfully loaded data from csv into portfolio")
        port.cash = port.df["CASH"].iloc[-1]
        print("Portfolio has $" + str(float(port.cash)) + " available in cash \n")
        while True:
            add = 0
            try:
                add += int(input("\nWould you like to deposit more cash? If so, type how much you would like to infuse (ex. 500 without $) and if not just enter 0.\n"))
            except ValueError:
                print("Sorry, you did not enter a number")
                continue
            if(add == 0):
                break
            else:
                port.cash+= add
                break
        
    print("\nUSER INSTRUCTIONS:\n1) To buy enter \"buy ticker_name\" (e.x. buy SNAP). Do the same for sells: \"sell ticker_name\" \n2) To view P/L history enter pl \n3) To exit enter exit ")
    cmds = ["buy", "sell", "pl", "exit"]
    while True:
        cmd = input("\nWhat would you like to do?\n")
        parts = cmd.split()
#        print(parts)
        if(parts[0] not in cmds):
            print("That is not a valid command. Please try again")
            continue
        if(parts[0] == "buy"):
            ticker_name = parts[1]
            port.buy(ticker_name)
        
        elif(parts[0] == "sell"):
            ticker_name = parts[1]
            port.sell(ticker_name)
        
        elif(parts[0] == "pl"):
            display(port.df)
        
        elif(parts[0] == "exit"):
            #write to csv file
            port.df.to_csv(p+".csv", index=True)
            return
        
            

if __name__=="__main__":
    trade()
