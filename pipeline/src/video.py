from moviepy.editor import ImageSequenceClip
import os

image_folder = "result/the_ocean"

images = []

for img in sorted(os.listdir(image_folder)):
    if img.endswith(".png"):
        images.append(f"{image_folder}/{img}")

clip = ImageSequenceClip(images, fps=2)

clip.write_videofile(f"{image_folder}/my_ai_video.mp4", codec="libx264")