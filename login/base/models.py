from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.utils.timezone import now

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='base/media/', default='static/images/user_dp.png')  

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

MONTH_CHOICES = (
    ('January', 'January'),
    ('February', 'February'),
    ('March', 'March'),
    ('April', 'April'),
    ('May', 'May'),
    ('June', 'June'),
    ('July', 'July'),
    ('August', 'August'),
    ('September', 'September'),
    ('October', 'October'),
    ('November', 'November'),
    ('December', 'December'),
)

def current_year():
    return timezone.now().year

class Report(models.Model):
    id = models.AutoField(primary_key=True)
    display_month = MultiSelectField(choices=MONTH_CHOICES, max_length=500)
    display_year = models.IntegerField(default=current_year)
    day = models.CharField(max_length=100)
    task_name = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_reports')
    date_submitted = models.DateField(null=True, blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verified_reports')
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name

    class Meta:
        indexes = [
            models.Index(fields=["display_month", "display_year"]),
        ]

    @classmethod
    def reset_all_tasks(cls, from_year):
        return cls.objects.filter(
            display_year=from_year
        ).update(is_done=False, date_submitted=None)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    url = models.URLField(null=True, blank=True)
    timestamp = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.message}"

    def time_since(self):
        from django.utils.timesince import timesince
        return timesince(self.timestamp, now()).split(',')[0] + " ago"