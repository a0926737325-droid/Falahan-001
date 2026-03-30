import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語學習 - Foting", 
    page_icon="🐟", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 視覺魔法 (深海科技風) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&display=swap');

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
        color: #00E5FF;
        font-size: 40px;
        font-weight: 700;
        letter-spacing: 3px;
        text-shadow: 0 0 10px #00E5FF;
        margin: 0;
    }
    
    .teacher-tag { 
        display: inline-block; 
        margin-top: 15px; 
        padding: 5px 15px; 
        border: 1px solid #FF4081; 
        color: #FF4081; 
        border-radius: 50px; 
        font-size: 14px; 
        font-weight: bold; 
    }

    .word-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px 10px;
        text-align: center;
        border: 1px solid rgba(0, 229, 255, 0.2);
        margin-bottom: 15px;
    }
    
    .amis-word { font-size: 22px; font-weight: 700; color: #FFFFFF; }
    .zh-word { font-size: 16px; color: #80DEEA; }

    .sentence-box {
        background: linear-gradient(90deg, rgba(0,229,255,0.05) 0%, rgba(0,0,0,0) 100%);
        border-left: 4px solid #FF4081;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 0 10px 10px 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #FFFFFF !important; 
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00E5FF !important;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 資料設定 (黃淑珍老師教材) ---
VOCABULARY = [
    {"amis": "foting", "zh": "魚", "emoji": "🐟", "file": "v_foting"},
    {"amis": "kalang", "zh": "螃蟹", "emoji": "🦀", "file": "v_kalang"},
]

SENTENCES = [
    {
        "amis": "Mifoting kako i 'alo.", 
        "zh": "我在河邊抓魚。", 
        "emoji": "🎣", 
        "file": "s_foting_sentence"
    },
    {
        "amis": "Mikalang kako i 'alo.", 
        "zh": "我在河邊抓螃蟹。", 
        "emoji": "🧺", 
        "file": "s_kalang_sentence"
    },
]

# --- 1.5 語音播放核心 ---
def play_audio(text, filename_base=None):
    if filename_base:
        for ext in ['m4a', 'mp3', 'wav']: 
            path = f"audio/{filename_base}.{ext}"
            if os.path.exists(path):
                mime = 'audio/mp4' if ext == 'm4a' else 'audio/mp3'
                st.audio(path, format=mime)
                return
        st.caption(f"🔍 尚未偵測到音檔: {filename_base}.m4a (將使用合成音)")

    try:
        # 使用印尼語引擎暫代阿美語發音
        tts = gTTS(text=text, lang='id') 
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    except:
        st.write("🔇 無法播放聲音")

# --- 2. 介面呈現 ---
def main():
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title">AMIS - FOTING</h1>
        <div style="color: #B2EBF2; margin-top:10px;">阿美語學習：魚與螃蟹</div>
        <div class="teacher-tag">講師：黃淑珍 | 教材提供：黃淑珍</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📖 學習模式", "🎮 挑戰任務"])
    
    with tab1:
        st.markdown("<h3 style='color:#00E5FF; text-align:center;'>單字練習</h3>", unsafe_allow_html=True)
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
        st.markdown("<h3 style='color:#00E5FF; text-align:center;'>句子練習</h3>", unsafe_allow_html=True)
        for item in SENTENCES:
            st.markdown(f"""
            <div class="sentence-box">
                <div style="font-size:18px; color:#FF80AB; font-weight:700;">{item['emoji']} {item['amis']}</div>
                <div style="color:#B2EBF2;">{item['zh']}</div>
            </div>
            """, unsafe_allow_html=True)
            play_audio(item['amis'], filename_base=item['file'])

    with tab2:
        st.info("💡 挑戰模式即將上線，請先在學習模式中熟悉發音！")

    # 底部診斷
    if not os.path.exists("audio"):
        st.error("🚨 警告：目錄下找不到 'audio' 資料夾，請建立該資料夾並放入音檔。")

if __name__ == "__main__":
    main()
