import datetime

class MeetupQueryDate:
    def Today(date_time=datetime.datetime.today()):
        return date_time.strftime("%Y-%m-%d")
    
    def Tomorrow(date_time_now=datetime.datetime.now(), date_time_delta=datetime.timedelta(days=1)): 
        return (date_time_now + date_time_delta).strftime("%Y-%m-%d")

class EventbriteQueryDate:
    def Today():
        return "today"
    
    def Tomorrow():
        return "tomorrow"