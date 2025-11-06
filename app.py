import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Cafe Nogales – Brand Blueprint",
    layout="wide",
)

# 1) sidebar structure (from PDF)
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

# 2) helper to map section name -> content file
def section_to_filename(section_name: str) -> Path:
    """
    Turn '1. Brand Narrative' into 'content/1-brand-narrative.md'
    """
    # take part after number
    # "1. Brand Narrative" -> "1-brand-narrative"
    number_part, title_part = section_name.split(".", 1)
    slug = title_part.strip().lower().replace(" ", "-")
    filename = f"{number_part.strip()}-{slug}.md"
    return Path("content") / filename

def load_markdown(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    else:
        return f"⚠️ Content file not found: `{path}`. Please create it in the /content folder."

st.sidebar.title("Cafe Nogales Blueprint")
main_section = st.sidebar.selectbox("Section", list(sections.keys()))
sub_section = st.sidebar.selectbox("Subsection", sections[main_section])

st.title(main_section)
st.subheader(sub_section)

# 3) load the markdown for the selected main section
content_file = section_to_filename(main_section)
markdown_text = load_markdown(content_file)

# 4) show markdown
st.markdown(markdown_text, unsafe_allow_html=False)

# (Optional) show which subsection was picked, to guide editors
st.caption(f"Currently viewing subsection: {sub_section}")
