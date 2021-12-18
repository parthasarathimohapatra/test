from django.conf.urls import url
from . import views
urlpatterns = [
	url( 'driver_attachments/', views.DriverAndVehicleDocuments.as_view()),
	url( 'driver_registration/', views.DriverRegistration.as_view()),
	url( 'driver_login/', views.DriverLogin.as_view()), 
	url( 'vehicle_models_by_type/', views.AllVehicleModels.as_view()),
	url( 'forgot_password/', views.ForgotPassword.as_view()),
	url( 'set_new_password/', views.ForgotPassword.as_view()),
	url( 'otp_verification_forgotpassword/', views.ForgotPasswordOTPVerify.as_view()),
	url( 'delivery_acknowledgement/', views.DeliveryAcknowledgement.as_view()),
	url( 'complete_trip/(?P<pk>[0-9]+)', views.DeliveryAcknowledgement.as_view()),	
	url( 'arrived_at_pickup_location/', views.PickupLocationArrived.as_view()),
	url( 'driver_bookings/', views.BookingRequestsByDriver.as_view()),	
	url( 'driver_status_change/', views.TempDriverStatusChange.as_view()),	
	url( 'check_driver_availablity/', views.ChecKOnGoingBooking.as_view()),	
	url( 'booking_history/', views.BookingHistoryWithPagination.as_view()),	
	url( 'complete_ongoing_booking_by_driver/', views.CompleteBookingByDriver.as_view()),	
	url( 'cancel_ongoing_booking_by_driver/', views.CancelBookingByDriver.as_view()),	
	url( 'cost_calculation_at_anytime/', views.CalculateCostingAtAnyTime.as_view()),
	url( 'driver_location_save_to_db/', views.DriverLocationSaveToDB.as_view()),
	url( 'current_booking_details/', views.CurrentBookingDetails.as_view()),
	url( 'update_driver_details/', views.UpdateDriverProfileDetails.as_view()),
	url( 'check_order_status_before_accept/', views.CheckOrderStatusBeforeAccept.as_view()),
	url( 'get_credit_balance/', views.DriverAccountBalance.as_view()),	
	url( 'get_booking_all_details', views.GetBookingAllDetails.as_view()),
	url( 'check_balance_status/', views.CheckBalanceStatus.as_view()), 
    
]

