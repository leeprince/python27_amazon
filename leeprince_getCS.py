import re
import socket
import urllib
import urllib2
#from bs4 import BeautifulSoup

DEBUG = True

headers = { 
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }

def getHtml(url):
    req = urllib2.Request(url,headers=headers)
    try:
        page = urllib2.urlopen(req, timeout=100)
        html = page.read()
    #except urllib2.URLError, e:
        #print "Oops, timed out?"
        #html = "";
    except socket.timeout:
        print "Timed out!"
        html = "";
    except :
        print "Expection!"
        html = "";
        
    return html

def getSellersID(html):
    sellersIDreg = r'seller=(A\w+)'
    sellersIDre = re.compile(sellersIDreg)
    sellersID_list = re.findall(sellersIDre, html)
    if (len(sellersID_list) > 0):
        sellersID = sellersID_list[0];
    else:
        sellersID = "None"
    return sellersID

offerList_url = "http://www.amazon.de/gp/offer-listing/B01AZ78DWE/ref=ref=olp_page_1&startIndex=0";
# offerList_url = "http://www.amazon.de/gp/offer-listing/"+asin+"/ref=ref=olp_page_"+str(j)+"&startIndex="+str((j-1)*10);
# offerList_url = "https://www.amazon.de/gp/offer-listing/B0104OQRJE/ref=ref=olp_page_1&startIndex=0";
print " offerList_url:", offerList_url
offerList_page = getHtml(offerList_url)
print offerList_page
sellersID_list = getSellersID(offerList_page)
print "sellersID_list::", sellersID_list
print 'python program DONE' 
