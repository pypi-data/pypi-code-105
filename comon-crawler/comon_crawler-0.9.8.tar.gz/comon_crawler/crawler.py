import json
from typing import List, Generator, Optional

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement

from . import schemas
from .core import CrawlerCore, Selector, Event


def crawler_method_provider(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        self.start()
        self.login()
        try:
            result = func(*args, **kwargs)
        except TimeoutException:
            result = func(*args, **kwargs)
        self.stop()
        return result

    return wrapper


class ComonCrawler(CrawlerCore):
    base_url = 'https://www.comon.ru'

    def __init__(self,
                 username: str,
                 password: str,
                 debug: bool = False,
                 remote: bool = False):
        self.username = username
        self.password = password
        super(ComonCrawler, self).__init__(debug=debug, remote=remote)

    def _go_to_main_page(self):
        url = f'{self.base_url}/'
        self.driver.get(url)

    def _go_to_login_page(self):
        url = f'{self.base_url}/login/'
        self.driver.get(url)

    def _go_to_trading_cabinet_page(self, account_id: int = None):
        url = f'{self.base_url}/cabinet'
        if account_id:
            url = f'{url}/?ac={account_id}&apgt=1'
        self.driver.get(url)

    def _go_to_strategy_detail_page(self, username: str, strategy_id: int):
        url = f'{self.base_url}/user/{username}/strategy/detail/?id={strategy_id}'
        self.driver.get(url)

    def login(self):
        self._go_to_login_page()

        username_field = self.wait_element(Selector.by_id, 'id-login')
        password_field = self.wait_element(Selector.by_id, 'id-password')
        submit_button = self.wait_element(Selector.by_id, 'id-authorize')
        self.send_keys(username_field, self.username)
        self.send_keys(password_field, self.password)
        self.click_on_element(submit_button)
        self.wait(3)

    @classmethod
    def _get_strategy_table_row_value(cls, row: WebElement) -> str:
        return row.find_elements_by_tag_name('td')[1].text

    def _get_strategy_plot_data(self, strategy_id: int) -> List[schemas.DataPlotSchema]:
        url = f'{self.base_url}/amcharts/chartdata.ashx?source=TradingStrategy&sourceId={strategy_id}'
        self.driver.get(url)
        raw_plot_data = json.loads(self.wait_element(Selector.by_tag_name, 'pre').text)
        return [schemas.DataPlotSchema(**data) for data in raw_plot_data]

    def _get_strategy_detail_data(self, strategy_id: int) -> schemas.StrategySchema:
        kpi_panel = self.wait_element(Selector.by_id, 'panel_accuracyFollowing')
        self.change_element_class_name(kpi_panel, 'mb20')
        kpi_table = kpi_panel.find_element_by_tag_name('table')
        kpi_table_rows = kpi_table.find_elements_by_tag_name('tr')
        total_profitability_row = kpi_table_rows[1]
        monthly_profitability_row = kpi_table_rows[10]
        yearly_profitability_row = kpi_table_rows[12]
        total_profitability_value = self._get_strategy_table_row_value(total_profitability_row)
        yearly_profitability_value = self._get_strategy_table_row_value(yearly_profitability_row)
        monthly_profitability_value = self._get_strategy_table_row_value(monthly_profitability_row)
        data_plots = self._get_strategy_plot_data(strategy_id)
        strategy = schemas.StrategySchema(
            strategy_id=strategy_id,
            yearly_profitability_percentage=yearly_profitability_value,
            monthly_profitability_percentage=monthly_profitability_value,
            total_profitability_percentage=total_profitability_value,
            data_plots=data_plots
        )
        return strategy

    def _generate_strategy_data(self) -> Generator[schemas.StrategySchema, None, None]:
        strategy_ids = [8364, 18470]
        strategy_holder_username = 'alexlk'
        for strategy_id in strategy_ids:
            self._go_to_strategy_detail_page(username=strategy_holder_username, strategy_id=strategy_id)
            strategy_data = self._get_strategy_detail_data(strategy_id)
            yield strategy_data

    @crawler_method_provider
    def get_strategy_data(self, strategy_id: int, owner_username: str) -> schemas.StrategySchema:
        self._go_to_strategy_detail_page(username=owner_username, strategy_id=strategy_id)
        strategy_data = self._get_strategy_detail_data(strategy_id)
        return strategy_data

    @staticmethod
    def _group_deals(deals: List[schemas.TradingDealSchema]) -> List[schemas.TradingDealSchema]:
        pass

    def _trading_is_available(self) -> bool:
        warning_message = self.wait_element(Selector.by_id,  'mesBriefcase')
        if warning_message.text == "":
            return True
        return False

    @crawler_method_provider
    def get_trading_portfolio_data(self, account_id: int = None) -> Optional[schemas.PortfolioSchema]:
        self._go_to_trading_cabinet_page(account_id)
        if not self._trading_is_available():
            return None
        portfolio_loader = self.wait_element(Selector.by_id, 'briefcaseLoader', condition=Event.be_invisible)
        portfolio_table_body = self.wait_element(Selector.by_id, 'tblBriefcaseBody')
        trading_assets = portfolio_table_body.find_elements_by_tag_name('tr')
        assets_data = list()
        for asset in trading_assets:
            asset_values = asset.find_elements_by_tag_name('td')
            current_price = asset_values[1].text
            currency = current_price
            if asset_values[0].text == "Доллар США":
                continue
            asset_data = schemas.TradingAssetSchema(
                name=asset_values[0].text,
                money_sum=asset_values[4].text,
                portfolio_percentage=asset_values[5].text,
                is_short="-" in asset_values[5].text,
                currency=currency
            )
            avg_price = asset_values[2].text
            count = asset_values[3].text.replace(" ", "")
            if all([bool(current_price), bool(avg_price), bool(count)]):
                asset_data.count = count
                asset_data.current_price = current_price
                asset_data.avg_price = avg_price
            else:
                asset_data.is_primary = True
            assets_data.append(asset_data)

        deals = []
        buttons_panel = self.driver.find_elements_by_xpath(".//ul[@class='b-box-title-tabs']")[1]
        deals_tab = buttons_panel.find_elements_by_class_name("item")[2]
        self.click_on_element(deals_tab)
        deal_table_body = self.wait_element(Selector.by_id, 'tblTrades')
        deal_table_rows = deal_table_body.find_elements_by_tag_name('tr')
        del deal_table_rows[0]
        for deal_row in deal_table_rows:
            deal_values = deal_row.find_elements_by_tag_name('td')
            deal = schemas.TradingDealSchema(
                name=deal_values[0].text,
                operation=deal_values[1].text,
                price=deal_values[2].text,
                count=deal_values[3].text.replace(" ", ''),
                summary=deal_values[4].text,
                time_created=deal_values[5].text
            )
            deals.append(deal)

        groupped_deals = self._group_deals(deals)
        portfolio_data = schemas.PortfolioSchema(assets=assets_data, deals=groupped_deals)
        return portfolio_data

    @staticmethod
    def _group_deals(deals: List[schemas.TradingDealSchema]) -> List[schemas.TradingDealSchema]:
        groupped = []
        groups = dict()
        for deal in deals:
            key = f"{deal.name} {deal.operation} {deal.time_created}"
            group = groups.get(key, None)
            if not group:
                groups[key] = [deal]
            else:
                group.append(deal)

        for _, group_items in groups.items():
            groupped_item: schemas.TradingDealSchema = group_items[0]
            if len(group_items) == 1:
                groupped.append(groupped_item)
                continue
            for item in group_items[1:]:
                groupped_item.count += item.count
                groupped_item.summary += item.summary
            groupped.append(groupped_item)
        return groupped

    @crawler_method_provider
    def trading_account_exists(self, account_id: int) -> bool:
        self._go_to_trading_cabinet_page(account_id)
        url = self.driver.current_url
        self.wait(3)
        return url.find(str(account_id)) != -1

    @crawler_method_provider
    def auth_data_is_valid(self) -> bool:
        try:
            self.wait_element(Selector.by_class_name, 'error-message')
        except TimeoutException:
            return True
        return False
