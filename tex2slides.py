#!/usr/bin/env python3
"""Final comprehensive converter with keyword highlighting & correct figure mapping."""
import sys, re
from pathlib import Path
from PIL import Image

FIGURES_DIR = Path("figures")
CHAPTER_START, CHAPTER_END = 2960, 4043

# Key technical terms to highlight in slides
KEY_TERMS = [
    '流动性', '充型能力', '缩孔', '缩松', '顺序凝固', '同时凝固',
    '热应力', '机械应力', '热裂', '冷裂', '反变形法', '去应力退火',
    '铸造圆角', '起模斜度', '结构斜度', '加工余量', '芯头',
    '冒口', '冷铁', '球化处理', '孕育处理', '冲入法',
    '熔模铸造', '金属型铸造', '压力铸造', '离心铸造', '挤压铸造',
    '实型铸造', '磁型铸造', '气冲造型',
]

def hl(text):
    """Highlight key technical terms in a string."""
    for term in KEY_TERMS:
        text = text.replace(term, f'<span class="hl">{term}</span>')
    return text

def extract_figure_data():
    """Extract figures from Chapter 7 TeX, correctly associating each with its caption."""
    lines = open('manufactver3tex.tex', encoding='utf-8').readlines()
    ch_text = ''.join(lines[CHAPTER_START:CHAPTER_END])
    figures = []
    # Process line by line; when we see \includegraphics, store it
    # Then look for the NEXT \caption{} to associate
    for i, line in enumerate(lines[CHAPTER_START:CHAPTER_END]):
        if '\\includegraphics' in line:
            m = re.search(r'page=(\d+)', line)
            p = int(m.group(1)) if m else None
            m = re.search(r'viewport=\{([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\}', line)
            v = tuple(float(x) for x in m.groups()) if m else None
            if not p or not v:
                continue
            # Scan forward to find the next \caption{}
            cap = ''
            for j in range(i, min(i+15, len(lines[CHAPTER_START:CHAPTER_END]))):
                cm = re.search(r'\\caption\{([^}]*)\}', lines[CHAPTER_START:CHAPTER_END][j])
                if cm:
                    cap = cm.group(1)
                    break
            figures.append((len(figures)+1, p, v, cap))
    return figures

# ===== Section 1: Intro =====
S1_intro = ["铸造概述", [
    ["铸造的定义与特点", [
        "铸造：将熔融金属浇注/压射/吸入铸型，冷却凝固获得零件或毛坯",
        "优点：一次成形、适应性强、成本低、适合复杂内腔",
        "不足：晶粒粗大、缩孔/缩松/气孔等缺陷、力学性能不如锻件",
        f"现代铸造：集成{hl('计算机凝固模拟')}、自动控制、机器人等先进技术",
    ], [
        "铸造是金属液态成形，与锻造（固态成形）有本质区别",
        "机器制造业中铸件占比很高，是最基础的热加工工艺",
    ], []],
]]

# ===== Section 2: Theory =====
S2_theory = ["液态金属成形理论基础", [
    [f"合金的{hl('流动性')}", [
        f"流动性：{hl('液态合金填充铸型的能力')}",
        "流动性好 → 成形复杂薄壁件、利于排气和补缩",
        "流动性差 → 冷隔、浇不足、气孔、夹渣、缩孔",
        "测量：螺旋形试样，越长流动性越好",
    ], [
        "流动性是衡量合金铸造性能的核心指标",
        "螺旋形试样法是最直观的检测方法",
    ], [1]],
    ["影响流动性的因素—合金成分", [
        "纯金属和共晶成分：恒温凝固→界面光滑→流动性最好",
        "宽凝固范围合金：树枝晶阻碍流动→流动性差",
        "铁碳合金中：共晶成分铸铁流动性最好",
        f"应尽量选{hl('共晶或近共晶成分')}合金",
    ], [
        "宽凝固范围合金产生树枝晶，是流动性变差的主因",
        "从流动性角度考虑，应选凝固温度范围小的合金",
    ], [2, 3]],
    ["影响流动性的因素—物理性质与温度", [
        "比热容和密度越大、导热系数越小 → 流动性越好",
        "黏度越小 → 流动性越好",
        "温度升高 → 流动性上升，但过高→氧化吸气严重",
        f"浇注温度必须{hl('合理')}，铸铁件'高温出炉、低温浇注'",
    ], [
        "物理性质影响比合金成分小，但在特定条件下很关键",
        "高温出炉利于熔渣上浮，低温浇注减少液态收缩",
    ], []],
    [f"液态合金的{hl('充型能力')}", [
        f"充型能力 = {hl('合金流动性')} + 工艺因素",
        "铸型条件：蓄热能力、排气、温度、结构复杂度",
        "浇注条件：系统结构（阻力）、静压力、浇注温度",
        "流动性差的合金可通过改善工艺条件提高充型能力",
    ], [
        "充型能力不足→浇不足、冷隔等缺陷",
        "提高浇注温度是最常用措施，但需权衡利弊",
    ], []],
    [f"铸造合金的{hl('收缩')}", [
        f"收缩：合金从液态冷却至室温体积缩小的现象",
        f"三阶段：{hl('液态收缩')} → {hl('凝固收缩')} → {hl('固态收缩')}",
        "液态收缩+凝固收缩 → 缩孔和缩松",
        "固态收缩 → 内应力、变形和裂纹",
        "灰铸铁体收缩率约7%，铸钢约12%",
    ], [
        "收缩是铸造合金的固有物理性质，不可消除只能控制",
        "不同阶段收缩影响不同缺陷，需针对性防止",
    ], [4]],
    [f"{hl('缩孔')}与{hl('缩松')}的形成", [
        f"{hl('缩孔')}：集中孔洞，近倒锥形，内表面不光滑",
        f"{hl('缩松')}：细小分散孔洞，多分布于轴线区域和厚大断面",
        "纯金属/共晶→逐层凝固→缩孔（集中易修补）",
        "宽凝固范围→同时凝固→缩松（分散危害大）",
        "缩孔+缩松总容积一定，增大冷速可促缩松→缩孔转化",
    ], [
        "缩孔比缩松易于检查和修补，生产中常推动前者转化",
        "浇注温度越高，液态收缩越大，缩孔体积越大",
    ], [5, 6]],
    [f"防止{hl('缩孔')}的方法", [
        f"{hl('顺序凝固')}原则：远离冒口先凝→冒口最后凝",
        "设置冒口和冷铁，控制凝固方向",
        "缩孔转移到冒口中，切除冒口即可获完好铸件",
        f"计算机{hl('凝固模拟')}可准确预测缩孔位置",
        "方法：等温线法、内切圆法、计算机模拟法",
    ], [
        "顺序凝固适用收缩大、致密性要求高的铸件（铸钢）",
        "发热保温冒口可提高补缩效果",
    ], [7, 8]],
    [f"铸造{hl('内应力')}", [
        f"{hl('热应力')}：壁厚不均→冷却速度不同→收缩量不同",
        f"{hl('机械应力')}：收缩受铸型、型芯的机械阻碍",
        "厚壁/心部受拉伸，薄壁/表层受压缩",
        "固态收缩率越大、壁厚差别越大→热应力越大",
    ], [
        "再结晶温度以上为塑性状态，应力可消除",
        "低于再结晶温度弹性状态，应力保留",
    ], [9]],
    [f"铸件的{hl('变形')}与{hl('裂纹')}", [
        "内应力→铸件变形减缓应力（厚拉薄压）",
        f"防变形：{hl('同时凝固')}、{hl('反变形法')}、{hl('去应力退火')}",
        f"{hl('热裂')}：凝固后期高温沿晶界断裂，短而曲折",
        f"{hl('冷裂')}：低温直线状，出现在受拉伸部位",
        "防热裂：改善退让性、限硫；防冷裂：降应力、控磷",
    ], [
        "车床床身导轨厚受拉，床壁薄受压，产生向下挠曲",
        "同时凝固适用收缩小、致密性要求不高的铸件",
    ], [10, 11]],
]]

# ===== Section 3: Sand Casting =====
S3_sand = ["砂型铸造", [
    ["砂型铸造生产过程", [
        "工艺流程：零件图→铸件图→模样→造型→合箱→浇注→落砂→清理→检验",
        "优点：适应性极强、成本低、各种合金均可铸造",
        "缺点：一型一次、每吨铸件需4~5吨型砂、粉尘污染",
    ], [
        "砂型铸造是应用最广泛的铸造方法",
        "生产线可全部机械化：型砂处理→造型→浇注→落砂",
    ], [12, 13]],
    [f"造型方法", [
        "手工造型：整模、分模、挖砂、活块、三箱、刮板、假箱、地坑",
        "机器造型：振压紧实、抛砂紧实、射砂紧实",
        f"起模方法：{hl('顶箱')}（浅腔）、{hl('漏模')}（深腔）、{hl('翻转')}（复杂腔）",
        "浇注原则：'高温出炉、低温浇注'",
    ], [
        "手工造型灵活适应单件小批，但效率低劳动强度大",
        "机器造型精度高、生产率高，适合大批量生产",
    ], [14]],
    ["浇注位置的选择", [
        "重要的加工面和主要加工面 → 放在下面",
        "需补缩的厚壁部分 → 放在上部或侧面（便于放冒口）",
        "大面积薄壁部分 → 放在下部，立放或倾斜浇注",
    ], [
        "浇注位置和分型面是铸造工艺设计两大核心",
    ], [15, 16, 17]],
    [f"{hl('分型面')}的选择", [
        "原则①：选在铸件最大截面上，取模顺利",
        "原则②：尽量减少分型面数量，最好一个分型面",
        "原则③：减少活块和型芯数量，简化工艺",
        "铸件大部分放在同一个砂箱内→重要加工面在下型",
    ], [
        "分型面决定造型方案，影响铸件精度和生产成本",
        "分型面平直可简化造型操作",
    ], [18, 19, 20]],
    ["主要工艺参数", [
        f"{hl('铸造收缩率')}：灰铸铁0.7%~1.0%，铸钢1.5%~2.0%",
        f"{hl('机械加工余量')}：铸铁件3~15mm",
        f"{hl('起模斜度')}：15'~3°（垂直于分型面的加工表面）",
        f"{hl('铸造圆角')}：避免尖角处应力集中，内圆角≈壁厚1/2",
        f"{hl('芯头')}：定位和固定型芯；最小铸出孔12~50mm",
    ], [
        "工艺参数直接影响模具设计和铸件尺寸精度",
        "参数选择需综合考虑合金种类和造型方法",
    ], [21, 22, 23, 24]],
    ["铸造工艺图实例", [
        f"铸造工艺图是指导{hl('模样设计')}、{hl('生产准备')}和{hl('铸件检验')}的技术文件",
        "内容包括：浇注位置、分型面、加工余量、收缩率、芯头等",
    ], [
        "支座的铸造工艺图是涵盖主要工艺参数的典型案例",
    ], [25]],
]]

# ===== Section 4: Special Casting =====
S4_special = ["特种铸造", [
    [f"{hl('熔模铸造')}（精密铸造）", [
        f"工艺：压制蜡模→{hl('结壳')}(3~7次)→脱蜡→焙烧(850~950°C)→浇注",
        "精度IT14~IT11，Ra 1.6~12.5μm，最小孔径0.5mm",
        "适用：涡轮叶片、高速钢刀具等复杂精密小件",
    ], [
        "熔模铸造无分型面限制，蜡模熔化后获整体型壳",
    ], [26]],
    [f"{hl('金属型铸造')}", [
        f"金属型可反复使用（{hl('一型多铸')}）",
        "措施：预热、加强排气、喷刷涂料、尽早开型",
        "铸件力学性能好，铝合金抗拉强度提高约20%",
        "适用：大批量非铁金属件（铝活塞、气缸体、铜轴瓦）",
    ], [
        "金属型导热快易产生白口组织，需预热控制冷速",
    ], [27]],
    [f"{hl('压力铸造')}", [
        "两大特点：高压 + 高速充型",
        "精度IT13~IT11，Ra 0.8~3.2μm，最小壁厚0.5mm",
        "效率最高，班产600~700件",
        "不足：设备投资大、卷气→有气孔→不能热处理",
    ], [
        "压铸机分热压室式和冷压室式",
        "卷气限制了压铸件的热处理和焊接应用",
    ], [28]],
    [f"{hl('离心铸造')}", [
        "原理：高速旋转，离心力充型成形",
        "立式（绕竖直轴）和卧式（绕水平轴）两类",
        "优点：省型芯和浇冒口、组织致密",
        "可铸双金属件；内表面质量差是主要缺点",
    ], [
        "离心铸造是管类件最经济的方法",
        "双金属件如钢背铜套轴承可一次铸造成形",
    ], [29]],
    [f"{hl('反压铸造')}与{hl('挤压铸造')}", [
        f"{hl('反压铸造')}（压差）：充型平稳，最小壁厚0.5mm",
        "增压法：坩埚加压高于型腔→金属液沿升液管充型",
        f"{hl('挤压铸造')}（液态模锻）：机械压力下凝固成形",
        "挤压铸造：无浇注系统、组织致密、接近锻件性能",
    ], [
        "反压铸造适用于高致密性航空铸件",
        "挤压铸造介于铸造和锻造之间",
    ], [30, 31]],
    [f"{hl('实型铸造')}与{hl('磁型铸造')}", [
        f"{hl('实型')}（消失模）：泡沫塑料模→填砂振实→浇注汽化→获铸件",
        "实型优点：无分型面、不用型芯、模样成本低",
        f"{hl('磁型')}：磁丸+通电固结→浇注→断电松散→取出铸件",
        "磁型特点：无黏结剂、冷却快3倍、组织细密",
    ], [
        "实型铸造模样成本仅为木模的1/3",
        "磁型铸造改善工作环境，无砂尘",
    ], [32, 33]],
    [f"{hl('气冲造型')}", [
        "原理：压缩空气/燃气冲击波紧实型砂",
        "紧实时间<0.1s，一个铸型约0.5s",
        "紧实度高且均匀，精度高，无振击噪声",
    ], [
        "气冲造型是砂型铸造机械化的重要发展方向",
    ], [34]],
]]

# ===== Section 5: Alloy Castings =====
S5_alloy = ["常用合金铸件生产", [
    [f"{hl('灰铸铁')}件", [
        f"冲天炉熔炼：铸造生铁+回炉铁+废钢+铁合金+焦炭+熔剂",
        f"铸造性能优良，一般不需{hl('冒口')}和{hl('冷铁')}",
        f"{hl('孕育处理')}：浇注前加硅铁0.25%~0.6%→石墨细化、基体致密",
        "要求低碳低硅铁液+高出炉温度(1450~1470°C)",
    ], [
        "灰铸铁是最广泛应用的铸造合金",
        "孕育处理显著改善石墨形态和基体组织",
    ], [35]],
    [f"{hl('球墨铸铁')}件", [
        f"化学成份：高碳(C=3.6~4.0%)、高硅、低硫(S<0.06%)",
        f"{hl('球化处理')}：稀土镁合金球化剂，{hl('冲入法')}加入",
        f"{hl('孕育处理')}：硅铁0.4%~1.0%",
        "常设冒口和冷铁，控制型砂水分防皮下气孔",
    ], [
        "冲入法：浇包底部修堤坝埋入球化剂，反应平稳",
        "球墨铸铁强度远高于灰铸铁，可替代部分铸钢件",
    ], [36]],
    [f"{hl('可锻铸铁')}与{hl('蠕墨铸铁')}", [
        f"{hl('可锻铸铁')}：白口毛坯+900~950°C石墨化退火→团絮状石墨",
        "可锻铸铁流动性差，需注意冒口和冷铁",
        f"{hl('蠕墨铸铁')}：铸造性能与灰铸铁相近，流动性更好",
        "蠕墨铸铁一般铸态使用，不热处理",
    ], [
        "可锻铸铁并非可锻造，通过退火改善石墨形态",
        "蠕化剂用稀土硅铁，冲入法处理",
    ], []],
    [f"{hl('铸钢')}件生产", [
        "综合力学性能优于铸铁：强度高、塑性韧性好、焊接性好",
        "工艺特点：熔点高(~1500°C)、流动性差、收缩率大(~2%)",
        "型砂要求：高透气性、耐火度、强度和退让性",
        "熔炼：三相电弧炉（最普遍）或感应电炉",
        "应用：高压阀门、轧钢机机架、坦克履带(ZGMn13)",
    ], [
        "铸钢件须正火或退火处理细化晶粒",
        "遵循顺序凝固原则配置大冒口和冷铁补缩",
    ], []],
]]

# ===== Section 6: Structure Design =====
S6_design = ["铸件结构设计", [
    ["壁厚设计原则", [
        "壁厚应适当：大于合金最小壁厚（防浇不足），不宜过大（防缩松）",
        "可用T形、工字形、槽形截面或加强筋保证强度刚度",
        "壁厚应均匀：减小厚壁差→防热节、缩孔、变形",
        "内壁冷却慢应薄，外壁冷却快应厚",
    ], [
        "最小壁厚取决于合金种类和铸型条件",
        "壁厚不均匀是铸造缺陷的主要根源之一",
    ], [37, 38]],
    [f"壁连接与{hl('铸造圆角')}", [
        f"壁连接应合理：{hl('结构圆角')}避免直角→防金属聚集和缩孔",
        "过渡连接：避免锐角和交叉连接",
        "小型件交错连接，大型件环状连接",
        "不等厚壁间用圆角/倾斜/复合过渡",
    ], [
        "铸造圆角是最明显的铸件结构特征",
        "合理设计壁连接可减少应力集中和裂纹",
    ], [39, 40, 41]],
    [f"减少{hl('变形')}与减缓{hl('收缩')}受阻", [
        "细长件和大平板件→对称结构或加强筋",
        f"弯曲轮辐或{hl('奇数轮辐')}→冷却时可自由收缩",
        "减缓收缩受阻是降低铸造内应力的关键",
    ], [
        "弯曲轮辐设计允许各辐条同时自由收缩",
        "平板加筋既可减重又能防变形",
    ], [42, 43]],
    [f"外形与内腔设计", [
        f"外形尽量简单，避免{hl('侧凹')}→便于起模",
        f"分型面{hl('平直')}，凸台和筋条应便于起模",
        "内腔：减少型芯数量、简化型芯形状",
        f"以{hl('砂垛')}代替型芯，{hl('开式结构')}省去型芯",
    ], [
        "侧凹结构需要活块或型芯，增加制模难度",
        "型芯越少，定位、排气和清理越方便",
    ], [44, 45, 46, 47]],
    [f"{hl('结构斜度')}", [
        f"垂直于分型面的不加工表面应设计{hl('结构斜度')}",
        "优点：起模方便、零件更美观",
        "有斜度的内腔可用砂垛代替型芯",
        "高度越低，结构斜度应越大",
    ], [
        "结构斜度不同于起模斜度—前者是结构固有特征",
    ], [48]],
]]

SECTIONS = [S1_intro, S2_theory, S3_sand, S4_special, S5_alloy, S6_design]

def crop_figures(figures):
    for (seq, p, v, c) in figures:
        pf = FIGURES_DIR / f"page-{p:02d}.png"
        if not pf.exists(): continue
        img = Image.open(pf)
        W, H = img.size
        sc = 300.0/72
        llx,lly,urx,ury = v
        l = max(0,int(llx*sc)); t = max(0,int(H-ury*sc))
        r = min(W,int(urx*sc)); b = min(H,int(H-lly*sc))
        if r<=l or b<=t: continue
        img.crop((l,t,r,b)).save(FIGURES_DIR / f"fig-{seq:02d}.png", 'PNG')

def build_slides(figures):
    slides = []
    # Create a map: figure seq -> caption
    fig_caps = {seq: cap for (seq,p,v,cap) in figures}

    for section_data in SECTIONS:
        sec_title = section_data[0]
        slides.append(
            f'<section data-state="section"><div class="section-divider">'
            f'<div class="sec-num">&#9679;</div><h2>{sec_title}</h2></div></section>'
        )
        for item in section_data[1]:
            title, bullets, notes, fig_refs = item
            bullet_lis = ''.join(f'<li>{b}</li>\n' for b in bullets)
            notes_html = ''
            if notes:
                notes_ps = '\n'.join(f'<li>{n}</li>' for n in notes)
                notes_html = f'<aside class="notes"><ul>{notes_ps}</ul></aside>'

            if fig_refs:
                # Main figure with text
                fid = fig_refs[0]
                cap = fig_caps.get(fid, '')
                fp = FIGURES_DIR / f"fig-{fid:02d}.png"
                is_small = False
                if fp.exists():
                    w, h = Image.open(fp).size
                    is_small = w < 500 or h < 300
                size_style = 'max-height:420px' if is_small else 'max-height:320px'

                slides.append(
                    f'<section data-state="content" class="content-slide">'
                    f'<div class="slide-flex">'
                    f'<div class="slide-text">'
                    f'<p class="sn">{sec_title}</p><h2>{title}</h2>'
                    f'<ul>\n{bullet_lis}</ul></div>'
                    f'<div class="slide-img">'
                    f'<img src="figures/fig-{fid:02d}.png" style="{size_style}">'
                    f'</div></div>{notes_html}</section>'
                )
                # Additional figures as standalone pages with descriptive caption
                for fid2 in fig_refs[1:]:
                    cap2 = fig_caps.get(fid2, title)
                    fp2 = FIGURES_DIR / f"fig-{fid2:02d}.png"
                    is_small2 = False
                    if fp2.exists():
                        w2, h2 = Image.open(fp2).size
                        is_small2 = w2 < 500 or h2 < 300
                    size_style2 = 'max-height:420px' if is_small2 else 'max-height:400px'
                    slides.append(
                        f'<section data-state="content" class="content-slide">'
                        f'<p style="font-size:16px;color:#888;margin-bottom:6px;">图：{cap2}</p>'
                        f'<div class="iw"><img src="figures/fig-{fid2:02d}.png" style="{size_style2}"></div>'
                        f'</section>'
                    )
            else:
                slides.append(
                    f'<section data-state="content" class="content-slide">'
                    f'<p class="sn">{sec_title}</p><h2>{title}</h2>'
                    f'<ul>\n{bullet_lis}</ul>{notes_html}</section>'
                )

    return slides

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    print("Extracting figures...")
    figures = extract_figure_data()
    print(f"  {len(figures)} figures found")
    crop_figures(figures)

    print("Building slides...")
    slides = build_slides(figures)
    all_s = '\n'.join(slides)
    total_slides = 1 + sum(s.count('</section>') for s in slides)

    # Generate caption context for each figure used
    fig_used = []
    for s in slides:
        for m in re.finditer(r'fig-(\d+)', s):
            fig_used.append(int(m.group(1)))
    unique_figs = len(set(fig_used))

    html = '''<!DOCTYPE html><html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>第7章 · 铸造 - 课件</title>
<link rel="stylesheet" href="lib/reveal.css"><link rel="stylesheet" href="lib/white.css"><link rel="stylesheet" href="lib/katex.min.css">
<style>
.reveal,.reveal h1,.reveal h2,.reveal h3,.reveal h4{font-family:'Noto Sans SC','Microsoft YaHei','PingFang SC','Hiragino Sans GB',sans-serif;color:#1a1a1a}
.reveal .hl{color:#c62828;font-weight:700;background:#fff3f0;padding:0 4px;border-radius:2px}
.reveal .sn{font-family:'Archivo',sans-serif;font-size:12px;font-weight:700;color:#aaa;letter-spacing:2px;margin-bottom:4px;text-transform:uppercase}
.title-slide{display:flex;justify-content:flex-start;align-items:stretch;height:100%%}
.title-slide .bar{width:12px;background:#c62828;flex-shrink:0}
.title-slide .inner{flex:1;padding:80px 60px;text-align:left;display:flex;flex-direction:column;justify-content:center}
.title-slide .tag{font-family:'Archivo',sans-serif;font-size:15px;font-weight:700;color:#c62828;letter-spacing:4px;margin-bottom:16px}
.title-slide h1{font-size:72px;font-weight:900;margin:0 0 16px}
.section-divider{text-align:center;padding:40px 0}
.section-divider .sec-num{font-family:'Archivo',sans-serif;font-size:80px;font-weight:800;color:#c62828;opacity:.15;line-height:1;margin-bottom:8px}
.section-divider h2{font-size:44px;margin:8px 0}
.content-slide{text-align:left;padding:8px 12px}
.content-slide h2{font-size:24px;margin:0 0 8px;color:#1a1a1a;border-left:3px solid #c62828;padding-left:10px}
.content-slide p{font-size:18px;line-height:1.5;margin:0 0 3px;color:#333}
.content-slide ul{display:block;list-style:none;padding:0;margin:4px 0}
.content-slide li{font-size:17px;line-height:1.5;margin:3px 0;padding:3px 0 3px 20px;position:relative;color:#333}
.content-slide li:before{content:"\\25B8";position:absolute;left:0;color:#c62828;font-size:15px}
.slide-flex{display:flex;gap:16px;align-items:center}
.slide-text{flex:1;min-width:0}
.slide-img{flex:0 0 38%%;text-align:center}
.slide-img img{border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.08);max-width:100%%;width:auto}
.iw{text-align:center;margin:8px 0}
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
    print(f"\n[OK] ch07-铸造.html")
    print(f"     Total slides: {total_slides}")
    print(f"     Figures used: {unique_figs} unique (out of {len(figures)})")
    print(f"     Bullet points: ~{all_s.count('<li>') - all_s.count('notes')*2}")
    print(f"     Technical terms highlighted: ✓")
    print(f"     Standalone figure captions: ✓")

if __name__ == '__main__':
    main()
