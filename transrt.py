import streamlit as st 
from easynmt import EasyNMT 
 
model = EasyNMT('opus-mt') 
LANGS = ['ja', 'es', 'fr', 'en', 'ko'] 
LANG_NAMES = {'ja': '日本語', 'es': 'スペイン語', 'fr': 'フランス語', 'en': '英語', 'ko': '韓国語'} 
 
def translate(sent, source, target): 
    return model.translate(sent, source_lang=source, target_lang=target) 
 
def display_props(): 
    st.markdown("## Subtitle Translator") 
    st.sidebar.markdown('## Possible Translations') 
    for lang in LANGS: 
        st.sidebar.markdown("* English _(en)_ - {} _({})_".format(LANG_NAMES[lang], lang)) 
    st.sidebar.text("\n") 
    st.sidebar.text("\n") 
    st.sidebar.markdown('Powered by: [EasyNMT](https://pypi.org/project/EasyNMT/0.0.7/) and [Streamlit](https://www.streamlit.io/)') 
    return 
 
def save_file(filename, content): 
    with open(filename, "w", encoding="utf-8-sig") as f: 
        f.write(content) 
 
display_props() 
 
source_lang_content = st.file_uploader("Upload SRT file", type=['srt']) 
 
if source_lang_content is not None: 
    all_data = [line.decode().strip() for line in source_lang_content.readlines()] 
    num_lines = len(all_data) 
    step = int(num_lines/100) 
 
    for lang in LANGS: 
        st.markdown('Processing from English to {}'.format(LANG_NAMES[lang])) 
        big_srt_text = "" 
        outfile = open('{}_translated.srt'.format(lang), 'w', encoding="utf-8-sig") 
        v = 0 
        for idx, line in enumerate(all_data): 
            if v!=100: 
                if idx%step==0: 
                    v+=1 
            if line and line[0].isdigit(): 
                big_srt_text += line+'\n' 
            elif line.strip(): 
                converted_line = translate(line, 'en', lang) 
                big_srt_text += converted_line+'\n' 
            else: 
                big_srt_text += '\n' 
 
        save_file('{}_translated.srt'.format(lang), big_srt_text) 
    st.markdown('### Translations Done!!') 
    st.write('Files saved on Disk')
