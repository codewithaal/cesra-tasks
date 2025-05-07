from django.core.management.base import BaseCommand
from django.utils.timezone import localtime
from django.db.models import Q
from base.models import Report

class Command(BaseCommand):
    help = "Reset only date_submitted and is_done fields for current month's completed tasks"

    def handle(self, *args, **kwargs):
        now = localtime()
        current_year = now.year
        current_month_name = now.strftime("%B")  
        
        matching_reports = Report.objects.filter(
            display_year=current_year,
            display_month__icontains=current_month_name,  
            assigned_to__isnull=False
        ).filter(
            Q(is_done=True) | Q(date_submitted__isnull=False)
        )

        updated_count = matching_reports.update(
            is_done=False,
            date_submitted=None
        )

        self.stdout.write(self.style.SUCCESS(f"Reset {updated_count} task(s)"))