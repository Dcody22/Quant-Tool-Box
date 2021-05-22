from Quant_Tool_Box import POD, BSM_Model

#POD Example
#defne model parameters
model = POD(Total_Assets = 1000000, Debt=500000, annual_mu=.15, annual_sigma=.40, risk_free_rate=.05, delta_t=1)
print('POD Class Example Output:')
print('__________________________')

#get probabilty of defualt 
probability = model.get_POD()
print(f"Firm's probability of default: {probability}")

#value firms equity
equity_value = model.value_equity()
print(f"Value of firm's equity: {equity_value}")

#value of firm put option 2
put_value = model.value_firm_put()
print(f"Value of firm's put: {put_value}")

#value of firms safe debt 
safe_debt = model.value_safe_debt()
print(f"\nValue of firm's safe debt: {safe_debt}")

#value of firms debt 
debt_value = model.value_debt()
print(f"Value of firm's debt: {debt_value}")

#firms cost of debt 
ytm = model.get_ytm()
print(f"YTM on firms debt: {ytm}")

#BSM Example 
#defne model parameters
bsm_call = BSM_Model(Flag = 'call', S = 100, K = 105, dt = .25, r = .05, sigma = .4, dividend_yield=.02)
bsm_put = BSM_Model(Flag = 'put', S = 100, K = 105, dt = .25, r = .05, sigma = .4, dividend_yield=.02)

print('___________________________')
print('\nBSM_Model Example output\n')
print('__________________________')

#get price of call option 
call_price = bsm_call.BlackScholes(verbose= True)

#price of put option
put_price = bsm_put.BlackScholes(verbose= True)

print(f"BSM price of call option: {call_price}")
print(f"BSM price of put option: {put_price}")

#get implied volatility of call 
call_market_price = 7
print(f"Market price of call: {call_market_price}")
call_iv = bsm_call.Implied_Vol(price = call_market_price)
print(f"IV of call option: {call_iv}")

#get implied volatility of put
put_market_price = 10
print(f"Market price of put: {put_market_price}")
put_iv = bsm_put.Implied_Vol(price = put_market_price)
print(f"IV of put option: {put_iv}")

#get greeks of call 
call_greeks_dict = bsm_call.Get_Greeks()
print('Greeks of Call:')
print(call_greeks_dict)

#get greeks of put 
put_greeks_dict = bsm_put.Get_Greeks()
print('Greeks of Put:')
print(put_greeks_dict)











