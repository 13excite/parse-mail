import urllib
from bs4 import  BeautifulSoup
import re
import pycurl
import cStringIO




base_url = 'https://help.mail.ru/cloud_web/app/linux'

# get pure html
def get_html(url):
    response = urllib.urlopen(url)
    return response.read()
# parsing pure html and get all href links
def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    my_link = []
    for link in soup.find_all('a'):
        my_link.append(link.get('href'))
    return my_link

#parse list with href and return our pattern links in list
def re_parse(teg_list):
    finish_link_lst = []
    p = re.compile('^http:\/\/r\.mail\.ru\/n\d{9}')
    for elm in teg_list:
        if p.findall(elm):
            finish_link_lst.append(elm)
    return finish_link_lst

# go to r.mail links and return list with headers, which have new link in desktop linux
def get_headers_link(links_lists):
    last_lst = []
    for elem in links_lists:
        buf = cStringIO.StringIO()
        URL = elem
        c = pycurl.Curl()
        c.setopt(c.URL, URL)
        c.setopt(c.NOBODY, 1)
        c.setopt(c.HEADERFUNCTION, buf.write)
        c.perform()

        header = buf.getvalue()
        last_lst.append(header)
    return last_lst

def main():
    txt = parse(get_html(base_url))
    link_lst = re_parse(txt)
    headers_lst = get_headers_link(link_lst)
    for i in headers_lst:
        print i


if __name__ == '__main__':
    main()