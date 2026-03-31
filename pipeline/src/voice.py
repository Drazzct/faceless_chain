from vieneu import Vieneu
import os
from dotenv import load_dotenv
import json

def create_voice(folder_path):
    with open(f"{folder_path}/script.json", "r", encoding="utf-8") as f:
        voices = json.load(f)
    
    load_dotenv()
    os.environ["HF_TOKEN"]

    tts = Vieneu()

    available_voices = tts.list_preset_voices()

    for voice in voices["script"]:
        text = voice["voice_text"]
        
        if available_voices:
            _, my_voice_id = available_voices[1] if len(available_voices) > 1 else available_voices[0]
            voice_data = tts.get_preset_voice(my_voice_id)
            audio_spec = tts.infer(text=text, voice=voice_data)
            tts.save(audio_spec, f"{folder_path}/standard_{my_voice_id}.wav")
            print(f"💾 Saved synthesis to: result/the_ocean/standard_{my_voice_id}.wav")

    tts.close()

if __name__ == "__main__":
    with open(f"result/the_twin_tower/script.json", "r", encoding="utf-8") as f:
        voices = json.load(f)

    for voice in voices["script"]:
        print(voice)
