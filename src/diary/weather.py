import datetime
import urllib.request
from bs4 import BeautifulSoup
# import location


# 過去の天気を取得する関数
def past_date(date,area):
    # エリアコードリスト
    area_dic = {'大分市':[47815,83],
    '福岡市':[47807,82]}
    
    # エリアコードを辞書から取得
    area_list = area_dic.get(area, [])
    areacode, code = area_list[0], area_list[1]

    # 対象url(エリアコードを位置情報で変更)
    url = "https://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?" \
        "prec_no=%d&block_no=%d&year=%d&month=%d&day=%d&view=" % (code,areacode,date.year, date.month, date.day)
    
    # 気象データのページを取得
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    trs = soup.find("table", {"class": "data2_s"})
    
    # table の中身を取得
    for tr in trs.findAll('tr')[2:]:
        tds = tr.findAll('td')

        # tds が空の場合はスキップ
        if not tds:
            continue
        
        # 日付を取得
        day=tds[0].string
        
        # creade_dataの日にち(date.day)と一致したら気温を取得
        if day==str(date.day):
            # 気温を取得。取得できない場合はNoneを返す
            value = tds[6].string if tds[6].string else None
            # 天気を取得して1文字目を返す。
            value2 = tds[19].string[0] if tds[20].string else None
            # 関数から値を返す
            return value, value2
        
# データ取得(create_data)
date = datetime.date(2024, 1, 2)

# 位置情報からエリアを取得
area='福岡市'

# 過去の日記を取得する関数(dateはcreate_data)
# temperature:気温、weather:天気
temperature,weather=past_date(date,area)

# 取得したデータを表示（テスト）
print(temperature)
print(weather)