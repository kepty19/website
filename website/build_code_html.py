#!/usr/bin/env python3
# Verbatim brochure → code.html + SEO/AIO helpers (prompt.txt).
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "kepty_ordered.txt"
DST = ROOT / "code.html"

TITLE = "Kepty English | サービス説明資料"
URL = "https://keptyenglish.jp/"
DESC = (
    "プロサッカー選手の英会話力を引き伸ばす英語コーチングサービス。"
    "約6か月の体系的プログラムと月額19,800円〜39,800円の価格帯。"
)


def esc(s: str) -> str:
    return html.escape(s.strip(), quote=True)


def br(s: str) -> str:
    return esc(s).replace("\n", "<br />\n")


def paras(s: str) -> str:
    return "\n".join(f"<p>{br(p.strip())}</p>" for p in s.split("\n\n") if p.strip())


def blocks() -> list[str]:
    out: list[str] = []
    for chunk in SRC.read_text(encoding="utf-8").split("<<<BLOCK>>>"):
        c = chunk.strip()
        if c:
            out.append(c.replace("\\n", "\n"))
    return out


def ld_json(bs: list[str]) -> str:
    faq = [
        ("英語コーチングの概要", bs[48].replace("\n", " ").strip()),
        ("なぜ、“英語コーチング”が有効か", bs[21].replace("\n", " ").strip()),
        ("【学習量の目安】", bs[59].replace("\n", " ").strip()),
        ("プログラム期間（理論と基礎の積み上げ）", bs[102].replace("\n", " ").strip()),
        ("他社サービスとの比較（脚注）", bs[143].replace("\n", " ").strip()),
    ]
    questions = [
        {"@type": "Question", "name": n, "acceptedAnswer": {"@type": "Answer", "text": t}} for n, t in faq
    ]
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": URL + "#organization",
                "name": "Kepty Co., Ltd.",
                "url": URL,
                "founder": {
                    "@type": "Person",
                    "name": bs[172].strip(),
                    "alternateName": bs[173].strip(),
                    "jobTitle": bs[175].strip(),
                },
            },
            {
                "@type": "WebPage",
                "@id": URL + "#webpage",
                "url": URL,
                "name": TITLE,
                "description": DESC,
                "inLanguage": "ja-JP",
                "publisher": {"@id": URL + "#organization"},
            },
            {"@type": "FAQPage", "@id": URL + "#faqpage", "mainEntity": questions},
        ],
    }
    return json.dumps(data, ensure_ascii=False)


def css() -> str:
    return r"""<style>
:root{--bg:#0f1419;--panel:#161d28;--c1:#ff9764;--c2:#fce4be;--tx:#ecf2fb;--mu:#95a7bd;--r:12px}
*{box-sizing:border-box}body{margin:0;font-family:"Hiragino Sans","Hiragino Kaku Gothic ProN","Yu Gothic","Yu Gothic Medium","Noto Sans JP",Meiryo,sans-serif;background:radial-gradient(1100px 520px at 10% -6%,rgba(255,151,100,.06),transparent),var(--bg);color:var(--tx);line-height:1.78}
.wrap{max-width:1040px;margin:0 auto;padding:0 clamp(14px,4vw,24px)}
a{color:var(--c1);text-underline-offset:3px}a:hover{color:var(--c2)}
header.h{position:sticky;top:0;z-index:40;background:rgba(15,19,27,.94);backdrop-filter:blur(10px);border-bottom:1px solid rgba(255,255,255,.06)}
.h-in{display:flex;gap:12px;flex-wrap:wrap;align-items:flex-start;justify-content:space-between;padding:.75rem 0}
.brand{font-weight:800;color:var(--tx);text-decoration:none;letter-spacing:.04em}
.nav{display:flex;flex-wrap:wrap;gap:.45rem .75rem;justify-content:flex-end;max-width:min(700px,100%)}
.nav a{color:var(--mu);text-decoration:none;font-size:.76rem;line-height:1.35}.nav a:hover{color:var(--c1)}
.hero{padding-top:2.85rem;text-align:center}
.k{font-size:.7rem;letter-spacing:.18em;color:var(--c1);text-transform:uppercase;margin:0}
h1{font-size:clamp(1.9rem,4.8vw,2.9rem);margin:.4rem 0 .4rem;font-weight:800;line-height:1.14}
.sub{color:var(--mu);max-width:32rem;margin:0 auto;font-size:1.05rem;line-height:1.55}
.tldr{margin:1.85rem auto 0;max-width:38rem;padding:1.05rem 1.12rem;border-radius:var(--r);border:1px solid rgba(255,151,100,.36);background:linear-gradient(150deg,rgba(255,151,100,.06),transparent);text-align:left}
.tldr h2{margin:0 0 .55rem;font-size:.97rem}
.tldr ul{margin:.35rem 0 0;padding-left:1rem;color:var(--mu);font-size:.9rem}.tldr li{margin:.4rem 0}
section{margin-bottom:2.75rem;scroll-margin-top:4.5rem}
h2.st{font-size:1.38rem;margin:1.9rem 0 .65rem;display:inline-block;border-bottom:3px solid var(--c1);padding-bottom:.28rem;line-height:1.3}
h3{font-size:1.05rem;color:var(--c2);margin:1.1rem 0 .4rem}
.cards{display:grid;gap:13px;grid-template-columns:repeat(auto-fill,minmax(248px,1fr))}
.card{background:var(--panel);border:1px solid rgba(255,255,255,.07);border-radius:var(--r);padding:clamp(12px,2vw,18px)}
.manifest{max-width:52rem;margin:2.75rem auto 0;color:#dbe8ff}.manifest p{margin:1rem 0}
.banner{background:var(--panel);border-radius:var(--r);padding:1.05rem 1.1rem;margin-top:1.9rem;color:var(--mu);border:1px solid rgba(255,255,255,.07)}
.q{background:rgba(0,0,0,.32);padding:.75rem;border-radius:10px;display:block;font-family:inherit;color:#dfecff;font-size:.9rem;line-height:1.58}
.sm{font-size:.87rem;color:var(--mu)}
table.t{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.83rem;line-height:1.5}
.t th,.t td{border:1px solid rgba(255,255,255,.09);padding:.55rem .48rem;vertical-align:top;text-align:left}
.t caption{text-align:left;font-weight:800;color:var(--c2);margin-bottom:.45rem;line-height:1.35}
.t thead th{background:rgba(255,151,100,.07)}
.grid-p{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px;margin-top:.5rem}
.grid-p div{background:rgba(0,0,0,.24);border-radius:10px;padding:.65rem;font-size:.85rem;color:#d3e0f5}
.grid-p b{display:block;color:var(--mu);font-size:.7rem;margin-bottom:.22rem;font-weight:600}
.faq{border:1px solid rgba(252,228,190,.42);padding:clamp(13px,2vw,21px);border-radius:var(--r);background:rgba(9,11,14,.93)}
.fa{padding:1rem 0;border-bottom:1px solid rgba(255,255,255,.06)}.fa:last-child{border-bottom:none}
.fa h3{font-size:.98rem;color:var(--tx);margin:.2rem 0 .45rem}
.pre{white-space:pre-wrap;margin:.25rem 0 0;color:#c9d8ec;font-size:.9rem}
ul.ls{padding-left:1.05rem;color:#dbefff}.ls li{margin:.3rem 0}
.eat{border:1px solid rgba(255,151,100,.43);padding:clamp(13px,2vw,21px);border-radius:var(--r);margin-top:.5rem;background:rgba(255,151,100,.042);line-height:1.62}
.fa2{display:flex;gap:13px}.av{width:86px;height:86px;border-radius:16px;background:linear-gradient(135deg,var(--c1),#ffd9b9);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.64rem;color:#301107;text-align:center;line-height:1.2}
footer.ft{border-top:1px solid rgba(255,255,255,.07);margin-top:2.8rem;padding:1.95rem 0 4.2rem;color:var(--mu);font-size:.86rem;line-height:1.55}
</style>"""


def main() -> None:
    b = blocks()

    tldr_ul = """<ul>
<li>プロサッカー選手の英会話力を引き伸ばす英語コーチングサービス</li>
<li>「プロサッカー選手に最適化した学習体験」「長期間の学習を支える価格設計」</li>
<li>月額19,800円〜39,800円／約6か月の体系的プログラム</li>
</ul>"""

    header = f"""<header class="h"><div class="wrap h-in">
<a class="brand" href="{esc(URL)}">Kepty English</a>
<nav class="nav" aria-label="ページ内セクションへ移動するリンク">
<a href="#tldr">TL;DR要点（結論ファースト）へ</a>
<a href="#effort">「英語習得に努力が必要」章へ</a>
<a href="#why-coach">「英語コーチングが有効」根拠・引用章へ</a>
<a href="#persona">想定利用者と英会話／コーチングの役割へ</a>
<a href="#outline">英語コーチングの概要・学習量目安へ</a>
<a href="#features">サービスの特徴・学習ステージへ</a>
<a href="#compare">他社サービス比較表へ</a>
<a href="#philosophy">一律クオリティ思想と価格脚注へ</a>
<a href="#pricing">リーグ別月額表へ</a>
<a href="#voices">利用者の声（表）へ</a>
<a href="#eat">CEOプロフィール（E-E-A-T）へ</a>
<a href="#faq">FAQ（構造化データ対応）へ</a>
</nav></div></header>"""

    hero = f"""<section class="hero" aria-labelledby="hx"><div class="wrap">
<p class="k">Kepty English service deck</p>
<h1 id="hx">{esc(b[0])}</h1>
<p class="sub">{br(b[1])}</p>
<aside class="tldr" id="tldr" aria-labelledby="tlh">
<h2 id="tlh">結論ファースト（本文抜粋）</h2>
{tldr_ul}
</aside></div></section>"""

    deck = f"""<article class="manifest wrap" id="deck" aria-label="メインメッセージ原文">
{paras(b[2])}
<aside class="banner">{br(b[3])}</aside>
</article>"""

    effort = f"""<section class="wrap" id="effort">
<h2 class="st">{esc(b[4])}</h2>
<div class="cards">
<article class="card"><h3>{esc(b[6])}</h3><p>{br(b[5])}</p><p class="sm">{br(b[7])}<br/>{br(b[8])}</p></article>
<article class="card"><h3>{esc(b[10])}</h3><p>{br(b[9])}</p><p class="sm">{br(b[11])}<br/>{br(b[12])}</p></article>
</div>
<article class="card" style="margin-top:14px"><p>{br(b[13])}</p>
<p class="sm">悩みの例</p><ul class="ls"><li>{br(b[14])}</li><li>{br(b[15])}</li><li>{br(b[16])}</li></ul>
<p class="sm">学習理論・プログラム設計で埋める方向性</p><ul class="ls"><li>{br(b[17])}</li><li>{br(b[18])}</li><li>{br(b[19])}</li></ul></article>
</section>"""

    coach = f"""<section class="wrap" id="why-coach">
<h2 class="st">{esc(b[20])}</h2>
<article class="card"><p>{br(b[21])}</p><div class="sm"><p>{br(b[23])}</p><p>{br(b[24])}</p></div></article>

<h3>他社英語コーチング利用選手の引用</h3>
<p class="sm">{br(b[30])}</p>
<article class="card"><p class="sm">{esc(b[25])}</p><code class="q">{br(b[25])}</code><p class="sm">{esc(b[26])}</p></article>
<article class="card"><p class="sm">{esc(b[27])}</p><code class="q">{br(b[27])}</code><p class="sm">{esc(b[28])}</p></article>
<article class="card"><p class="sm">{esc(b[29])}</p><code class="q">{br(b[29])}</code></article>

<article class="card"><ul class="ls"><li>{br(b[31])}</li><li>{br(b[32])}</li><li>{br(b[33])}</li><li>{br(b[34])}</li><li>{br(b[35])}</li></ul></article>
</section>"""

    persona = f"""<section class="wrap" id="persona">
<p class="sm">{br(b[36])}</p>
<article class="card"><p>{br(b[37])}</p></article>
<ul class="ls">{''.join(f'<li>{br(x.strip())}</li>' for x in (b[38], b[39], b[40]))}</ul>
</section>"""

    outline_body = "".join(f'<article class="card"><p>{br(x)}</p></article>' for x in b[41:61])
    outline_note = esc("注記：" + b[57].replace("\n", " "))
    outline = f"""<section class="wrap" id="outline">
<h2 class="st">{esc(b[41])}</h2>
{outline_body}
<p class="sm">{outline_note}</p>
</section>"""

    feat_mid = "".join(f'<article class="card"><p>{br(x)}</p></article>' for x in b[61:91])
    phase_a = "".join(f"<div><b>{esc(t)}</b>{br(b[i])}</div>" for t, i in zip(("音声知覚", "意味理解", "概念化", "文章化", "音声化"), range(71, 76)))
    phase_b = "".join(
        f"<div><b>{esc(t)}</b>{br(b[i])}</div>" for t, i in zip(("序盤", "中盤", "終盤", "強固な基礎固め", "武器の磨き込み", "型の確立"), range(78, 84))
    )
    features = f"""<section class="wrap" id="features">
<h2 class="st">{esc("サービスの特徴／拘り")}<span class="sm">（原文見出し：{esc(b[61])}）</span></h2>
{feat_mid}
<div class="card"><div class="grid-p">{phase_a}</div><div class="grid-p" style="margin-top:10px">{phase_b}</div></div>
{''.join(f'<article class="card"><p>{br(x)}</p></article>' for x in b[91:113])}
</section>"""

    compare = f"""<section class="wrap" id="compare">
<h2 class="st">{esc(b[142])}</h2>
<table class="t" aria-label="英語学習サービス形態の比較（参考）">
<caption>{esc(b[142])}</caption>
<thead><tr>
<th scope="col">{esc("観点")}</th>
<th scope="col">{br(b[113])}</th>
<th scope="col">{br(b[117])}</th>
<th scope="col">{br(b[121])}</th>
<th scope="col">Kepty</th>
</tr></thead>
<tbody>
<tr><th scope="row">{esc(b[109])}</th>
<td>{br(b[113])}<br/><span class="sm">{br(b[114])}</span></td>
<td>{br(b[116])}<br/><span class="sm">{br(b[117])}</span></td>
<td>{br(b[121])}<br/><span class="sm">{br(b[122])}</span></td>
<td>{br(b[125])}<br/><span class="sm">{br(b[126])}<br/>{br(b[127])}<br/>{br(b[128])}</span></td></tr>
<tr><th scope="row">{esc(b[110])}</th>
<td>{br(b[114])}<br/>{br(b[115])}</td>
<td>{br(b[118])}</td>
<td>{br(b[119])}</td>
<td>{br(b[120])}</td></tr>
<tr><th scope="row">{esc(b[111])}</th>
<td>{br(b[123])}</td>
<td>{br(b[120])}</td>
<td>{br(b[123])}</td>
<td>{br(b[90])}</td></tr>
<tr><th scope="row">{esc(b[111])} / {esc(b[112])}</th>
<td>{br(b[115])}<br/><span class="sm">{br(b[116])}</span></td>
<td>{br(b[126])}</td>
<td>{br(b[121])}<br/><span class="sm">{br(b[123])}</span></td>
<td>{br(b[68])}</td></tr>
<tr><th scope="row">{esc(b[128])}</th>
<td>{br(b[129])}<br/>{br(b[130])}</td>
<td>{br(b[129])}<br/>{br(b[131])}</td>
<td>{br(b[129])}<br/>{br(b[132])}</td>
<td>{br(b[133])}<br/><span class="sm">{br(b[96])}</span></td></tr>
<tr><th scope="row">{esc(b[134])}</th>
<td>{br(b[135])}<br/>{br(b[136])}</td>
<td>{br(b[136])}<br/><span class="sm">{br(b[127])}</span></td>
<td>{br(b[127])}<br/>{br(b[136])}</td>
<td>{br(b[128])}<br/><span class="sm">{br(b[137])}<br/>{br(b[99])}</span></td></tr>
<tr><th scope="row">{esc(b[138])}</th>
<td>{br(b[138])}<br/>{br(b[139])}</td>
<td>{br(b[140])}</td>
<td>{br(b[139])}<br/>{br(b[140])}</td>
<td>{br(b[140])}<br/>{br(b[141])}<br/><span class="sm">{br(b[101])}</span></td></tr>
</tbody></table>
<p class="sm">{br(b[143])}</p></section>"""

    philo = f"""<section class="wrap" id="philosophy">
<div class="card"><p>{br(b[153])}</p></div>
</section>"""

    pricing = f"""<section class="wrap" id="pricing">
<h2 class="st">{esc(b[144])}</h2>
<table class="t" aria-label="リーグ区分と月額">
<caption>{esc(b[144])}</caption>
<thead><tr><th scope="col">{esc("区分")}</th><th scope="col">{esc("月額")}</th></tr></thead>
<tbody>
<tr><th scope="row">{br(b[148])}</th><td>{br(b[145])}</td></tr>
<tr><th scope="row">{br(b[149])}</th><td>{br(b[146])}</td></tr>
<tr><th scope="row">{br(b[150])}</th><td>{br(b[147])}</td></tr>
<tr><th scope="row">{br(b[151])}</th><td>{br(b[147])}</td></tr>
<tr><th scope="row">{br(b[152])}</th><td>{br(b[147])}</td></tr>
</tbody></table>
<p class="sm">{br(b[143])}</p><p class="sm">{br(b[99])}</p>
</section>"""

    voices = f"""<section class="wrap" id="voices">
<h2 class="st">{esc(b[154])}</h2>
<p class="sm">{br(b[155])}</p>
<table class="t" aria-label="利用者アンケートの抜粋">
<caption>{esc(b[154])}</caption>
<thead><tr><th scope="col"></th>
<th scope="col">{esc(b[161])}</th><th scope="col">{esc(b[162])}</th><th scope="col">{esc(b[171])}</th></tr></thead>
<tbody>
<tr><th scope="row">{esc(b[157])}</th><td>{br(b[160])}</td><td>{br(b[165])}</td><td>{br(b[168])}</td></tr>
<tr><th scope="row">{esc(b[158])}</th><td>{br(b[163])}</td><td>{br(b[166])}</td><td>{br(b[169])}</td></tr>
<tr><th scope="row">{esc(b[159])}</th><td>{br(b[164])}</td><td>{br(b[167])}</td><td>{br(b[170])}</td></tr>
</tbody></table>
<p class="sm">{br(b[156])}</p>
</section>"""

    eat = f"""<section class="eat wrap" id="eat" aria-labelledby="eh">
<h2 id="eh" class="st">創業・運営責任者（E-E-A-T）</h2>
<div class="fa2"><div class="av" aria-hidden="true">{esc(b[173])}<br/>{esc(b[175])}</div><div>
<p><strong>{esc(b[172])}</strong>／{esc(b[173])}</p>
<p>{br(b[174])}</p>
<p class="sm">{br(b[3])}</p>
</div></div></section>"""

    faq_specs = [
        ("英語コーチングの概要", "<p>" + br(b[48]) + "</p>"),
        ("なぜ、“英語コーチング”が有効か", "<div><p>" + br(b[20]) + "</p><p>" + br(b[21]) + "</p></div>"),
        ("【学習量の目安】", '<div class="pre">' + br(b[59]) + "</div>"),
        ("「理論」や「基礎からの積み上げ」を軸にしたプログラム期間", paras(b[102])),
        ("他社サービスとの比較（脚注）", "<p>" + br(b[143]) + "</p>"),
    ]
    faq_html = "".join(
        f'<article class="fa" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">'
        f'<h3 itemprop="name">{esc(t)}</h3>'
        f'<div itemprop="acceptedAnswer" itemscope itemtype="https://schema.org/Answer">'
        f'<div itemprop="text">{body}</div></div></article>'
        for t, body in faq_specs
    )
    faq = f"""<section class="wrap faq" id="faq"><h2 class="st">FAQ（構造化マークアップ）</h2>{faq_html}</section>"""

    footer = f"""<footer class="ft wrap">
<p>{br(b[3])}</p>
<p><a href="{esc(URL)}">{esc(b[175])}</a></p>
</footer>"""

    doc = "\n".join(
        [
            "<!DOCTYPE html>",
            '<html lang="ja-JP" dir="ltr"><head>',
            '<meta charset="utf-8" />',
            '<meta name="viewport" content="width=device-width, initial-scale=1" />',
            f'<meta name="description" content="{esc(DESC)}" />',
            '<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1" />',
            f'<link rel="canonical" href="{esc(URL)}" />',
            f'<meta property="og:title" content="{esc(TITLE)}" />',
            '<meta property="og:type" content="website" />',
            f'<meta property="og:url" content="{esc(URL)}" />',
            f'<meta property="og:description" content="{esc(DESC)}" />',
            f"<title>{esc(TITLE)}</title>",
            '<link rel="icon" href="favicon.ico" />',
            "<script type=\"application/ld+json\">\n" + ld_json(b) + "\n</script>",
            css(),
            "</head><body>",
            header,
            "<main>",
            hero,
            deck,
            effort,
            coach,
            persona,
            outline,
            features,
            compare,
            philo,
            pricing,
            voices,
            eat,
            faq,
            "</main>",
            footer,
            '<script defer>document.documentElement.classList.add("ready");</script>',
            "</body></html>",
        ]
    )

    DST.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
