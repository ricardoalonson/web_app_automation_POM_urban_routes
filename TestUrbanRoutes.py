import main
import time
import data

from selenium import webdriver

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
        cls.routes_page = main.UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)              # Abre la página de Urban.Routes
        time.sleep(2)
        routes_page = main.UrbanRoutesPage(self.driver)          # Crea un objeto de página para la página de incio
        address_from = data.address_from                    # Toma la dirección "from" de la pestaña "data"
        address_to = data.address_to                        # Toma la dirección "to" de la pestaña "data"
        routes_page.set_route(address_from, address_to)     # Paso de la combinación de métodos
        assert routes_page.get_from() == address_from       # Corrobora que la dirección en "from" sea la misma a la de adress_from
        assert routes_page.get_to() == address_to           # Corrobora que la dirección en "to" sea la misma a la de adress_to

    def test_comfort_tariff(self):
        ride_types  = main.TaxiComfort(self.driver)
        ride_types.select_comfort_tariff()
        expected_tariff = "Comfort"
        actual_tariff = ride_types.get_tariff()
        assert expected_tariff == actual_tariff, f"Las tarifa esperada {expected_tariff} no coincide con la tarifa actual {actual_tariff}"

    def test_fill_phone_number(self):
        phone_field = main.PhoneNumber(self.driver)
        phone_field.set_phone_number_and_confirm()
        entered_phone_number = phone_field.get_phone_number()
        expected_phone_number = data.phone_number
        assert entered_phone_number == expected_phone_number, f"El número ingresado {entered_phone_number} no coincide con el esperado {expected_phone_number}"

    def test_set_credit_card(self):
        cc_field = main.CreditCard(self.driver)   #cc: credit card
        cc_field.step_credit_card()
        entered_cc_number = cc_field.get_cc_number()
        expected_cc_number = data.card_number
        assert entered_cc_number == expected_cc_number, f"El número de tarjeta de credito ingresado: {entered_cc_number} no coincide con el número de tarjeta de credito esperado: {expected_cc_number}"
        entered_cc_code = cc_field.get_cc_code()
        expected_cc_code = data.card_code
        assert entered_cc_code == expected_cc_code, f"El código de tarjeta de credito ingresado: {entered_cc_code} no coincide con el código de tarjeta de credito esperado: {expected_cc_code}"

    def test_set_message_for_the_driver(self):
        message_field = main.MessageDriver(self.driver)
        message = data.message_for_driver
        message_field.set_message_for_the_driver(message)
        entered_message = message_field.get_message_for_the_driver()
        expected_message = data.message_for_driver
        assert entered_message == expected_message, f"El mensage ingresado: {entered_message}, no coincide con el mensaje esperado: {expected_message}"
        time.sleep(1)

    def test_ask_for_tissues_and_blancket(self):
        blanket_tissues_field = main.BlanketAndTissues(self.driver)
        blanket_tissues_field.click_blanket_and_tissues_switch()
        expected_checkbox_text = "Manta y pañuelos"
        actual_checkbox_text = blanket_tissues_field.get_checkbox_text()
        assert expected_checkbox_text == actual_checkbox_text, f"El nombre del checkbox esperado {expected_checkbox_text} no coincide con el actual {actual_checkbox_text}"
        time.sleep(1)

    def test_set_two_ice_creams(self):
        ice_cream_field = main.IceCream(self.driver)
        ice_cream_field.set_number_of_ice_creams(2)   #El valor aquí es el número de clicks en el botón "+" del contador de "Helado"
        expected_number_of_ice_creams = "2"
        actual_number_of_ice_creams = ice_cream_field.get_number_of_ice_creams()
        assert expected_number_of_ice_creams == actual_number_of_ice_creams, f"El número de helados esperados: {expected_number_of_ice_creams} no coincide con el número de helados actuales: {actual_number_of_ice_creams}"
        time.sleep(1)

    def test_pedir_taxi(self):
        pedir_taxi_field = main.SearchTaxi(self.driver)
        pedir_taxi_field.click_pedir_un_taxi_button()
        expected_text_button = "Pedir un taxi"
        actual_text_button = pedir_taxi_field.get_buscar_un_taxi_text_button()
        assert expected_text_button in actual_text_button, f"El texto esperado: {expected_text_button}; no coincide con el actual: {actual_text_button}"
        time.sleep(1)

    def test_wait_taxi_timer(self):
        taxi_timer_field = main.WaitDriverInfo(self.driver)
        expected_header = "Buscar automóvil"
        actual_header = taxi_timer_field.get_waiting_window_header()
        taxi_timer_field.wait_for_driver_information()
        assert expected_header == actual_header, f"El header actual {actual_header}, no coincide con el esperado {expected_header}"
        time.sleep(1)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()