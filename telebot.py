from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

import asyncio
import datetime
import logging

from data import  get_schedule,chat_id_load,chat_id_save,get_time_lesson
from config import tg_token,teacher,send_time,delta_days

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

bot = Bot(token = tg_token)
dp = Dispatcher()
chat_id = chat_id_load()


@dp.message(Command("start"))
async def start(message: types.Message):
    global chat_id
    chat_id = message.chat.id
    
    chat_id_save(chat_id)
    

    logger.info(f"Новый старт: Chat ID={chat_id}, User ID={message.from_user.id}")  # type: ignore
    await message.answer("✅ Чат зарегистрирован для получения уведомлений!")

async def send_notification():

    date = (datetime.date.today() + datetime.timedelta(days=delta_days)).strftime("%d.%m.%Y")
    try:
        schedule_data = get_schedule(teacher, date)
    except Exception as e:
        logger.error(f"Проблема с получением расписания {e}")
    if not schedule_data or chat_id is None:
        return


    groups_usable = set()
    message = f"📅 Расписание на {date}:\n"
    for pair in schedule_data:
        groups_uniq = []
        for group in schedule_data[pair]:
            if group not in groups_usable:
                groups_usable.add(group)
                groups_uniq.append(group)
        if groups_uniq:
            message += f"В {get_time_lesson[pair]} у групп:"  + ", ".join(groups_uniq) + "\n"
    
    message += f"Завтра занятие. Не опаздывать!"
    
    await bot.send_message( chat_id=chat_id, text=message)



async def send_message_by_schedule():
    while True:
        if datetime.datetime.now().strftime('%H:%M')  == send_time:
            await send_notification()
        await asyncio.sleep(60)


async def main():
    scheduler_task = asyncio.create_task(send_message_by_schedule())
    await dp.start_polling(bot)
    await scheduler_task

if __name__ == "__main__":
    for i in range(100):
        try:
            asyncio.run(main())
        except Exception as e:
            logger.error(f"Критическая ошибка: {e}")
    logger.error("Лимит критических ошибок переполнен. Пожалуйста перезапустите приложение.")
