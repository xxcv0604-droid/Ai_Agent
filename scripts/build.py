#!/usr/bin/env python3
"""
회차별 공개일(schedule.json)에 따라, 오늘(한국시간) 기준으로 공개된 회차만
_build/ 폴더에 모아 GitHub Pages로 배포할 정적 사이트를 만든다.

- content/lessonN.html, content/files/lessonN/* : 공개되면 그대로 복사
- schedule.json에 날짜가 없거나 아직 안 된 회차는 index에서 "준비 중"으로만 표시 (파일 복사 안 함)
- template.html(강사용 템플릿)은 항상 포함
"""
import json
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
BUILD = ROOT / "_build"

KST = timezone(timedelta(hours=9))


def today_kst() -> str:
    return datetime.now(KST).strftime("%Y-%m-%d")


def is_released(lesson_id: str, schedule: dict, today: str) -> bool:
    date = schedule.get(lesson_id)
    if not date:
        return False
    return date <= today


def lesson_card(lesson: dict, ready: bool) -> str:
    n = lesson["n"]
    title = lesson["title"]
    if ready:
        return (
            f'<a class="lesson ready" href="{lesson["id"]}.html">'
            f'<div class="n">{n}회차</div><div class="t">{title}</div>'
            f'<span class="s">공개됨</span></a>'
        )
    return (
        f'<div class="lesson soon">'
        f'<div class="n">{n}회차</div><div class="t">{title}</div>'
        f'<span class="s">준비 중</span></div>'
    )


def build_index(lessons_data: dict, schedule: dict, today: str) -> str:
    sections = []
    for course in lessons_data["courses"]:
        cards = "\n      ".join(
            lesson_card(l, is_released(l["id"], schedule, today))
            for l in course["lessons"]
        )
        sections.append(f"""
  <section class="course">
    <div class="course-head"><h2>{course["name"]}</h2><span class="range">{course["range"]}</span></div>
    <p class="course-desc">{course["desc"]}</p>
    <div class="grid">
      {cards}
    </div>
  </section>""")

    return HTML_TEMPLATE.format(
        sections="\n".join(sections),
        today=today,
    )


HTML_TEMPLATE = """<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}html{{scroll-padding-top:env(safe-area-inset-top,0px)}}body{{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#faf9f5;color:#141413}}img{{max-width:100%}}[hidden]:not([hidden=until-found i]){{display:none!important}}</style></head><body>
<title>AI 에이전트 과정 — 전체 커리큘럼</title>
<style>
  :root{{
    --bg:#F6F7FA;--surface:#FFFFFF;--surface-2:#EEF1F7;--text:#1B2130;--text-muted:#5B6475;
    --border:#E1E5EC;--accent:#3652D6;--accent-ink:#22348F;--accent-soft:#E8ECFC;
    --good:#1D7A4C;--good-soft:#E4F5EC;--warn:#9A5B12;--warn-soft:#FBEFDB;--warn-border:#EFD3A3;
    color-scheme:light;
  }}
  @media (prefers-color-scheme:dark){{
    :root:not([data-theme="light"]){{
      --bg:#12151C;--surface:#1A1E27;--surface-2:#20242F;--text:#E8EAF0;--text-muted:#9BA3B4;
      --border:#2B303C;--accent:#8DA0FF;--accent-ink:#C4CFFF;--accent-soft:#242C4C;
      --good:#7BD3A6;--good-soft:#153627;--warn:#E8B369;--warn-soft:#3A2C14;--warn-border:#5B441F;
      color-scheme:dark;
    }}
  }}
  :root[data-theme="dark"]{{
    --bg:#12151C;--surface:#1A1E27;--surface-2:#20242F;--text:#E8EAF0;--text-muted:#9BA3B4;
    --border:#2B303C;--accent:#8DA0FF;--accent-ink:#C4CFFF;--accent-soft:#242C4C;
    --good:#7BD3A6;--good-soft:#153627;--warn:#E8B369;--warn-soft:#3A2C14;--warn-border:#5B441F;
    color-scheme:dark;
  }}
  *{{box-sizing:border-box;}}
  body{{
    margin:0;background:var(--bg);color:var(--text);
    font-family:"Noto Sans KR","Pretendard",-apple-system,sans-serif;
    font-size:17px;line-height:1.65;
    padding-inline:20px;padding-block:max(24px, env(safe-area-inset-top,0px)) 64px;
  }}
  h1,h2,h3{{font-family:"IBM Plex Sans KR","Noto Sans KR",sans-serif;text-wrap:balance;margin:0;}}
  .wrap{{max-width:880px;margin:0 auto;}}
  header.top{{padding-block:32px 24px;border-bottom:1px solid var(--border);margin-bottom:28px;}}
  .eyebrow{{display:inline-block;font-size:14px;font-weight:700;letter-spacing:.06em;color:var(--accent-ink);background:var(--accent-soft);padding:4px 10px;border-radius:999px;margin-bottom:12px;}}
  header.top h1{{font-size:clamp(28px,5vw,40px);font-weight:800;}}
  header.top .sub{{color:var(--text-muted);font-size:16px;margin-top:10px;max-width:60ch;}}
  .meta{{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px;}}
  .meta span{{font-size:14px;font-weight:600;color:var(--text-muted);background:var(--surface-2);padding:6px 12px;border-radius:999px;}}
  .course{{margin-block:36px;}}
  .course-head{{display:flex;align-items:baseline;gap:10px;margin-bottom:6px;flex-wrap:wrap;}}
  .course-head h2{{font-size:24px;font-weight:800;}}
  .course-head .range{{font-size:14px;color:var(--text-muted);font-weight:600;}}
  .course-desc{{color:var(--text-muted);font-size:15.5px;margin-bottom:16px;}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px;}}
  .lesson{{display:block;border-radius:14px;padding:16px 18px;border:1px solid var(--border);background:var(--surface);text-decoration:none;color:var(--text);transition:border-color .15s;}}
  .lesson.ready{{border-color:color-mix(in srgb, var(--good) 35%, var(--border));}}
  .lesson.ready:hover,.lesson.ready:focus-visible{{border-color:var(--good);outline:none;}}
  .lesson.soon{{opacity:.55;cursor:default;}}
  .lesson .n{{font-size:13px;font-weight:800;letter-spacing:.04em;color:var(--accent-ink);margin-bottom:6px;}}
  .lesson.soon .n{{color:var(--text-muted);}}
  .lesson .t{{font-size:16px;font-weight:700;margin-bottom:8px;line-height:1.4;}}
  .lesson .s{{display:inline-block;font-size:12px;font-weight:700;padding:2px 8px;border-radius:999px;}}
  .lesson.ready .s{{background:var(--good-soft);color:var(--good);}}
  .lesson.soon .s{{background:var(--surface-2);color:var(--text-muted);}}
  .legend{{display:flex;gap:18px;flex-wrap:wrap;margin-block:20px 8px;font-size:14px;color:var(--text-muted);}}
  .legend span{{display:inline-flex;align-items:center;gap:6px;}}
  .dot{{width:9px;height:9px;border-radius:50%;display:inline-block;}}
  .dot.ready{{background:var(--good);}}
  .dot.soon{{background:var(--text-muted);}}
  .tools{{margin-top:40px;padding-top:28px;border-top:1px solid var(--border);}}
  .tools h2{{font-size:20px;font-weight:800;margin-bottom:12px;}}
  .toolcard{{display:flex;justify-content:space-between;align-items:center;gap:12px;border:1px solid var(--border);border-radius:12px;padding:14px 18px;background:var(--surface);text-decoration:none;color:var(--text);flex-wrap:wrap;}}
  .toolcard .t{{font-weight:700;font-size:15.5px;}}
  .toolcard .d{{font-size:14px;color:var(--text-muted);margin-top:2px;}}
  .toolcard .go{{font-size:13px;font-weight:700;color:var(--accent-ink);background:var(--accent-soft);padding:6px 12px;border-radius:999px;white-space:nowrap;}}
  footer{{margin-top:48px;padding-top:20px;border-top:1px solid var(--border);color:var(--text-muted);font-size:14px;}}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=IBM+Plex+Sans+KR:wght@600;700&display=swap">

<div class="wrap">
  <header class="top">
    <span class="eyebrow">그린컵으로 배우는</span>
    <h1>AI 에이전트 과정</h1>
    <p class="sub">Claude로 업무를 다시 설계하는 16회차 커리큘럼. Agent1(입문)에서 Chat·Project로 시작해, Agent2(심화)에서 자동화·에이전트 팀까지 이어집니다.</p>
    <div class="meta">
      <span>총 16회차</span>
      <span>회당 3시간</span>
      <span>Agent1 1~8회차 · Agent2 9~16회차</span>
    </div>
  </header>

  <div class="legend">
    <span><i class="dot ready"></i>공개됨 — 클릭해서 보기</span>
    <span><i class="dot soon"></i>준비 중</span>
  </div>
{sections}

  <div class="tools">
    <h2>강사용 도구</h2>
    <a class="toolcard" href="template.html">
      <div>
        <div class="t">슬라이드 템플릿</div>
        <div class="d">새 회차를 같은 디자인으로 만들 때 복사해서 쓰는 컴포넌트 모음</div>
      </div>
      <span class="go">열기 →</span>
    </a>
  </div>

  <footer>AI 에이전트 과정 · 전체 커리큘럼 허브 · 마지막 갱신 {today}</footer>
</div>
</body></html>
"""


def main():
    lessons_data = json.loads((ROOT / "lessons.json").read_text(encoding="utf-8"))
    schedule = json.loads((ROOT / "schedule.json").read_text(encoding="utf-8"))
    schedule = {k: v for k, v in schedule.items() if not k.startswith("_")}
    today = today_kst()

    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)

    # 항상 포함: 강사용 템플릿
    shutil.copy(CONTENT / "template.html", BUILD / "template.html")

    released = []
    for course in lessons_data["courses"]:
        for lesson in course["lessons"]:
            lid = lesson["id"]
            if is_released(lid, schedule, today):
                src_html = CONTENT / f"{lid}.html"
                src_files = CONTENT / "files" / lid
                if not src_html.exists():
                    print(f"  경고: {lid} 공개일이 지났지만 content/{lid}.html 이 없음 — 건너뜀")
                    continue
                shutil.copy(src_html, BUILD / f"{lid}.html")
                if src_files.exists():
                    shutil.copytree(src_files, BUILD / "files" / lid)
                released.append(lid)

    (BUILD / "index.html").write_text(
        build_index(lessons_data, schedule, today), encoding="utf-8"
    )

    print(f"오늘({today}) 기준 공개: {released}")


if __name__ == "__main__":
    main()
