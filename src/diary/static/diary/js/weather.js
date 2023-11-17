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
const weatherCode = {
  100: ["weather2.png", "晴れ"],
  101: ["weather2.png", "晴れ時々曇り"],
  102: ["weather2.png",  "晴れ一時雨"],
  103: ["weather2.png",  "晴れ時々雨"],
  104: ["weather2.png",  "晴れ一時雪"],
  105: ["weather2.png",  "晴れ時々雪"],
  106: ["weather2.png",  "晴れ一時雨か雪"],
  107: ["weather2.png",  "晴れ時々雨か雪"],
  108: ["weather2.png",  "晴れ一時雨か雷雨"],
  110: ["weather2.png",  "晴れ後時々曇り"],
  111: ["weather2.png",  "晴れ後曇り"],
  112: ["weather2.png",  "晴れ後一時雨"],
  113: ["weather2.png",  "晴れ後時々雨"],
  114: ["weather2.png",  "晴れ後雨"],
  115: ["weather2.png",  "晴れ後一時雪"],
  116: ["weather2.png",  "晴れ後時々雪"],
  117: ["weather2.png",  "晴れ後雪"],
  118: ["weather2.png",  "晴れ後雨か雪"],
  119: ["weather2.png",  "晴れ後雨か雷雨"],
  120: ["weather2.png",  "晴れ朝夕一時雨"],
  121: ["weather2.png",  "晴れ朝の内一時雨"],
  122: ["weather2.png",  "晴れ夕方一時雨"],
  123: ["weather2.png",  "晴れ山沿い雷雨"],
  124: ["weather2.png",  "晴れ山沿い雪"],
  125: ["weather2.png",  "晴れ午後は雷雨"],
  126: ["weather2.png",  "晴れ昼頃から雨"],
  127: ["weather2.png",  "晴れ夕方から雨"],
  128: ["weather2.png",  "晴れ夜は雨"],
  130: ["weather2.png",  "朝の内霧後晴れ"],
  131: ["weather2.png",  "晴れ明け方霧"],
  132: ["weather2.png",  "晴れ朝夕曇り"],
  140: ["weather2.png",  "晴れ時々雨と雷"],
  160: ["weather2.png",  "晴れ一時雪か雨"],
  170: ["weather2.png",  "晴れ時々雪か雨"],
  181: ["weather2.png",  "晴れ後雪か雨"],
  200: ["weather4.png", "曇り"],
  201: ["weather4.png",  "曇り時々晴れ"],
  202: ["weather4.png",  "曇り一時雨"],
  203: ["weather4.png",  "曇り時々雨"],
  204: ["weather4.png",  "曇り一時雪"],
  205: ["weather4.png",  "曇り時々雪"],
  206: ["weather4.png",  "曇り一時雨か雪"],
  207: ["weather4.png",  "曇り時々雨か雪"],
  208: ["weather4.png",  "曇り一時雨か雷雨"],
  209: ["weather4.png", "霧"],
  210: ["weather4.png",  "曇り後時々晴れ"],
  211: ["weather4.png",  "曇り後晴れ"],
  212: ["weather4.png",  "曇り後一時雨"],
  213: ["weather4.png",  "曇り後時々雨"],
  214: ["weather4.png",  "曇り後雨"],
  215: ["weather4.png", "曇り後一時雪"],
  216: ["weather4.png", "曇り後時々雪"],
  217: ["weather4.png", "曇り後雪"],
  218: ["weather4.png",  "曇り後雨か雪"],
  219: ["weather4.png",  "曇り後雨か雷雨"],
  220: ["weather4.png",  "曇り朝夕一時雨"],
  221: ["weather4.png",  "曇り朝の内一時雨"],
  222: ["weather4.png",  "曇り夕方一時雨"],
  223: ["weather4.png",  "曇り日中時々晴れ"],
  224: ["weather4.png",  "曇り昼頃から雨"],
  225: ["weather4.png",  "曇り夕方から雨"],
  226: ["weather4.png",  "曇り夜は雨"],
  228: ["weather4.png", "曇り昼頃から雪"],
  229: ["weather4.png", "曇り夕方から雪"],
  230: ["weather4.png", "曇り夜は雪"],
  231: ["weather4.png", "曇り海岸霧か霧雨"],
  240: ["weather4.png",  "曇り時々雨と雷"],
  250: ["weather4.png",  "曇り時々雪と雷"],
  260: ["weather4.png",  "曇り一時雪か雨"],
  270: ["weather4.png",  "曇り時々雪か雨"],
  281: ["weather4.png", "曇り後雪か雨"],
  300: ["weather1.png", , "雨"],
  301: ["weather1.png","雨時々晴れ"],
  302: ["weather1.png", "雨時々止む"],
  303: ["weather1.png", "雨時々雪"],
  304: ["weather1.png", , "雨か雪"],
  306: ["weather1.png", , "大雨"],
  308: ["weather1.png", "雨で暴風を伴う"],
  309: ["weather1.png", "雨一時雪"],
  311: ["weather1.png", "雨後晴れ"],
  313: ["weather1.png","雨後曇り"],
  314: ["weather1.png", "雨後時々雪"],
  315: ["weather1.png", "雨後雪"],
  316: ["weather1.png", "雨か雪後晴れ"],
  317: ["weather1.png","雨か雪後曇り"],
  320: ["weather1.png", "朝の内雨後晴れ"],
  321: ["weather1.png","朝の内雨後曇り"],
  322: ["weather1.png", "雨朝晩一時雪"],
  323: ["weather1.png", "雨昼頃から晴れ"],
  324: ["weather1.png", "雨夕方から晴れ"],
  325: ["weather1.png", "雨夜は晴れ"],
  326: ["weather1.png", "雨夕方から雪"],
  327: ["weather1.png", "雨夜は雪"],
  328: ["weather1.png", "雨一時強く降る"],
  329: ["weather1.png", "雨一時みぞれ"],
  340: ["weather1.png", "雪か雨"],
  350: ["weather1.png", "雨で雷を伴う"],
  361: ["weather3.png", "雪か雨後晴れ"],
  371: ["weather3.png", "雪か雨後曇り"],
  400: ["weather3.png", "雪"],
  401: ["weather3.png", "雪時々晴れ"],
  402: ["weather3.png", "雪時々止む"],
  403: ["weather3.png", "雪時々雨"],
  405: ["weather3.png", "大雪"],
  406: ["weather3.png", "風雪強い"],
  407: ["weather3.png", "暴風雪"],
  409: ["weather3.png", "雪一時雨"],
  411: ["weather3.png", "雪後晴れ"],
  413: ["weather3.png", "雪後曇り"],
  414: ["weather3.png", "雪後雨"],
  420: ["weather3.png", "朝の内雪後晴れ"],
  421: ["weather3.png", "朝の内雪後曇り"],
  422: ["weather3.png", "雪昼頃から雨"],
  423: ["weather3.png", "雪夕方から雨"],
  425: ["weather3.png", "雪一時強く降る"],
  426: ["weather3.png", "雪後みぞれ"],
  427: ["weather3.png", "雪一時みぞれ"],
  450: ["weather3.png", "雪で雷を伴う"],
};

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

                // 成功時に結果をresolveするPromise
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

async function getareacode() {
  const location = await getLocation();//async function内でPromiseの結果（resolve、reject）が返されるまで待機する（処理を一時停止する）
  const areacode = area_dic[location];
  return areacode;//エリアコードが返ってくる
}

async function main() {
  const areacode = await getareacode();
  const url = `https://www.jma.go.jp/bosai/forecast/data/forecast/${areacode}.json`;
  console.log(url)
  return url;
}


const dayList = ["日", "月", "火", "水", "木", "金", "土"];

const timeDefinesList = new Array();
const weatherCodeList = new Array();
const tempsMinList = new Array();
const tempsMaxList = new Array();

main().then(url =>{
// JSON取得
fetch(url)
  .then(function (response) {
    return response.json();
  })
  .then(function (weather) {
    document
      .getElementById("location")
      .prepend(
        `${weather[1].publishingOffice}: ${weather[1].timeSeries[0].areas[0].area.name} `
      );
    const isTodaysData = weather[0].timeSeries[2].timeDefines.length === 4;
    const weatherCodes = weather[0].timeSeries[0].areas[0].weatherCodes;
    const timeDefines = weather[0].timeSeries[0].timeDefines;
    const temps = weather[0].timeSeries[2].areas[0].temps;
    weatherCodeList.push(weatherCodes[0], weatherCodes[1]);
    timeDefinesList.push(timeDefines[0], timeDefines[1]);
    if (isTodaysData) {
      tempsMinList.push(temps[0] === temps[1] ? "--" : temps[0], temps[2]);
      tempsMaxList.push(temps[1], temps[3]);
    } else {
      tempsMinList.push("--", temps[0]);
      tempsMaxList.push("--", temps[1]);
    }

    const startCount =
      weather[1].timeSeries[0].timeDefines.indexOf(timeDefines[1]) + 1;
    for (let i = startCount; i < startCount + 5; i++) {
      weatherCodeList.push(weather[1].timeSeries[0].areas[0].weatherCodes[i]);
      timeDefinesList.push(weather[1].timeSeries[0].timeDefines[i]);
      tempsMinList.push(weather[1].timeSeries[1].areas[0].tempsMin[i]);
      tempsMaxList.push(weather[1].timeSeries[1].areas[0].tempsMax[i]);
    }

    const date = document.getElementsByClassName("date");
    const weatherImg = document.getElementsByClassName("weatherImg");
    const weatherTelop = document.getElementsByClassName("weatherTelop");
    const tempMin = document.getElementsByClassName("tempMin");
    const tempMax = document.getElementsByClassName("tempMax");

    weatherCodeList.forEach(function (el, i) {
      let dt = new Date(timeDefinesList[i]);
      let weekdayCount = dt.getDay();
      if (weekdayCount === 0) date[i].style.color = "red";
      if (weekdayCount === 6) date[i].style.color = "blue";
      var m = ("00" + (dt.getMonth() + 1)).slice(-2);
      var d = ("00" + dt.getDate()).slice(-2);
      date[i].textContent = `${m}/${d}(${dayList[weekdayCount]})`;
      
      weatherImg[i].src = STATIC_URL + weatherCode[el][0];


      weatherTelop[i].textContent = weatherCode[el][1];//晴れ後雨等
      tempMin[i].textContent = tempsMinList[i] + "℃";
      tempMax[i].textContent = tempsMaxList[i] + "℃";
    });
  });
});