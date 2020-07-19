from bs4 import BeautifulSoup
from urllib.parse import urljoin

baseurl = open('data/base.txt', 'r').readline()

#parser
def summarize(source):
    soup = BeautifulSoup(source, 'html.parser')

    summary = []

    for elem in soup.find_all():
        edict = elem.attrs  #elem dict
        sdict = {}          #summary dict

        name = elem.name
        sdict['name'] = name

        if 'href' in edict:
            absurl = urljoin(baseurl, edict['href'])
            if absurl.startswith(baseurl):
                sdict['absurl'] = absurl

        if 'src' in edict:
            src = urljoin(baseurl, edict['src'])
            if src.startswith(baseurl):
                sdict['src'] = src

        if 'alt' in edict:
            alt = edict['alt']
            sdict['alt'] = alt

        text = elem.get_text(separator='\n').split('\n')
        fine_text = [t for t in text if t.strip() != '']
        if len(fine_text) > 0:
            sdict['fine_text'] = fine_text

        summary.append(sdict)

    return summary

def remove_duplicates(summary):
    pass

def filter_links(summary):
    for s in summary:
        # print(s)
        if 'a' == s['name'] or 'href' == s['name'] or 'a' == s['name']:
            try:
                print(s)
            except:
                pass

def filter_text(summary):
    for s in summary:
        if 'p' == s['name']:
            try:
                print(s['name'], s['fine_text'])
            except:
                pass

def filter_heading(summary):
    for s in summary:
        if 'h1' == s['name'] or 'h2' == s['name'] or 'h3' == s['name'] or \
            'h4' == s['name'] or 'h5' == s['name'] or 'h6' == s['name']:
                try:
                    print(s['name'], s['fine_text'])
                except:
                    pass


if __name__ == '__main__':
    source = open('data/page.html', 'r')
    summary = summarize(source)
    # filter_links(summary)
    # filter_text(summary)
    filter_heading(summary)
