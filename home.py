import streamlit as st
import yt_dlp
import urllib.parse

def get_direct_url(youtube_url, max_height=1080):
    ydl_opts = {
        'format': f'bestvideo[ext=mp4][height<={max_height}]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            if 'url' in info:
                return True, info['url'], info.get('title', 'video') + '.mp4', ""
            else:
                return False, "", "", "Não foi possível obter o link direto do vídeo."
    except Exception as e:
        return False, "", "", f"Erro ao processar o vídeo: {str(e)}"

st.title('YouTube Video Downloader')

url = st.text_input('Insira o link do vídeo do YouTube:')
max_resolution = st.selectbox('Selecione a resolução máxima:', [1080, 720, 480, 360])

if st.button('Gerar Link de Download'):
    if url:
        with st.spinner('Gerando link de download...'):
            success, direct_url, file_name, error_message = get_direct_url(url, max_resolution)
            
            if success:
                st.success('Link de download gerado com sucesso!')
                encoded_filename = urllib.parse.quote(file_name)
                download_link = f'<a href="{direct_url}" download="{encoded_filename}">Clique aqui para baixar o vídeo</a>'
                st.markdown(download_link, unsafe_allow_html=True)
                
                st.warning("Nota: O link de download é temporário e pode expirar após algum tempo.")
            else:
                st.error(f'Erro ao gerar o link: {error_message}')
    else:
        st.warning('Por favor, insira um link de vídeo válido.')
