import streamlit as st
import yt_dlp
import os
import tempfile

# Configuração do logger
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@st.cache_data
def get_video_info(url):
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info
        except Exception as e:
            logger.error(f"Erro ao obter informações do vídeo: {str(e)}")
            return None

def download_youtube_video(url, max_height=1080):
    try:
        info = get_video_info(url)
        if not info:
            return False, None, "", "Não foi possível obter informações do vídeo."

        # Verifica o tamanho do vídeo
        file_size = info.get('filesize')
        if file_size and file_size > 200 * 1024 * 1024:  # 200 MB limit
            return False, None, "", "O vídeo é muito grande para download direto (limite de 200 MB)."

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            ydl_opts = {
                'format': f'bestvideo[ext=mp4][height<={max_height}]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': temp_file.name,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            temp_file.seek(0)
            file_data = temp_file.read()
            file_name = f"{info['title']}.mp4"
            
            return True, file_data, file_name, ""
    except Exception as e:
        logger.error(f"Erro durante o download: {str(e)}")
        return False, None, "", f"Erro durante o download: {str(e)}"

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
                        data=file_data,
                        file_name=file_name,
                        mime="video/mp4"
                    )
                except Exception as e:
                    logger.error(f"Erro ao preparar o botão de download: {str(e)}")
                    st.error(f"Erro ao preparar o download: {str(e)}")
            else:
                st.error(f'Erro ao preparar o vídeo: {error_message}')
    else:
        st.warning('Por favor, insira um link de vídeo válido.')
