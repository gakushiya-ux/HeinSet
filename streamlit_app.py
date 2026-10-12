import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.iimport os
import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip
from gtts import gTTS
import tempfile

st.set_page_config(page_title="AI Movie Recap Studio", layout="wide", page_icon="🎬")

st.title("🎬 AI Movie Recap & Video Generator")
st.write("ဗီဒီယိုတင်ရုံဖြင့် မူရင်းအသံဖျောက်ခြင်း၊ အရောင်ပြောင်းခြင်းနှင့် မြန်မာ AI Voiceover ထည့်သွင်းပေးသည့် စနစ်")

with st.sidebar:
    st.header("⚙️ Settings")
    ratio = st.selectbox("ဗီဒီယို Ratio:", ["Original", "16:9 (Landscape)", "9:16 (Shorts/TikTok)", "1:1 (Square)"])
    color_preset = st.selectbox("Color Filter:", ["None", "Cinematic Warm", "Cyberpunk / Cold", "Black & White"])

def apply_color_grading(clip, preset):
    if preset == "Cinematic Warm":
        return clip.fl_image(lambda frame: (frame * [1.1, 1.0, 0.9]).clip(0, 255).astype('uint8'))
    elif preset == "Cyberpunk / Cold":
        return clip.fl_image(lambda frame: (frame * [0.9, 1.0, 1.2]).clip(0, 255).astype('uint8'))
    elif preset == "Black & White":
        return clip.fx(lambda c: c.to_mask().to_RGB())
    return clip

def resize_aspect_ratio(clip, selected_ratio):
    w, h = clip.size
    if selected_ratio == "9:16 (Shorts/TikTok)":
        new_w = int(h * 9 / 16)
        if new_w <= w:
            return clip.crop(x_center=w/2, width=new_w, height=h)
    elif selected_ratio == "1:1 (Square)":
        min_dim = min(w, h)
        return clip.crop(x_center=w/2, y_center=h/2, width=min_dim, height=min_dim)
    return clip

uploaded_file = st.file_uploader("ရုပ်ရှင် / ဗီဒီယိုဖိုင် ရွေးချယ်တင်ပါ (MP4, MKV, MOV)", type=["mp4", "mkv", "mov"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    st.subheader("📼 Original Video")
    st.video(video_path)

    custom_script = st.text_area(
        "မြန်မာလို ဇာတ်လမ်းပြောမည့်စာသား:",
        value="ဒီဇာတ်ကားမှာတော့ အဓိကဇာတ်ကောင်ဟာ မထင်မှတ်ထားတဲ့ အန္တရာယ်ကြီးတစ်ခုနဲ့ ရင်ဆိုင်ရပါတော့တယ်။",
        height=120
    )

    if st.button("🚀 Recap Video စတင် Generate လုပ်မည်"):
        progress_bar = st.progress(0)
        status = st.empty()

        status.text("၁/၃ - မူရင်းအသံဖျောက်ခြင်းနှင့် အရောင်ချိန်ညှိနေပါသည်...")
        progress_bar.progress(30)
        
        video_clip = VideoFileClip(video_path).without_audio()
        video_clip = resize_aspect_ratio(video_clip, ratio)
        video_clip = apply_color_grading(video_clip, color_preset)

        status.text("၂/၃ - မြန်မာ Voiceover အသံဖန်တီးနေပါသည်...")
        progress_bar.progress(60)

        tts_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        tts = gTTS(text=custom_script, lang='my', slow=False)
        tts.save(tts_path)

        narration_audio = AudioFileClip(tts_path)
        if video_clip.duration > narration_audio.duration:
            video_clip = video_clip.subclip(0, narration_audio.duration)
        video_clip = video_clip.set_audio(narration_audio)

        status.text("၃/၃ - Video Render ထုတ်လုပ်နေပါသည်...")
        progress_bar.progress(85)

        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24, logger=None)
        
        progress_bar.progress(100)
        status.success("🎉 ပြီးပါပြီ!")

        st.subheader("📺 Generated Recap Video")
        st.video(output_path)

        with open(output_path, "rb") as file:
            st.download_button(
                label="📥 Download Video",
                data=file,
                file_name="recap_video.mp4",
                mime="video/mp4"
            )
Please replace the entire content of streamlit_app.py with this complete Movie Recap code, then save and commit it:

import os
import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip
from gtts import gTTS
import tempfile

st.set_page_config(page_title="AI Movie Recap Studio", layout="wide", page_icon="🎬")
st.title("🎬 AI Movie Recap & Video Generator")
st.write("ဗီဒီယိုတင်ရုံဖြင့် မူရင်းအသံဖျောက်ခြင်း၊ အရောင်ပြောင်းခြင်းနှင့် မြန်မာ AI Voiceover ထည့်သွင်းပေးသည့် စနစ်")

with st.sidebar:
    st.header("⚙️ Settings")
    ratio = st.selectbox("ဗီဒီယို Ratio:", ["Original", "16:9 (Landscape)", "9:16 (Shorts/TikTok)", "1:1 (Square)"])
    color_preset = st.selectbox("Color Filter:", ["None", "Cinematic Warm", "Cyberpunk / Cold", "Black & White"])

def apply_color_grading(clip, preset):
    if preset == "Cinematic Warm":
        return clip.fl_image(lambda frame: (frame * [1.1, 1.0, 0.9]).clip(0, 255).astype('uint8'))
    elif preset == "Cyberpunk / Cold":
        return clip.fl_image(lambda frame: (frame * [0.9, 1.0, 1.2]).clip(0, 255).astype('uint8'))
    elif preset == "Black & White":
        return clip.fx(lambda c: c.to_mask().to_RGB())
    return clip

def resize_aspect_ratio(clip, selected_ratio):
    w, h = clip.size
    if selected_ratio == "9:16 (Shorts/TikTok)":
        new_w = int(h * 9 / 16)
        if new_w <= w:
            return clip.crop(x_center=w/2, width=new_w, height=h)
    elif selected_ratio == "1:1 (Square)":
        min_dim = min(w, h)
        return clip.crop(x_center=w/2, y_center=h/2, width=min_dim, height=min_dim)
    return clip

uploaded_file = st.file_uploader("ရုပ်ရှင် / ဗီဒီယိုဖိုင် ရွေးချယ်တင်ပါ (MP4, MKV, MOV)", type=["mp4", "mkv", "mov"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    st.subheader("📼 Original Video")
    st.video(video_path)

    custom_script = st.text_area(
        "မြန်မာလို ဇာတ်လမ်းပြောမည့်စာသား:",
        value="ဒီဇာတ်ကားမှာတော့ အဓိကဇာတ်ကောင်ဟာ မထင်မှတ်ထားတဲ့ အန္တရာယ်ကြီးတစ်ခုနဲ့ ရင်ဆိုင်ရပါတော့တယ်။",
        height=120
    )

    if st.button("🚀 Recap Video စတင် Generate လုပ်မည်"):
        progress_bar = st.progress(0)
        status = st.empty()

        status.text("၁/၃ - မူရင်းအသံဖျောက်ခြင်းနှင့် အရောင်ချိန်ညှိနေပါသည်...")
        progress_bar.progress(30)
        
        video_clip = VideoFileClip(video_path).without_audio()
        video_clip = resize_aspect_ratio(video_clip, ratio)
        video_clip = apply_color_grading(video_clip, color_preset)

        status.text("၂/၃ - မြန်မာ Voiceover အသံဖန်တီးနေပါသည်...")
        progress_bar.progress(60)

        tts_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        tts = gTTS(text=custom_script, lang='my', slow=False)
        tts.save(tts_path)

        narration_audio = AudioFileClip(tts_path)
        if video_clip.duration > narration_audio.duration:
            video_clip = video_clip.subclip(0, narration_audio.duration)
        video_clip = video_clip.set_audio(narration_audio)

        status.text("၃/၃ - Video Render ထုတ်လုပ်နေပါသည်...")
        progress_bar.progress(85)

        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24, logger=None)
        
        progress_bar.progress(100)
        status.success("🎉 ပြီးပါပြီ!")

        st.subheader("📺 Generated Recap Video")
        st.video(output_path)

        with open(output_path, "rb") as file:
            st.download_button(
                label="📥 Download Video",
                data=file,
                file_name="recap_video.mp4",
                mime="video/mp4"
            )
