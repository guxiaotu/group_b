function initBar() {
    const c = echarts.init(document.getElementById("bar"));
    c.setOption({
        tooltip: {trigger: "axis"},
        xAxis: {type: "category", data: DATA.brands, axisLabel: {color: "#9fdcff"}},
        yAxis: {type: "value", axisLabel: {color: "#9fdcff"}},
        series: [{
            type: "bar",
            data: DATA.brand_sales,
            itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    {offset: 0, color: "#00e0ff"},
                    {offset: 1, color: "#0066ff"}
                ])
            }
        }]
    });
    return c;
}

function initPie() {
    const c = echarts.init(document.getElementById("pie"));
    c.setOption({
        tooltip: {trigger: "item"},
        legend: {textStyle: {color: "#9fdcff"}},
        series: [{
            type: "pie",
            radius: ["40%", "70%"],
            data: DATA.price_dist,
            label: {color: "#cfe8ff"}
        }]
    });
    return c;
}

function initLine() {
    const c = echarts.init(document.getElementById("line"));
    c.setOption({
        tooltip: {trigger: "axis"},
        xAxis: {type: "category", data: DATA.months, axisLabel: {color: "#9fdcff"}},
        yAxis: {type: "value", axisLabel: {color: "#9fdcff"}},
        series: [{
            type: "line",
            smooth: true,
            areaStyle: {},
            data: DATA.sales_trend,
            lineStyle: {color: "#00ffa3"},
            itemStyle: {color: "#00ffa3"}
        }]
    });
    return c;
}


function startClock() {
    const el = document.getElementById("clock");
    setInterval(() => {
        el.textContent = new Date().toLocaleString();
    }, 1000);
}

function autoScale() {
    const scale = Math.min(
        window.innerWidth / 1920,
        window.innerHeight / 1080
    );
    document.querySelector(".screen").style.transform = `scale(${scale})`;
    window.addEventListener("resize", autoScale);
}

window.addEventListener("DOMContentLoaded", () => {
    initBar();
    initPie();
    initLine();
    startClock();
    autoScale();
});