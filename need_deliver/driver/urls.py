from django.contrib import admin

from django.urls import path, include

from driver import views
from .views import driver_list
# from django.views.decorators.csrf import csrf_exempt
# from .views import login
# from other_app.views import Home
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [ 
    path('driver-list', driver_list, name='driver-list'),
    path('driver_list_json', views.driver.as_view(), name='driver_list_json'),
    path( 'details/<int:id>/', views.RecordDetailsDriver.as_view()),
    path( 'details_popup/<int:id>/', views.RecordDetailsDriverPopUp.as_view()),
    path( 'joining-report', views.DriverJoiningReport.as_view()),
    path( 'updateCustomerRecords/<int:pk>/', views.driver.as_view(),name="updateCustomer"),
    path( 'updateCustomerRecords/', views.driver.as_view(),name="updateCustomer"),
    path( 'updateDriverUsersRecords', views.UpdateMultiRecordUsers.as_view()),
    path( 'deleteAttacment', views.deleteAttachmentFile.as_view()),
    path( 'checkUniquePhone', views.checkUniquePhoneNumber.as_view()),

    path('driver-cancelled-trip-list', views.driver_cancelled_trip_list, name='driver-cancelled-trip-list'),
    path('driver_cancelled_trip_json', views.driver_cancelled_trip.as_view(), name='driver_cancelled_trip_json'),
    path('cancel-trip-details/<int:id>/', views.RecordCancelTripDetails.as_view()),
    
    path( 'edit/<int:id>/', views.RecordDetailsDriver.as_view()),
    path( 'add/', views.driverAddForm),

    path( 'get-vehiclemodel-by-vtype/<int:id>/', views.getVehicleModelByVehicleType.as_view()),
   
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

