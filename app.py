import streamlit as st
import yt_dlp
import os
import imageio_ffmpeg

st.set_page_config(page_title="Reel → MP3 Downloader", page_icon="🎵", layout="centered")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.main-card {
    background: rgba(255,255,255,0.08);
    padding: 35px;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 0 30px rgba(0,0,0,0.3);
}

.title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: white;
}

.subtitle {
    text-align: center;
    color: #d1d1d1;
    margin-bottom: 25px;
}

.stTextInput>div>div>input {
    background-color: rgba(255,255,255,0.1);
    color: white;
    border-radius: 10px;
}

.stRadio > div {
    color: white;
}

.stButton button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    background: linear-gradient(90deg,#ff416c,#ff4b2b);
    color: white;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stDownloadButton button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color: white;
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- UI CARD ----------
st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.markdown('<div class="title">🎵 Reel → MP3</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Download Instagram Reel audio in best quality</div>', unsafe_allow_html=True)

url = st.text_input("🔗 Paste Public Reel URL")

download_format = st.radio(
    "Select Format",
    ["Original Best Audio", "MP3 (320kbps)"],
    horizontal=True
)

if st.button("🚀 Download Now"):

    if url.strip() == "":
        st.warning("Please paste a valid URL")

    else:
        with st.spinner("Processing... Please wait"):

            output_file = "reel_audio"

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_file + '.%(ext)s',
                'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
                'quiet': True
            }

            if download_format == "MP3 (320kbps)":
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }]

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                for file in os.listdir():
                    if file.startswith(output_file):

                        st.success("✅ Download Ready")

                        with open(file, "rb") as f:
                            st.download_button(
                                label="⬇ Download File",
                                data=f,
                                file_name=file
                            )
                        break

            except Exception as e:
                st.error("❌ " + str(e))

st.markdown('</div>', unsafe_allow_html=True)