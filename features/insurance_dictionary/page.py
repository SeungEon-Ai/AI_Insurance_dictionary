import base64
import html
import re

import streamlit as st

from .ai import answer, get_api_key
from .config import LOGO_MARK
from .data import load_terms, search_terms
from features.local_secrets import save_local_openai_api_key
from features.shared_header import render_feature_header


MESSAGE_KEY = "dictionary_chat_messages_v15"
PENDING_KEY = "pending_dictionary_prompt_v15"

EXAMPLE_QUESTIONS = [
    "보험계약자가 무슨 뜻이야?",
    "자동갱신계약이 무슨 뜻이야?",
    "보험료와 보험금의 차이가 뭐야?",
    "면책기간이 무슨 뜻이야?",
]


def assistant_avatar():
    return str(LOGO_MARK) if LOGO_MARK.exists() else None


def logo_data_uri():
    if not LOGO_MARK.exists():
        return ""
    encoded = base64.b64encode(LOGO_MARK.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def clean_answer_text(text):
    text = str(text or "")
    text = re.sub(r"</?div[^>]*>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"</?p[^>]*>", "", text, flags=re.IGNORECASE)
    text = text.replace("**", "")
    text = re.sub(r"^-?\s*쉬운 설명\s*:\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^-?\s*분류\s*:\s*.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n*\s*참고\s*출처\s*:.*$", "", text, flags=re.MULTILINE)
    return text.strip()


def html_text(text):
    return html.escape(clean_answer_text(text)).replace("\n", "<br>")


def render_chat_css():
    st.markdown(
        """
        <style>
        .dictionary-title-row {
            display: flex;
            align-items: center;
            gap: .5rem;
            height: 32px;
            margin-bottom: .8rem;
        }
        .dictionary-title-logo {
            width: 30px;
            height: 30px;
            object-fit: contain;
            display: block;
            flex: 0 0 30px;
        }
        .dictionary-title {
            color: #15202b;
            font-size: 1.42rem;
            font-weight: 900;
            line-height: 32px;
            height: 32px;
            margin: 0;
            letter-spacing: 0;
            white-space: nowrap;
        }
        div[data-testid="stSegmentedControl"] label {
            font-size: .68rem !important;
            min-height: 1.25rem !important;
            padding: .1rem .5rem !important;
            white-space: nowrap !important;
        }
        .chat-row {
            display: flex;
            align-items: flex-start;
            width: 100%;
            margin: .6rem 0;
            gap: .72rem;
        }
        .chat-row.assistant {
            justify-content: flex-start;
        }
        .chat-row.user {
            justify-content: flex-end;
        }
        .chat-avatar {
            width: 28px;
            height: 28px;
            object-fit: contain;
            flex: 0 0 28px;
            border-radius: 7px;
        }
        .chat-bubble {
            max-width: 74%;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            padding: .12rem .35rem .35rem;
            font-size: .98rem;
            line-height: 1.45;
            color: #252b36;
            word-break: keep-all;
            overflow-wrap: anywhere;
        }
        .chat-row.user .chat-bubble {
            max-width: 52%;
            padding: .48rem .72rem;
        }
        .chat-row.assistant .chat-bubble {
            background: #ffffff;
            box-shadow: 0 1px 2px rgba(15, 23, 42, .03);
        }
        .chat-row.user .chat-bubble {
            background: #f5f6f8;
        }
        div[data-testid="stForm"] {
            border: 0;
            padding: 0;
            background: transparent;
        }
        .dictionary-chat-input-spacer {
            height: .7rem;
        }
        .dictionary-loading-inline {
            display: flex;
            align-items: center;
            gap: .55rem;
            flex-wrap: nowrap;
            white-space: nowrap;
        }
        .dictionary-loading-bubble {
            padding: .48rem .72rem !important;
        }
        .dictionary-loading-spinner {
            width: 20px;
            height: 20px;
            border: 3px solid #e5e7eb;
            border-top-color: #5b83df;
            border-radius: 999px;
            flex: 0 0 20px;
            animation: dictionary-loading-spin .75s linear infinite;
        }
        @keyframes dictionary-loading-spin {
            to { transform: rotate(360deg); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_api_key():
    with st.sidebar:
        st.markdown("### GPT API 키")
        st.caption("로컬 테스트용입니다. 입력한 키는 파일에 저장하지 않고 현재 세션에서만 사용합니다.")
        key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            key="local_openai_api_key_input_v15",
        )
        if key and key.strip().startswith("sk-") and key.strip() != st.session_state.get("local_openai_api_key", ""):
            save_local_openai_api_key(key.strip())
            st.success("API 키가 연결됐습니다.")
            st.rerun()


def render_inline_api_key():
    with st.expander("GPT API 키 입력", expanded=False):
        st.caption("사이드바가 보이지 않을 때 여기서도 로컬 테스트용 API 키를 입력할 수 있습니다.")
        key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            key="local_openai_api_key_inline_v15",
        )
        if key and key.strip().startswith("sk-") and key.strip() != st.session_state.get("local_openai_api_key", ""):
            save_local_openai_api_key(key.strip())
            st.success("API 키가 연결됐습니다.")
            st.rerun()


def init_messages():
    for key in list(st.session_state.keys()):
        if key.startswith("dictionary_chat_messages") and key != MESSAGE_KEY:
            del st.session_state[key]

    if MESSAGE_KEY not in st.session_state:
        st.session_state[MESSAGE_KEY] = [
            {
                "role": "assistant",
                "content": "보험용어에 대해 궁금한 점을 물어보세요!",
            }
        ]

    for msg in st.session_state[MESSAGE_KEY]:
        if msg["role"] == "assistant":
            msg["content"] = clean_answer_text(msg.get("content", "")) or "보험용어에 대해 궁금한 점을 물어보세요!"


def messages():
    return st.session_state[MESSAGE_KEY]


def render_header():
    render_feature_header("AI보험용어사전")


def render_status(df):
    return


def queue_prompt(prompt):
    messages().append({"role": "user", "content": prompt})
    st.session_state[PENDING_KEY] = prompt


def render_quick_examples():
    selected = st.segmented_control(
        "예시 질문",
        EXAMPLE_QUESTIONS,
        key="example_question_segmented_v15",
    )
    if selected and st.session_state.get("last_example_question_v15") != selected:
        st.session_state.last_example_question_v15 = selected
        queue_prompt(selected)
        st.rerun()


def render_message(msg):
    role = msg["role"]
    content = html_text(msg["content"])
    if role == "assistant":
        avatar = logo_data_uri()
        avatar_html = f'<img class="chat-avatar" src="{avatar}" alt="LINA">' if avatar else ""
        st.markdown(
            f"""
            <div class="chat-row assistant">
                {avatar_html}
                <div class="chat-bubble">{content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="chat-row user">
                <div class="chat-bubble">{content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_messages():
    for msg in messages():
        render_message(msg)


def complete_pending_prompt(df):
    prompt = st.session_state.get(PENDING_KEY, "")
    if not prompt:
        return

    loading_slot = st.empty()
    avatar = logo_data_uri()
    avatar_html = f'<img class="chat-avatar" src="{avatar}" alt="LINA">' if avatar else ""
    loading_slot.markdown(
        f"""
        <div class="chat-row assistant">
            {avatar_html}
            <div class="chat-bubble dictionary-loading-bubble">
                <div class="dictionary-loading-inline">
                    <div class="dictionary-loading-spinner"></div>
                    <div>AI가 보험용어 DB에서 용어를 찾아 정리하고 있는 중이에요.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    results = search_terms(df, prompt)
    response = clean_answer_text(answer(prompt, results))

    messages().append(
        {
            "role": "assistant",
            "content": response,
        }
    )
    st.session_state[PENDING_KEY] = ""
    st.rerun()


def render():
    render_chat_css()
    render_sidebar_api_key()
    df = load_terms()
    init_messages()
    render_header()
    render_status(df)
    render_inline_api_key()
    render_quick_examples()
    render_messages()
    complete_pending_prompt(df)

    st.markdown('<div class="dictionary-chat-input-spacer"></div>', unsafe_allow_html=True)
    with st.form("dictionary_inline_chat_form", clear_on_submit=True):
        input_col, send_col = st.columns([12, 1])
        prompt = input_col.text_input(
            "보험용어 질문 입력",
            placeholder="예: 보험계약자가 무슨 뜻이야?",
            label_visibility="collapsed",
        )
        submitted = send_col.form_submit_button("↑", use_container_width=True)

    if submitted and prompt.strip():
        queue_prompt(prompt)
        st.rerun()
