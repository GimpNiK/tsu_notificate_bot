from aiogram import Bot, Dispatcher, types

import asyncio
import datetime
import logging

from data import  get_schedule,chat_id_load,chat_id_save
from config import (
                    BOT_TOKEN,
                    TEACHER,
                    SEND_TIME,
                    DELTA_DAYS,
                    
                    START_MESSAGE,
                    MAIN_MESSAGE_HEAD,
                    MAIN_MESSAGE_BODY,
                    MAIN_MESSAGE_END,

                    BOT_LOG,
                    TIME_FORMAT,
                    RATE_CHECK_DATETIME,
                    MAX_ERROR,
                    ENCODING
)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(BOT_LOG, encoding = ENCODING),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

bot = Bot(token = BOT_TOKEN)
dp = Dispatcher()
chat_id = chat_id_load()


@dp.my_chat_member()
async def start(event: types.ChatMemberUpdated):
    global chat_id
    chat_id = event.chat.id
    
    chat_id_save(chat_id)
    

    logger.info(f"Start: Chat ID={chat_id}, User ID={event.from_user.id}")
    await event.answer(START_MESSAGE)

async def send_notification():

    date = (datetime.date.today() + datetime.timedelta(days=DELTA_DAYS)).strftime("%d.%m.%Y")
    try:
        schedule_data = get_schedule(TEACHER, date)
    except Exception as e:
        logger.error(f"Problem with getting the schedule {e}")
    if not schedule_data or chat_id is None:
        return


    groups_usable = set()
    message = MAIN_MESSAGE_HEAD(date)
    for pair in schedule_data:
        groups_uniq = []
        for group in schedule_data[pair]:
            if group not in groups_usable:
                groups_usable.add(group)
                groups_uniq.append(group)
        if groups_uniq:
            message += MAIN_MESSAGE_BODY(pair, groups_uniq)
    
    message += MAIN_MESSAGE_END
    
    await bot.send_message( chat_id=chat_id, text=message)



async def send_message_by_schedule():
    while True:
        if datetime.datetime.now().strftime(TIME_FORMAT)  == SEND_TIME:
            await send_notification()
        await asyncio.sleep(RATE_CHECK_DATETIME)


async def main():
    scheduler_task = asyncio.create_task(send_message_by_schedule())
    await dp.start_polling(bot)
    await scheduler_task

if __name__ == "__main__":
    for i in range(MAX_ERROR):
        try:
            asyncio.run(main())
        except Exception as e:
            logger.error(f"Critical error: {e}")
    logger.error("The critical error limit is full. Please restart the application.")
