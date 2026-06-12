import os
import tomllib
from pathlib import Path

import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
LOCAL_SECRETS_FILE = ROOT / ".streamlit" / "local_secrets.toml"


def _read_local_key() -> str:
    if not LOCAL_SECRETS_FILE.exists():
        return ""
    try:
        data = tomllib.loads(LOCAL_SECRETS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return ""
    return str(data.get("OPENAI_API_KEY", "") or "").strip()


def save_local_openai_api_key(api_key: str) -> None:
    api_key = str(api_key or "").strip()
    if not api_key:
        return
    LOCAL_SECRETS_FILE.parent.mkdir(parents=True, exist_ok=True)
    escaped = api_key.replace("\\", "\\\\").replace('"', '\\"')
    LOCAL_SECRETS_FILE.write_text(f'OPENAI_API_KEY = "{escaped}"\n', encoding="utf-8")
    st.session_state.local_openai_api_key = api_key


def get_openai_api_key() -> str:
    session_key = str(st.session_state.get("local_openai_api_key", "") or "").strip()
    if session_key:
        return session_key

    local_key = _read_local_key()
    if local_key:
        st.session_state.local_openai_api_key = local_key
        return local_key

    try:
        secret_key = str(st.secrets.get("OPENAI_API_KEY", "") or "").strip()
    except Exception:
        secret_key = ""
    return secret_key or os.getenv("OPENAI_API_KEY", "")


def has_saved_local_key() -> bool:
    return bool(_read_local_key())
