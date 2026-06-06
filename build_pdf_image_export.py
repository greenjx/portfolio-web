from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "薛婧睿-作品集.pdf"
PAGE_W, PAGE_H = 1240, 1754
M = 104

INK = "#30261f"
BRICK = "#b95448"
GOLD = "#f3d98b"
CREAM = "#fff3ca"
PAPER = "#fffaf0"
NIGHT = "#22313a"
WATER = "#4db7be"
GRID = "#d7bf7a"
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"


def font(size):
    return ImageFont.truetype(FONT_PATH, size=size, index=0)


F16 = font(16)
F20 = font(20)
F24 = font(24)
F26 = font(26)
F30 = font(30)
F38 = font(38)
F52 = font(52)


def asset(path):
    return ROOT / path


def page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), GOLD)
    d = ImageDraw.Draw(img)
    for x in range(0, PAGE_W, 52):
        d.line((x, 0, x, PAGE_H), fill=GRID, width=1)
    for y in range(0, PAGE_H, 52):
        d.line((0, y, PAGE_W, y), fill=GRID, width=1)
    return img


def text(draw, xy, value, fnt, fill=INK, max_width=None, line_gap=8):
    x, y = xy
    if not max_width:
        draw.text((x, y), value, font=fnt, fill=fill)
        return y + fnt.size + line_gap
    line = ""
    for ch in value:
        w = draw.textlength(line + ch, font=fnt)
        if w <= max_width:
            line += ch
        else:
            draw.text((x, y), line, font=fnt, fill=fill)
            y += fnt.size + line_gap
            line = ch
    if line:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def header(img, title, subtitle):
    d = ImageDraw.Draw(img)
    x, y, w, h = M, 92, PAGE_W - 2 * M, 160
    d.rectangle((x, y, x + w, y + h), fill=PAPER, outline=INK, width=3)
    d.text((x + 44, y + 36), subtitle, font=F20, fill=BRICK)
    d.text((x + 44, y + 82), title, font=F52, fill=INK)
    return y + h + 42


def paste_fit(base, path, box, bg=PAPER, border=True):
    x, y, w, h = box
    d = ImageDraw.Draw(base)
    d.rectangle((x, y, x + w, y + h), fill=bg)
    im = Image.open(path).convert("RGB")
    im.thumbnail((w - 24, h - 24), Image.Resampling.LANCZOS)
    px = x + (w - im.width) // 2
    py = y + (h - im.height) // 2
    base.paste(im, (px, py))
    if border:
        d.rectangle((px - 4, py - 4, px + im.width + 4, py + im.height + 4), outline="#8a7a5a", width=2)


def label(draw, x, y, value):
    draw.rectangle((x, y, x + 220, y + 54), fill=BRICK)
    tw = draw.textlength(value, font=F24)
    draw.text((x + (220 - tw) / 2, y + 13), value, font=F24, fill=CREAM)


def cover():
    img = page()
    d = ImageDraw.Draw(img)
    d.rectangle((M, 140, PAGE_W - M, 300), fill=NIGHT)
    d.text((M + 58, 192), "薛婧睿-作品集", font=F52, fill=CREAM)
    d.text((M + 58, 255), "Creator / Writer / Visual Explorer", font=F20, fill=BRICK)
    paste_fit(img, asset("assets/photos/avatar-original.jpg"), (M + 40, 410, 300, 300))
    y = 420
    x = M + 400
    y = text(d, (x, y), "27届广播电视编导专业在读", F26, max_width=PAGE_W - M - x)
    y = text(d, (x, y), "意向工作地点：全国｜可实习六个月以上", F26, max_width=PAGE_W - M - x)
    y = text(d, (x, y), "微信：18709853879", F26, max_width=PAGE_W - M - x)
    y = text(d, (x, y), "邮箱：lianqiaoooo@163.com", F26, max_width=PAGE_W - M - x)
    d.rectangle((M, 1220, PAGE_W - M, 1456), fill=PAPER)
    text(d, (M + 48, 1282), "在影像、文本与传播的三条岔路上，拼凑关于我的碎片。", F34 if False else F30, max_width=PAGE_W - 2 * M - 96)
    return img


def image_grid_pages(title, subtitle, items, cols=2):
    pages = []
    rows = 2 if cols > 1 else 1
    per_page = cols * rows
    gap = 48
    box_w = (PAGE_W - 2 * M - gap * (cols - 1)) // cols
    box_h = 330 if cols > 1 else 880
    for start in range(0, len(items), per_page):
        img = page()
        d = ImageDraw.Draw(img)
        top = header(img, title, subtitle)
        for i, (name, path) in enumerate(items[start : start + per_page]):
            row, col = divmod(i, cols)
            x = M + col * (box_w + gap)
            y = top + row * (box_h + 112)
            label(d, x, y, name)
            paste_fit(img, path, (x, y + 72, box_w, box_h))
        pages.append(img)
    return pages


def script_pages(items):
    pages = []
    for category, tag, path in items:
        img = page()
        d = ImageDraw.Draw(img)
        top = header(img, "剧本策划", category)
        d.rectangle((M, top, PAGE_W - M, top + 64), fill=PAPER)
        d.text((M + 34, top + 17), tag, font=F26 if False else F24, fill=BRICK)
        paste_fit(img, path, (M + 58, top + 106, PAGE_W - 2 * M - 116, PAGE_H - top - 150))
        pages.append(img)
    return pages


def account_pages(items):
    pages = []
    for name, stats, path in items:
        img = page()
        d = ImageDraw.Draw(img)
        top = header(img, "运营宣传", "ACCOUNT WORKS")
        d.rectangle((M, top, PAGE_W - M, top + 72), fill=PAPER)
        d.text((M + 34, top + 20), name, font=F30, fill=INK)
        if stats:
            d.text((PAGE_W - M - 470, top + 23), stats, font=F24, fill=BRICK)
        paste_fit(img, path, (M + 280, top + 112, PAGE_W - 2 * M - 560, PAGE_H - top - 170))
        pages.append(img)
    return pages


def identity_page():
    img = page()
    d = ImageDraw.Draw(img)
    top = header(img, "身份卡片", "PLAYER INFO")
    lines = [
        "薛婧睿｜Pay attention. Be astonished. Tell about it.",
        "专业背景：27届广播电视编导专业在读",
        "工作地点：全国",
        "可实习：六个月以上",
        "微信：18709853879",
        "邮箱：lianqiaoooo@163.com",
    ]
    y = top + 10
    for line in lines:
        y = text(d, (M + 44, y), line, F30, max_width=PAGE_W - 2 * M - 88)
    bubbles = [
        "王者荣耀50+星老农民，欢迎偷我菜",
        "专业陪拍，出片能手，快揣上我出去玩吧",
        "性格抽象，好相处",
        "有一万种抠门生活小技巧",
        "国乙氪金玩家",
    ]
    y += 38
    for i, b in enumerate(bubbles):
        fill = "#d8eef0" if i % 2 == 0 else CREAM
        d.rectangle((M + 44, y, PAGE_W - M - 44, y + 70), fill=fill, outline="#8a7a5a", width=2)
        d.text((M + 78, y + 19), b, font=F24, fill=INK)
        y += 92
    return img


def build():
    pages = [cover()]
    pages += image_grid_pages("影像作品", "PHOTO WORKS", [
        ("剧照 01", asset("assets/photos/still-01.jpg")),
        ("剧照 02", asset("assets/photos/still-02.jpg")),
        ("剧照 03", asset("assets/photos/still-03.jpg")),
        ("街拍 01", asset("assets/photos/street-01.jpg")),
        ("街拍 02", asset("assets/photos/street-02.jpg")),
        ("街拍 03", asset("assets/photos/street-03.jpg")),
        ("街拍 04", asset("assets/photos/street-04.jpg")),
    ], cols=2)
    pages += image_grid_pages("影像作品", "PORTRAIT", [
        ("写真 01", asset("assets/photos/portrait-01.jpg")),
        ("写真 02", asset("assets/photos/portrait-02.jpg")),
        ("写真 03", asset("assets/photos/portrait-03.jpg")),
        ("写真 04", asset("assets/photos/portrait-04.jpg")),
    ], cols=2)
    pages += script_pages([
        ("长剧", "古装 / 悬疑 / 喜剧", asset("assets/script-shots/long-01.png")),
        ("长剧", "古装 / 悬疑 / 喜剧", asset("assets/script-shots/long-02.png")),
        ("短剧", "大女主1", asset("assets/script-shots/short-danv-01.png")),
        ("短剧", "大女主2", asset("assets/script-shots/short-danv-02.png")),
        ("短剧", "乙女漫", asset("assets/script-shots/short-yinvman.png")),
        ("短剧", "现言1", asset("assets/script-shots/short-xianyan-01.png")),
        ("短剧", "现言2", asset("assets/script-shots/short-xianyan-02.png")),
        ("中剧", "青春 / 现言 / 甜宠", asset("assets/script-shots/mid-01.png")),
        ("中剧", "青春 / 现言 / 甜宠", asset("assets/script-shots/mid-02.png")),
        ("策划评估", "女性悬疑改编1", asset("assets/script-shots/plan-female-suspense-01.png")),
        ("策划评估", "女性悬疑改编2", asset("assets/script-shots/plan-female-suspense-02.png")),
    ])
    pages += account_pages([
        ("抖音 01", "点赞 8.9万｜收藏 1863", asset("assets/account/douyin-01.jpg")),
        ("抖音 02", "点赞 45.7万｜收藏 1.7万", asset("assets/account/douyin-02.jpg")),
        ("抖音 03", "点赞 61.4万｜收藏 1.5万", asset("assets/account/douyin-03.jpg")),
        ("小红书", "", asset("assets/account/redbook-01.jpg")),
        ("B站 01", "", asset("assets/account/bilibili-01.jpg")),
        ("B站 02", "", asset("assets/account/bilibili-02.jpg")),
        ("B站 03", "", asset("assets/account/bilibili-03.jpg")),
        ("微博 01", "", asset("assets/account/weibo-01.jpg")),
        ("微博 02", "", asset("assets/account/weibo-02.jpg")),
    ])
    pages += image_grid_pages("AI实验室", "SCENE / ANCHOR", [
        ("主视觉", asset("assets/ai-lab/anchor-01.jpg")),
        ("锚点 02", asset("assets/ai-lab/anchor-02.jpg")),
        ("锚点 03", asset("assets/ai-lab/anchor-03.jpg")),
        ("锚点 04", asset("assets/ai-lab/anchor-04.jpg")),
    ], cols=2)
    pages += image_grid_pages("AI实验室", "STORYBOARD", [("分镜", asset("assets/ai-lab/storyboard-01.jpg"))], cols=1)
    pages += image_grid_pages("AI实验室", "KEY FRAMES", [
        ("关键静帧 01", asset("assets/ai-lab/still-01.png")),
        ("关键静帧 02", asset("assets/ai-lab/still-02.jpg")),
    ], cols=1)
    pages.append(identity_page())

    pages[0].save(OUT, save_all=True, append_images=pages[1:], resolution=150.0, quality=86)
    print(OUT)


if __name__ == "__main__":
    build()
