# Black-Scholes-Merton option pricing

The Black Scholes model, also known as the Black-Scholes-Merton (BSM) model, is a mathematical model for pricing an options contract.

The insight
- By combining a position in the option with a position in the underlying security, it is possible to create a portfolio which is riskless over an infinitesimal time period
- No arbitrage implies that, over this infinitesimal time period, the return on this portfolio must be equal to the riskless rate of interest
- These prices do not depend on: risk preference and or the expected return on the underlying security
- So-called “risk neutral” valuation methods are based on this observation

Assumptions
- The stock price follows a geometric Brownian motion with drift μ and volatility σ
- Continuous trading, no restriction on short sales
- No transaction cost, no taxes
- Constant riskless rate of interest

A note on the derivation
- Consider a portfolio consisting of one long option position (say, a call) and short position in some quantity ∆ of the stock: Π = c(S, t) − ∆ × S 
- Consider the change in value of Π from t to t + dt. This change is partly due to the change in the option value and partly due to the change in the stock 
- Also, the change in value is composed of a deterministic part associated with dt and a random part associated with the risk of the stock 
- Since the value of the option is dependent on the value of the stock, we can eliminate the random part by choosing an appropriate ∆ 
- Now we have a portfolio whose change in value is completely deterministic and thus riskless 
- Together with assumptions on the stochastic process that the stock follows we can derive the B-S formula 

Formula

<p align="center"><img src="./img_formula/d1_d2.png" alt="d1d2" align="middle" /></p>

- Call (with N as the c.d.f. of a standard normal):

<p align="center"><img src="./img_formula/C.png" alt="C" align="middle" /></p>


- Put:

<p align="center"><img src="./img_formula/P.png" alt="P" align="middle" /></p>


### About this code:
