import streamlit as st
from pysubs2 import SSAFile, SSAEvent
from googletrans import Translator

# 创建用户界面
uploaded_file = st.file_uploader("Upload SRT file", type="srt")
languages = ["Japanese", "Spanish", "French", "English", "Korean"]
selected_languages = st.multiselect("Select languages to translate", languages, default=languages)

if uploaded_file is not None:
    # 读取上传的SRT文件
    subs = SSAFile.from_string(uploaded_file.getvalue().decode("utf-8"))
    
    for lang in selected_languages:
        # 使用Google Translate API将字幕翻译成其他语言
        translator = Translator(service_urls=["translate.google.com"])
        translated_subs = SSAFile()
        for event in subs:
            translated_event = SSAEvent()
            translated_event.start = event.start
            translated_event.end = event.end
            translated_event.text = translator.translate(event.text, dest=lang.lower()).text
            translated_subs.append(translated_event)
        
        # 保存单独的SRT文件
        with open(f"{lang.lower()}.srt", "w", encoding="utf-8") as f:
            f.write(translated_subs.to_string())
        
    st.success("Translation and saving complete!")
