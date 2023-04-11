from django.urls import path

from . import views


def trigger_error(request):
    division_by_zero = 1 / 0
    return division_by_zero


app_name = 'lettings'

urlpatterns = [
    path('lettings/', views.index, name='index'),
    path('lettings/<int:letting_id>/', views.letting, name='letting'),
    path('sentry-debug/', trigger_error),
]
