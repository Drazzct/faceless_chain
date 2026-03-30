from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import json
from langchain_core.output_parsers import JsonOutputParser
import re
from image import create_image
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ai_base_url: str
    ai_model_name: str
    ai_api_key: str = "none"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Khởi tạo settings
settings = Settings()

# Khởi tạo model cực kỳ gọn gàng
model = ChatOpenAI(
    base_url=settings.ai_base_url,
    model=settings.ai_model_name,
    api_key=settings.ai_api_key,
)

parser = JsonOutputParser()

def create_model(topic):
    json_format = """
    {
    "metadata": {
        "topic": "Tên chủ đề",
        "duration_target": "60s",
        "language_voice": "Vietnamese",
        "language_tags": "English"
    },
    "script": [
        {
        "segment_id": 1,
        "voice_text": "Nội dung lời thoại tiếng Việt (khoảng 12-15 giây mỗi đoạn để tổng đạt 60s).",
        "image_to_show": "English tags for Stable Diffusion, comma separated, high quality, masterpiece, [Chi tiết hình ảnh]"
        }
    ]
    }
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
         Bạn là một chuyên gia biên kịch và kỹ sư AI (Prompt Engineer). 
         Nhiệm vụ của bạn là tạo ra một kịch bản video ngắn 60 giây về chủ đề được cung cấp.
        """),
        
        ("human", """
        Hãy trả về DUY NHẤT một đối tượng JSON (không kèm văn bản giải thích) theo cấu trúc sau: {json_format}
        
        # QUY TẮC NỘI DUNG
        1. **Voice Text (Tiếng Việt):** Lời thoại phải tự nhiên, lôi cuốn, phù hợp với giọng đọc AI. Tổng độ dài 5 đoạn phải khớp với khoảng 150-180 từ tiếng Việt để đảm bảo thời lượng 60 giây.
        2. **Image Tags (Tiếng Anh):** Mỗi đoạn phải có 1 mô tả hình ảnh dạng TAGS. Phải bao gồm các từ khóa chất lượng cao như: "8k resolution, cinematic lighting, highly detailed".
        3. **Số lượng:** Phải có chính xác 5 đoạn (segments).
        4. **Chủ đề:** {topic}

        # VÍ DỤ TAGS MẪU
        "majestic tiger, cosmic galaxy background, glowing red eyes, sharp focus, digital art, hyperrealistic"
        """)
    ])

    chain = prompt | model | parser

    response = chain.invoke({"topic": topic, "json_format": json_format})
    
    return response

def slugify(text):
    text = text.lower()
    
    # 3. Thay thế khoảng trắng và ký tự đặc biệt bằng dấu gạch ngang (-)
    # Chỉ giữ lại chữ cái, số và dấu gạch ngang
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '_', text).strip('_')
    
    return text

def processing():
    topic = input("Please type in your choosen topic: ")

    response = create_model(topic)

    print(response)

    if (topic):
        folder_path = f"./result/{slugify(topic)}"
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        with open(f"{folder_path}/script.json", "w", encoding="utf-8") as f:
            json.dump(response, f, indent=4, ensure_ascii=False)
        
        for i in range(len(response["script"])):
            prompt = response["script"][i]["image_to_show"]
            # create_image(prompt, folder_path, i)

if __name__ == "__main__":
    print("1. Full pipeline")
    print("2. Upload video")

    option = input("Please choose (1-2): ")

    match option:
        case "1":
            print("Processing full pipeline")
            processing()
        case "2":
            print("Prcessing using uploaded video")
        case _:
            print("Invalid arguement!")