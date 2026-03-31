import torch
import soundfile as sf
from kokoro import KPipeline
import json

def create_voice_en(folder_path):
    pipeline = KPipeline(lang_code='a') 

    with open("result/the_ocean/script.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    voice = data["full_voice_script"]

    text = voice

    generator = pipeline(text, voice='af_heart', speed=1)

    for i, (gs, ps, audio) in enumerate(generator):
        print(f"Processing part {i}...")
        sf.write(f'result/the_ocean/voice_{i}.wav', audio, 24000)
        print(f"Saved: output_{i}.wav")