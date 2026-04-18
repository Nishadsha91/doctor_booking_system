from datetime import datetime,timedelta

def generate_slots(start,end,duration):

    slots = []

    current = datetime.combine(datetime.today(),start)

    end_time = datetime.combine(datetime.today(),end)

    while current < end_time:

        slots.append(current.time())

        current += timedelta(minutes=duration)

    return slots