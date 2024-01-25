import requests
from gps3 import gps3
from geopy.geocoders import Nominatim
import geopy.exc

def get_current_location():
    try:
        # GPS機能を使用して現在の位置情報を取得
        geolocator = Nominatim(user_agent="my_geocoder")
        location = geolocator.geocode("")

        if location:
            latitude, longitude = location.latitude, location.longitude
            return latitude, longitude
        else:
            raise geopy.exc.GeocoderTimedOut("Failed to get location.")
    except Exception as e:
        raise e

def get_address_from_location(latitude, longitude):
    try:
        # 緯度と経度から逆ジオコーディングで住所を取得
        geolocator = Nominatim(user_agent="my_geocoder")
        location = geolocator.reverse((latitude, longitude), language="ja")

        if location:
            address = location.address
            return address
        else:
            raise geopy.exc.GeocoderTimedOut("Failed to get address.")
    except Exception as e:
        raise e

def main():
    try:
        # 現在の位置情報を取得
        latitude, longitude = get_current_location()
        print(f"緯度: {latitude}, 経度: {longitude}")

        # 緯度と経度から住所を取得
        address = get_address_from_location(latitude, longitude)
        print("住所:", address)

    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    main()
geolocator = Nominatim(user_agent="my_geocoder")

# def get_location(api_key, latitude, longitude):
#     url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}&language=ja"

#     response = requests.get(url)
#     data = response.json()

#     if data["status"] == "OK":
#         # 一般的には最初の結果が最も詳細な情報を含みます
#         result = data["results"][0]

#         # 住所の取得
#         address = result["formatted_address"]

#         # 都道府県、市の情報を取得
#         components = result["address_components"]
#         prefecture = next((comp["long_name"] for comp in components if "administrative_area_level_1" in comp["types"]), None)
#         city = next((comp["long_name"] for comp in components if "locality" in comp["types"]), None)

#         return {
#             "address": address,
#             "prefecture": prefecture,
#             "city": city
#         }
#     else:
#         return None


# # APIキー、緯度、経度を設定
# api_key = "AIzaSyDummV9aw8Ned2gn7EwN-SgkIyuV0RdLSA"
# latitude = geolocator.latitude
# longitude = geolocator.longitude

# result = get_location(api_key, latitude, longitude)

# if result:
#     print("住所:", result["address"])
#     print("都道府県:", result["prefecture"])
#     print("市:", result["city"])
# else:
#     print("位置情報の取得に失敗しました。")