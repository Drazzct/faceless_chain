from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
import json
from langchain_core.output_parsers import JsonOutputParser
import re
from image import create_image_server
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ai_base_url: str
    ai_model_name: str
    ai_api_key: str = "none"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra='ignore'
    )

settings = Settings()

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
        "topic": "Topic Name",
        "duration": "60s",
        "total_words": "approx 150-180 words"
    },
    "full_voice_script": "The entire 60-second continuous narration in English.",
    "visual_segments": [
        {
        "segment_id": 1,
        "image_description": "A clear description of the scene in English",
        "diffusion_prompt": "masterpiece, 8k, cinematic lighting, [Stable Diffusion tags here...]"
        }
    ]
    }
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are an expert Scriptwriter and AI Prompt Engineer. 
        Your task is to create a professional 60-second video script in English 
        and 5 high-quality image prompts in English for Stable Diffusion.
        """),
        
        ("human", """
        Please return ONLY a JSON object based on the following topic: {topic}
        
        ### JSON STRUCTURE GUIDE:
        {json_format}
        
        ### CONTENT RULES:
        1. **full_voice_script (English):** - Write a continuous, engaging narration without breaks.
           - Length: 150-180 words (precisely for 60 seconds).
           - Tone: Captivating and storytelling.
           
        2. **visual_segments (Exactly 5 items):**
           - **image_description:** A prose description of what the image shows.
           - **diffusion_prompt:** High-quality tags for Stable Diffusion (e.g., "photorealistic, 8k, highly detailed, cinematic lighting, trending on artstation").
           - These 5 images should represent key moments throughout the 60-second script.

        3. **Language:**
           - Script: English.
           - Image Prompts & Metadata: English.
           
        Return only raw JSON. No conversational filler.
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
        
        # create_image
        create_image_server(folder_path)

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