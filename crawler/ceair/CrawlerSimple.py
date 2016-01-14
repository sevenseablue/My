# coding: utf8

import urllib2
import time
import random
import sys
sys.path.append("..")
import util
import util.proxy_ip as proxy_ip
import util.user_agents as user_agents
import json


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


def crawl_url(url, proxy_list):
    try:
        proxy_ip = random.choice(proxy_list)  # 在proxy_list中随机取一个ip
        print "haha", proxy_ip
        proxy_support = urllib2.ProxyHandler(proxy_ip)
        opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        request = urllib2.Request(url)
        user_agent = random.choice(user_agents.user_agents)  # 在user_agents中随机取一个做user_agent
        request.add_header('User-Agent', user_agent)  # 修改user-Agent字段
        page = urllib2.urlopen(request, timeout=10)
        html = page.read()
        page.close()
        return html

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
    f = open("E:\PycharmProjects\My\crawler\umetrip\hangbianqingqiu.20150720.100.txt", 'r')
    # re.S, the symbol '.' matches any character including \n
    p1 = re.compile("""class="state">.*?<div class=".*?">(.*?)</div>.*?</div>""", re.S)
    ind = 1
    proxy_list = proxy_ip.get_proxy_list_from_file()
    for line in f:
        if ind < 0:
            ind += 1
            continue
        print ind, line.strip()
        ind += 1
        arr = line.rstrip("\n").split("\t")
        # arr1 = arr[1].split(",")
        url = "http://www.umetrip.com/mskyweb/fs/fc.do?flightNo=%s&date=%s&channel=" % (arr[0], arr[1])
        s1 = crawl_url(url, proxy_list)
        while s1 is None:
            print "s1 is None, sleep..."
            time.sleep(1)
            s1 = crawl_url(url, proxy_list)
        # print s1
        l1 = re.findall(p1, s1)
        if len(l1) >= 1:
            result = l1[0].strip()
        else:
            result = "no_found"
        fo.write("%s %s\n" % (" ".join(arr), result))
        fo.flush()
        time.sleep(1)

    f.close()
    fo.close()



def main2():
    ts = int((time.time()-3600*24)*1000)
    url = "http://www.ceair.com/addservice/new-aoc!queryNewFlightStatus.shtml?qType=0&flightTime=%%2B&queryCxr=MU&queryFlightno=5757&_=%s" % ts
    url = "http://www.ceair.com/addservice/new-aoc!queryNewFlightStatus.shtml?qType=0&flightTime=.&queryCxr=MU&queryFlightno=5319&_=%s" % ts
    url = "http://www.ceair.com/addservice/new-aoc!queryNewFlightStatus.shtml?qType=0&flightTime=-&queryCxr=MU&queryFlightno=5319&_=%s" % ts
    # url = "http://www.baidu.com/"
    proxy_list = proxy_ip.get_proxy_list_from_file()
    s1 = None
    print "s1"
    print len(proxy_list)
    while s1 is None:
        print "s1 is none."
        s1 = crawl_url(url, proxy_list)
    print s1
    js1_str = s1[s1.find("(")+1:s1.rfind(")")]
    print js1_str
    js1 = json.loads(js1_str)
    for flight_seg in js1:
        print flight_seg["flightno"],flight_seg["actualFlightShowList"][0]["depAirportCode"],\
            flight_seg["actualFlightShowList"][0]["arrAirportCode"],\
            flight_seg["actualFlightShowList"][0]["status"]


if __name__ == "__main__":
    main2()