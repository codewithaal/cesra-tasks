from datetime import date, timedelta
from .models import Report
import calendar

#Helper function to get the last day of a month
def get_last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]

#Function to get the next due date based on a specific day or 'eom' for end of the month
def get_next_due_date(day):
    today = date.today()
    year = today.year
    month = today.month

    #Handle 'End of the month' as a special case with day = 'eom'
    if day == 'eom':
        last_day = get_last_day_of_month(year, month)
        due_date = date(year, month, last_day)
        if today > due_date:
            # Move to the next month if due date is in the past
            if month == 12:
                year += 1
                month = 1
            else:
                month += 1
            last_day = get_last_day_of_month(year, month)
            due_date = date(year, month, last_day)
        return due_date

    #Handle normal fixed day logic
    try:
        due_date = date(year, month, day)
        if today > due_date:
            #Move to next month if the due date is in the past
            if month == 12:
                year += 1
                month = 1
            else:
                month += 1
            due_date = date(year, month, day)
        return due_date
    except ValueError:
        #Handle invalid day (e.g., Feb 30), fall back to last day of that month
        last_day = get_last_day_of_month(year, month)
        return date(year, month, last_day)

# Function to get upcoming tasks for a user
def get_upcoming_tasks(user):
    today = date.today()
    alert_tasks = []

    task_schedule = [
        {"label": "Every 2nd", "day": 2},
        {"label": "Every 5th", "day": 5},
        {"label": "Every 10th", "day": 10},
        {"label": "Every 15th", "day": 15},
        {"label": "Every 17th", "day": 17},
        {"label": "17th of the ff month", "day": 17},
        {"label": "Every 20th", "day": 20},
        {"label": "29th of the ff month", "day": 29},
        {"label": "30th of the ff month", "day": 30},
        {"label": "End of the month", "eom": True},
        
        #Specific fixed dates
        {"label": "15th of February", "day": 15, "month": 2},
        {"label": "15th of December", "day": 15, "month": 12},
        {"label": "16th of February", "day": 16, "month": 2},
        {"label": "20th of February", "day": 20, "month": 2},
        {"label": "25th of January", "day": 25, "month": 1},
        {"label": "30th of April", "day": 30, "month": 4},
        {"label": "30th of June", "day": 30, "month": 6},
        {"label": "30th of January of the ff year", "day": 30, "month": 1},
        {"label": "31st of January of the ff year", "day": 31, "month": 1},
        {"label": "30th of March", "day": 30, "month": 3},
        {"label": "30th of the month", "day": 30, "months": [1, 7]},
    ]

    for schedule in task_schedule:
        year = today.year + schedule.get("year_offset", 0)

        try:
            if schedule.get("eom"):
                #End of current month
                due_date = get_next_due_date('eom')

            elif "months" in schedule:
                # e.g. 30th of the month only on Jan and Jul
                if today.month in schedule["months"]:
                    due_date = date(today.year, today.month, schedule["day"])
                else:
                    continue  #Skip this schedule if not in allowed months

            elif "month" in schedule:
                #Fixed specific date
                due_date = date(year, schedule["month"], schedule["day"])

            else:
                #Regular same-month schedule
                due_date = date(today.year, today.month, schedule["day"])

            #Alert 7 days before due date
            upcoming_alert_day_7 = due_date - timedelta(days=7)
            #Alert 6 days before due date
            upcoming_alert_day_6 = due_date - timedelta(days=6)
            #Alert 5 days before due date
            upcoming_alert_day_5 = due_date - timedelta(days=5)
            #Alert 4 days before due date
            upcoming_alert_day_4 = due_date - timedelta(days=4)
            #Alert 3 days before due date
            upcoming_alert_day_3 = due_date - timedelta(days=3)
            #Alert 2 days before due date
            upcoming_alert_day_2 = due_date - timedelta(days=2)
            #Alert 1 day before due date
            upcoming_alert_day_1 = due_date - timedelta(days=1)
            # Alert on the due date
            upcoming_alert_day = due_date

            if today == upcoming_alert_day_7:
                reports = Report.objects.filter(day__iexact=schedule["label"], assigned_to=user)
                for task in reports:
                    days_remaining = (due_date - today).days
                    alert_tasks.append({
                        'task_name': task.task_name,
                        'days_remaining': days_remaining,
                    })
            
            if today == upcoming_alert_day_6:
                reports = Report.objects.filter(day__iexact=schedule["label"], assigned_to=user)
                for task in reports:
                    days_remaining = (due_date - today).days
                    alert_tasks.append({
                        'task_name': task.task_name,
                        'days_remaining': days_remaining,
                    })
            
            if today == upcoming_alert_day_5:
                reports = Report.objects.filter(day__iexact=schedule["label"], assigned_to=user)
                for task in reports:
                    days_remaining = (due_date - today).days
                    alert_tasks.append({
                        'task_name': task.task_name,
                        'days_remaining': days_remaining,
                    })
            
            if today == upcoming_alert_day_4:
                reports = Report.objects.filter(day__iexact=schedule["label"], assigned_to=user)
                for task in reports:
                    days_remaining = (due_date - today).days
                    alert_tasks.append({
                        'task_name': task.task_name,
                        'days_remaining': days_remaining,
                    })
            
            if today == upcoming_alert_day_3:
                reports = Report.objects.filter(day__iexact=schedule["label"], assigned_to=user)
                for task in reports:
                    days_remaining = (due_date - today).days
                    alert_tasks.append({
                        'task_name': task.task_name,
                        'days_remaining': days_remaining,
                    })
            
            if today == upcoming_alert_day_2:
                reports = Report.objects.filter(day__iexact=schedule["label"], assigned_to=user)
                for task in reports:
                    days_remaining = (due_date - today).days
                    alert_tasks.append({
                        'task_name': task.task_name,
                        'days_remaining': days_remaining,
                    })
            
            if today == upcoming_alert_day_1:
                reports = Report.objects.filter(day__iexact=schedule["label"], assigned_to=user)
                for task in reports:
                    days_remaining = (due_date - today).days
                    alert_tasks.append({
                        'task_name': task.task_name,
                        'days_remaining': days_remaining,
                    })
            
            if today == upcoming_alert_day:
                reports = Report.objects.filter(day__iexact=schedule["label"], assigned_to=user)
                for task in reports:
                    days_remaining = (due_date - today).days
                    alert_tasks.append({
                        'task_name': task.task_name,
                        'days_remaining': days_remaining,
                    })

        except ValueError:
            #Handles invalid dates like Feb 30
            continue

    return alert_tasks