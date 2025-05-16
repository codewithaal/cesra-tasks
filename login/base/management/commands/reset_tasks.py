from django.core.management.base import BaseCommand
from django.utils.timezone import localtime
from django.db.models import Q
from base.models import Report
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Reset only date_submitted and is_done fields for current month's completed tasks"

    def handle(self, *args, **kwargs):
        # Get current UTC time
        now_utc = datetime.utcnow()
        # Convert to Philippine Time (UTC+8)
        now_ph = now_utc + timedelta(hours=8)

        # Only run at midnight PH time on the 1st day of the month
        if now_ph.day != 1 or now_ph.hour != 0:
            self.stdout.write("Not midnight of the 1st in PH time. Skipping reset.")
            return

        now = localtime()
        current_year = now.year
        current_month_name = now.strftime("%B")  # e.g. 'May'

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