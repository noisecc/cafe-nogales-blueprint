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
# STRUCTURE (EN + KO LABELS)
# ---------------------------------------------------------
# English base keys — used for file loading
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

# Korean labels mapped to the SAME keys/subkeys
sections_ko = {
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
# HELPERS
# ---------------------------------------------------------
def section_to_filename(section_name: str) -> Path:
    # use EN key to build filename
    number_part, title_part = section_name.split(".", 1)
    slug = title_part.strip().lower().replace(" ", "-")
    return Path("content") / f"{number_part.strip()}-{slug}.md"

def load_markdown(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"⚠️ Missing: `{path}`"

def extract_subsection(full_md: str, subsection_title: str) -> str:
    # in KO mode, subsection_title will be Korean, but our markdown likely uses English headings,
    # so if no match, we fall back to full_md
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
# SIDEBAR (with language)
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

# use session state to persist selection
if "main_section" not in st.session_state:
    st.session_state.main_section = list(sections_en.keys())[0]
if "sub_section_idx" not in st.session_state:
    st.session_state.sub_section_idx = 0

# pick correct label set
sections_ui = sections_en if lang == "English" else sections_ko

# build sidebar as expanders
for sec_key in sections_en.keys():
    # show EN or KO section name
    ui_section_title = sec_key if lang == "English" else sections_ko[sec_key][0].split(" / ")[0] if sections_ko[sec_key] else sec_key
    # but Korean top-level in our dict is still the EN key — we can just show sec_key for clarity
    ui_section_title = sec_key if lang == "English" else sec_key  # simpler: show numbering always

    expanded = (sec_key == st.session_state.main_section)
    with st.sidebar.expander(ui_section_title, expanded=expanded):
        # get subsections in UI language
        ui_subsections = sections_ui[sec_key]
        # figure out the current index for this section
        current_idx = st.session_state.sub_section_idx if expanded else 0
        chosen_sub = st.radio(
            "sub",
            ui_subsections,
            index=current_idx if current_idx < len(ui_subsections) else 0,
            key=f"radio_{sec_key}_{lang}",
            label_visibility="collapsed",
        )
        if expanded:
            # update session state
            st.session_state.main_section = sec_key
            st.session_state.sub_section_idx = ui_subsections.index(chosen_sub)

# now resolve active section/subsection
active_section_key = st.session_state.main_section
active_sub_idx = st.session_state.sub_section_idx

# what to display in MAIN title
display_section_title = active_section_key if lang == "English" else f"{active_section_key} (KR)"
display_subsection_title = (
    sections_en[active_section_key][active_sub_idx]
    if lang == "English"
    else sections_ko[active_section_key][active_sub_idx]
)

# ---------------------------------------------------------
# LOAD CONTENT (always from EN file)
# ---------------------------------------------------------
content_file = section_to_filename(active_section_key)
full_md = load_markdown(content_file)

# try to extract subsection — will only work automatically in EN;
# in KO we just show full section (safe fallback)
if lang == "English":
    sub_md = extract_subsection(full_md, display_subsection_title)
else:
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
    st.title(display_section_title)
    st.subheader(display_subsection_title)
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

st.caption(f"Source file: {content_file}")
