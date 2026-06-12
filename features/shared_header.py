import base64
from pathlib import Path

import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
LOGO_MARK = ROOT / "assets" / "lina_mark_color_sharp.png"


def _image_data_uri(path):
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def render_feature_header(title, subtitle=None):
    logo_uri = _image_data_uri(LOGO_MARK)
    title_html = "".join(f"<span>{part}</span>" for part in title.split(" "))
    logo_html = f'<img class="feature-header-logo" src="{logo_uri}" alt="LINA">' if logo_uri else ""
    subtitle_html = f'<div class="feature-header-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <style>
        .feature-header-wrap {{
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
            height: 34px !important;
            margin: 0 0 8px 0 !important;
            padding: 0 !important;
        }}
        .feature-header-logo {{
            width: 30px !important;
            height: 30px !important;
            min-width: 30px !important;
            max-width: 30px !important;
            object-fit: contain !important;
            display: block !important;
            margin: 0 !important;
            padding: 0 !important;
        }}
        .feature-header-title {{
            display: inline-flex !important;
            align-items: center !important;
            gap: 5px !important;
            color: #15202b !important;
            font-family: "Malgun Gothic", "Apple SD Gothic Neo", sans-serif !important;
            font-size: 26px !important;
            font-weight: 900 !important;
            line-height: 34px !important;
            margin: 0 !important;
            padding: 0 !important;
            letter-spacing: 0 !important;
            word-spacing: 0 !important;
            white-space: nowrap !important;
        }}
        .feature-header-title span {{
            display: inline-block !important;
            color: inherit !important;
            font: inherit !important;
            line-height: inherit !important;
            letter-spacing: 0 !important;
            word-spacing: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }}
        .feature-header-subtitle {{
            color: #64748b !important;
            font-family: "Malgun Gothic", "Apple SD Gothic Neo", sans-serif !important;
            font-size: 14px !important;
            font-weight: 400 !important;
            line-height: 20px !important;
            margin: 0 0 16px 0 !important;
            padding: 0 !important;
            letter-spacing: 0 !important;
            word-spacing: 0 !important;
        }}
        </style>
        <div class="feature-header-wrap">
            {logo_html}
            <div class="feature-header-title">{title_html}</div>
        </div>
        {subtitle_html}
        """,
        unsafe_allow_html=True,
    )
