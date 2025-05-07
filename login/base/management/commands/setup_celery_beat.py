from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils import timezone

class Command(BaseCommand):
    help = 'Set up periodic task to run at midnight on the first day of every month.'

    def handle(self, *args, **kwargs):
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute='0',  
            hour='0',    
            day_of_month='1',  
            month_of_year='*',  
            day_of_week='*',    
        )

        PeriodicTask.objects.get_or_create(
            crontab=schedule,
            name='Run reset_tasks command monthly',
            task='base.tasks.run_reset_tasks_command',
        )

        self.stdout.write(self.style.SUCCESS('Periodic task set to run at midnight on the first day of every month'))