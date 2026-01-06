import asyncio
import edge_tts
import re
import subprocess
import os
import requests
import datetime

# --- CONFIGURACIÓN ---
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
VIDEO_OUTPUT_DIR = "videos_generados"
os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)
# Ruta de la fuente instalada en el Dockerfile (fonts-liberation)
FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def get_background_video(query="agriculture nature drone", output_path="temp_video.mp4"):
    """Descarga clips de alta calidad. Si falla, usa un color sólido."""
    if PEXELS_API_KEY:
        url = "https://api.pexels.com/videos/search"
        headers = {"Authorization": PEXELS_API_KEY}
        params = {"query": query, "orientation": "landscape", "per_page": 1}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                videos = response.json().get("videos", [])
                if videos:
                    video_url = videos[0].get("video_files")[0].get("link")
                    video_data = requests.get(video_url).content
                    with open(output_path, 'wb') as handler:
                        handler.write(video_data)
                    return output_path
        except Exception as e:
            print(f"Error en Pexels: {e}")
    return None

async def produce_video(text_to_say, vpd, temp):
    """Genera video con Intro, Datos fijos y Subtítulos limpios."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    audio_file = os.path.join(VIDEO_OUTPUT_DIR, f"locucion_{timestamp}.mp3")
    video_output = os.path.join(VIDEO_OUTPUT_DIR, f"agro_report_{timestamp}.mp4")
    
    # 1. Limpiar el texto para FFmpeg (quitar paréntesis y escapar dos puntos)
    # Gemini a veces pone (Música...), esto lo elimina:
    clean_speech = re.sub(r'\(.*?\)', '', text_to_say).strip()
    # Escapar caracteres críticos para el filtro drawtext
    text_for_ffmpeg = clean_speech.replace(":", "\\:").replace("'", "").replace(",", "")
    short_sub = text_for_ffmpeg[:60] + "..." # Versión corta para el subtítulo

    # 2. Obtener clip de acción
    bg_video = get_background_video(query="corn field farming")
    if not bg_video:
        # Fallback si no hay video: creamos uno negro de 5 seg para que no de error
        bg_video = "color_fallback.mp4"
        subprocess.run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1280x720:d=5', bg_video])

    # 3. Voz con Álvaro
    communicate = edge_tts.Communicate(clean_speech, "es-ES-AlvaroNeural")
    await communicate.save(audio_file)

    # 4. Duración del audio
    cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_file]
    duration = float(subprocess.run(cmd_dur, capture_output=True, text=True).stdout.strip())

    # 5. FILTROS PRO: Intro, Datos en esquina y Subtítulos
    # Añadimos fontfile={FONT_PATH} para que Docker no falle
    video_filter = (
        f"scale=1280:720,format=yuv420p,"
        f"drawtext=fontfile={FONT_PATH}:text='AGROSENTINEL REPORT':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,0,3)',"
        f"drawtext=fontfile={FONT_PATH}:text='VPD\: {vpd} kPa | T\: {temp}C':fontcolor=green:fontsize=36:x=40:y=h-60:box=1:boxcolor=black@0.7,"
        f"drawtext=fontfile={FONT_PATH}:text='{short_sub}':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=h-120:enable='gt(t,3)'"
    )

    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-stream_loop', '-1', '-i', bg_video,
        '-i', audio_file,
        '-vf', video_filter,
        '-c:v', 'libx264',
        '-t', str(duration),
        '-map', '0:v:0', '-map', '1:a:0',
        '-shortest',
        video_output
    ]
    
    subprocess.run(ffmpeg_cmd, check=True)
    return video_output