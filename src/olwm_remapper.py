# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="bmillett"
__date__ ="$Dec 2, 2010 6:24:03 PM$"


from mymath import rational
import sys
import os.path
import re
import difflib

from xml.dom import minidom
from urlparse import urlparse

def make_conf(source,match):
    doc_s=parse_xml_file(source)
    old_urls = doc_s.getElementsByTagName("url")

    doc_m=parse_xml_file(match)
    new_urls = doc_m.getElementsByTagName("url")

    results = {}
    new_urls_dict = {}

    for m in new_urls:
        new_url = m.childNodes[1].firstChild.data
        new_urls_dict[new_url] = get_distilled_uri_string(new_url)

    print "working...please wait."

    for s in old_urls:
        old_url = s.childNodes[1].firstChild.data
        
        if 'summary' in old_url:
            continue

        old_uri_string = get_distilled_uri_string(old_url)

        results[old_url] = 0

        for new_url in new_urls_dict:

            s = difflib.SequenceMatcher(None, old_uri_string, new_urls_dict[new_url])

            #print "compared %s to %s: %.4f" % (old_uri_string, new_urls_dict[new_url], s.ratio())

            if old_url.strip() != new_url.strip() and s.ratio() >= 0.5 and s.ratio() > results[old_url]:
                #print "compared %s to %s: %.4f" % (old_uri_string, new_urls_dict[new_url], s.ratio())
                results[old_url] = new_url

            if results[old_url] == 0:
                results[old_url] = False

    for key in results:
        if results[key] != False:
            print "Redirect 301 %s %s" % (get_url_path(key), results[key])

def get_distilled_uri_string(url_string):
    #get the uri part
    url = get_url_path(url_string)
    #remove file extensions
    url = re.sub('\.(php|html*)$', '', url)
    # get just words to use for compare
    return re.sub('[-./]+', ' ', url).strip()

def get_url_path(url_string):
    return urlparse(url_string).path

def parse_xml_file(path):
    if os.path.isfile(path):
        try:
            xmldoc = minidom.parse(path)
        except xml.parsers.expat.ExpatError, e:
            print e.args[0]
            sys.exit(1);
    else:
        print 'path is not a file!'
        sys.exit(1);

    return xmldoc


if __name__ == "__main__":
    make_conf(sys.argv[1], sys.argv[2])
