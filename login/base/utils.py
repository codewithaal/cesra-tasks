from datetime import date, timedelta
from .models import Report
from base.models import Notification
from django.urls import reverse
import calendar

def get_last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]

def get_next_due_date(day):
    today = date.today()
    year = today.year
    month = today.month

    if day == 'eom':
        last_day = get_last_day_of_month(year, month)
        due_date = date(year, month, last_day)
        if today > due_date:
            if month == 12:
                year += 1
                month = 1
            else:
                month += 1
            last_day = get_last_day_of_month(year, month)
            due_date = date(year, month, last_day)
        return due_date

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
        last_day = get_last_day_of_month(year, month)
        return date(year, month, last_day)

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
        
        {"label": "25th of January", "day": 25, "month": 1},
        {"label": "30th of January of the ff year", "day": 30, "month": 1},
        {"label": "31st of January of the ff year", "day": 31, "month": 1},
        {"label": "15th of February", "day": 15, "month": 2},
        {"label": "16th of February", "day": 16, "month": 2},
        {"label": "20th of February", "day": 20, "month": 2},
        {"label": "30th of March", "day": 30, "month": 3},
        {"label": "30th of April", "day": 30, "month": 4},
        {"label": "30th of June", "day": 30, "month": 6},
        {"label": "15th of December", "day": 15, "month": 12},
        {"label": "30th of the month", "day": 30, "months": [1, 7]},
    ]

    for schedule in task_schedule:
        year = today.year + schedule.get("year_offset", 0)

        try:
            if schedule.get("eom"):
                # End of current month
                due_date = get_next_due_date('eom')

            elif "months" in schedule:
                if today.month in schedule["months"]:
                    due_date = date(today.year, today.month, schedule["day"])
                else:
                    continue  
            elif "month" in schedule:
                due_date = date(year, schedule["month"], schedule["day"])

            else:
                due_date = date(today.year, today.month, schedule["day"])

            upcoming_alert_day_7 = due_date - timedelta(days=7)
            upcoming_alert_day_6 = due_date - timedelta(days=6)
            upcoming_alert_day_5 = due_date - timedelta(days=5)
            upcoming_alert_day_4 = due_date - timedelta(days=4)
            upcoming_alert_day_3 = due_date - timedelta(days=3)
            upcoming_alert_day_2 = due_date - timedelta(days=2)
            upcoming_alert_day_1 = due_date - timedelta(days=1)

            if today == upcoming_alert_day_7:
                reports = Report.objects.filter(day__iexact=schedule["label"], assigned_to=user)
                for task in reports:
                    days_remaining = (due_date - today).days
                    formatted_days = f"{days_remaining} day" if days_remaining == 1 else f"{days_remaining} days"
                    alert_tasks.append({
                        'task_name': task.task_name,
                        'days_remaining': formatted_days,
                    })
            
            if today == upcoming_alert_day_6:
                reports = Report.objects.filter(day__iexact=schedule["label"], assigned_to=user)
                for task in reports:
                    days_remaining = (due_date - today).days
                    formatted_days = f"{days_remaining} day" if days_remaining == 1 else f"{days_remaining} days"
                    alert_tasks.append({
                        'task_name': task.task_name,
                        'days_remaining': formatted_days,
                    })
            
            if today == upcoming_alert_day_5:
                reports = Report.objects.filter(day__iexact=schedule["label"], assigned_to=user)
                for task in reports:
                    days_remaining = (due_date - today).days
                    formatted_days = f"{days_remaining} day" if days_remaining == 1 else f"{days_remaining} days"
                    alert_tasks.append({
                        'task_name': task.task_name,
                        'days_remaining': formatted_days,
                    })
            
            if today == upcoming_alert_day_4:
                reports = Report.objects.filter(day__iexact=schedule["label"], assigned_to=user)
                for task in reports:
                    days_remaining = (due_date - today).days
                    formatted_days = f"{days_remaining} day" if days_remaining == 1 else f"{days_remaining} days"
                    alert_tasks.append({
                        'task_name': task.task_name,
                        'days_remaining': formatted_days,
                    })
            
            if today == upcoming_alert_day_3:
                reports = Report.objects.filter(day__iexact=schedule["label"], assigned_to=user)
                for task in reports:
                    days_remaining = (due_date - today).days
                    formatted_days = f"{days_remaining} day" if days_remaining == 1 else f"{days_remaining} days"
                    alert_tasks.append({
                        'task_name': task.task_name,
                        'days_remaining': formatted_days,
                    })
            
            if today == upcoming_alert_day_2:
                reports = Report.objects.filter(day__iexact=schedule["label"], assigned_to=user)
                for task in reports:
                    days_remaining = (due_date - today).days
                    formatted_days = f"{days_remaining} day" if days_remaining == 1 else f"{days_remaining} days"
                    alert_tasks.append({
                        'task_name': task.task_name,
                        'days_remaining': formatted_days,
                    })
            
            if today == upcoming_alert_day_1:
                reports = Report.objects.filter(day__iexact=schedule["label"], assigned_to=user)
                for task in reports:
                    days_remaining = (due_date - today).days
                    formatted_days = f"{days_remaining} day" if days_remaining == 1 else f"{days_remaining} days"
                    alert_tasks.append({
                        'task_name': task.task_name,
                        'days_remaining': formatted_days,
                    })

        except ValueError:
            continue

    return alert_tasks

def create_task_transfer_notification(report, user):
    message = f"Report '{report.task_name}' was marked as submitted by {user.get_full_name()}."
    url = reverse("report_detail", args=[report.id])  
    Notification.objects.create(user=report.assigned_to, message=message, url=url)