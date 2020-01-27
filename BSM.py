import math


# return value of normal distribution (mu=0, sigma=1) at point x
def phi(x):
    return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)


# return value of cumulative distribution function (mu=0, sigma=1) at point x
def Phi(z):
    if z < -8.0:
        return 0.0
    if z > 8.0:
        return 1.0
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


def black_sholes(s, k, t, r, sigma, type="call", q=0.0):
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
