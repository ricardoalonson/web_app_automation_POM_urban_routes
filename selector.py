from selenium.webdriver.common.by import By

# Está página conserva todos los selectores utilizados en las clases de main.py

# class UrbanRoutesPage:
from_field = (By.ID, 'from')
to_field = (By.ID, 'to')

# class TaxiComfort:
personal_button = (By.XPATH, "//div[@class='mode' and text()='Personal']")
taxi_button = (By.XPATH, "//div[@class='types-container']//div[contains(@class, 'type') and .//img[contains(@src, 'taxi')]]")
pedir_un_taxi_button = (By.CSS_SELECTOR, "button.button.round")
comfort_button = (By.XPATH, "//div[@class='tariff-cards']//div[contains(@class, 'tcard')]//div[@class='tcard-title' and text()='Comfort']")

# class PhoneNumber:
phone_number_button = (By.CLASS_NAME, "np-button")
phone_number_field = (By.ID, "phone")
siguiente_button = (By.XPATH, "//div[@class='buttons']//button[@class='button full']")
sms_code = (By.ID, "code")
confirm_button = (By.XPATH, "//div[@class='buttons']//button[@class='button full' and text()='Confirmar']")

# class CreditCard:
pay_method_button = (By.XPATH, "//div[@class='pp-button filled']")
agregar_tajeta_button = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")
cc_number_field = (By.XPATH, "//div[@class='card-number-input']//input[@id='number']")
cc_code_field = (By.XPATH, "//div[@class='card-code-input']//input[@id='code']")
cc_agregar_button = (By.XPATH, "//button[@class='button full' and text()='Agregar']")
cc_random_element = (By.XPATH, "//div[@class='head' and text()='Agregar tarjeta']")
cc_close_window = (By.XPATH, "//div[@class='payment-picker open']//div[@class='modal']//div[@class='section active']//button[@class='close-button section-close']")

# class MessageDriver:
message_button = (By.XPATH, "//input[@id='comment']")

# class BlanketAndTissues:
blanket_and_tissues_button = (By.XPATH, "//div[@class='r-sw-container']//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div[@class='r-sw']")
blanket_and_tissues_button_text = (By.XPATH, "//div[@class='r-sw-container']//div[@class='r-sw-label' and text()='Manta y pañuelos']")

# class IceCream:
ice_cream_counter_plus_button = (By.XPATH, "//div[@class='r-counter-label' and text()='Helado']/following-sibling::div[@class='r-counter']//div[@class='counter-plus']")
ice_cream_counter_value = (By.XPATH, "//div[@class='r-counter-label' and text()='Helado']/following-sibling::div[@class='r-counter']//div[@class='counter-value']")

# class SearchTaxi:
pedir_un_taxi_final_button = (By.XPATH, "//div[@class='smart-button-wrapper']//button[@class='smart-button']")

# class WaitDriverInfo:
timer_taxi = (By.XPATH, "//div[@class='order-header-time']")
pedir_un_taxi_header = (By.CLASS_NAME, "order-header-title")