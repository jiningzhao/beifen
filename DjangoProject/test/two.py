import requests
import urllib.request
import time
# import pymysql
from DB_config import DB

# import pymongo
# client = pymongo.MongoClient('localhost', 27017)
# book_qunar = client['qunar']
# sheet_qunar_zyx = book_qunar['qunar_zyx']

# conn = conn = pymysql.connect('localhost', 'root', '123456')
# conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='jining_test', charset='utf8')
url = "https://touch.dujia.qunar.com/depCities.qunar"
strhtml = requests.get(url)
dep_dict = strhtml.json()
values = []
for dep_item in dep_dict['data']:
    for dep in dep_dict['data'][dep_item]:
        a = []
        print(dep)
        url = "https://touch.dujia.qunar.com/golfz/sight/arriveRecommend?dep={}" \
              "&exclude=&extensionImg=255,175".format(urllib.request.quote(dep))
        time.sleep(1)
        strhtml = requests.get(url)
        arrive_dict = strhtml.json()
        for arr_iteam in arrive_dict['data']:
            for arr_iteam_1 in arr_iteam['subModules']:
                for query in arr_iteam_1['items']:
                    if query['query'] not in a:
                        a.append(query['query'])
        print("++++")
        for item in a:
            url = "https://touch.dujia.qunar.com/list?" \
                  "modules=list%2CbookingInfo%2CactivityDetail" \
                  "&dep={0}" \
                  "&query={1}" \
                  "&dappDealTrace=true" \
                  "&mobFunction=%E6%89%A9%E5%B1%95%E8%87%AA%E7%94%B1%E8%A1%8C" \
                  "&cfrom=zyx" \
                  "&it=pop_arrive_0" \
                  "&date=&needNoResult=true" \
                  "&originalquery={1}" \
                  "&limit=0,20&includeAD=true" \
                  "&qsact=search ".format(urllib.request.quote(dep), urllib.request.quote(item))
            time.sleep(1)
            strhtml = requests.get(url)
            print(strhtml.json()['data']['limit'])
            routeCount = int(strhtml.json()['data']['limit']['routeCount'])

            print(routeCount)
            for limit in range(0, routeCount, 20):
                url = "https://touch.dujia.qunar.com/list?" \
                  "modules=list%2CbookingInfo%2CactivityDetail" \
                  "&dep={0}" \
                  "&query={1}" \
                  "&dappDealTrace=true" \
                  "&mobFunction=%E6%89%A9%E5%B1%95%E8%87%AA%E7%94%B1%E8%A1%8C" \
                  "&cfrom=zyx" \
                  "&it=pop_arrive_0" \
                  "&date=&needNoResult=true" \
                  "&originalquery={1}" \
                  "&limit={2},20&includeAD=true" \
                  "&qsact=search ".format(urllib.request.quote(dep), urllib.request.quote(item), limit)
                time.sleep(1)
                strhtml = requests.get(url)
                result = {
                    'date': time.strftime('%Y-%m-%d', time.localtime(time.time())),
                    'dep': dep,
                    'arrive': item,
                    'limit': limit,
                    'result': strhtml.json()
                }
                print(result)

                values.append((len(values), result['date'], result['dep'], result['arrive'], result['limit'],
                               result['result']))
print(values)
DB().db_con(values)
