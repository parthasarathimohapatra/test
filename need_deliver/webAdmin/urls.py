from django.contrib import admin

from django.urls import path, include

from webAdmin import views
from django.conf import settings
from .views import dashboard, logout, reset_password, vehicletype_list,image_list, splah_screen_list,cancellation_reason_list, parcel_info_list, pickup_request_list, language_list, currency_list, order_list, vehiclemodel_list, driver_subscription_list, promotioncode_list
from django.views.generic import TemplateView

# from .views import login
# from other_app.views import Home
urlpatterns = [ 
    path('', dashboard, name='dashboard'),
    path('login', views.user.as_view(), name='login'),
    path( 'logout', logout, name='logout'),
    path( 'dashboard', dashboard, name='dashboard'),
    path( 'forgot_password_mail_send', views.ForgotPasswordMailSend.as_view(), name='forgot_password_mail_send'),
    path( 'changePassword', views.Change_password.as_view()),

    path( 'reset_password', reset_password, name='reset_password'),
    path( 'reset_password_ajax', views.ResetPassword.as_view(), name='reset_password_ajax'),
    # path( 'states/<int:id>/', views.States.as_view(), name='states'), 

    path('vehicletype-list', vehicletype_list, name='vehicletype-list'),
    path('vehicletype_list_json', views.vehicletype.as_view(), name='vehicletype_list_json'),
    path( 'vehicletype-details/<int:id>/', views.RecordDetailsVehicleType.as_view(), name='vehicletype_record_details'),
    path( 'updateVehicletypeRecords/<int:pk>/', views.vehicletype.as_view(),name="updateVehicletype"),
    path( 'updateVehicletypeRecords/', views.vehicletype.as_view(),name="updateVehicletype"),
    path( 'updateVehicleActionRecords', views.UpdateMultiRecordVehicleType.as_view()),

    path('banner-image-list', image_list, name='banner-image-list'),
    path('image-list-json', views.imagefile.as_view(), name='image-list-json'),
    path( 'image-details/<int:id>/', views.RecordDetailsImage.as_view(), name='image-details'),
    path( 'bannerImageRecords/<int:pk>/', views.imagefile.as_view(),name="bannerImageRecords"),
    path( 'bannerImageRecords/', views.imagefile.as_view(),name="bannerImageRecords"),
    path( 'updateImageActionRecords', views.UpdateMultiRecordImage.as_view()),

    path('splash-screen-list', splah_screen_list, name='splash-screen-list'),
    path('splash-screen-list-json', views.splash_screen.as_view(), name='splash-screen-list-json'),
    path( 'splash-screen-details/<int:id>/', views.RecordDetailsSplashscreen.as_view(), name='splash-screen-details'),
    path( 'updateSplashScreenRecords/<int:pk>/', views.splash_screen.as_view(),name="updateSplashScreenRecords"),
    path( 'updateSplashScreenRecords/', views.splash_screen.as_view(),name="updateSplashScreenRecords"),
    path( 'updateSplashScreenActionRecords', views.UpdateMultiRecordSplashScreen.as_view()),

    path('cancellation-reason-list', cancellation_reason_list, name='cancellation-reason-list'),
    path('cancellation-reason-list-json', views.cancellation_reason.as_view(), name='cancellation-reason-list-json'),
    path( 'cancellation-reason-details/<int:id>/', views.RecordDetailsCancellationReason.as_view()),
    path( 'updateCancellationReasonRecords/<int:pk>/', views.cancellation_reason.as_view()),
    path( 'updateCancellationReasonRecords/', views.cancellation_reason.as_view()),
    path( 'updateCancellationReasonActionRecords', views.UpdateMultiRecordCancellationReason.as_view()),

    path('parcel-info-list', parcel_info_list, name='parcel-info-list'),
    path('parcel-info-list-json', views.parcel_information.as_view(), name='parcel-info-list-json'),
    path('parcel-info-details/<int:id>/', views.RecordDetailsParcelInfo.as_view()),

    path('pickup-request-list', pickup_request_list, name='pickup-request-list'),
    path('pickup-request-list-json', views.pickup_request.as_view(), name='pickup-request-list-json'),
    path('pickup-request-details/<int:id>/', views.RecordDetailsPickupRequest.as_view()),

    path('language-list', language_list, name='language-list'),
    path('language-list-json', views.language.as_view(), name='language-list-json'),
    # path( 'language-details/<int:id>/', views.RecordDetailsLanguage.as_view(), name='language-details'),
    # path( 'languageRecords/<int:pk>/', views.language.as_view(),name="languageRecords"),
    # path( 'languageRecords/', views.language.as_view(),name="languageRecords"),
    path( 'updateLanguageActionRecords', views.UpdateMultiRecordLanguage.as_view()),

    path('currency-list', currency_list, name='currency-list'),
    path( 'updateCurrConversionRecords/<int:pk>/', views.currency.as_view(), name='updateCurrConversionRecords'),
    # path('currency-list-json', views.language.as_view(), name='currency-list-json'),
    # path( 'currency-details/<int:id>/', views.RecordDetailsLanguage.as_view(), name='language-details'),
    # path( 'languageRecords/<int:pk>/', views.language.as_view(),name="languageRecords"),
    # path( 'languageRecords/', views.language.as_view(),name="languageRecords"),
    # path( 'updateCurrencyActionRecords', views.UpdateMultiRecordCurrency.as_view()),

    path('order-list', order_list, name='order-list'),
    path('order-list-json', views.order.as_view(), name='order-list-json'),
    path('order-details/<int:id>/', views.RecordDetailsOrder.as_view()),

    path('vehiclemodel-list', vehiclemodel_list, name='vehiclemodel-list'),
    path('vehiclemodel_list_json', views.vehiclemodel.as_view(), name='vehiclemodel_list_json'),
    path( 'vehiclemodel-details/<int:id>/', views.RecordDetailsVehicleModel.as_view(), name='vehicletype_record_details'),
    path( 'updateVehiclemodelRecords/<int:pk>/', views.vehiclemodel.as_view(),name="updateVehiclemodel"),
    path( 'updateVehiclemodelRecords/', views.vehiclemodel.as_view(),name="updateVehiclemodel"),
    path( 'updateVehicleModelActionRecords', views.UpdateMultiRecordVehicleModel.as_view()),

    path('driver-subscription-list', driver_subscription_list, name='driver-subscription-list'),
    path('driver_subscription_list_json', views.driver_subscription.as_view(), name='driver_subscription_list_json'),
    path( 'driver-subscription-details/<int:id>/', views.RecordDetailsDriverSubscription.as_view(), name='driver-subscription-details'),
    path( 'updateDriverSubscriptionRecords/<int:pk>/', views.driver_subscription.as_view(),name="updateDriverSubscriptionRecords"),
    # path( 'updateDriverSubscriptionRecords/', views.driver_subscription.as_view(),name="updateVehicletype"),
    path( 'updateDriverSubscriptionActionRecords', views.UpdateMultiRecordSubscriptionPlan.as_view()),

    path('promotioncode-list', promotioncode_list, name='promotioncode-list'),
    path('promotioncode_list_json', views.promotioncode.as_view(), name='promotioncode_list_json'),
    path( 'promotioncode-details/<int:id>/', views.RecordDetailsPromotionCode.as_view(), name='promotioncode-details'),
    path( 'updatePromotionCode/<int:pk>/', views.promotioncode.as_view(),name="updatePromotionCode"),
    path( 'updatePromotionCode/', views.promotioncode.as_view(),name="updatePromotionCode"),
    path( 'updatePromotionCodeRecords', views.UpdateMultiRecordPromotionCode.as_view()),

    path('paymentmethod-list', views.paymentmethod_list, name='paymentmethod-list'),
    path('paymentmethod_list_json', views.paymentmethod.as_view(), name='paymentmethod_list_json'),
    path( 'paymentmethod-details/<int:id>/', views.RecordDetailsPaymentMethod.as_view(), name='paymentmethod-details'),
    path( 'updatePaymentMethod/<int:pk>/', views.paymentmethod.as_view(),name="updatePromotionCode"),
    path( 'updatePaymentMethod/', views.paymentmethod.as_view(),name="updatePaymentMethod"),
    path( 'updatePaymentMethodActionRecords', views.UpdateMultiRecordPaymentMethod.as_view()),

    path('drivertrip-list', views.driver_trip_list, name='drivertrip-list'),
    path('drivertrip-list-json', views.drivertrip.as_view(), name='drivertrip-list-json'),
    path('drivertrip-details/<int:id>/', views.RecordDetailsDriverTrip.as_view()),

    path('completedtrip-list', views.completedtrip_list, name='completedtrip-list'),
    path('completedtrip-list-json', views.completedtrip.as_view(), name='completedtrip-list-json'),
    path('completedtrip-details/<int:id>/', views.RecordDetailsCompletedtrip.as_view()),

    path('map_route_list_json/<int:id>/', views.maproute_list.as_view(), name='map_route_list_json'),
    path('map_route_single_coordinate/<int:id>/', views.maproute_single.as_view(), name='map_route_single_coordinate'),

    path('regTimeInterval', views.regTimeInterval.as_view(), name='regTimeInterval'),

    path('getSubscriptionPlanDetails/<int:id>/<int:prev_plan_id>', views.subscription_plan_data.as_view(), name='getSubscriptionPlanDetails'),

    
    path( 'settings', views.siteSettings, name='settings'),
    path( 'save-settings/', views.Settings.as_view(), name='save-settings'),

    path('push-notification-list', views.push_notification_list, name='push-notification-list'),
    path('push_notification_list_json', views.push_notification.as_view(), name='push_notification_list_json'),
    path( 'push-notification-details/<int:id>/', views.RecordDetailsPushNotification.as_view(), name='vehicletype_record_details'),
    path( 'updatePushNotificationRecords/<int:pk>/', views.push_notification.as_view(),name="updatePushNotificationRecords"),
    path( 'updatePushNotificationRecords/', views.push_notification.as_view(),name="updatePushNotificationRecords"),
    path( 'updatePushNotificationActionRecords', views.UpdateMultiRecordPushNotification.as_view()),

    path( 'bulk-push-notification', views.pushNotifications, name='bulk-push-notification'),

    path('review-reason-list', views.review_reason_list, name='review-reason-list'),
    path('review-reason-list-json', views.review_reason.as_view(), name='review-reason-list-json'),
    path( 'review-reason-details/<int:id>/', views.RecordDetailsReviewReason.as_view()),
    path( 'updateReviewReasonRecords/<int:pk>/', views.review_reason.as_view()),
    path( 'updateReviewReasonRecords/', views.review_reason.as_view()),
    path( 'updateReviewReasonActionRecords', views.UpdateMultiRecordReviewReason.as_view()),

    path('subscription-plan-list', views.subscription_plan_list, name='subscription-plan-list'),
    path('subscription-plan-list-json', views.subscription_plan.as_view(), name='subscription-plan-list-json'),
    path( 'subscription-plan-details/<int:id>/', views.RecordDetailsSubscriptionPlan.as_view()),
    path( 'updateSubscriptionPlanRecords/<int:pk>/', views.subscription_plan.as_view()),
    path( 'updateSubscriptionPlanRecords/', views.subscription_plan.as_view()),
    path( 'updateSubscriptionPlanActionRecords', views.UpdateMultiRecordSubscriptionPlan.as_view()),
	path('privacypolicy', views.policyFile, name='policyFile'),
    path( 'order_summary/', views.OngoingBooking.as_view()), 


    path('adminuser-list', views.adminuser_list, name='adminuser-list'),
    path('adminuser_list_json', views.adminuser.as_view(), name='adminuser_list_json'),
    path( 'adminuser-details/<int:id>/', views.RecordDetailsAdminUser.as_view(), name='adminuser-details'),
    path( 'updateAdminUserRecords/<int:pk>/', views.adminuser.as_view(),name="updateAdminUserRecords"),
    path( 'updateAdminUserRecords/', views.adminuser.as_view(),name="updateAdminUserRecords"),
    path( 'updateAdminUserMulRecords', views.UpdateMultiRecordAdminUsers.as_view()),
    path( 'checkUniqueEmail', views.checkUniqueEmail.as_view()),    

    
] 
