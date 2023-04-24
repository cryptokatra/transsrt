import streamlit as st
import os
from googletrans import Translator
from typing import List

def translate_srt_file(srt_file_path: str, language_codes: List[str]):
    # 打开原始srt文件
    with open(srt_file_path, 'r', encoding='utf-8') as f:
        # 读取srt字幕内容
        srt_content = f.read()

    # 循环翻译每个目标语言
    for language_code in language_codes:
        # 创建Google翻译器实例
        translator = Translator()
        # 翻译字幕内容
        translated_content = translator.translate(srt_content, dest=language_code).text
        # 构造新的文件路径
        new_file_path = srt_file_path[:-4] + '_' + language_code + '.srt'

        # 将翻译后的字幕内容写入新文件
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)

    st.write("五个srt文件已创建。")

# Streamlit App
def app():
    st.title("SRT字幕翻译")
    st.write("使用Google Translate将SRT字幕翻译成五种目标语言。")

    # 显示选择文件按钮
    srt_file = st.file_uploader("选择一个SRT字幕文件", type="srt")

    if srt_file and st.button("翻译并保存"):
        # 将checkbox的值作为参数传递给translate_srt_file函数
        language_codes = [lang_code for lang_code, selected in checkbox_state.items() if selected]
        # 执行翻译并保存
        translate_srt_file(srt_file.name, language_codes)

# 显示checkbox
checkbox_state = st.sidebar.multiselect("选择要翻译成的语言", options=["日文", "西班牙文", "法文", "英文", "韩文"], default=["日文", "西班牙文", "法文", "英文", "韩文"])

# 运行Streamlit App
if __name__ == '__main__':
    app()
