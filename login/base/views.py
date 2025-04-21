from PIL import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.core.files.base import ContentFile
from .models import Report
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from django.http import HttpResponseForbidden
from django.db.models import Case, When, Value, IntegerField
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.utils import timezone
import base64
import io

@login_required
def home(request):
 return render(request, "home.html", {})

def loginView(request):
 return redirect("base:login")

def alertSection(request):
 return render(request, "alerts.html", {})

def profilePicture(request):
    from .models import UserProfile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if request.POST.get('cropped_image'):
            cropped_image_data = request.POST['cropped_image']
            format, imgstr = cropped_image_data.split(';base64,')  # e.g., data:image/jpeg;base64,...
            ext = format.split('/')[-1]
            img_data = base64.b64decode(imgstr)

            image = Image.open(io.BytesIO(img_data))
            image_io = io.BytesIO()
            image.save(image_io, format=ext)
            image_file = ContentFile(image_io.getvalue(), name=f'{request.user.username}_profile.{ext}')

            user_profile.profile_picture.save(image_file.name, image_file)
            user_profile.save()

            return redirect('base:profilePicture')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile.html', {'form': form, 'user_profile': user_profile})
  
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keep the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('base:loginView')  # Redirect to the profile page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})

@require_POST
def update_date_submitted(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    date = request.POST.get("date")

    if not date:
        return HttpResponseBadRequest("Missing date")

    report.date_submitted = date
    report.save()

    html = render_to_string("report_row.html", {"report": report, "user": request.user})
    return HttpResponse(html)

@login_required
def mark_done_inline(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if request.user != report.verified_by:
        return HttpResponseForbidden("Not allowed.")

    report.is_done = True
    report.save()

    # Render undo button
    html = render_to_string('undo_row.html', {'report': report})
    return HttpResponse(html)

@login_required
def tasks(request):
    now = timezone.now()
    reports = Report.objects.filter(
        display_month__year=now.year,
        display_month__month=now.month,
        is_done=False
    )
    return render(request, 'tasks.html', {'reports': reports, 'now': now})

def mark_done(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    
    if report.verified_by == request.user:
        report.is_done = True
        report.save()

    return redirect('base:tasksList')

@login_required
def tasksList(request):
    today = now()
    current_month = today.strftime('%B')
    current_year = today.year

    # Reset old tasks
    outdated_reports = Report.objects.filter(
        display_month__icontains=current_month,
        display_year__lt=current_year
    )
    for report in outdated_reports:
        report.date_submitted = None
        report.display_year = current_year
        report.save()

    # Rank 'End of the month' tasks to the bottom
    reports = Report.objects.filter(
        display_month__icontains=current_month,
        display_year=current_year,
        is_done=False
    ).annotate(
    is_end_of_month=Case(
        When(day__icontains='End of the month', then=Value(1)),
        default=Value(0),
        output_field=IntegerField()
    )
).order_by('is_end_of_month', 'task_name')

    context = {
        'reports': reports,
        'display_month': current_month,
        'display_year': current_year
    }
    return render(request, 'tasks.html', context)

@login_required
def undo_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if request.user != report.verified_by:
        return HttpResponseForbidden("Not allowed.")

    report.is_done = False
    report.save()

    # Re-render the row
    html = render_to_string('report_row.html', {'report': report, 'user': request.user})
    return HttpResponse(html)