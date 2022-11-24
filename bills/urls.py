from django.urls import path

from bills.views import BillViewSet

app_name = 'bills'

urlpatterns = [
    path(
        'bill/',
        BillViewSet.as_view({'post': 'create'}),
        name='bills-file',
    ),
]
