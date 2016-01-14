# coding: utf8

import urllib2
import time
import random

user_agent = 'User-Agent'
ua = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/16.9',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/15.1',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/14.5',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/13.7',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/12.3',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/11.4',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/10.0',
      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/3.2']


def crawl_url(url):
    try:
        request = urllib2.Request(url)
        request.add_header(user_agent, ua[random.randint(0, 8)])
        page = urllib2.urlopen(request, timeout=10)
        data = page.read()
        page.close()
        return data.decode('gb2312', "ignore").encode("utf8")
    except Exception:
        time.sleep(0.37)


import re
import sys


def usage():
    print "./CrawlerSimple.py resultPath."
    print "store the result to the default path result.txt"


def main():
    if len(sys.argv) != 2:
        usage()
        result_path = "result.txt"
    else:
        result_path = sys.argv[1]
    fo = open(result_path, 'w')
    f = open("f_special_refund_orderno_20150713.txt.flightno.2.success", 'r')
    ind = 1
    for line in f:
        if ind < 0:
            ind += 1
            continue
        arr = line.rstrip("\n").split("\t")
        arr1 = arr[1].split(",")
        for fno in arr1:
            url = "http://flights.ctrip.com/actualtime/fno-%s/t%s" % (fno, arr[2].replace("-", ""))
            s1 = crawl_url(url)
            while s1 is None:
                time.sleep(1)
                s1 = crawl_url(url)
            l1 = re.findall("<strong class=.*?</strong>", s1)
            if len(l1) >= 2:
                result = re.split("<|>", l1[1])[2]
            else:
                result = "no_found"
            fo.write("%s %s\n" % (" ".join(arr), result))

    f.close()
    fo.close()


if __name__ == "__main__":
    main()