import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Setup
driver = webdriver.Chrome()
file_path = os.path.abspath("assets/checkout.html")
driver.get(f"file:///{file_path}")

# Smart Cart Logic
test_case_json = {"test_id": "DISCOUNT_006", "description": "Apply discount code with cart total greater than $200", "expected_result": "15% discount applied to the total cart value and Express Shipping is free", "grounded_in": "Product Specifications & Business Rules: Discount Codes and Shipping Rules"}
if "empty" not in test_case_json["description"]:
    if test_case_json["test_id"] == "DISCOUNT_006":
        driver.find_element(By.ID, "btn-add-headphones").click()
        driver.find_element(By.ID, "btn-add-keyboard").click()
        driver.find_element(By.ID, "btn-add-keyboard").click()
    time.sleep(1)

# Capture & Action
price_before = float(driver.find_element(By.ID, "total-price").text)
driver.find_element(By.ID, "discount-code").send_keys("SAVE15")
driver.find_element(By.ID, "apply-coupon-btn").click()
time.sleep(1)
price_after = float(driver.find_element(By.ID, "total-price").text)

# Assertion
expected = price_before * 0.85
assert abs(price_after - expected) < 0.01

# Finish
time.sleep(10)
driver.quit()