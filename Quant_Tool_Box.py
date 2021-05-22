
"""
Requirements: 

pip install scipy
pip install numpy 
pip install py_vollib

or 

pip3 install scipy
pip3 install numpy 
pip3 install py_vollib

"""

from scipy.stats import norm
import numpy as np
from py_vollib.black_scholes.implied_volatility import implied_volatility



""" 
The Black Scholes Documentation:

    Inputs:
        __init__
            - Flag (str): This is set to 'call' for call option or 'put; for put options
            - S (float): Price of underlying 
            - K (float): Strike price
            - dt (float): Time in years till the contract expires
            - r (float): Risk free rate
            - sigma (float): Annualized volatility of stock 
            - dividend yield (float): Annual dividend yield, default = None
    Methods: 
        BlackScholes
        - Function to price call and put options of stocks using the Black Scholes Merton Model 
        
            Inputs:
            - Self
            - verbose (Bool): prints value of underlying less pv of continious dividends
        
            Returns 
            Price of a call/put option (float)
        
            Exceptions: 
                Attribute error  
                    :if Flag is not 'Call', 'call', 'Put', or 'Put'
                    
        Implied_vol
            Inputs
            - price (float): Market price of call/put
            - verbose (Bool): prints value of underlying less pv of continious dividends

        
            Returns 
            Market implied volatility of a call/put option (float)
        
                
        get_greeks
            Inputs: 
            - Self 
            
            Returns 
            - dictionary of the option's greeks (dictionary)

"""
class BSM_Model:
    
    def __init__(self, Flag, S, K, dt, r, sigma, dividend_yield = None):
        self.__Flag = Flag
        self.__S= S
        self.__K = K
        self.__dt = dt
        self.__r = r
        self.__sigma = sigma
        self.__div_yield = dividend_yield
        
    
    def BlackScholes(self, verbose = False):
        #print('S:',S, '\nSigma:',sigma, '\ndt:', dt, '\nr:', r, '\nK', K )
        if self.__div_yield != None:
            V0= self.__S * np.exp(-(self.__r-self.__div_yield)*self.__dt)
            if verbose == True:
                print('Value of underlying less present value of dividend payments:', V0)
        else: 
            V0 = self.__S
            
        d1 = (np.log(V0/self.__K) + (self.__r +.5*self.__sigma**2)*self.__dt)/self.__sigma
        d2 = d1-self.__sigma*np.sqrt(self.__dt)
        try:
            if self.__Flag == 'call':
                call_price = round(V0*norm.cdf(d1) - self.__K*np.exp(-self.__r*self.__dt)*norm.cdf(d2),2)
                return float(call_price)
            if self.__Flag =='put':
                put_price = round(self.__K*np.exp(-self.__r*self.__dt)*norm.cdf(-d2) - V0*norm.cdf(-d1),2)
                return float(put_price)
        except: 
            print()
            print("Set Flag as 'Call' or 'Put'. :) ")
            print()
            raise AttributeError
        
    def Implied_Vol(self, price, verbose = False): 
        if self.__Flag == 'call': 
            flag = 'c'
        if self.__Flag == 'put':
            flag = 'p'
        if self.__div_yield != None:
            V0 = self.__S * np.exp(-(self.__r-self.__div_yield)*self.__dt)
            if verbose == True:
                print('Value of underlying less pv of dividend payments:', V0)
                
        iv = implied_volatility(price = price,
                                S = V0,
                                K = self.__K,
                                t = self.__dt,
                                r = self.__r, 
                                flag = flag)
        return iv
    
    def Get_Greeks(self, verbose = False):
        S = self.__S
        K = self.__K
        
        if self.__div_yield != None:
            V0 = self.__S * np.exp(-(self.__r-self.__div_yield)*self.__dt)
        if verbose == True:
            print('Value of underlying less pv of dividend payments:', V0)
        else:
            V0 = self.__S
        
        d1 = (np.log(V0/self.__K) + (self.__r +.5*self.__sigma**2)*self.__dt)/self.__sigma
        d2 = d1-self.__sigma*np.sqrt(self.__dt)
        gamma = norm.cdf(d1)/(V0*self.__sigma*np.sqrt(self.__dt))
        if self.__Flag == 'call': 
            S_delta = norm.cdf(d1)
            K_delta = -np.exp(-self.__r*self.__dt)*norm.cdf(d2)
            rho = self.__dt*self.__K*np.exp(-self.__r*self.__dt)*-np.exp(-self.__r*self.__dt)*norm.cdf(d2)
            theta = -V0*norm.cdf(d1)*((.5*self.__sigma)/np.sqrt(self.__dt))-self.__r*K*np.exp(-self.__r*self.__dt)* norm.cdf(d2)
            vega = V0*norm.cdf(d1)*np.sqrt(self.__dt)
        if self.__Flag == 'put': 
            S_delta = norm.cdf(-d1)
            K_delta = np.exp(-self.__r*self.__dt)*norm.cdf(-d2)
            rho = -self.__dt*K*np.exp(-self.__r*self.__dt)*np.exp(-self.__r*self.__dt)*norm.cdf(-d2)
            theta = -V0*norm.cdf(d1)*((.5*self.__sigma)/np.sqrt(self.__dt))+self.__r*self.__K*np.exp(-self.__r*self.__dt)* norm.cdf(-d2)
            vega = V0*norm.cdf(-d2)*np.sqrt(self.__dt)
            
        return {
            'Asset Price Delta': S_delta,
            'Excercise Price Delta': K_delta,
            'Rho': rho,
            'Theta': theta,
            'Vega': vega, 
            'Gamma': gamma, 
        }
        
"""
Probabilty of Defualt Documentation: 
    Inputs: 
        - Total_Assets (float): Value of firm's assets 
        - Debt (float): Face value of firms debt
        - annual_mu (float): Annual growth rate forecast 
        - annual_sigma (float): Annualized volatility of company's value 
        - risk_free_rate (float): Riskless rate of interest 
        -delta_t (float): Annualized change in time 
            Note: delta_t = 1 would return the probability of default in one year 
            
    Methods: 
        get_POD:
            Description:
                Probability of default using lognormal and Geometric Brownian 
                Motion assumptions
            Inputs: 
                Self 
            Returns:
                Probability of default (float)
                
        value_equity:
            Description: 
                Value of firm's equity using the forecasted growth rate as the discount rate 
            
            Inputs:
                Self 
                
        value_firm_put:
            Description: 
                   Value of a put option of a firm's assets where the strike 
                   price is the promised payment to credit holders

            Inputs:
                Self 
                
            Returns:
                Value of firm's put (float)
                
        value_safe_debt: 
            Description: 
                Value of a firm's riskless debt 
                
            Inputs: 
                Self 
                
        value_debt:
            Description: 
                Value of the firm's debt is the value of the safe debt less the 
                value of the firm's put option. 
                
            Inputs: 
                Self
                
            Returns: 
                Value of a firm's debt (float)
                
            get_ytm: 
                Description: 
                    Cost of firm's debt 
                    
                Inputs: 
                    Self 
                    
                Returns: 
                    Yield to maturity of firm’s debt (float    
"""
class POD:
    def __init__(self, Total_Assets, Debt, annual_mu, annual_sigma, risk_free_rate, delta_t): 
        self.__VF = Total_Assets
        self.__B = Debt
        self.__mu = annual_mu
        self.__sigma = annual_sigma
        self.__r = risk_free_rate
        self.__dt = delta_t
        self.__d1 = (np.log(self.__VF/self.__B)+(self.__r +0.5*self.__sigma**2)*self.__dt)/(self.__sigma*np.sqrt(self.__dt))
        self.__d2 = self.__d1 - self.__sigma*np.sqrt(self.__dt)
        
    def get_POD(self):
        """
        Probability of default using lognormal and Geometric Brownian 
        Motion assumptions
        """
        z_defualt = (np.log(self.__B/self.__VF)-(self.__mu-0.5*self.__sigma**2)*self.__dt)/(self.__sigma*np.sqrt(self.__dt))
        return norm.cdf(z_defualt)
        
    def value_equity(self):
        """
        Value of a firm is the price of a call option on the firm's
        assets where the strike price is the promised payment to 
        credit holders
        """
        return self.__VF*norm.cdf(self.__d1)-self.__B*np.exp(-self.__r)*norm.cdf(self.__d2)
    
    def value_firm_put(self):
        """
        Value of a put option of a firms assets where the strike 
        price is the promised payment to creditholders
        """
        put = self.__B * np.exp(-self.__r*self.__dt) * norm.cdf(-self.__d2) - self.__VF * norm.cdf(-self.__d1)
        return put
    
    def value_safe_debt(self):
        """
        Value of a firms riskless debt 
        """
        return self.__B*np.exp(-self.__r*self.__dt)
    
    def value_debt(self): 
        """
        Value of firms debt
        """
        VP = self.value_firm_put()
        VB = self.value_safe_debt()
        return VB - VP      
    
    def get_ytm(self): 
        """
        Yield to maturity of firms debt 
        """
        VD = self.value_debt()
        return np.log(self.__B/VD)/self.__dt
        