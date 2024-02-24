#!/usr/bin/env python

# # ====================
# # Usage example (from another file)
# import os
# from bing_image_creator import BingImageCreator

# prompt = "a giant fish in the cloud, realistic"
# cookie = os.environ["bing_cookie"]

# image_creator = BingImageCreator(prompt,
#                                  save_folder=".",
#                                  cookie_value=cookie)
# image_creator.run()

# # ====================
# # Usage example (from command line)
# # Single prompt example:
# bing_image_creator "a giant fish in the cloud, realistic" --cookie_value <your_cookie_value> --save_folder .

# # Multiple prompts example:
# bing_image_creator "prompt 1" "prompt 2" --cookie_value <your_cookie_value> --save_folder .

# # ====================
import os
import random
import string
import time
import requests

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from seleniumbase import Driver
from urllib.parse import urlparse, urlunparse

import piexif
from PIL import Image as PILImage


def print_colored_text(text, color, bold=True):
    color_mapping = {
        'black': '\033[30m',
        'blue': '\033[34m',
        'red': '\033[31m',
        'yellow': '\033[33m',
        'green': '\033[32m',
    }
    color_code = color_mapping.get(color.lower(), '')
    # Check if bold is requested
    if bold:
        color_code += '\033[1m'
    reset_code = '\033[0m'
    print(color_code + text + reset_code)


class BingImageCreator:
    def __init__(self, prompts, cookie_value=None, save_folder="images"):
        self.prompts = prompts if isinstance(prompts, list) else [prompts]
        self.cookie_value = cookie_value
        self.save_folder = save_folder
        self.current_prompt = ""
        # Setup driver
        self.driver = Driver(headless2=True, no_sandbox=True)

    def set_prompts(self, new_prompts):
        self.prompts = new_prompts if isinstance(new_prompts, list) else [new_prompts]

    def set_save_folder(self, new_save_folder):
        self.save_folder = new_save_folder

    def navigate_to_bing_create_page(self):
        self.driver.get("https://www.bing.com/images/create")

    def set_cookie(self):
        cookie = {"name": "_U", "value": self.cookie_value}
        self.driver.add_cookie(cookie)

    def enter_prompt(self, prompt):
        try:
            # Find the search box by its ID and enter a new prompt
            search_box = self.driver.find_element("id", "sb_form_q")
            search_box.clear()  # Clear existing text
            formatted_prompt = prompt.replace("\n", ",").strip()  # Replace newlines with commas and strip whitespace
            limited_prompt = formatted_prompt[:480]  # Limit prompt to 480 characters
            search_box.send_keys(limited_prompt)
            time.sleep(3)
            search_box.send_keys(Keys.RETURN)  # Press Enter
            time.sleep(1)  # Introduce a small delay (1 second) for stability
        except Exception as e:
            print(f"Error: {e}")

    def wait_for_loader(self):
        time.sleep(3)
        try:
            # Check if the prompt has been blocked (presence of class "block_icon")
            if self.driver.find_elements(By.CLASS_NAME, "block_icon"):
                # Print the error messages
                error_mt_elements = self.driver.find_elements(By.CLASS_NAME, "gil_err_mt")
                error_sbt_elements = self.driver.find_elements(By.CLASS_NAME, "gil_err_sbt1")
                if error_mt_elements:
                    print_colored_text("Error Message (gil_err_mt):", error_mt_elements[0].text, "red")
                if error_sbt_elements:
                    print_colored_text("Error Message (gil_err_sbt1):", error_sbt_elements[0].text, "red")
                raise Exception("Prompt is blocked")
            # Default wait time
            time_to_wait_seconds = 30  # Adjust the timeout as needed
            wait = WebDriverWait(self.driver, time_to_wait_seconds)
            # Wait until the element with ID "giloader" is present
            wait.until(EC.presence_of_element_located((By.ID, "giloader")))  # self.driver.find_element(By.ID, "giloader")
            # Check if boosts have run out (data-tb attribute of the element with id "reward_c" is 0)
            reward_element = self.driver.find_element(By.ID, "reward_c")
            data_tb_value = reward_element.get_attribute("data-tb")
            if data_tb_value == "0":
                # If data-tb is 0, get wait time from the text of the span with id "gi_rmtime" e.g. "1 min wait", "45 sec wait"
                time.sleep(1)
                # Find all elements with ID "gi_rmtime"
                wait_time_elements = self.driver.find_elements(By.ID, "gi_rmtime")
                if wait_time_elements:
                    # If at least one element is found, get wait time from the text of the first element
                    wait_time_text = wait_time_elements[0].text
                    # Split the wait time text into words
                    wait_time_words = wait_time_text.split()
                    # Extract the numerical value and unit from the wait time text
                    value = int(wait_time_words[0])
                    unit = wait_time_words[1]
                    # Convert minutes or seconds to seconds and add it to the wait time
                    if unit == "min":
                        time_to_wait_seconds += value * 60
                    elif unit == "sec":
                        time_to_wait_seconds += value
                else:
                    # If no elements are found, default to 1 minute wait
                    time_to_wait_seconds += 60
            # Wait until the style becomes "display: none;"
            wait = WebDriverWait(self.driver, time_to_wait_seconds)
            print("time_to_wait_seconds:", time_to_wait_seconds)
            wait.until(EC.invisibility_of_element_located((By.ID, "giloader")))
            time.sleep(3)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def remove_middle_text(text, max_length, indicator="___"):
        """
        Remove excess characters from the middle of the text if its length exceeds the specified maximum.
        """
        if len(text) > max_length:
            excess_chars = len(text) - max_length
            chars_to_remove_from_middle = (
                excess_chars + 1
            ) // 2  # Calculate the number of characters to remove from the middle
            start_index = (len(text) - max_length - chars_to_remove_from_middle) // 2
            end_index = start_index + max_length
            text = text[:start_index] + indicator + text[end_index:]
        return text

    @classmethod
    def sanitize_filename(self, filename):
        """
        Sanitize the given filename to make it compatible across different operating systems.
        """
        valid_chars = set("-_.() %s%s" % (string.ascii_letters, string.digits))
        sanitized_filename = "".join(c if c in valid_chars else "_" for c in filename)
        # Limit the filename length to 196 characters
        max_length = 196
        sanitized_filename = self.remove_middle_text(sanitized_filename, max_length)
        # Remove leading and trailing underscores
        sanitized_filename = sanitized_filename.strip("_")
        # Truncate the filename from the right to a maximum length of 196 characters
        sanitized_filename = (
            sanitized_filename[-max_length:]
            if len(sanitized_filename) > max_length
            else sanitized_filename
        )
        # If the filename is empty, generate a random string and append to "unnamed"
        if not sanitized_filename:
            random_string = "".join(
                random.choice(string.ascii_letters + string.digits) for _ in range(8)
            )
            sanitized_filename = f"unnamed_{random_string}"
        return sanitized_filename

    @staticmethod
    def generate_random_string():
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
        return random_string

    def download_images(self):
        try:
            # Select .mimg elements that are descendants of .img_cont
            image_elements = self.driver.find_elements(
                By.CSS_SELECTOR, ".img_cont .mimg"
            )
            image_urls = [element.get_attribute("src") for element in image_elements]
            # Create the save folder if it doesn't exist
            os.makedirs(self.save_folder, exist_ok=True)
            # Download images using alt values as sanitized file names
            random_string = self.generate_random_string()
            for url, element in zip(image_urls, image_elements):
                alt = element.get_attribute("alt")
                sanitized_alt = self.sanitize_filename(alt)
                # Remove unwanted parameters from the URL
                parsed_url = urlparse(url)
                new_url = urlunparse(
                    (
                        parsed_url.scheme,
                        parsed_url.netloc,
                        parsed_url.path,
                        parsed_url.params,
                        "",
                        "",
                    )
                )
                new_url += "?pid=ImgGn"
                # Retrieve the full image content
                response = requests.get(new_url)
                # Modify the file path to save the images to Google Drive
                file_path = os.path.join(self.save_folder, f"{sanitized_alt}_{random_string}.jpg")
                # Write the image content to the file
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print_colored_text(f'Image saved to "{file_path}".', 'blue')
                # Write self.prompt as description metadata of the image
                self.add_description_to_image(file_path, self.current_prompt)

            # Save self.prompt as a text file with the same name as the first sanitized_alt
            first_sanitized_alt = self.sanitize_filename(image_elements[0].get_attribute("alt"))
            prompt_file_path = os.path.join(self.save_folder, "prompts", f"{first_sanitized_alt}.txt")
            os.makedirs(os.path.dirname(prompt_file_path), exist_ok=True)
            with open(prompt_file_path, "w", encoding="utf-8") as prompt_file:
                prompt_file.write(self.current_prompt)
            print_colored_text(f'Prompt saved to "{prompt_file_path}".', 'green')
        except Exception as e:
            print(f"Error: {e}")

    def refresh_and_recheck(self, timeout=10):
        # 0. Check if the "Your images are on the way" popup exists
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.gi_nb.gi_nb_r.show_n')
            if elements:
                popup_text = elements[0].text.replace("\n", ". ")
                print_colored_text(f"Popup found: {popup_text}", "yellow")
                timeout = 150  # Change the timeout if the popup is found
        except:
            pass
        print("Refreshing and rechecking for the loader.")
        self.driver.refresh()
        time.sleep(3)
        # 1. Check if not class="girr_blocked"
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#girrcc > div:first-child.girr_blocked'))
            )
            print("The first child div does not have class 'girr_blocked'")
        except Exception as e:
            print(f"The first child div has class 'girr_blocked': {e}")
            return False
        # 2. Check if not imgcount="0"
        unwanted_element = '.girr_set.seled[data-imgcount="0"]'
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, unwanted_element))
            )
            print("The image count is greater than 0.")
            return True
        # Handle timeout by refreshing the page and trying again
        except TimeoutException:
            print("Timeout exceeded. Refreshing the page and trying again.")
            self.driver.refresh()
            try:
                # Wait again after refresh
                WebDriverWait(self.driver, timeout).until_not(
                    EC.presence_of_element_located((By.CSS_SELECTOR, unwanted_element))
                )
                print("The image count is greater than 0 after refresh.")
                return True
            # Handle timeout after refresh
            except TimeoutException:
                print("Timeout exceeded after refresh. The image count is still 0.")
                return False
        # Handle other exceptions
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def add_description_to_image(file_path, description):
        try:
            # Open the image
            img = PILImage.open(file_path)
            # Get the existing Exif data (if any)
            exif_dict = piexif.load(img.info["exif"])
            # Modify or add the 'Description' tag in the Exif data
            exif_dict['0th'][piexif.ImageIFD.ImageDescription] = description
            # Dump the modified Exif data back to bytes
            exif_bytes = piexif.dump(exif_dict)
            # Save the image with the updated Exif data
            img.save(file_path, exif=exif_bytes)
            # Close the image
            img.close()
        except Exception as e:
            print(f"An error occurred while saving description to image: {str(e)}")

    def run(self):
        try:
            for prompt in self.prompts:
                print()
                print_colored_text(prompt, "black")
                print("Save folder:", os.path.abspath(self.save_folder))
                self.navigate_to_bing_create_page()
                self.set_cookie()
                self.driver.refresh()
                self.current_prompt = prompt
                self.enter_prompt(self.current_prompt)
                try:
                    if self.wait_for_loader():
                        self.download_images()
                    else:
                        if self.refresh_and_recheck():
                            self.download_images()
                except Exception:
                    if self.refresh_and_recheck():
                        self.download_images()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.driver.quit()
