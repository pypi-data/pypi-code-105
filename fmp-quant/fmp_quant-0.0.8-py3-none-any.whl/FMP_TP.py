# FMP Module for Target Prices

import pandas as pd
import numpy as np

class Target_Price:

    def __init__(self,
                 target_ticker:str,
                 option:str,
                 price_data:pd.DataFrame = None,
                 target_price:float = None,
                 var_price:float = 10,
                 high_channel:float = None,
                 low_channel:float = None,
                 moving_up_pct:float = None,
                 moving_down_pct:float = None,
                 only_once:bool = True,
                 extra_text:str = None,
                 is_crypto:bool = True):

        self._price_data = price_data,
        self._target_ticker = target_ticker
        self._option = option
        self._target_price = target_price
        self._var_price = var_price
        self._high_channel = high_channel
        self._low_channel = low_channel
        self._moving_up_pct = moving_up_pct
        self._moving_down_pct = moving_down_pct
        self._only_once = only_once
        self._expired = False
        self._extra_text = extra_text
        self._is_crypto = is_crypto


    def set_prices(self,price_data):
      self._price_data = price_data

    def get_title(self):

      base = self._target_ticker + ' ' + self._option + ' '

      if self._option == 'Equals' or self._option == 'Greater Than' or self._option == 'Less Than':

        title = base + str(self._target_price)

      elif self._option == 'Inside Channel' or self._option == 'Outside Channel':

        title = base + str(self._low_channel) + ' and ' + str(self._high_channel)

      elif self._option == 'Moving Up %':
        title = base + str(self._moving_up_pct) + '%'

      elif self._option == 'Moving Down %':
        title = base + str(self._moving_down_pct) + '%'
      else:
        title = base

      return title

    
    def set_expired_alert(self):
        self._expired = True

    def reset_expiration(self):
      self._expired = False

    def get_target_price(self) -> float:

        return self._target_price



    def get_current_price(self) -> float:

      price_df = self._price_data

      if not isinstance(price_df,pd.DataFrame): raise TypeError('Price data is not a dataframe')
        
      current_asset = price_df[price_df.index == self._target_ticker]

      current_price = current_asset['price'].values[0]

      return current_price

        

    # Options Logic

    
    def equals(self):
        

        current_price = self.get_current_price()

        low_range = self._target_price - self._var_price

        high_range = self._target_price + self._var_price

        if current_price <= high_range and current_price >= low_range:

            self._message = f'Target Price of {self._target_price} for {self._target_ticker} is triggered, current price is {current_price}'

            return True

        else:

            return False

    def greater_less_than(self,option:str = 'Greater Than'):

        current_price = self.get_current_price()

        target_price = self.get_target_price()

        if option == 'Greater Than':
            
            if current_price > target_price:

                self._message  = f'Current price for {self._target_ticker} is greater than {target_price}. Current price is {current_price}'

                return True
            else:
                return False
        
        elif option == 'Less Than':

            if current_price < target_price:

                self._message = f'Current price for {self._target_ticker} is less than {target_price}. Current price is {current_price}'

                return True
            else:
                 return False
        else:
            raise ValueError(f'{option} as an option is  not supported. Must be either Greater Than or Less Than')
        
    def inside_outside_channel(self,option:str = 'Inside Channel'):

        current_price = self.get_current_price()

        high_channel = self._high_channel

        low_channel = self._low_channel

        if option == 'Inside Channel':

            if current_price <= high_channel and current_price >= low_channel:

                self._message = f'Current price for {self._target_ticker} is inside channel between {low_channel} and {high_channel} with price of {current_price}'
                
                return True
            else:
                return False

        elif option == 'Outside Channel':

            if not (current_price <= high_channel and current_price >= low_channel):

                self._message = f'Current price for {self._target_ticker} is outside channel between {low_channel} and {high_channel} with price of {current_price}'
                
                return True
            else:
                return False
        else:
            raise ValueError(f'{option} as an option is not supported. Must be either Inside Channel or Outside Channel')


    def moving_up_down_pct(self,option='Moving Up %'):

        current_price = self.get_current_price()

        target_price = self.get_target_price()

        change = (current_price / target_price - 1) * 100

        if option == 'Moving Up %':

            target_change = self._moving_up_pct

            if change >= target_change:

                self._message = f'Current price for {self._target_ticker} at {current_price} is greater than or equal to {target_change}% from {target_price}'
                
                return True
            else:
                return False
        
        elif option == 'Moving Down %':

            target_change = self._moving_down_pct

            if change <= target_change:

                self._message = f'Current price for {self._target_ticker} at {current_price} is less than or equal to {target_change}% from {target_price}'

                return True
            else:
                return False

        else:

            raise ValueError(f'{option} is not supported, must be either Moving Up % or Moving Down %')

    
    def run(self):

        if self._expired == True: return (False,None)

        if self._price_data is None: return (False,None)
        
        option = self._option

        state:bool = False

        if option == 'Equals':
            
            state = self.equals()

        elif option == 'Greater Than' or option == 'Less Than':
            state = self.greater_less_than(option=option)
        
        elif option == 'Inside Channel' or option == 'Outside Channel':
            state = self.inside_outside_channel(option=option)

        elif option == 'Moving Up %' or option == 'Moving Down %':
            state = self.moving_up_down_pct(option=option)
        else:
            raise ValueError(f'{option} not supported: Use the following:Equals, Greater Than, Less Than, Inside Channel, Outside Channel,Moving Up %, Moving Down %')

        if state == True:

            if self._only_once == True: self.set_expired_alert()

            msg = self._message + ' ' + self._extra_text if self._extra_text is not None else self._message

            return (True, msg)

        else:
            return (False,None)

class Target_Prices_Bank:

    def __init__(self,alerts):
        self._alerts = alerts

    def set_price_data(self,price_data):

      for alert in self._alerts:

        alert.set_prices(price_data)

    def get_non_crypto_tickers(self):

      alerts = self.get_alerts()

      non_crypto_tickers = [alert._target_ticker for alert in alerts if alert._is_crypto == False]

      return non_crypto_tickers

    def count_alerts(self):
        return len(self._alerts)

    def get_alerts(self):
        return self._alerts

    def append_alert(self,alert:Target_Price):

        self._alerts.append(alert)

    def get_summary(self):

      alerts = self.get_alerts()
      n_alerts = self.count_alerts()

      deactivated_alerts = [deactivated for deactivated in alerts if deactivated._expired == True]

      activated_alerts = [deactivated for deactivated in alerts if deactivated._expired == False]

      n_alerts_deactivated = len(deactivated_alerts)

      n_alerts_activated = len(activated_alerts)

      text = f""" 

      Number of Deactivated Alerts: {n_alerts_deactivated}
      
      Number of Activated Alerts: {n_alerts_activated}
      
      """

      return text

    def reset_expirations(self):

      for idx,alert in enumerate(self._alerts):

        new_alert = alert
        new_alert.reset_expiration()

        self._alerts[idx] = new_alert        






        






    



        
        

    

    
