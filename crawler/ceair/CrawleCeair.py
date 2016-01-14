# coding: utf8

import urllib2
import time
import random
import sys
sys.path.append("../")
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
import datetime


def usage():
    print "./CrawlerSimple.py inputPath resultPath."
    print "store the result to the default path result.txt"


def main():
    if len(sys.argv) != 3:
        usage()
        input_path = "E:\PycharmProjects\My\crawler\umetrip\hangbianqingqiu.20150720.100.txt"
        result_path = "result.txt"
    else:
        input_path = sys.argv[1]
        result_path = sys.argv[2]

    proxy_list = proxy_ip.get_proxy_list_from_file()
    fo = open(result_path, 'w')
    f = open(input_path, 'r')
    ts = int((time.time()-3600*24)*1000)

    dt = datetime.datetime.now()
    dt_m1 = dt - datetime.timedelta(1)
    dt_p1 = dt + datetime.timedelta(1)
    dt_str, dt_m1_str, dt_p1_str = dt.strftime('%Y-%m-%d'), dt_m1.strftime('%Y-%m-%d'), dt_p1.strftime('%Y-%m-%d')
    dt_flag_dic = {dt_str: ".", dt_m1_str: "-", dt_p1_str: "%%2B"}

    for line in f:
        line = line.rstrip("\n")
        arr = line.split("\t")
        flightno, dep_code, arr_code, dep_date = arr[3:]
        if dep_date not in dt_flag_dic:
            continue
        url = "http://www.ceair.com/addservice/new-aoc!queryNewFlightStatus.shtml?qType=0&flightTime=%s&queryCxr=%s&queryFlightno=%s&_=%s" \
              % (dt_flag_dic[dep_date], flightno[0:2], flightno[2:], ts)
        s1 = crawl_url(url, proxy_list)
        while s1 is None:
            s1 = crawl_url(url, proxy_list)
        js1_str = s1[s1.find("(")+1:s1.rfind(")")]
        js1 = json.loads(js1_str)
        seg_list = []
        for flight_seg in js1:
            seg_list += flight_seg["actualFlightShowList"]
        for seg in seg_list:
            if seg["flightno"]==flightno and seg["depAirportCode"]==dep_code and seg["arrAirportCode"]==arr_code and seg["std"][0:8]==dep_date.replace("-",""):
                ata, sta = datetime.datetime.strptime(seg["ata"], "%Y%m%d %H:%M"), datetime.datetime.strptime(seg["sta"], "%Y%m%d %H:%M")
                late_hours = (ata-sta).seconds/3600.
                if late_hours>=3:
                    fact_result = "延误"
                else:
                    fact_result = seg["status"]
                fo.write("%s\t%s\t%s\t%s\t%s\n" % (line, seg["status"].encode("utf8"), fact_result, str(late_hours), js1_str))
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
    main()