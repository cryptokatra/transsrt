import streamlit as st
from easynmt import EasyNMT
import chardet
import opencc

model = EasyNMT('opus-mt')
converter = opencc.OpenCC('s2twp.json')

LANGS = [('zh', 'ja'), ('zh', 'es'), ('zh', 'fr'), ('zh', 'en'), ('zh', 'ko')]

def translate(sent, source, target):
    return model.translate(sent, source_lang=source, target_lang=target)

def convert(text):
    return converter.convert(text)

def detect_encoding(file):
    rawdata = file.read()
    return chardet.detect(rawdata)['encoding']

def display_props():
    st.markdown("## Subtitle Translator")
    st.sidebar.markdown('## Possible Translations')
    st.sidebar.text("\n")
    st.sidebar.markdown("* Chinese _(zh)_ - Japanese _(ja)_")
    st.sidebar.markdown("* Chinese _(zh)_ - Spanish _(es)_")
    st.sidebar.markdown("* Chinese _(zh)_ - French _(fr)_")
    st.sidebar.markdown("* Chinese _(zh)_ - English _(en)_")
    st.sidebar.markdown("* Chinese _(zh)_- Korean _(ko)_")
    st.sidebar.text("\n")
    st.sidebar.text("\n")
    st.sidebar.markdown('Powered by: [EasyNMT](https://pypi.org/project/EasyNMT/0.0.7/) and [Streamlit](https://www.streamlit.io/)')
    return

display_props()

source_lang_content = st.file_uploader("", type=['srt'])

if source_lang_content is not None:
    all_data = [convert(line.decode(detect_encoding(source_lang_content))) for line in source_lang_content]
    num_lines = sum(1 for line in all_data)
    step = int(num_lines/100)

    for idx1, lang_pair in enumerate(LANGS):
        if idx1 == 0:
            st.markdown('Processing  __{0}__  to  __{1}__'.format(lang_pair[0], lang_pair[1]))
            outfile = open('{0}_{1}.srt'.format(lang_pair[0], lang_pair[1]), 'w', encoding='utf-8')
        if idx1 == 1:
            st.markdown('Processing  __{0}__  to  __{1}__'.format(lang_pair[0], lang_pair[1]))
            outfile = open('{0}_{1}.srt'.format(lang_pair[0], lang_pair[1]), 'w', encoding='utf-8')
        if idx1 == 2:
            st.markdown('Processing  __{0}__  to  __{1}__'.format(lang_pair[0], lang_pair[1]))
            outfile = open('{0}_{1}.srt'.format(lang_pair[0], lang_pair[1]), 'w', encoding='utf-8')
        if idx1 == 3:
            st.markdown('Processing  __{0}__  to  __{1}__'.format(lang_pair[0], lang_pair[1]))
            outfile = open('{0}_{1}.srt'.format(lang_pair[0], lang_pair[1]), 'w', encoding='utf-8')
        if idx1 == 4:
            st.markdown('Processing  __{0}__  to  __{1}__'.format(lang_pair[0], lang_pair[1]))
            outfile = open('{0}_{1}.srt'.format(lang_pair[0], lang_pair[1]), 'w', encoding='utf-8')

        my_bar = st.progress(0)
        big_srt_text = ""
        v = 0
        for idx2, line in enumerate(all_data):
            print(idx2, v, num_lines, step)
            line = str(line)
            if v != 100:
                if idx2 % step == 0:
                    v += 1
                    my_bar.progress(v)

            if line[0].isnumeric():
                big_srt_text += line
            else:
                converted_line = translate(line, lang_pair[0], lang_pair[1])
                big_srt_text += converted_line

        outfile.write(big_srt_text)
        if idx1 == len(LANGS)-1:
            st.markdown('### Translations Done!!')
            st.write('Files saved on Disk')
