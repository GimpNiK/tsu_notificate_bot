import json
import urllib.parse
import urllib.request
from typing import Dict, List
from datetime import datetime
from config import (
    DEFAULT_HEADERS,
    GETDATES_URL,URL1_PARAMS,
    GETSCHEDULE_URL,URL2_PARAMS,

    ENCODING,
    DATE_FORMAT_INPUT,
    CHAT_ID_FILE)


def get_schedule(teacher: str, date: str) -> Dict[int, List[str]]:
    try:
        url1 = GETDATES_URL
        data1 = urllib.parse.urlencode({URL1_PARAMS['search_value']: teacher}).encode(ENCODING)
        req1 = urllib.request.Request(url1, data=data1, headers=DEFAULT_HEADERS, method='POST')
        
        with urllib.request.urlopen(req1) as res:
            data1 = json.loads(res.read().decode(ENCODING))
        
        if not data1.get(URL1_PARAMS["min_date"]):
            return {}
        
        params2 = urllib.parse.urlencode({
            URL2_PARAMS["search_field"]: data1[URL1_PARAMS["search_field"]],
            URL2_PARAMS['search_value']: teacher
        })
        
        url2 = GETSCHEDULE_URL+"?"+ params2
        req2 = urllib.request.Request(url2, headers = DEFAULT_HEADERS)
        
        with urllib.request.urlopen(req2) as res:
            schedule_data = json.loads(res.read().decode(ENCODING))
        
        if date:
            target_date = datetime.strptime(date, DATE_FORMAT_INPUT)
            schedule_data = [
                lesson for lesson in schedule_data 
                if lesson.get(URL2_PARAMS["date"]) and 
                datetime.strptime(lesson[URL2_PARAMS["date"]], DATE_FORMAT_INPUT) == target_date
            ]
        
        result = {}
        for i, lesson in enumerate(schedule_data, 1):
            groups = [
                group.get(URL2_PARAMS["group_p"], '') 
                for group in lesson.get(URL2_PARAMS["groups"], [])
            ]
            result[i] = [g for g in groups if g]
        
        return result
    
    except Exception:
        return {}

def chat_id_load():
    with open(CHAT_ID_FILE, "r", encoding=ENCODING) as f:
        content = f.read().strip()
        if content:
            chat_id = int(content)

        else:
            chat_id = None
    return chat_id

def chat_id_save(chat_id):
    with open(CHAT_ID_FILE, "w", encoding=ENCODING) as f:
        f.write(str(chat_id))

