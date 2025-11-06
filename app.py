import streamlit as st
from pathlib import Path
from PIL import UnidentifiedImageError  # for safe logo loading

st.set_page_config(
    page_title="Cafe Nogales – Brand Blueprint",
    layout="wide",
)

# ---------------------------------------------------------
# GLOBAL STYLES + GOOGLE FONTS
# ---------------------------------------------------------
st.markdown("""
<!-- Google Fonts: Noto Sans (Latin), KR, JP -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;700&family=Noto+Sans+KR:wght@400;500;700&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">

<style>
:root {
  --cnb-blue: #0038f4;
  --cnb-white: #ffffff;
  --cnb-light: #f5f7ff;
  --cnb-text: #1b1b1b;
}

/* apply Noto Sans globally */
html, body, [class*="css"] {
  font-family: 'Noto Sans', 'Noto Sans KR', 'Noto Sans JP', sans-serif;
  color: var(--cnb-text);
  background-color: var(--cnb-white);
  -webkit-font-smoothing: antialiased;
}

/* top bar */
.cnb-topbar {
  background: var(--cnb-white);
  border-bottom: 2px solid var(--cnb-blue);
  padding: 0.7rem 1.2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.cnb-title {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--cnb-blue);
  letter-spacing: 0.3px;
}
.cnb-tagline {
  font-size: 0.9rem;
  color: #4a4a4a;
}

.markdown-text-container, .stMarkdown {
  line-height: 1.55;
}

/* headings in brand blue */
h1, h2, h3 {
  color: var(--cnb-blue);
  font-weight: 700;
}

/* right context box */
.context-box {
  background: var(--cnb-light);
  border: 1px solid #dbe3ff;
  border-radius: 10px;
  padding: 1rem 1.1rem;
}

/* reduce top padding on main */
.main > div {
  padding-top: 0rem;
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
# STRUCTURE FROM PDF
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
    # "1. Brand Narrative" -> "1-brand-narrative.md"
    number_part, title_part = section_name.split(".", 1)
    slug = title_part.strip().lower().replace(" ", "-")
    filename = f"{number_part.strip()}-{slug}.md"
    return Path("content") / filename

def load_markdown(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"⚠️ Missing: `{path}`"

def extract_subsection(full_md: str, subsection_title: str) -> str:
    """
    Find '## {subsection_title}' and return that block until the next '## '.
    If not found, return full_md.
    """
    lines = full_md.splitlines()
    target = f"## {subsection_title}".strip()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == target:
            start = i
            break
    if start is None:
        return full_md

    subsection_lines = []
    for j in range(start, len(lines)):
        line_j = lines[j]
        if j > start and line_j.startswith("## "):
            break
        subsection_lines.append(line_j)
    return "\n".join(subsection_lines)

# ---------------------------------------------------------
# SIDEBAR (safe logo)
# ---------------------------------------------------------
logo_path = Path("assets/logo-primary.png")
if logo_path.exists():
    try:
        st.sidebar.image(str(logo_path), use_container_width=True)
    except UnidentifiedImageError:
        # file exists but isn't a valid image
        st.sidebar.write("Cafe Nogales")
else:
    st.sidebar.write("Cafe Nogales")

st.sidebar.title("Cafe Nogales Blueprint")
main_section = st.sidebar.selectbox("Section", list(sections.keys()))
sub_section = st.sidebar.selectbox("Subsection", sections[main_section])

# ---------------------------------------------------------
# MAIN CONTENT
# ---------------------------------------------------------
st.title(main_section)
st.subheader(sub_section)

content_file = section_to_filename(main_section)
full_md = load_markdown(content_file)
sub_md = extract_subsection(full_md, sub_section)

left, right = st.columns([2.1, 1])
with left:
    st.markdown(sub_md, unsafe_allow_html=False)
with right:
    st.markdown('<div class="context-box">', unsafe_allow_html=True)
    st.markdown("### Full section (context)")
    st.markdown(full_md, unsafe_allow_html=False)
    st.markdown("</div>", unsafe_allow_html=True)

st.caption(f"Source file: {content_file}")
