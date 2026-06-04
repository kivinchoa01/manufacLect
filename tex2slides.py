#!/usr/bin/env python3
"""
TeX -> Reveal.js 课件生成器
学生页面：简明要点 + 配图
教师备注：每条要点的扩展解释（非全文搬运）
"""
import sys, re
from pathlib import Path
from PIL import Image

TEX_FILE = "manufactver3tex.tex"
FIGURES_DIR = Path("figures")

# ===== 每张幻灯片的完整数据 =====
# structure: [section_title, [[sub_title, [bullets], [notes], [fig_seq]], ...]]
CHAPTER_CONTENT = [
    ["液态金属成形理论基础", [
        ["液态合金的充型能力", [
            "流动性：液态合金填充铸型的能力",
            "流动性好 → 获复杂薄壁铸件，利于排气补缩",
            "流动性差 → 冷隔、浇不足、气孔、夹渣、缩孔",
            "测量方法：螺旋形试样，越长流动性越好",
            "影响因素：合金成分、物理性质、温度、杂质和气体",
            "纯金属和共晶合金流动性最好（恒温凝固）",
        ], [
            "流动性直接影响铸件质量和成品率，是合金铸造性能的核心指标",
            "良好流动性便于制造薄壁复杂结构，有利于气体和夹杂物上浮排除",
            "流动性差是多数铸造缺陷的直接原因，需针对性调整工艺",
            "螺旋形试样法直观可靠，是铸造生产中常用的检测手段",
            "合金成分是影响流动性的首要因素，近共晶成分流动性最优",
            "纯金属和共晶成分在恒定温度下凝固，界面光滑，流动阻力小",
        ], [1]],
        ["铸造合金的收缩", [
            "收缩：合金冷却时体积或尺寸缩小",
            "三阶段：液态收缩 → 凝固收缩 → 固态收缩",
            "液态收缩+凝固收缩 → 缩孔（集中）和缩松（分散）",
            "固态收缩 → 内应力、变形和裂纹",
            "防止缩孔：顺序凝固 + 冒口 + 冷铁",
        ], [
            "收缩是铸造合金的固有物理性质，无法消除，只能通过工艺控制",
            "三个收缩阶段对应不同的温度区间，对铸件质量的影响也不同",
            "缩孔集中在最后凝固部位，外形倒锥形；缩松细小分散，危害更大",
            "固态收缩是铸件产生应力和变形的根本原因，影响尺寸精度",
            "顺序凝固让缩孔转移到冒口中，切除冒口即可获得完好铸件",
        ], [5]],
        ["铸造内应力及铸件的变形、裂纹", [
            "内应力 = 热应力（壁厚不均）+ 机械应力（铸型阻碍）",
            "厚壁/心部受拉伸，薄壁/表层受压缩",
            "防止变形：同时凝固、反变形法、去应力退火",
            "热裂：高温沿晶界产生，短而曲折，常见于铸钢和铝合金",
            "冷裂：低温直线状裂缝，控制磷含量可预防",
        ], [
            "热应力由冷却速度差异引起，机械应力由铸型退让性不足造成",
            "拉伸/压缩的分布规律是分析铸件变形方向的基本依据",
            "同时凝固适用于收缩小的合金（如灰铸铁），反变形法需精确计算变形量",
            "热裂与硫含量密切相关，改善型砂退让性可有效预防",
            "冷裂与磷含量有关，减少内应力和降低合金脆性是防治关键",
        ], [8]],
    ]],
    ["砂型铸造", [
        ["砂型铸造的生产过程及特点", [
            "工艺流程：零件图→铸件图→模样→造型→合箱→浇注→落砂→清理→检验",
            "优点：适应性强、成本低、适用范围广",
            "缺点：一型一次使用、粉尘污染、精度低",
        ], [
            "砂型铸造是应用最广泛的铸造方法，约占总铸件产量的70%以上",
            "可铸造各种尺寸和重量的铸件，从几克到数百吨均可",
            "每吨合格铸件需4~5吨型砂，砂尘污染是环保治理重点",
        ], [12]],
        ["砂型铸造工艺简介", [
            "手工造型：整模、分模、挖砂、活块、三箱、刮板、假箱、地坑",
            "机器造型：振压紧实、抛砂紧实、射砂紧实",
            "起模方法：顶箱（浅腔）、漏模（深腔）、翻转（复杂腔）",
            "浇注原则：'高温出炉、低温浇注'",
        ], [
            "手工造型灵活适应单件小批生产，但效率低、劳动强度大",
            "机器造型精度高、生产率高，适合大批量生产",
            "起模方式的选择取决于型腔深度和复杂程度",
            "高温出炉利于熔渣上浮，低温浇注减少气体溶解和液态收缩",
        ], [13]],
        ["铸造工艺图", [
            "浇注位置：重要加工面朝下，厚壁部分朝上（便于补缩）",
            "分型面：选在最大截面，尽量一个分型面",
            "主要工艺参数：收缩率、加工余量、起模斜度、铸造圆角",
            "芯头：定位和固定型芯；最小铸出孔12~50mm",
        ], [
            "浇注位置和分型面是铸造工艺设计的两大核心决策",
            "分型面越少越好——两箱造型最简单，三箱造型复杂",
            "铸造圆角是铸件最明显的结构特征，内圆角约壁厚1/2",
            "芯头需有合适的长度、斜度和装配间隙",
        ], [14]],
    ]],
    ["特种铸造", [
        ["熔模铸造（精密铸造）", [
            "工艺：压蜡模→结壳→脱蜡→焙烧→浇注",
            "精度高：IT14~IT11，Ra 1.6~12.5μm",
            "适用：涡轮叶片、高速钢刀具等复杂精密小件",
        ], [
            "熔模铸造又称失蜡铸造，适合形状极其复杂的精密铸件",
            "蜡模需反复浸涂耐火浆料3~7次，形成5~10mm的型壳",
            "不需要分型面，可铸最小壁厚0.3mm，最小孔径0.5mm",
        ], [26]],
        ["金属型铸造", [
            "金属型可反复使用（'一型多铸'）",
            "措施：预热、排气、喷涂料、尽早开型",
            "适用：大批量非铁金属件（铝活塞、气缸体、铜轴瓦）",
        ], [
            "金属型铸造的力学性能好于砂型，铝合金可提高抗拉强度约20%",
            "金属型导热快，需提前预热防止白口组织",
            "壁厚应大于15mm，防止浇不足",
        ], [27]],
        ["压力铸造", [
            "两大特点：高压 + 高速充型",
            "精度IT13~IT11，最小壁厚0.5mm",
            "生产效率最高（班产600~700件）",
            "缺点：设备投资大，卷气→不能热处理",
        ], [
            "压铸机分热压室式和冷压室式两大类",
            "充型速度极高，可充满非常薄的复杂型腔",
            "高压下凝固组织致密，强度可比砂型提高25%~30%",
            "卷气导致内部气孔，限制了压铸件的热处理和焊接应用",
        ], [28]],
        ["离心铸造", [
            "原理：高速旋转、离心力充型",
            "省型芯/浇冒口，组织致密，可铸双金属件",
            "缺点：内表面质量差，精度不易控制",
            "应用：铸铁管、气缸套、滑动轴承",
        ], [
            "立式离心铸造绕竖直轴旋转，卧式绕水平轴旋转",
            "离心力促进金属液顺序凝固，组织致密无缩孔",
            "双金属件如钢背铜套轴承可一次铸造成形",
        ], [29]],
        ["其他铸造方法简介", [
            "反压铸造（压差铸造）：充型平稳，最小壁厚0.5mm",
            "挤压铸造（液态模锻）：力学性能接近锻件",
            "实型铸造（消失模）：泡沫塑料模，无分型面",
            "磁型铸造：磁丸固结成铸型，冷却快3倍",
            "气冲造型：紧实时间<0.1s，精度高无噪声",
        ], [
            "反压铸造适用于要求高致密性的铸件，如飞机零件",
            "挤压铸造介于铸造和锻造之间，兼有两者的优点",
            "消失模铸造模样成本仅为木模的1/3",
            "磁型铸造不用黏结剂，改善了工作环境",
            "气冲造型紧实度高且均匀，是砂型铸造的重要发展方向",
        ], [32]],
        ["铸造技术的发展趋势", [
            "绿色集约化：低消耗、无废弃物",
            "专业化、自动化、智能化生产",
            "计算机和机器人应用：CAD/CAE/凝固模拟",
        ], [
            "铸造技术正朝着绿色、高效、精密的方向发展",
            "计算机凝固模拟可准确预测缩孔位置，优化工艺",
            "机器人操作改善了铸造工人的劳动条件和安全性",
        ], []],
    ]],
    ["常用合金铸件生产特点", [
        ["铸铁件生产", [
            "灰铸铁：冲天炉熔炼，'高温出炉、低温浇注'",
            "球墨铸铁：球化处理（稀土镁合金）+ 孕育处理",
            "可锻铸铁：白口毛坯 + 高温石墨化退火",
            "蠕墨铸铁：蠕化剂处理，铸造性能好",
        ], [
            "灰铸铁铸造性能优良，一般不需冒口和冷铁，工艺简化",
            "球化处理常用冲入法——浇包底部修堤坝埋入球化剂",
            "可锻铸铁并非可锻造，而是通过退火获得团絮状石墨",
            "蠕墨铸铁一般铸态使用，不经过热处理",
        ], [34]],
        ["铸钢件生产", [
            "综合力学性能优于铸铁，强度高、韧性好、焊接性好",
            "工艺难点：熔点高（~1500°C）、流动性差、收缩率大",
            "型砂要求：高透气性、耐火度、退让性",
            "熔炼设备：三相电弧炉为主",
        ], [
            "铸钢件须经正火或退火处理以细化晶粒",
            "铸钢收缩率约2%，需配置大冒口和冷铁补缩",
            "应用领域：高压阀门、轧钢机架、坦克履带（ZGMn13）",
        ], []],
    ]],
    ["铸件结构设计", [
        ["铸造性能对铸件结构的要求", [
            "壁厚适当：大于最小壁厚，可用加强筋",
            "壁厚均匀：减小厚壁差，防热节和缩孔",
            "壁连接用圆角：避免直角，防金属聚集",
            "减少变形：对称结构或加强筋",
            "减缓收缩受阻：弯曲或奇数轮辐",
        ], [
            "最小壁厚取决于合金种类和铸型条件，灰铸铁可铸更薄壁件",
            "壁厚不均匀会导致冷却速度差异，产生热节和缩孔",
            "圆角半径约为相邻壁厚的1/3~1/2",
            "细长件和大平板件最容易发生变形",
            "奇数轮辐设计使各辐条可同时自由收缩，减小内应力",
        ], [35]],
        ["铸造工艺对铸件结构的要求", [
            "外形尽量简单，避免侧凹结构",
            "分型面应平直，减少活块和型芯",
            "以砂垛代替型芯，减少制芯成本",
            "开式结构可省去型芯",
            "垂直于分型面的不加工面应有结构斜度",
        ], [
            "侧凹结构需要活块或型芯，增加制模和造型难度",
            "结构斜度不同于起模斜度——前者是结构固有，后者是工艺附加",
            "减少型芯数量不仅降低成本，还利于排气和清理",
            "内腔有斜度时可用砂垛代替型芯，显著简化工艺",
        ], [43]],
    ]],
]

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    ch, ch_name = 7, '铸造'
    # Extract figures
    lines = open('manufactver3tex.tex', encoding='utf-8').read()
    figures = []
    cap = None
    for line in lines.split('\n'):
        cm = re.search(r'\\caption\{([^}]*)\}', line)
        if cm: cap = cm.group(1)
        if '\\includegraphics' in line:
            m = re.search(r'page=(\d+)', line)
            p = int(m.group(1)) if m else None
            m = re.search(r'viewport=\{([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\}', line)
            v = tuple(float(x) for x in m.groups()) if m else None
            if p and v:
                figures.append((len(figures)+1, p, v, cap or ""))
                cap = None

    # Crop figures
    for (seq, p, v, c) in figures:
        pf = FIGURES_DIR / f"page-{p:02d}.png"
        if not pf.exists(): continue
        img = Image.open(pf)
        W, H = img.size
        sc = 300.0/72
        llx,lly,urx,ury = v
        l,t = int(llx*sc), int(H-ury*sc)
        r,b = int(urx*sc), int(H-lly*sc)
        l,t,r,b = max(0,l),max(0,t),min(W,r),min(H,b)
        if r<=l or b<=t: continue
        img.crop((l,t,r,b)).save(FIGURES_DIR / f"fig-{seq:02d}.png", 'PNG')

    # Build slides
    slides_html = []
    for sec_title, subs in CHAPTER_CONTENT:
        slides_html.append(
            f'<section data-state="section"><div class="section-divider">'
            f'<div class="sec-num">&#9679;</div><h2>{sec_title}</h2></div></section>'
        )
        for item in subs:
            title, bullets, notes, fig_seqs = item
            bullet_lis = ''.join(f'<li>{b}</li>\n' for b in bullets)

            # Build notes - one per bullet
            if notes:
                notes_ps = '\n'.join(f'<li>{n}</li>' for n in notes)
                notes_html = f'<aside class="notes"><ul>{notes_ps}</ul></aside>'
            else:
                notes_html = ''

            # Layout
            if fig_seqs:
                fseq = fig_seqs[0]
                slides_html.append(
                    f'<section data-state="content" class="content-slide">'
                    f'<div class="slide-flex">'
                    f'<div class="slide-text">'
                    f'<p class="sn">{sec_title}</p><h2>{title}</h2><ul>\n{bullet_lis}</ul>'
                    f'</div>'
                    f'<div class="slide-img">'
                    f'<img src="figures/fig-{fseq:02d}.png">'
                    f'</div>'
                    f'</div>{notes_html}</section>'
                )
            else:
                slides_html.append(
                    f'<section data-state="content" class="content-slide">'
                    f'<p class="sn">{sec_title}</p><h2>{title}</h2><ul>\n{bullet_lis}</ul>{notes_html}'
                    f'</section>'
                )

    all_s = '\n'.join(slides_html)
    total = slides_html.count('</section>\n') + 1

    html = '''<!DOCTYPE html><html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>第7章 · 铸造</title>
<link rel="stylesheet" href="lib/reveal.css"><link rel="stylesheet" href="lib/white.css"><link rel="stylesheet" href="lib/katex.min.css">
<style>
.reveal,.reveal h1,.reveal h2,.reveal h3,.reveal h4{font-family:'Noto Sans SC','Microsoft YaHei','PingFang SC','Hiragino Sans GB',sans-serif;color:#1a1a1a}
.reveal .sn{font-family:'Archivo',sans-serif;font-size:12px;font-weight:700;color:#aaa;letter-spacing:2px;margin-bottom:4px}
.reveal .sub{font-size:18px;color:#888}
.title-slide{display:flex;justify-content:flex-start;align-items:stretch;height:100%%}
.title-slide .bar{width:12px;background:#e03020;flex-shrink:0}
.title-slide .inner{flex:1;padding:80px 60px;text-align:left;display:flex;flex-direction:column;justify-content:center}
.title-slide .tag{font-family:'Archivo',sans-serif;font-size:15px;font-weight:700;color:#e03020;letter-spacing:4px;margin-bottom:16px}
.title-slide h1{font-size:72px;font-weight:900;margin:0 0 16px}
.section-divider{text-align:center;padding:40px 0}
.section-divider .sec-num{font-family:'Archivo',sans-serif;font-size:80px;font-weight:800;color:#e03020;opacity:.15;line-height:1;margin-bottom:8px}
.section-divider h2{font-size:44px;margin:8px 0}
.content-slide{text-align:left;padding:8px 0}
.content-slide h2{font-size:26px;margin:0 0 6px;color:#1a1a1a;border-bottom:2px solid #e03020;padding-bottom:3px;display:inline-block}
.content-slide p{font-size:18px;line-height:1.5;margin:0 0 3px;color:#333}
.content-slide ul{display:block;list-style:none;padding:0;margin:4px 0}
.content-slide li{font-size:18px;line-height:1.5;margin:2px 0;padding:2px 0 2px 22px;position:relative;color:#333}
.content-slide li:before{content:"\\25B8";position:absolute;left:0;color:#e03020;font-size:16px}
.slide-flex{display:flex;gap:16px;align-items:center}
.slide-text{flex:1;min-width:0}
.slide-img{flex:0 0 36%%;text-align:center;max-width:380px}
.slide-img img{max-height:280px;max-width:100%%;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.08)}
.slide-img .cap{font-size:13px;color:#888;margin-top:2px}
.slide-background.title{background:#fff}
.slide-background.section{background:#f5f5f5}
.notes{font-size:16px}
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
</script></body></html>''' % all_s

    open('ch07-铸造.html', 'w', encoding='utf-8').write(html)
    print(f"[OK] ch07-铸造.html  ({total} slides)")
    print(f"     学生页面: 简明要点 + 配图")
    print(f"     教师备注: 每条要点的扩展解释 (按S键查看)")

if __name__ == '__main__':
    main()
