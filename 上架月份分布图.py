#!/usr/bin/env python3
"""上架月份分布图：读取真实 Excel，生成可离线打开的 ECharts 图表。

安装：python -m pip install -r requirements.txt
运行：python 上架月份分布图.py "苹果手机壳行业数据.xlsx"
"""

import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

KIND = "launch"
TITLE = "上架月份分布图"


def numeric(series):
    return pd.to_numeric(
        series.astype(str).str.replace(r"[,，$￥¥\s]", "", regex=True), errors="coerce"
    ).replace([np.inf, -np.inf], np.nan)


def require(df, columns):
    absent = [c for c in columns if c not in df.columns]
    if absent:
        raise ValueError(f"工作表缺少字段：{absent}")


def launch_data(path):
    df = pd.read_excel(path, sheet_name="US")
    df.columns = df.columns.astype(str).str.strip()
    require(df, ["ASIN", "上架时间"])
    raw_count = len(df)
    df["ASIN"] = df["ASIN"].astype("string").str.strip().replace("", pd.NA)
    if df["ASIN"].isna().any():
        raise ValueError("存在空 ASIN，请先核对商品标识。")
    df["上架时间"] = pd.to_datetime(df["上架时间"], errors="coerce")
    conflict = df.groupby("ASIN")["上架时间"].nunique(dropna=False).gt(1)
    if conflict.any():
        raise ValueError(
            f"同一 ASIN 的上架时间冲突：{conflict[conflict].index.tolist()}"
        )
    df = df.drop_duplicates("ASIN").copy()
    total = len(df)
    missing = int(df["上架时间"].isna().sum())
    valid = df.dropna(subset=["上架时间"])
    if valid.empty:
        raise ValueError("没有可解析的上架日期。")
    periods = valid["上架时间"].dt.to_period("M")
    full_range = pd.period_range(periods.min(), periods.max(), freq="M")
    counts = periods.value_counts().reindex(full_range, fill_value=0).sort_index()
    result = pd.DataFrame(
        {"月份": counts.index.astype(str), "商品数量": counts.to_numpy()}
    )
    result["样本占比(%)"] = result["商品数量"] / len(valid) * 100
    result["样本累计数量"] = result["商品数量"].cumsum()
    assert result["商品数量"].sum() == len(valid)
    assert np.isclose(result["样本占比(%)"].sum(), 100)
    meta = {
        "source": Path(path).name,
        "sheet": "US",
        "raw": raw_count,
        "count": total,
        "duplicates": raw_count - total,
        "missing": missing,
        "valid": len(valid),
        "first": str(periods.min()),
        "last": str(periods.max()),
    }
    return result, meta


def brand_data(path):
    df = pd.read_excel(path, sheet_name="Brands")
    df.columns = df.columns.astype(str).str.strip()
    require(df, ["品牌", "月销量", "月销售额($)"])
    df["品牌"] = df["品牌"].astype("string").str.strip().replace("", pd.NA)
    if df["品牌"].isna().any() or df["品牌"].duplicated().any():
        raise ValueError("品牌名称缺失或重复，请先核对 Brands 工作表。")
    for col in ["月销量", "月销售额($)"]:
        df[col] = numeric(df[col])
        if df[col].isna().any() or df[col].lt(0).any():
            raise ValueError(f"{col} 含缺失或负值，不能完整计算品牌集中度。")
        if df[col].sum() <= 0:
            raise ValueError(f"{col} 合计必须大于 0。")
    result = df[["品牌", "月销量", "月销售额($)"]].copy()
    # 不使用已四舍五入的“市场份额”列，从原始总量重新计算。
    for col, prefix in [("月销量", "销量"), ("月销售额($)", "销售额")]:
        ranked = result.sort_values([col, "品牌"], ascending=[False, True]).copy()
        ranked[prefix + "排名"] = np.arange(1, len(ranked) + 1)
        ranked[prefix + "占比(%)"] = ranked[col] / ranked[col].sum() * 100
        ranked[prefix + "累计占比(%)"] = ranked[prefix + "占比(%)"].cumsum()
        for field in [prefix + "排名", prefix + "占比(%)", prefix + "累计占比(%)"]:
            result[field] = ranked[field]
        assert np.isclose(ranked[prefix + "占比(%)"].sum(), 100)
        assert np.isclose(ranked[prefix + "累计占比(%)"].iloc[-1], 100)
    result = result.sort_values("销量排名")
    return result, {
        "source": Path(path).name,
        "sheet": "Brands",
        "count": len(result),
        "sales_total": float(result["月销量"].sum()),
        "revenue_total": float(result["月销售额($)"].sum()),
    }


PAGE = r"""<!DOCTYPE html><html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__PAGE_TITLE__</title>__LIBRARY__
<style>
*{box-sizing:border-box}body{margin:0;background:#fff;color:#404751;font:14px -apple-system,BlinkMacSystemFont,"Microsoft YaHei",sans-serif}
main{max-width:1550px;margin:0 auto;padding:30px 36px}h1{font-size:25px;font-weight:600;margin:0 0 10px}.sub{font-size:13px;color:#818894;line-height:1.8}
.controls{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:22px 0 6px}select,button{font:inherit;padding:8px 13px;color:#5e6570;background:#fff;border:1px solid #dbe0e8;border-radius:6px;cursor:pointer}
label{font-size:13px;color:#757d89}.summary{margin-left:auto;font-size:13px;color:#85621e}.chart-wrap{overflow-x:auto}#chart{height:590px;min-width:680px;width:100%}
.notes{font-size:12px;color:#7b8491;line-height:1.9;border-top:1px solid #e8ecf1;padding-top:15px;margin:10px 0 0}details{margin-top:16px}summary{cursor:pointer;font-size:13px;color:#737d88}.table-wrap{max-height:320px;overflow:auto;margin-top:10px}table{border-collapse:collapse;width:100%;font-size:12px}th,td{padding:9px 12px;text-align:right;border-bottom:1px solid #edf0f4;white-space:nowrap}th{position:sticky;top:0;background:#fafbfc}th:first-child,td:first-child{text-align:left}
@media(max-width:720px){main{padding:22px 14px}h1{font-size:21px}.summary{margin-left:0;width:100%}#chart{height:530px}}
</style></head><body><main>
<h1>__PAGE_TITLE__</h1><div class="sub" id="subtitle"></div>
<div class="controls">__CONTROLS__<span class="summary" id="summary"></span></div>
<div class="chart-wrap"><div id="chart"></div></div>
<p class="notes" id="notes"></p>
<details><summary>查看当前分组数据</summary><div class="table-wrap" id="table"></div></details>
</main><script>
const rows=__DATA__,meta=__META__;
const $=id=>document.getElementById(id);
const format=(value,digits=2)=>Number(value).toLocaleString('zh-CN',{maximumFractionDigits:digits});
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function table(headers,records){$('table').innerHTML='<table><thead><tr>'+headers.map(v=>'<th>'+escapeHTML(v)+'</th>').join('')+'</tr></thead><tbody>'+records.map(r=>'<tr>'+r.map(v=>'<td>'+escapeHTML(v)+'</td>').join('')+'</tr>').join('')+'</tbody></table>';}
if(typeof echarts==='undefined'){$('chart').textContent='图表库加载失败，请将 echarts.min.js 放在 Python 文件旁并重新运行。';throw Error('ECharts not loaded');}
const chart=echarts.init($('chart'));
const axis={axisLine:{show:true,lineStyle:{color:'#d8dde7'}},axisTick:{show:false},axisLabel:{color:'#7b8490',fontSize:13},nameTextStyle:{color:'#7b8490',fontSize:13},nameGap:20};
const base={backgroundColor:'#ffffff',animationDuration:350,color:['#ffac26','#5ca5f9'],grid:{left:92,right:90,top:82,bottom:130},
 legend:{top:14,left:'center',textStyle:{color:'#636b75',fontSize:15},itemGap:25},
 toolbox:{top:8,right:2,feature:{saveAsImage:{title:'保存图片',name:'__PAGE_TITLE__',pixelRatio:2}}},
 tooltip:{trigger:'axis',confine:true,axisPointer:{type:'shadow'},backgroundColor:'rgba(255,255,255,.97)',borderColor:'#e5e9ef'},
 dataZoom:[{type:'slider',bottom:8,height:28,borderColor:'#dce1e9',backgroundColor:'#f4f6f9',fillerColor:'rgba(156,173,196,.22)'},{type:'inside',zoomOnMouseWheel:false}],
 xAxis:{...axis,type:'category',boundaryGap:true},
 yAxis:{...axis,type:'value',min:0,minInterval:1,splitLine:{lineStyle:{color:'#dce1e9',type:'dashed'}}}};
__CHART_CODE__
window.addEventListener('resize',()=>chart.resize());
</script></body></html>"""

LAUNCH_JS = r"""
$('subtitle').textContent=`${meta.source} / US · ${meta.valid} 款具有有效上架日期的样本商品 · ${meta.first} 至 ${meta.last}`;
$('notes').textContent=`口径：按上架日期统计当前样本中的商品数量，不是浏览量，也不是历史逐月销量或全市场新品总量。原始 ${meta.raw} 条，去除 ${meta.duplicates} 条重复 ASIN，${meta.missing} 款日期缺失未纳入。空月份表示本样本没有商品在该月上架。默认展示最近 24 个月；最新月份可能不完整，可拖动下方滑块查看全部记录。`;
function render(){
 const period=$('period').value;
 const grouped=new Map();
 rows.forEach(r=>{let key=r['月份'];if(period==='quarter')key=key.slice(0,4)+' Q'+(Math.floor((Number(key.slice(5))-1)/3)+1);if(period==='year')key=key.slice(0,4);grouped.set(key,(grouped.get(key)||0)+r['商品数量']);});
 const data=[...grouped].map(([date,count])=>({date,count}));
 const showAll=$('range').value==='all';
 const windowSize=period==='month'?24:period==='quarter'?8:2;
 const first=showAll?0:Math.max(0,data.length-windowSize);
 const visible=data.slice(first).reduce((sum,r)=>sum+r.count,0);
 $('summary').textContent=`${showAll?'全部时段':'初始显示区间'}：${format(visible,0)} 款，占有效日期样本 ${format(visible/meta.valid*100)}%`;
 chart.setOption({...base,
   legend:{...base.legend,data:['上架商品数量（样本）']},
   xAxis:{...base.xAxis,data:data.map(r=>r.date),axisLabel:{color:'#7b8490',rotate:55,hideOverlap:true}},
   yAxis:{...base.yAxis,name:'商品数量（款）'},
   dataZoom:base.dataZoom.map(z=>({...z,startValue:first,endValue:data.length-1})),
   tooltip:{...base.tooltip,formatter:params=>{const r=data[params[0].dataIndex];return `<b>${escapeHTML(r.date)}</b><br>上架商品：${format(r.count,0)} 款<br>占有效日期样本：${format(r.count/meta.valid*100)}%`;}},
   series:[{name:'上架商品数量（样本）',type:'line',data:data.map(r=>r.count),smooth:0.18,showSymbol:false,symbol:'emptyCircle',symbolSize:7,lineStyle:{width:3,color:'#ffac26'},itemStyle:{color:'#ffac26'}}]
 },true);
 table([period==='month'?'月份':period==='quarter'?'季度':'年份','商品数量（款）','样本占比（%）'],data.map(r=>[r.date,r.count,format(r.count/meta.valid*100)]));
}
$('period').onchange=render;$('range').onchange=render;render();
"""

BRAND_JS = r"""
$('subtitle').textContent=`${meta.source} / Brands · ${meta.count} 个品牌 · 月度销售快照`;
$('notes').textContent='柱形按当前指标由高到低排列，折线表示从第 1 名到该名次的累计占比；分母始终是 Brands 表全部品牌总量，切换 Top 10 / Top 20 不改变分母。CR3、CR5、CR10 分别为前 3、5、10 个品牌合计占比。占比由原始销量或销售额重新计算，不直接累加原表已舍入的“市场份额”。这是一份样本的品牌集中度分析，不代表全行业市场份额。';
function render(){
 const key=$('metric').value;
 const prefix=key==='月销量'?'销量':'销售额';
 const rankKey=prefix+'排名';
 const unit=key==='月销量'?'件':'美元';
 const total=rows.reduce((sum,r)=>sum+r[key],0);
 const sorted=[...rows].sort((a,b)=>a[rankKey]-b[rankKey]);
 let cumulative=0;const all=sorted.map(r=>{const share=r[key]/total*100;cumulative+=share;return {...r,share,cumulative};});
 const top=$('top').value==='all'?all.length:Number($('top').value);
 const data=all.slice(0,top);
 const cr=n=>all[Math.min(n,all.length)-1].cumulative;
 $('summary').textContent=`CR3 ${format(cr(3))}% · CR5 ${format(cr(5))}% · CR10 ${format(cr(10))}%`;
 const seriesName=key==='月销量'?'月销量':'月销售额';
 chart.setOption({...base,
   legend:{...base.legend,data:[seriesName,'累计占比']},
   xAxis:{...base.xAxis,data:data.map(r=>r['品牌']),axisLabel:{color:'#7b8490',rotate:35,hideOverlap:true,fontSize:12}},
   yAxis:[{...base.yAxis,name:`${seriesName}（${unit}）`,axisLabel:{color:'#7b8490',formatter:value=>value>=10000?format(value/10000)+'万':format(value,0)}},
          {...axis,type:'value',name:'累计占比',position:'right',min:0,max:100,interval:20,axisLabel:{color:'#7b8490',formatter:'{value}%'},splitLine:{show:false}}],
   dataZoom:base.dataZoom.map(z=>({...z,start:0,end:100})),
   tooltip:{...base.tooltip,formatter:params=>{const r=data[params[0].dataIndex];return `<b>${escapeHTML(r['品牌'])}</b><br>排名：${r[rankKey]}<br>${seriesName}：${format(r[key],0)} ${unit}<br>品牌占比：${format(r.share)}%<br>累计占比：${format(r.cumulative)}%`;}},
   series:[{name:seriesName,type:'bar',yAxisIndex:0,data:data.map(r=>r[key]),barMaxWidth:50,itemStyle:{color:'#ffac26'}},
           {name:'累计占比',type:'line',yAxisIndex:1,data:data.map(r=>r.cumulative),smooth:false,symbol:'emptyCircle',symbolSize:6,lineStyle:{width:2.5,color:'#5ca5f9'},itemStyle:{color:'#5ca5f9'},markLine:{silent:true,symbol:'none',label:{formatter:'80%',color:'#9ca5b3',position:'insideEndTop'},lineStyle:{color:'#c2cad6',type:'dashed'},data:[{yAxis:80}]}}]
 },true);
 table(['排名','品牌',`${seriesName}（${unit}）`,'品牌占比（%）','累计占比（%）'],data.map(r=>[r[rankKey],r['品牌'],format(r[key],0),format(r.share),format(r.cumulative)]));
}
$('metric').onchange=render;$('top').onchange=render;render();
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("excel", nargs="?", default="苹果手机壳行业数据.xlsx")
    parser.add_argument("--out", default=TITLE + ".html")
    parser.add_argument("--echarts", type=Path, help="可选：ECharts 本地库路径")
    args = parser.parse_args()
    data, meta = launch_data(args.excel) if KIND == "launch" else brand_data(args.excel)
    library = args.echarts or Path(__file__).with_name("echarts.min.js")
    if not library.is_file():
        raise FileNotFoundError(
            "未找到 echarts.min.js；请完整解压实现包，或用 --echarts 指定本地库。"
        )
    lib_text = library.read_text(encoding="utf-8").replace("</script", r"<\/script")
    if KIND == "launch":
        controls = '<label for="period">时间粒度</label><select id="period"><option value="month">按月</option><option value="quarter">按季度</option><option value="year">按年</option></select><label for="range">初始范围</label><select id="range"><option value="recent">最近时段（24月 / 8季 / 2年）</option><option value="all">全部时段</option></select>'
        chart_code = LAUNCH_JS
    else:
        controls = '<label for="metric">分析指标</label><select id="metric"><option value="月销量">月销量</option><option value="月销售额($)">月销售额</option></select><label for="top">展示品牌</label><select id="top"><option value="10">Top 10</option><option value="20">Top 20</option><option value="all">全部品牌</option></select>'
        chart_code = BRAND_JS
    page = PAGE.replace("__PAGE_TITLE__", TITLE).replace(
        "__LIBRARY__", "<script>" + lib_text + "</script>"
    )
    page = page.replace("__CONTROLS__", controls).replace("__CHART_CODE__", chart_code)
    page = page.replace(
        "__DATA__",
        data.to_json(orient="records", force_ascii=False, double_precision=12).replace(
            "</", "<\\/"
        ),
    )
    page = page.replace(
        "__META__", json.dumps(meta, ensure_ascii=False).replace("</", "<\\/")
    )
    output = Path(args.out).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    data.to_csv(
        output.with_name(output.stem + "_分析数据.csv"),
        index=False,
        encoding="utf-8-sig",
        float_format="%.8f",
    )
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    print(f"已生成：{output}")


if __name__ == "__main__":
    main()
