from django.contrib import admin

from django.urls import path, include

from customer import views
from .views import cust_list
# from django.views.decorators.csrf import csrf_exempt
# from .views import login
# from other_app.views import Home
urlpatterns = [ 
    path('cust-list', views.cust_list, name='cust-list'),
    path('customer_list_json', views.customer.as_view(), name='customer_list_json'),
    path( 'details/<int:id>/', views.RecordDetailsUsers.as_view(), name='users_record_details'),
    path( 'updateCustomerRecords/<int:pk>/', views.customer.as_view(),name="updateCustomer"),
    path( 'updateCustomerRecords/', views.customer.as_view(),name="updateCustomer"),
    path( 'updateUsersRecords', views.UpdateMultiRecordUsers.as_view()),
]

