import os
from time import sleep, time
from random import uniform
import speech_recognition as sr

import requests
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from speech import get_audio_text


def wait_between(a, b):
    rand = uniform(a, b)
    sleep(rand)


def save_file(content, filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)


start = time()


def resolve(driver, filename="1.mp3"):
    main_win = driver.current_window_handle

    driver.switch_to.default_content()

    # *************  locate outer iframe  **************
    outer_iframe = WebDriverWait(driver, 0.5).until(
        ec.presence_of_element_located((By.ID, "main-iframe"))
    )

    # move the driver to the first iFrame
    driver.switch_to.frame(outer_iframe)

    # *************  locate inner iframe  **************
    try:
        inner_iframe = WebDriverWait(driver, 0.5).until(
            ec.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "iframe[name*='a-'][src*='https://www.google.com/recaptcha/api2/anchor?']",
                )
            )
        )
    except Exception:
        inner_iframe = WebDriverWait(driver, 0.5).until(
            ec.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "iframe[src*='https://www.google.com/recaptcha/api/fallback?']",
                )
            )
        )

    # move the driver to the inner iFrame
    driver.switch_to.frame(inner_iframe)

    fallback_error = driver.find_elements(By.CLASS_NAME, "fbc-main-message")
    if len(fallback_error) > 0 and "Please upgrade to a" in fallback_error[0].text:
        return False

    # *************  locate CheckBox  **************
    check_box = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, "recaptcha-anchor"))
    )

    # *************  click CheckBox  ***************
    wait_between(0.5, 0.7)
    # making click on captcha CheckBox
    check_box.click()

    # ***************** back to main window **************************************
    driver.switch_to.window(main_win)

    wait_between(2.0, 2.5)

    driver.switch_to.frame(outer_iframe)

    # *************  locate the popup's iframe  **************
    iframe_popup = WebDriverWait(driver, 0.5).until(
        ec.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "iframe[title*='recaptcha challenge'][src*='https://www.google.com/recaptcha/api2/bframe?']",
            )
        )
    )

    if not iframe_popup and check_box.get_attribute("aria-checked") == "true":
        return True

    try:
        driver.switch_to.frame(iframe_popup)

        wait_between(1, 2)

        # *************  locate the audio button  **************
        audio_btn = WebDriverWait(driver, 1).until(
            ec.presence_of_element_located((By.ID, "recaptcha-audio-button"))
        )
        # making click on captcha audio button
        audio_btn.click()

        try:
            wait_between(1, 2)

            while not is_bot_detected(driver):
                href = driver.find_element(By.ID, "audio-source").get_attribute("src")
                response = requests.get(href, stream=True)
                save_file(response, filename)
                response = get_audio_text(filename)

                input_btn = driver.find_element(By.ID, "audio-response")
                input_btn.send_keys(response)
                input_btn.send_keys(Keys.ENTER)
                sleep(2)

                error_msg = driver.find_elements_by_class_name(
                    "rc-audiochallenge-error-message"
                )[0]
                if (
                    error_msg.text == ""
                    or error_msg.value_of_css_property("display") == "none"
                ):
                    print("Success")
                    break

            return False
        except Exception as e:
            print(e)
            print("Caught. Need to change proxy now")
    except Exception as e:
        print(e)
        print("Button not found. This should not happen.")


def is_bot_detected(driver):
    bot_header_arr = driver.find_elements(By.CLASS_NAME, "rc-doscaptcha-header-text")
    try_again_header_arr = driver.find_elements(
        By.CLASS_NAME, "rc-audiochallenge-error-message"
    )

    if (
        len(bot_header_arr) == 0
        or bot_header_arr[0].text == ""
        or bot_header_arr[0].value_of_css_property("display") == "none"
    ) and (
        len(try_again_header_arr) == 0
        or try_again_header_arr[0].text == ""
        or try_again_header_arr[0].value_of_css_property("display") == "none"
    ):
        return False

    return True
