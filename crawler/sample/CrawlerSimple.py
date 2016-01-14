# coding: utf8

import urllib2
import time
import random
import re
from crawler.util import user_agents

# sys.path.append("..")


def crawl_url(url):
    try:
        opener = urllib2.build_opener(urllib2.HTTPHandler)
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


def usage():
    print "./CrawlerSimple.py resultPath."
    print "store the result to the default path result.txt"


def main():
    url = "http://www.baidu.com"
    s1 = crawl_url(url)
    print s1
    # # re.S, the symbol '.' matches any character including \n
    # p1 = re.compile("""class="state">.*?<div class=".*?">(.*?)</div>.*?</div>""", re.S)
    # l1 = re.findall(p1, s1)
    # print l1[0].strip()


if __name__ == "__main__":
    main()