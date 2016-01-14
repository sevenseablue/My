# coding: utf8

url = "http://cn-proxy.com/"

import urllib2
import time
import random
import re, os
import user_agents


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
ips_file = "E:\PycharmProjects\My\crawler\util\ips_list.txt"
last_time = 0


def crawl_url():
    try:
        request = urllib2.Request(url)
        request.add_header(user_agent, ua[random.randint(0, 8)])
        page = urllib2.urlopen(request, timeout=10)
        data = page.read()
        page.close()
        return data

    except Exception:
        time.sleep(1.3)


def usage():
    print "./CrawlerSimple.py resultPath."
    print "store the result to the default path result.txt"


def refresh_proxy_from_cn_proxy():
    proxy_list_1 = get_proxy_list_from_file()
    s1 = None
    if len(proxy_list_1) >= 2:
        while s1 is None:
            s1 = crawl_url_proxy(proxy_list_1)
    else:
        while s1 is None:
            s1 = crawl_url()
    # re.S, the symbol '.' matches any character including \n
    p1_tr = re.compile("""<tr>.*?((?:<td>.*?</td>.*?){5}).*?</tr>""", re.S)
    p2_td = re.compile("""<td>(.*?)</td>""", re.S)
    p3_speed = re.compile("""width: (\d+)%""", re.S)
    l1_tr = re.findall(p1_tr, s1)
    list_result = []
    for e in l1_tr:
        l2_td = re.findall(p2_td, e)
        l_result = [re.findall(p3_speed, e_td)[0] if e_td.find("style=\"width: ") > 0 else e_td for e_td in l2_td]
        if re.match("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", l_result[0]):
            list_result.append(l_result)

    list_result = sorted(list_result, key=lambda x: int(x[3]))
    list_result = [e for e in list_result if int(e[3])]  # < 69]
    if len(list_result) >= 1:
        fo = open(ips_file, 'w')
        for e in list_result:
            fo.write(",".join(e)+"\n")
        fo.close()
        return True

    return False


def get_proxy_list_from_file():
    proxy_list = []
    if os.path.exists(ips_file):
        f = open(ips_file, 'r')
    else:
        return proxy_list

    for line in f:
        line = line.strip()
        arr = line.split(",")
        proxy_list.append({"http": "http://%s:%s" % (arr[0], arr[1])})
    f.close()
    return proxy_list


def get_proxy_list():
    if refresh_proxy_from_cn_proxy():
        return get_proxy_list_from_file()
    return []


def crawl_url_proxy(proxy_list_1):
    try:
        proxy_ip = random.choice(proxy_list_1)  # 在proxy_list中随机取一个ip
        proxy_support = urllib2.ProxyHandler(proxy_ip)
        opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        request = urllib2.Request(url)
        user_agent_this = random.choice(user_agents.user_agents)  # 在user_agents中随机取一个做user_agent
        request.add_header('User-Agent', user_agent_this)  # 修改user-Agent字段
        page = urllib2.urlopen(request, timeout=10)
        html = page.read()
        page.close()
        return html
    except Exception:
        time.sleep(0.37)

if __name__ == "__main__":
    print get_proxy_list_from_file()
    for e in get_proxy_list():
        print e
