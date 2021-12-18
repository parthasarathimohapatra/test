from .models import *
from rest_framework import serializers
from django.contrib.postgres import fields
from django.db.models import F, Q, Count, Min, Sum, Avg, FloatField, ExpressionWrapper
import calendar
import datetime
from django.utils.timezone import is_aware, utc
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
def calculateCurrentRateByLang( conversion_rate,  amount, currentLang ):
    currencyDetailsObj = NdCurrencies.objects.filter(language_type__iexact=currentLang).values('id', 'conversion_rate', 'currency').first()
    currencyConvertedToKhr = float(amount)/float(conversion_rate)
    convertedToRequired = currencyConvertedToKhr * float(currencyDetailsObj['conversion_rate'])
    convertedToRequired = format(float(convertedToRequired), '.2f')
    return {"convertedAmount":convertedToRequired, "currency": currencyDetailsObj['currency'] }


class NdRoleSE(serializers.ModelSerializer):
    class Meta:
        model = NdRoles
        fields = ( 'id', 'role_title' )
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True},
            'is_deleted': {'read_only': True, 'default': False},
        }
class NdRoleCountriesSE(serializers.ModelSerializer):
    class Meta:
        model = NdCountries
        fields = ( 'id', 'country_name', 'country_isd_code', 'country_code')
        extra_kwargs = {
            'is_status': {'read_only': True, 'default': True},
            'is_deleted': {'read_only': True, 'default': False},
        }

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
    class Meta:
        model = NdUsers
        fields = ('id','first_name', 'last_name', "profile_picture")
class NdUsersUniqueUUIDSE(serializers.ModelSerializer):
    class Meta:
        model = NdUsers
        fields = ('id', 'device_uuid')
class NdUsersProfileImageSE(serializers.ModelSerializer):
    class Meta:
        model = NdUsers
        fields = ('id', 'profile_picture')
class NdCountriesSE(serializers.ModelSerializer):
    class Meta:
        model = NdCountries
        fields = ('id', 'country_code', 'country_name', 'country_isd_code')
class NdAllHomeBannerImagesSE(serializers.ModelSerializer):
    class Meta:
        model = NdImage
        fields = ('id', 'is_status', 'image_file', 'title')
class SplashImagesSE(serializers.ModelSerializer):
    class Meta:
        model = NdSplashScreen
        fields = ('id', 'is_status', 'splash_text', 'heading', 'image_file')
class NdSavedLocationsSE(serializers.ModelSerializer):
    user=NdUsersFullNameSE(required=False)
    class Meta:
        model = NdSavedLocations
        fields = ('id', 'location', 'location_name', 'latitude', 'longitude', 'user')
class NdVehicleTypeSE(serializers.ModelSerializer):
    class Meta:
        model = NdVehicleType
        fields = ('id', 'vehicle_type_name', 'max_distance', 'vehicle_logo', 'person_capcity')
class NdCurrenciesDetailsSe(serializers.ModelSerializer):

    class Meta:
        model = NdCurrencies
        fields = ("id",  "currency") 
class OrderDetailsSE(serializers.ModelSerializer):
    driver = NdUsersFullNameSE(required=False)
    supplier = NdUsersFullNameSE(required=False)
    vehicles_type = NdVehicleTypeSE(required=False)
    parcelInformations = serializers.SerializerMethodField()
    vehicle_details = serializers.SerializerMethodField()
    dropping_locations = serializers.SerializerMethodField()
    currency = NdCurrenciesDetailsSe(required=False)
    converted_price = serializers.SerializerMethodField()
    def get_converted_price(self, item):
        currentLang = self.context.get('currentLang')
        old_lang = item.currency.language_type
        currencyConverted = calculateCurrentRateByLang(item.conversion_rate, item.base_price, 'km-KH')
        return currencyConverted
    def get_dropping_locations(self, item):
        dropLocations = NdDropOffLocation.objects.filter(order_id=item).values("id", "latitude", "longitude", "location")
        return dropLocations
    def get_vehicle_details(self, item):
        print(item.driver_id)
        recordDetails = NdDriverDetails.objects.filter(user_id=item.driver_id).values('id', 'vehicle_type_id', 'vehicle_type__vehicle_type_name', 'vehicle_type__vehicle_logo').first()
        # if recordDetails:
        #     if recordDetails['vehicle_type__vehicle_logo']:
        #         recordDetails['vehicle_type__vehicle_logo'] =  static(recordDetails['vehicle_type__vehicle_logo'])
        return recordDetails
    def get_parcelInformations(self, item):
        recordObj = NdParcelInformations.objects.filter(order=item).values('id', 'location', 'parcel_file')
        return recordObj
    class Meta:
        model = NdOrder
        fields = ( 'location', 'distance', 'base_price', 'latitude', 'longitude', 'order_uid', 'base_fare_payment_method_first', 'total_time_taken',
             'booking_time', 'driver', 'supplier', 'vehicles_type', 'parcelInformations', 'vehicle_details', 'dropping_locations', 'base_fare_payment_method_second',
             'total_time_taken', 'booking_status', 'converted_price', 'currency', 'conversion_rate')