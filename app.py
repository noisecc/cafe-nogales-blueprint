import streamlit as st
from pathlib import Path
from datetime import datetime
from PIL import UnidentifiedImageError

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Cafe Nogales – Brand Blueprint",
    layout="wide",
)

# ---------------------------------------------------------
# GLOBAL STYLES + GOOGLE FONTS (DARK THEME)
# ---------------------------------------------------------
st.markdown("""
<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;700&family=Noto+Sans+KR:wght@400;500;700&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">

<style>
:root {
  --cnb-blue: #0038f4;       /* main background */
  --cnb-navy: #050040;       /* sidebar / panels */
  --cnb-white: #ffffff;
  --cnb-light: #2a2a7a;
  --cnb-text: #ffffff;
}

/* Global font and background */
html, body, [class*="css"] {
  font-family: 'Noto Sans', 'Noto Sans KR', 'Noto Sans JP', sans-serif;
  color: var(--cnb-text);
  background-color: var(--cnb-blue);
  -webkit-font-smoothing: antialiased;
}

/* Top bar */
.cnb-topbar {
  background: var(--cnb-navy);
  border-bottom: 2px solid var(--cnb-white);
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

/* Markdown & headings */
.markdown-text-container, .stMarkdown {
  line-height: 1.55;
}
h1, h2, h3 {
  color: var(--cnb-white);
  font-weight: 700;
}

/* Right context box */
.context-box {
  background: var(--cnb-navy);
  border: 1px solid #1a1a5e;
  border-radius: 16px;
  padding: 1.2rem 1.4rem;
  box-shadow: 0 0 8px rgba(0,0,0,0.25);
}

/* Sidebar background */
[data-testid="stSidebar"] {
  background-color: #050040;
}

/* Reduce top padding on main so it sits under topbar */
.main > div {
  padding-top: 0rem;
}

/* Make expanders blend with dark bg */
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
# STRUCTURE (FROM YOUR PDF)
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
    """
    Turn "1. Brand Narrative" into content/1-brand-narrative.md
    """
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
    Find '## <subsection_title>' and return that block until the next '## '.
    If not found, return the full markdown.
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
# SIDEBAR (SAFE LOGO)
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
main_section = st.sidebar.selectbox("Section", list(sections.keys()))
sub_section = st.sidebar.selectbox("Subsection", sections[main_section])

# ---------------------------------------------------------
# LOAD CONTENT
# ---------------------------------------------------------
content_file = section_to_filename(main_section)
full_md = load_markdown(content_file)
sub_md = extract_subsection(full_md, sub_section)

# ---------------------------------------------------------
# RIGHT-PANEL DATA (NOTES + LINKS)
# ---------------------------------------------------------
section_notes = {
    "1. Brand Narrative": "High-level storytelling: why Café Nogales exists and what sets it apart.",
    "2. Brand Voice and Messaging": "Keep tone clear, human, and transparent. Avoid hype or vague praise.",
    "3. Visual Identity System": "Reference only master Figma components. Follow color, logo, and grid rules.",
    "4. Product Structure & Architecture": "Document tiers and origins consistently so roasters can read the offer sheet fast.",
    "5. Brand Assets": "Use only approved and final assets. No drafts or unbranded files.",
    "6. Key Brand Touchpoints": "Capture rules for physical and digital brand moments — bags, signage, socials.",
    "7. Brand Guidelines": "Treat this as the canonical source. Update the version log with every approved change.",
}

related_links = {
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

    # Section Info (always visible)
    st.markdown("### 🧭 Section Info")
    st.markdown(f"**Main section:** {main_section}")
    st.markdown(f"**Subsection:** {sub_section}")
    if content_file.exists():
        ts = content_file.stat().st_mtime
        dt = datetime.fromtimestamp(ts)
        st.markdown(f"**Last updated:** {dt.strftime('%Y-%m-%d %H:%M')}")

    # Editor Notes (collapsible)
    with st.expander("✏️ Editor Notes", expanded=False):
        st.markdown(section_notes.get(main_section, "_No notes for this section yet._"))

    # Related Links (collapsible)
    with st.expander("🔗 Related Links", expanded=True):
        links = related_links.get(main_section, [])
        if links:
            for label, url in links:
                st.markdown(f"- [{label}]({url})")
        else:
            st.markdown("_No related links yet._")

    st.markdown("</div>", unsafe_allow_html=True)

# Footer / source
st.caption(f"Source file: {content_file}")
