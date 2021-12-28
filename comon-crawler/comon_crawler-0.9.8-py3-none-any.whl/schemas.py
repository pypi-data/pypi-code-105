import re
import enum
import datetime
from typing import List, Optional, Union, Any

from pydantic import BaseModel, validator, Field


def parse_percentage(value: str) -> float:
    match = re.search(r'([+-]\d+(\.\d+)?%)', value.replace(' ', ''))
    if not match:
        return 0.0
    _numeric_value = match.group(1).replace('%', '')
    return float(_numeric_value)


def price_validator(value: str) -> float:
    deprecated_symbols = ["₽", "$", " "]
    formatted = value.strip()
    for symbol in deprecated_symbols:
        formatted = formatted.replace(symbol, '')
    try:
        return float(formatted)
    except ValueError:
        return 0


class DataPlotSchema(BaseModel):
    date: datetime.date
    value: float = Field(..., alias='val')


class StrategySchema(BaseModel):
    strategy_id: int
    total_profitability_percentage: float
    yearly_profitability_percentage: float
    monthly_profitability_percentage: float
    data_plots: List[DataPlotSchema] = []

    @validator('total_profitability_percentage', pre=True)
    def _percentage_validator_t(cls, value):
        return parse_percentage(value)

    @validator('monthly_profitability_percentage', pre=True)
    def _percentage_validator_m(cls, value):
        return parse_percentage(value)

    @validator('yearly_profitability_percentage', pre=True)
    def _percentage_validator_y(cls, value):
        return parse_percentage(value)


class Currency(enum.Enum):
    ruble = 0
    dollar = 1


class TradingAssetSchema(BaseModel):
    date: Optional[datetime.datetime] = None
    name: str
    avg_price: Optional[float] = None
    current_price: Optional[float] = None
    count: Optional[int] = None
    money_sum: Optional[float] = None
    portfolio_percentage: float
    is_primary: bool = False
    currency: Currency = Currency.ruble
    is_short: bool = False

    class Config:
        validate_assignment = True

    @validator('avg_price', 'current_price', 'money_sum', pre=True, always=True)
    def _price_validator(cls, value):
        if not value:
            return None
        return price_validator(value)

    @validator("currency", pre=True, always=True)
    def _currency_validator(cls, value):
        if '₽' in value:
            return Currency.ruble
        if '$' in value:
            return Currency.dollar
        return Currency.dollar


class TradingDealSchema(BaseModel):
    name: str
    operation: str
    price: float
    count: int
    summary: float
    time_created: datetime.time
    date_created: datetime.date = datetime.date.today()

    class Config:
        validate_assignment = True

    @validator('summary', 'price',  pre=True, always=True)
    def _price_validator(cls, value):
        if isinstance(value, float):
            return value
        return price_validator(value)


class PortfolioSchema(BaseModel):
    deals: List[TradingDealSchema] = []
    assets: List[TradingAssetSchema] = []
