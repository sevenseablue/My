# coding: utf8

import urllib2
import urllib
import time
import ssl
import random as r
import os

__author__ = 'wangdawei'


def crawlUrl(url):
    headers = {
    'User-agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)'}
    data = urllib.urlencode({})
    req = urllib2.Request(url, data, headers)
    gContext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    response = urllib2.urlopen(req, context=gContext, timeout=13)
    the_page = response.read()

    return the_page


def crawl12306():
    ind = 1
    dirInd = 5
    while True:
        dataDir = "E:/data/pic/12306/raw/%s" % dirInd

        if ind % 500 == 0:
            dirInd += 1
            dataDir = "E:/data/pic/12306/raw/%s" % dirInd
            if not os.path.exists(dataDir):
                os.mkdir(dataDir)
        try:
            name = "%s%s%s" % (r.randint(10000, 99999), r.randint(10000, 99999), r.randint(10000, 99999))
            url = "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&0.%s" % name
            the_page = crawlUrl(url)
            fw = open("%s/%s.png" % (dataDir, name), 'wb')
            fw.write(the_page)
            fw.close()
            print str(ind).center(30, "*")
            time.sleep(11 + r.random() * 4)
            ind += 1
            # if dirInd == 5:
            # break

        except Exception:
            time.sleep(120)


def main():
    crawl12306()


if __name__ == "__init__":
    main()