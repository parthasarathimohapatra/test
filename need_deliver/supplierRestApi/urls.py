from django.conf.urls import url
from . import views
urlpatterns = [
	url( 'distance_calculation/', views.DistanceCalculation.as_view()),
	url( 'cost_calculation/', views.CostCalculation.as_view()),
    url( 'order_processing/', views.OrderProcessing.as_view()),
    url( 'vehicle_types/', views.VehicleTypes.as_view()),
    url( 'cancellation_reason/(?P<pk>[0-9]+)', views.CancelBooking.as_view()),
    # url( 'cancellation_reason/(?P<lang>[-\w]+)/$', views.OrderProcessing.as_view()),
    url( 'cancel_booking/$', views.CancelBooking.as_view()),
    url( 'book_nearest_driver/$', views.NearestVehicleBooking.as_view()),
    url( 'driver_response/(?P<pk>[0-9]+)', views.DriverResponse.as_view()),
    url( 'review_types/$', views.ReviewTypes.as_view()),
    url( 'review_post/$', views.ReviewPost.as_view()),
    url( 'fetch_driver_details', views.FetchDriverDetails.as_view()),
    url( 'cancel_reasons', views.CancelReasons.as_view()),
    url( 'coupon_calculation_validation', views.CouponCalculationValidation.as_view()),
    url( 'cash_in_hand_calculation', views.CashInHandCalculation.as_view()),
    url( 'closest_vehicle_selection', views.CloesetVehicleSelection.as_view()),
    url( 'supplier_booking_history/', views.BookingHistoryWithPagination.as_view()), 
    url( 'supplier_ongoing_booking/', views.OngoingBooking.as_view()), 
    
    
]

