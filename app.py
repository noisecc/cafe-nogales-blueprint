import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Cafe Nogales – Brand Blueprint",
    layout="wide",
)

# Sidebar structure from the PDF
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

def section_to_filename(section_name: str) -> Path:
    # "1. Brand Narrative" -> "1-brand-narrative.md"
    number_part, title_part = section_name.split(".", 1)
    slug = title_part.strip().lower().replace(" ", "-")
    filename = f"{number_part.strip()}-{slug}.md"
    return Path("content") / filename

def load_markdown(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"⚠️ Content file not found: `{path}`. Please create it in the /content folder."

def extract_subsection(full_md: str, subsection_title: str) -> str:
    """
    Very simple extractor:
    - We assume subsections start with '## '
    - We find the line '## {subsection_title}'
    - We return everything until the next '## ' or end of file
    If not found, we return the full_md so editors never see blank content.
    """
    lines = full_md.splitlines()
    target_header = f"## {subsection_title}".strip()
    start_idx = None
    for i, line in enumerate(lines):
        if line.strip() == target_header:
            start_idx = i
            break

    if start_idx is None:
        # subsection not found — return full markdown
        return full_md

    # collect lines from start_idx until next "## " (but keep "# ..." above? no, we just show subsection)
    subsection_lines = []
    for j in range(start_idx, len(lines)):
        line = lines[j]
        if j > start_idx and line.startswith("## "):
            # next subsection begins — stop
            break
        subsection_lines.append(line)

    return "\n".join(subsection_lines)


st.sidebar.title("Cafe Nogales Blueprint")
main_section = st.sidebar.selectbox("Section", list(sections.keys()))
sub_section = st.sidebar.selectbox("Subsection", sections[main_section])

# page titles
st.title(main_section)
st.subheader(sub_section)

# load whole file
content_file = section_to_filename(main_section)
full_markdown = load_markdown(content_file)

# try to show only the chosen subsection
sub_markdown = extract_subsection(full_markdown, sub_section)

# render
st.markdown(sub_markdown, unsafe_allow_html=False)

# helper footer so editors know where text comes from
st.caption(f"Source file: {content_file}")
