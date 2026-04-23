from selenium.webdriver.common.by import By


class ProductPageLocators:
    """Класс для хранения локаторов элементов на странице товара."""

    input_quantity = (By.ID, "product_quantity")
    option_radio_buttons = (By.CSS_SELECTOR, "input[type='radio'][name^='option']")
    add_to_cart_button = (By.CSS_SELECTOR, "a.cart")
    cart_button = (By.CSS_SELECTOR, ".top.nobackground")
