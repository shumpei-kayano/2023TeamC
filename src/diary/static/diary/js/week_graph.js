import Emotion
// データベースから取得したデータ
var data = {{ Emotion|safe }};

// ラベルと各感情のデータ
var labels = data.labels;
var positiveData = data.positive_data;
var negativeData = data.negative_data;
var neutralData = data.neutral_data;
var mixedData = data.mixed_data;

// 折れ線グラフの描画
var lineChartCanvas = document.getElementById("lineChart");
var lineChart = new Chart(lineChartCanvas, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [
            {
                label: 'ポジティブ',
                data: positiveData,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            },
            {
                label: 'ネガティブ',
                data: negativeData,
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,
                fill: false
            },
            {
                label: '中立',
                data: neutralData,
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 1,
                fill: false
            },
            {
                label: '混合',
                data: mixedData,
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1,
                fill: false
            }
        ]
    },
    options: {
        scales: {
            x: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: '日付'
                }
            }],
            y: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: '感情スコア'
                }
            }]
        }
    }
});
