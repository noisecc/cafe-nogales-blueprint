import streamlit as st
from pathlib import Path
from PIL import UnidentifiedImageError

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Cafe Nogales – Brand Blueprint",
    layout="wide",
)

# ---------------------------------------------------------
# GLOBAL STYLES + GOOGLE FONTS
# ---------------------------------------------------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;700&family=Noto+Sans+KR:wght@400;500;700&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">

<style>
:root {
  --cnb-blue: #0038f4;
  --cnb-navy: #050040;
  --cnb-white: #ffffff;
  --cnb-text: #ffffff;
}

/* Global typography */
html, body, [class*="css"] {
  font-family: 'Noto Sans', 'Noto Sans KR', 'Noto Sans JP', sans-serif;
  color: var(--cnb-text);
  background-color: var(--cnb-blue);
  -webkit-font-smoothing: antialiased;
}

/* Top bar */
.cnb-topbar {
  background: var(--cnb-blue);
  border-bottom: none;
  padding: 0.7rem 1.2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.cnb-title {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--cnb-white);
}
.cnb-tagline {
  font-size: 0.9rem;
  color: #d8d8ff;
}

/* Right context box — flat blue */
.context-box {
  background: var(--cnb-blue);
  border: none;
  border-radius: 0.75rem;
  padding: 1.2rem 1.4rem;
}

/* Sidebar background */
[data-testid="stSidebar"] {
  background-color: #050040;
}

/* Headings + spacing */
h1, h2, h3 {
  color: var(--cnb-white);
  font-weight: 700;
}
.markdown-text-container, .stMarkdown {
  line-height: 1.55;
}

/* Push content down so it doesn't hide behind top bar */
.main > div {
  padding-top: 1.6rem;
}

/* Make expanders blend with dark */
details {
  background: transparent !important;
  color: var(--cnb-white);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# TOP BAR
# ---------------------------------------------------------
st.markdown("""
<div class="cnb-topbar">
  <div class="cnb-title">☕ Cafe Nogales — Brand Blueprint</div>
  <div class="cnb-tagline">Closer to Origin</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# STRUCTURE: ENGLISH BASE
# ---------------------------------------------------------
sections_en = {
    "1. Brand Narrative": [
        "Our Story: Who We Are & Why We Exist",
        "Mission & Vision",
        "Strategic Definitions",
        "Audience Insight",
    ],
    "2. Brand Voice and Messaging": [
        "Brand Voice Framework",
        "Voice Dos and Donts",
        "Sample Messaging per Channel",
        "Brand Language Guide",
    ],
    "3. Visual Identity System": [
        "Logo Suite",
        "Typography System",
        "Color Strategy",
        "Layout & Grid Systems",
        "Motifs & Accent Visuals",
    ],
    "4. Product Structure & Architecture": [
        "Product Tiers",
        "Tier Attributes",
        "Origin Integration",
        "Visual Tier Coding",
    ],
    "5. Brand Assets": [
        "Logo Files",
        "Color Codes & Style Swatches",
        "Label Templates",
        "Social Media Templates",
        "Coffee Catalog & Offer Sheet Templates",
        "Email Signatures, Presentation Decks",
    ],
    "6. Key Brand Touchpoints": [
        "B2B Website Layout Guidelines",
        "Green Coffee Bag Design (tier variations)",
        "Roaster Welcome Kit",
        "Cupping Cards & Traceability Sheets",
        "Social Media Brand Experience",
        "Event / Pop-up Signage System",
    ],
    "7. Brand Guidelines": [
        "Full PDF Manual (Visual + Verbal)",
        "Internal Values Summary",
        "Brand Book Slide Deck",
        "Optional: Korean-language version",
        "Ongoing update log (versioning + approvals)",
    ],
}

# Korean display labels
sections_ko_labels = {
    "1. Brand Narrative": "1. 브랜드 내러티브",
    "2. Brand Voice and Messaging": "2. 브랜드 보이스 & 메시징",
    "3. Visual Identity System": "3. 비주얼 아이덴티티 시스템",
    "4. Product Structure & Architecture": "4. 제품 구조 & 아키텍처",
    "5. Brand Assets": "5. 브랜드 자산",
    "6. Key Brand Touchpoints": "6. 주요 브랜드 터치포인트",
    "7. Brand Guidelines": "7. 브랜드 가이드라인",
}

# Korean subsections
sections_ko_subs = {
    "1. Brand Narrative": [
        "브랜드 스토리",
        "미션 & 비전",
        "전략적 정의",
        "타깃 인사이트",
    ],
    "2. Brand Voice and Messaging": [
        "브랜드 보이스 프레임워크",
        "보이스 Do / Don't",
        "채널별 메시지 예시",
        "브랜드 언어 가이드",
    ],
    "3. Visual Identity System": [
        "로고 시스템",
        "타이포그래피",
        "컬러 전략",
        "레이아웃 & 그리드",
        "모티프 & 악센트 비주얼",
    ],
    "4. Product Structure & Architecture": [
        "제품/원두 티어",
        "티어 속성",
        "원산지(Origin) 연계",
        "티어 시각 코딩",
    ],
    "5. Brand Assets": [
        "로고 파일",
        "컬러 코드 & 스타일 스와치",
        "라벨 템플릿",
        "소셜 미디어 템플릿",
        "커피 카탈로그 & 오퍼 시트 템플릿",
        "이메일 시그니처, 프레젠테이션 덱",
    ],
    "6. Key Brand Touchpoints": [
        "B2B 웹사이트 레이아웃 가이드",
        "그린 커피 백 디자인 (티어별)",
        "로스터 웰컴 키트",
        "커핑 카드 & 트레이서빌리티 시트",
        "소셜 미디어 브랜드 경험",
        "이벤트 / 팝업 사인 시스템",
    ],
    "7. Brand Guidelines": [
        "풀 PDF 매뉴얼 (비주얼 + 버벌)",
        "내부 가치 요약본",
        "브랜드북 슬라이드 덱",
        "한국어 버전",
        "업데이트 로그 (버전 & 승인)",
    ],
}

# ---------------------------------------------------------
# KOREAN PER-SUBSECTION OVERRIDES
# use this when a Korean subsection lives in a different file than English structure
# key = Korean subsection label, value = filename inside content_ko/
# ---------------------------------------------------------
KO_SUBSECTION_FILE_OVERRIDE = {
    # example from your case:
    "미션 & 비전": "2-brand-voice-and-messaging-ko.md",
    # add more here if other Korean subsections live in other files
}

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def section_to_filename(section_name: str) -> Path:
    """'1. Brand Narrative' -> content/1-brand-narrative.md"""
    number_part, title_part = section_name.split(".", 1)
    slug = title_part.strip().lower().replace(" ", "-")
    return Path("content") / f"{number_part.strip()}-{slug}.md"


def load_markdown_for_lang(base_path: Path, lang: str, active_subsection: str | None = None) -> tuple[str, Path]:
    """
    Try to load a Korean file first, respecting overrides.
    Order:
      0) if active subsection has an explicit override -> use that
      1) content_ko/<same-filename>.md
      2) content_ko/<same-filename>-ko.md
      3) content_ko/<number-*.md>
      4) fallback to English
    Returns (markdown_text, actual_path_used)
    """
    if lang == "한국어":
        ko_dir = Path("content_ko")

        # 0. explicit per-subsection override
        if active_subsection and active_subsection in KO_SUBSECTION_FILE_OVERRIDE:
            override_path = ko_dir / KO_SUBSECTION_FILE_OVERRIDE[active_subsection]
            if override_path.exists():
                return override_path.read_text(encoding="utf-8"), override_path

        # 1. exact same filename
        exact_ko = ko_dir / base_path.name
        if exact_ko.exists():
            return exact_ko.read_text(encoding="utf-8"), exact_ko

        # 2. same filename with -ko.md
        ko_variant = ko_dir / (base_path.stem + "-ko.md")
        if ko_variant.exists():
            return ko_variant.read_text(encoding="utf-8"), ko_variant

        # 3. match by section number prefix
        prefix = base_path.name.split("-", 1)[0]  # e.g. "3" from "3-visual-identity-system.md"
        candidates = sorted(ko_dir.glob(f"{prefix}-*.md"))
        if candidates:
            chosen = candidates[0]
            return chosen.read_text(encoding="utf-8"), chosen

    # 4. fallback to English
    if base_path.exists():
        return base_path.read_text(encoding="utf-8"), base_path

    return f"⚠️ Missing: `{base_path}`", base_path


def extract_subsection(full_md: str, subsection_title: str) -> str:
    """English-only subsection extraction by '## <title>'."""
    lines = full_md.splitlines()
    target = f"## {subsection_title}".strip()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == target:
            start = i
            break
    if start is None:
        return full_md
    out_lines = []
    for j in range(start, len(lines)):
        line_j = lines[j]
        if j > start and line_j.startswith("## "):
            break
        out_lines.append(line_j)
    return "\n".join(out_lines)

# ---------------------------------------------------------
# SIDEBAR (logo + language + EXPANDERS)
# ---------------------------------------------------------
logo_path = Path("assets/logo-primary.png")
if logo_path.exists():
    try:
        st.sidebar.image(str(logo_path), use_container_width=True)
    except UnidentifiedImageError:
        st.sidebar.write("Cafe Nogales")
else:
    st.sidebar.write("Cafe Nogales")

# language selector
lang = st.sidebar.selectbox("Language / 언어", ["English", "한국어"])

st.sidebar.title("Cafe Nogales Blueprint" if lang == "English" else "카페 노갈레스 브랜드 기준서")

# init session state
if "main_section" not in st.session_state:
    st.session_state.main_section = list(sections_en.keys())[0]
if "sub_section" not in st.session_state:
    st.session_state.sub_section = sections_en[st.session_state.main_section][0]

# pick label set for UI
if lang == "English":
    sections_ui_labels = {k: k for k in sections_en.keys()}
    sections_ui_subs = sections_en
else:
    sections_ui_labels = sections_ko_labels
    sections_ui_subs = sections_ko_subs

# build expander-style nav
for sec_key in sections_en.keys():
    expanded = (sec_key == st.session_state.main_section)
    ui_section_title = sections_ui_labels.get(sec_key, sec_key)
    with st.sidebar.expander(ui_section_title, expanded=expanded):
        ui_subs = sections_ui_subs[sec_key]
        # if this is the active section, preselect the active subsection
        if sec_key == st.session_state.main_section and st.session_state.sub_section in ui_subs:
            current_index = ui_subs.index(st.session_state.sub_section)
        else:
            current_index = 0

        selected_sub = st.radio(
            "Select subsection",
            ui_subs,
            index=current_index,
            key=f"radio_{sec_key}_{lang}",
            label_visibility="collapsed",
        )

        # if user clicked inside this expander, update active section and subsection
        if sec_key == st.session_state.main_section or selected_sub != st.session_state.sub_section:
            st.session_state.main_section = sec_key
            st.session_state.sub_section = selected_sub

# active selection
active_section_key = st.session_state.main_section
active_subsection_title = st.session_state.sub_section

# ---------------------------------------------------------
# LOAD CONTENT (LANG-AWARE, with actual path)
# ---------------------------------------------------------
content_file = section_to_filename(active_section_key)
full_md, actual_path = load_markdown_for_lang(content_file, lang, active_subsection=active_subsection_title)

if lang == "English":
    sub_md = extract_subsection(full_md, active_subsection_title)
else:
    # Korean files likely don't have the exact same '##' headings
    sub_md = full_md

# ---------------------------------------------------------
# RELATED LINKS
# ---------------------------------------------------------
related_links = {
    "1. Brand Narrative": [
        ("📘 Company Story Deck", "https://drive.google.com/your-story-link"),
    ],
    "3. Visual Identity System": [
        ("🎨 Figma — Master Brand System", "https://figma.com/your-brand-system-link"),
        ("🗂 Logo Pack — Google Drive", "https://drive.google.com/your-logo-pack-link"),
    ],
    "5. Brand Assets": [
        ("📱 Social Template Folder", "https://drive.google.com/your-social-template-link"),
        ("📄 Offer Sheet Template", "https://drive.google.com/your-offer-sheet-link"),
    ],
    "7. Brand Guidelines": [
        ("📘 Master PDF Manual", "https://drive.google.com/your-guidelines-pdf-link"),
        ("🧾 Version Log Spreadsheet", "https://drive.google.com/your-version-log-link"),
    ],
}

# ---------------------------------------------------------
# LAYOUT
# ---------------------------------------------------------
left_col, right_col = st.columns([2.1, 1])

with left_col:
    if lang == "English":
        st.title(active_section_key)
        st.subheader(active_subsection_title)
    else:
        st.title(sections_ko_labels.get(active_section_key, active_section_key))
        st.subheader(active_subsection_title)

    st.markdown(sub_md, unsafe_allow_html=False)

with right_col:
    st.markdown('<div class="context-box">', unsafe_allow_html=True)
    with st.expander("🔗 Related Documents" if lang == "English" else "🔗 관련 문서", expanded=True):
        links = related_links.get(active_section_key, [])
        if links:
            for label, url in links:
                st.markdown(f"- [{label}]({url})")
        else:
            st.markdown("_No related documents yet._" if lang == "English" else "_관련 문서가 없습니다._")
    st.markdown("</div>", unsafe_allow_html=True)

# show which file we actually used
st.caption(f"Source file: {actual_path}")
