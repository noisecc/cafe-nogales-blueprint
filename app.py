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
# STRUCTURE (from PDF)
# ---------------------------------------------------------
sections = {
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

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def section_to_filename(section_name: str) -> Path:
    number_part, title_part = section_name.split(".", 1)
    slug = title_part.strip().lower().replace(" ", "-")
    filename = f"{number_part.strip()}-{slug}.md"
    return Path("content") / filename

def load_markdown(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"⚠️ Missing: `{path}`"

def extract_subsection(full_md: str, subsection_title: str) -> str:
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
# SIDEBAR (new navigation)
# ---------------------------------------------------------
logo_path = Path("assets/logo-primary.png")
if logo_path.exists():
    try:
        st.sidebar.image(str(logo_path), use_container_width=True)
    except UnidentifiedImageError:
        st.sidebar.write("Cafe Nogales")
else:
    st.sidebar.write("Cafe Nogales")

st.sidebar.title("Cafe Nogales Blueprint")

# initialize session state
if "main_section" not in st.session_state:
    st.session_state.main_section = list(sections.keys())[0]
if "sub_section" not in st.session_state:
    st.session_state.sub_section = sections[st.session_state.main_section][0]

# build sidebar as expanders
for sec_name, subsecs in sections.items():
    expanded = sec_name == st.session_state.main_section
    with st.sidebar.expander(sec_name, expanded=expanded):
        # radio for subsections in this section
        selected_sub = st.radio(
            "Select subsection",
            subsecs,
            index=subsecs.index(st.session_state.sub_section) if sec_name == st.session_state.main_section and st.session_state.sub_section in subsecs else 0,
            key=f"radio_{sec_name}",
            label_visibility="collapsed",
        )
        # if user interacted with this expander, set current section/subsection
        if expanded:
            st.session_state.sub_section = selected_sub
            st.session_state.main_section = sec_name

# now read current selection from session state
main_section = st.session_state.main_section
sub_section = st.session_state.sub_section

# ---------------------------------------------------------
# LOAD CONTENT
# ---------------------------------------------------------
content_file = section_to_filename(main_section)
full_md = load_markdown(content_file)
sub_md = extract_subsection(full_md, sub_section)

# ---------------------------------------------------------
# RELATED LINKS PANEL
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
    st.title(main_section)
    st.subheader(sub_section)
    st.markdown(sub_md, unsafe_allow_html=False)

with right_col:
    st.markdown('<div class="context-box">', unsafe_allow_html=True)
    with st.expander("🔗 Related Documents", expanded=True):
        links = related_links.get(main_section, [])
        if links:
            for label, url in links:
                st.markdown(f"- [{label}]({url})")
        else:
            st.markdown("_No related documents yet._")
    st.markdown("</div>", unsafe_allow_html=True)

st.caption(f"Source file: {content_file}")
