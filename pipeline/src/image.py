import os 
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import json
import requests
import base64

load_dotenv()

client = InferenceClient(
    provider="hf-inference",
    api_key=os.environ["HF_TOKEN"]
)

def extract_prompt(folder_path):
    with open(f"{folder_path}/script.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    prompts = []
    for prompt in data["visual_segments"]:
        prompts.append(prompt["diffusion_prompt"])
    return prompts

negative_prompt  = (
        "lowres, bad anatomy, text, error, cropped, worst quality, low quality, "
        "jpeg artifacts, watermark, blurry, out of focus, multiple images, "
        "split screen, multi panel, collage, distorted, grainy"
    )

def create_image_hf(prompt, folder_path, num):
    image = client.text_to_image(
                prompt,
                negative_prompt=negative_prompt,
                model="stabilityai/stable-diffusion-xl-base-1.0",
            )

    file_path = f"{folder_path}/generated_image_{num}.png"
    image.save(file_path)

def create_image_server(folder_path):
    url = os.getenv("SD_API_URL", "http://127.0.0.1:7860")

    prompts = extract_prompt(folder_path)

    for num, prompt in enumerate(prompts):
        payload = {
        "prompt": prompt,
        "negative_prompt": "negative_prompt",
        "steps": 30,
        "seed": -1,
        "cfg_scale": 5,
        "width": 1024,
        "height": 1024,
        "sampler_name": "Euler a"
        }
        
        response = requests.post(f'{url}/sdapi/v1/txt2img', json=payload)

        r = response.json()
        for i in r['images']:
            image_data = base64.b64decode(i.split(",", 1)[0])
            with open(f"{folder_path}/generated_image_{num}.png", 'wb') as f:
                f.write(image_data)
        print("Đã tạo ảnh thành công!")


if __name__ == "__main__":
    data = extract_prompt("result/the_ocean")

    for num, prompt in enumerate(data):
        print(prompt)