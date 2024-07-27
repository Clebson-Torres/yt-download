import streamlit as st
import yt_dlp
import os
import tempfile
import shutil
import io

def download_youtube_video(url, max_height=1080):
    with tempfile.TemporaryDirectory() as temp_dir:
        ydl_opts = {
            'format': f'bestvideo[ext=mp4][height<={max_height}]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                if os.path.exists(filename):
                    # Lê o arquivo em memória
                    with open(filename, "rb") as file:
                        file_data = file.read()
                    return True, file_data, os.path.basename(filename), ""
                else:
                    return False, None, "", f"Arquivo não encontrado: {filename}"
        except Exception as e:
            return False, None, "", str(e)

st.title('YouTube Video Downloader')

url = st.text_input('Insira o link do vídeo do YouTube:')
max_resolution = st.selectbox('Selecione a resolução máxima:', [1080, 720, 480, 360])

if st.button('Preparar Download'):
    if url:
        with st.spinner('Preparando o vídeo para download...'):
            success, file_data, file_name, error_message = download_youtube_video(url, max_resolution)
            
            if success:
                st.success('Vídeo pronto para download!')
                try:
                    st.download_button(
                        label="Baixar Vídeo",
                        data=io.BytesIO(file_data),
                        file_name=file_name,
                        mime="video/mp4"
                    )
                except Exception as e:
                    st.error(f"Erro ao preparar o download: {str(e)}")
            else:
                st.error(f'Erro ao preparar o vídeo: {error_message}')
    else:
        st.warning('Por favor, insira um link de vídeo válido.')
