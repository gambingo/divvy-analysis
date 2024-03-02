"""
Download flat files from Divvy and prepare them to be uploaded to the database
"""
import os
import json
from collections import defaultdict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.directories import DATA_DIR



def update_list_of_available_datasets():
    filepath = DATA_DIR / "datasets.json"
    if not os.path.exists(filepath):
        datasets = defaultdict(dict)

    else:
        with open(filepath, 'r') as fp:
            datasets = json.load(fp)

    datasets = scrape_divvy_flat_file_listing(datasets)

    with open(filepath, 'w') as fp:
        json.dump(datasets, fp)


def scrape_divvy_flat_file_listing(datasets):
    # Download Webpage
    url = "https://divvy-tripdata.s3.amazonaws.com/index.html"
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        # Wait up to 10 seconds before throwing a TimeoutException
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
        )
        
        links = driver.find_elements(By.TAG_NAME, 'a')
        for link in links:
            href = link.get_attribute('href')
            if href is not None:
                if link.text.split(".")[-1].lower() == "zip":
                    if link.text not in datasets:
                        datasets[link.text]["source"] = href
                        datasets[link.text]["in database"] = False              
    finally:
        driver.quit()

    return datasets


if __name__ == "__main__":
    get_list_of_available_files()