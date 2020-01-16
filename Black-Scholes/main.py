import math


#return value of normal distribution (mu=0, sigma=1) at point x
def phi(x):
    return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)

#return value of cumulative distribution function (mu=0, sigma=1) at point x
def Phi(z):
    if z < -8.0: return 0.0
    if z > 8.0: return 1.0
    total = 0.0
    term = z
    i = 3
    while total != total + term:
        total += term
        term *= z * z / float(i)
        i += 2
    return 0.5 + total * phi(z)

def cdf(z, mu=0.0, sigma=1.0):
    return Phi((z - mu) / sigma)





def black_sholes(s,k,t,r,sigma,type="call",q=0.0):
    d1 = (math.log(s/k) + (r - q + sigma * sigma/2.0) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)

    if type == "call":
        res = s * math.exp(-q * t) * cdf(d1) - k * math.exp(-r * t) * cdf(d2)
    elif type == "put":
        res = k * math.exp(-r * t) * cdf(-d2) - s * math.exp(-q * t) * cdf(-d1)

    else:
        print(f"invalid type selection: {type}. Types are 'put' or 'call\n")
        return

    return res



def main():
    print("Welcome, this is a cmd-line interface tool to calculate option prices based on the Black-Scholes formula.")
    print("If you are unfamiliar with Black-Scholes please read the README.md file.\n")
    print("You can end this program by pressing 'ctrl' + 'c' at any time.\n")
    while True:
        try:
            option = input("Please enter the option type (put/call): ")
            s = float(input("Please enter the option's spot rate: "))
            k = float(input("Please enter the option's strike price: "))
            r = float(input("Please enter the risk-free interest rate (e.g. 3 month t-bill - format: 0.XX): "))
            q = float(input("Please enter the dividend rate (format: 0.XX): "))
            sigma = float(input("Please enter the sigma of the underlying security: "))
            t = float(input("Please enter the number of months to maturity: "))/12.0

            print(f"black_sholes({s},{k},{t},{r},{sigma},{option},{q})")

            res = black_sholes(s,k,t,r,sigma,option,q)

            print(f"According to Black-Scholes the price of your selectef {option} should be: {res}\n")

        except KeyboardInterrupt:
            print("\nThank you, goodbye.")
            break


main()
