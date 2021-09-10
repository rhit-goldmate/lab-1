import os
from io import BytesIO
import pytest
from selenium import webdriver
from app import create_app
from flask import url_for
from PIL import Image, ImageChops

# Fixes https://github.com/pytest-dev/pytest-flask/issues/104
import multiprocessing
multiprocessing.set_start_method("fork")

@pytest.fixture(scope="session")
def app():
    app = create_app({'TESTING': True})
    app.testing = True
    app.config.update(
        LIVESERVER_PORT=8910
    )
    yield app

@pytest.fixture
def client(app):
    with app.app_context():
        with app.test_client() as client:
            yield client

@pytest.fixture(scope="session")
def chromedriver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_homepage_loads_in_traditional_test(client):
    homepage = client.get('/')
    assert b"Hello, World!" in homepage.data

def test_homepage_loads_in_selenium_test(client, chromedriver, live_server):
    chromedriver.get('http://localhost:8910')
    assert "Hello, World!" in chromedriver.page_source

def test_uploading_a_jpg_does_not_cause_errors(client, chromedriver, live_server):
    test_image_filename = 'postive_possum_shirt.jpeg'
    upload_image_and_check_for_errors(chromedriver, test_image_filename)

def test_uploading_a_png_with_alpha_transparency_does_not_cause_errors(client, chromedriver, live_server):
    test_image_filename = 'rose_hulman_website.png'
    upload_image_and_check_for_errors(chromedriver, test_image_filename)

def test_images_are_actually_transformed(client):
    # Ideally we would round out the selenium-based tests with something like the following:
    #   chrome_image = Image.open(chromedriver.page_source)
    #   source_image = Image.open(os.path.join(os.getcwd(), 'tests', 'files', test_image_filename))
    #   check_that_images_are_different(chrome_image, source_image)
    # However, that has proven difficult with selenium-python, so I'm doing it through
    # pytest-flask in this testcase instead.
    test_image_filename = 'rose_hulman_website.png'
    test_image_full_path = os.path.join(os.getcwd(), 'tests', 'files', test_image_filename)
    with open(test_image_full_path, 'rb') as source_image:
        image_contents = BytesIO(source_image.read())
    data = dict(
        image=(image_contents, test_image_filename),
    )
    response = client.post(url_for("spp.process"), data=data, follow_redirects=True, content_type='multipart/form-data')
    allegedly_transformed_image = Image.open(BytesIO(response.data))
    source_image = Image.open(test_image_full_path)
    check_that_images_are_different(allegedly_transformed_image, source_image)

def test_uploading_no_image_redirects_back_with_message(chromedriver):
    chromedriver.get('http://localhost:8910')
    click_link(chromedriver, 'Simple Photo Processor')
    assert "Simple Photo Processor Upload Page" in chromedriver.page_source
    click_button(chromedriver, 'Upload')
    assert "Error" not in chromedriver.page_source
    assert "Select an image file to upload" in chromedriver.page_source

@pytest.mark.skip(reason="Implement this for extra credit :)")
def test_non_images_are_not_allowed(chromedriver):
    test_non_image_filename = 'not_actually_an_image.jpg'
    upload_image_and_check_for_errors(chromedriver, test_non_image_filename)
    assert "Select an image file to upload" in chromedriver.page_source

## Helpers Specific To These Tests:

def check_that_images_are_different(chrome_image, source_image):
    diff = ImageChops.difference(chrome_image.convert('RGB'), source_image.convert('RGB'))

    if diff.getbbox():
        pass # images have some differences
    else:
        pytest.fail("there were no differences detected between the source image and the output image")

def upload_image_and_check_for_errors(chromedriver, test_image_filename):
    chromedriver.get('http://localhost:8910')
    click_link(chromedriver, 'Simple Photo Processor')
    assert "Simple Photo Processor Upload Page" in chromedriver.page_source
    attach_file(chromedriver, 'Select an image to upload', test_image_filename)
    click_button(chromedriver, 'Upload')
    assert "Error" not in chromedriver.page_source

## Generic Helpers:
## (Normally these would be pulled out into a helper file, but I left them here for easier reference)
## (These are also things that are built into more complex testing tools like seleniumbase, which we
##  will be using in future labs)

def attach_file(chromedriver, file_upload_label, image_name):
    full_path = os.path.join(os.getcwd(), 'tests', 'files', image_name)
    id_from_label = chromedriver.find_element_by_xpath(f"//label[contains(text(), '{file_upload_label}')]").get_attribute("for")
    file_upload_field = chromedriver.find_element_by_id(id_from_label)
    file_upload_field.send_keys(full_path)

def click_button(chromedriver, button_text):
    button = chromedriver.find_element_by_xpath(f"//input[@type=\"submit\"][@value=\"{button_text}\"]")
    button.click()

def click_link(chromedriver, link_text):
    link = chromedriver.find_element_by_link_text(link_text)
    link.click()