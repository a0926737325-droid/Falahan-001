import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 漁獲 Fating", 
    page_icon="🐟", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 視覺魔法 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&family=Noto+Sans+TC:wght@400;700&display=swap');

    .stApp { 
        background-color: #000810;
        background-image: radial-gradient(circle at 50% 0%, #0D47A1 0%, #000810 80%);
        font-family: 'Noto Sans TC', sans-serif;
        color: #E0F7FA;
    }
    
    .header-container {
        background: rgba(13, 71, 161, 0.3);
        border: 1px solid #00E5FF;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.3);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        margin-bottom: 40px;
        backdrop-filter: blur(10px);
    }
    
    .main-title {
        font-family: 'Roboto Mono', monospace;
        color: #00E5FF;
        font-size: 40px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 0 0 10px #00E5FF;
        margin: 0;
    }
    
    .sub-title { color: #B2EBF2; font-size: 18px; margin-top: 10px; letter-spacing: 1px; }
    .teacher-tag { display: inline-block; margin-top: 15px; padding: 5px 15px; border: 1px solid #FF4081; color: #FF4081; border-radius: 50px; font-size: 12px; font-weight: bold; letter-spacing: 1px; }

    .word-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px 10px;
        text-align: center;
        border: 1px solid rgba(0, 229, 255, 0.2);
        margin-bottom: 15px;
    }
    .amis-word { font-size: 20px; font-weight: 700; color: #FFFFFF; margin-bottom: 5px; }
    .zh-word { font-size: 16px; color: #80DEEA; }

    .sentence-box {
        background: linear-gradient(90deg, rgba(0,229,255,0.05) 0%, rgba(0,0,0,0) 100%);
        border-left: 4px solid #FF4081;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 0 10px 10px 0;
    }
    .sentence-amis { font-size: 18px; color: #FF80AB; font-weight: 700; margin-bottom: 8px; }
    
    .stButton>button { width: 100%; border-radius: 5px; background: transparent; border: 2px solid #00E5FF; color: #00E5FF !important; font-weight: bold; }
    .stButton>button:hover { background: #00E5FF; color: #000 !important; }

    .stTabs [data-baseweb="tab"] {
        color: #FFFFFF !important; 
        background-color: rgba(255, 255, 255, 0.1) !important;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00E5FF !important;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 資料設定 (更新為黃淑珍老師教材內容) ---
VOCABULARY = [
    {"amis": "fating", "zh": "魚", "emoji": "🐟", "file": "v_fating"},
    {"amis": "kalang", "zh": "螃蟹", "emoji": "🦀", "file": "v_kalang"},
]

SENTENCES = [
    {
        "amis": "Mifoting kako i 'alo.", 
        "zh": "我在河邊抓魚。", 
        "emoji": "🎣", 
        "file": "s_fating_sentence"
    },
    {
        "amis": "Mikalang kako i 'alo.", 
        "zh": "我在河邊抓螃蟹。", 
        "emoji": "🧺", 
        "file": "s_kalang_sentence"
    },
]

# --- 1.5 語音核心 ---
def play_audio(text, filename_base=None):
    if filename_base:
        for ext in ['m4a', 'mp3', 'wav']: 
            path = f"audio/{filename_base}.{ext}"
            if os.path.exists(path):
                mime = 'audio/mp4' if ext == 'm4a' else 'audio/mp3'
                st.audio(path, format=mime)
                return
        st.markdown(f"<span style='color:#FF4081; font-size:12px;'>🔍 待上傳音檔: {filename_base}.m4a</span>", unsafe_allow_html=True)

    try:
        tts = gTTS(text=text.split('.')[0], lang='id') 
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    except:
        st.caption("🔇")

# --- 2. 測驗初始化 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q = 0

# --- 3. 介面呈現 ---
def show_learning_mode():
    st.markdown("<h3 style='color:#00E5FF; text-align:center;'>🐟 單字學習</h3>", unsafe_allow_html=True)
    cols = st.columns(2)
    for idx, item in enumerate(VOCABULARY):
        with cols[idx]:
            st.markdown(f"""
            <div class="word-card">
                <div style="font-size:40px;">{item['emoji']}</div>
                <div class="amis-word">{item['amis']}</div>
                <div class="zh-word">{item['zh']}</div>
            </div>
            """, unsafe_allow_html=True)
            play_audio(item['amis'], filename_base=item['file'])

    st.markdown("---")
    st.markdown("<h3 style='color:#00E5FF; text-align:center;'>🗣️ 常用句子</h3>", unsafe_allow_html=True)
    for item in SENTENCES:
        st.markdown(f"""
        <div class="sentence-box">
            <div class="sentence-amis">{item['emoji']} {item['amis']}</div>
            <div style="color:#B2EBF2;">{item['zh']}</div>
        </div>
        """, unsafe_allow_html=True)
        play_audio(item['amis'], filename_base=item['file'])

def main():
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title">AMIS - FATING</h1>
        <div class="sub-title">阿美語學習：魚與螃蟹</div>
        <div class="teacher-tag">講師：黃淑珍 | 教材提供者：黃淑珍</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📖 學習模式", "🎮 挑戰任務"])
    
    with tab1:
        show_learning_mode()
    with tab2:
        st.info("測驗模式開發中，請先練習左側學習模式。")

    # 診斷工具
    if not os.path.exists("audio"):
        st.warning("⚠️ 提醒：請在 GitHub 建立 'audio' 資料夾並放置音檔。")

if __name__ == "__main__":
    main()
