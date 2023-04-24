import os
import streamlit as st
from googletrans import Translator
from pathlib import Path


def translate_srt_file(srt_file_path, language_codes):
    try:
        translator = Translator()
        with open(srt_file_path, 'r', encoding='utf-8') as f:
            original_srt_text = f.read()
            for language_code in language_codes:
                translated_text = translator.translate(original_srt_text, dest=language_code).text
                output_file_path = os.path.splitext(srt_file_path)[0] + f'_{language_code}.srt'
                Path(output_file_path).write_text(translated_text)
    except Exception as e:
        st.error(str(e))


def main():
    st.set_page_config(page_title="SRT Translator")

    st.title("SRT Translator")

    # Create browse file button
    srt_file = st.file_uploader("Upload your SRT file", type=['srt'])

    # Create language checkboxes
    st.subheader("Choose target languages:")
    language_codes = ['ja', 'es', 'fr', 'en', 'ko']
    selected_languages = st.multiselect('Select languages', language_codes, default=language_codes)

    # Create translate button
    if st.button("Translate and save"):
        if srt_file is not None:
            srt_file_path = srt_file.name
            translate_srt_file(srt_file_path, selected_languages)
            st.success("Translation completed and files saved to local directory!")

if __name__ == "__main__":
    main()
