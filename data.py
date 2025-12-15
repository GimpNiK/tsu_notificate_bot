import json
import urllib.parse
import urllib.request
from typing import Dict, List
from datetime import datetime
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
chat_id_file = current_dir / "chat_id.txt"


def get_schedule(teacher: str, date: str) -> Dict[int, List[str]]:
    base_url = "https://tulsu.ru/schedule/queries/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    
    try:
        url1 = base_url + 'GetDates.php'
        data1 = urllib.parse.urlencode({'search_value': teacher}).encode('utf-8')
        req1 = urllib.request.Request(url1, data=data1, headers=headers, method='POST')
        
        with urllib.request.urlopen(req1) as res:
            data1 = json.loads(res.read().decode('utf-8'))
        
        if not data1.get('MIN_DATE'):
            return {}
        
        params2 = urllib.parse.urlencode({
            'search_field': data1['SEARCH_FIELD'],
            'search_value': teacher
        })
        
        url2 = base_url + 'GetSchedule.php?' + params2
        req2 = urllib.request.Request(url2, headers=headers)
        
        with urllib.request.urlopen(req2) as res:
            schedule_data = json.loads(res.read().decode('utf-8'))
        
        if date:
            target_date = datetime.strptime(date, "%d.%m.%Y")
            schedule_data = [
                lesson for lesson in schedule_data 
                if lesson.get('DATE_Z') and 
                datetime.strptime(lesson['DATE_Z'], "%d.%m.%Y") == target_date
            ]
        
        result = {}
        for i, lesson in enumerate(schedule_data, 1):
            groups = [
                group.get('GROUP_P', '') 
                for group in lesson.get('GROUPS', [])
            ]
            result[i] = [g for g in groups if g]
        
        return result
    
    except Exception:
        return {}

def chat_id_load():
    

    with open(chat_id_file, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content:
            chat_id = int(content)

        else:
            chat_id = None
    return chat_id

def chat_id_save(chat_id):
    with open(chat_id_file, "w", encoding="utf-8") as f:
        f.write(str(chat_id))

get_time_lesson = {
    1:"7:45",
    2:"9:40",
    3:"11:35",
    4:"13:40",
    5:"15:35",
    6:"17:30",
}