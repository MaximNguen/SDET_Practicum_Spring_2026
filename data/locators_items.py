from selenium.webdriver.common.by import By

class ItemPageLocators:
    """Класс для хранения локаторов элементов на странице товаров."""
    
    filter_select = (By.ID, 'sort')
    cards = (By.CSS_SELECTOR, '.col-md-3.col-sm-6.col-xs-12')
    name_product = (By.CSS_SELECTOR, '.prdocutname')
    price_product = (By.CSS_SELECTOR, '.oneprice')
    price_product_new = (By.CSS_SELECTOR, '.pricenew')