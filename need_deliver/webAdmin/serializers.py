from .models import *
from driver.models import *
from rest_framework import serializers, generics
# from drf_extra_fields.fields import Base64ImageField
# from django.contrib.postgres import fields
from django.db.models import F, Q, Count, Min, Sum, Avg, FloatField, ExpressionWrapper
import datetime
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
# from rest_framework import generics
def shaEncode(str):
    return hashlib.sha224(str.encode('utf-8')).hexdigest()
class NdRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NdRoles
        fields = ( 'id', 'role_title' )
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True},
            'is_deleted': {'read_only': True, 'default': False},
        }
class NdCountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NdCountries
        fields = ('id', 'country_code', 'country_name','country_isd_code')
        # extra_kwargs = {
        #     'is_status': {'read_only': True, 'default': True},
        #     'is_deleted': {'read_only': True, 'default': False},
        # }
class NdStatesSerializer(serializers.ModelSerializer):
    country = NdCountriesSerializer(required=False)
    class Meta:
        model = NdStates
        fields = ('id', 'state_name', 'country')
        # extra_kwargs = {
        #     'is_status': {'read_only': True, 'default': True},
        #     'is_deleted': {'read_only': True, 'default': False},
        # }

 
class NdCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = NdCurrencies
        fields = ('id', 'currency_name', 'default_currency', 'conversion_rate','currency', 'is_status')

   
class NdSubscriptionPlanSerializer(serializers.ModelSerializer):
    ndcurrency = NdCurrencySerializer(required=False)
    class Meta:
        model = NdSubscriptionPlan
        fields = ('id', 'plan_name','price','currency','ndcurrency', 'is_status')


class NdPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = NdPaymentMethod
        fields = ('id', 'name','payment_logo', 'is_status')

class NdUsersSerializer(serializers.ModelSerializer):
    role = NdRoleSerializer(required=False)
    class Meta:
        model = NdUsers
        fields = ('id', 'first_name', 'last_name','email_id', 'phone_number', 'profile_picture', 'role', 'device_token')

class NdUsersCreateSerializer(serializers.ModelSerializer):
    # password =shaEncode()
    role = NdRoleSerializer(required=False)
    country = NdCountriesSerializer(required=False)
    state = NdStatesSerializer(required=False)
    class Meta:
        model = NdUsers
        fields = ('id', 'first_name', 'last_name' ,'email_id', 'phone_number', 'profile_picture', 'role', 'is_status','country','state','city','zipcode','description','dob','gender','password','is_phone_no_verified', 'device_token')
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True},
            'is_phone_no_verified':{ 'read_only': True, 'default': True}
        }

class NdUsersCreateWithoutDPSerializer(serializers.ModelSerializer):
    # password =shaEncode()
    role = NdRoleSerializer(required=False)
    country = NdCountriesSerializer(required=False)
    state = NdStatesSerializer(required=False)
    # language = FlntLanguagesSerializer(required=False)
    class Meta:
        model = NdUsers
        fields = ('id', 'first_name', 'last_name' ,'email_id', 'phone_number',  'role', 'is_status','country','state','city','zipcode','description','dob','gender', 'password','is_phone_no_verified')
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True}
        }

class NdUsersDriverSerializer(serializers.ModelSerializer):
    # password =shaEncode()
    role = NdRoleSerializer(required=False)
    country = NdCountriesSerializer(required=False)
    state = NdStatesSerializer(required=False)
    # language = FlntLanguagesSerializer(required=False)
    class Meta:
        model = NdUsers
        fields = ('id', 'first_name', 'last_name' ,'email_id', 'phone_number', 'profile_picture', 'role', 'is_status','country','state','city','zipcode','description','dob','gender','password')
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True},
           
            'is_phone_validate': {'read_only': True, 'default': False},
            'is_email_validate': {'read_only': True, 'default': False},
        }


 
class NdVehicleTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NdVehicleType
        fields = ('id', 'vehicle_type_name','base_fare', 'khr','person_capcity','vehicle_logo', 'top_view_logo', 'is_status')
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True},
        }

class NdVehicleTypeTopViewLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NdVehicleType
        fields = ('id', 'top_view_logo')

class NdVehicleTypeLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NdVehicleType
        fields = ('id', 'vehicle_logo')

class NdPromotionCodeSerializer(serializers.ModelSerializer,):
    
    class Meta:
        model = NdPromotions
        fields = ('id', 'promotion_code','discount', 'start_date','end_date', 'is_status')
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True},
        }

class NdVehiclModelSerializer(serializers.ModelSerializer,):
    
    vehicle_type = NdVehicleTypeSerializer(required=False)
    class Meta:
        model = NdVehicleModel
        fields = ('id', 'vehicle_type', 'model_name' , 'is_status')
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True},
        }

class NdVehicleDetailsSerializer(serializers.ModelSerializer,):
    driver_vehicle_details = NdUsersSerializer(required=False)
    vehicle_model = NdVehiclModelSerializer(required=False)
    vehicle_type = NdVehicleTypeSerializer(required=False)
    # language = FlntLanguagesSerializer(required=False)
    class Meta:
        model = NdVehicleDetails
        fields = ('id', 'image_file', 'vehicle_type', 'plate_number' ,'registration_expiry_date', 'insurance_expiry_date', 'driver_vehicle_details','city','vehicle_model','year','wheel_chair_support','booster_seat_support')
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True},
        }

class NdDriverDetailsSerializer(serializers.ModelSerializer):
    user = NdUsersSerializer(required=False)
    vehicle_type = NdVehicleTypeSerializer(required=False)
    subscription_plan = NdSubscriptionPlanSerializer(required=False)
    account_balance_currency = NdCurrencySerializer(required=False)
    class Meta:
        model = NdDriverDetails
        fields = ('id','user',  'driving_licence_expiry_date' ,'vehicle_type', 'subscription_plan','account_balance','account_balance_currency', 'is_status')
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True}
        }

class NdObjectTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NdObjectTypeModel
        fields = ('id', 'object_name', 'is_status')
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True}
        }


class NdAttachmentsSerializer(serializers.ModelSerializer):
    object_type = NdObjectTypeSerializer(required=False)
    user = NdUsersSerializer(required=False)
    class Meta:
        model = NdAttachments
        fields = ('id', 'object_type','user', 'attached_file', 'record_number', 'is_status')
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True},
        }



class NdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NdImage
        fields = ('id', 'title', 'image_file','applied_to', 'is_status')
        
class NdSplashScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = NdSplashScreen
        fields = ('id', 'heading', 'image_file', 'splash_text', 'is_status')

class NdCancellationReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = NdCancellationReason
        fields = ('id', 'reason', 'is_status')

# class NdOrderSerializer(serializers.ModelSerializer):
#     supplier = NdUsersSerializer(required=False)
#     driver = NdUsersSerializer(required=False)
#     class Meta:
#         model = NdOrder
#         fields = ('id', 'supplier', 'driver', 'contact_name', 'contact_number', 'is_status','delivery_time')

class NdOrderSerializer(serializers.ModelSerializer):
    supplier = NdUsersSerializer(required=False)
    driver = NdUsersSerializer(required=False)
    vehicles_type = NdVehicleTypeSerializer(required=False)
    class Meta:
        model = NdOrder
        fields = ('id','booking_time','delivery_time', 'order_uid','contact_name','contact_number','note_to_driver','base_price', 'supplier', 'driver', 'location', 'vehicles_type','booking_status', 'is_status')
      



class NdDropOffLocationSerializer(serializers.ModelSerializer):
    order = NdOrderSerializer(required=False)
    
    class Meta:
        model = NdDropOffLocation
        fields = ('id', 'location', 'latitude', 'longitude', 'item_name', 'order', 'contact_name', 'contact_number', 'note_to_driver','cash_collection','is_status')

class NdParcelInformationsSerializer(serializers.ModelSerializer):
    order = NdOrderSerializer(required=False)
    location = NdDropOffLocationSerializer(required=False)
    class Meta:
        model = NdParcelInformations
        fields = ('id', 'order', 'location',  'parcel_file', 'is_status')


class NdPickupRequestSerializer(serializers.ModelSerializer):
    supplier = NdUsersSerializer(required=False)
    driver = NdUsersSerializer(required=False)
    class Meta:
        model = NdOrder
        fields = ('id', 'supplier', 'driver', 'contact_name', 'contact_number','location', 'is_status')


class NdLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NdLanguages
        fields = ('id', 'lang_name', 'image_file', 'is_status')


class NdDriverTripSerializer(serializers.ModelSerializer):
    supplier = NdUsersSerializer(required=False)
    driver = NdUsersSerializer(required=False)
    class Meta:
        model = NdOrder
        fields = ('id', 'supplier', 'driver', 'contact_name', 'contact_number', 'order_uid',
            'booking_status','booking_time','delivery_time', 'is_status', 'distance', 'base_price', 
            'total_time_taken')     

class NdUsersProfilePicture(serializers.ModelSerializer):
    class Meta:
        model = NdUsers
        fields = ('id', 'profile_picture')

class NdVehicleDetailsWithoutImageSerializer(serializers.ModelSerializer,):
    driver_vehicle_details = NdUsersSerializer(required=False)
    vehicle_model = NdVehiclModelSerializer(required=False)
    vehicle_type = NdVehicleTypeSerializer(required=False)
    # language = FlntLanguagesSerializer(required=False)
    class Meta:
        model = NdVehicleDetails
        fields = ('id', 'vehicle_type', 'plate_number' ,'registration_expiry_date', 'insurance_expiry_date', 'driver_vehicle_details','city','vehicle_model','year','wheel_chair_support','booster_seat_support')
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True},
        }

class NdSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NdSettings
        fields = ('id', 'field_name', 'field_val', 'is_status')     

class NdAppliedCouponSerializer(serializers.ModelSerializer):
    supplier = NdUsersSerializer(required=False)
    coupon = NdPromotionCodeSerializer(required=False)
    class Meta:
        model = NdAppliedCoupons
        fields = ('id', 'supplier', 'coupon', 'is_status')     
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True},
        }
        
class NdCurrentDriverLocationSerializer(serializers.ModelSerializer):
    driver = NdUsersSerializer(required=False)
    order = NdOrderSerializer(required=False)
    class Meta:
        model = NdCurrentDriverLocation
        fields = ('id', 'order', 'driver','latitude','longitude','real_distance')    

class NdLatLngDriverLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NdCurrentDriverLocation
        fields = ('id', 'latitude','longitude')   

class NdOrderCompletionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NdOrderCompletionDetails
        fields = ('id', 'latitude','longitude','arrival_time') 
        
class NdAdminPushNotificationsSerializer(serializers.ModelSerializer):
    # password =shaEncode()
    role = NdRoleSerializer(required=False)
    class Meta:
        model = NdAdminPushNotifications
        fields = ('id', 'message_title', 'message_body', 'role', 'is_status')
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True}
        }

class NdRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NdRoles
        fields = ('id', 'role_title', 'is_status')
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True}
        }


class NdReviewTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NdReviewTypes
        fields = ('id', 'review_reason', 'is_status')

class NdBookingRequestsSerializer(serializers.ModelSerializer):
    driver = NdUsersSerializer(required=False)
    order = NdOrderSerializer(required=False)
    class Meta:
        model = NdBookingRequests
        fields = ('id', 'order', 'driver','estimate_time','date_created','is_deleted','is_booked')

class NdCancelBookingByDriverSerializer(serializers.ModelSerializer):
    driver = NdUsersSerializer(required=False)
    
    class Meta:
        model = NdBookingRequests
        fields = ( 'driver')
class NdDriverObjSE(serializers.ModelSerializer):
    over_all_rating = serializers.SerializerMethodField()
    vehicle_details = serializers.SerializerMethodField()
    vehicle_type_obj = serializers.SerializerMethodField()
    isd = serializers.SerializerMethodField()
    def get_isd(self, item):
        recordObj = NdCountries.objects.filter(id=item.country_id).values('id', 'country_isd_code').first()
        return recordObj['country_isd_code']
    def get_vehicle_type_obj(self, item):
        recordObj = NdDriverDetails.objects.filter(user=item).values('id', 'vehicle_type__vehicle_type_name', 'vehicle_type__vehicle_type_name_com').first()
        lang = self.context.get('lang')
        if lang != 'en':
            recordObj['vehicle_type__vehicle_type_name'] = recordObj['vehicle_type__vehicle_type_name_com']
        return recordObj
    def get_vehicle_details(self, item):
        recordObj = NdVehicleDetails.objects.filter(user=item).values('id', 'plate_number').first()
        return recordObj
    def get_over_all_rating(self, item):
        recordDetails = NdUsersObjects.objects.filter(user=item)
        if recordDetails.count()>0:
            recordDetailsObj = recordDetails.values('over_all_rating').first()
            if recordDetailsObj['over_all_rating']>0:
                return recordDetailsObj['over_all_rating']
            else:
                return 0.0
        return 0.0
    class Meta:
        model = NdUsers
        fields = ('id','first_name', 'last_name', "phone_number", "profile_picture","over_all_rating", "vehicle_type_obj", "country_id", "vehicle_details", "isd") 
      
class NdOrderForCurrentBookingSe(serializers.ModelSerializer):
    driver = NdDriverObjSE(required=False)
    timing = serializers.SerializerMethodField()
    dropping_locations = serializers.SerializerMethodField()
    arrived_status = serializers.SerializerMethodField()
    def get_arrived_status(self, item):
        arrivalStatus = NdOrderCompletionDetails.objects.filter(order_id=item,
            location_type=0)
        if arrivalStatus.exists():
            return True
        else:
            return False
    def get_dropping_locations(self, item):
        dropLocations = NdDropOffLocation.objects.filter(order_id=item).values("id", "latitude", "longitude", "location")
        return dropLocations
    def get_timing(self, item):
       recordDetails = NdBookingRequests.objects.filter(order_id=item, driver_id=item.driver_id, is_deleted=True).values("id", "estimate_time", "date_created").first()
       return recordDetails
    class Meta:
        model = NdOrder
        fields = ('id','order_uid', 'latitude', 'longitude', 'location', 'driver', 'timing', 'dropping_locations', 'arrived_status')
class NdAdminUsersCreateSerializer(serializers.ModelSerializer):
    # password =shaEncode()
    role = NdRoleSerializer(required=False)
    
    class Meta:
        model = NdUsers
        fields = ('id', 'first_name', 'last_name' ,'email_id', 'phone_number','role', 'is_status','password')
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True}
        }

class OngoingOrderDetailsSE(serializers.ModelSerializer):
    driver_details = serializers.SerializerMethodField()
    supplier_details = serializers.SerializerMethodField()
    arrival_time = serializers.SerializerMethodField()
    dropping_locations = serializers.SerializerMethodField()
    support_number = serializers.SerializerMethodField()
    def get_driver_details(self, item):
        details = NdUsers.objects.filter(id=item.driver_id).values('profile_picture', 'id', 'first_name', 'last_name').first()
        details['profile_picture'] = static(details['profile_picture'])
        return details
    def get_supplier_details(self, item):
        details = NdUsers.objects.filter(id=item.supplier_id).values('profile_picture', 'id', 'first_name', 'last_name').first()
        details['profile_picture'] = static(details['profile_picture'])
        return details
    def get_support_number(self, item):
        support_num = NdSettings.objects.filter(field_name="support_number", is_status=True, is_deleted=False).values('field_val').first()
        return support_num['field_val']
    # drop_distance = 
    def get_arrival_time(self, item):
        completedDetails = NdOrderCompletionDetails.objects.filter(order_id=item, location_type=0)
        arrival_time = ""
        if completedDetails.exists():
            completedDetailsObj = completedDetails.values('arrival_time').first()
            arrival_time = completedDetailsObj['arrival_time']
        return arrival_time

    def get_dropping_locations(self, item):
        dropLocations = NdDropOffLocation.objects.filter(order_id=item).order_by('drop_location_type').values("id", "location", "contact_name", "contact_number",
            "item_name", 'note_to_driver', 'drop_location_type', 'distance')
        return dropLocations
    def get_vehicle_details(self, item):
        recordDetails = NdDriverDetails.objects.filter(user_id=item.driver_id).values('id', 'vehicle_type_id', 'vehicle_type__vehicle_type_name', 'vehicle_type__vehicle_logo').first()
        return recordDetails
    def get_parcelInformations(self, item):
        recordObj = NdParcelInformations.objects.filter(order=item).values('id', 'location', 'parcel_file')
        return recordObj
    class Meta:
        model = NdOrder
        fields = ('id', 'location', 'order_uid', 'booking_time', 'dropping_locations', "contact_name", "contact_number", "arrival_time", "support_number", 'driver_details', 'supplier_details' )