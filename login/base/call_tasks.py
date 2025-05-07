from celery import shared_task
from django.core.management import call_command

@shared_task
def run_reset_tasks_command():
    call_command('reset_tasks')