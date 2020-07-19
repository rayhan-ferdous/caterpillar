from selenium import webdriver
import argparse
from urllib.parse import urlsplit

baseurl = None

#site source extractor
def get_page(parser):
    #default kwargs
    defaults = [
        'popup',
        'ui',
        'site',
        'end'
    ]

    for arg in defaults:
        parser.add_argument('--' + arg)
    user_args = parser.parse_args()

    chrome_options = webdriver.ChromeOptions()

    #None for no popup
    if user_args.popup is None:
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs",prefs)

    #None for no UI
    if user_args.ui is None:
        chrome_options.headless = True

    browser = webdriver.Chrome(chrome_options=chrome_options)

    global baseurl
    #None for google search page
    if user_args.site is None:
        browser.get('https://www.google.com/')
        site = 'https://www.google.com/'
    else:
        browser.get(user_args.site)
        site = user_args.site

    baseurl = "{0.scheme}://{0.netloc}/".format(urlsplit(site))
    print(baseurl)


    #None for scroll to end
    if user_args.end is None:
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    #get page source
    source = browser.page_source
    return source

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    source = get_page(parser)
    data = open('data/' + 'page.html', 'w')
    data.write(source)

    base = open('data/base.txt', 'w')
    base.write(baseurl)
