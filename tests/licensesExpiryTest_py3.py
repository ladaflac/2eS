# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import unittest
from datetime import datetime, date


class SnipeitappLicensesExpiryTestPy2V2(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", desired_capabilities={"browserName": "chrome"})
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_snipeitapp_licenses_expiry_test_py2_v2(self):
        driver = self.driver

        # login
        driver.get("https://demo.snipeitapp.com/login")
        driver.find_element_by_name("username").click()
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("admin")
        driver.find_element_by_name("password").click()
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("password")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='password'])[1]/following::button[1]").click()

        # check the dates
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Bulk Audit'])[1]/following::i[1]").click()
        WebDriverWait(driver, 30).until(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "fixed-table-loading")))
        rows = driver.find_elements(By.XPATH, ".//table[@id='licensesTable']/tbody[1]/tr")
        row = 1
        today = date.today()
        while row < len(rows):
            expiration_date_source = driver.find_element_by_xpath("//table[@id='licensesTable']/tbody[1]/tr[" + str(row) + "]/td[3]").text
            if expiration_date_source == '':
                print("Expiration date in row %d is empty" % row)
            else:
                expiration_date = datetime.strptime(expiration_date_source[4:16], '%b %d, %Y').date()
                assert expiration_date >= today, "Expiration date '%s' should not be in the past" % expiration_date
                print("Expiration date " + str(expiration_date) + " in row %d is valid" % row)
            row += 1

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
