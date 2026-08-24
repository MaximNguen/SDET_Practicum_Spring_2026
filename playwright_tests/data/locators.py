"""Локаторы элементов для страниц.

В Playwright локатор — это строка (CSS/XPath) или role-based селектор,
а не кортеж (By.CSS_SELECTOR, "..."), как в Selenium.
"""


class MainPageLocators:
    navbar_list = "ul.nav-pills.categorymenu"
    search_input = "#filter_keyword"
    product_cards = ".col-md-3.col-sm-6.col-xs-12"
    product_name = ".prdocutname"
    product_cart_button = ".productcart"
    cart_button = "a[href*='rt=checkout/cart']"


class ItemPageLocators:
    filter_select = "#sort"
    cards = ".col-md-3.col-sm-6.col-xs-12"
    name_product = ".prdocutname"
    price_product = ".oneprice"
    price_product_new = ".pricenew"


class ProductPageLocators:
    input_quantity = "#product_quantity"
    option_radio_buttons = "input[type='radio'][name^='option']"
    add_to_cart_button = "a.cart"


class SearchPageLocators:
    cards = ".col-md-3.col-sm-6.col-xs-12"
    cart_button = ".productcart"


class CartPageLocators:
    table = "#cart > div > div.container-fluid.cart-info.product-list > table"
    cart_rows = "tbody tr"
    name_product = "td.align_left a"
    unit_price = "td.align_right"
    quantity_input = "input[type='text'][name^='quantity']"
    remove_item_button = "a[href*='remove=']"
    total_price = 'span.bold.totalamout:not(:has-text("Total"))'
