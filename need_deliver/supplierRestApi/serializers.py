from .models import *
from rest_framework import serializers
from django.contrib.postgres import fields
from django.db.models import F, Q, Count, Min, Sum, Avg, FloatField, ExpressionWrapper
import calendar
import datetime
from django.utils.timezone import is_aware, utc
from django.conf import settings
from commonApp.serializers import *
from commonApp.views import calculateCurrentRateByLang
from django.contrib.staticfiles.templatetags.staticfiles import static
class NdOrderProcessingDataSE(serializers.ModelSerializer):
	class Meta:
		model = NdOrder
		fields = '__all__'

class NdDropOffLocationSE(serializers.ModelSerializer):
	class Meta:
		model = NdDropOffLocation
		fields = '__all__'   

class NdParcelInformationsSE(serializers.ModelSerializer):
	class Meta:
		model = NdParcelInformations
		fields = '__all__'      
class NdVehicleTypeSE(serializers.ModelSerializer):
	vehicle_type_name = serializers.SerializerMethodField()
	def get_vehicle_type_name(self, item):
		lang = self.context.get('lang')
		print(lang)
		if lang != 'en':
			return item.vehicle_type_name_com
		else:
			return item.vehicle_type_name

	class Meta:
		model = NdVehicleType
		fields = ('id','vehicle_type_name', 'vehicle_type_name_com', 'max_distance', 'vehicle_logo', 'base_fare', 'person_capcity')

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
	  
class NdOrderDriverDetailsSe(serializers.ModelSerializer):
	driver = NdDriverObjSE(required=False)
	timing = serializers.SerializerMethodField()
	dropping_locations = serializers.SerializerMethodField()
	def get_dropping_locations(self, item):
		dropLocations = NdDropOffLocation.objects.filter(order_id=item).values("id", "latitude", "longitude")
		return dropLocations
	def get_timing(self, item):
	   recordDetails = NdBookingRequests.objects.filter(order_id=item, driver_id=item.driver_id, is_deleted=True).values("id", "estimate_time", "date_created").first()
	   return recordDetails
	class Meta:
		model = NdOrder
		fields = ('id','order_uid', 'latitude', 'longitude', 'location', 'driver', 'timing', 'dropping_locations')

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
class NdDropOffLocationSe(serializers.ModelSerializer):

	class Meta:
		model = NdDropOffLocation
		fields = ("id",  "latitude", "longitude", "location", "drop_location_type")  
class NdCurrenciesDetailsSe(serializers.ModelSerializer):

	class Meta:
		model = NdCurrencies
		fields = ("id",  "currency")  
class OrderDetailsForHistorySE(serializers.ModelSerializer):
	# supplier = NdUsersFullNameSE(required=False)
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

	class Meta:
		model = NdOrder
		fields = ( 'id', 'location',  'latitude', 'longitude', 'order_uid', 'booking_time', 'total_time_taken', 'distance', 'conversion_rate', 'currency',
			'dropping_locations', 'booking_status', 'vehicle_details', 'base_price', 'cash_collection_method_first', 'cash_collection_method_second', 'converted_price')