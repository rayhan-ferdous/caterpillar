from bs4 import BeautifulSoup
from urllib.parse import urljoin

baseurl = open('data/base.txt', 'r').readline()

#good for tiny elemnt mining, e.g. date of publication
#holds order of bs4 tag matching in BFS and redundancy
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

        text = elem.get_text(separator='~~~').split('~~~')          #separate text in the same tag with uncommon string, only stripping will still leave a lot of '\n' in the mid of string
        text = [t.strip() for t in text if t.strip() != '']         #still text holds too many space/newline characters


        if text != []:
            sdict['text'] = text

        summary.append(sdict)

    return summary

#good for article mining and no redundancy
#compromises HTML structure
def clean_text(summary):
    #repeated substring must occur after the original string
    #in other words, parent tag holds a string and child tag only holds a substring; the child tag with substring always occurs after the parent tag

    # text_summary = [t for t in summary if 'text' in t]

    for i in range((len(summary))):
        if 'text' in summary[i]:
            summary[i]['text'] = '~~~'.join(summary[i]['text'])


    #target substring
    for i in reversed(range(len(summary))):
        if 'text' in summary[i]:
            # namei = summary[i]['name']
            texti = summary[i]['text']

            #duplicate holder string
            for j in reversed(range(i)):
                if 'text' in summary[j]:
                    # namej = summary[j]['name']
                    textj = summary[j]['text']

                    if texti in textj and (textj.startswith('~~~') or textj.endswith('~~~')):
                        # print(j)
                        # print(texti)
                        # print(textj)
                        replaced = summary[j]['text'].replace(texti, '')
                        # print(replaced)
                        summary[j]['text'] = replaced



    for i in range(len(summary)):
        if 'text' in summary[i]:
            summary[i]['text'] = summary[i]['text'].split('~~~')
            summary[i]['text'] = [t for t in summary[i]['text'] if t != '']
            if summary[i]['text'] == []:
                del summary[i]['text']

    # for s in summary:
    #     print(s)
    return summary


def filter_links(summary):
    for s in summary:
        # print(s)
        if 'a' == s['name'] or 'href' == s['name'] or 'src' == s['name']:
            try:
                print(s)
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
    clean_summary = clean_text(summary)

    # filter_links(summary)
    # filter_heading(summary)


    for c in clean_summary:
        print(c)
        if 'text' in c and c['name'] == 'p':
            para = ' '.join(c['text'])
            wordcount = len(para.split(' '))
            charcount = len(para)
            print(wordcount, charcount, para)
