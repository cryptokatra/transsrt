import os
import streamlit as st
from pysubs2 import SSAFile, SSAEvent
from googletrans import Translator
import time

def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download,str):
        object_to_download = object_to_download.encode('utf-8')
    try:
        #生成下载链接：
        with open(download_filename, 'w') as f:
            f.write(object_to_download)
        with open(download_filename, 'rb') as f:
            bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download={download_filename}> {download_link_text}</a>'
        return href
    except Exception as e:
        print(e)

def main():
    uploaded_file = st.file_uploader("Upload SRT file", type="srt")
    languages = ["Japanese", "Spanish", "French", "English", "Korean"]
    selected_languages = st.multiselect("Select languages to translate", languages, default=languages)
    if uploaded_file is not None:
        # 读取上传的SRT文件
        subs = SSAFile.from_string(uploaded_file.getvalue().decode("utf-8"))

        progress_bar = st.progress(0)
        download_links = []
        for i, lang in enumerate(selected_languages):
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
                
            progress_percent = (i + 1) / len(selected_languages) * 100
            progress_bar.progress(progress_percent)
            time.sleep(0.1)

            # 添加下载链接
            download_links.append(download_link(f"{lang.lower()}.srt", f"{lang.lower()}.srt", f"{lang}.srt"))

        st.success("Translation and saving complete!")
        for link in download_links:
            st.markdown(link, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
