from .models import *
from rest_framework import serializers
from django.contrib.postgres import fields
from django.db.models import F, Q, Count, Min, Sum, Avg, FloatField, ExpressionWrapper
import calendar
import datetime
from django.utils.timezone import is_aware, utc
from django.conf import settings
from commonApp.serializers import *
from django.contrib.staticfiles.templatetags.staticfiles import static
from commonApp.views import calculateCurrentRateByLang
def calculateCurrentRateByLang( conversion_rate,  amount, currentLang ):
    currencyDetailsObj = NdCurrencies.objects.filter(language_type__iexact=currentLang).values('id', 'conversion_rate', 'currency').first()
    currencyConvertedToKhr = float(amount)/float(conversion_rate)
    convertedToRequired = currencyConvertedToKhr * float(currencyDetailsObj['conversion_rate'])
    convertedToRequired = format(float(convertedToRequired), '.2f')
    return {"convertedAmount":convertedToRequired, "currency": currencyDetailsObj['currency'] }


class NdStatesSE(serializers.ModelSerializer):
    class Meta:
        model = NdStates
        fields = '__all__'
class NdDriverDetailsSaveSE(serializers.ModelSerializer):
    country=NdRoleCountriesSE(required=False)
    role=NdRoleSE(required=False)
    class Meta:
        model = NdUsers
        fields = ( 'id', 'first_name', 'last_name', 'phone_number', 'email_id', 'gender', 'dob', 
            'password', 'country', 'profile_picture', 'role', 'verification_code' )
class NdUsersLoginSE(serializers.ModelSerializer):
    role = NdRoleSE(required=False)
    country = NdRoleCountriesSE(required=False)
    vehicle_details = serializers.SerializerMethodField()
    def get_vehicle_details(self, item):
        recordDetails = NdDriverDetails.objects.filter(user_id=item).values('id', 'vehicle_type_id', 'vehicle_type__vehicle_type_name', 'vehicle_type__vehicle_logo', 'vehicle_type__top_view_logo').first()
        if recordDetails:
            if recordDetails['vehicle_type__vehicle_logo']:
                recordDetails['vehicle_type__vehicle_logo'] =  static(recordDetails['vehicle_type__vehicle_logo'])
            if recordDetails['vehicle_type__top_view_logo']:
                recordDetails['vehicle_type__top_view_logo'] =  static(recordDetails['vehicle_type__top_view_logo'])
        return recordDetails
    class Meta:
        model = NdUsers
        fields = ('id', 'email_id', 'first_name', 'last_name', 'phone_number',
         'is_status', 'is_deleted',  'role', 'country', 'device_uuid', 'profile_picture', 'device_token', 'is_phone_no_verified', 'vehicle_details')
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True},
            'is_deleted': {'read_only': True, 'default': False},
            'email_id': { 'default': ""},
        }
class NdUsersFullNameSE(serializers.ModelSerializer):
    isd = serializers.SerializerMethodField()
    def get_isd(self, item):
        details = NdCountries.objects.filter(id=item.country_id).values('country_isd_code').first()
        return details['country_isd_code']
    class Meta:
        model = NdUsers
        fields = ('id','first_name', 'last_name', "profile_picture", "phone_number", "isd")

class OrderDetailsSE(serializers.ModelSerializer):
    supplier = NdUsersFullNameSE(required=False)
    dropping_locations = serializers.SerializerMethodField()
    converted_price = serializers.SerializerMethodField()
    def get_converted_price(self, item):
        currentLang = self.context.get('currentLang')
        old_lang = item.currency.language_type
        currencyConverted = calculateCurrentRateByLang(item.conversion_rate, item.base_price, 'km-KH')
        return currencyConverted
    def get_dropping_locations(self, item):
        dropLocations = NdDropOffLocation.objects.filter(order_id=item).order_by('drop_location_type').values("id", "latitude", "longitude", "location")
        return dropLocations
    def get_vehicle_details(self, item):
        recordDetails = NdDriverDetails.objects.filter(user_id=item.driver_id).values('id', 'vehicle_type_id', 'vehicle_type__vehicle_type_name', 'vehicle_type__vehicle_logo').first()
        return recordDetails
    def get_parcelInformations(self, item):
        recordObj = NdParcelInformations.objects.filter(order=item).values('id', 'location', 'parcel_file')
        return recordObj
    class Meta:
        model = NdOrder
        fields = ( 'location',  'latitude', 'longitude', 'order_uid', 'booking_time', 'supplier',  'distance', 'dropping_locations','converted_price')
class NdBookingRequestsSe(serializers.ModelSerializer):
    order = OrderDetailsSE(required=False)
    class Meta:
        model = NdBookingRequests
        fields = ("id", "order", "estimate_time", "order_id", 'date_created')

class NdDropOffLocationSe(serializers.ModelSerializer):
    # parcelInformations = serializers.SerializerMethodField()
    # def get_parcelInformations(self, item):
    #   # print("3333333333333333333", str(item['id']))
    #   recordObj = NdParcelInformations.objects.filter(location=item).values('id', 'parcel_file')
    #   return recordObj
    class Meta:
        model = NdDropOffLocation
        fields = ("id",  "latitude", "longitude", "location", "drop_location_type")
class NdCurrenciesDetailsSe(serializers.ModelSerializer):

    class Meta:
        model = NdCurrencies
        fields = ("id",  "currency") 
class OrderDetailsForHistorySE(serializers.ModelSerializer):
    supplier = NdUsersFullNameSE(required=False)
    dropping_locations = serializers.SerializerMethodField()
    vehicle_details = serializers.SerializerMethodField()
    converted_price = serializers.SerializerMethodField()
    currency = NdCurrenciesDetailsSe(required=False)
    # complete_order_details = serializers.SerializerMethodField()
    # def get_complete_order_details(self, item):
    #   completeDetails = NdOrderCompletionDetails.objects.filter(order_id=item).values('id', 'latitude', 'longitude', 'actual_distance', 'arrival_time', 'location_type')
    #   return completeDetails
    # parcelInformations = serializers.SerializerMethodField()
    def get_converted_price(self, item):
        currentLang = self.context.get('currentLang')
        old_lang = item.currency.language_type
        print(item.currency.language_type)
        currencyConverted = calculateCurrentRateByLang(item.conversion_rate, item.base_price, 'km-KH')
        return currencyConverted

    def get_dropping_locations(self, item):
        dropLocations = NdDropOffLocation.objects.filter(order_id=item).order_by('drop_location_type')
        ndDropOffLocationSe = NdDropOffLocationSe(dropLocations, many=True)
        return ndDropOffLocationSe.data
    def get_vehicle_details(self, item):
        recordDetails = NdDriverDetails.objects.filter(user_id=item.driver_id).values('id', 'vehicle_type_id', 'vehicle_type__vehicle_type_name',
         'vehicle_type__vehicle_logo').first()
        recordDetails['vehicle_type__vehicle_logo'] = static(recordDetails['vehicle_type__vehicle_logo'])
        return recordDetails
    # def get_parcelInformations(self, item):
    #   recordObj = NdParcelInformations.objects.filter(order_id=item).values('id', 'location', 'parcel_file')
    #   return recordObj
    class Meta:
        model = NdOrder
        fields = ( 'id', 'location',  'latitude', 'longitude', 'order_uid', 'booking_time', 'supplier', 
            'dropping_locations', 'booking_status', 'vehicle_details', 'base_price', 'converted_price', 'conversion_rate', 'currency')
class OrderDetailsWithDropSE(serializers.ModelSerializer):
    supplier = NdUsersFullNameSE(required=False)
    dropping_locations = serializers.SerializerMethodField()
    def get_dropping_locations(self, item):
        dropLocations = NdDropOffLocation.objects.filter(order_id=item).order_by('drop_location_type').values("id", "latitude", "longitude", "location")
        return dropLocations
    def get_vehicle_details(self, item):
        recordDetails = NdDriverDetails.objects.filter(user_id=item.driver_id).values('id', 'vehicle_type_id', 'vehicle_type__vehicle_type_name', 'vehicle_type__vehicle_logo').first()
        return recordDetails
    def get_parcelInformations(self, item):
        recordObj = NdParcelInformations.objects.filter(order=item).values('id', 'location', 'parcel_file')
        return recordObj
    class Meta:
        model = NdOrder
        fields = ( 'location',  'latitude', 'longitude', 'order_uid', 'booking_time', 'base_price', 'distance', 'supplier', 'dropping_locations')
# class NdBookingRequestsSe(serializers.ModelSerializer):
#     order = OrderDetailsWithDropSE(required=False)
#     class Meta:
#         model = NdBookingRequests
#         fields = ("id", "order", "estimate_time", "order_id", 'date_created')

class CurrentOrderDetailsSE(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()
    supplier = NdUsersFullNameSE(required=False)
    dropping_locations = serializers.SerializerMethodField()
    last_driver_position = serializers.SerializerMethodField()
    arrival_time = serializers.SerializerMethodField()
    def get_arrival_time(self, item):
        completedDetails = NdOrderCompletionDetails.objects.filter(order_id=item, location_type=0)
        arrival_time = ""
        if completedDetails.exists():
            completedDetailsObj = completedDetails.values('arrival_time').first()
            arrival_time = completedDetailsObj['arrival_time']
        return arrival_time
    def get_last_driver_position(self, item):
        ndCurrentDriverLocationObj = NdCurrentDriverLocation.objects.filter(order_id=item, 
            driver_id=item.driver_id).order_by("-date_created").values('id', 'latitude', 'longitude',
            'real_distance', 'date_created')
        if ndCurrentDriverLocationObj.exists():
            ndCurrentDriverLocationObj = ndCurrentDriverLocationObj.first()
            return ndCurrentDriverLocationObj
        else:
            return dict()
    def get_position(self, item):
        OrderCompletionDetails = NdOrderCompletionDetails.objects.filter(order_id=item)
        dropOff = NdDropOffLocation.objects.filter(order_id=item)
        countDropOff = dropOff.count()
        print("rrrrrrrrrrr", str(countDropOff))
        print("tttttttttttt", str(OrderCompletionDetails.count()))
        if OrderCompletionDetails.count() == 0:
            aheadLocation = 1
        elif OrderCompletionDetails.count() == 1:
            aheadLocation = 2
        elif OrderCompletionDetails.count() == 2 and countDropOff == 1:
            aheadLocation = 2
        elif OrderCompletionDetails.count() == 2 and countDropOff == 2:
            aheadLocation = 3
        else:
            aheadLocation = 4
        return aheadLocation
    def get_dropping_locations(self, item):
        dropLocations = NdDropOffLocation.objects.filter(order_id=item).order_by('drop_location_type').values("id", "latitude", "longitude", "location")
        return dropLocations
    def get_vehicle_details(self, item):
        recordDetails = NdDriverDetails.objects.filter(user_id=item.driver_id).values('id', 'vehicle_type_id', 'vehicle_type__vehicle_type_name', 'vehicle_type__vehicle_logo').first()
        return recordDetails
    def get_parcelInformations(self, item):
        recordObj = NdParcelInformations.objects.filter(order=item).values('id', 'location', 'parcel_file')
        return recordObj
    class Meta:
        model = NdOrder
        fields = ( 'id', 'location',  'latitude', 'longitude', 'order_uid', 'booking_time', 'supplier', 'dropping_locations', 'position', 'last_driver_position', 
            'arrival_time')

class OngoingOrderDetailsSE(serializers.ModelSerializer):
    arrival_time = serializers.SerializerMethodField()
    dropping_locations = serializers.SerializerMethodField()
    support_number = serializers.SerializerMethodField()
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
        fields = ('id', 'location', 'order_uid', 'booking_time', 'dropping_locations', "contact_name", "contact_number", "arrival_time", "support_number" )