from django.shortcuts import render
from .serializers import *
from .message import *
from django.contrib.postgres import fields
from django.db.models import F, Q, Count, Min, Sum, Avg, FloatField,\
ExpressionWrapper
from rest_framework.views import APIView
import base64
from rest_framework.response import Response
from django.utils.crypto import get_random_string
import uuid
import boto3
import os.path
from django.conf import settings
from geopy.distance import vincenty
from rest_framework.parsers import MultiPartParser
from commonApp.views import fieldEmptyCheck, get_latest_device_token_by_userid,\
sendGenericMessage, generateUID,get_latest_device_uuid_by_userid, sanitize, current_date_time,\
pushNotificationFCM, update_over_all_rating, calculationCurrencyConversion
import json
from django.db import  transaction, connection
cursor = connection.cursor()
from math import radians, cos, sin, asin, sqrt
from operator import itemgetter
import googlemaps
gmaps = googlemaps.Client(key='AIzaSyDOZCiwPSXUm58TOjViGXwbsfKYkP6t0jw')
import math
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def distanceBtwTwoLocationGoogle( originLatLong, destinationLatLong ):
	try:
		now = datetime.now()
		directions_result = gmaps.directions(originLatLong, destinationLatLong, mode="driving", avoid="ferries")
		totalDistance = directions_result[0]['legs'][0]['distance']['value']
		estimatedTime = directions_result[0]['legs'][0]['duration']['value']
		return {'status':True, "totalDistance":totalDistance, "estimatedTime":estimatedTime}
	except Exception as e:
		return False
#-------------------------------------------------------------- Location And Costing Calculation  --------------------------------------------------------------------# 

class DistanceCalculation(APIView):

	def post(self, request):
		lang = request.data['langC']
		try:
			loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
			 request.data.get('session_unique_uuid'))
			if not loggedInStatus:
				return Response({"status":False, "msg":GenericMsgMod.Msg(lang, 'session_out'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('current_lat_long')): 
				return Response({"status":False, "msg":DistanceAndCostingCalculationMsgMod.Msg(lang, 'current_lat_long'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('drop_location_lat_long1')): 
				return Response({"status":False, "msg": DistanceAndCostingCalculationMsgMod.Msg(lang, 'drop_location_lat_long1'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			else:
				distanceAndDurationFirstDrop = distanceBtwTwoLocationGoogle(request.data.get('current_lat_long'), request.data.get('drop_location_lat_long1'))  
				if distanceAndDurationFirstDrop:
					totalTime = distanceAndDurationFirstDrop['estimatedTime']
					totalDistance = distanceAndDurationFirstDrop['totalDistance']
					if fieldEmptyCheck(request.data.get('drop_location_lat_long2')): 
						distanceAndDurationSecondDrop = distanceBtwTwoLocationGoogle(request.data.get('drop_location_lat_long1'),  request.data.get('drop_location_lat_long2'))  
						if distanceAndDurationSecondDrop:
							totalDistance = float(totalDistance) + float(distanceAndDurationSecondDrop['totalDistance'])
							totalTime = int(totalTime) + int(distanceAndDurationSecondDrop['estimatedTime'])
					return Response({'status':True, "data":dict(), "total_distance":totalDistance, "total_time": totalTime, "msg":DistanceAndCostingCalculationMsgMod.Msg(lang, 'distance_calculated'), 'loggedInStatus':True})
				else:
					return Response({'status':False,  'data':dict(), 'msg':DistanceAndCostingCalculationMsgMod.Msg(lang, 'route_not_found'), 'loggedInStatus':True})
		except Exception as e:
			return Response({'status':False,  'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'error-msg'), 'loggedInStatus':True})
class CostCalculation(APIView):
	def post(self, request):
		lang = request.data['langC']
		try:
			loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
			 request.data.get('session_unique_uuid'))
			if not loggedInStatus:
				return Response({"status":False, "msg":GenericMsgMod.Msg(lang, 'session_out'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('vehicle_type')): 
				return Response({"status":False, "msg":CostCalculationMsgMod.Msg(lang, 'vehicle_type'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('distance')): 
				return Response({"status":False, "msg":CostCalculationMsgMod.Msg(lang, 'distance'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			else:
				vahicleTypeDetailsObj = NdVehicleType.objects.filter(id=int(request.data.get('vehicle_type'))).values('base_fare', 'khr')
				if vahicleTypeDetailsObj.count()>0:
					vahicleTypeDetails = vahicleTypeDetailsObj.first()
					totalDistance = request.data.get('distance')
					totalDistance = totalDistance.replace(",", '.', 1)
					# print("+++++++++++++++", totalDistance)
					totalDistance = float(totalDistance) 
					if not fieldEmptyCheck(vahicleTypeDetails['khr']) or not fieldEmptyCheck(vahicleTypeDetails['base_fare']):
						return Response({'status':False,  'data':dist(), 'msg':CostCalculationMsgMod.Msg(lang, 'base_price'), 'loggedInStatus':True})
					if float(totalDistance) > 1:
						print("base",vahicleTypeDetails['khr'])
						restFare = float(vahicleTypeDetails['khr']) *(float(totalDistance)-1)
						totalCharge  = float(vahicleTypeDetails['base_fare']) + restFare
					else:
						print(str(vahicleTypeDetails['base_fare']) , "rrrrrrrrr" + str(float(totalDistance)))
						# totalCharge  = float(vahicleTypeDetails['base_fare']) *float(totalDistance)
						totalCharge  = float(vahicleTypeDetails['base_fare']) 
					#print(float(vahicleTypeDetails['khr']) )
					# totalCharge = format(totalCharge, '.2f')
					# totalCharge = format(totalCharge, '.2f')
					discountData = NdSettings.objects.filter(field_name="discount", is_status=True, is_deleted=False).values('field_val')
					discountAmt = 0
					isDiscoundApplied = False

					if discountData.exists():
						discountDataObj = discountData.first()
						if discountDataObj['field_val'] !="" or discountDataObj['field_val']:
							if float(discountDataObj['field_val']) >0  :
								isDiscoundApplied = True
								discountAmt = discountDataObj['field_val']
								percentage = totalCharge * float(discountDataObj['field_val'])/100
								#print("dddddddddddd", percentage)

								totalCharge = totalCharge - percentage
								#print("dddddddddddd", totalCharge)
				#	print(totalCharge)	
					# if totalCharge<1:
					# 	totalCharge = 0.1
					langReq = 'km-KH'
					convertedRateObj = calculationCurrencyConversion(totalCharge, langReq)
					totalCharge = format(totalCharge, '.2f')
					# print(totalCharge)
					return Response({'status':True,  'data':dict(), 'totalCharge':totalCharge, 'msg':CostCalculationMsgMod.Msg(lang, 'cost_calculated'),
					 'isDiscoundApplied':isDiscoundApplied, "cost_discount_applied":discountAmt, "conversion_rate": convertedRateObj['conversion_rate'], "currency": convertedRateObj['currency'],
					 "currency_id": convertedRateObj['currency_id'], 'loggedInStatus':True})
				else:
					return Response({'status':False,  'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'error-msg'), 'loggedInStatus':True})
		except Exception as e:
			return Response({'status':False,  'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'error-msg'), 'loggedInStatus':True})
#-------------------------------------------------------------- Order Processing --------------------------------------------------------------------# 
class OrderProcessing(APIView):
	def random_order_uid(self, request):
		random_code = get_random_string(length=7, allowed_chars='123456789')
		random_code_with_prefix = settings.ORDER_PREFIX + random_code
		randomKeycheck = NdOrder.objects.filter(order_uid=random_code_with_prefix, is_deleted=False).count()
		if randomKeycheck >0 :
			self.random_order_uid(request)
		else:
			return random_code_with_prefix
	def merge_two_dicts(self, x, y):
		z = x.copy()
		z.update(y)
		return z
	def pick_up_data_manipulate(self, request, order_uid):
		
		lang = request.data['langC']
		pick_up_lat_long_obj = json.loads(request.data.get('pick_up_lat_long'))
		for key, value in pick_up_lat_long_obj.items():
			if not fieldEmptyCheck(value):
				return {"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'pick_up_'+ key),
				 "data":dict(), 'loggedInStatus':True}

		pick_up_data_obj = json.loads(request.data.get('pick_up_data'))
		# for key, value in pick_up_data_obj.items():
		# 	if not fieldEmptyCheck(value):
		# 		return {"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'pick_up_'+ key),
		# 		 "data":dict(), 'loggedInStatus':True}


		margedDict = self.merge_two_dicts(pick_up_lat_long_obj, pick_up_data_obj)
		margedDict['distance'] = format(float(request.data.get('distance')),'.2f')
		margedDict['conversion_rate'] = float(request.data.get('conversion_rate'))
		margedDict['base_price'] = format(float(request.data.get('base_price')),'.2f')
		if float(request.data.get('cost_discount_applied'))>0:
			margedDict['cost_discount_applied'] = float(request.data.get('cost_discount_applied'))
		if float(request.data.get('cash_on_hand_discount'))>0:
			margedDict['cash_on_hand_discount'] = float(request.data.get('cash_on_hand_discount'))
		

		margedDict['order_uid'] = order_uid
		if fieldEmptyCheck(request.data.get('base_fare_payment_method_first')):
			margedDict['base_fare_payment_method_first'] = int(request.data.get('base_fare_payment_method_first'))
		if fieldEmptyCheck(request.data.get('base_fare_payment_method_second')):
			margedDict['base_fare_payment_method_second'] = int(request.data.get('base_fare_payment_method_second'))
		
		if fieldEmptyCheck(request.data.get('cash_collection_method_first')):
			margedDict['cash_collection_method_first'] = int(request.data.get('cash_collection_method_first'))
		if fieldEmptyCheck(request.data.get('cash_collection_method_second')):
			margedDict['cash_collection_method_second'] = int(request.data.get('cash_collection_method_second'))
		
		margedDict['cash_collection_first_currency'] = str(request.data.get('cash_collection_first_currency'))	
		margedDict['cash_collection_second_currency'] = str(request.data.get('cash_collection_second_currency'))	
		# if fieldEmptyCheck(request.data.get('cash_collection_method')):
		# 	margedDict['cash_collection_method'] = int(request.data.get('cash_collection_method'))
		ndOrderObj = NdOrder(supplier_id=int(request.data.get('supplier_id')), currency_id=int(request.data.get('currency_id')))
		if fieldEmptyCheck(request.data.get('coupon_id')):
			ndOrderObj  = NdOrder(coupon_id=int(request.data.get('coupon_id')), currency_id=int(request.data.get('currency_id')), supplier_id=int(request.data.get('supplier_id')))
		ndOrderProcessingDataSE = NdOrderProcessingDataSE( ndOrderObj, data=margedDict )
		lastOrderId = None
		if ndOrderProcessingDataSE.is_valid():
			updatededData = ndOrderProcessingDataSE.save()
			lastOrderId = updatededData.id
		else:
			return {"status":False, "msg": GenericMsgMod.Msg(lang, 'error-msg'),
				 "data":dict(), 'loggedInStatus':True}  
		return {"status":True, 'lastOrderId':lastOrderId}
	def first_drop_location_manipulate(self, request, order_id):
		pick_up_lat_long_obj = json.loads(request.data.get('pick_up_lat_long'))

		lang = request.data['langC']
		firstDropOffLatLong = json.loads(request.data.get('first_drop_off_lat_long'))
		for key, value in firstDropOffLatLong.items():
			if not fieldEmptyCheck(value):
				return {"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'first_drop_off_'+ key),
				 "data":dict(), 'loggedInStatus':True}     
		drop_off_data_data_obj1 = json.loads(request.data.get('drop_off_data1'))
		pickUplatLong = '"'+str(pick_up_lat_long_obj['latitude'])+', '+ str(pick_up_lat_long_obj['longitude'])+'"'
		firstLatLong = '"'+str(firstDropOffLatLong['latitude'])+', '+ str(firstDropOffLatLong['longitude'])+'"'
		print(firstLatLong)
		# for key, value in drop_off_data_data_obj1.items():
		# 	if not fieldEmptyCheck(value):
		# 		return {"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'first_drop_off_'+ key),
		# 		 "data":dict(), 'loggedInStatus':True}   

		margeDataWithFirstDrop = self.merge_two_dicts(firstDropOffLatLong, drop_off_data_data_obj1)

		margeDataWithFirstDrop['drop_location_type'] = 1
		margeDataWithFirstDrop['item_name'] = request.data.get('first_location_item_name')



		distanceAndDurationFirstDrop = distanceBtwTwoLocationGoogle(pickUplatLong, firstLatLong)  
		if distanceAndDurationFirstDrop:
			firstDropDistance = float(distanceAndDurationFirstDrop['totalDistance'])/1000
			firstDropDistance = format(firstDropDistance, '.2f')
			margeDataWithFirstDrop['distance'] = firstDropDistance

		if fieldEmptyCheck(request.data.get('cash_collection_location_one')):
			margeDataWithFirstDrop['cash_collection'] = request.data.get('cash_collection_location_one')
		ndDropOffLocationObj = NdDropOffLocation(order_id=order_id)
		firstDropInsertId = None
		secondDropInsertId = None

		ndOrderProcessingDataSE = NdDropOffLocationSE(ndDropOffLocationObj, margeDataWithFirstDrop)
		if ndOrderProcessingDataSE.is_valid():
			updatededData = ndOrderProcessingDataSE.save()
			firstDropInsertId = updatededData.id
		else:
			return {"status":False, "msg": GenericMsgMod.Msg(lang, 'error-msg'),
				 "data":dict(), 'loggedInStatus':True}  
		return {"status":True, 'firstDropInsertId':firstDropInsertId}
	def second_drop_location_manipulate(self, request, order_id):
		lang = request.data['langC']
		secondDropOffLatLong = json.loads(request.data.get('second_drop_off_lat_long'))
		for key, value in secondDropOffLatLong.items():
			if not fieldEmptyCheck(value):
				return {"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'second_drop_off_'+ key),
				 "data":dict(), 'loggedInStatus':True}     
		
		drop_off_data_data_obj2 = json.loads(request.data.get('drop_off_data2'))
		# for key, value in drop_off_data_data_obj1.items():
		# 	if not fieldEmptyCheck(value):
		# 		return {"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'second_drop_off_'+ key),
		# 		 "data":dict(), 'loggedInStatus':True}   
		margeDataWithSecondDrop = self.merge_two_dicts(secondDropOffLatLong, drop_off_data_data_obj2)
		margeDataWithSecondDrop['drop_location_type'] = 2
		margeDataWithSecondDrop['item_name'] = request.data.get('second_location_item_name')
		firstDropOffLatLong = json.loads(request.data.get('first_drop_off_lat_long'))
		firstLatLong = '"'+str(firstDropOffLatLong['latitude'])+', '+ str(firstDropOffLatLong['longitude'])+'"'
		secondLatLong = '"'+str(secondDropOffLatLong['latitude'])+', '+ str(secondDropOffLatLong['longitude'])+'"'

		distanceAndDurationSecondDrop = distanceBtwTwoLocationGoogle(firstLatLong, secondLatLong)  
		if distanceAndDurationSecondDrop:
			secondDropDistanceLoc = float(distanceAndDurationSecondDrop['totalDistance'])/1000
			secondDropDistanceLoc = format(secondDropDistanceLoc, '.2f')
			margeDataWithSecondDrop['distance'] = secondDropDistanceLoc

		if fieldEmptyCheck(request.data.get('cash_collection_location_two')):
			margeDataWithSecondDrop['cash_collection'] = request.data.get('cash_collection_location_two')
		ndDropOffLocationObj = NdDropOffLocation(order_id=order_id)
		secondDropInsertId = None
		secondDropInsertId = None
		ndOrderProcessingDataSE = NdDropOffLocationSE(ndDropOffLocationObj, margeDataWithSecondDrop)
		if ndOrderProcessingDataSE.is_valid():
			updatededData = ndOrderProcessingDataSE.save()
			secondDropInsertId = updatededData.id
		else:
			return {"status":False, "msg": GenericMsgMod.Msg(lang, 'error-msg'),
				 "data":dict(), 'loggedInStatus':True}  
		return {"status":True, 'secondDropInsertId':secondDropInsertId}
	@transaction.atomic	
	def post(self, request):
		lang = request.data['langC']
		# try:
		loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
		 request.data.get('session_unique_uuid'))
		if not loggedInStatus:
			return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'session_out'),
			 "data":dict(), 'loggedInStatus':loggedInStatus})
		elif not fieldEmptyCheck(request.data.get('pick_up_data')):
			return Response({"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'pick_up_data'), 
				"data":dict(), 'loggedInStatus':loggedInStatus})
		elif not fieldEmptyCheck(request.data.get('drop_off_data1')):
			return Response({"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'drop_off_data1'),
			 "data":dict(), 'loggedInStatus':loggedInStatus})
		elif not fieldEmptyCheck(request.data.get('distance')):
			return Response({"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'distance'),
			 "data":dict(), 'loggedInStatus':loggedInStatus})   
		elif not fieldEmptyCheck(request.data.get('base_price')):
			return Response({"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'base_price'),
			 "data":dict(), 'loggedInStatus':loggedInStatus})
		# elif not fieldEmptyCheck(request.data.get('first_location_item_name')):
		# 	return Response({"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'first_location_item_name'),
		# 	 "data":dict(), 'loggedInStatus':loggedInStatus})
		# fedInStatus':loggedInStatus})
		# elif not fieldEmptyCheck(request.data.get('base_fare_payment_method')):
		# 	return Response({"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'base_fare_payment_method'),
		# 	 "data":dict(), 'loggedInStatus':loggedInStatus})
		elif not fieldEmptyCheck(request.data.get('pick_up_lat_long')):
			return Response({"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'pick_up_lat_long'),
			 "data":dict(), 'loggedInStatus':loggedInStatus})
		elif not fieldEmptyCheck(request.data.get('first_drop_off_lat_long')):
			return Response({"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'first_drop_off_lat_long'),
			 "data":dict(), 'loggedInStatus':loggedInStatus})
		elif not fieldEmptyCheck(request.data.get('supplier_id')):
			return Response({"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'supplier_id'),
			 "data":dict(), 'loggedInStatus':loggedInStatus})
		# elif not fieldEmptyCheck(request.data.get('driver_id')):
		# 	return Response({"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'driver_id'),
		# 	 "data":dict(), 'loggedInStatus':loggedInStatus})
		else:
			# return Response({"status":True, "msg": request.data.get('drop_off_data1')})
			random_order_uid = self.random_order_uid(request)
			pickUpDataManipulate = self.pick_up_data_manipulate(request, random_order_uid)
			if not pickUpDataManipulate['status']:
				return Response({"status":False, "msg": pickUpDataManipulate['msg'],
			 "data":dict(), 'loggedInStatus':loggedInStatus})
			# return Response({"status":True, "msg": pickUpDataManipulate})
			firstDropLocationManipulate = self.first_drop_location_manipulate(request, pickUpDataManipulate['lastOrderId'])
			if not firstDropLocationManipulate['status']:
				return Response({"status":False, "msg": firstDropLocationManipulate['msg'],
			 "data":dict(), 'loggedInStatus':loggedInStatus})
			for count, attach_file in enumerate(request.FILES.getlist("attach_files_first_location")):
				print(count)
				ndParcelInformationsObj = NdParcelInformations(order_id=pickUpDataManipulate['lastOrderId'], \
					location_id=firstDropLocationManipulate['firstDropInsertId'])
				ndParcelInformationsSe = NdParcelInformationsSE(ndParcelInformationsObj, data={'parcel_file' : attach_file})
				if ndParcelInformationsSe.is_valid():
					ndParcelInformationsSe.save()
			if fieldEmptyCheck(request.data.get('drop_off_data2')): 
				secondDropLocationManipulate = self.second_drop_location_manipulate(request, pickUpDataManipulate['lastOrderId'])	
				for count, attach_file in enumerate(request.FILES.getlist("attach_files_second_location")):
					ndParcelInformationsObj = NdParcelInformations(order_id=pickUpDataManipulate['lastOrderId'],\
						location_id=secondDropLocationManipulate['secondDropInsertId'])
					ndParcelInformationsSe = NdParcelInformationsSE(ndParcelInformationsObj, data={'parcel_file' : attach_file})
					if ndParcelInformationsSe.is_valid():
						ndParcelInformationsSe.save()	
			return Response({"status":True, "msg": OrderProcessingMsgMod.Msg(lang, 'success-msg'),
		 "data":dict(), "order_uid":random_order_uid, "order_id": pickUpDataManipulate['lastOrderId'], 'loggedInStatus':loggedInStatus})
		# except Exception as e:
		# 	return Response({'status':False, 'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'error-msg'), 'loggedInStatus':True})
	
	def push_send(self, request, customParam, dataFields):
		userIDS = [dataFields['userIDS']]
		
		if dataFields['deviceIDS']:
			deviceIDS = dataFields['deviceIDS']
		pushNotificationFCM.send_push_notification( deviceIDS, userIDS, 
			{"title": dataFields['title'], "body": dataFields['body'], "notification_type_id" : 2}, customParam)
		return True
	
class CancelBooking(APIView):
	def push_send(self, request, customParam, dataFields):
		userIDS = dataFields['userIDS']
		if dataFields['deviceIDS']:
			deviceIDS = dataFields['deviceIDS']
		pushNotificationFCM.send_push_notification( deviceIDS, userIDS, 
			{"title": dataFields['title'], "body": dataFields['body'], "notification_type_id" : 4}, customParam)
		return True
	@transaction.atomic	
	def post(self, request):
		lang = request.data.get('langC')
		try:
			orderFilter = NdOrder.objects.filter(id=int(request.data.get('order_id')))
			
			is_already_deleted = orderFilter.filter(booking_status=settings.BOOKING_STATUS_CANCELLED)
			loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')), 
				request.data.get('session_unique_uuid'))
			if not loggedInStatus:
				return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'session_out'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			# elif is_already_deleted.count() >0 :
			# 	return Response({"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'already-deleted'),
			# 	 "data":dict(), 'loggedInStatus':loggedInStatus})
			
			else:
				bookingDetailsObj = NdOrder.objects.filter(id=int(request.data.get('order_id'))).values("id", "order_uid", "supplier_id", "supplier__first_name",
					 "supplier__last_name", "supplier__profile_picture", "driver__device_token", "location", "driver_id", "location")
				if not bookingDetailsObj.exists():
					return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'error-msg'),
					 "data":dict(), 'loggedInStatus':loggedInStatus})
				bookingDetailsObj = bookingDetailsObj.first()
				ObjectCompleteObj = NdOrderCompletionDetails.objects.filter(order_id=int(request.data.get('order_id')))

				if ObjectCompleteObj.count()>0:
					NdOrder.objects.filter(id=int(request.data.get('order_id'))).update(booking_status=settings.BOOKING_STATUS_CANCELLED, base_price=0)

					ndCancelOrder = NdCancelOrder(supplier_id=int(request.data.get('supplier_id')), driver_id=bookingDetailsObj['driver_id'],
						 reason_id=int(request.data.get('reason_id')), order_id=int(request.data.get('order_id')), 
						 reason_description=sanitize(request.data.get('reason_description')), cancelled_by_id=int(bookingDetailsObj['driver_id']))
					ndCancelOrder.save()
					title = "Cancelled: Your trip  has been cancelled by the Supplier"
					body = "Order ID: #"+ str(bookingDetailsObj['order_uid']) + "\n" + "Pickup From: "+ str(bookingDetailsObj['location'])

					NdUsersObjects.objects.filter(user_id=bookingDetailsObj['driver_id']).update(is_available=True)
					deviceIDS = [bookingDetailsObj['driver__device_token']]
					userIDS = [bookingDetailsObj['driver_id']]
					dataFields = {"title":title, "body":body, "deviceIDS":deviceIDS, "userIDS":userIDS }	
					customParam = {}
					customParam['push_type'] = settings.NOTIFICATION_TYPE['cancelled_by_supplier']
					customParam['body'] = body
					customParam['title'] = title
					NdBookingRequests.objects.filter(Q(order_id=int(request.data.get('order_id'))), ~Q(driver_id=bookingDetailsObj['driver_id'])).update(is_deleted=True)
					self.push_send(request, customParam, dataFields)
				else:
					driverID = None
					if bookingDetailsObj['driver_id']:
						driverID = bookingDetailsObj['driver_id']
						title = "Cancelled: Your trip  has been cancelled by the Supplier"
						body = "Order ID: #"+ str(bookingDetailsObj['order_uid']) + "\n" + "Pickup From: "+ str(bookingDetailsObj['location'])

						NdUsersObjects.objects.filter(user_id=bookingDetailsObj['driver_id']).update(is_available=True)
						deviceIDS = [bookingDetailsObj['driver__device_token']]
						userIDS = [bookingDetailsObj['driver_id']]
						dataFields = {"title":title, "body":body, "deviceIDS":deviceIDS, "userIDS":userIDS }	
						customParam = {}
						customParam['push_type'] = settings.NOTIFICATION_TYPE['cancelled_by_supplier']
						customParam['body'] = body
						customParam['title'] = title
						print()
						self.push_send(request, customParam, dataFields)
						NdBookingRequests.objects.filter(Q(order_id=int(request.data.get('order_id'))), ~Q(driver_id=driverID)).update(is_deleted=True)
					else:
						NdBookingRequests.objects.filter(Q(order_id=int(request.data.get('order_id')))).update(is_deleted=True)	
					NdOrder.objects.filter(id=int(request.data.get('order_id'))).update(booking_status=settings.BOOKING_STATUS_CANCELLED, base_price=0)
					ndCancelOrder = NdCancelOrder(supplier_id=int(request.data.get('supplier_id')), driver_id=driverID,
						 reason_id=int(request.data.get('reason_id')), order_id=int(request.data.get('order_id')), 
						 reason_description=sanitize(request.data.get('reason_description')), cancelled_by_id=int(request.data.get('supplier_id')))
					ndCancelOrder.save()
				return Response({"status":True, "msg": OrderProcessingMsgMod.Msg(lang, 'cancel-success'),
					 "data":dict(), 'loggedInStatus':loggedInStatus})
		except Exception as E:
			return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'error-msg'),
			 "data":dict(), 'loggedInStatus':True})
	@transaction.atomic	
	def patch(self, request, pk):
		lang = request.data.get('langC')
		try:
			# is_already_deleted = NdOrder.objects.filter(id=int(pk), booking_status=settings.BOOKING_STATUS_CANCELLED)
			loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')), 
				request.data.get('session_unique_uuid'))
			# if is_already_deleted.count() >0 :
			# 	return Response({"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'already-deleted'),
			# 	 "data":dict(), 'loggedInStatus':loggedInStatus})
			if not loggedInStatus: 
				return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'session_out'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(int(request.data.get('reason_id'))):
				return Response({"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'reason_id'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('reason_description')):
				return Response({"status":False, "msg": OrderProcessingMsgMod.Msg(lang, 'reason_description'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			else:
				bookingDetailsObj = NdOrder.objects.filter(id=int(pk)).values("id", "order_uid", "supplier_id", "supplier__first_name",
				 "supplier__last_name", "supplier__profile_picture", "supplier__device_token", "location").first()
				ndCancelOrder = NdCancelOrder(supplier_id=int(request.data.get('supplier_id')), driver_id=int(request.data.get('driver_id')),
					 reason_id=int(request.data.get('reason_id')), order_id=int(pk), 
					 reason_description=sanitize(request.data.get('reason_description')))
				ndCancelOrder.save()
				return Response({"status":True, "msg": CancelBookingMsgMod.Msg(lang, 'cancel-success'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
		except Exception as E:
			return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'error-msg'),
			 "data":dict(), 'loggedInStatus':loggedInStatus})
#---------------------------------------------------- Vehicles Type ------------------------------------------------#
class VehicleTypes(APIView):
	def post(self, request):
		lang = request.data['langC']
		try:
			loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
			 request.data.get('session_unique_uuid'))
			if not loggedInStatus:
				return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'session_out'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('max_distance')):
				return Response({"status":False, "msg": VehicleTypesMsgMod.Msg(lang, 'max_distance'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			else:
				vehicleTypeObj = NdVehicleType.objects.filter(Q(is_status=True), Q(is_deleted=False), ~Q(vehicletype__id=None), 
				Q(vehicletype__is_status=True), Q(vehicletype__is_deleted=False), 
				Q(max_distance__gte=float(request.data.get('max_distance')))).distinct()
				if vehicleTypeObj.count()> 0:
					ndVehicleTypeSE = NdVehicleTypeSE(vehicleTypeObj, many=True, context={'lang': lang})
					return Response({"status":True, "msg": VehicleTypesMsgMod.Msg(lang, 'record-found'),
					 "data": ndVehicleTypeSE.data, 'loggedInStatus':loggedInStatus}) 
				else:
					return Response({"status":False, "msg": VehicleTypesMsgMod.Msg(lang, 'not-found'),
					 "data": dict(), 'loggedInStatus':loggedInStatus})
		except Exception as e:
			return Response({'status':False, 'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'error-msg'),
			 'loggedInStatus':True})

# class NearestVehicleBooking(APIView):
# 	def push_send(self, request, customParam, userDetailsObj):
# 		userDetailsObj=NdUsers.objects.filter(id=int(customParam['driver_id'])).values('device_token').first()
# 		userIDS = [customParam['driver_id']]
# 		deviceIDS = []
# 		title = "Booking(#" + customParam['order_uid'] + ") declined"
# 		body = "Reason: Wait time is over."
# 		customData = userDetailsObj
# 		if userDetailsObj['device_token']:
# 			deviceIDS = [userDetailsObj['device_token']]
# 		customData = {"order_id": int(customParam['order_id']), "supplier_id":int(customParam['supplier_id'])}
# 		pushNotificationFCM.send_push_notification( deviceIDS, userIDS, {"title": title, "body": body},	customData)
# 		return True
# 	def distance(self, lat1, lon1, lat2, lon2):
# 		# p = 0.017453292519943295
# 		# a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
# 		# return 6367 *  asin(sqrt(a))

# 		lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

# 	# haversine formula 
# 		dlon = lon2 - lon1 
# 		dlat = lat2 - lat1 
# 		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
# 		c = 2 * asin(sqrt(a)) 
# 		r = 6371 # Radius of earth in kilometers. Use 3956 for miles
# 		return c * r
	
# 	def vehicles_within_range(self, lat1, lon1, lat2, lon2):
# 		distance = self.distance(float(lat1), float(lon1), float(lat2), float(lon2))
# 		return format(float(distance), '.2f')
# 	def closest(self, data, v):
# 		return min(data, key=lambda p: self.distance(float(v['latitude']), float(v['longitude']), float(p['latitude']), float(p['longitude'])))
# 	def post(self, request):
# 		lang = request.data['langC']
# 		# try:
# 		loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
# 		 request.data.get('session_unique_uuid'))
# 		if not loggedInStatus:
# 			return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'session_out'),
# 			 "data":dict(), 'loggedInStatus':loggedInStatus})
# 		elif not fieldEmptyCheck(request.data.get('order_id')):
# 			return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'error-msg'),
# 			 "data":dict(), 'loggedInStatus':loggedInStatus})
# 		else:
# 			orderDetailsObj=NdOrder.objects.filter(id=int(request.data.get('order_id')))
# 			if orderDetailsObj.count()>0:
# 				orderDetailsObj = orderDetailsObj.values('latitude', 'longitude', 'driver_id', 'supplier_id',
# 				 'driver__phone_number', 'driver__first_name', 'driver__last_name', 'order_uid',
# 				 'driver__profile_picture', 'driver__current_location', 'driver__device_token').first()
# 				if orderDetailsObj['driver_id']:
# 					return Response({'status':True, 'data':orderDetailsObj, 'msg':NearestVehicleBookingMsgMod.Msg(lang, 'booking-confirmed'), 
# 					'loggedInStatus':True})
# 				driverListObj =  NdUsers.objects.filter(is_status=True, is_deleted=False, role_id=settings.IS_DRIVER)
# 				driverIds = request.data.get('driver_ids')
# 				if driverIds:
# 					for userId in driverIds:
# 						driverListObj = driverListObj.filter(~Q(id=userId))
# 				tempDataList = []
# 				if driverIds:
# 					lastSelectedDriver = driverIds[-1]
# 					customParam = {"order_id": int(request.data.get('order_id')), "driver_id":lastSelectedDriver,
# 					 "order_uid": orderDetailsObj['order_uid'], "supplier_id":orderDetailsObj['supplier_id']  }		
# 					self.push_send(request, customParam, orderDetailsObj)
# 				vehicles_within_range = []
# 				if driverListObj.count()>0:
# 					tempDataList = driverListObj.values('id', 'latitude', 'longitude')
# 					for item in tempDataList:
# 						distance = self.vehicles_within_range(orderDetailsObj['latitude'], orderDetailsObj['longitude'], 
# 							item['latitude'], item['longitude'])
# 						if float(distance) <= settings.VEHICLE_BOOKING_RANGE:
# 							vehicles_within_range.append({ 'id' : item['id'], 'distance' : float(distance)})
# 				else:
# 					return Response({'status':False, 'data':dict(), 'msg':NearestVehicleBookingMsgMod.Msg(lang, 'not-available'), 
# 					'loggedInStatus':True})			
# 				if vehicles_within_range:
# 					choosedVehicles = sorted(vehicles_within_range, key=itemgetter('distance'))
# 					return Response({ 'status':False, 'data':dict(), 'msg':NearestVehicleBookingMsgMod.Msg(lang, 'searching'),
# 					 "selected_driver_id":choosedVehicles[0]['id'], "distance":choosedVehicles[0]['distance']})
# 				else:
# 					return Response({'status':False, 'data':dict(), 'msg':NearestVehicleBookingMsgMod.Msg(lang, 'not-available'), 
# 					'loggedInStatus':True})
# 			else:
# 				return Response({'status':False, 'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'error-msg'), 
# 					'loggedInStatus':True})
# 		# except Exception as E:
# 		# 	return Response({'status':False, 'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'error-msg'), 
# 		# 		'loggedInStatus':True})
class NearestVehicleBooking(APIView):
	def push_send(self, request, customParam, userDetailsObj):
		userDetailsObj=NdUsers.objects.filter(id=int(customParam['driver_id'])).values('device_token').first()
		userIDS = [customParam['driver_id']]
		deviceIDS = []
		title = "Booking(#" + customParam['order_uid'] + ") declined"
		body = "Reason: Wait time is over."
		customData = userDetailsObj
		if userDetailsObj['device_token']:
			deviceIDS = [userDetailsObj['device_token']]
		customData = {"order_id": int(customParam['order_id']), "supplier_id":int(customParam['supplier_id'])}
		pushNotificationFCM.send_push_notification( deviceIDS, userIDS, {"title": title, "body": body},	customData)
		return True
	def distance(self, lat1, lon1, lat2, lon2):
		# p = 0.017453292519943295
		# a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
		# return 6367 *  asin(sqrt(a))

		lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

	# haversine formula 
		dlon = lon2 - lon1 
		dlat = lat2 - lat1 
		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
		c = 2 * asin(sqrt(a)) 
		r = 6371 # Radius of earth in kilometers. Use 3956 for miles
		return c * r
	
	def vehicles_within_range(self, lat1, lon1, lat2, lon2):
		distance = self.distance(float(lat1), float(lon1), float(lat2), float(lon2))
		return format(float(distance), '.2f')
	def closest(self, data, v):
		return min(data, key=lambda p: self.distance(float(v['latitude']), float(v['longitude']), float(p['latitude']), float(p['longitude'])))
	def post(self, request):
		lang = request.data['langC']
		# return Response({'status':False, 'data':request.data, 'msg':GenericMsgMod.Msg(lang, 'error-msg'), 
		# 			'loggedInStatus':True})
		# try:
		loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
		 request.data.get('session_unique_uuid'))
		if not loggedInStatus:
			return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'session_out'),
			 "data":dict(), 'loggedInStatus':loggedInStatus})
		elif not fieldEmptyCheck(request.data.get('order_id')):
			return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'error-msg'),
			 "data":dict(), 'loggedInStatus':loggedInStatus})
		else:
			return Response({'status':False, 'data':request.data, 'msg':GenericMsgMod.Msg(lang, 'error-msg'), 
					'loggedInStatus':True})
			orderDetailsObj=NdOrder.objects.filter(id=int(request.data.get('order_id')))
			if orderDetailsObj.count()>0:
				orderDetailsObj = orderDetailsObj.values('latitude', 'longitude', 'driver_id', 'supplier_id',
				 'driver__phone_number', 'driver__first_name', 'driver__last_name', 'order_uid',
				 'driver__profile_picture', 'driver__current_location', 'driver__device_token').first()
				if orderDetailsObj['driver_id']:
					return Response({'status':True, 'data':orderDetailsObj, 'msg':NearestVehicleBookingMsgMod.Msg(lang, 'booking-confirmed'), 
					'loggedInStatus':True})
				driverListObj =  NdUsers.objects.filter(is_status=True, is_deleted=False, role_id=settings.IS_DRIVER)
				driverIds = request.data.get('driver_ids')
				if driverIds:
					for userId in driverIds:
						driverListObj = driverListObj.filter(~Q(id=userId))
				tempDataList = []
				if driverIds:
					lastSelectedDriver = driverIds[-1]
					customParam = {"order_id": int(request.data.get('order_id')), "driver_id":lastSelectedDriver,
					 "order_uid": orderDetailsObj['order_uid'], "supplier_id":orderDetailsObj['supplier_id']  }		
					self.push_send(request, customParam, orderDetailsObj)
				vehicles_within_range = []
				if driverListObj.count()>0:
					tempDataList = driverListObj.values('id', 'latitude', 'longitude')
					for item in tempDataList:
						distance = self.vehicles_within_range(orderDetailsObj['latitude'], orderDetailsObj['longitude'], 
							item['latitude'], item['longitude'])
						if float(distance) <= settings.VEHICLE_BOOKING_RANGE:
							vehicles_within_range.append({ 'id' : item['id'], 'distance' : float(distance)})
				else:
					return Response({'status':False, 'data':dict(), 'msg':NearestVehicleBookingMsgMod.Msg(lang, 'not-available'), 
					'loggedInStatus':True})			
				if vehicles_within_range:
					choosedVehicles = sorted(vehicles_within_range, key=itemgetter('distance'))
					return Response({ 'status':False, 'data':dict(), 'msg':NearestVehicleBookingMsgMod.Msg(lang, 'searching'),
					 "selected_driver_id":choosedVehicles[0]['id'], "distance":choosedVehicles[0]['distance']})
				else:
					return Response({'status':False, 'data':dict(), 'msg':NearestVehicleBookingMsgMod.Msg(lang, 'not-available'), 
					'loggedInStatus':True})
			else:
				return Response({'status':False, 'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'error-msg'), 
					'loggedInStatus':True})
		# except Exception as E:
		# 	return Response({'status':False, 'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'error-msg'), 
		# 		'loggedInStatus':True})
class DriverResponse(APIView):
	def push_send(self, request, customParam, userDetailsObj):
		userIDS = userDetailsObj['supplier_id']
		deviceIDS = []
		title = "Your booking (" + userDetailsObj['order_uid'] + ") has been confirmed"
		body = "Driver Name:"+ str(userDetailsObj['driver__first_name']) + " " + str(userDetailsObj['driver__last_name'])\
		 +" Location:" + str(userDetailsObj['driver__current_location'])
		customData = userDetailsObj
		if userDetailsObj['supplier__device_token']:
			deviceIDS = [userDetailsObj['supplier__device_token']]
		customData = {"order_id": int(customParam['pk']), "driver_id":int(request.data.get('driver_id'))}
		pushNotificationFCM.send_push_notification( deviceIDS, userIDS, {"title": title, "body": body}, customData)
		return True
	def patch(self, request, pk):
		lang = request.data['langC']
		try:
			loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
			 request.data.get('session_unique_uuid'))
			if not loggedInStatus:
				return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'session_out'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('driver_id')):
				return Response({"status":False, "msg": DriverResponseMsgMod.Msg(lang, 'driver_id'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('device_type')):
				return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'device_type'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			else:
				userDetailsObj = NdOrder.objects.filter(id=int(pk)).values('supplier_id', 'supplier__device_token',
					'latitude', 'longitude', 'driver_id','driver__phone_number',
					'driver__first_name', 'driver__last_name','driver__profile_picture', 
					'driver__current_location','order_uid').first()
				if request.data.get('response_type'): 
					NdOrder.objects.filter(id=int(pk)).update(driver_id=int(request.data.get('driver_id')), 
						booking_time=current_date_time(), booking_status=settings.BOOKING_STATUS_PLACED)	
					customParam = {"pk": int(pk) }		
					self.push_send(request, customParam, userDetailsObj)
					return Response({'status':True, 'data':userDetailsObj, 'msg':DriverResponseMsgMod.Msg(lang, 'driver_accepted'), 
					'loggedInStatus':True, "response_type" : True})
				else:
					ndBookingRejectsObj = NdBookingRejects(order_id=int(pk),
					 driver_id=int(request.data.get('driver_id')))
					ndBookingRejectsObj.save()
					# customParam = {"pk": int(pk) }		
					# self.push_send(request, customParam)
					return Response({'status':True, 'data':userDetailsObj, 'msg':DriverResponseMsgMod.Msg(lang, 'driver_declined'), 
					'loggedInStatus':True, "response_type" : False, "driver_id":int(request.data.get('driver_id'))})
		except Exception as E:
			return Response({'status':False, 'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'error-msg'), 
					'loggedInStatus':True})
class ReviewTypes(APIView):
	def get(self, request):
		try:
			reviewTypesObj = NdReviewTypes.objects.filter(is_status=True, is_deleted=False).values('id', 'review_reason')
			return Response({"status":True, "msg":"", "data":reviewTypesObj, 'loggedInStatus':True})
		except Exception as e:
			return Response({'status':False, 'data':dict(), 'msg':"Something went wrong", 
					'loggedInStatus':True})

class ReviewPost(APIView):
	def push_send(self, request, customParam, dataFields):
		userIDS = dataFields['userIDS']
		
		if dataFields['deviceIDS']:
			deviceIDS = dataFields['deviceIDS']
		pushNotificationFCM.send_push_notification( deviceIDS, userIDS, 
			{"title": dataFields['title'], "body": dataFields['body'], "notification_type_id" : 3}, customParam)
		return True
	def is_already_posted(self, request):
		checkExistance = NdReviewPosted.objects.filter(driver_id=int(request.data.get('driver_id')), order_id=int(request.data.get('order_id')),
			is_deleted=False )
		if checkExistance.count()>0:
			return True
		else:
			return False
	@transaction.atomic	
	def post(self, request):
		lang = request.data['langC']
		try:
			loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
			 request.data.get('session_unique_uuid'))
			if not loggedInStatus:
				return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'session_out'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('posted_by')):
				return Response({"status":False, "msg": ReviewPostMsgMod.Msg(lang, 'posted_by'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif self.is_already_posted(request):
				return Response({"status":False, "msg": ReviewPostMsgMod.Msg(lang, 'already_posted'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('driver_id')):
				return Response({"status":False, "msg": ReviewPostMsgMod.Msg(lang, 'driver_id'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('star_rate')):
				return Response({"status":False, "msg": ReviewPostMsgMod.Msg(lang, 'star_rate'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('order_id')):
				return Response({"status":False, "msg": ReviewPostMsgMod.Msg(lang, 'order_id'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			else:

				reviewPostObj = NdReviewPosted(posted_by_id=int(request.data.get('posted_by')), driver_id=int(request.data.get('driver_id')),
					star_rate=int(request.data.get('star_rate')), review_type_id=int(request.data.get('review_type')), review_text=request.data.get('review_text'), 
					order_id=int(request.data.get('order_id')))
				
				reviewPostObj.save()
				reviewDetails = update_over_all_rating(int(request.data.get("driver_id")))
				
				customParam = {}
				orderDetails = NdOrder.objects.filter(id=int(request.data.get('order_id'))).values('id', 'supplier__first_name',
				 'supplier__last_name', 'supplier__profile_picture', 'order_uid', 'driver_id', 'driver__device_token').first()
				title = str(request.data.get('star_rate')) + " star rating by " + str(orderDetails['supplier__first_name']) + " " + str(orderDetails['supplier__last_name'])
				body = "Order ID: "+ str(orderDetails['order_uid'])
				deviceIDS = [orderDetails['driver__device_token']]
				userIDS = [int(request.data.get('driver_id'))]
				customParam = {}
				customParam['push_type'] = settings.NOTIFICATION_TYPE['review_posted']
				customParam['body'] = body
				customParam['title'] = title
				dataFields = {"title":title, "body":body, "deviceIDS":deviceIDS, "userIDS":userIDS }	
				self.push_send(request, customParam, dataFields)
				
				return Response({"status":True, "msg":ReviewPostMsgMod.Msg(lang, 'success-msg'), "data":list(),
				 'loggedInStatus':True, 'over_all_review':reviewDetails['avg_rating'], 'no_of_reviews':reviewDetails['no_of_reviews']})
		except Exception as e:
			return Response({'status':False, 'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'error-msg'),'loggedInStatus':True})
class FetchDriverDetails(APIView):
	def post(self, request):
		lang = request.data['langC']
		try:
			loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
			 request.data.get('session_unique_uuid'))
			if not loggedInStatus:
				return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'session_out'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('order_id')):
				return Response({"status":False, "msg": FetchDriverDetailsMsgMod.Msg(lang, 'order_id'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			else:
				record = NdOrder.objects.filter(is_deleted=False, id=int(request.data.get('order_id')))
				if record.count()>0:
					fetchDriverDetails = NdOrderDriverDetailsSe(record.first(), many=False, context={'lang':lang})
					return Response({"status":True, "msg":FetchDriverDetailsMsgMod.Msg(lang, 'success-msg'), "data":fetchDriverDetails.data,
				 'loggedInStatus':True})
		except Exception as e:
			return Response({'status':False, 'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'error-msg'), 
					'loggedInStatus':True})
class CancelReasons(APIView):
	def post(self, request):
		lang = request.data['langC']
		try:
			reasonObj= NdCancellationReason.objects.filter(is_status=True, is_deleted=False).order_by('sort_by')
			loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
			 request.data.get('session_unique_uuid'))
			if not loggedInStatus:
				return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'session_out'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif reasonObj.count()>0 :
				reasonObj = reasonObj.values('id', 'reason')
				return Response({"status": True, 'data':reasonObj, 'msg':OrderProcessingMsgMod.Msg(lang, 'record-found'),
				 'loggedInStatus':True})
			else:
				return Response({"status":False, 'data':dict(), 'msg':OrderProcessingMsgMod.Msg(lang, 'not-found'),
				 'loggedInStatus':True})
		except Exception as E:
			return Response({"status":False, 'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'error-msg'), 
				'loggedInStatus':True})

class CouponCalculationValidation(APIView):
	@transaction.atomic	
	def post(self, request):
		lang = request.data.get('langC')
		try:
			loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')), 
				request.data.get('session_unique_uuid'))
			if not loggedInStatus:
				return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'session_out'),
				 "data":dict(), "coupon_id": 0, 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('promotion_code')):
				return Response({"status":False, "msg":CouponCalculationValidationMsgMod.Msg(lang, 'promotion_code'),
				 "data":dict(), "coupon_id": 0, 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('delivery_fee')):
				return Response({"status":False, "msg":CouponCalculationValidationMsgMod.Msg(lang, 'delivery_fee'),
				 "data":dict(), "coupon_id": 0, 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('supplier_id')):
				return Response({"status":False, "msg":CouponCalculationValidationMsgMod.Msg(lang, 'supplier_id'),
				 "data":dict(), "coupon_id": 0, 'loggedInStatus':loggedInStatus})
			else:
				now = datetime.now()
				now = now.strftime("%Y-%m-%d")
				availableCoupon = NdPromotions.objects.filter(is_status=True,  is_deleted=False, couponDetails__id__isnull = False, couponDetails__is_status=True, 
				couponDetails__is_deleted=False, couponDetails__supplier_id=int(request.data.get('supplier_id')), promotion_code = request.data.get('promotion_code'))
				if availableCoupon.exists():
					availableCouponObj = availableCoupon.values('id', "promotion_code", "start_date", "end_date", "discount").first()
					if now < str(availableCouponObj['start_date']):
						return Response({"status":False, "msg":CouponCalculationValidationMsgMod.Msg(lang, 'applicable_soon'),
							"data":dict(), "coupon_id": 0, 'loggedInStatus':loggedInStatus})
					elif now > str(availableCouponObj['end_date']):
						return Response({"status":False, "msg":CouponCalculationValidationMsgMod.Msg(lang, 'expired'),
							"data":dict(), "coupon_id": 0, 'loggedInStatus':loggedInStatus})
					else:
						delivery_fee = float(request.data.get('delivery_fee'))
						percentageDiscount = (delivery_fee * float(availableCouponObj['discount']))/100
						afterCouponApplied = delivery_fee - percentageDiscount

						return Response({"status":True, "msg": CouponCalculationValidationMsgMod.Msg(lang, 'coupon_applied_successfully'),
							"fee":format(float(afterCouponApplied), '.2f'), "old_fee": float(request.data.get('delivery_fee')),
							"coupon_id":availableCouponObj['id'], 'loggedInStatus':loggedInStatus})
				else:
					return Response({"status":False, "msg": CouponCalculationValidationMsgMod.Msg(lang, 'not_exists'),
							"data":dict(), "coupon_id": 0, 'loggedInStatus':loggedInStatus})		
		except Exception as E:
			return Response({"status":False, "coupon_id": 0, 'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'error-msg'), 
				'loggedInStatus':True})

class CashInHandCalculation(APIView):
	@transaction.atomic	
	def post(self, request):

		lang = request.data.get('langC')
		try:
			loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')), 
				request.data.get('session_unique_uuid'))
			if not loggedInStatus:
				return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'session_out'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('delivery_fee')):
				return Response({"status":False, "msg":CouponCalculationValidationMsgMod.Msg(lang, 'delivery_fee'),
				 "data":dict(), 'loggedInStatus':loggedInStatus})
			else:
				discountData = NdSettings.objects.filter(field_name="discount", is_status=True, is_deleted=False).values('field_val')
				# print(str(discountData))
				isDiscoundApplied = False
				if discountData.exists():
					discountDataObj = discountData.first()
					if discountDataObj['field_val'] !="" or discountDataObj['field_val']:
						if float(discountDataObj['field_val']) >0  :
							isDiscoundApplied = True

				cashDiscountData = NdSettings.objects.filter(field_name="Cash collection discount", is_status=True, is_deleted=False).values('field_val')
				delivery_fee = float(request.data.get('delivery_fee'))
				totalCharge = 0
				cash_in_hand_discount = 0
				if not isDiscoundApplied:
					if cashDiscountData.exists():
						discountDataObj = cashDiscountData.first()
						if discountDataObj['field_val'] !="" or discountDataObj['field_val']:
							if float(discountDataObj['field_val']) >0  :
								cash_in_hand_discount = discountDataObj['field_val']
								percentage = delivery_fee * float(discountDataObj['field_val'])/100
								totalCharge = delivery_fee + percentage
							else:
								totalCharge = delivery_fee * 2
						else:
							totalCharge = delivery_fee * 2
					else:
						totalCharge = delivery_fee * 2	
				else:
					totalCharge = delivery_fee		

				return Response({"status":True,  "old_fee":request.data.get('delivery_fee'), "cash_on_hand_discount":float(cash_in_hand_discount), "msg": GenericMsgMod.Msg(lang, 'data-fetched'),
					"fee":format(float(totalCharge), '.2f'), 'loggedInStatus':loggedInStatus})
				# else:
	
		except Exception as E:
			return Response({"status":False, 'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'error-msg'), 
				'loggedInStatus':True})

class CloesetVehicleSelection(APIView):
	def push_send(self, request, customParam, dataFields):
		userIDS = dataFields['userIDS']
		
		if dataFields['deviceIDS']:
			deviceIDS = dataFields['deviceIDS']
		pushNotificationFCM.send_push_notification( deviceIDS, userIDS, 
			{"title": dataFields['title'], "body": dataFields['body'], "notification_type_id" : 3}, customParam)
		return True
	def sortedList(self, unSortedData):
		# sorted_d = sorted(unSortedData.items(), key=operator.itemgetter(2))
		newlist= sorted(unSortedData.keys('distance'))
		# newlist = sorted(unSortedData, key=itemgetter('distance')) 
		return newlist
	def post(self, request):
		# return Response({"status":False, "msg": request.data['request_data']})
		# lang = request.data['langC']
		# try:
		requestData = request.data['request_data']
		driversData = request.data['drivers_data']
		maxRadius = float(request.data['radius'])
		lists =[] # create empty list
		for val in requestData['tried_drivers']: 
			if val in lists :
				# print("yyyyyy/yy", val) 
				if val == '':
					continue 
				continue
			else:
				lists.append(val)

		print("^^^^^^^^^^^", lists)
		requestData['tried_drivers'] = lists
		filteredVehicles ={}
		if lists and not bool(requestData['retry'])	 :
			listLength = len(lists)
			prevData = listLength - 1
			# print("^^^^^^^^^^^", requestData)
			driverKey = lists[prevData]
			driverKeyObj = driverKey.split("~")
			i=0
			if fieldEmptyCheck(driverKey):
				userDetails = NdUsers.objects.filter(id=int(driverKeyObj[0])).values('id', 'device_token')
				if userDetails.exists():
					# print("^^^^^^^^^^^^^^^^", int(driverKeyObj[0]))
					# print("()()()()()()()()()()")
					userDetailsObj = userDetails.first()
					if fieldEmptyCheck(userDetailsObj['device_token']):
						title = "Normal wait time crossed"
						body = "Your booking #"+ requestData['order_uid']+" has been cancelled"
						deviceIDS = [userDetailsObj['device_token']]
						userIDS = [userDetailsObj['id']]
						dataFields = {"title":title, "body":body, "deviceIDS":deviceIDS, "userIDS":userIDS }	
						customParam = {}
						customParam['push_type'] = settings.NOTIFICATION_TYPE['cross_overhead']
						customParam['body'] = body
						customParam['title'] = title
						self.push_send(request, customParam, dataFields)

		# else:
		supplier_lat_long = '"'+str(requestData['latitude'])+', '+ str(requestData['longitude'])+'"'
		# print(maxRadius)
		bookingEstimate = float(requestData['booking_cost'])
		# print("&&&",lists)
		if driversData:
			for key in driversData:
				if key not in lists:
					driver_lat_long = '"'+str(driversData[key]['latitude'])+', '+ str(driversData[key]['longitude'])+'"'
					distanceCalculated = distanceBtwTwoLocationGoogle(supplier_lat_long, driver_lat_long)  
					distanceInKm = distanceCalculated['totalDistance']/1000
					driverIdObj = key.split("~")
					ndDriverDetails = NdDriverDetails.objects.filter(user_id=int(driverIdObj[0]), user__users_object_details__is_available=True).values('account_balance')
					if ndDriverDetails.exists():
						ndDriverDetails = ndDriverDetails.first()
						if maxRadius>= float(distanceInKm) and float(ndDriverDetails['account_balance'])>= bookingEstimate:
							driversData[key]['distance'] = distanceCalculated['totalDistance']
							driversData[key]['estimated_time'] = distanceCalculated['estimatedTime']
							filteredVehicles[key] = driversData[key]
		# sortedList = self.sortedList(filteredVehicles)				
		# print(filteredVehicles)
			return Response({"status":True, "data":filteredVehicles })
		else:
			return Response({"status":False, "data":dict() })
		# except Exception as E:
		# 	return Response({"status":False, 'data':dict(), 'msg':"", 
		# 		'loggedInStatus':True})

class BookingHistoryWithPagination(APIView):
	def post(self, request):
		lang = request.data['langC']
		try:
			loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
			 request.data.get('session_unique_uuid'))
			if not loggedInStatus:
				return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
			 "data" : dict(), 'loggedInStatus' : loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('supplier_id')):
				return Response({"status":False, "msg":GenericMsgMod.Msg(lang, 'error-msg'),
				 "data" : dict(), 'loggedInStatus' : loggedInStatus})
			else:
				orderDetails = NdOrder.objects.filter(Q(supplier_id=int(request.data.get('supplier_id'))), ~Q(booking_status=settings.BOOKING_STATUS_PROCESSING),
				Q(driver_id__isnull = False))
				if fieldEmptyCheck(request.data.get('start_date')) and fieldEmptyCheck(request.data.get('end_date')): 
					orderDetails = orderDetails.filter(booking_time__range=[request.data.get('start_date'), request.data.get('end_date')] )
				elif fieldEmptyCheck(request.data.get('start_date')):
					startDate = datetime.strptime(request.data.get('start_date'), "%Y-%m-%d").date()
					orderDetails = orderDetails.filter(booking_time__year=startDate.year, booking_time__month=startDate.month, booking_time__day=startDate.day )
				try:
					orderDetailObj = orderDetails.order_by('-id')
					page = request.data.get('start',1)
					paginator = Paginator(orderDetailObj, settings.FRONT_END_NO_OF_RECORD)
					orderDetailObj = paginator.page(int(page))

				except EmptyPage:   
					return Response({'status':False, 'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'data-not-found'),
					 'total_record': orderDetails.count(), 'loggedInStatus' : loggedInStatus})
				orderDetailsForHistorySE = OrderDetailsForHistorySE(orderDetailObj, many=True, context= { 'currentLang': lang })

				return Response({"status":True, "msg":GenericMsgMod.Msg(lang, 'data-fetched'),
				 "data" : orderDetailsForHistorySE.data, 'total_record': orderDetails.count() , 'loggedInStatus' : loggedInStatus})
		except Exception as e:
		  return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict(), 'loggedInStatus' : True})
class OngoingBooking(APIView):
	def post(self, request):
		lang = request.data['langC']
		try:
			loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
			 request.data.get('session_unique_uuid'))
			if not loggedInStatus:
				return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
			 "data" : dict(), 'loggedInStatus' : loggedInStatus})
			elif not fieldEmptyCheck(request.data.get('supplier_id')):
				return Response({"status":False, "msg":OngoingBookingMsgMod.Msg(lang, 'supplier_id'),
				 "data" : dict()})
			elif not fieldEmptyCheck(request.data.get('order_id')):
				return Response({"status":False, "msg":OngoingBookingMsgMod.Msg(lang, 'order_id'),
				 "data" : dict()})
			else:
				orderDetails = NdOrder.objects.filter(id=int(request.data.get('order_id')), supplier_id=int(request.data.get('supplier_id')), 
					booking_status=settings.BOOKING_STATUS_PLACED)
				if orderDetails.exists():
					orderDetailsObj = NdOrderForCurrentBookingSe(orderDetails.first(), many=False, context={'lang':lang})
					return Response({"status":True, "msg":GenericMsgMod.Msg(lang, 'data-fetched'), "data" : orderDetailsObj.data})
				else:
					return Response({"status":True, "msg":GenericMsgMod.Msg(lang, 'data-fetched'), "data" : dict()})
		except Exception as e:
		  return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict()})