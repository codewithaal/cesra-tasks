from django.urls import path, include
from .views import loginView, tasksList, alertSection, profilePicture, home
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
 path("", home, name="home"),
 path("accounts/logout/", loginView, name="loginView"),
 path("tasks/", tasksList, name="tasksList"),
 path("alerts/", alertSection, name="alertSection"),
 path("notifications/", views.notifications, name='notifications'),
 path("profile/", profilePicture, name="profilePicture"),
 path("accounts/", include("django.contrib.auth.urls")),
 path('change-password/', views.change_password, name='changePassword'),
 path('update-date/<int:report_id>/', views.update_date_submitted, name='update_date'),
 path('mark-done-inline/<int:report_id>/', views.mark_done_inline, name='mark_done_inline'),
 path('undo/<int:report_id>/', views.undo_report, name='undo_report'),
 path('undo_submission/<int:report_id>/', views.undo_submission, name='undo_submission'),
]