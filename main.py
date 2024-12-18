from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
from PIL import Image
import os

# Ваш токен Telegram-бота
API_TOKEN = "7904802317:AAGlyX-J3bQnopolyw3OAyRaWxRsS9LflL4"

# Создание бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Директория для временного хранения фотографий
TEMP_DIR = "temp_photos"

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@dp.message_handler(content_types=ContentType.PHOTO)
async def handle_photo(message: types.Message):
    # Загружаем фото
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = file_info.file_path
    downloaded_file = await bot.download_file(file_path)

    # Сохраняем фото во временный файл
    input_path = os.path.join(TEMP_DIR, f"{photo.file_id}.jpg")
    with open(input_path, "wb") as f:
        f.write(downloaded_file.read())

    # Обрезаем изображение
    output_path = os.path.join(TEMP_DIR, f"cropped_{photo.file_id}.jpg")
    crop_image(input_path, output_path)

    # Отправляем обрезанное изображение пользователю
    with open(output_path, "rb") as f:
        await bot.send_photo(chat_id=message.chat.id, photo=f)

    # Удаляем временные файлы
    os.remove(input_path)
    os.remove(output_path)

def crop_image(input_path, output_path):
    with Image.open(input_path) as img:
        width, height = img.size
        top_crop = 245
        bottom_crop = 245

        # Рассчитываем новую высоту
        new_height = height - top_crop - bottom_crop
        if new_height <= 0:
            raise ValueError("Высота изображения слишком мала для обрезки.")

        # Обрезаем изображение
        cropped_img = img.crop((0, top_crop, width, height - bottom_crop))
        cropped_img.save(output_path)

if __name__ == "__main__":
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    executor.start_polling(dp, skip_updates=True)
