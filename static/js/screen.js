// ============ 地图注册 ============
let chinaGeoLoaded = false;

async function registerChinaMap() {
  if (chinaGeoLoaded) return;
  const res = await fetch('/static/js/china.json');
  const geoJson = await res.json();
  echarts.registerMap('china', geoJson);
  chinaGeoLoaded = true;
}

// ============ 柱状图 ============
function initBar() {
  const c = echarts.init(document.getElementById('bar'));
  c.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: DATA.brands,
      axisLabel: { color: '#9fdcff', rotate: 30 }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#9fdcff' },
      splitLine: { lineStyle: { color: 'rgba(31,58,95,0.3)' } }
    },
    series: [{
      type: 'bar',
      data: DATA.brand_sales,
      barWidth: '40%',
      itemStyle: {
        borderRadius: [4, 4, 0, 0],
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#00e0ff' },
          { offset: 1, color: '#0066ff' }
        ])
      }
    }]
  });
  return c;
}

// ============ 饼图 ============
function initPie() {
  const c = echarts.init(document.getElementById('pie'));
  c.setOption({
    tooltip: { trigger: 'item' },
    legend: {
      textStyle: { color: '#9fdcff' },
      bottom: 0
    },
    series: [{
      type: 'pie',
      radius: ['35%', '65%'],
      center: ['50%', '45%'],
      avoidLabelOverlap: true,
      itemStyle: { borderRadius: 6, borderColor: '#050b18', borderWidth: 2 },
      label: { color: '#cfe8ff', fontSize: 11 },
      data: DATA.price_dist
    }]
  });
  return c;
}

// ============ 折线图 ============
function initLine() {
  const c = echarts.init(document.getElementById('line'));
  c.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: DATA.months,
      axisLabel: { color: '#9fdcff' }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#9fdcff' },
      splitLine: { lineStyle: { color: 'rgba(31,58,95,0.3)' } }
    },
    series: [{
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: { color: '#00ffa3', width: 3 },
      itemStyle: { color: '#00ffa3' },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(0,255,163,0.4)' },
          { offset: 1, color: 'rgba(0,255,163,0.0)' }
        ])
      },
      data: DATA.sales_trend
    }]
  });
  return c;
}

// ============ 地图（含散点 + 飞线） ============
async function initMap() {
  await registerChinaMap();

  const c = echarts.init(document.getElementById('map'));

  // 城市坐标映射（飞线用）
  const cityCoords = {
    '广东': [113.2, 23.1],
    '浙江': [120.1, 30.3],
    '江苏': [118.8, 32.0],
    '上海': [121.5, 31.2],
    '北京': [116.4, 39.9],
    '四川': [104.1, 30.7],
    '湖北': [114.3, 30.6],
    '福建': [119.3, 26.1]
  };

  // 飞线数据：从各省飞向北京（示例）
  const linesData = DATA.map_points
    .filter(p => p.name !== '北京')
    .map(p => ({
      fromName: p.name,
      toName: '北京',
      coords: [cityCoords[p.name] || [116.4, 39.9], cityCoords['北京']]
    }));

  c.setOption({
    tooltip: { trigger: 'item', formatter: '{b}<br/>销量: {c}' },
    visualMap: {
      min: 0,
      max: 10000,
      left: 'left',
      bottom: '10%',
      text: ['高', '低'],
      textStyle: { color: '#9fdcff' },
      calculable: true,
      inRange: { color: ['#0b1f3a', '#1e90ff', '#00e0ff', '#00ffa3'] }
    },
    geo: {
      map: 'china',
      roam: false,
      zoom: 1.2,
      center: [104.5, 36],
      label: { show: false, color: '#fff' },
      itemStyle: {
        areaColor: 'rgba(20,60,120,0.6)',
        borderColor: '#1e90ff',
        borderWidth: 1
      },
      emphasis: {
        itemStyle: { areaColor: 'rgba(30,144,255,0.8)' },
        label: { show: true, color: '#fff' }
      }
    },
    series: [
      // 散点（城市圆点）
      {
        type: 'effectScatter',
        coordinateSystem: 'geo',
        data: DATA.map_points.map(p => ({
          name: p.name,
          value: [...(cityCoords[p.name] || [116.4, 39.9]), p.value]
        })),
        symbolSize: function (val) { return Math.max(val[2] / 500, 6); },
        rippleEffect: { brushType: 'stroke', scale: 4 },
        itemStyle: { color: '#00e0ff', shadowBlur: 10, shadowColor: '#00e0ff' },
        zlevel: 2
      },
      // 飞线
      {
        type: 'lines',
        coordinateSystem: 'geo',
        zlevel: 1,
        effect: {
          show: true,
          period: 4,
          trailLength: 0.3,
          symbol: 'arrow',
          symbolSize: 6
        },
        lineStyle: {
          color: '#00ffa3',
          width: 1.5,
          opacity: 0.4,
          curveness: 0.3
        },
        data: linesData
      }
    ]
  });

  return c;
}

// ============ 时钟 ============
function startClock() {
  const el = document.getElementById('clock');
  const tick = () => {
    el.textContent = new Date().toLocaleString('zh-CN');
  };
  tick();
  setInterval(tick, 1000);
}

// ============ 大屏自适应 ============
function autoScale() {
  const scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
  document.querySelector('.screen').style.transform = `scale(${scale})`;
}

// ============ 启动 ============
window.addEventListener('DOMContentLoaded', async () => {
  const charts = [];

  charts.push(initBar());
  charts.push(initPie());
  charts.push(initLine());
  charts.push(await initMap());

  startClock();
  autoScale();

  window.addEventListener('resize', () => {
    autoScale();
    charts.forEach(c => c.resize());
  });
});