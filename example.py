# needed for the next function
import subprocess
import importlib
import sys


# function that imports a library if it is installed, else installs it and then imports it
def getpack(package):
    try:
        return importlib.import_module(package)
        # import package
    except ImportError:
        subprocess.call([sys.executable, "-m", "pip", "install", package],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return importlib.import_module(package)
        # import package


from BSM import *
pd = getpack("pandas")
yf = getpack("yfinance")
dt = getpack("datetime")
dateutil = getpack("dateutil")
from dateutil import relativedelta


def main():
    print("Welcome, this is a cmd-line interface tool to calculate option prices based on the Black-Scholes formula.")
    print("If you are unfamiliar with Black-Scholes please read the README.md file.\n")

    log = ""

    results = pd.DataFrame(
        columns=["ID", "Type", "Expiration date", "Strike price", "Current price", "Estimated price"])

    while True:
        sel = input("\nIf you want to run a custom simulation enter '0'.\n"
                    "If you want to run simulations for a specific ticker based on option type and expiration dates "
                    "enter '1'.\n\nTo end the programm enter 'q'.\n")

        if sel == 'q':
            break

        elif sel == '0':
            custom()
            log += '0'

        elif sel == '1':
            results = results.append(ticker_based())
            log += '1'

        else:
            print("invalid selection")

    if '1' in log:
        if input("If you want to export the Black-Scholes data press any key and hit enter, else just press enter: "):
            results.to_csv(f"./Black_Scholes_Sims_{dt.datetime.now().strftime('%m-%d-%Y-%H-%M')}.csv")
            print("Data exported.\n")

    print("Thank you.\nGoodbye.")


def custom():
    option = input("Please enter the option type (put/call): ")
    s = float(input("Please enter the underlying security's price: "))
    k = float(input("Please enter the option's strike price: "))
    r = float(input("Please enter the risk-free interest rate (e.g. 3 month t-bill - format: 0.XX): "))
    q = float(input("Please enter the dividend rate (format: 0.XX): "))
    sigma = float(input("Please enter the sigma of the underlying security: "))
    t = float(input("Please enter the number of months to maturity: ")) / 12.0

    # if you want to check what is passed to the function uncomment below
    # print(f"black_sholes({s},{k},{t},{r},{sigma},{option},{q})")

    res = black_sholes(s, k, t, r, sigma, option, q)

    print(f"According to Black-Scholes the price of your selected {option} should be: {res}\n")

    choice = input("Do you want to run another custom simulation? (y/n)")

    if choice == "y":
        custom()

    return


def ticker_based():

    Ticker = input("Please enter the Ticker of the underlying security: ")
    option = input("Please enter the option type (put/call): ")

    # get data
    data_tick = yf.Ticker(Ticker)

    # current stock price
    s = data_tick.history(period="1y").Close[-1]

    # get standard deviation
    sigma = data_tick.history(period="5y").Close.std()/s

    # get risk-free rate (i.e. 3-month t-bill)
    r = yf.Ticker("^IRX").history(period="1y").Close[-1]/100

    # show dividends
    div = data_tick.dividends[-4:].mean()
    if math.isnan(div):
        div = 0.0

    inp = input("Please enter the expected dividend in USD, if you just hit enter the average dividend over the past 4 periods of {div} will be used: ")
    if len(inp) > 0:
        div = float(inp)
    del inp

    # dividend rate
    q = (div*4)/s

    # show options expirations
    dates = data_tick.options
    print("Following option expiration dates are available")
    for n, i in enumerate(dates):
        print(f"{i} ({n})")

    print("\n")

    date_sel = [int(x) for x in input("Please selected an expiration date by using the ID-Numbers (X) of the dates named"
                                      " above. You can make one or multiple selections seperated by a space.").split()]

    results = pd.DataFrame(columns=["ID", "Type", "Expiration date", "Strike price", "Current price", "Estimated price"])

    for i in date_sel:
        if option == "call":
            opt_data = data_tick.option_chain(dates[i]).calls
        else:
            opt_data = data_tick.option_chain(dates[i]).puts

        # time to end of contract:
        now = dt.datetime.now()
        end = dt.datetime.strptime(dates[i], '%Y-%m-%d')

        t = relativedelta.relativedelta(end, now).months/12.0

        for index, row in opt_data.iterrows():
            # option id
            symb = row[0]
            # current price
            current_price = row[3]

            # strike price
            k = row[2]

            # if you want to check what is passed to the function uncomment below
            # print(f"black_sholes({s},{k},{t},{r},{sigma},{option},{q})")

            est = black_sholes(s, k, t, r, sigma, option, q)

            results.loc[len(results)] = [symb, option, end, k, current_price, est]

    print(results)

    return results


main()
