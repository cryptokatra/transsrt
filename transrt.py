import streamlit as st
from googletrans import Translator
from pathlib import Path

# 根据选择的语言返回对应的语言代码
def get_language_code(language):
    if language == '日本語':
        return 'ja'
    elif language == 'Español':
        return 'es'
    elif language == 'Français':
        return 'fr'
    elif language == 'English':
        return 'en'
    elif language == '한국어':
        return 'ko'
    else:
        return None

# 翻译srt文件
def translate_srt_file(srt_file_path, language_codes):
    with open(srt_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    translator = Translator()
    for i in range(len(lines)):
        # 判断是否为时间轴行
        try:
            int(lines[i])
            is_time_line = True
        except ValueError:
            is_time_line = False
        
        # 如果不是时间轴行，则进行翻译
        if not is_time_line and lines[i] != '\n':
            for language_code in language_codes:
                translation = translator.translate(lines[i], src='zh-CN', dest=language_code)
                lines[i] += f'\n{language_code}:{translation.text}\n'
    
    # 保存翻译结果
    for language_code in language_codes:
        translated_file_path = str(srt_file_path)[:-4] + f'_{language_code}.srt'
        with open(translated_file_path, 'w', encoding='utf-8') as f:
            for line in lines:
                if f':{language_code}' in line:
                    f.write(line)
                elif not f':en' in line:
                    f.write(line)

# Streamlit app
def app():
    st.title('SRT文件翻译器')
    
    # 文件上传
    srt_file = st.file_uploader('选择要翻译的SRT文件', type=['srt'])
    if srt_file is not None:
        st.write('文件上传成功！')
        
        # 选择要翻译的语言
        language_list = ['日本語', 'Español', 'Français', 'English', '한국어']
        selected_languages = st.multiselect('选择要翻译的语言', language_list, default=language_list)
        language_codes = [get_language_code(language) for language in selected_languages]
        
        # 翻译并保存文件
        if st.button('翻译并保存文件'):
            srt_file_path = Path(srt_file.name)
            translate_srt_file(srt_file_path, language_codes)
            st.write('文件翻译成功！')
            
            # 显示保存的文件路径
            for language_code in language_codes:
                translated_file_path = str(srt_file_path)[:-4] + f'_{language_code}.srt'
                st.write(f'{selected_languages[language_codes.index(language_code)]}翻译结果保存在：{translated_file_path}')

if __name__ == '__main__':
    app()
