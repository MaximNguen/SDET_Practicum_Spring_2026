from selenium.webdriver.common.by import By

class CartPageLocators:
    """Класс для хранения локаторов элементов на странице корзины."""
    
    table = (By.CSS_SELECTOR, '#cart > div > div.container-fluid.cart-info.product-list > table')
    cart_rows = (By.CSS_SELECTOR, "tbody tr")
    name_product = (By.CSS_SELECTOR, 'td.align_left a')
    unit_price = (By.CSS_SELECTOR, "td.align_right")
    quantity_input = (By.CSS_SELECTOR, "input[type='text'][name^='quantity']")
    total_price_on_product = (By.CSS_SELECTOR, "td.align_right")
    total_price = (By.XPATH, "//span[@class='bold totalamout' and not(contains(text(), 'Total'))]")