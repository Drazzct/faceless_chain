from vieneu import Vieneu
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["HF_TOKEN"]

tts = Vieneu()

# 1. List preset voices
available_voices = tts.list_preset_voices()
for desc, name in available_voices:
    print(f"   - {desc} (ID: {name})")

text = "Bãi biển rộng lớn vô bờ nơi con người chưa một ai đặt chân đến. Tại đó ẩn chứa vô vàn những bí ẩn đang chờ được khám phá"

if available_voices:
    _, my_voice_id = available_voices[1] if len(available_voices) > 1 else available_voices[0]
    voice_data = tts.get_preset_voice(my_voice_id)
    audio_spec = tts.infer(text=text, voice=voice_data)
    tts.save(audio_spec, f"result/the_ocean/standard_{my_voice_id}.wav")
    print(f"💾 Saved synthesis to: result/the_ocean/standard_{my_voice_id}.wav")

tts.close()


