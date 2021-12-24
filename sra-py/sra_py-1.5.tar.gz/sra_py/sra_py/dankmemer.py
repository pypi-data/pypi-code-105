import requests

BASE = "https://some-random-api.ml/dank/sale"

class DankMemerItem:
    def __init__(self , raw: dict):
        self.raw = raw

    @property
    def name(self):
        return self.raw['name']

    @property
    def description(self):
        return self.raw['description']

    @property
    def image_url(self):
        return self.raw['item_picture']

    @property
    def original_price(self):
        return self.raw['original_price']

    @property
    def discounted_price(self):
        return self.raw['discounted_price']

    @property
    def discount_percent(self):
        return self.raw['discount_percent']

    @property
    def last_update(self):
        return self.raw['last_updated_utc']

    @property
    def last_update_epoch(self):
        return self.raw['last_updated_utc_epoch']

def current_sale_item():
    r = requests.request("GET" , BASE).json()
    return DankMemerItem(r)