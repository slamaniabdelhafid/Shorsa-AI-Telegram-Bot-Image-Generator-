import base64
from gigachat import GigaChat
from gigachat.models import Image, Chat, Messages, MessagesRole
import os
from dotenv import load_dotenv
import urllib3
 
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
SECRET = os.getenv("SECRET")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
key = base64.b64encode(f"{CLIENT_ID}:{SECRET}".encode("utf-8")).decode("utf-8")
 
from bs4 import BeautifulSoup
 
def image_generator(prompt):
    # Инициализируем клиент
    giga = GigaChat(credentials=key, verify_ssl_certs=False)

    # Формируем запрос
    payload = Chat(
        messages=[
            Messages(
                role=MessagesRole.USER,
                content=prompt
            )
        ],
        model="GigaChat-Pro",  # Или "GigaChat-Lite"
        function_call="auto",  # Включаем автоматический вызов функций
        functions=[{"name": "text2image"}]  # Указываем нужную функцию
    )

    # Отправляем запрос
    response = giga.chat(payload)

    # Извлекаем идентификатор изображения
    image_id = None
    for choice in response.choices:
        if "<img src=" in choice.message.content:
            # Ищем UUID в теге <img>
            start = choice.message.content.find('<img src="') + len('<img src="')
            end = choice.message.content.find('"', start)
            image_id = choice.message.content[start:end]
            break

    if image_id:
        print(f"Идентификатор изображения: {image_id}")
        print(f"Ссылка для скачивания: https://gigachat.devices.sberbank.ru/api/v1/files/{image_id}/content")
        image = giga.get_image(image_id)
    return image
    
    # try:
    #     soup = BeautifulSoup(chat_response, "html.parser")
    #     img_tag = soup.find('img')
    #     if img_tag and img_tag.get('src'):
    #         file_id_from_tag = img_tag['src']
    #         print("suuuui", file_id_from_tag)
    #         image_data = giga.get_image(file_id_from_tag)
    #         if image_data and image_data.content:
    #             print(f"Debug: Image content size from GigaChat: {len(image_data.content)} bytes")
    #             return image_data.content
    #         else:
    #             print("Debug: No image content received from GigaChat.")
    #             return b''
    # except Exception as e:
    #     print(f"Error processing image from GigaChat response: {e}")
    
    # return b''
 
 
    
 
# Сохранение изображения в файл
#with open('image.jpg', mode="wb") as fd:
    #fd.write(base64.b64decode(image.content))
 
 
