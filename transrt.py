import streamlit as st
import os
from googletrans import Translator
from pysrt import SubRipFile

# 定義翻譯功能
def translate_srt_file(srt_file_path, language_codes):
    # 讀取 SRT 文件
    with open('0.srt', 'r', encoding='utf-8') as f:
        srt = SubRipFile().from_string(f.read())

    # 翻譯每一條字幕
    for subtitle in srt:
        for lang in language_codes:
            # 翻譯
            translator = Translator()
            translation = translator.translate(subtitle.text, dest=lang).text
            # 將翻譯添加到字幕中
            if lang == 'ja':
                subtitle.text_ja = translation
            elif lang == 'es':
                subtitle.text_es = translation
            elif lang == 'fr':
                subtitle.text_fr = translation
            elif lang == 'en':
                subtitle.text_en = translation
            elif lang == 'ko':
                subtitle.text_ko = translation

    # 將翻譯后的字幕保存到新文件
    srt.save('0_ja.srt', encoding='utf-8-sig', eol='\r\n')
    srt.save('0_es.srt', encoding='utf-8-sig', eol='\r\n')
    srt.save('0_fr.srt', encoding='utf-8-sig', eol='\r\n')
    srt.save('0_en.srt', encoding='utf-8-sig', eol='\r\n')
    srt.save('0_ko.srt', encoding='utf-8-sig', eol='\r\n')

# 定義可選擇的語言
languages = {'日文': 'ja', '西班牙文': 'es', '法文': 'fr', '英文': 'en', '韓文': 'ko'}

# Streamlit 界面設計
def app():
    st.title('SRT 字幕翻譯器')

    # 上傳本機文件
    srt_file = st.file_uploader('上傳 SRT 文件（格式必須為 SRT）', type='srt')

    if srt_file is not None:
        # 選擇要翻譯的語言
        st.write('選擇要翻譯的語言（可以多選）：')
        lang_choices = st.multiselect('語言', list(languages.keys()), list(languages.keys()))

        # 當用戶點擊翻譯按鈕時
        if st.button('翻譯'):
            # 獲取語言代碼
            language_codes = [languages[lang] for lang in lang_choices]

            # 確認文件是否存在
            if os.path.exists(srt_file.name):
                # 翻譯文件
                translate_srt_file(srt_file.name, language_codes)

                # 顯示翻譯成功信息
                st.success('SRT 文件已經翻譯成功，請檢查本機文件夾中的文件')
            else:
                # 顯示錯誤信息
                st.error('SRT 文件不存在')

# 運行應用程序
if __name__ == '__main__':
    app()
