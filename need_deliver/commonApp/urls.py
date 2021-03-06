from django.conf.urls import url
from . import views
urlpatterns = [
   url( 'login/', views.Login.as_view()),
   url( 'save_basic_info/(?P<pk>[0-9]+)$', views.Login.as_view()),
   url( 'login_otp_generate/', views.LoginOTP.as_view()),
   url( 'country_list/', views.Countries.as_view()),
   url( 'home_banner_images/', views.HomeBannerSlider.as_view()),
   url( 'splash_banner_images/', views.SplashBannerSlider.as_view()),
   url( 'update_profile_picture/', views.UpdateProfilePicture.as_view()),
   url( 'users_record_details/$', views.UsersRecordDetails.as_view()),
   url( 'save_your_location/$', views.SaveLocations.as_view()),
   url( 'saved_locations_list_by_id/', views.SaveLocationsList.as_view()),
   url( 'update_saved_location/(?P<pk>[0-9]+)/$', views.SaveLocations.as_view()),
   url( 'delete_location/(?P<pk>[0-9]+)/$', views.SaveLocations.as_view()),
   url( 'get_otp_by_number/', views.GetOtpByName.as_view()),
   url( 'order_details/', views.OrderDetails.as_view()),
   url( 'all_vehicle_types/$', views.AllVehicleTypes.as_view()),
   url( 'check_loggedin_status/$', views.CheckLoggedInStatus.as_view()),
   url( 'change_phone_number/$', views.ChangePhoneNumber.as_view()),
   url( 'delete_record/(?P<pk>[0-9]+)$', views.DeleteRecord.as_view()),
   url( 'test_sms/$', views.TestSms.as_view()),
   url( 'app_version_checker', views.AppVersionChecker.as_view()),
   url( 'logout', views.Logout.as_view()),
   url('remove_device_token', views.RemoveDeviceToken.as_view()),
   url( 'version_check_automatic', views.VersionCheckAutomatic.as_view()),
   url( 'automatic_device_token_insert', views.AutoDeviceTokenUpdate.as_view()),
   url('check_account_status', views.CheckAccountStatus.as_view()),
]

