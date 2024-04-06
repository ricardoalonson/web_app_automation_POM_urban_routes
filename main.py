import data
import time
import selector

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

    # Métodos
    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*selector.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*selector.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*selector.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*selector.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)
        time.sleep(1)

class TaxiComfort:

    #Métodos
    def __init__(self, driver):
        self.driver = driver

    def wait_for_clickeable_personal_button(self):
        WebDriverWait(self.driver, 4).until(expected_conditions.element_to_be_clickable(selector.personal_button))

    def click_personal_button(self):
        self.driver.find_element(*selector.personal_button).click()

    def click_taxi_button(self):
        self.driver.find_element(*selector.taxi_button).click()

    def click_pedir_taxi_button(self):
        self.driver.find_element(*selector.pedir_un_taxi_button).click()

    def click_comfort_button(self):
        self.driver.find_element(*selector.comfort_button).click()

    def get_tariff(self):
        return self.driver.find_element(*selector.comfort_button).text.strip()

    def select_comfort_tariff(self):
        self.wait_for_clickeable_personal_button()
        self.click_personal_button()
        time.sleep(1)
        self.click_taxi_button()
        self.click_pedir_taxi_button()
        time.sleep(1)
        self.click_comfort_button()
        time.sleep(1)

class PhoneNumber:

    #Métodos
    def __init__(self, driver):
        self.driver = driver

    def wait_for_phone_number_button(self):
        WebDriverWait(self.driver, 4).until(expected_conditions.element_to_be_clickable(selector.phone_number_button))

    def click_phone_number_button(self):
        self.driver.find_element(*selector.phone_number_button).click()

    def fill_phone_number(self, phone_number):
        self.driver.find_element(*selector.phone_number_field).send_keys(phone_number)

    def click_siguiente_button(self):
        self.driver.find_element(*selector.siguiente_button).click()

    def set_sms_code(self, sms_code):
        self.driver.find_element(*selector.sms_code).send_keys(sms_code)

    def click_confirm_button(self):
        self.driver.find_element(*selector.confirm_button).click()

    def get_phone_number(self):
        return self.driver.find_element(*selector.phone_number_button).text.strip()

    def set_phone_number_and_confirm(self):
        self.wait_for_phone_number_button()
        self.click_phone_number_button()
        time.sleep(1)
        phone_number = data.phone_number
        self.fill_phone_number(phone_number)
        time.sleep(1)
        self.click_siguiente_button()
        self.set_sms_code(retrieve_phone_code(self.driver))
        time.sleep(1)
        self.click_confirm_button()
        time.sleep(1)

class CreditCard:

    #Métodos
    def __init__(self, driver):
        self.driver = driver
        self.cc_number = None
        self.cc_code = None

    def click_pay_method_button(self):
        self.driver.find_element(*selector.pay_method_button).click()

    def click_agregar_tarjeta_button(self):
        self.driver.find_element(*selector.agregar_tajeta_button).click()

    def set_credit_card_number(self, cc_number):
        self.driver.find_element(*selector.cc_number_field).send_keys(cc_number)
        self.cc_number = cc_number

    def set_credit_card_code(self, cc_code):
        self.driver.find_element(*selector.cc_code_field).send_keys(cc_code)
        self.cc_code = cc_code

    def wait_agregar_button_clickeable(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(selector.cc_agregar_button))

    def click_random_element(self):
        self.driver.find_element(*selector.cc_random_element).click()

    def click_agregar_button(self):
        self.driver.find_element(*selector.cc_agregar_button).click()

    def wait_close_pay_method_button(self):
        WebDriverWait(self.driver,10).until(expected_conditions.element_to_be_clickable(selector.cc_close_window))

    def close_pay_method_window(self):
        self.driver.find_element(*selector.cc_close_window).click()

    def get_cc_number(self):
        return self.cc_number

    def get_cc_code(self):
        return self.cc_code

    def step_credit_card(self):
        self.click_pay_method_button()
        time.sleep(1)
        self.click_agregar_tarjeta_button()
        time.sleep(1)
        cc_number = data.card_number
        self.set_credit_card_number(cc_number)
        time.sleep(1)
        cc_code = data.card_code
        self.set_credit_card_code(cc_code)
        self.click_random_element()
        self.wait_agregar_button_clickeable()
        time.sleep(1)
        self.click_agregar_button()
        time.sleep(1)
        self.wait_close_pay_method_button()
        self.close_pay_method_window()
        time.sleep(1)

class MessageDriver:

    #Métodos
    def __init__(self, driver):
        self.driver = driver

    def set_message_for_the_driver(self, message):
        self.driver.find_element(*selector.message_button).send_keys(message)

    def get_message_for_the_driver(self):
        return self.driver.find_element(*selector.message_button).get_property('value')

class BlanketAndTissues:

    # Métodos
    def __init__(self,driver):
        self.driver = driver

    def click_blanket_and_tissues_switch(self):
        self.driver.find_element(*selector.blanket_and_tissues_button).click()

    def get_checkbox_text(self):
        return self.driver.find_element(*selector.blanket_and_tissues_button_text).text.strip()

class IceCream:

    #Métodos
    def __init__(self, driver):
        self.driver = driver

    #Múltiples clicks
    def set_number_of_ice_creams(self,value):
        for i in range(value):
            self.driver.find_element(*selector.ice_cream_counter_plus_button).click()

    def get_number_of_ice_creams(self):
        return self.driver.find_element(*selector.ice_cream_counter_value).text.strip()

class SearchTaxi:

    #Métodos
    def __init__(self,driver):
        self.driver = driver

    def click_pedir_un_taxi_button(self):
        self.driver.find_element(*selector.pedir_un_taxi_final_button).click()

    def get_buscar_un_taxi_text_button(self):
        return self.driver.find_element(*selector.pedir_un_taxi_final_button).text.strip()

class WaitDriverInfo:

    #Métodos
    def __init__(self, driver):
        self.driver = driver

    def wait_for_driver_information(self):
        WebDriverWait(self.driver, 60).until(expected_conditions.invisibility_of_element_located(selector.timer_taxi))

    def get_waiting_window_header(self):
        return self.driver.find_element(*selector.pedir_un_taxi_header).text.strip()
