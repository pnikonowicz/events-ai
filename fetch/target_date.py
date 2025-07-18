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
    def Today():
        return "today"
    
    def Tomorrow():
        return "tomorrow"
    
    def Friday():
        return "friday"
    
class QueryDate:
    class Today:
        def meetup():
            return MeetupQueryDate.Today()
        def eventbrite():
            return EventbriteQueryDate.Today()
        def day():
            return "today"
        
    class Tomorrow:
        def meetup():
            return MeetupQueryDate.Tomorrow()
        def eventbrite():
            return EventbriteQueryDate.Tomorrow()
        def day():
            return "tomorrow"
    
    class Friday:
        def meetup():
            return MeetupQueryDate.Friday()
        def eventbrite():
            return EventbriteQueryDate.Friday()
        def day():
            return "friday"
    
