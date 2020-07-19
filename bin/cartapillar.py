""""
python3 cartapillar.py site=www.prothomalo.com
"""

import argparse
import browser
import scrap

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    source, site = browser.get_page(parser)
    scrap.summarize(source, site)
