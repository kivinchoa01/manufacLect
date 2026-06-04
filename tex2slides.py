#!/usr/bin/env python3
"""Comprehensive Chapter 7 slide generator with intelligent image sizing."""
import sys, re
from pathlib import Path
from PIL import Image

FIGURES_DIR = Path("figures")
CHAPTER_START, CHAPTER_END = 2960, 4043  # 0-indexed TeX line range

# ===== Full slide data: [section_title, [[sub_title, [bullets], [notes], [figs]], ...]] =====
S = [
["铸造概述", [
    ["铸造的定义与特点", [
        "铸造：熔融金属浇注/压射/吸入铸型，冷却凝固获得零件或毛坯",
        "优点：一次成形、适应性强、成本低、适合复杂内腔",
        "缺点：晶粒粗大、缩孔/缩松/气孔等缺陷、力学性能不如锻件",
        "现代铸造：计算机凝固模拟、自动控制、机器人集成",
    ], [
        "铸造是金属液态成形，与锻造（固态成形）有本质区别",
        "机器制造业中铸件占比很高，是基础制造工艺",
        "现代铸造技术已集成CAD/CAE、真空技术、激光技术等",
    ], []],
]],
["液态金属成形理论基础", [
    ["合金的流动性", [
        "流动性：液态合金填充铸型的能力",
        "流动性好 → 成形复杂薄壁件，利于排气和补缩",
        "流动性差 → 冷隔、浇不足、气孔、夹渣、缩孔",
        "测量方法：螺旋形试样，越长流动性越好",
    ], [
        "流动性是衡量合金铸造性能的核心指标",
        "螺旋形试样法直观可靠，是铸造生产常用检测手段",
    ], [1]],
    ["影响流动性的因素—合金成分", [
        "纯金属和共晶成分：恒温凝固，界面光滑，流动性最好",
        "宽凝固范围合金：树枝晶阻碍流动，流动性差",
        "铁碳合金：共晶成分铸铁流动性最好",
        "应尽量选共晶或近共晶成分合金",
    ], [
        "纯金属在恒温下凝固，固液界面光滑，阻力最小",
        "宽凝固范围合金中树枝晶阻碍流动是流动性差的主因",
    ], [2, 3]],
    ["影响流动性的因素—物理性质与温度", [
        "比热容和密度越大、导热系数越小 → 流动性越好",
        "黏度越小 → 流动性越好",
        "温度升高 → 流动性上升，但过高→氧化吸气严重",
        "浇注温度必须合理，并非越高越好",
    ], [
        "物理性质的影响比合金成分小，但在特定条件下很关键",
        "生产中对铸铁件采用'高温出炉、低温浇注'策略",
    ], []],
    ["液态合金的充型能力", [
        "充型能力：液态合金充满铸型、获得完整铸件的能力",
        "充型能力 = 合金流动性 + 工艺因素",
        "铸型条件：蓄热能力、排气、温度、结构复杂度",
        "浇注条件：系统结构（阻力）、静压力、浇注温度",
    ], [
        "对于流动性差的合金，可通过改善工艺条件提高充型能力",
        "提高浇注温度是生产中提高充型能力最常用的措施",
    ], []],
    ["铸造合金的收缩", [
        "收缩：合金从液态冷却至室温体积缩小的现象",
        "三阶段：液态收缩 → 凝固收缩 → 固态收缩",
        "液态收缩+凝固收缩 → 缩孔和缩松",
        "固态收缩 → 内应力、变形和裂纹",
        "灰铸铁体收缩率约7%，铸钢约12%",
    ], [
        "收缩是铸造合金的固有物理性质，无法消除只能控制",
        "不同阶段的收缩对铸件质量的影响不同，需针对性防止",
    ], [4]],
    ["缩孔与缩松的形成", [
        "缩孔：集中孔洞，近倒锥形，内表面不光滑",
        "缩松：细小分散孔洞，多分布在轴线区域和厚大断面",
        "纯金属/共晶合金 → 逐层凝固 → 缩孔（集中）",
        "宽凝固范围合金 → 同时凝固 → 缩松（分散）",
        "缩孔容积 + 缩松容积 = 定值，可互相转化",
    ], [
        "缩孔比缩松易检查和修补，因此常促使缩松→缩孔转化",
        "增大冷却速度可促进缩松向缩孔转化",
    ], [5, 6]],
    ["防止缩孔的方法", [
        "顺序凝固原则：远离冒口先凝→冒口最后凝→缩孔转移至冒口",
        "设置冒口和冷铁，控制凝固方向",
        "冒口最后凝固，缩孔集中在冒口中，切除即可",
        "计算机凝固模拟可准确预测缩孔位置",
        "确定缩孔位置的方法：等温线法、内切圆法、模拟法",
    ], [
        "顺序凝固适用于收缩大、致密性要求高的铸件（如铸钢）",
        "发热保温冒口可提高补缩效果，减少冒口体积",
    ], [7, 8]],
    ["铸造内应力", [
        "热应力：壁厚不均→冷却速度不同→收缩量不同",
        "机械应力：收缩受铸型、型芯的机械阻碍",
        "厚壁/心部受拉伸，薄壁/表层受压缩",
        "合金固态收缩率越大，壁厚差别越大→热应力越大",
    ], [
        "金属在再结晶温度以上为塑性状态，应力可自行消除",
        "低于再结晶温度为弹性状态，应力保留",
    ], [9]],
    ["铸件的变形与裂纹", [
        "存在内应力时，铸件通过变形减缓内应力",
        "防止变形：同时凝固原则、反变形法、去应力退火",
        "热裂：凝固后期高温形成，沿晶界，短而曲折",
        "冷裂：低温直线状裂缝，出现在受拉伸部位",
        "防止热裂：改善退让性、限制硫；冷裂：减少应力、控制磷",
    ], [
        "车床床身导轨厚→受拉，床壁薄→受压，产生向下挠曲",
        "同时凝固原则适用于收缩小、致密性要求不高的铸件",
    ], [10, 11]],
]],
["砂型铸造", [
    ["砂型铸造生产过程", [
        "工艺流程：零件图→铸件图→模样→造型→合箱→浇注→落砂→清理→检验",
        "优点：适应性极强，成本低，各种合金均可铸造",
        "缺点：一型一次使用，每吨铸件需4~5吨型砂，粉尘污染",
    ], [
        "砂型铸造是应用最广泛的铸造方法，约占总铸件产量70%以上",
        "生产线可实现型砂处理、造型、浇注、落砂全部机械化",
    ], [12, 13]],
    ["造型方法", [
        "手工造型：整模、分模、挖砂、活块、三箱、刮板、假箱、地坑",
        "机器造型：振压紧实、抛砂紧实、射砂紧实",
        "起模方法：顶箱（浅腔）、漏模（深腔）、翻转（复杂腔）",
        "熔炼与浇注：'高温出炉、低温浇注'",
    ], [
        "手工造型灵活，适应单件小批生产，但效率低",
        "机器造型精度高、生产率高，适合大批量生产",
    ], [14]],
    ["浇注位置的选择", [
        "重要加工面和主要加工面 → 放在下面",
        "需补缩的厚壁部分 → 放在上部或侧面（便于放置冒口）",
        "大面积薄壁部分 → 放在下部，立放或倾斜浇注",
        "大平面 → 放在下面（防夹砂缺陷）",
    ], [
        "浇注位置直接影响铸件质量和补缩效果",
        "同时考虑浇注位置和分型面的综合优化",
    ], [15, 16]],
    ["分型面的选择", [
        "原则①：选在铸件最大截面上，取模顺利",
        "原则②：尽量减少分型面数量，最好一个分型面",
        "原则③：减少活块和型芯数量，简化工艺",
        "原则④：铸件大部分放在同一砂箱内",
    ], [
        "分型面决定造型方案，影响铸件精度和成本",
        "分型面平直→简化造型，减少错箱风险",
    ], [17, 18, 19, 20]],
    ["主要工艺参数", [
        "铸造收缩率：灰铸铁0.7%~1.0%，铸钢1.5%~2.0%",
        "机械加工余量：铸铁件3~15mm",
        "起模斜度：15'~3°（垂直于分型面的加工表面）",
        "铸造圆角：避免尖角处应力集中，内圆角≈壁厚1/2",
        "芯头：定位和固定型芯；最小铸出孔12~50mm",
    ], [
        "工艺参数直接影响模具设计和铸件尺寸精度",
        "参数选择需综合考虑合金种类、造型方法和生产批量",
    ], [21, 22, 23, 24]],
    ["铸造工艺图实例", [
        "铸造工艺图指导模样设计、生产准备和铸件检验",
        "包括：浇注位置、分型面、加工余量、收缩率、芯头等",
        "是铸造生产的基本技术文件",
    ], [
        "支座的铸造工艺图是典型实例，涵盖主要工艺参数标注",
    ], [25]],
]],
["特种铸造", [
    ["熔模铸造（精密铸造）", [
        "工艺过程：压制蜡模→结壳(3~7次)→脱蜡→焙烧(850~950°C)→浇注",
        "精度高：IT14~IT11，Ra 1.6~12.5μm",
        "最小孔径0.5mm，最小壁厚0.3mm",
        "适用：涡轮叶片、高速钢刀具等复杂精密小件",
    ], [
        "熔模铸造又称失蜡铸造，无分型面限制",
        "蜡模熔失后获得整体型壳，可铸出极复杂形状",
    ], [26]],
    ["金属型铸造", [
        "金属型可反复使用（'一型多铸'）",
        "措施：预热金属型、加强排气、喷刷涂料、尽早开型",
        "铸件力学性能高，铝合金抗拉强度提高约20%",
        "适用：大批量非铁金属件（铝活塞、气缸体、铜轴瓦）",
    ], [
        "金属型导热快易产生白口组织，需预热控制冷却速度",
        "壁厚应大于15mm防止浇不足",
    ], [27]],
    ["压力铸造", [
        "两大特点：高压 + 高速充型",
        "精度IT13~IT11，Ra 0.8~3.2μm，最小壁厚0.5mm",
        "效率最高，班产600~700件",
        "缺点：设备投资大，卷气→气孔→不能热处理",
        "适用：低熔点非铁金属中小型件",
    ], [
        "压铸机分热压室式和冷压室式两大类",
        "卷气导致内部气孔，限制压铸件热处理和焊接应用",
    ], [28]],
    ["离心铸造", [
        "原理：高速旋转，离心力充型成形",
        "立式：绕竖直轴旋转；卧式：绕水平轴旋转",
        "优点：省型芯和浇冒口，组织致密，可铸双金属件",
        "缺点：内表面质量差，孔尺寸不易控制",
    ], [
        "离心铸造是管道类铸件最经济的生产方法",
        "双金属件如钢背铜套轴承可一次铸造成形",
    ], [29]],
    ["反压铸造与挤压铸造", [
        "反压铸造（压差铸造）：充型平稳，最小壁厚0.5mm",
        "增压法：坩埚加压高于型腔→金属液沿升液管充型",
        "挤压铸造（液态模锻）：对液态金属施加机械压力成形",
        "挤压铸造：无浇注系统，组织致密，力学性能接近锻件",
    ], [
        "反压铸造适用于高致密性要求的航空铸件",
        "挤压铸造介于铸造和锻造之间，兼有两者的优点",
    ], [30, 31]],
    ["实型铸造与磁型铸造", [
        "实型铸造（消失模）：泡沫塑料模→填砂振实→浇注汽化",
        "实型铸造优点：无分型面、不用型芯、模样成本低",
        "磁型铸造：磁丸+通电固结成铸型→浇注→断电松散",
        "磁型铸造特点：无黏结剂、冷却速度块3倍、组织细密",
    ], [
        "实型铸造模样成本仅为木模的1/3",
        "磁型铸造改善了工作环境，无砂尘污染",
    ], [32, 33]],
    ["气冲造型与其他", [
        "气冲造型：压缩空气/燃气冲击波紧实型砂",
        "紧实时间<0.1s，一个铸型约0.5s",
        "紧实度高且均匀，精度高，无振击噪声",
    ], [
        "气冲造型是砂型铸造机械化的重要发展方向",
    ], [34]],
]],
["常用合金铸件生产", [
    ["灰铸铁件", [
        "冲天炉熔炼：铸造生铁+回炉铁+废钢+铁合金+焦炭+熔剂",
        "铸造性能优良，一般不需冒口和冷铁",
        "孕育处理：浇注前加硅铁0.25%~0.6%→石墨细化",
        "要求低碳低硅铁液+高出炉温度（1450~1470°C）",
    ], [
        "灰铸铁是应用最广泛的铸造合金",
        "孕育处理显著改善石墨形态和基体组织",
    ], [35]],
    ["球墨铸铁件", [
        "化学成分要求：高碳(C=3.6~4.0%)、高硅、低硫(S<0.06%)",
        "球化处理：稀土镁合金球化剂，冲入法加入",
        "孕育处理：硅铁0.4%~1.0%",
        "常设冒口和冷铁，控制型砂水分防皮下气孔",
    ], [
        "冲入法：浇包底部修堤坝埋入球化剂，反应平稳",
        "球墨铸铁强度远高于灰铸铁，可替代部分铸钢件",
    ], [36]],
    ["可锻铸铁与蠕墨铸铁", [
        "可锻铸铁：白口毛坯+900~950°C石墨化退火→团絮状石墨",
        "可锻铸铁流动性差，需注意冒口和冷铁",
        "蠕墨铸铁：铸造性能与灰铸铁相近，流动性更好",
        "蠕墨铸铁一般铸态使用，不热处理",
    ], [
        "可锻铸铁并非可锻造，而是通过退火改善石墨形态",
        "蠕化剂用稀土硅铁，冲入法处理",
    ], []],
    ["铸钢件生产", [
        "综合力学性能优于铸铁，强度高、塑性韧性好、焊接性好",
        "工艺特点：熔点高(~1500°C)、流动性差、收缩率大(~2%)",
        "型砂要求：高透气性、耐火度、强度和退让性",
        "熔炼：三相电弧炉（最普遍）或感应电炉",
        "应用：高压阀门壳体、轧钢机机架、坦克履带(ZGMn13)",
    ], [
        "铸钢件须正火或退火处理细化晶粒",
        "遵循顺序凝固原则配置大冒口和冷铁补缩",
    ], []],
]],
["铸件结构设计", [
    ["壁厚设计原则", [
        "壁厚应适当：大于合金最小壁厚（防浇不足），不宜过大（防缩松）",
        "可用T形、工字形、槽形截面或加强筋保证强度",
        "壁厚应均匀：减小厚壁差→防热节、缩孔、变形",
        "内壁冷却慢应薄，外壁冷却快应厚",
    ], [
        "最小壁厚取决于合金种类和铸型条件",
        "壁厚不均匀是铸造缺陷的主要根源之一",
    ], [37, 38]],
    ["壁连接设计", [
        "壁连接应合理：结构圆角避免直角→防金属聚集和缩孔",
        "过渡连接：避免锐角和交叉连接",
        "小型件用交错连接，大型件用环状连接",
        "不等厚壁之间用圆角/倾斜/复合过渡",
    ], [
        "铸造圆角是最明显的铸件结构特征之一",
        "合理设计壁连接可显著减少应力集中和裂纹",
    ], [39, 40, 41]],
    ["减少变形与减缓收缩受阻", [
        "细长件和大平板件 → 对称结构或加强筋",
        "弯曲轮辐或奇数轮辐 → 冷却时可自由收缩",
        "减缓收缩受阻是降低铸造内应力的关键",
    ], [
        "弯曲轮辐设计允许各辐条同时自由收缩",
        "平板加筋既可减重又能防变形",
    ], [42, 43]],
    ["外形与内腔设计", [
        "外形尽量简单，避免侧凹 → 便于起模",
        "凸台和筋条应便于起模，分型面平直",
        "内腔：减少型芯数量、简化型芯形状",
        "以砂垛代替型芯，开式结构省去型芯",
    ], [
        "侧凹结构需要活块或型芯，增加制模难度",
        "型芯越少，定位、固定、排气和清理越方便",
    ], [44, 45, 46, 47]],
    ["结构斜度", [
        "垂直于分型面的不加工表面应设计结构斜度",
        "优点：起模方便、零件更美观",
        "有斜度的内腔可用砂垛代替型芯",
        "高度越低，结构斜度应越大",
    ], [
        "结构斜度不同于起模斜度—前者是结构固有特征",
    ], [48]],
]],
]
# Map subsection titles to their figure sequence numbers in the extraction
TITLE_FIG_MAP = {
    "合金的流动性": [1], "影响流动性的因素—合金成分": [2, 3],
    "影响流动性的因素—物理性质与温度": [], "液态合金的充型能力": [],
    "铸造合金的收缩": [4], "缩孔与缩松的形成": [5, 6],
    "防止缩孔的方法": [7, 8], "铸造内应力": [9],
    "铸件的变形与裂纹": [10, 11],
    "砂型铸造生产过程": [12, 13], "造型方法": [14],
    "浇注位置的选择": [15, 16, 17], "分型面的选择": [18, 19, 20],
    "主要工艺参数": [21, 22, 23, 24], "铸造工艺图实例": [25],
    "熔模铸造（精密铸造）": [26], "金属型铸造": [27],
    "压力铸造": [28], "离心铸造": [29],
    "反压铸造与挤压铸造": [30, 31],
    "实型铸造与磁型铸造": [32, 33], "气冲造型与其他": [34],
    "灰铸铁件": [35], "球墨铸铁件": [36],
    "可锻铸铁与蠕墨铸铁": [], "铸钢件生产": [],
    "壁厚设计原则": [37, 38], "壁连接设计": [39, 40, 41],
    "减少变形与减缓收缩受阻": [42, 43],
    "外形与内腔设计": [44, 45, 46, 47], "结构斜度": [48],
}

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    # Extract ONLY Chapter 7 figures
    lines = open('manufactver3tex.tex', encoding='utf-8').readlines()
    ch_lines = lines[CHAPTER_START:CHAPTER_END]
    figures = []
    cap = None
    for line in ch_lines:
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
    print(f"Chapter 7: {len(figures)} figures")

    # Crop with intelligent sizing
    for (seq, p, v, c) in figures:
        pf = FIGURES_DIR / f"page-{p:02d}.png"
        if not pf.exists(): continue
        img = Image.open(pf)
        W, H = img.size
        sc = 300.0/72
        llx,lly,urx,ury = v
        l = max(0, int(llx*sc)); t = max(0, int(H-ury*sc))
        r = min(W, int(urx*sc)); b = min(H, int(H-lly*sc))
        if r<=l or b<=t: continue
        img.crop((l,t,r,b)).save(FIGURES_DIR / f"fig-{seq:02d}.png", 'PNG')

    # Build slides
    slides_html = []
    total_content = 0
    for sec_title, subs in S:
        slides_html.append(
            f'<section data-state="section"><div class="section-divider">'
            f'<div class="sec-num">&#9679;</div><h2>{sec_title}</h2></div></section>'
        )
        for item in subs:
            title, bullets, notes, _ = item
            figs = TITLE_FIG_MAP.get(title, [])

            bullet_lis = ''.join(f'<li>{b}</li>\n' for b in bullets)
            if notes:
                notes_ps = '\n'.join(f'<li>{n}</li>' for n in notes)
                notes_html = f'<aside class="notes"><ul>{notes_ps}</ul></aside>'
            else:
                notes_html = ''

            # Get figure dimensions for intelligent sizing
            img_widths = []
            for fid in figs:
                fp = FIGURES_DIR / f"fig-{fid:02d}.png"
                if fp.exists():
                    w, h = Image.open(fp).size
                    img_widths.append((fid, w, h))

            total_content += 1
            if figs and img_widths:
                # Use first figure; if image is small (<500px), display larger
                fid, w, h = img_widths[0]
                is_small = w < 500 or h < 300
                style = 'max-height:320px' if not is_small else 'max-height:420px;max-width:100%'

                slides_html.append(
                    f'<section data-state="content" class="content-slide">'
                    f'<div class="slide-flex">'
                    f'<div class="slide-text">'
                    f'<p class="sn">{sec_title}</p><h2>{title}</h2>'
                    f'<ul>\n{bullet_lis}</ul></div>'
                    f'<div class="slide-img" style="flex:0 0 38%">'
                    f'<img src="figures/fig-{fid:02d}.png" style="{style}">'
                    f'</div></div>{notes_html}</section>'
                )
                if len(figs) > 1:
                    # Additional figures as separate image-only slides
                    for fid2, w2, h2 in img_widths[1:]:
                        is_small2 = w2 < 500 or h2 < 300
                        style2 = 'max-height:320px' if not is_small2 else 'max-height:420px;max-width:100%'
                        slides_html.append(
                            f'<section data-state="content" class="content-slide">'
                            f'<div class="iw"><img src="figures/fig-{fid2:02d}.png" style="{style2}">'
                            f'</div></section>'
                        )
            else:
                slides_html.append(
                    f'<section data-state="content" class="content-slide">'
                    f'<p class="sn">{sec_title}</p><h2>{title}</h2>'
                    f'<ul>\n{bullet_lis}</ul>{notes_html}</section>'
                )

    all_s = '\n'.join(slides_html)
    total_slides = slides_html.count('</section>') + 1

    html = '''<!DOCTYPE html><html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>第7章 · 铸造 - 课件</title>
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
.content-slide h2{font-size:24px;margin:0 0 6px;color:#1a1a1a;border-bottom:2px solid #e03020;padding-bottom:3px;display:inline-block}
.content-slide p{font-size:18px;line-height:1.5;margin:0 0 3px;color:#333}
.content-slide ul{display:block;list-style:none;padding:0;margin:4px 0}
.content-slide li{font-size:17px;line-height:1.5;margin:2px 0;padding:2px 0 2px 20px;position:relative;color:#333}
.content-slide li:before{content:"\\25B8";position:absolute;left:0;color:#e03020;font-size:15px}
.slide-flex{display:flex;gap:16px;align-items:center}
.slide-text{flex:1;min-width:0}
.slide-img{text-align:center}
.slide-img img{border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.08);max-width:100%%}
.iw{text-align:center;margin:10px 0}
.iw img{border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.08);max-width:100%%}
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
</script></body></html>''' % all_s

    open('ch07-铸造.html', 'w', encoding='utf-8').write(html)
    print(f"[OK] ch07-铸造.html ({total_slides} slides)")
    fig_count = sum(1 for s in slides_html if 'fig-0' in s or 'fig-1' in s or 'fig-2' in s or 'fig-3' in s or 'fig-4' in s)
    print(f"      Figures used: ~{fig_count}")

if __name__ == '__main__':
    main()
