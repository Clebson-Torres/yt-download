import streamlit as st
import yt_dlp
import os
import tempfile
import shutil

st.set_page_config(
    page_title="yt-download Clebin",
    page_icon= "./icon.png"
    )

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
                    # Copia o arquivo para um local temporário que o Streamlit pode acessar
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                    shutil.copy2(filename, temp_file.name)
                    return True, temp_file.name, ""
                else:
                    return False, "", f"Arquivo não encontrado: {filename}"
        except Exception as e:
            return False, "", str(e)

st.title('Clebin YouTube Video Downloader')

url = st.text_input('Insira o link do vídeo do YouTube:')
max_resolution = st.selectbox('Selecione a resolução máxima:', [1080, 720, 480, 360])

if st.button('Preparar Download'):
    if url:
        with st.spinner('Preparando o vídeo para download...'):
            success, file_path, error_message = download_youtube_video(url, max_resolution)
            
            if success:
                st.success('Vídeo pronto para download!')
                try:
                    with open(file_path, "rb") as file:
                        st.download_button(
                            label="Baixar Vídeo",
                            data=file,
                            file_name=os.path.basename(file_path),
                            mime="video/mp4"
                        )
                except Exception as e:
                    st.error(f"Erro ao preparar o download: {str(e)}")
                finally:
                    # Limpa o arquivo temporário
                    if os.path.exists(file_path):
                        os.unlink(file_path)
            else:
                st.error(f'Erro ao preparar o vídeo: {error_message}')
    else:
        st.warning('Por favor, insira um link de vídeo válido.')
