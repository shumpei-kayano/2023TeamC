import requests
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_geocoder")

location = geolocator.geocode("東京タワー")
print("緯度:", location.latitude)
print("経度:", location.longitude)

def get_location(api_key, latitude, longitude):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}&language=ja"

    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        # 一般的には最初の結果が最も詳細な情報を含みます
        result = data["results"][0]

        # 住所の取得
        address = result["formatted_address"]

        # 都道府県、市の情報を取得
        components = result["address_components"]
        prefecture = next((comp["long_name"] for comp in components if "administrative_area_level_1" in comp["types"]), None)
        city = next((comp["long_name"] for comp in components if "locality" in comp["types"]), None)

        return {
            "address": address,
            "prefecture": prefecture,
            "city": city
        }
    else:
        return None

# APIキー、緯度、経度を設定
api_key = "AIzaSyDummV9aw8Ned2gn7EwN-SgkIyuV0RdLSA"
latitude = # 現在位置の緯度
longitude = # 現在位置の経度

result = get_location(api_key, latitude, longitude)

if result:
    print("住所:", result["address"])
    print("都道府県:", result["prefecture"])
    print("市:", result["city"])
else:
    print("位置情報の取得に失敗しました。")