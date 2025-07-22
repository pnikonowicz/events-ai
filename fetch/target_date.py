import datetime

class MeetupQueryDate:
    def Today(date_time=datetime.datetime.today()):
        return date_time.strftime("%Y-%m-%d")
    
    def Tomorrow(date_time_now=datetime.datetime.now(), date_time_delta=datetime.timedelta(days=1)): 
        return (date_time_now + date_time_delta).strftime("%Y-%m-%d")
    
    def Friday(date_time_now=datetime.datetime.now()):
        # Find the closest Friday (today if Friday, else next Friday)
        weekday = date_time_now.weekday()  # return the day number Monday=0, Sunday=6
        days_until_friday = (4 - weekday) % 7
        closest_friday = date_time_now + datetime.timedelta(days=days_until_friday)
        return closest_friday.strftime("%Y-%m-%d")

class EventbriteQueryDate:
    BASE_URL = "https://www.eventbrite.com/d/ny--new-york/events--{day}/?page={page_number}"

    def __init__(self, day: str):
        self.day = day

    def create(self, page_number: int) -> str:
        return self.BASE_URL.format(day=self.day, page_number=page_number)
    
class QueryDate:
    class Today:
        @staticmethod
        def meetup():
            return MeetupQueryDate.Today()
        @staticmethod
        def eventbrite():
            return EventbriteQueryDate("today")
        @staticmethod
        def day():
            return "today"

    class Tomorrow:
        @staticmethod
        def meetup():
            return MeetupQueryDate.Tomorrow()
        @staticmethod
        def eventbrite():
            return EventbriteQueryDate("tomorrow")
        @staticmethod
        def day():
            return "tomorrow"

    class Friday:
        @staticmethod
        def meetup():
            return MeetupQueryDate.Friday()
        @staticmethod
        def eventbrite():
            return EventbriteQueryDate("friday")
        @staticmethod
        def day():
            return "friday"
    
