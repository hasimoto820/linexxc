# モジュールのインポート
import json
import urllib.request
import ssl

#認証方法をTLSv1に指定
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

# API に渡すパラメータの値の指定
# https://api.gnavi.co.jp/api/manual/restsearch/
# https://api.gnavi.co.jp/api/tools/     #ここでAPIのテストができる
base_url = "https://api.gnavi.co.jp/RestSearchAPI/v3/"

key = '90dc4b25c570c60b83ebefe5d98aedcc'

##### 上記の key は、ぐるなびAPI のアカウントを作成した際、取得したkeyidを指定
# shop_name = "焼肉"　#店名も含める場合はコメントアウト外す
g_code = 'RSFST03001' # 寿司のコード
address = '那覇'
# API を使う関数の定義
def gnavi_api(g_code,address):
    params = urllib.parse.urlencode({
        'keyid': key,
        # 'name' : shop_name,　#店名も含める場合はコメントアウト外す
        'category_s' : g_code,
        'address' : address
    })
    url = base_url + '?' + params
    print(url)
    response = urllib.request.urlopen(url,context=context)
    return response.read()

# 関数を使って、API から情報を取得
data = gnavi_api(g_code,address)

# 取得した情報をJSON形式から辞書型に変換
read_data = json.loads(data)["rest"]

# お店の名前の一覧を格納する list の作成
list_name = []

# お店ごとにループし、お店の名前を list に追加する関数の定義
def get_name(read_data):
    for dic in read_data:
        list_name.append(dic.get("name"))
        #list_name.append(dic.get("address")) #住所を取得したい場合はこちら
    return list_name

# 関数を実行し、お店の名前の list を取得
get_name(read_data)

print(list_name)
