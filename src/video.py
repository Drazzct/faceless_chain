from moviepy.editor import ImageClip, AudioFileClip, concatenate_audioclips, concatenate_videoclips, TextClip, CompositeVideoClip
import os
import json
import re
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})

def split_full_text(folder_path, num_parts=3):
    with open(f"{folder_path}/script.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    full_text = data["full_voice_script"]
    
    sentences = re.split(r'(?<=[.!?])\s+', full_text.strip())
    
    # Gom các câu lại thành đúng 5 nhóm
    avg = len(sentences) // num_parts
    if avg == 0: avg = 1
    
    parts = []
    for i in range(num_parts):
        if i == num_parts - 1: # Nhóm cuối lấy hết phần còn lại
            parts.append(" ".join(sentences[i*avg:]))
        else:
            parts.append(" ".join(sentences[i*avg : (i+1)*avg]))
    return parts


def create_video(folder_path):
    images = []
    audios = []
    for resource in sorted(os.listdir(folder_path)):
        if resource.endswith(".png"):
            images.append(f"{folder_path}/{resource}")
        if resource.endswith(".wav"):
            audios.append(f"{folder_path}/{resource}")

    audio_clips = [AudioFileClip(f) for f in audios]
    final_audio = concatenate_audioclips(audio_clips)
    captions_list = split_full_text(folder_path, 3)

    total_duration = final_audio.duration
    
    duration_per_segment =  total_duration / len(images)
    video_segments = []

    for i, img_path in enumerate(images):
        # 1. Tạo clip ảnh gốc
        img_clip = ImageClip(img_path).set_duration(duration_per_segment)
        
        # 2. Tạo phụ đề cho đoạn này
        # captions_list là danh sách các câu văn tương ứng với từng ảnh
        txt_clip = TextClip(
            captions_list[i], 
            fontsize=50, 
            color='white', 
            font='Arial',
            stroke_color='black', # Viền chữ đen cho dễ đọc
            stroke_width=1,
            method='caption',      # Tự động xuống dòng nếu câu quá dài
            size=(img_clip.w * 0.8, None) # Chiều rộng bằng 80% ảnh
        ).set_duration(duration_per_segment).set_position(('center', 'bottom')) # Hiện ở dưới cùng

        # 3. Đè chữ lên ảnh dùng CompositeVideoClip
        segment_with_sub = CompositeVideoClip([img_clip, txt_clip])
        video_segments.append(segment_with_sub)

    final_visuals = concatenate_videoclips(video_segments, method="compose")

    final_video = final_visuals.set_audio(final_audio)

    final_video.write_videofile(
        f"{folder_path}/my_ai_video.mp4", 
        fps=24, 
        codec="libx264", 
        audio_codec="aac",
        temp_audiofile='temp-audio.m4a', 
        remove_temp=True
    )

    final_video.close()
    final_audio.close()
    for a in audio_clips: a.close()
    for v in video_segments: v.close()

if __name__ == "__main__":
    create_video("result/the_ocean")