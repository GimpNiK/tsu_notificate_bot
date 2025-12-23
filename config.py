from pathlib import Path

BOT_TOKEN = "<yout_token>"
TEACHER = "<teacher>"
SEND_TIME = "21:00"
DELTA_DAYS = 1

#telebot.py config
BOT_LOG = "bot.log"
MAX_ERROR = 100
RATE_CHECK_DATETIME = 60
TIME_FORMAT = "%H:%M"

START_MESSAGE ="✅ Чат зарегистрирован для получения уведомлений!"

MAIN_MESSAGE_HEAD = lambda date:f"📅 Расписание на {date}:\n"
MAIN_MESSAGE_BODY = lambda pair,groups: f"В {GET_TIME_LESSON[pair]} у групп: "  + ", ".join(groups) + "\n"
MAIN_MESSAGE_END = f"Завтра занятие. Не опаздывать!"

#data.py config
CURRENT_DIR = Path(__file__).parent.absolute()
CHAT_ID_FILE    = CURRENT_DIR / "chat_id.txt"

SCHEDULE_URL    = "https://tulsu.ru/schedule/queries/"
GETDATES_URL    = SCHEDULE_URL + "GetDates.php"
GETSCHEDULE_URL = SCHEDULE_URL + "GetSchedule.php"

URL1_PARAMS = {
    'search_value': "search_value",
    "min_date": "MIN_DATE",
    'search_field': "SEARCH_FIELD",

}
URL2_PARAMS = {
    'search_field':'search_field',
    'search_value':'search_value',
    'date':'DATE_Z',
    'group_p':"GROUP_P",
    'groups': "GROUPS",
}
ENCODING = "utf-8"
DATE_FORMAT_INPUT = "%d.%m.%Y"
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

REQUEST_TIMEOUT = 30
GET_TIME_LESSON = {
    1: "7:45",
    2: "9:40", 
    3: "11:35",
    4: "13:40",
    5: "15:35",
    6: "17:30",
}
