area_dic = {'北海道/釧路':'014100',
            '北海道/旭川':'012000',
            '北海道/札幌':'016000',
            '青森県':'020000',
            '岩手県':'030000',
            '宮城県':'040000',
            '秋田県':'050000',
            '山形県':'060000',
            '福島県':'070000',
            '茨城県':'080000',
            '栃木県':'090000',
            '群馬県':'100000',
            '埼玉県':'110000',
            '千葉県':'120000',
            '東京都':'130000',
            '神奈川県':'140000',
            '新潟県':'150000',
            '富山県':'160000',
            '石川県':'170000',
            '福井県':'180000',
            '山梨県':'190000',
            '長野県':'200000',
            '岐阜県':'210000',
            '静岡県':'220000',
            '愛知県':'230000',
            '三重県':'240000',
            '滋賀県':'250000',
            '京都府':'260000',
            '大阪府':'270000',
            '兵庫県':'280000',
            '奈良県':'290000',
            '和歌山県':'300000',
            '鳥取県':'310000',
            '島根県':'320000',
            '岡山県':'330000',
            '広島県':'340000',
            '山口県':'350000',
            '徳島県':'360000',
            '香川県':'370000',
            '愛媛県':'380000',
            '高知県':'390000',
            '福岡県':'400000',
            '佐賀県':'410000',
            '長崎県':'420000',
            '熊本県':'430000',
            '大分県':'440000',
            '宮崎県':'450000',
            '鹿児島県':'460100',
            '沖縄県/那覇':'471000',
            '沖縄県/石垣':'474000'
}


function getLocation() {
  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(
      function(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        const geocoder = new google.maps.Geocoder();
        geocoder.geocode(
          {
            location: { lat: latitude, lng: longitude },
          },
          function(results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
              if (results[0]) {
                const addressComponents = results[0].address_components;
                let prefecture;

                // 住所コンポーネントから都道府県を抽出
                for (let i = 0; i < addressComponents.length; i++) {
                  const types = addressComponents[i].types;
                  if (types.includes("administrative_area_level_1")) {
                    prefecture = addressComponents[i].long_name;
                    break;
                  }
                }

                // フォーマットされた住所を構築
                const formattedAddress = `${prefecture}`;

                // フォーマットされた住所を解決するPromise
                resolve(formattedAddress);
              } else {
                // 結果が見つからない場合
                reject("Geocoder: No results found");
              }
            } else {
              // Geocoderエラー
              reject(`Geocoder error: ${status}`);
            }
          }
        );
      },
      function(error) {
        // Geolocationエラー
        reject(`Geolocation error: ${error.code}`);
      }
    );
  });
}

