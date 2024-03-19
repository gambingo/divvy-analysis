"""
Download flat files from Divvy and prepare them to be uploaded to the database
"""
import os
import json
import shutil
from zipfile import ZipFile
from collections import defaultdict

import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.directories import DATA_DIR


### Download

def download_single_file(datasets, filename):
    if not datasets[filename]["in database"]:
        # Download
        source_url = datasets[filename]["source"]
        temp_dir = DATA_DIR / "temp"
        temp_dir.mkdir(exist_ok=True)
        zipped_filepath = temp_dir / filename
        download_zip_file(source_url, zipped_filepath)

        # Open 
        unzipped_filename = unzip_file(zipped_filepath, temp_dir)
        unzipped_filepath = temp_dir / unzipped_filename
        df = pd.read_csv(unzipped_filepath)

        # Remove flat files
        shutil.rmtree(temp_dir)

        return df       


def download_zip_file(url, filepath, chunk_size=128):
    if not os.path.exists(filepath):
        response = requests.get(url, stream=True)
        with open(filepath, "wb") as fp:
            for chunk in response.iter_content(chunk_size=chunk_size):
                fp.write(chunk)


def unzip_file(filepath, save_dir):
    with ZipFile(filepath, "r") as zip_ref:
        zip_ref.extractall(save_dir)
        
    # Look for a file with the same basename but not a .zip extension
    folder = os.path.dirname(filepath)
    filenames = [fn for fn in os.listdir(folder) if fn.split(".")[-1] == "csv"]
    return filenames[0]


### Web Scraping

def update_list_of_available_datasets():
    datasets = load_record_keeping_file()
    datasets = scrape_divvy_datasets_listing(datasets)
    save_record_keeping_file(datasets)


def load_record_keeping_file():
    """
    Loads the JSON file we are using to keep track of which flat files are
    available and have been uploaded to our database.
    """
    filepath = DATA_DIR / "datasets.json"
    if not os.path.exists(filepath):
        datasets = defaultdict(dict)
    else:
        with open(filepath, 'r') as fp:
            datasets = json.load(fp)
    return datasets


def record_flat_file_upload(datasets, filename):
    datasets[filename]["in database"] = True
    save_record_keeping_file(datasets)
    

def save_record_keeping_file(datasets):
    filepath = DATA_DIR / "datasets.json"
    with open(filepath, 'w') as fp:
        json.dump(datasets, fp)


def scrape_divvy_datasets_listing(datasets):
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