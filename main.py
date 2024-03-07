import data
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    # Localizadores
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # Métodos
    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

class TaxiComfort:
    #Localizadores
    personal_button = (By.XPATH, "//div[@class='mode' and text()='Personal']")
    taxi_button = (By.XPATH, "//div[@class='types-container']//div[contains(@class, 'type') and .//img[contains(@src, 'taxi')]]")
    pedir_un_taxi_button = (By.XPATH, "//button[@class='button round' and text()='Pedir un taxi']")
    comfort_button = (By.XPATH, "//div[@class='tariff-cards']//div[contains(@class, 'tcard')]//div[@class='tcard-title' and text()='Comfort']")

    #Métodos
    def __init__(self, driver):
        self.driver = driver

    def wait_for_clickeable_personal_button(self):
        WebDriverWait(self.driver, 4).until(expected_conditions.element_to_be_clickable(self.personal_button))

    def click_personal_button(self):
        self.driver.find_element(*self.personal_button).click()

    def click_taxi_button(self):
        self.driver.find_element(*self.taxi_button).click()

    def click_pedir_taxi_button(self):
        self.driver.find_element(*self.pedir_un_taxi_button).click()

    def click_comfort_button(self):
        self.driver.find_element(*self.comfort_button).click()

    def select_comfort_tariff(self):
        self.wait_for_clickeable_personal_button()
        self.click_personal_button()
        self.click_taxi_button()
        # time.sleep(1)
        self.click_pedir_taxi_button()
        # time.sleep(1)
        self.click_comfort_button()
        # time.sleep(1)

class PhoneNumber:
    #Localizadores
    phone_number_button = (By.XPATH, "//div[@class='np-text']")
    phone_number_field = (By.XPATH, "//div[@class='input-container']//input[@id='phone']")
    siguiente_button = (By.XPATH, "//div[@class='buttons']//button[@class='button full']")
    sms_code = (By.XPATH, "//div[@class='input-container']//input[@id='code']")
    confirm_button = (By.XPATH, "//div[@class='buttons']//button[@class='button full' and text()='Confirmar']")

    #Métodos
    def __init__(self, driver):
        self.driver = driver

    def wait_for_phone_number_button(self):
        WebDriverWait(self.driver, 4).until(expected_conditions.element_to_be_clickable(self.phone_number_button))

    def click_phone_number_button(self):
        self.driver.find_element(*self.phone_number_button).click()

    def fill_phone_number(self, phone_number):
        self.driver.find_element(*self.phone_number_field).send_keys(phone_number)

    def click_siguiente_button(self):
        self.driver.find_element(*self.siguiente_button).click()

    def set_sms_code(self, sms_code):
        self.driver.find_element(*self.sms_code).send_keys(sms_code)

    def click_confirm_button(self):
        self.driver.find_element(*self.confirm_button).click()

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number_button).text.strip()

    def set_phone_number_and_confirm(self):
        self.wait_for_phone_number_button()
        self.click_phone_number_button()
        # time.sleep(1)
        phone_number = data.phone_number
        self.fill_phone_number(phone_number)
        # time.sleep(1)
        self.click_siguiente_button()
        # time.sleep(1)
        self.set_sms_code(retrieve_phone_code(self.driver))
        # time.sleep(1)
        self.click_confirm_button()
        time.sleep(1)

class CreditCard:
    #Localizadores
    pay_method_button = (By.XPATH, "//div[@class='pp-button filled']")
    agregar_tajeta_button = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")
    cc_number_field = (By.XPATH, "//div[@class='card-number-input']//input[@id='number']")
    cc_code_field = (By.XPATH, "//div[@class='card-code-input']//input[@id='code']")
    cc_agregar_button = (By.XPATH, "//button[@class='button full' and text()='Agregar']")
    cc_random_element = (By.XPATH, "//div[@class='head' and text()='Agregar tarjeta']")
    cc_close_window = (By.XPATH, "//div[@class='payment-picker open']//div[@class='modal']//div[@class='section active']//button[@class='close-button section-close']")

    #Métodos
    def __init__(self, driver):
        self.driver = driver
        self.cc_number = None
        self.cc_code = None

    def click_pay_method_button(self):
        self.driver.find_element(*self.pay_method_button).click()

    def click_agregar_tarjeta_button(self):
        self.driver.find_element(*self.agregar_tajeta_button).click()

    def set_credit_card_number(self, cc_number):
        self.driver.find_element(*self.cc_number_field).send_keys(cc_number)
        self.cc_number = cc_number

    def set_credit_card_code(self, cc_code):
        self.driver.find_element(*self.cc_code_field).send_keys(cc_code)
        self.cc_code = cc_code

    def wait_agregar_button_clickeable(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(self.cc_agregar_button))

    def click_random_element(self):
        self.driver.find_element(*self.cc_random_element).click()

    def click_agregar_button(self):
        self.driver.find_element(*self.cc_agregar_button).click()

    def wait_close_pay_method_button(self):
        WebDriverWait(self.driver,10).until(expected_conditions.element_to_be_clickable(self.cc_close_window))

    def close_pay_method_window(self):
        self.driver.find_element(*self.cc_close_window).click()

    def get_cc_number(self):
        return self.cc_number

    def get_cc_code(self):
        return self.cc_code

    def step_credit_card(self):
        self.click_pay_method_button()
        # time.sleep(1)
        self.click_agregar_tarjeta_button()
        # time.sleep(1)
        cc_number = data.card_number
        self.set_credit_card_number(cc_number)
        # time.sleep(1)
        cc_code = data.card_code
        self.set_credit_card_code(cc_code)
        # time.sleep(1)
        self.click_random_element()
        self.wait_agregar_button_clickeable()
        # time.sleep(1)
        self.click_agregar_button()
        # time.sleep(1)
        self.wait_close_pay_method_button()
        self.close_pay_method_window()
        # time.sleep(1)

class MessageDriver:
    #Localizadores
    message_button = (By.XPATH, "//input[@id='comment']")

    #Métodos
    def __init__(self, driver):
        self.driver = driver

    def set_message_for_the_driver(self, message):
        self.driver.find_element(*self.message_button).send_keys(message)

    def get_message_for_the_driver(self):
        return self.driver.find_element(*self.message_button).get_property('value')

class BlanketAndTissues:
    # Localizadores
    blanket_and_tissues_button = (By.XPATH, "//div[@class='r-sw-container']//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div[@class='r-sw']//div[@class='switch']")

    # Métodos
    def __init__(self,driver):
        self.driver = driver

    def click_blanket_and_tissues_switch(self):
        self.driver.find_element(*self.blanket_and_tissues_button).click()

class IceCream:
    # Localizadores
    ice_cream_counter_plus_button = (By.XPATH, "//div[@class='r-counter-label' and text()='Helado']/following-sibling::div[@class='r-counter']//div[@class='counter-plus']")
    #Métodos
    def __init__(self, driver):
        self.driver = driver

    #Múltiples clicks
    def set_number_of_ice_creams(self,value):
        for i in range(value):
            self.driver.find_element(*self.ice_cream_counter_plus_button).click()

class SearchTaxi:
    #Localizadores
    pedir_un_taxi_button = (By.XPATH, "//div[@class='smart-button-wrapper']//button[@class='smart-button']")


    #Métodos
    def __init__(self,driver):
        self.driver = driver

    def click_pedir_un_taxi_button(self):
        self.driver.find_element(*self.pedir_un_taxi_button).click()

class WaitDriverInfo:
    #Localizadores
    timer_taxi = (By.XPATH, "//div[@class='order-header-time']")

    #Métodos
    def __init__(self, driver):
        self.driver = driver

    def wait_for_driver_information(self):
        # WebDriverWait(self.driver, 60).until(expected_conditions.invisibility_of_element_located(*self.timer_taxi))
        WebDriverWait(self.driver, 60).until(expected_conditions.invisibility_of_element_located(self.timer_taxi))


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)              # Abre la página de Urban.Routes
        time.sleep(2)
        routes_page = UrbanRoutesPage(self.driver)          # Crea un objeto de página para la página de incio
        address_from = data.address_from                    # Toma la dirección "from" de la pestaña "data"
        address_to = data.address_to                        # Toma la dirección "to" de la pestaña "data"
        routes_page.set_route(address_from, address_to)     # Paso de la combinación de métodos
        assert routes_page.get_from() == address_from       # Corrobora que la dirección en "from" sea la misma a la de adress_from
        assert routes_page.get_to() == address_to           # Corrobora que la dirección en "to" sea la misma a la de adress_to

    def test_comfort_tariff(self):
        ride_types  = TaxiComfort(self.driver)
        ride_types.select_comfort_tariff()

    def test_fill_phone_number(self):
        phone_field = PhoneNumber(self.driver)
        phone_field.set_phone_number_and_confirm()
        entered_phone_number = phone_field.get_phone_number()
        expected_phone_number = data.phone_number
        assert entered_phone_number == expected_phone_number, f"El número ingresado {entered_phone_number} no coincide con el esperado {expected_phone_number}"

    def test_set_credit_card(self):
        cc_field = CreditCard(self.driver)   #cc: credit card
        cc_field.step_credit_card()
        entered_cc_number = cc_field.get_cc_number()
        expected_cc_number = data.card_number
        assert entered_cc_number == expected_cc_number, f"El número de tarjeta de credito ingresado: {entered_cc_number} no coincide con el número de tarjeta de credito esperado: {expected_cc_number}"
        entered_cc_code = cc_field.get_cc_code()
        expected_cc_code = data.card_code
        assert entered_cc_code == expected_cc_code, f"El código de tarjeta de credito ingresado: {entered_cc_code} no coincide con el código de tarjeta de credito esperado: {expected_cc_code}"

    def test_set_message_for_the_driver(self):
        message_field = MessageDriver(self.driver)
        message = data.message_for_driver
        message_field.set_message_for_the_driver(message)
        entered_message = message_field.get_message_for_the_driver()
        expected_message = data.message_for_driver
        assert entered_message == expected_message, f"El mensage ingresado: {entered_message}, no coincide con el mensaje esperado: {expected_message}"
        time.sleep(1)

    def test_ask_for_tissues_and_blancket(self):
        blanket_tissues_field = BlanketAndTissues(self.driver)
        blanket_tissues_field.click_blanket_and_tissues_switch()
        time.sleep(1)

    def test_set_two_ice_creams(self):
        ice_cream_field = IceCream(self.driver)
        ice_cream_field.set_number_of_ice_creams(2)   #El valor aquí es el número de clicks en el botón "+" del contador de "Helado"
        time.sleep(1)

    def test_pedir_taxi(self):
        pedir_taxi_field = SearchTaxi(self.driver)
        pedir_taxi_field.click_pedir_un_taxi_button()
        time.sleep(3)

    def test_wait_taxi_timer(self):
        taxi_timer_field = WaitDriverInfo(self.driver)
        taxi_timer_field.wait_for_driver_information()
        time.sleep(3)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
