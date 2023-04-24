import streamlit as st
from easynmt import EasyNMT
from pathlib import Path
from pysubs2 import SSAFile,SSAEvent

model = EasyNMT('opus-mt')

TARGET_LANGS = ['ja', 'es', 'fr', 'en', 'ko']

def translate(sent, source, target):
    return model.translate(sent, source_lang=source, target_lang=target)

st.sidebar.markdown("## 字幕翻译器")
st.sidebar.text("\n")
st.sidebar.markdown("目标语言：日语、西班牙语、法语、英语、韩语")
st.sidebar.text("\n")
st.sidebar.text("\n")
st.sidebar.markdown('Powered by EasyNMT and Streamlit')

input_subtitle = st.file_uploader("请上传SRT字幕文件", type='srt')

if input_subtitle is not None:
    input_content = SSAFile.from_string(input_subtitle.read().decode('utf-8'))
    st.write('上传成功！')

    translated_subtitles = {}
    for lang in TARGET_LANGS:
        st.write(f'开始翻译为{lang}...')
        translated_subs = SSAFile()
        for event in input_content.events:
            translated_text = translate(event.text, 'zh', lang)
            translated_subs.events.append(
                SSAEvent(start=event.start,
                         end=event.end,
                         text=translated_text))
        translated_subtitles[lang] = translated_subs
        st.write(f'{lang}翻译完成！')

    if st.button("下载翻译后的字幕文件"):
        for lang in TARGET_LANGS:
            output_file_name = f"{Path(input_subtitle.name).stem}-{lang}.srt"
            with open(output_file_name, 'w') as f:
                f.write(translated_subtitles[lang].to_string())
                st.markdown(f'[点此下载 {output_file_name}]({output_file_name})')
