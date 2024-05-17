from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from urllib.parse import unquote, quote
from pydub import AudioSegment
from io import BytesIO
from wssapi import run_predict
from time import sleep
import aiohttp
import re

app = FastAPI()

async def get_audio(text, speaker, speed):
    max_retries = 10
    retries = 0

    async with aiohttp.ClientSession() as session:
        while retries < max_retries:
            try:
                response = await run_predict(speaker, text)
                if response is None:
                    raise ValueError("run_predict returned None")
                file_url = response

                async with session.get(file_url) as audio_response:
                    if audio_response.status == 200:
                        content = await audio_response.read()
                        return AudioSegment.from_file(BytesIO(content), format="wav")
                    else:
                        retries += 1
                        print(f"Retry {retries}/{max_retries} for audio download.")
            except Exception as e:
                print(f"Error during get_audio: {e}")
                retries += 1

        if retries == max_retries:
            print("Max retries reached for audio download.")
            return None
@app.get('/process')
async def process_request(text: str = quote('未输入文本内容'), speaker: str = quote('派蒙_ZH'), speaker2: str = None, speed: float = 21):
    text = unquote(text)
    speaker = unquote(speaker)
    if speaker2:
        speaker2 = unquote(speaker2)
    text = text.replace(" ", ",")
    text = text.replace("+", "加")
    text = text.replace("-", "减")
    text = text.replace("\u3000", "")

    # 分割引号内外的文本
    parts = re.split(r'(["“”])', text)
    combined_audio = None
    inside_quotes = False

    for part in parts:
        if part in ['"', '“', '”']:
            inside_quotes = not inside_quotes
            continue
        if part.strip() == "":
            continue
        current_speaker = speaker2 if inside_quotes and speaker2 else speaker
        audio_segment = await get_audio(part, current_speaker, speed)
        if audio_segment:
            if combined_audio is None:
                combined_audio = audio_segment
            else:
                combined_audio = combined_audio.append(audio_segment, crossfade=0)

    if combined_audio:
        buffer = BytesIO()
        combined_audio.export(buffer, format="mp3")
        buffer.seek(0)
        return Response(content=buffer.read(), media_type='audio/mp3')
    else:
        return JSONResponse(content={'error': 'Failed to generate audio'}, status_code=500)
