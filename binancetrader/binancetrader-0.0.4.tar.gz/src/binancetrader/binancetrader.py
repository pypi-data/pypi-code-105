import requests


"""binance trader main class"""
class BinanceTrader:
    def __init__(self,
                strat:      str = "strategy",
                address:    str = "8.8.8.8",
                port:       int = 8000,
                api_key:    str = "123456"):

        self.strat  = strat
        self.address= address
        self.port   = port
        if port is None:
            self.url    = "https://"+self.address+"/algotrade/"
        else:
            self.url    = "http://"+self.address+":"+str(self.port)+"/algotrade/"
        self.header = {'Authorization': 'Token '+str(api_key)}


    """to send a market order"""
    def marketOrder(self,symbol,side,quantity):
        data = {
            "strat"     : self.strat,
            "symbol"    : symbol.upper(),
            "side"      : side.upper(),
            "quantity"  : str(quantity)
        }
        res  = requests.post(self.url+"MarketOrder/", headers=self.header, data=data)
        return res.json()


    """to send a limit order"""
    def limitOrder(self,symbol,side,quantity,price):
        data = {
            "strat"     : self.strat,
            "symbol"    : symbol.upper(),
            "side"      : side.upper(),
            "quantity"  : str(quantity),
            "price"     : str(price)
        }
        res  = requests.post(self.url+"LimitOrder/", headers=self.header, data=data)
        return res.json()


    """to send a stop order"""
    def stopOrder(self,symbol,side,quantity,price,stopPrice):
        data = {
            "strat"     : self.strat,
            "symbol"    : symbol.upper(),
            "side"      : side.upper(),
            "quantity"  : str(quantity),
            "price"     : str(price),
            "stopPrice" : str(stopPrice)
        }
        res  = requests.post(self.url+"StopOrder/", headers=self.header, data=data)
        return res.json()


    """to send a tp order"""
    def takeProfitOrder(self,symbol,side,quantity,price,stopPrice):
        data = {
            "strat"     : self.strat,
            "symbol"    : symbol.upper(),
            "side"      : side.upper(),
            "quantity"  : str(quantity),
            "price"     : str(price),
            "stopPrice" : str(stopPrice)
        }
        res  = requests.post(self.url+"TakeProfitOrder/", headers=self.header, data=data)
        return res.json()


    """to send a trailstop order"""
    def trailStopOrder(self,symbol,side,quantity,activationPrice,callbackRate):
        data = {
            "strat"             : self.strat,
            "symbol"            : symbol.upper(),
            "side"              : side.upper(),
            "quantity"          : str(quantity),
            "activationPrice"   : str(activationPrice),
            "callbackRate"      : str(callbackRate)
        }
        res  = requests.post(self.url+"TrailStopOrder/", headers=self.header, data=data)
        return res.json()


    """to get current positions"""
    def currentPositions(self,symbol):
        data = {
            "strat"     : self.strat,
            "symbol"    : symbol.upper(),
        }
        res  = requests.post(self.url+"CurrentPositions/", headers=self.header, data=data)
        return res.json()
    
    
    """to close all current positions"""
    def closeCurrentPositions(self,symbol):
        data = {
            "strat"     : self.strat,
            "symbol"    : symbol.upper(),
        }
        res  = requests.post(self.url+"CloseCurrentPositions/", headers=self.header, data=data)
        return res.json()


    """to get current orders"""
    def currentOrders(self,symbol):
        data = {
            "strat"     : self.strat,
            "symbol"    : symbol.upper(),
        }
        res  = requests.post(self.url+"CurrentOrders/", headers=self.header, data=data)
        return res.json()
    
    
    """to cancel a specific order"""
    def cancelOrder(self,symbol,orderId):
        data = {
            "strat"     : self.strat,
            "symbol"    : symbol.upper(),
            "orderId"   : int(orderId),
        }
        res  = requests.post(self.url+"CancelOrder/", headers=self.header, data=data)
        return res.json()


    """to cancel all open orders"""
    def cancelAllOpenOrder(self,symbol):
        data = {
            "strat"     : self.strat,
            "symbol"    : symbol.upper(),
        }
        res  = requests.post(self.url+"CancelAllOpenOrder/", headers=self.header, data=data)
        return res.json()