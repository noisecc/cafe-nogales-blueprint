import streamlit as st
from pathlib import Path
from PIL import UnidentifiedImageError  # to safely handle bad/missing images

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Cafe Nogales – Brand Blueprint",
    layout="wide",
)

# ---------------------------------------------------------
# GLOBAL STYLES + GOOGLE FONTS
# (aligned with your dark theme in .streamlit/config.toml)
# ---------------------------------------------------------
st.markdown("""
<!-- Google Fonts: Noto Sans (Latin), KR, JP -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;700&family=Noto+Sans+KR:wght@400;500;700&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">

<style>
:root {
  --cnb-blue: #0038f4;       /* main background from your theme */
  --cnb-navy: #050040;       /* secondary/darker panels */
  --cnb-white: #ffffff;      /* text & accents */
  --cnb-light: #2a2a7a;      /* subtle boxes */
  --cnb-text: #ffffff;
}

/* apply Noto Sans globally */
html, body, [class*="css"] {
  font-family: 'Noto Sans', 'Noto Sans KR', 'Noto Sans JP', sans-serif;
  color: var(--cnb-text);
  background-color: var(--cnb-blue);
  -webkit-font-smoothing: antialiased;
}

/* top bar */
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
  letter-spacing: 0.3px;
}
.cnb-tagline {
  font-size: 0.9rem;
  color: #d8d8ff;
}

/* markdown content */
.markdown-text-container, .stMarkdown {
  line-height: 1.55;
}

/* headings */
h1, h2, h3 {
  color: var(--cnb-white);
  font-weight: 700;
}

/* right context box */
.context-box {
  background: var(--cnb-navy);
  border: 1px solid #1a1a5e;
  border-radius: 10px;
  padding: 1rem 1.1rem;
}

/* reduce top padding on main so it hugs the*
