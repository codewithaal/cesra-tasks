from django.contrib import admin
from django import forms
from .models import Report

# Define a custom form for the Report model
class ReportAdminForm(forms.ModelForm):
    MONTH_CHOICES = [
        ("January", "January"),
        ("February", "February"),
        ("March", "March"),
        ("April", "April"),
        ("May", "May"),
        ("June", "June"),
        ("July", "July"),
        ("August", "August"),
        ("September", "September"),
        ("October", "October"),
        ("November", "November"),
        ("December", "December"),
    ]

    display_month = forms.MultipleChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Display Months"
    )

    class Meta:
        model = Report
        fields = "__all__"

    def clean_display_month(self):
        return self.cleaned_data['display_month']

# Customize the admin panel for Report model
class ReportAdmin(admin.ModelAdmin):
    form = ReportAdminForm
    list_display = ('task_name', 'display_month', 'display_year', 'is_done')
    list_filter = ('display_year', 'is_done')
    search_fields = ('task_name',)

    def save_model(self, request, obj, form, change):
        obj.display_month = form.cleaned_data['display_month']
        super().save_model(request, obj, form, change)

# Register the Report model using the custom admin
admin.site.register(Report, ReportAdmin)