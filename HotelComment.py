from time import sleep

import requests
import json
import pymysql

hotel_id = '375265'
base_url = 'http://m.ctrip.com/restapi/soa2/14605/gethotelcomment?_fxpcqlniredt=09031089110364396442'


def request_data(pageIndex):  # 向网页发出请求
    post_data = {
        "hotelId": hotel_id,
        "pageIndex": pageIndex,
        "tagId": 0,
        "pageSize": 10,
        "groupTypeBitMap": 2,
        "needStatisticInfo": 0,
        "order": 0,
        "basicRoomName": "",
        "travelType": -1,
        "head":
            {
                "cid": "09031089110364396442",
                "ctok": "", "cver": "1.0",
                "lang": "01",
                "sid": "8888",
                "syscode": "09",
                "auth": "",
                "extension": []
            }
    }
    headers = {  # 获取携程酒店评论的信息
        "Cookie": "_abtest_userid=ce69273e-c6d7-48fb-8a10-23829b80c758; _RSG=0aqjq8JL1.0RUAEIlI73G8; _RDG=2860c1e0e7c0722325147ffd9ccbdf69bc; _RGUID=0f815532-34b7-4900-8403-1d2bd238a79b; _ga=GA1.2.1806967655.1536243523; _jzqco=%7C%7C%7C%7C1536243523139%7C1.1795580862.1536243523039.1546334123103.1546334137464.1546334123103.1546334137464.0.0.0.7.7; Session=smartlinkcode=U135371&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; __zpspc=9.4.1550212629.1550212629.1%233%7Cwww.google.com%7C%7C%7C%7C%23; appFloatCnt=1; Union=AllianceID=949992&SID=1566142&OUID=; _RF1=222.184.15.238; _bfa=1.1534769124941.351deq.1.1550225770783.1551009073806.13.37.228032; Mkt_UnionRecord=%5B%7B%22aid%22%3A%22949992%22%2C%22timestamp%22%3A1551009073943%7D%5D; arp_scroll_position=3104; GUID=09031089110364396442",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        "cookieOrigin": "http://m.ctrip.com",
        "Host": "m.ctrip.com",
        "Origin": "http://m.ctrip.com",
        "Referer": "http://m.ctrip.com/html5/hotel/HotelDetail/dianping/435383.html?tdsourcetag=s_pctim_aiomsg"
    }
    response = requests.post(url=base_url, json=post_data, headers=headers)
    return response.text


# 打开数据库连接
db = pymysql.connect(host="localhost",user="root",password="123456",db="test",port=3306)

# 使用cursor()方法获取操作游标



def insert_data(checkInDate, postDate, content, ratingPoint, h_id):
    cursor = db.cursor()
    try:
        # SQL 插入语句
        sql = """INSERT INTO comment(checkInDate,postDate,content,ratingPoint,h_id)VALUES ("%s", "%s", "%s", "%f","%s")""" % (checkInDate, postDate, content, ratingPoint, h_id)
        try:
        # 执行sql语句
            cursor.execute(sql)
        # 提交到数据库执行
            db.commit()
        except  Exception as e:
        # 如果发生错误则回滚
            print(e)
            db.rollback()
            print('error')

    except:
        pass


def close_db():
    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    for page in range(1, 10):
        # print('request...')
        string_data = request_data(page)
        # print('load json...')
        json_data = json.loads(string_data)
        comment_list = json_data['othersCommentList']
        if comment_list != []:
            for comment in comment_list:
                print(comment['checkInDate'], comment['postDate'],
                      comment['content'], comment['ratingPoint'])
                insert_data(comment['checkInDate'], comment['postDate'],
                            comment['content'], comment['ratingPoint'], hotel_id)
        else:
            break

    close_db()
