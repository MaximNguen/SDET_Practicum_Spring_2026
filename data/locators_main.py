from selenium.webdriver.common.by import By


class MainPageLocators:
    """Класс для хранения локаторов элементов и значений ячеек на странице."""

    navbar_list = (By.CSS_SELECTOR, "ul.nav-pills.categorymenu")
    search_input = (By.ID, "filter_keyword")
    product_cards = (By.CSS_SELECTOR, ".col-md-3.col-sm-6.col-xs-12")
    product_name = (By.CSS_SELECTOR, ".prdocutname")
    product_cart_button = (By.CSS_SELECTOR, ".productcart")
    cart_button = (By.CSS_SELECTOR, "a[href*='rt=checkout/cart']")
    logo_button = (By.CSS_SELECTOR, 'a[class="logo"]')
    