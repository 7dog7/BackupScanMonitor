# coding: utf-8
# me7dog7
import time
import threading
import sys
import ctypes
import inspect
import argparse
import random
import requests
import thread
import Queue
import os

targetListCount = 0
threadLock = 0
threadList = dict()
targetList = Queue.Queue()

headerss = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]


def isTrueDate(a):
    """查询输入日期是否有效"""
    # 把年月日剥离出来
    try:
        year = int(a[0:4])
        month = int(a[4:6])
        day = int(a[6:])
        # 判断月份是否不在0-12的范围内
        if month == 0 | month > 12:
            return False
        # 如果 一三五七八十腊 那么 三十一天永不差
        else:
            if month == 1 | month == 3 | month == 5 | month == 7 | month == 8 | month == 10 | month == 12:
                if day > 31:
                    return False
            # 四六九冬三十天
            else:
                if month == 4 | month == 6 | month == 9 | month == 11:
                    if day > 30:
                        return False
                # 平年二月二十八，但如果年份是400的倍数，二月还是二十九天
                else:
                    if year % 400 != 0 & year % 4 == 0:
                        if day > 28:
                            return False
                    else:
                        if day > 29:
                            return False
    except Exception, e:
        return False
    return True


# www.baidu.com return baidu.com
def urlFormat(url):
    if len(url.split('.')) >= 3:
        data = url[url.rfind('.', 0, url.rfind('.')) + 1:]
    else:
        data = url[url.rfind('/', 0, url.rfind('.')) + 1:]
    return data


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def _stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def dictPath(path):
    fileData = []
    path = str(path).split(',')
    if len(path) > 1:
        for i in path:
            file = open(str(i), "rb")
            fileData.append(file.read())
            file.close()
    else:
        file = open(str(path[0]), "rb")
        fileData.append(file.read())
        file.close()
    dataList = []
    for i in fileData:
        for dictTxt in i.split('\n'):
            dictTxt = dictTxt.strip()
            if dictTxt is not '':
                dataList.append(dictTxt)
    return dataList


def dictGroup(data, threadCount):
    l = [i for i in data]
    n = int(threadCount)  # 大列表中几个数据组成一个小列表
    return ([l[i:i + n] for i in range(0, len(l), n)])


def ruleDict(url, dictList, ruleDictList, postfixList):
    dataList = []
    for postfix in postfixList:
        for dictTxt in dictList:
            if isTrueDate(dictTxt):
                dictTxt.append('{0}_{1}_{2}'.format(int(dictTxt[0:4]), int(dictTxt[4:6]), int(dictTxt[6:])))
                dictTxt.append('{0}-{1}-{2}'.format(int(dictTxt[0:4]), int(dictTxt[4:6]), int(dictTxt[6:])))
                dictTxt.append('{0}_{1}'.format(int(dictTxt[4:6]), int(dictTxt[6:])))
                dictTxt.append('{0}{1}'.format(int(dictTxt[4:6]), int(dictTxt[6:])))
            else:
                for ruleDict in ruleDictList:
                    dataList.append(str(ruleDict).format(dictTxt=dictTxt, urlFormat=urlFormat(url).replace('.', ''),
                                                         postfix=postfix))
    return dataList


def scanBackMain(url, dictList, ruleDictList, postfixList, sleep):
    ruleDictList = ruleDict(url, dictList, ruleDictList, postfixList)
    for i in ruleDictList:
        headers = {'User-Agent': random.choice(headerss)}
        try:
            proxies = {
                "http": None,
                "https": None
            }
            r5 = requests.head(url='{0}/{1}'.format(url, i), headers=headers, timeout=5, proxies=proxies)
            if 'Content-Length' in r5.headers.keys():
                headers = str(r5.headers["Content-Length"])
            else:
                headers = 0
            time.sleep(float(sleep))
            print r5.url + ' : ' + str(r5.status_code) + ' : ' + str(headers)
            if int(headers) > 188888:
                with open('backup.txt', 'a+') as backup:
                    targetList.put('{0}/{1}'.format(url, i))
                    backup.write('{0}/{1}'.format(url, i) + '\n')
        except Exception, e:
            pass


def readDictTxt(path):
    f = open(path, 'rb')
    dataList = []
    for line in f.readlines():
        line = line.strip('\n')
        line = line.strip('\r')
        line = line.strip()
        if line is not '':
            dataList.append(line)
    return dataList


def main(threadCount, url, dictList, ruleDictList, postfixList, sleep):
    global threadLock
    for i in url:
        try:
            if threadLock == 0:
                while True:
                    for dictCut in dictList:
                        if len(threadList) < threadCount:
                            t = threading.Thread(target=scanBackMain,
                                                 args=(i, dictCut, ruleDictList, postfixList, sleep,))
                            t.start()
                            threadList[t.getName()] = {'thread': t, 'time': time.time()}  # 记录
                        else:
                            time.sleep(2)
                    break
        except KeyboardInterrupt as e:
            print e
            if len(threadList) > 0:
                threadLock = 1  # 锁线程
                for k, v in threadList.items():
                    _stop_thread(v['thread'])
                sys.exit()
            else:
                if len(threadList) == 0:
                    break


def parser_error(errmsg):
    print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
    sys.exit()


def threadCheck(record, _timeout):
    while True:
        dellist = []
        if len(record) > 0:
            for k, v in record.items():
                # print('检测：' + k)
                if v['thread'].isAlive():
                    if time.time() - v['time'] > _timeout:
                        _stop_thread(v['thread'])
                        dellist.append(k)
                else:
                    dellist.append(k)
            time.sleep(1)
            for dl in dellist:
                del (record[dl])


def getContentFile(num):
    while True:
        if not targetList.empty():
            target = targetList.get()
            r = requests.get(target, stream=True)
            f = open(target[target.rfind('/', 0, target.rfind('/') + 1) + 1:], "wb")
            # chunk是指定每次写入的大小，每次只写了512byte
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='\tExample: \r\n' +
                                           'scanBak: python ' + sys.argv[
                                               0] + ' -u https://www.163.com -dp ' + os.path.dirname(
        __file__) + '/dict1.txt -px ' + os.path.dirname(__file__) + '/postfix.txt'
                                                                    ' -t 10 -rl ' + os.path.dirname(
        __file__) + '/ruleDict.txt -sp 0.2\n' +
                                           'scanBak: python ' + sys.argv[
                                               0] + ' -u ' + os.path.dirname(
        __file__) + '/url.txt -dp ' + os.path.dirname(__file__) + '/dict1.txt -px ' + os.path.dirname(
        __file__) + '/postfix.txt'
                    ' -t 10 -rl ' + os.path.dirname(__file__) + '/ruleDict.txt -sp 0.2\n'
                                     )
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-u', '--url', help="target url: -u /home/me7dog7/url.txt", required=True)
    parser.add_argument('-dp', '--dictPath', help='dictPath: -dp /home/me7dog7/dict1.txt,/home/me7dog7/dict2.txt',
                        required=False)
    parser.add_argument('-px', '--postfix', help='postfix: -px /home/me7dog7/postfix.txt', required=True)
    parser.add_argument('-rl', '--ruleDict', help='ruleDict: -rl /home/me7dog7/ruleDict.txt', required=True)
    parser.add_argument('-t', '--threadSum', help='threadSum: -t 10', required=True)
    parser.add_argument('-sp', '--sleep', help='sleep: -sp 0  help:D elay per request', required=True)
    # parser.add_argument('-sd', '--subDomain', help='subDomain: -sd /home/me7dog7/sudDomain.txt', required=False)

    args = parser.parse_args()
    if args.url is None and args.dictPath is None and args.postfix is None \
            and args.ruleDict is None and args.threadSum is None and args.sleep is None:
        print 'python ' + sys.argv[0] + ' -h'
        exit()

    if 'http' not in args.url:
        urlList = readDictTxt(args.url)
    else:
        urlList = [args.url]
    dictPathList = readDictTxt(args.dictPath)
    postfixList = readDictTxt(args.postfix)
    ruleDictList = readDictTxt(args.ruleDict)
    dictList = dictGroup(dictPath(args.dictPath), args.threadSum)  # 分割字典
    thread.start_new_thread(getContentFile, (1,))
    main(args.threadSum, urlList, dictList, ruleDictList, postfixList, args.sleep)
    time.sleep(2)
    thread.start_new_thread(threadCheck, (threadList, 3600))  # 检测线程超时情况 1小时
