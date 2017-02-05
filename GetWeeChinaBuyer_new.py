import time
import random
import re
import socket
import urllib
import urllib2
from bs4 import BeautifulSoup

DEBUG = True

headers = []
headers.append({'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6' })
headers.append({'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0' })
headers.append({'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)' })
headers.append({'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)' })
headers.append({'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)' })
headers.append({'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1' })
headers.append({'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3' })
headers.append({'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13' })

def getHtml(url):
    time.sleep(random.randint(2,5))  #avoid being detected as a robot
    agent = random.randint(0,7);
    # print headers[agent];

    req = urllib2.Request(url,headers=headers[agent])
    try:
        page = urllib2.urlopen(req, timeout=100)
        html = page.read()
    #except urllib2.URLError, e:
    #    print "Oops, timed out?"
    #    html = "";
    except socket.timeout:
        # print "Timed out!"
        html = "";
    except :
        # print "Expection!"
        html = "";
        
    return html

def getASIN(html):
    reg = r'<a class="a-size-small a-link-normal" href="/product-reviews/(B.{9})'
    asinre = re.compile(reg)
    asinlist = re.findall(asinre, html)
    return asinlist

def getSellersNum(html):
    sellersNumreg = r'<span class="olp-padding-right"><a href="/gp/offer-listing/B.{9}.+">(\d+)'
    sellersNumre = re.compile(sellersNumreg)
    sellersNum_list = re.findall(sellersNumre, html)
    if (len(sellersNum_list) > 0):
        sellersNum = sellersNum_list[0];
    else:
        sellersNum = 1;
    return sellersNum

def getSellersID(html):
    sellersIDreg = r'seller=(A\w+)'
    sellersIDre = re.compile(sellersIDreg)
    sellersID_list = re.findall(sellersIDre, html)
    if (len(sellersID_list) > 0):
        sellersID = sellersID_list[0];
    else:
        sellersID = "None"
    return sellersID

# def getShipFrom(html):
#     fromreg = r'Ships from (\w+)'
#     fromre = re.compile(fromreg)
#     from_list = re.findall(fromre, html)
#     if (len(from_list) > 0):
#         from_place = from_list[0];
#     else:
#         from_place = "Unknown";
#     return from_place

def getShipFromChina(html):
    chinareg = r'<li>(CN|HK|AT|BR|CA|CH|DE|DK|ES|FR|GB|IN|IT|JP|KP|KR|LU|MO|NL|NO|PA|PL|PH|PT|RO|RU|SE|SG|TH|TW|UA|US|VA|VN)</li>'
    chinare = re.compile(chinareg)
    china_list = re.findall(chinare, html)
    if (len(china_list) == 1 ):
        china_Seller = china_list[0]
    elif(len(china_list) == 2 ):
        china_Seller = china_list[1]
    else :
        china_Seller = "NoCountry"
    return china_Seller

def getSellerRate(html):
    ratereg = r'<b>(\S+)</b> Bewertungen'
    ratere = re.compile(ratereg)
    rate = re.findall(ratere, html)
    if (len(rate) > 0):
        seller_rate = rate[0].replace(".","")
    else:
        seller_rate = "NoFeedback"
    return seller_rate

# category_list = [line.rstrip('\n') for line in open('category_computers_sortedA.txt')] #//Protective sleeve and shell
# category_list = [line.rstrip('\n') for line in open('category_computers_sortedB.txt')] #//Screen protector
# category_list = [line.rstrip('\n') for line in open('category_computers_sortedC.txt')] #//Data line
# category_list = [line.rstrip('\n') for line in open('category_computers_sortedD.txt')] #//Bluetooth headset
# category_list = [line.rstrip('\n') for line in open('category_computers_sortedE.txt')] #//Mobile phone
# category_list = [line.rstrip('\n') for line in open('category_computers_sortedF.txt')] #//Portable Speakers && Outdoor Speakers>>leeprince_2017-1-12
# category_list = [line.rstrip('\n') for line in open('category_computers_sortedG.txt')] #//MP3 player accessories && Video camera
# category_list = [line.rstrip('\n') for line in open('category_computers_sortedH.txt')] #//Slide ,scanner && Digital camera
# category_list = [line.rstrip('\n') for line in open('category_computers_sortedI.txt')] #//Telephone, VOIP and accessories && SmartWatch mobile phones and accessories
# category_list = [line.rstrip('\n') for line in open('category_computers_sortedJ.txt')] #//Home theater, TV and video && hi-fi stereo && MP3 player && Navigation>>leeprince_2017-1-12
# category_list = [line.rstrip('\n') for line in open('category_computers_sortedK.txt')] #//SLR && Tablet PC
# category_list = [line.rstrip('\n') for line in open('category_computers_sortedL.txt')] #//television && Ornaments
category_list = [line.rstrip('\n') for line in open('category_computers_sortedM.txt')]   #//television && Ornaments >>leeprince_2017-1-16

# print category_list
# print len(category_list)

print 'sellerID',',','china_Seller',',','seller_rate',',','category',',','asin',',','product_url',',','offerList_url',',','sellers_url',',','RunTime'
for ii in range (0, len(category_list)):
    category = category_list[ii]
    bestseller_prefix = "http://www.amazon.de/gp/bestsellers/"+str(category)
    for i in range (1, 6): # 5 pages for 100 best products
        bestsellers_url = bestseller_prefix+"#"+str(i);
        # print 'bestsellers_url',bestsellers_url

        bestsellers_page = getHtml(bestsellers_url)
        # print bestsellers_page

        asin_list = getASIN(bestsellers_page)
        # print asin_list

        for jj in range(0, len(asin_list)):  # 20 best products per page
            asin = asin_list[jj]
            product_url = "http://www.amazon.de/gp/product/"+asin
            # print "asin::", asin, " product_url::", product_url

            product_page = getHtml(product_url)
            # print product_page    

            sellersNum = getSellersNum(product_page)
            # print 'asin::',asin,' sellersNum::',sellersNum

            pageNum = int(sellersNum)/10 + 1
            # print 'asin::',asin,' pageNum::',pageNum

            for j in range (1, pageNum+1):  # Number of pages for the sellers list
                offerList_url = "http://www.amazon.de/gp/offer-listing/"+asin+"/ref=olp_page_"+str(j)+"&startIndex="+str((j-1)*10);
                # print "asin::", asin," page No. ", j," offerList_url::", offerList_url

                offerList_page = getHtml(offerList_url)
                # print "asin", asin,'offerList_page::',j,r'\n',offerList_page

                soup = BeautifulSoup(offerList_page)
                # print "asin", asin,r'soup\n',offerList_page

                div_list = soup.findAll(attrs={"class" : "a-row a-spacing-mini olpOffer"})
                # div_list = soup.findAll(attrs={"class" : "a-column a-span3 olpDeliveryColumn"}) # That would be a little bit of a problem
                # print 'div_list',asin,r'\n',div_list

                for k in range (0, len(div_list)):  # 10 sellers per page
                    sellerID = getSellersID(str(div_list[k]))
                    # print "category:", ii, " ASIN:", (i-1)*20+jj, "-", asin, "seller:", (j-1)*10+k ,"-", sellerID, "ships from :", from_place
                    if(sellerID == 'A8KICS1PHF7ZO'):
                        china_Seller = 'NoCountry'
                        seller_rate = '111325'
                    else:
                        sellers_url = "https://www.amazon.de/gp/aag/details/ref=olp_merch_cust_glance_1?seller="+sellerID;
                        # print 'asin::',asin," sellerID::",sellerID,' sellers_url::',sellers_url

                        sellers_page = getHtml(sellers_url)
                        # print 'sellers_page_',sellerID,'sellers_page',sellers_page

                        china_Seller = getShipFromChina(sellers_page)
                        # print 'asin::',asin," sellerID::",sellerID,' china_Seller::',china_Seller

                        seller_rate = getSellerRate(sellers_page)
                        # print 'asin::',asin," sellerID::",sellerID,' seller_rate::',seller_rate

                    if china_Seller == 'CN' or china_Seller == 'HK':
                        RunTime = time.strftime('%Y-%m-%d %X',time.localtime())
                        print sellerID,',',china_Seller,',',seller_rate,',',category,',',asin,',',product_url,',',offerList_url,',',sellers_url,',',RunTime