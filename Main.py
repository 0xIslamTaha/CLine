#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Created by Dagger -- https://github.com/DaggerES
import CCcamTester
import requests, re, datetime, queue, threading

clines = []
results = queue.Queue()


def GetTestiousClines():
    global clines
    header = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    session = requests.Session()
    session.headers.update(header)

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    regExpr = re.compile('([CN]:.*?)#.*\n<br>')
    for url in ["http://www.testious.com/free-cccam-servers/" + datetime.date.today().strftime("%Y-%m-%d"),
                "http://www.testious.com/free-cccam-servers/" + yesterday.strftime("%Y-%m-%d")]:
        htmlCode = session.get(url=url).text
        matches = regExpr.findall(htmlCode)
        for match in matches:
            clines.append(str(match))


def work():
    while not cline_queue.empty():
        cline_test = cline_queue.get()
        cline_result = CCcamTester.TestCline(cline_test)
        if cline_result:
            results.put(cline_result)
        cline_queue.task_done()


if __name__ == "__main__":
    GetTestiousClines()

    cline_queue = queue.Queue()
    for cline in clines:
        cline_queue.put(cline)

    for _ in range(50):
        thread = threading.Thread(target=work)
        thread.start()

    cline_queue.join()

    with open('result', 'w') as file:
        while not results.empty():
            file.write(str(results.get()))
            file.write('\n')
