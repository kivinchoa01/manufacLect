#!/usr/bin/env python3
"""Final version based on extracted content markdown."""
import sys, re
from pathlib import Path
from PIL import Image

FIG_DIR = Path("figures")
CH_START, CH_END = 2960, 4043

def extract_figures():
    lines = open('manufactver3tex.tex', encoding='utf-8').readlines()
    figs = []
    for i, line in enumerate(lines[CH_START:CH_END]):
        if '\\includegraphics' not in line: continue
        m = re.search(r'page=(\d+)', line)
        p = int(m.group(1)) if m else None
        m = re.search(r'viewport=\{([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\}', line)
        v = tuple(float(x) for x in m.groups()) if m else None
        if not p or not v: continue
        cap = ''
        for j in range(i, min(i+15, len(lines[CH_START:CH_END]))):
            cm = re.search(r'\\caption\{([^}]*)\}', lines[CH_START:CH_END][j])
            if cm: cap = cm.group(1); break
        figs.append((len(figs)+1, p, v, cap))
    return figs

def crop(figs):
    for seq, p, v, c in figs:
        pf = FIG_DIR / f"page-{p:02d}.png"
        if not pf.exists(): continue
        img = Image.open(pf); W, H = img.size; sc = 300.0/72
        l = max(0,int(v[0]*sc)); t = max(0,int(H-v[3]*sc))
        r = min(W,int(v[2]*sc)); b = min(H,int(H-v[1]*sc))
        if r<=l or b<=t: continue
        img.crop((l,t,r,b)).save(FIG_DIR / f"f{seq:02d}.png", 'PNG')

def sz(fid):
    """Check if image is small."""
    fp = FIG_DIR / f"f{fid:02d}.png"
    if not fp.exists(): return ''
    w, h = Image.open(fp).size
    return 'max-height:380px' if (w < 500 or h < 300) else 'max-height:280px'

# ========== Slide data ==========
# Each entry: (title, [bullets], [notes], [fig_refs])
S = [
("§7.1 液态金属成形理论基础 — 流动性", [
    "合金流动性：液态合金填充铸型的能力",
    "流动性好 → 成形复杂薄壁件，利于排气补缩",
    "流动性差 → 冷隔、浇不足、气孔、夹渣、缩孔",
    "测量：螺旋形试样，越长流动性越好",
], [
    "流动性是铸造性能首要指标，直接影响充型和补缩",
    "螺旋形试样法最直观，浇注相同温度比较长度",
], [1]),

("影响流动性的因素 — 合金成分", [
    "纯金属和共晶成分：恒温凝固→界面光滑→流动性最好",
    "宽凝固范围合金：树枝晶阻碍→流动性差",
    "铁碳合金中：共晶成分铸铁流动性最好",
    "结论：应优先选共晶或近共晶成分合金",
], [
    "树枝晶在两相区阻碍液体流动是流动性变差主因",
    "从流动性考虑应选凝固温度范围小的合金",
], [2, 3]),

("影响流动性的因素 — 物理性质与温度", [
    "比热容↑密度↑导热系数↓结晶潜热↑ → 流动性↑",
    "黏度↓ → 流动性↑",
    "温度↑ → 流动性直线上升",
    "温度过高→氧化吸气严重→气孔夹渣等缺陷",
    "浇注温度必须合理，不可过高",
], [
    "物理性质影响比成分小，但特定条件下很关键",
    "铸铁件采用'高温出炉、低温浇注'策略",
], []),

("充型能力及影响因素", [
    "充型能力 = 合金流动性 + 工艺因素",
    "铸型条件：蓄热能力↑排气差→充型能力↓",
    "浇注条件：系统复杂阻力大→充型差",
    "静压力↑温度↑→充型能力↑",
    "流动性差的合金可通过改善工艺条件补偿",
], [
    "充型能力不足直接导致浇不足冷隔缺陷",
    "实际生产中提高浇注温度是最常用手段",
], []),

("§7.1 铸造合金的收缩", [
    "收缩：合金冷却时体积或尺寸缩小的现象",
    "三阶段：液态收缩 → 凝固收缩 → 固态收缩",
    "液态收缩+凝固收缩 → 缩孔和缩松",
    "固态收缩 → 内应力、变形和裂纹",
    "灰铸铁体收缩率约7%，铸钢约12%",
], [
    "收缩是铸造合金固有物理性质，不可消除只能工艺控制",
    "不同阶段收缩对应不同的铸造缺陷",
], [4]),

("缩孔与缩松的形成机理", [
    "缩孔：集中孔洞，近倒锥形，内表面不光滑",
    "缩松：细小分散孔洞，分布于轴线/厚大断面",
    "纯金属/共晶→逐层凝固→倾向集中缩孔",
    "宽凝固范围→同时凝固→树枝晶分隔液体→缩松",
    "缩孔+缩松总容积一定，增大冷速促转化",
], [
    "缩孔比缩松易检查和修补，生产中促缩松→缩孔转化",
    "浇注温度越高，液态收缩越大，缩孔体积越大",
], [5, 6]),

("防止缩孔的方法", [
    "顺序凝固原则：远离冒口先凝→冒口最后凝",
    "设置冒口和冷铁，控制凝固方向",
    "缩孔转移至冒口，切除冒口得完好铸件",
    "计算机凝固模拟可准确预测缩孔位置",
    "方法：等温线法、内切圆法、计算机模拟",
], [
    "顺序凝固适用收缩大、致密性要求高的铸件",
    "发热保温冒口可提高补缩效果",
], [7, 8]),

("§7.1 铸造内应力与变形裂纹", [
    "热应力：壁厚不均→冷却速度不同→收缩量不同",
    "机械应力：收缩受铸型/型芯机械阻碍",
    "厚壁/心部受拉伸，薄壁/表层受压缩",
    "防止变形：同时凝固、反变形法、去应力退火",
    "热裂（高温沿晶界）vs 冷裂（低温直线状）",
], [
    "再结晶温度以上塑性状态→应力可消除",
    "热裂与硫有关，冷裂与磷有关",
], [9, 10]),

("§7.2 砂型铸造", [
    "流程：零件图→铸件图→模样→造型→合箱→浇注→落砂→清理→检验",
    "优点：适应性极强、成本低、各种合金均可铸造",
    "缺点：一型一次使用、粉尘污染、精度低",
    "手工造型（灵活/低效）vs 机器造型（高效/高精）",
], [
    "砂型铸造约占总铸件产量70%以上",
    "生产线可实现型砂处理到落砂全部机械化",
], [12, 13]),

("浇注位置与分型面", [
    "重要加工面→下面；需补缩厚壁→上部/侧面",
    "分型面选在最大截面，尽量一个分型面",
    "减少活块和型芯数量",
    "铸件大部分放同一砂箱内",
], [
    "浇注位置和分型面是工艺设计两大核心决策",
    "分型面平直可简化造型操作",
], [15, 18]),

("主要工艺参数", [
    "铸造收缩率：灰铸铁0.7~1.0%，铸钢1.5~2.0%",
    "机械加工余量：铸铁件3~15mm",
    "起模斜度：15'~3°",
    "铸造圆角：内圆角≈壁厚1/2",
    "芯头定位固定型芯；最小铸出孔12~50mm",
], [
    "参数选择影响模具设计和铸件尺寸精度",
    "铸造工艺图是指导生产的基本技术文件",
], [21, 22, 24]),

("§7.3 熔模铸造与金属型铸造", [
    "熔模铸造：压制蜡模→结壳(3~7次)→脱蜡→焙烧→浇注",
    "熔模精度IT14~IT11，适用涡轮叶片等复杂精密件",
    "金属型铸造可反复使用（一型多铸）",
    "金属型需预热、排气、喷涂料、尽早开型",
    "适用大批量非铁金属件",
], [
    "熔模铸造无分型面限制，可铸最小壁厚0.3mm",
    "金属型导热快，需预热防白口",
], [26, 27]),

("§7.3 压力铸造与离心铸造", [
    "压铸：高压+高速充型，精度IT13~IT11",
    "效率最高（班产600~700件），最小壁厚0.5mm",
    "不足：卷气→气孔→不能热处理",
    "离心铸造：高速旋转离心力充型",
    "省型芯浇冒口，组织致密可铸双金属件",
], [
    "卷气限制压铸件热处理和焊接应用",
    "离心铸造是管类件最经济的生产方法",
], [28, 29]),

("§7.3 其他特种铸造方法", [
    "反压铸造（压差）：充型平稳，可铸0.5mm薄壁件",
    "挤压铸造（液态模锻）：组织致密接近锻件性能",
    "实型铸造（消失模）：泡沫塑料模，无分型面",
    "磁型铸造：磁丸固结，冷却快3倍",
    "气冲造型：紧实时间<0.1s，精度高无噪声",
], [
    "消失模模样成本仅为木模的1/3",
    "气冲造型是砂型铸造机械化的重要发展方向",
], [30, 32]),

("§7.4 灰铸铁与球墨铸铁", [
    "灰铸铁：冲天炉熔炼，铸造性能优良不需冒口冷铁",
    "孕育处理：加硅铁0.25~0.6%→石墨细化",
    "球墨铸铁：高碳低硫磷，球化+孕育处理",
    "球化处理：稀土镁合金冲入法",
    "球墨铸铁强度远高于灰铸铁",
], [
    "灰铸铁是最广泛应用的铸造合金",
    "冲入法：浇包底部修堤坝埋入球化剂反应平稳",
], [35, 36]),

("§7.4 可锻铸铁、蠕墨铸铁与铸钢", [
    "可锻铸铁：白口毛坯+900~950°C石墨化退火",
    "蠕墨铸铁：铸造性能好，一般铸态使用",
    "铸钢：综合力学性能优于铸铁",
    "铸钢难点：熔点高(~1500°C)、流动性差、收缩率大(~2%)",
    "熔炼：三相电弧炉为主，须正火或退火处理",
], [
    "可锻铸铁并非可锻造，通过退火获团絮状石墨",
    "铸钢件应用：高压阀门、轧钢机架、坦克履带",
], []),

("§7.5 铸件结构设计 — 壁厚与壁连接", [
    "壁厚适当：大于最小壁厚，可用加强筋",
    "壁厚均匀：减小厚壁差防热节和缩孔",
    "壁连接用圆角：避免直角防金属聚集",
    "小型件交错连接，大型件环状连接",
], [
    "内壁冷却慢应薄，外壁冷却快应厚",
    "铸造圆角是最明显铸件特征之一",
], [37, 39]),

("§7.5 减少变形与外形设计", [
    "细长件/大平板件→对称结构或加强筋",
    "弯曲轮辐/奇数轮辐→可自由收缩减小应力",
    "外形避免侧凹，分型面平直",
    "减少型芯数量，以砂垛代替型芯",
    "不加工面设计结构斜度便于起模",
], [
    "结构斜度不同于起模斜度",
    "有斜度的内腔可用砂垛代替型芯简化工艺",
], [41, 43]),

]

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    figs = extract_figures()
    print(f"Figures: {len(figs)}")
    crop(figs)
    fig_caps = {s:c for (s,p,v,c) in figs}

    slides = []
    # Section headers + content
    sec_order = ['§7.1', '§7.2', '§7.3', '§7.4', '§7.5']
    sec_titles = {
        '§7.1': '液态金属成形理论基础',
        '§7.2': '砂型铸造',
        '§7.3': '特种铸造',
        '§7.4': '常用合金铸件生产',
        '§7.5': '铸件结构设计',
    }
    sec_map = {s: [] for s in sec_order}
    for i, (title, _, _, _) in enumerate(S):
        for sec in sec_order:
            if title.startswith(sec):
                sec_map[sec].append(i)
                break
        else:
            sec_map['§7.1'].append(i)

    # Intro slide
    slides.append(
        '<section data-state="content" class="content-slide">'
        '<p class="sn">铸造概述</p><h2>铸造的定义与特点</h2>'
        '<ul>\n<li>铸造：熔融金属浇注/压射/吸入铸型型腔，冷却凝固获得零件或毛坯</li>\n'
        '<li>优点：一次成形、适应性强、成本低、适合复杂内腔</li>\n'
        '<li>不足：晶粒粗大、缩孔/缩松/气孔等缺陷、力学性能不如锻件</li>\n'
        '<li>现代发展：集成计算机凝固模拟、自动控制、机器人技术</li>\n'
        '</ul></section>'
    )

    for sec_key in sec_order:
        sec_title = sec_titles[sec_key]
        slides.append(
            f'<section data-state="section"><div class="section-divider">'
            f'<div class="sec-num">&#9679;</div><h2>{sec_title}</h2></div></section>'
        )
        for idx in sec_map[sec_key]:
            title, bullets, notes, fig_refs = S[idx]
            bl = ''.join(f'<li>{b}</li>\n' for b in bullets)
            nh = ''
            if notes:
                np = '\n'.join(f'<li>{n}</li>' for n in notes)
                nh = f'<aside class="notes"><ul>{np}</ul></aside>'

            if fig_refs:
                fid = fig_refs[0]
                cap = fig_caps.get(fid, '')
                ss = sz(fid)
                slides.append(
                    f'<section data-state="content" class="content-slide">'
                    f'<div class="slide-flex"><div class="slide-text">'
                    f'<p class="sn">{sec_title}</p><h2>{title}</h2><ul>\n{bl}</ul></div>'
                    f'<div class="slide-img">'
                    f'<img src="figures/f{fid:02d}.png" style="{ss}">'
                    f'</div></div>{nh}</section>'
                )
                for fid2 in fig_refs[1:]:
                    cap2 = fig_caps.get(fid2, '')
                    ss2 = sz(fid2)
                    slides.append(
                        f'<section data-state="content" class="content-slide">'
                        f'<p style="font-size:15px;color:#888;margin-bottom:6px;">{cap2}</p>'
                        f'<div class="iw"><img src="figures/f{fid2:02d}.png" style="{ss2}"></div>'
                        f'</section>'
                    )
            else:
                slides.append(
                    f'<section data-state="content" class="content-slide">'
                    f'<p class="sn">{sec_title}</p><h2>{title}</h2>'
                    f'<ul>\n{bl}</ul>{nh}</section>'
                )

    html = '''<!DOCTYPE html><html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>第7章 · 铸造</title>
<link rel="stylesheet" href="lib/reveal.css"><link rel="stylesheet" href="lib/white.css"><link rel="stylesheet" href="lib/katex.min.css">
<style>
.reveal,.reveal h1,.reveal h2,.reveal h3,.reveal h4{font-family:'Noto Sans SC','Microsoft YaHei','PingFang SC','Hiragino Sans GB',sans-serif;color:#1a1a1a}
.reveal .hl{color:#c62828;font-weight:700;background:#fff3f0;padding:0 4px;border-radius:2px}
.reveal .sn{font-family:'Archivo',sans-serif;font-size:11px;font-weight:700;color:#aaa;letter-spacing:2px;margin-bottom:4px}
.title-slide{display:flex;justify-content:flex-start;align-items:stretch;height:100%%}
.title-slide .bar{width:12px;background:#c62828;flex-shrink:0}
.title-slide .inner{flex:1;padding:80px 60px;text-align:left;display:flex;flex-direction:column;justify-content:center}
.title-slide .tag{font-family:'Archivo',sans-serif;font-size:15px;font-weight:700;color:#c62828;letter-spacing:4px;margin-bottom:16px}
.title-slide h1{font-size:72px;font-weight:900;margin:0 0 16px}
.section-divider{text-align:center;padding:40px 0}
.section-divider .sec-num{font-family:'Archivo',sans-serif;font-size:80px;font-weight:800;color:#c62828;opacity:.15;line-height:1;margin-bottom:8px}
.section-divider h2{font-size:40px;margin:8px 0}
.content-slide{text-align:left;padding:8px 16px}
.content-slide h2{font-size:22px;margin:0 0 8px;color:#1a1a1a;border-left:3px solid #c62828;padding-left:10px;line-height:1.3}
.content-slide p{font-size:17px;line-height:1.5;margin:0 0 3px;color:#333}
.content-slide ul{display:block;list-style:none;padding:0;margin:4px 0}
.content-slide li{font-size:16px;line-height:1.5;margin:2px 0;padding:2px 0 2px 18px;position:relative;color:#333}
.content-slide li:before{content:"\\25B8";position:absolute;left:0;color:#c62828;font-size:14px}
.slide-flex{display:flex;gap:14px;align-items:center}
.slide-text{flex:1;min-width:0}
.slide-img{flex:0 0 36%%;text-align:center}
.slide-img img{border-radius:6px;box-shadow:0 2px 6px rgba(0,0,0,.08);max-width:100%%;width:auto}
.iw{text-align:center;margin:8px 0}
.iw img{border-radius:6px;box-shadow:0 2px 6px rgba(0,0,0,.08);max-width:100%%}
.slide-background.title{background:#fff}
.slide-background.section{background:#f5f5f5}
</style></head><body>
<div class="reveal"><div class="slides">
<section data-state="title"><div class="title-slide"><div class="bar"></div><div class="inner"><div class="tag">CHAPTER 07</div><h1>铸造</h1><p class="sub">工程材料与机械制造基础（第3版）</p></div></div></section>
%s
</div></div>
<script src="lib/reveal.js"></script><script src="lib/notes/notes.js"></script><script src="lib/katex.min.js"></script><script src="lib/auto-render.min.js"></script>
<script>
Reveal.initialize({hash:true,controls:true,progress:true,center:false,slideNumber:'c/t',transition:'slide',width:1280,height:720,margin:0.04,minScale:0.2,maxScale:1.5,plugins:[RevealNotes]});
Reveal.on('ready',a);Reveal.on('slidechanged',a);
function a(){var b=document.querySelectorAll('.slide-background');for(var i=0;i<b.length;i++){b[i].className=b[i].className.replace(/\\b(title|section|content)\\b/g,'');b[i].classList.add(Reveal.getCurrentSlide().dataset.state||'content')}}
</script></body></html>''' % '\n'.join(slides)

    open('ch07-铸造.html', 'w', encoding='utf-8').write(html)
    total = 1 + html.count('</section>\n')
    ul = html.count('<li>') - html.count('notes')*2
    imgs = html.count('src="figures/f')
    print(f"Slides: {total}, Bullets: ~{ul}, Images: {imgs}")

if __name__ == '__main__':
    main()
