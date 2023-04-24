import streamlit as st
import os
from googletrans import Translator
from pathlib import Path

# 设置语言选项
LANGUAGES = {
    'ja': '日本語',
    'es': 'Español',
    'fr': 'Français',
    'en': 'English',
    'ko': '한국어'
}

# 定义翻译函数
def translate_srt(text, dest):
    translator = Translator()
    return translator.translate(text, dest=dest).text

# 定义保存函数
def save_srt(text, filename):
    with open(filename, 'w') as f:
        f.write(text)

# 显示上传文件按钮
uploaded_file = st.file_uploader("选择一个SRT文件", type=['srt'])

# 显示语言选项 checkbox
selected_languages = st.multiselect("选择要翻译的语言（默认全选）", LANGUAGES.values(), default=LANGUAGES.values())

# 显示翻译和保存按钮
if st.button("翻译并保存"):
    if uploaded_file is not None:
        # 读取文件内容
        file_contents = uploaded_file.read()

        # 分割为多个字幕
        subtitles = file_contents.split('\n\n')

        # 遍历每个字幕
        for i, subtitle in enumerate(subtitles):
            # 分割为三行
            lines = subtitle.split('\n')
            # 第一行是序号，第二行是时间范围，第三行是文本内容
            text = lines[2]
            # 遍历所有选中的语言
            for lang, name in LANGUAGES.items():
                if name in selected_languages:
                    # 翻译文本
                    translated_text = translate_srt(text, lang)
                    # 保存到文件
                    save_srt(translated_text, Path(f"{os.path.splitext(uploaded_file.name)[0]}_{i}_{lang}.srt"))
    
        # 显示成功消息
        st.success("字幕翻译并保存成功")
    else:
        # 如果没有选择文件，显示错误消息
        st.error("请先选择一个SRT文件")