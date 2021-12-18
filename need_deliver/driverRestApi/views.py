from django.shortcuts import render
from .serializers import *
from webAdmin.serializers import *
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
pushNotificationFCM, generateUID, is_document_upload_pending, calculationCurrencyConversion,calculationCurrencyConversionWithPresentCur
import json
from django.db import  transaction, connection
cursor = connection.cursor()
from math import radians, cos, sin, asin, sqrt
from operator import itemgetter
from webAdmin.views import encrypt, decrypt, encrypt_val, decrypt_val
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
import ast
from django.utils import timezone
client = boto3.client(
    "sns",
    aws_access_key_id= settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY,
    region_name= settings.SEGION_NAME
)
def distanceCalculation( distance, order_id ):
    getOrderDetails = NdOrder.objects.filter(id=int(order_id)).values('base_price', 'distance', 'booking_time' ).first()
    return format(float(getOrderDetails['base_price']), '.2f')
    costCalculated = 0
    if float(distance)>0:
        if float(distance) >= float(getOrderDetails['distance']):
            getUnitDistanceCosting = float(getOrderDetails['base_price'])/float(getOrderDetails['distance'])
            costCalculated = getUnitDistanceCosting * totalDistance
            return format(float(costCalculated), '.2f')
        else:
             return format(float(getOrderDetails['base_price']), '.2f')
    else:
        return format(float(getOrderDetails['base_price']), '.2f')
# ---------------------------------------------- Driver Registration -------------------------------------------------- #
class DriverRegistration(APIView):
    def randomPassword( self, request ):
        # return "1111"
        random_code = get_random_string(length=4, allowed_chars='123456789')
        randomKeycheck = NdUsers.objects.filter(verification_code=random_code, is_deleted=False).count()
        if randomKeycheck >0 :
            self.randomPassword( request )
        else:
            return random_code
    #------------------------ Method to check unique Email Address -------------------------------------#         
    def get_unique_email(self, request,  pk = None):
        lang = request.data['langC']
        # return {'status': True}
        try:
            if request.data.get('email_id') != "":
                is_exists = NdUsers.objects.filter(Q(email_id__iexact=request.data.get('email_id')), Q(role_id=settings.IS_DRIVER), Q(is_deleted=False)).count()
                if is_exists >0 :
                    return {'status': False, 'msg': DriverRegistrationMsgMod.Msg(lang, 'email_already_reg')}
                else:
                    return {'status': True, 'msg': ''}
            else:
                return {'status': True, 'msg': ''}
        except Exception as e:
            return {'status': False, 'msg': GenericMsgMod.Msg(lang, 'error-msg')}
    #------------------------ Method to check unique phone number -------------------------------------#         
    def get_unique_phone(self, request,):
        lang = request.data['langC']
        try:
            if not fieldEmptyCheck(request.data.get('phone_number')):
                return {'status': False, 'msg': DriverRegistrationMsgMod.Msg(lang, 'phone_number')}
            is_exists = NdUsers.objects.filter(Q(phone_number=request.data.get('phone_number')), Q(role_id=settings.IS_DRIVER), Q(is_deleted=False)).count()
            if is_exists >0 :
                return {'status': False, 'msg': DriverRegistrationMsgMod.Msg(lang, 'phone_number_already_reg')}
            else:
                return {'status': True}
        except Exception as e:
            return {'status': False, 'msg': GenericMsgMod.Msg(lang, 'error-msg')}
    parser_classes = (MultiPartParser,)
    @transaction.atomic
    def post(self, request):
        lang = request.data['langC']
        try:
            get_unique_phone = self.get_unique_phone(request)
            get_unique_email = self.get_unique_email(request)
            if not fieldEmptyCheck(request.data.get('first_name')) :
                return Response({"status" : False,"msg" :  DriverRegistrationMsgMod.Msg(lang, 'first_name'),
                 "data" : dict()})
            elif not fieldEmptyCheck(request.data.get('last_name')) :
                return Response({"status" : False,"msg" :  DriverRegistrationMsgMod.Msg(lang, 'last_name'),
                 "data" : dict()})
            elif not get_unique_phone['status']:
                return Response({"status" : False,"msg" :  get_unique_phone['msg'],
                 "data" : dict()})
            # elif not get_unique_email['status']:
            #     return Response({"status" : False,"msg" :  get_unique_email['msg'],
            #      "data" : dict()})
            # elif not fieldEmptyCheck(request.data.get('gender')) :
            #   return Response({"status" : False,"msg" :  DriverRegistrationMsgMod.Msg(lang, 'gender'),
            #    "data" : dict()})
            # elif not fieldEmptyCheck(request.data.get('dob')) :
            #   return Response({"status" : False,"msg" :  DriverRegistrationMsgMod.Msg(lang, 'dob'),
            #    "data" : dict()})
            elif not fieldEmptyCheck(request.data.get('password')) :
                return Response({"status" : False,"msg" :  DriverRegistrationMsgMod.Msg(lang, 'password'),
                 "data" : dict()})
            elif not fieldEmptyCheck(request.data.get('confirm_password')) :
                return Response({"status" : False,"msg" :  DriverRegistrationMsgMod.Msg(lang, 'confirm_password'),
                 "data" : dict()})
            elif request.data.get('confirm_password') != request.data.get('password'):
                return Response({"status" : False,"msg" :  DriverRegistrationMsgMod.Msg(lang, 'wrong_confirm_password'),
                 "data" : dict()})
            elif not fieldEmptyCheck(request.data.get('isd_code')) :
                return Response({"status" : False,"msg" :  DriverRegistrationMsgMod.Msg(lang, 'isd_code'),
                 "data" : dict()})
            elif not fieldEmptyCheck(request.data.get('country_id')) :
                return Response({"status" : False,"msg" :  DriverRegistrationMsgMod.Msg(lang, 'country_id'),
                 "data" : dict()})
            else:
                random_code = self.randomPassword( request )
                request.POST._mutable = True
                request.data['password'] = str(encrypt_val(request.data.get('password')))
                request.data['verification_code'] = random_code
                request.POST._mutable = False
                phoneNoWithISD = request.data.get('isd_code') + request.data.get('phone_number')
                msg = "Your Need Deliver verification code is " + random_code + "."
                ndUsersInstance = NdUsers(country_id =int(request.data.get('country_id')), role_id=settings.IS_DRIVER)
                ndDriverDetailsSaveSE = NdDriverDetailsSaveSE(ndUsersInstance, data=request.data)
                if ndDriverDetailsSaveSE.is_valid():
                    ndDriverDetailsSaveSE.save()
                else:
                    return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'error-msg'),
                 "data" : dict()})
                isMsgSend = sendGenericMessage( phoneNoWithISD, msg )
                return Response({"status" : True,"msg":DriverRegistrationMsgMod.Msg(lang, 'success-msg'),
                    "data" : dict(), 'otp':random_code })
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), 
                "data" : dict()})
class DriverLogin(APIView):
    def sendPushToOlderLoggedInUser(self, request, customParam, dataFields):
        userIDS = dataFields['userIDS']
        if dataFields['deviceIDS']:
            deviceIDS = dataFields['deviceIDS']
        pushNotificationFCM.send_push_notification( deviceIDS, userIDS, 
            {"title": dataFields['title'], "body": dataFields['body'], "notification_type_id" : 4}, customParam)
        return True
    def randomPassword( self, request ):
        # return "1111"
        random_code = get_random_string(length=4, allowed_chars='123456789')
        randomKeycheck = NdUsers.objects.filter(verification_code=random_code, is_deleted=False).count()
        if randomKeycheck >0 :
            self.randomPassword( request )
        else:
            return random_code
    def validationAndDataReturn(self, request):
        lang = request.data['langC']
        
        password = encrypt_val(request.data.get('password'))
        record = NdUsers.objects.filter(phone_number=request.data.get('phone_number'), role_id=settings.IS_DRIVER, password=password)
        if record.count()>0:
            record1= record.order_by('-id')
            recordObj = NdUsersLoginSE(record1.first(), many=False)
            print("ddddddddddddddddddddddddddd",str(recordObj.data['id']))
            if recordObj.data['is_phone_no_verified']:
                print(423423423)
                uniqueUUID = generateUID()
                print("++++++++++++++++++++",uniqueUUID)
                # record.update(device_uuid=uniqueUUID)
                if not recordObj.data['is_status']:
                    return {"status": False, "msg": DriverLoginMsgMod.Msg(lang, 'deactivated'), "data":dict(), 
                'device_uuid' : "", 'verify_status': True}
                elif recordObj.data['is_deleted']:
                    return {"status": False, "msg": DriverLoginMsgMod.Msg(lang, 'deleted'), "data":dict(), 
                    'device_uuid' : "", 'verify_status': True}
                else:
                    record.filter(is_deleted=False, is_status=True).update(device_uuid=uniqueUUID)
                    return {"status": True, "msg": DriverLoginMsgMod.Msg(lang, 'success-msg'), "data":recordObj.data, 
                    'device_uuid' : uniqueUUID, 'verify_status': True}
            
            else:
                if not recordObj.data['is_status']:
                    return {"status": False, "msg": DriverLoginMsgMod.Msg(lang, 'deactivated'), "data":dict(), 
                'device_uuid' : "", 'verify_status': True}
                elif recordObj.data['is_deleted']:
                    return {"status": False, "msg": DriverLoginMsgMod.Msg(lang, 'deleted'), "data":dict(), 
                    'device_uuid' : "", 'verify_status': True}
                
                phone_no = request.data.get('phone_number')
                firstChar =  phone_no[0]
                
                if firstChar == '0':
                    phone_no = phone_no.lstrip('0')
                random_code = self.randomPassword( request )
                record.update(verification_code=random_code)
                client.publish(
                        PhoneNumber=recordObj.data['country']['country_isd_code'] + phone_no,
                        Message="Your Need Deliver verification code is " + random_code + "."
                )
                return {"status": True, "msg": DriverLoginMsgMod.Msg(lang, 'phone_no_not_verified'), "data": recordObj.data,
                 'device_uuid':"", 'verify_status': False }
        else:
            return {"status": False, "msg": DriverLoginMsgMod.Msg(lang, 'wrong_credential'), "data": dict(), "device_uuid":""}
    def post(self, request, format=None):
        lang = request.data['langC']
        # request.POST._mutable = True
        # try:
            # phone_no = request.data.get('phone_number')
            # firstChar =  phone_no[0]
            
            # if firstChar == '0':
            #     phone_no = phone_no.lstrip('0')
            # request.data['phone_number'] = phone_no
        if not fieldEmptyCheck(request.data.get('phone_number')) :
            return Response({"status" : False,"msg" :  DriverLoginMsgMod.Msg(lang, 'phone_number')})
        elif not fieldEmptyCheck(request.data.get('password')) :
            return Response({"status" : False,"msg" :  DriverLoginMsgMod.Msg(lang, 'password')})
        else:
            validation = self.validationAndDataReturn(request)
            if not validation['status']:
                return Response({"status": False, "msg":validation['msg'], "data": validation['data'], 
                    'device_uuid': validation['device_uuid']})
            else:
                if not validation['verify_status']:
                    return Response({"status": True, "msg":validation['msg'], "data": validation['data'], 
                        'device_uuid': validation['device_uuid'], 'is_document_attached': is_document_upload_pending(validation['data']['id'])})
                if fieldEmptyCheck(validation['data']['device_token']) and request.data.get('device_token') != validation['data']['device_token']:
                    title = 'Login Expired'
                    body = "Your current logged in session has expired."
                    deviceIDS = [validation['data']['device_token']]
                    userIDS = [validation['data']['id']]
                    dataFields = {"title":title, "body":body, "deviceIDS":deviceIDS, "userIDS":userIDS }    
                    customParam = {}
                    customParam['push_type'] = settings.NOTIFICATION_TYPE['session_expired']
                    customParam['body'] = body
                    customParam['title'] = title
                    self.sendPushToOlderLoggedInUser(request, customParam, dataFields)    
                password = encrypt_val(request.data.get('password'))
                NdUsers.objects.filter(phone_number=request.data.get('phone_number'), role_id=settings.IS_DRIVER, password=password).update(
                    device_token=request.data.get('device_token'))
                return Response({"status": True, "msg":validation['msg'], "data": validation['data'], 
                    'device_uuid': validation['device_uuid'], 'is_document_attached': is_document_upload_pending(validation['data']['id'])})
        # except Exception as e:
        #     return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), 
        #         "data" : dict()})

class DriverAndVehicleDocuments(APIView):
    parser_classes = (MultiPartParser,)
    tmpSaveData = []
    @transaction.atomic
    def post(self, request):
        self.tmpSaveData = list()
        lang = request.data['langC']
        # try:
        loggedInStatus = get_latest_device_uuid_by_userid(int(request.POST.get('session_user_id')),
         request.POST.get('session_unique_uuid'))
        if not loggedInStatus:
            return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
             "data" : dict(), 'loggedInStatus' : loggedInStatus})
        if not fieldEmptyCheck(request.data.get('driver_id')) :
            return Response({"status" : False,"msg" :  DriverAndVehicleDocumentsMsgMod.Msg(lang, 'driver_id'),
             "data" : dict(), 'loggedInStatus' : loggedInStatus})
        else:
            # print(str(request.FILES['vehicle_image']))
            # return Response({"status" : True,"msg":str(request.FILES['vehicle_image']), "data" : dict(),
             # 'loggedInStatus' : loggedInStatus})
            is_already_added = NdVehicleDetails.objects.filter(user_id=int(request.data.get('driver_id')))
            if is_already_added.count()>0:
                return Response({"status" : False,"msg" :  DriverAndVehicleDocumentsMsgMod.Msg(lang, 'already_added'),
                        "data" : dict(), 'loggedInStatus' : loggedInStatus})
            tmpObjTipeArray = {}
            attachmentObjTypes = NdObjectTypeModel.objects.filter(is_status=True, is_deleted=False)
            if attachmentObjTypes.count()>0:
                attachmentObjTypes = attachmentObjTypes.values('id', 'object_name')
                for item in attachmentObjTypes:
                    tmpObjTipeArray[item['object_name']] = item['id']
            tmpAttachedArray = []
            for count, driving_licence_file in enumerate(request.FILES.getlist("driving_licence")):
                if tmpObjTipeArray['driving_licence']:
                    driving_licence_obj = NdAttachments(attached_file=driving_licence_file, user_id=int(request.data.get('driver_id')), 
                        object_type_id=int(tmpObjTipeArray['driving_licence']))
                    # driving_licence_obj.save()
                    self.tmpSaveData.append(driving_licence_obj)
            for count, vehicle_registration_file in enumerate(request.FILES.getlist("vehicle_registration")):
                if tmpObjTipeArray['vehicle_registration']:
                    vehicle_registration_obj = NdAttachments(attached_file=vehicle_registration_file, user_id=int(request.data.get('driver_id')), 
                        object_type_id=int(tmpObjTipeArray['vehicle_registration']))
                    self.tmpSaveData.append(vehicle_registration_obj)
            for count, vehicle_insurance_file in enumerate(request.FILES.getlist("vehicle_insurance")):
                if tmpObjTipeArray['vehicle_insurance']:
                    vehicle_insurance_obj = NdAttachments(attached_file=vehicle_insurance_file, user_id=int(request.data.get('driver_id')), 
                        object_type_id=int(tmpObjTipeArray['vehicle_insurance']))
                    self.tmpSaveData.append(vehicle_insurance_obj)
            # for count, vehicle_image_file in enumerate(request.FILES.getlist("vehicle_image")):
            #   if tmpObjTipeArray['vehicle_image']:
            #       vehicle_image_obj = NdAttachments(attached_file=vehicle_image_file, user_id=int(request.data.get('driver_id')), 
            #           object_type_id=int(tmpObjTipeArray['vehicle_image']))
            #       self.tmpSaveData.append(vehicle_image_obj)
            if self.tmpSaveData:
                NdAttachments.objects.bulk_create(self.tmpSaveData)
            ndDriverDetailsObj = NdDriverDetails(driving_licence_expiry_date=request.data.get('driving_licence_expiry_date'),
                vehicle_type_id=int(request.data.get('vehicle_type')), user_id=int(request.data.get('driver_id')))
            ndDriverDetailsObj.save()
            defaultCityName = 'Phnom Penh'
            ndVehicleDetailsObj = NdVehicleDetails(registration_expiry_date=request.data.get('registration_expiry_date'),
                insurance_expiry_date=request.data.get('insurance_expiry_date'), plate_number=request.data.get('plate_number'),
                user_id=int(request.data.get('driver_id')), city=defaultCityName, vehicle_model_id=int(request.data.get('vehicle_model')),
                wheel_chair_support=request.data.get('wheel_chair_support'), booster_seat_support=request.data.get('booster_seat_support'),
                image_file=request.FILES['vehicle_image'], year=int(request.data.get('vehicle_year')))
            ndVehicleDetailsObj.save()
            return Response({"status" : True,"msg":DriverAndVehicleDocumentsMsgMod.Msg(lang, 'success-msg'), "data" : dict(),
             'loggedInStatus' : loggedInStatus})
        # except Exception as e:
        #   return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), 
        #       "data" : dict(), 'loggedInStatus' : True})
class AllVehicleModels(APIView):
    def post(self, request):
        lang = request.data['langC']
        try:
            ndVehicleModelInstance = NdVehicleModel.objects.filter(is_status=True, is_deleted=False, vehicle_type_id=int(request.data.get('vehicle_type')))
            if ndVehicleModelInstance.count()>0:
                ndVehicleTypeObj = ndVehicleModelInstance.values('id', 'model_name', 'vehicle_type_id')
                return Response({"status":True, "msg": AllVehicleModelsMsgMod.Msg(lang, 'found'), 
                    "data":ndVehicleTypeObj})
            else:
                return Response({"status":False, "msg": AllVehicleModelsMsgMod.Msg(lang, 'not-found'),
                 "data":dict()})
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict()})
class ForgotPassword(APIView):
    def randomPassword( self, request ):
        # return "1111"
        random_code = get_random_string(length=4, allowed_chars='123456789')
        randomKeycheck = NdUsers.objects.filter(random_key=random_code, is_deleted=False).count()
        if randomKeycheck >0 :
            self.randomPassword( request )
        else:
            return random_code
    @transaction.atomic
    def post(self, request):
        lang = request.data['langC']
        try:
            random_code = self.randomPassword( request )
            record = NdUsers.objects.filter(phone_number=request.data.get('phone_number'), role_id=settings.IS_DRIVER, is_deleted=False)
            if record.count()>0:
                recordObj = record.values('country__country_isd_code', 'is_status').first()
                if not recordObj['is_status']:
                    return Response({"status":False, "msg": ForgotPasswordMsgMod.Msg(lang, 'account_deactivated'),
                         "data":dict()})
                phone_no = request.data.get('phone_number')
                firstChar =  phone_no[0]
                
                if firstChar == '0':
                    phone_no = phone_no.lstrip('0')
                record.update(random_key=random_code)
                client.publish(
                        PhoneNumber=recordObj['country__country_isd_code'] + phone_no,
                        Message="Your Need Deliver password reset verification code is " + random_code + "."
                )
                return Response({"status":True, "msg": ForgotPasswordMsgMod.Msg(lang, 'OTP-send'),
                         "data":dict()})
            else:
                return Response({"status":False, "msg": ForgotPasswordMsgMod.Msg(lang, 'not-found'),
                         "data":dict()})
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict()})
    def patch(self, request, pk=None):
        lang = request.data['langC']
        try:
            if not fieldEmptyCheck(request.data.get('password')) :
                return Response({"status" : False,"msg" :  ForgotPasswordMsgMod.Msg(lang, 'password'),
                 "data" : dict()})
            elif not fieldEmptyCheck(request.data.get('confirm_password')) :
                return Response({"status" : False,"msg" :  ForgotPasswordMsgMod.Msg(lang, 'confirm_password'),
                 "data" : dict()})
            elif request.data.get('password') != request.data.get('confirm_password') :
                return Response({"status" : False,"msg" :  ForgotPasswordMsgMod.Msg(lang, 'confirm_not_match'),
                 "data" : dict()})
            else:
                record = NdUsers.objects.filter(phone_number=request.data.get('phone_number'), role_id=settings.IS_DRIVER,
                    random_key=request.data.get('verification_code'))
                if record.count()>0:
                    recordDetails = record
                    recordDetailObj = record.values('country__country_isd_code').first()
                    password = str(encrypt_val(request.data.get('password')))
                    recordObj = NdUsersLoginSE(recordDetails.first(), many=False)
                    record.update(random_key=None, password=password)
                    phone_no = request.data.get('phone_number')
                    firstChar =  phone_no[0]
                    
                    if firstChar == '0':
                        phone_no = phone_no.lstrip('0')
                    # record.update(random_key=random_code)
                    client.publish(
                            PhoneNumber=recordDetailObj['country__country_isd_code'] + phone_no,
                            Message="Need Deliver credential has been changed. If you did not then please reset your password."
                    )
                    
                    return Response({"status":True, "msg": ForgotPasswordMsgMod.Msg(lang, 'password-changed'),
                             "data":recordObj.data})
                else:
                    return Response({"status":False, "msg": ForgotPasswordMsgMod.Msg(lang, 'not-found'),
                             "data":dict()})
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict()})
class ForgotPasswordOTPVerify(APIView):
    def post(self, request):
        lang = request.data['langC']
        try:
            record = NdUsers.objects.filter(phone_number=request.data.get('phone_number'), role_id=settings.IS_DRIVER,
                random_key=request.data.get('verification_code'))
            if record.count()>0:
                return Response({"status":True, "msg": ForgotPasswordMsgMod.Msg(lang, 'OTP-match'), "data":dict()})
            else:
                return Response({"status":False, "msg": ForgotPasswordMsgMod.Msg(lang, 'OTP-not-match'), "data":dict()})
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict()})
#---------------------------------------------------------- Delivery Acknowledgement --------------------------------------------------------------------#
class DeliveryAcknowledgement(APIView):
    def commissionDeduction(self, driver_id, amount):
        driverDetails = NdDriverDetails.objects.filter(user_id=int(driver_id)).values('account_balance').first()
        print(str(driverDetails))
        commission = NdSettings.objects.filter(field_name__icontains="Commission( % )", is_status=True, is_deleted=False).values('field_val').first()
        # try:
        comDivide = float(commission['field_val'])/100.00
        print("yyyyyyyyyy", str(comDivide))
        commission = float(comDivide) * float(amount)
        print("fffffff", str(commission))
        # deductedAmt = float(driverDetails['account_balance']) - commission
        deductedAmt = "{0:.2f}".format(commission)
        
        return commission
        # except deductedAmt as e:
        #     print("fdfgdfgdfg", str(amount))
        #     return amount

        float(tota)*(100.0/500.0)
    def push_send(self, request, customParam, dataFields):
        userIDS = dataFields['userIDS']
        
        if dataFields['deviceIDS']:
            deviceIDS = dataFields['deviceIDS']
            pushNotificationFCM.send_push_notification( deviceIDS, userIDS, 
            {"title": dataFields['title'], "body": dataFields['body'], "notification_type_id" : 4}, customParam)
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
    # @transaction.atomic
    def post(self, request):
        lang = request.data['langC']
        # try:
        loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
         request.data.get('session_unique_uuid'))
        
        if not loggedInStatus:
            return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
             "data" : dict(), 'loggedInStatus' : loggedInStatus})
        elif not fieldEmptyCheck(request.data.get('driver_id')):
            return Response({"status":False, "msg":DeliveryAcknowledgementMsgMod.Msg(lang, 'driver_id'),
             "data" : dict()})
        elif not fieldEmptyCheck(request.data.get('location_type')):
            return Response({"status":False, "msg":DeliveryAcknowledgementMsgMod.Msg(lang, 'location_type'),
             "data" : dict()})
        elif not fieldEmptyCheck(request.data.get('latitude')):
            return Response({"status":False, "msg":DeliveryAcknowledgementMsgMod.Msg(lang, 'latitude'),
             "data" : dict()})
        elif not fieldEmptyCheck(request.data.get('longitude')):
            return Response({"status":False, "msg":DeliveryAcknowledgementMsgMod.Msg(lang, 'longitude'),
             "data" : dict()})
        else: 
            bookingStatus = NdOrder.objects.filter(id=int(request.data.get('order_id'))).values('booking_status')
            if bookingStatus.count():
                bookingStatus = bookingStatus.first()
                if bookingStatus['booking_status'] == settings.BOOKING_STATUS_CANCELLED:
                    return Response({"status" : False,"msg" :  DeliveryAcknowledgementMsgMod.Msg(lang, 'already_cancelled'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})   
                elif bookingStatus['booking_status'] == settings.BOOKING_STATUS_COMPLETED:
                    return Response({"status" : False,"msg" :  DeliveryAcknowledgementMsgMod.Msg(lang, 'already_completed'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})     
            NdOrderCompletionDetails.objects.filter(order_id=int(request.data.get('order_id')),location_type=int(request.data.get('location_type'))).delete()

            arrivalStatus = NdOrderCompletionDetails.objects.filter(order_id=int(request.data.get('order_id')),
            location_type=int(request.data.get('location_type')))

            # if arrivalStatus.exists():
            #     return Response({"status":False, "msg":DeliveryAcknowledgementMsgMod.Msg(lang, 'already_arrived'),
            #  "data" : dict()})
            startLat = None
            startLong = None
            if int(request.data.get('location_type')) == 1:
                pickUpLocationObj = NdOrder.objects.filter(id=int(request.data.get('order_id'))).values('latitude', 'longitude').first()
                startLat = pickUpLocationObj['latitude']
                startLong = pickUpLocationObj['longitude']
            else:
                ndOrderCompletionDetailsData = NdOrderCompletionDetails.objects.filter(order_id=int(request.data.get('order_id')),
                    location_type=1).values('latitude', 'longitude').first()
                startLat = ndOrderCompletionDetailsData['latitude']
                startLong = ndOrderCompletionDetailsData['longitude']

            # distance = self.vehicles_within_range(startLat, startLong, request.data.get('latitude'), request.data.get('longitude'))
            NdOrderCompletionDetails.objects.filter(id=int(request.data.get('order_id')),location_type=int(request.data.get('location_type'))).delete()

            distance = request.data.get('actual_distance')
            distance = distance.replace(",", '.', 1)
            ndOrderCompletionDetailsObj = NdOrderCompletionDetails(latitude=request.data.get('latitude'), longitude=request.data.get('longitude'),
            order_id=int(request.data.get('order_id')), location_type=int(request.data.get('location_type')), actual_distance=distance)
            ndOrderCompletionDetailsObj.save()  
            dataForFirstDropLoc = list()
            dataForsecondDropLoc = list()
            packageDetails = NdDropOffLocation.objects.filter(order_id=int(request.data.get('order_id'))).values('item_name', "location",
             "order__supplier__device_token", "order__supplier__id", "order__order_uid")
            # print(str(packageDetails))
            if packageDetails.count() >1:
                dataForFirstDropLoc = packageDetails[0]
                dataForsecondDropLoc = packageDetails[1]
            else:
                dataForFirstDropLoc = packageDetails[0]
            _firstDropItemName = "No Item Name"
            if fieldEmptyCheck(dataForFirstDropLoc['item_name']):
                _firstDropItemName = dataForFirstDropLoc['item_name']
            # print("%%%%%%%%%%%%%", packageDetails.count())
            title = 'Delivered: '+ str(_firstDropItemName) + ' at your dropping location'
            
            
            if packageDetails.count() >=2:
                title = 'Delivered: '+ str(_firstDropItemName) + ' at first dropping location'
            body = "Order ID: #"+ str(dataForFirstDropLoc['order__order_uid']) + "\n" + "Location: "+ str(dataForFirstDropLoc['location'])
            if int(request.data.get('location_type')) == 2: 
                _secondDropItemName = "No Item Name"
                if fieldEmptyCheck(dataForsecondDropLoc['item_name']):
                    _secondDropItemName = dataForsecondDropLoc['item_name']
                title = 'Delivered: '+ str(_secondDropItemName ) + ' at second dropping location'
                body = "Order ID: #"+ str(dataForsecondDropLoc['order__order_uid']) + "\n" + "Pickup From: "+ str(dataForsecondDropLoc['location'])
            deviceIDS = [dataForFirstDropLoc['order__supplier__device_token']]
            userIDS = [dataForFirstDropLoc['order__supplier__id']]
            dataFields = {"title":title, "body":body, "deviceIDS":deviceIDS, "userIDS":userIDS }    
            customParam = {}
            customParam['push_type'] = settings.NOTIFICATION_TYPE['arrived_first_drop']
            customParam['body'] = body
            customParam['title'] = title
            if int(request.data.get('location_type')) == 2: 
                customParam['push_type'] = settings.NOTIFICATION_TYPE['arrived_second_drop']
            if fieldEmptyCheck(dataForFirstDropLoc['order__supplier__device_token']):
                self.push_send(request, customParam, dataFields)

            msg = DeliveryAcknowledgementMsgMod.Msg(lang, 'dropped_at_first_location')
            if int(request.data.get('location_type')) == 2:
                msg = DeliveryAcknowledgementMsgMod.Msg(lang, 'dropped_at_second_location')
            return Response({'status':True, 'msg':msg, "data":dict()})
        # except Exception as e:
        #   return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict()})
    # @transaction.atomic
    def patch(self, request, pk):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
             request.data.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
                     "data" : dict(), 'loggedInStatus' : loggedInStatus})
            else:

                nowTime = timezone.now() 
                actual_distance = request.data.get('actual_distance')
                actual_distance = actual_distance.replace(",", '.', 1)
                totalDistance = float(actual_distance) 
                costCalculated = 0
                getOrderDetails = NdOrder.objects.filter(id=int(pk)).values('base_price', 'distance', 'booking_time' ).first()
                costCalculated = distanceCalculation(actual_distance, int(pk))
              
                       
                diff = (nowTime - getOrderDetails['booking_time']).total_seconds()
                # difInMin =  diff / 60.0
                    
                # print("Difference:", type(getOrderDetails['booking_time']))
                # print("Days:", minutes_diff )
                # print("Microseconds:", diff.microseconds)
                # print("Seconds:", diff.seconds)
                # return Response({'status':33, 'msg':DeliveryAcknowledgementMsgMod.Msg(lang, 'trip_completed'), "data":dict()})
                # For Grand total by Ishita
                orderInstance = NdOrder.objects.filter(id=int(pk), driver_id__isnull=False)
                if orderInstance.count()>0:
                    orderObj = OrderDetailsSE(orderInstance.first(), many=False, context = { 'currentLang': lang })
                # For Grand total by Ishita
     
                NdOrder.objects.filter(id=int(pk)).update(distance=float(totalDistance), booking_status=settings.BOOKING_STATUS_COMPLETED,
                 delivery_time=nowTime, total_time_taken=diff, base_price=float(costCalculated))
                orderDetailsObj = NdOrder.objects.filter(id=int(pk)).values('supplier__phone_number', 'supplier__country__country_isd_code', 
                    'order_uid', "driver_id", 'supplier__device_token', 'supplier_id', "location").first()

                supplier_phone_no = orderDetailsObj['supplier__country__country_isd_code'] + orderDetailsObj['supplier__phone_number']
                NdUsersObjects.objects.filter(user_id=orderDetailsObj['driver_id']).update(is_available=True)
                msg = "Delivered: Your parcel #"+ str(orderDetailsObj['order_uid']) + " from Need Deliver was delivered successfully. "+"Grand Total: "+ str(orderObj.data['converted_price']['convertedAmount'])+""+str(orderObj.data['converted_price']['currency'])
                isMsgSend = sendGenericMessage( supplier_phone_no, msg )
                convertedPrice = calculationCurrencyConversionWithPresentCur(costCalculated, 'km-KH', lang)  
                deductionAfterCommission = self.commissionDeduction(orderDetailsObj['driver_id'], costCalculated)
                
                NdDriverDetails.objects.filter(user_id=orderDetailsObj['driver_id']).update(account_balance=F('account_balance') -  deductionAfterCommission)
                title = "Parcel Delivered"
                body = "Order ID: "+ str(orderDetailsObj['order_uid']) +"\n"+ "Pickup Location: "+orderDetailsObj['location']
                if fieldEmptyCheck(orderDetailsObj['supplier__device_token']):
                    deviceIDS = [orderDetailsObj['supplier__device_token']]
                    userIDS = [orderDetailsObj['supplier_id']]
                    dataFields = {"title":title, "body":body, "deviceIDS":deviceIDS, "userIDS":userIDS }    
                    customParam = {}
                    customParam['push_type'] = settings.NOTIFICATION_TYPE['trip_completed']
                    customParam['body'] = body
                    customParam['title'] = title
                    self.push_send(request, customParam, dataFields)

                return Response({'status':True, 'msg':DeliveryAcknowledgementMsgMod.Msg(lang, 'trip_completed'), "data":dict()})
        except Exception as e:
          return Response({'status':True, 'msg':GenericMsgMod.Msg(lang, 'error-msg'), "data":dict()})
#------------------------------------------------------- Pickup location set --------------------------------------------------------------#
class PickupLocationArrived(APIView):
    def push_send(self, request, customParam, dataFields):
        userIDS = dataFields['userIDS']
        if dataFields['deviceIDS']:
            deviceIDS = dataFields['deviceIDS']
        pushNotificationFCM.send_push_notification( deviceIDS, userIDS, 
            {"title": dataFields['title'], "body": dataFields['body'], "notification_type_id" : 4}, customParam)
        return True
    # @transaction.atomic
    def post(self, request):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
             request.data.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})

            elif not fieldEmptyCheck(request.data.get('driver_id')):
                return Response({"status":False, "msg":DeliveryAcknowledgementMsgMod.Msg(lang, 'driver_id'),
                 "data" : dict()})
            elif not fieldEmptyCheck(request.data.get('latitude')):
                return Response({"status":False, "msg":DeliveryAcknowledgementMsgMod.Msg(lang, 'latitude'),
                 "data" : dict()})
            elif not fieldEmptyCheck(request.data.get('longitude')):
                return Response({"status":False, "msg":DeliveryAcknowledgementMsgMod.Msg(lang, 'longitude'),
                 "data" : dict()})
            else:   
                bookingStatus = NdOrder.objects.filter(id=int(request.data.get('order_id'))).values('booking_status')
                if bookingStatus.count():
                    bookingStatus = bookingStatus.first()
                    if bookingStatus['booking_status'] == settings.BOOKING_STATUS_CANCELLED:
                        return Response({"status" : False,"msg" :  DeliveryAcknowledgementMsgMod.Msg(lang, 'already_cancelled'),
                     "data" : dict(), 'loggedInStatus' : loggedInStatus})   
                    elif bookingStatus['booking_status'] == settings.BOOKING_STATUS_COMPLETED:
                        return Response({"status" : False,"msg" :  DeliveryAcknowledgementMsgMod.Msg(lang, 'already_completed'),
                     "data" : dict(), 'loggedInStatus' : loggedInStatus})
                arrivalStatus = NdOrderCompletionDetails.objects.filter(order_id=int(request.data.get('order_id')),  
                location_type=0)
                if arrivalStatus.exists():
                    return Response({"status":True, "msg":DeliveryAcknowledgementMsgMod.Msg(lang, 'already_arrived'),
                 "data" : dict()})

                pickUpLocationObj = NdOrder.objects.filter(id=int(request.data.get('order_id'))).values('latitude', 'longitude', 'order_uid', 'id',
                    'supplier__device_token', 'supplier__id', 'location', 'coupon_id').first()
                
                ndOrderCompletionDetailsObj = NdOrderCompletionDetails(latitude=request.data.get('latitude'), longitude=request.data.get('longitude'),
                order_id=int(request.data.get('order_id')), location_type=0)
                ndOrderCompletionDetailsObj.save()  
                NdOrder.objects.filter(id=int(request.data.get('order_id'))).update(booking_time=current_date_time())
                if fieldEmptyCheck(pickUpLocationObj['coupon_id']):
                    NdAppliedCoupons.objects.filter(id=pickUpLocationObj['coupon_id']).update(is_deleted=True)
                title = 'Arrived: Driver arrived at pickup location'
                body = "Order ID: #"+ str(pickUpLocationObj['order_uid']) + "\n" + "Location: "+ str(pickUpLocationObj['location'])
                # print("pick-----------------",pickUpLocationObj['supplier__device_token'])  
                if fieldEmptyCheck(pickUpLocationObj['supplier__device_token']):
                    deviceIDS = [pickUpLocationObj['supplier__device_token']]
                    userIDS = [pickUpLocationObj['supplier__id']]
                    dataFields = {"title":title, "body":body, "deviceIDS":deviceIDS, "userIDS":userIDS }    
                    customParam = {}
                    customParam['push_type'] = settings.NOTIFICATION_TYPE['arrived_at_pickup']
                    customParam['body'] = body
                    customParam['title'] = title
                    self.push_send(request, customParam, dataFields)
                return Response({'status':True, 'msg':DeliveryAcknowledgementMsgMod.Msg(lang, 'arrived_pickup_location'), "data":dict()})
        except Exception as e:
          return Response({'status':True, 'msg':msg, "data":dict()})          
class BookingRequestsByDriver(APIView):
    def post(self, request):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
             request.data.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
             "data" : dict(), 'loggedInStatus' : loggedInStatus})
            record = NdBookingRequests.objects.filter(is_deleted=False, driver_id=int(request.data.get('driver_id'))).order_by('-id')
            if record.count()>0:
                recordObj = NdBookingRequestsSe(record, many=True, context={ 'currentLang': lang} )
                return Response({"status":True, "msg": BookingRequestsByDriverMsgMod.Msg(lang, 'fetched'), "data":recordObj.data, 'loggedInStatus' : loggedInStatus})
            else:
                return Response({"status":False, "msg": BookingRequestsByDriverMsgMod.Msg(lang, 'no_booking'), "data":dict(), 'loggedInStatus' : loggedInStatus})
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict(), 'loggedInStatus' : True})
class TempDriverStatusChange(APIView):
    def post(self, request):
        NdUsersObjects.objects.filter(user_id=int(request.data.get('user_id'))).update(is_available=True)
        return Response({"status":True, "msg": ""})

class ChecKOnGoingBooking(APIView):
    def post(self, request):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
             request.data.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
             "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('driver_id')):
                return Response({"status":False, "msg":GenericMsgMod.Msg(lang, 'error-msg'),
                 "data" : dict()})
            else:
                OrderStatus = NdOrder.objects.filter(booking_status=settings.BOOKING_STATUS_PROCESSING, driver_id=int(request.data.get('driver_id')))
                if OrderStatus.exists():
                    OrderStatusObj =  OrderStatus.values('id', 'supplier_id').first()
                    OrderCompletionDetails = NdOrderCompletionDetails.objects.filter(order_id=OrderStatusObj['id'])
                    aheadLocation = 1
                    if OrderCompletionDetails.count() == 1:
                        aheadLocation = 2
                    elif OrderCompletionDetails.count() == 2:
                        aheadLocation = 3
                    return Response({"status":True, "msg":GenericMsgMod.Msg(lang, 'data-fetched'), "data" : OrderStatusObj, 
                        'location_ahead': aheadLocation})
                return Response({"status":False, "msg":GenericMsgMod.Msg(lang, 'data-not-found'), "data" : dict()}) 
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict()})
class BookingHistoryWithPagination(APIView):
    def post(self, request):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
             request.data.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
             "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('driver_id')):
                return Response({"status":False, "msg":GenericMsgMod.Msg(lang, 'error-msg'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            else:
                orderDetails = NdOrder.objects.filter(driver_id=int(request.data.get('driver_id')))
                if fieldEmptyCheck(request.data.get('start_date')) and fieldEmptyCheck(request.data.get('end_date')): 
                    orderDetails = orderDetails.filter(booking_time__range=[request.data.get('start_date'), request.data.get('end_date')] )
                elif fieldEmptyCheck(request.data.get('start_date')):
                    startDate = datetime.datetime.strptime(request.data.get('start_date'), "%Y-%m-%d").date()
                    orderDetails = orderDetails.filter(booking_time__year=startDate.year, booking_time__month=startDate.month, booking_time__day=startDate.day, )
                    # post_date__year=today.year,
                    #            post_date__month=today.month,
                    #            post_date__day=today.day   
                try:
                    orderDetailObj = orderDetails.order_by('-id')
                    page = request.data.get('start',1)
                    paginator = Paginator(orderDetailObj, settings.FRONT_END_NO_OF_RECORD)
                    orderDetailObj = paginator.page(int(page))

                except EmptyPage:   
                    return Response({'status':False, 'data':dict(), 'msg':GenericMsgMod.Msg(lang, 'data-not-found'), 
                        'total_record': orderDetails.count(), 'loggedInStatus' : loggedInStatus})
                orderDetailsForHistorySE = OrderDetailsForHistorySE(orderDetailObj, many=True, context={ 'currentLang': lang })
                return Response({"status":True, "msg":GenericMsgMod.Msg(lang, 'data-fetched'),
                 "data" : orderDetailsForHistorySE.data, 'total_record': orderDetails.count(),'loggedInStatus' : loggedInStatus })
        except Exception as e:
          return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict()})
class CompleteBookingByDriver(APIView):
    def push_send(self, request, customParam, dataFields):
        userIDS = dataFields['userIDS']
        if dataFields['deviceIDS']:
            deviceIDS = dataFields['deviceIDS']
        pushNotificationFCM.send_push_notification( deviceIDS, userIDS, 
            {"title": dataFields['title'], "body": dataFields['body'], "notification_type_id" : 4}, customParam)
        return True
    @transaction.atomic
    def post(self, request):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
                 request.data.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
             "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('order_id')):
                return Response({"status":False, "msg":CancelBookingByDriverMsgMod.Msg(lang, 'order_id'),
                 "data" : dict()})
            else:
                orderDetails =  NdOrder.objects.filter(id=int(request.data.get('order_id')), booking_status=settings.BOOKING_STATUS_PLACED)
                if orderDetails.exists():
                    ObjectCompleteObj = NdOrderCompletionDetails.objects.filter(order_id=int(request.data.get('order_id')))
                    location_type = ObjectCompleteObj.count() + 1
                    pickUpLocationObj = NdOrder.objects.filter(id=int(request.data.get('order_id'))).values('latitude', 'longitude', 'order_uid', 'id',
                        'supplier__device_token', 'supplier__id', 'supplier__phone_number', 'driver_id', 'supplier__country__country_isd_code', 'location', 'base_price', 'distance', 'booking_time').first()
                    
                    ndOrderCompletionDetailsObj = NdOrderCompletionDetails(latitude=request.data.get('latitude'), longitude=request.data.get('longitude'),
                    order_id=int(request.data.get('order_id')), location_type=location_type)
                    ndOrderCompletionDetailsObj.save()  
                    totalDistance = float(request.data.get('actual_distance')) 
                    costCalculated = distanceCalculation(request.data.get('actual_distance'), int(request.data.get('order_id')))
                    nowTime = timezone.now() 
                    diff = nowTime - pickUpLocationObj['booking_time']
                    seconds = diff.seconds 
                    NdOrder.objects.filter(id=int(request.data.get('order_id'))).update(total_time_taken=seconds, base_price=costCalculated,
                        booking_status=settings.BOOKING_STATUS_COMPLETED, delivery_time=nowTime)
                    NdUsersObjects.objects.filter(user_id=pickUpLocationObj['driver_id']).update(is_available=True)
                    msg = "Parcel Dropped: Your parcel #"+ str(pickUpLocationObj['order_uid']) + " from Need Deliver was dropped before completing full trip"
                    supplier_phone_no = pickUpLocationObj['supplier__country__country_isd_code']+pickUpLocationObj['supplier__phone_number']
                    isMsgSend = sendGenericMessage( supplier_phone_no, msg )


                    NdDriverDetails.objects.filter(user_id=request.data.get('order_id')).update(account_balance=F('account_balance') - costCalculated)
                    title = "Parcel Dropped"
                    body = "Your parcel #"+ str(pickUpLocationObj['order_uid']) + " from Need Deliver was dropped before completing full trip"
                    deviceIDS = [pickUpLocationObj['supplier__device_token']]
                    userIDS = [pickUpLocationObj['supplier__id']]
                    dataFields = {"title":title, "body":body, "deviceIDS":deviceIDS, "userIDS":userIDS }    
                    customParam = {}
                    customParam['push_type'] = settings.NOTIFICATION_TYPE['trip_completed']
                    customParam['body'] = body
                    customParam['title'] = title
                    self.push_send(request, customParam, dataFields)
                    return Response({"status":True, "msg":CancelBookingByDriverMsgMod.Msg(lang, 'success-msg'),
                         "data" : dict()})
                else:
                    return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict()})
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict()})
class CalculateCostingAtAnyTime(APIView):
    def post(self, request):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
                 request.data.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
             "data" : dict(), 'loggedInStatus' : loggedInStatus})
            else:
                vahicleTypeDetailsObj = NdVehicleType.objects.filter(id=int(request.data.get('vehicle_type'))).values('base_fare', 'khr')
                if vahicleTypeDetailsObj.count()>0:
                    vahicleTypeDetails = vahicleTypeDetailsObj.first()
                    totalDistance = request.data.get('distance')
                    totalDistance = float(totalDistance) 
                    if not fieldEmptyCheck(vahicleTypeDetails['khr']) or not fieldEmptyCheck(vahicleTypeDetails['base_fare']):
                        return Response({'status':False,  'data':dist(), 'msg':CostCalculationMsgMod.Msg(lang, 'base_price'), 'loggedInStatus':True})
                    if float(totalDistance) > 1:
                        # print("base",vahicleTypeDetails['khr'])
                        restFare = float(vahicleTypeDetails['khr']) *(float(totalDistance)-1)
                        totalCharge  = float(vahicleTypeDetails['base_fare']) + restFare
                    else:
                        # print(str(vahicleTypeDetails['base_fare']) , "rrrrrrrrr" + str(float(totalDistance)))
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
                #   print(totalCharge)  
                    # if totalCharge<1:
                    #   totalCharge = 0.1
                    langReq = 'km-KH'
                    convertedRateObj = calculationCurrencyConversion(totalCharge, langReq)
                    totalCharge = "{0:.2f}".format(totalCharge)


                # #---------------------------------
                # totalDistance = float(request.data.get('distance')) 
                # getOrderDetails = NdOrder.objects.filter(id=int(request.data.get('order_id'))).values('base_price', 'distance', "currency_id", 'conversion_rate').first()
                # getUnitDistanceCosting = float(getOrderDetails['base_price'])/float(getOrderDetails['distance'])
                # costCalculated = getUnitDistanceCosting * totalDistance
                # costCalculated = "{0:.2f}".format(costCalculated)
                
                # langReq = 'km-KH'
                # convertedRateObj = calculateCurrentRateByLang(getOrderDetails['conversion_rate'], totalCharge, langReq)
                return Response({'status':True,  'data':dict(), 'totalCharge':totalCharge, 'msg':GenericMsgMod.Msg(lang, 'data-fetched'), 
                    'loggedInStatus':True, "currency": convertedRateObj['currency']})
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict()})

class CancelBookingByDriver(APIView):
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
            if is_already_deleted.count() >0 :
                return Response({"status":False, "msg": CancelBookingByDriverMsgMod.Msg(lang, 'already-deleted'),
                 "data":dict(), 'loggedInStatus':loggedInStatus})
            else:
                bookingDetailsObj = NdOrder.objects.filter(id=int(request.data.get('order_id'))).values("id", "order_uid", "supplier_id", "supplier__first_name",
                     "supplier__last_name", "supplier__profile_picture", "supplier__device_token", "location", "driver_id", "location")
                if bookingDetailsObj.count() == 0:
                    return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'error-msg'),
                     "data":dict(), 'loggedInStatus':loggedInStatus})
                bookingDetailsObj = bookingDetailsObj.first()
                # print(str(bookingDetailsObj['supplier_id']))
                ObjectCompleteObj = NdOrderCompletionDetails.objects.filter(order_id=int(request.data.get('order_id')))

                if ObjectCompleteObj.count()>0:
                    NdOrder.objects.filter(id=int(request.data.get('order_id'))).update(booking_status=settings.BOOKING_STATUS_CANCELLED)

                    ndCancelOrder = NdCancelOrder(supplier_id=int(bookingDetailsObj['supplier_id']), driver_id=int(request.data.get('driver_id')),
                         reason_id=int(request.data.get('reason_id')), order_id=int(request.data.get('order_id')), 
                         reason_description=sanitize(request.data.get('reason_description')), cancelled_by_id=int(request.data.get('driver_id')))
                    ndCancelOrder.save()
                    title = "Cancelled: Your trip  has been cancelled by the Supplier"
                    body = "Order ID: #"+ str(bookingDetailsObj['order_uid']) + "\n" + "Pickup From: "+ str(bookingDetailsObj['location'])

                    NdUsersObjects.objects.filter(user_id=int(request.data.get('driver_id'))).update(is_available=True)
                    deviceIDS = [bookingDetailsObj['supplier__device_token']]
                    userIDS = [bookingDetailsObj['supllier_id']]
                    dataFields = {"title":title, "body":body, "deviceIDS":deviceIDS, "userIDS":userIDS }    
                    customParam = {}
                    customParam['push_type'] = settings.NOTIFICATION_TYPE['cancelled_by_driver']
                    customParam['body'] = body
                    customParam['title'] = title
                    self.push_send(request, customParam, dataFields)
                else:
                    NdOrder.objects.filter(id=int(request.data.get('order_id'))).update(booking_status=settings.BOOKING_STATUS_CANCELLED)
                    ndCancelOrder = NdCancelOrder(supplier_id=bookingDetailsObj['supplier_id'], driver_id=int(request.data.get('driver_id')),
                         reason_id=int(request.data.get('reason_id')), order_id=int(request.data.get('order_id')), 
                         reason_description=sanitize(request.data.get('reason_description')), cancelled_by_id=int(request.data.get('driver_id')))
                    ndCancelOrder.save()
                return Response({"status":True, "msg": CancelBookingByDriverMsgMod.Msg(lang, 'cancel-success'),
                     "data":dict(), 'loggedInStatus':loggedInStatus})
        except Exception as E:
          return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'error-msg'),
           "data":dict(), 'loggedInStatus':True})

class DriverLocationSaveToDB(APIView):
    @transaction.atomic 
    def post(self, request):
        lang = request.data.get('langC')
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')), 
                request.data.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'session_out'),
                 "data":dict(), 'loggedInStatus':loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('driver_id')):
                return Response({"status":False, "msg":DriverLocationSaveToDBMsgMod.Msg(lang, 'driver_id'),
                 "data" : dict()})
            elif not fieldEmptyCheck(request.data.get('order_id')):
                return Response({"status":False, "msg":DriverLocationSaveToDBMsgMod.Msg(lang, 'order_id'),
                 "data" : dict()})
            elif not fieldEmptyCheck(request.data.get('latlong')):
                return Response({"status":False, "msg":DriverLocationSaveToDBMsgMod.Msg(lang, 'latlong'),
                 "data" : dict()})
            else:
                latlongList = ast.literal_eval(request.data.get('latlong'))
                if type(latlongList) is not list:
                    return Response({"status":str(type(envData)), "msg": GenericMsgMod.Msg(lang, 'error-msg'),
                        "data":dict(), 'loggedInStatus':True})
                tmpSaveData = list()
                if latlongList:
                    for item in latlongList:
                        if item['latitude'] != '0.0' and item['longitude'] != '0.0':
                            ndCurrentDriverLocationObj = NdCurrentDriverLocation(latitude=item['latitude'], longitude=item['longitude'], order_id=int(request.data.get('order_id')), 
                            driver_id=int(request.data.get('driver_id')), real_distance=float(item['real_distance']))
                            tmpSaveData.append(ndCurrentDriverLocationObj)
                if tmpSaveData:
                    NdCurrentDriverLocation.objects.bulk_create(tmpSaveData)
                    return Response({"status":True, "msg": DriverLocationSaveToDBMsgMod.Msg(lang, 'current_locations_saved'),
                        "data":dict(), 'loggedInStatus':True})
                else:
                    return Response({"status":True, "msg": DriverLocationSaveToDBMsgMod.Msg(lang, 'no_new_data'),
                        "data":dict(), 'loggedInStatus':True})
        except Exception as E:
            return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'error-msg'),
             "data":dict(), 'loggedInStatus':True})

class CurrentBookingDetails(APIView):
    def post(self, request):
        lang = request.data.get('langC')
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')), 
                request.data.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'session_out'),
                 "data":dict(), 'loggedInStatus':loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('driver_id')):
                return Response({"status":False, "msg":CurrentBookingDetailsMsgMod.Msg(lang, 'driver_id'),
                 "data" : dict()})
            elif not fieldEmptyCheck(request.data.get('order_id')):
                return Response({"status":False, "msg":CurrentBookingDetailsMsgMod.Msg(lang, 'order_id'),
                 "data" : dict()})
            else:
                orderIns = NdOrder.objects.filter(id=int(request.data.get('order_id')), driver_id=int(request.data.get('driver_id')),
                    booking_status=settings.BOOKING_STATUS_PLACED)
                if not orderIns.exists():
                    return Response({"status":False, "msg": CurrentBookingDetailsMsgMod.Msg(lang, 'not_current_booking'),
                        "data":dict(), 'loggedInStatus':loggedInStatus})
                else:
                    currentOrderDetailsObj = CurrentOrderDetailsSE(orderIns.first(), many=False)
                    return Response({"status":True, "msg": GenericMsgMod.Msg(lang, 'data-fetched'),
                        "data":currentOrderDetailsObj.data, 'loggedInStatus':loggedInStatus})
        except Exception as E:
            return Response({"status":False, "msg": GenericMsgMod.Msg(lang, 'error-msg'),
             "data":dict(), 'loggedInStatus':True})
class UpdateDriverProfileDetails(APIView):
#------------------------ Method to check unique Email Address -------------------------------------#         
    def get_unique_email(self, request,  pk = None):
        lang = request.data['langC']
        try:
            user_id = pk
            if not pk :
                user_id = request.data.get('id') 
            user_id = int(user_id)

            if not fieldEmptyCheck(request.data.get('email_id')):
                return {'status': False, 'msg': LoginMsgMod.Msg(lang, 'email_id')}
            is_exists = NdUsers.objects.filter(Q(email_id__iexact=request.data.get('email_id')), Q(role_id=settings.IS_DRIVER), ~Q(id=user_id),
             Q(is_deleted=False)).count()
            if is_exists >0 :
                return {'status': False, 'msg': LoginMsgMod.Msg(lang, 'email_already_reg')}
            else:
                return {'status': True}
        except Exception as e:
            return {'status': False, 'msg': GenericMsgMod.Msg(lang, 'error-msg')}
    #------------------------ Method to check unique phone number -------------------------------------#         
    def get_unique_phone(self, request, pk = None):
        lang = request.data['langC']
        try:
            user_id = pk
            if not pk :
                user_id = request.data.get('id')
            user_id = int(user_id)
            if not fieldEmptyCheck(request.data.get('phone_number')):
                return {'status': False, 'msg': LoginMsgMod.Msg(lang, 'phone_number')}
            is_exists = NdUsers.objects.filter(Q(phone_number=request.data.get('phone_number')),
             ~Q(id=user_id), Q(role_id=settings.IS_DRIVER), Q(is_deleted=False)).count()
            if is_exists >0 :
                return {'status': False, 'msg': LoginMsgMod.Msg(lang, 'phone_number_already_reg')}
            else:
                return {'status': True}
        except Exception as e:
            return {'status': False, 'msg': GenericMsgMod.Msg(lang, 'error-msg')}
    @transaction.atomic
    def post( self, request ):
        lang = request.data['langC']
        try:
            get_unique_phone = self.get_unique_phone(request, int(request.data.get('driver_id')))
            get_unique_email = self.get_unique_email(request, int(request.data.get('driver_id')))
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
             request.data.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('first_name')):
                return Response({"status" : False,"msg" :  LoginMsgMod.Msg(lang, 'first_name'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('last_name')):
                return Response({"status" : False,"msg" :  LoginMsgMod.Msg(lang, 'last_name'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('phone_number')):
                return Response({"status" : False,"msg" :  LoginMsgMod.Msg(lang, 'phone_number'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not get_unique_phone['status']:
                return Response({"status" : False,"msg" :  get_unique_phone['msg'],
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not get_unique_email['status']:
                return Response({"status" : False,"msg" :  get_unique_email['msg'],
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            else:

                if not request.data.get('is_same_number'):
                    phoneNoWithISD = request.data.get('isd_code') + request.data.get('phone_number')
                    random_code = self.randomPassword( request )
                    msg = "Your Need Deliver verification code is " + random_code + "."
                    isMsgSend = sendGenericMessage( phoneNoWithISD, msg )
                    NdUsers.objects.filter(id=int(request.data.get('driver_id'))).update(first_name=sanitize(request.data.get('first_name')),
                         last_name=sanitize(request.data.get('last_name')), 
                    phone_number= sanitize(request.data.get('phone_number')), email_id= sanitize(request.data.get('email_id')), 
                    country_id= int(request.data.get('country_id')), verification_code = random_code)
                    phone_no = request.data.get('phone_number')
                    firstChar =  phone_no[0]
                    
                    if firstChar == '0':
                        phone_no = phone_no.lstrip('0')
                    client.publish(
                        PhoneNumber=request.data.get('isd_code') + phone_no,
                        Message="Your Need Deliver verification code is " + random_code + "."
                    )
                    return Response({'status': True, 'msg' :  LoginMsgMod.Msg(lang, 'basic-info-save-msg'),
                     "data" : dict(), 'loggedInStatus' : True})
                if fieldEmptyCheck(request.data.get('password')) and fieldEmptyCheck(request.data.get('cpassword')):
                    if request.data.get('password') != request.data.get('cpassword'):
                        return Response({"status" : False,"msg" :  LoginMsgMod.Msg(lang, 'confirm_not_match'),
                            "data" : dict(), 'loggedInStatus' : loggedInStatus})
                    else:
                        newpassword = str(encrypt_val(request.data.get('password')))
                        NdUsers.objects.filter(id=int(request.data.get('driver_id'))).update(first_name=sanitize(request.data.get('first_name')),
                             last_name=sanitize(request.data.get('last_name')), password=newpassword,
                             email_id= sanitize(request.data.get('email_id')), country_id= int(request.data.get('country_id'))) 
                else:
                    NdUsers.objects.filter(id=int(request.data.get('driver_id'))).update(first_name=sanitize(request.data.get('first_name')),
                             last_name=sanitize(request.data.get('last_name')), email_id= sanitize(request.data.get('email_id')),
                             country_id=int(request.data.get('country_id')))            
                
                return Response({'status':True, 'data':dict(), "msg":LoginMsgMod.Msg(lang, 'basic-info-save-msg'),
                 'loggedInStatus':loggedInStatus})
        except Exception as e:
          return Response({'status':False, 'msg':GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict(),  'loggedInStatus' : True})
def time_diff(start, end):
    from datetime import datetime, time as datetime_time, timedelta
    if isinstance(start, datetime_time): # convert to datetime
        assert isinstance(end, datetime_time)
        start, end = [datetime.combine(datetime.min, t) for t in [start, end]] 
    if start <= end: # e.g., 10:33:26-11:15:49
        return end - start
    else: # end < start e.g., 23:55:00-00:25:00
        end += timedelta(1) # +day
        assert end > start
        return end - start
class CheckOrderStatusBeforeAccept(APIView):
    def post(self, request):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
             request.data.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('driver_id')):
                return Response({"status" : False,"msg" :  CheckOrderStatusBeforeAcceptMsgMod.Msg(lang, 'driver_id'),
                     "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('order_id')):
                return Response({"status" : False,"msg" :  CheckOrderStatusBeforeAcceptMsgMod.Msg(lang, 'order_id'),
                     "data" : dict(), 'loggedInStatus' : loggedInStatus})
            else:
                bookingReqDetails = NdBookingRequests.objects.filter(order_id=int(request.data.get('order_id')), driver_id=int(request.data.get('driver_id'))).values('date_created', 'id').first()
                nowTime = timezone.now() 
                diff = (nowTime - bookingReqDetails['date_created']).total_seconds()
                if diff >= 19:
                    NdBookingRequests.objects.filter(id=bookingReqDetails['id']).update(is_deleted=True)
                    return Response({"status" : False,"msg":CheckOrderStatusBeforeAcceptMsgMod.Msg(lang, 'booking_expired'), "data" : dict(), 'loggedInStatus' : loggedInStatus})
                orderDetails = NdOrder.objects.filter(id=int(request.data.get('order_id')), book_order__driver_id=int(request.data.get('driver_id')),
                    book_order__is_deleted=False)
                orderDetailsObj = orderDetails.values('driver_id', 'booking_status').first()
                if orderDetails.exists() and orderDetailsObj['booking_status'] == settings.BOOKING_STATUS_PROCESSING:
                    return Response({"status" : True,"msg" :"", "data" : dict(), 'loggedInStatus' : loggedInStatus})
                else:
                    NdBookingRequests.objects.filter(Q(order_id=int(request.data.get('order_id'))), ~Q(driver_id=request.data.get('driver_id'))).update(is_deleted=True)
                    return Response({"status" : False,"msg":CheckOrderStatusBeforeAcceptMsgMod.Msg(lang, 'booking_expired'), "data" : dict(), 'loggedInStatus' : loggedInStatus})
        except Exception as e:
          return Response({'status':False, 'msg':GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict(),  'loggedInStatus' : True})
# Ishita
class DriverAccountBalance(APIView):
    def post(self, request):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
             request.data.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
             "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('driver_id')):
                return Response({"status":False, "msg":GenericMsgMod.Msg(lang, 'error-msg'),
                 "data" : dict()})
            else:
                driverDetailsObj = NdDriverDetails.objects.filter(user_id=int(request.data.get('driver_id'))).first()
                ndDriverDetailsSerializer = NdDriverDetailsSerializer(driverDetailsObj, context={ 'currentLang': lang })
                
                account_bal = ndDriverDetailsSerializer.data['account_balance']
                # currentLang = "en" #need to change to make 
                # print(account_bal)
                langReq = 'km-KH'
                convertedRateObj = calculationCurrencyConversion(account_bal, langReq)
                # calculateCurrentRateByLang( conversion_rate,  amount, currentLang )
                
                return Response({"status":True, "msg":GenericMsgMod.Msg(lang, 'data-fetched'),
                 'totalCharge':account_bal, "currency": convertedRateObj['currency'] })
        except Exception as e:
          return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict()})
class GetBookingAllDetails(APIView):
    def post(self, request):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
             request.data.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
             "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('order_id')):
                return Response({"status":False, "msg":GenericMsgMod.Msg(lang, 'error-msg'),
                 "data" : dict()})
            elif not fieldEmptyCheck(request.data.get('order_id')):
                return Response({"status":False, "msg":GenericMsgMod.Msg(lang, 'error-msg'),
                 "data" : dict()})
            else:
                orderDetails = NdOrder.objects.filter(id=int(request.data.get('order_id')), driver_id=int(request.data.get('driver_id')))
                if orderDetails.exists():
                    orderDetailsObj = OngoingOrderDetailsSE(orderDetails.first(), many=False)

                    return Response({"status":True, "msg": GenericMsgMod.Msg(lang, 'data-fetched'), 'data':orderDetailsObj.data })
                else:

                    return Response({"status":False, "msg":GenericMsgMod.Msg(lang, 'data-not-found'), "data" : dict()})
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict()})
class CheckBalanceStatus(APIView):
    def post(self, request):
        lang = request.data['langC']
        try:
            driverDetails = NdDriverDetails.objects.filter(user_id=int(request.data.get('user_id'))).values('account_balance')
            driverDetailsObj = driverDetails.first()
            balanceStatus = 0
            if driverDetailsObj['account_balance']>0 and driverDetailsObj['account_balance'] <= settings.DRIVER_LOW_BALANCE_THRESHOLD :
                balanceStatus = 1
            elif driverDetailsObj['account_balance'] > settings.DRIVER_LOW_BALANCE_THRESHOLD :
                balanceStatus = 2
            return Response({"status":True, "msg":GenericMsgMod.Msg(lang, 'data-fetched'), "balanceStatus" : balanceStatus})
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict()})
