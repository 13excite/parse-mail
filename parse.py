#!/usr/bin/python
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

def last_pars_headers(lst):
    link_pattern = re.compile('https:\/\/linuxdesktopcloud\.mail\.ru.*deb')
    lst_deb = []
    lst_rpm = []
    for item in lst:
        if link_pattern.findall(item):
            a = re.findall(r"https:\/\/linuxdesktopcloud\.mail\.ru.*deb", item)
            lst_deb.append(a)
        else:
            b = re.findall(r"https:\/\/linuxdesktopcloud\.mail\.ru.*rpm", item)
            lst_rpm.append(b)
        #if link_pattern.findall(item):
            #lst_in_pattern.append(item)
    return [lst_deb, lst_rpm]

def main():
    txt = parse(get_html(base_url))
    link_lst = re_parse(txt)
    headers_lst = get_headers_link(link_lst)
    hdrs = last_pars_headers(headers_lst)
    first_lst = hdrs[:1]  #list deb packege
    second_lst = hdrs[-1:]   #list rpm packege

    #extract nested DEB list
    lst_for_deb = []
    for f in first_lst:
        for u in range(len(f)):
            for m in range(len(f[u])):
                lst_for_deb.append(f[u][m])
    deb_uniq = set(lst_for_deb)

    #write data in file
    for line1 in deb_uniq:
        my_deb_file = open("deb.txt", "a")
        my_deb_file.write(line1 + "\n")
        my_deb_file.close()


    #extract nested RPM list
    lst_for_rpm = []
    for i in second_lst:
        new_second_lst = i[0:-2]
        for iter_lst in range(len(new_second_lst)):
            for j in range(len(new_second_lst[iter_lst])):
                lst_for_rpm.append(new_second_lst[iter_lst][j])
    rpm_uniq = set(lst_for_rpm)
    #write data in file
    for line2 in rpm_uniq:
        rpm_file = open("rpm.txt", "a")
        rpm_file.write(line2 + "\n")
        rpm_file.close()


if __name__ == '__main__':
    main()