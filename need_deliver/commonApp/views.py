from django.shortcuts import render
from .serializers import *
from .message import *
import bleach
from django.contrib.postgres import fields
from django.db.models import F, Q, Count, Min, Sum, Avg, FloatField, ExpressionWrapper
from rest_framework.views import APIView
from Crypto.Cipher import AES
import base64
from rest_framework.response import Response
import uuid
from django.utils.crypto import get_random_string
import boto3
import os.path
from django.conf import settings
from geopy.distance import vincenty
from rest_framework.parsers import MultiPartParser
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import  transaction
from datetime import datetime
from pyfcm import FCMNotification
push_service = FCMNotification(api_key=settings.FCM_API_KEY)
#------------------------------------------------------------------ Field Empty check ----------------------------------------------------#
def fieldEmptyCheck( inputVal ):
    if not inputVal or  inputVal == "":
        return False
    else:
        return True
def calculationCurrencyConversion( amount, langC ):
    print(langC)
    currencyDetails = NdCurrencies.objects.filter(language_type__iexact=langC, is_status=True, is_deleted=False)
    if currencyDetails.exists():
        currencyDetailsObj = currencyDetails.values('id', 'conversion_rate', 'default_currency', 'currency').first()
        amount = float(amount) * float(currencyDetailsObj['conversion_rate'])
        amount = format(float(amount), '.2f')
        return {"status":True, "amount":amount, "conversion_rate":currencyDetailsObj['conversion_rate'], "currency_id":currencyDetailsObj['id'], "currency":currencyDetailsObj['currency']}
    else:
        return {"status":False, "amount":amount, "conversion_rate":currencyDetailsObj['conversion_rate'], "currency_id":currencyDetailsObj['id'], "currency":currencyDetailsObj['currency']}
# Ishita
def calculationCurrencyConversionWithPresentCur( amount, langC, currentLang ):
    currencyDetails = NdCurrencies.objects.filter(language_type__iexact=langC, is_status=True, is_deleted=False)
    currentCurrencyDetailsObj = NdCurrencies.objects.filter(language_type__iexact=currentLang, is_status=True, is_deleted=False).values('id','currency', 'conversion_rate').first()
    currencyDetailsObj = currencyDetails.values('id', 'conversion_rate', 'default_currency', 'currency').first()
    if langC != currentLang :
        would_be_conversion_rate = float(currencyDetailsObj['conversion_rate'])
        current_conversion_rate = float(currentCurrencyDetailsObj['conversion_rate'])
        currencyConvertedToKhr = float(amount)/current_conversion_rate
        convertedToRequired = currencyConvertedToKhr * would_be_conversion_rate
        amount = format(float(convertedToRequired), '.2f')
        return {"status":True, "amount":amount, "currency":currencyDetailsObj['currency']}
    else:
        
        return {"status":True, "amount":amount,  "currency":currentCurrencyDetailsObj['currency']}

    
# Ishita
def calculateCurrentRateByLang( conversion_rate,  amount, currentLang ):

    currencyDetailsObj = NdCurrencies.objects.filter(language_type__iexact=currentLang).values('id', 'conversion_rate', 'currency').first()
    currencyConvertedToKhr = float(amount)/float(conversion_rate)
    convertedToRequired = currencyConvertedToKhr * float(currencyDetailsObj['conversion_rate'])
    # khr_amount = amount 
    convertedToRequired = format(float(convertedToRequired), '.2f')
    return { "convertedAmount":convertedToRequired, "currency": currencyDetailsObj['currency'] }

    
    # if currencyDetails.exists():
    #   currencyDetailsObj = currencyDetails.filter(language_type__iexact=langC).values('id', 'conversion_rate', 'default_currency').first()
    #   return {"status":True, "conversion_rate":currencyDetailsObj['conversion_rate'], "currency_id":currencyDetailsObj['id']}
    # else:
    #   currencyDetailsObj = currencyDetails.filter(default_currency=True).values('id', 'conversion_rate').first()
    #   return {"status":False, "amount":amount, "conversion_rate":currencyDetailsObj['conversion_rate'], "currency_id":currencyDetailsObj['id']}
#-------------------------------------------- Calculate And Update Overall rating ---------------------------------------#
def update_over_all_rating(user_id):
    reviewRecords = NdReviewPosted.objects.filter(driver_id=user_id, is_status=True, is_deleted=False)
    if reviewRecords.count()>0:
        avgRating =  reviewRecords.aggregate(Avg('star_rate'))
        checkExistance = NdUsersObjects.objects.filter(user_id=user_id)
        if checkExistance.count()>0:
            NdUsersObjects.objects.filter(user_id=user_id).update(over_all_rating=avgRating['star_rate__avg'], no_of_reviews=reviewRecords.count())
        else:
            ndUsersObjectsObj = NdUsersObjects(user_id=user_id, over_all_rating=avgRating['star_rate__avg'], no_of_reviews=reviewRecords.count())
            ndUsersObjectsObj.save()
        return {'status': True, 'avg_rating':avgRating['star_rate__avg'], 'no_of_reviews':reviewRecords.count()}
    else:
        return {'status': False}
#----------------------------------- check pending document attachments -------------------------------------------------#
def is_document_upload_pending(driver_id):
    is_already_added = NdVehicleDetails.objects.filter(user_id=driver_id)
    if is_already_added.count()>0:
        return True
    else:
        return False
#------------------------------------------------- Push notification VIA FCM ------------------------------------------#
class pushNotificationFCM( APIView ):
    def save_notification_data( notifyObj, extraData):
        if notifyObj['userIDs']:
            for item in notifyObj['userIDs']:
                ndNotifications = NdNotifications(user_id=item, title=notifyObj['title'],
                 body=notifyObj['body'], extra_data=extraData)
                ndNotifications.save()
    def send_push_notification( deviceIDs, userIDs, dataObj, customData, isNotDataSaved =None):
        message_title = dataObj['title']
        message_body = dataObj['body']
        image = ""
        if 'image' in dataObj:
            image = dataObj['image']
        style = ""
        if 'style' in dataObj:
            image = dataObj['style']
        notifyObj = {'userIDs': userIDs, 'title' :message_title, 'body': message_body, 'style' : style, 'image' : image}
        customData['sound'] = 'notification.mp3'
        if not isNotDataSaved:
            pushNotificationFCM.save_notification_data(notifyObj, customData)
        if deviceIDs:
            customData['sound'] = 'notification.mp3'
            result = push_service.notify_multiple_devices(registration_ids=deviceIDs, message_title=message_title, sound='notification.mp3', message_body=message_body, 
                data_message=customData, content_available=True)
            print(result)
        return True
        
client = boto3.client(
    "sns",
    aws_access_key_id= settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY,
    region_name= settings.SEGION_NAME
)
def current_date_time():
    current_date_time = datetime.utcnow()
    return current_date_time
#--------------------------------------------------------------- Password Encrypt ----------------------------------------------------#
def encrypt_val(clear_text):
    clear_text = clear_text
    enc_secret = AES.new(settings.MASTER_KEY[:32])
    tag_string = (str(clear_text) +
                  (AES.block_size -
                   len(str(clear_text)) % AES.block_size) * "\0")
    cipher_text = base64.b64encode(enc_secret.encrypt(tag_string))
    return cipher_text.decode('utf-8')
#--------------------------------------------------------------- Password decrypt ----------------------------------------------------#
def decrypt_val(cipher_text):
    dec_secret = AES.new(settings.MASTER_KEY[:32])
    raw_decrypted = dec_secret.decrypt(base64.b64decode(cipher_text))
    clear_val = raw_decrypted.decode().rstrip("\0")
    return clear_val
#------------------------------------------------------------------ Sanitized Data ----------------------------------------------------#
def sanitize(inputstr):
    sanitized = inputstr
    badstrings = [
        ';',
        '$',
        '&&',
        '../',
        '<',
        '>',
        '%3C',
        '%3E',
        '\'',
        '--',
        '1,2',
        '\x00',
        '`',
        '(',
        ')',
        'file://',
        'input://'
    ]
    for badstr in badstrings:
        if badstr in sanitized:
            sanitized = sanitized.replace(badstr, '')
    return sanitized.strip()

#------------------------------------------------------------------ Get Latest Device Token by Logged in User ID ----------------------------------------------------#

def get_latest_device_token_by_userid( user_id ):
    try:
        getRecords = NdUsers.objects.filter(id=int(user_id))
        if getRecords.count()>0:
            getDeviceObj = NdUsersUniqueDeviceIDSE( getRecords.first(), many=False )
            if getDeviceObj['device_token'] != "" or getDeviceObj['device_token'] is not None : 
                return getDeviceObj['device_token']
            else:
                return ""
        else: 
            return ""
    except Exception as e:
        return ""
#------------------------------------------------------------------ Send Generic SMS ---------------------------------------------------------------------#
def sendGenericMessage( phone_number, msg ):
    try:
        client.set_sms_attributes(
            attributes={
                'DefaultSMSType': 'Transactional'
            }
        )
        client.publish(
            PhoneNumber=phone_number,
            Message=msg
        )
        return True

    except Exception as e:
        return False
#------------------------------------------------------------------ Generate UID by Logged in User ID ----------------------------------------------------#
def generateUID():

    uid = uuid.uuid4()

    try:
        obj = NdUsers.objects.get(device_uuid=uid)
    except NdUsers.DoesNotExist:

        return uid
    else:
        print(4444444)
        return generateUID()

        #------------------------------------------------------------------ Get Device UID of Logged in User ID ----------------------------------------------------#
def get_latest_device_uuid_by_userid(user_id, client_device_uuid):
    # try:
    print("----------------------")
    getRecords = NdUsers.objects.filter(id=int(user_id), device_uuid = client_device_uuid)
    if getRecords.count()>0: 
        userDetails = NdUsers.objects.filter(id=int(user_id)).values('is_status', 'is_deleted').first()   
        print(19)
        if userDetails['is_status'] and getRecords.count() > 0:
            print(18)
            return True
        elif userDetails['is_deleted'] and getRecords.count() > 0: 
            print(17)
            return False
        elif userDetails['is_status'] and not userDetails['is_deleted'] and getRecords.count()>0:
            print(16)
            return True
        elif not userDetails['is_status'] or  userDetails['is_deleted']:
            print(21)
            return False
        else:
            True

    else: 
        print(14)
        userDetails = NdUsers.objects.filter(id=int(user_id)).values('is_status', 'is_deleted').first()
        if userDetails['is_status'] and getRecords.count() == 0:
            print(13)
            return False
        elif userDetails['is_deleted'] and getRecords.count() == 0: 
            print(12)
            return False
        elif userDetails['is_status'] and not userDetails['is_deleted']:
            print(11)
            return True
        elif not userDetails['is_status'] or userDetails['is_deleted']:
            print(23)
            return True
        else:
            print(10)
            return False
    # except Exception as e:
    #     return False
#------------------------------------------------------- Start Developer by Arijit Chandra ------------------------------------------------------------#
class Login(APIView):  
    #------------------------ Login for Customer and Driver -------------------------------------#        
    def randomPassword( self, request ):
        random_code = get_random_string(length=4, allowed_chars='123456789')
        randomKeycheck = NdUsers.objects.filter(verification_code=random_code, is_deleted=False).count()
        if randomKeycheck >0 :
            self.randomPassword( request )
        else:
            return random_code
    def sendPushToOlderLoggedInUser(self, request, customParam, dataFields):
        userIDS = dataFields['userIDS']
        if dataFields['deviceIDS']:
            deviceIDS = dataFields['deviceIDS']
        pushNotificationFCM.send_push_notification( deviceIDS, userIDS, 
            {"title": dataFields['title'], "body": dataFields['body'], "notification_type_id" : 4}, customParam)
        return True
    @transaction.atomic 
    def post(self, request, format=None):
        lang = request.data['langC']
        try:
            if not fieldEmptyCheck(request.data.get('verification_code')) :
                return Response({"status" : False,"msg" :  LoginMsgMod.Msg(lang, 'verification_code'),
                 "data" : dict(), 'device_uuid' : ""})
            elif not fieldEmptyCheck( request.data.get('role_id') ):
                return Response({"status" : False,"msg" :  LoginMsgMod.Msg(lang, 'role_id'),
                 "data" : dict(), 'device_uuid' : ""})
            else:
                uniqueUUID = generateUID()
                records = NdUsers.objects.filter(Q(verification_code=request.data.get('verification_code')),
                 Q(role_id = int(request.data.get('role_id'))), Q(is_deleted=False), Q(phone_number=request.data.get('phone_number')))
                if records.count() >0 :
                    loggedinData = NdUsersLoginSE(records.first(), many=False)
                    is_pending = False
                    if fieldEmptyCheck(loggedinData.data['device_token']) and request.data.get('device_token') != loggedinData.data['device_token']:
                        title = 'Login Expired'
                        body = "Your current logged in session has expired."
                        deviceIDS = [loggedinData.data['device_token']]
                        userIDS = [loggedinData.data['id']]
                        dataFields = {"title":title, "body":body, "deviceIDS":deviceIDS, "userIDS":userIDS }    
                        customParam = {}
                        customParam['push_type'] = settings.NOTIFICATION_TYPE['session_expired']
                        customParam['body'] = body
                        customParam['title'] = title
                        self.sendPushToOlderLoggedInUser(request, customParam, dataFields)  
                    # if loggedinData.data['is_status'] == True :
                    updateDeviceToken = NdUsers.objects.filter(id=loggedinData.data['id']).update(device_uuid=uniqueUUID, 
                     verification_code =None, is_phone_no_verified=True, device_token=request.data.get('device_token'))

                    if int(request.data.get('role_id')) == settings.IS_DRIVER:
                        is_pending = is_document_upload_pending(loggedinData.data['id'])

                      
                    return Response({'status': True, 'data' : loggedinData.data, "msg" :  LoginMsgMod.Msg(lang, 'login-success-msg'),
                     'device_uuid' : uniqueUUID, 'is_document_attached':is_pending})
                    # elif loggedinData.data['is_status'] == False :
                    #   return Response({'status': False, "msg" :  LoginMsgMod.Msg(lang, 'ac_deactivate'),
                    #    "data" : dict(), 'device_uuid' : ""})
                    # else :
                    #   return Response({'status': False, "msg" :  LoginMsgMod.Msg(lang, 'phone_no_not_verified'), 
                    #       "data" : dict(), 'device_uuid' : ""})
                else:
                    return Response({'status': False, 'msg' :  LoginMsgMod.Msg(lang, 'not_match'),
                     "data" : dict(), 'device_uuid' : ""})
        except Exception as e:
          return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), 
              "data" : dict(), 'device_uuid' : ""})
    #------------------------ Method to check unique Email Address -------------------------------------#         
    def get_unique_email(self, request,  pk = None):
        lang = request.data['langC']
        try:
            user_id = pk
            if not pk :
                user_id = request.data.get('id')
            user_id = int(user_id)

            
            is_exists = NdUsers.objects.filter(Q(email_id__iexact=request.data.get('email_id')), Q(role_id=settings.IS_SUPPLIER), ~Q(id=user_id),
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
             ~Q(id=user_id), Q(role_id=settings.IS_SUPPLIER), Q(is_deleted=False)).count()
            if is_exists >0 :
                return {'status': False, 'msg': LoginMsgMod.Msg(lang, 'phone_number_already_reg')}
            else:
                return {'status': True}
        except Exception as e:
            return {'status': False, 'msg': GenericMsgMod.Msg(lang, 'error-msg')}
    @transaction.atomic
    def patch( self, request, pk ):
        lang = request.data['langC']
        try:
            get_unique_phone = self.get_unique_phone(request, pk)
            get_unique_email = self.get_unique_email(request, pk)
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
                # print("ssssssssss",request.data.get('is_same_number'))
                if not request.data.get('is_same_number'):
                    phoneNoWithISD = request.data.get('isd_code') + request.data.get('phone_number')
                    random_code = self.randomPassword( request )
                    msg = "Your Need Deliver verification code is " + random_code + "."
                    isMsgSend = sendGenericMessage( phoneNoWithISD, msg )
                    NdUsers.objects.filter(id=int(pk)).update(first_name=sanitize(request.data.get('first_name')),
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
                NdUsers.objects.filter(id=int(pk)).update(first_name=sanitize(request.data.get('first_name')),
                 last_name=sanitize(request.data.get('last_name')), 
                email_id= sanitize(request.data.get('email_id')), country_id= int(request.data.get('country_id')))
                return Response({'status':True, 'data':dict(), "msg":LoginMsgMod.Msg(lang, 'basic-info-save-msg'),
                 'loggedInStatus':loggedInStatus})
        except Exception as e:
            return Response({'status':False, 'msg':GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict(),  'loggedInStatus' : True})

#----------------------------------------------------------- Update Profile Picture ----------------------------------------------------------------------------#  
class UpdateProfilePicture( APIView ):
    parser_classes = (MultiPartParser,)
    @transaction.atomic
    def patch( self, request ):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.POST.get('session_user_id')),
             request.POST.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.FILES): 
                return Response({"status" : False,"msg" :  UpdateProfilePictureMsgMod.Msg(lang, 'profile_picture'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            else:
                NdUsers.objects.filter(id=int(request.POST.get('id')))
                tmpUserData = request.data
                del tmpUserData['session_user_id']
                del tmpUserData['langC']
                del tmpUserData['session_unique_uuid']
                u = NdUsers.objects.get(id =int(request.POST.get('id')))
                ndUsersProfileImageSE = NdUsersProfileImageSE(u, data={'profile_picture' : request.FILES['profile_picture']})
                if ndUsersProfileImageSE.is_valid():
                    ndUsersProfileImageSE.save()
                return Response({'status': True, 'msg' :  UpdateProfilePictureMsgMod.Msg(lang, 'success-msg'),
                 "data" : dict(), 'loggedInStatus' : True})
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'),
             "data" : dict(), 'loggedInStatus' : True})
#------------------------ Login OTP Generate for Customer and Driver -------------------------------------#         
class LoginOTP(APIView):
    def randomPassword( self, request ):
        # return "1111"
        random_code = get_random_string(length=4, allowed_chars='123456789')
        randomKeycheck = NdUsers.objects.filter(verification_code=random_code, is_deleted=False).count()
        if randomKeycheck >0 :
            self.randomPassword( request )
        else:
            return random_code
    @transaction.atomic
    def post( self, request ):
        lang = request.data['langC']
        try:
            request.POST._mutable = True
            phone_no = request.data.get('phone_number')
            firstChar =  phone_no[0]
            
            if firstChar == '0':
                phone_no = phone_no.lstrip('0')
            # request.data['phone_number'] = phone_no
            if request.data.get('phone_number') == "" :
                return Response({"status" : False,"msg" :  LoginMsgMod.Msg(lang, 'phone_number'), "data" : dict()})
            else:
                records = NdUsers.objects.filter(Q(phone_number=sanitize(request.data.get('phone_number'))), Q(role_id=int(request.data.get('role_id'))), is_deleted=False)    
                random_code = self.randomPassword( request )
                # random_code = "1111"
                if records.count() >0:
                    userDetails = records.values('id', 'is_status', 'is_deleted').first()
                    if not userDetails['is_status']:
                        return Response({"status" : False,"msg" :  LoginMsgMod.Msg(lang, 'ac_deactivate'), "data" : dict()})
                    if  userDetails['is_deleted']:
                        return Response({"status" : False,"msg" :  LoginMsgMod.Msg(lang, 'ac_not_exists'), "data" : dict()})
                    NdUsers.objects.filter(id= int(userDetails['id'])).update( verification_code=random_code,
                     phone_number= request.data.get('phone_number'), country_id= int(request.data.get('country_id')) ) 
                else:
                    ndUsersSaveObj = NdUsers(verification_code=random_code, phone_number= request.data.get('phone_number'),
                     country_id= int(request.data.get('country_id')), role_id = int(request.data.get('role_id')))
                    ndUsersSaveObj.save()
                client.publish(
                        PhoneNumber=request.data.get('isd_code') + phone_no,
                        Message="Your Need Deliver verification code is " + random_code + "."
                )
                return Response({'status': True, "msg" :  LoginMsgMod.Msg(lang, 'login_otp_generate'),
                 "data" : dict(), 'code' : random_code})
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict()})
#-------------------------------------------------------------- Get Country List --------------------------------------------------------------------#          
class Countries( APIView ):
    def get( self, request ):
        try:
            allCounties = NdCountries.objects.filter().order_by('country_name')
            if allCounties.count()>0 :
                countryListObj = NdCountriesSE(allCounties, many=True)
                cloneRecords = countryListObj.data
                i=0
                for item in cloneRecords:
                    flagImgCode = item['country_code'].lower()
                    # flagImgPath =  static( settings.FLAG_SMALL + flagImgCode + ".png")
                    flagImgPath =  settings.STATIC_URL + settings.FLAG_SMALL + flagImgCode + ".png"
                    cloneRecords[i]['flag_logo'] = flagImgPath
                    i+=1
                return Response({'status' : True, 'data' : cloneRecords, 'msg' : ""})
            else: 
                return Response({'status' : False, 'data' : dict(), 'msg' : ''})
        except Exception as e:
            return Response({'status' : False,  'data' : dict(), 'msg' : ''})
#-------------------------------------------------------------- Get Home banner slider List --------------------------------------------------------------------#           
class HomeBannerSlider( APIView ):
    def get( self, request ):
        try:
            allRecords = NdImage.objects.filter(is_deleted=False, is_status=True, applied_to=settings.CONST_SPLASH_BANNER_TYPE)
            if allRecords.count()>0 :
                homeBannerImagesObj = NdAllHomeBannerImagesSE(allRecords, many=True)
                return Response({'status' : True, 'data' : homeBannerImagesObj.data, 'msg' : ""})
            else: 
                return Response({'status' : False, 'data' : dict(), 'msg' : ''})
        except Exception as e:
            return Response({'status' : False,  'data' : dict(), 'msg' : ''})
#-------------------------------------------------------------- Get Splash slider List --------------------------------------------------------------------#        
class SplashBannerSlider( APIView ):
    def get( self, request ):
        try:
            allRecords = NdSplashScreen.objects.filter(is_deleted=False, is_status=True)
            if allRecords.count()>0 :
                splashImagesObj = SplashImagesSE(allRecords, many=True)
                return Response({'status' : True, 'data' : splashImagesObj.data, 'msg' : ""})
            else: 
                return Response({'status' : False, 'data' : dict(), 'msg' : ''})
        except Exception as e:
            return Response({'status' : False,  'data' : dict(), 'msg' : ''})
#----------------------------------------------------------- Users record  details wrt role id ----------------------------------------------------------------------------#  
class UsersRecordDetails( APIView ):
    def post( self, request ):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
             request.data.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            else:
                userData = NdUsers.objects.filter(Q(id=(request.data.get('id'))), ~Q(role_id=settings.IS_ADMIN))
                userDataObj = NdUsersLoginSE(userData.first(), many=False)
                return Response({'status': True, 'msg' :  "", "data" : userDataObj.data, 'loggedInStatus' : True})
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'),
             "data" : dict(), 'loggedInStatus' : True})
#----------------------------------------------------------- Location saved ----------------------------------------------------------------------------#  
class SaveLocationsList( APIView ):
    def post(self, request):
        lang = request.data['langC']
        try:
            ndSavedLocationsObj = NdSavedLocations.objects.filter(user_id=int(request.data.get('supplier_id')), is_deleted=False, is_status=True)
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
             request.data.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif ndSavedLocationsObj.count()>0:
                ndSavedLocationsSEObj =  NdSavedLocationsSE(ndSavedLocationsObj, many=True)
                return Response({"status":True, "msg": SaveLocationsMsgMod.Msg(lang, 'record-found'), 
                    "data":ndSavedLocationsSEObj.data, 'no_of_records': ndSavedLocationsObj.count()})
            else:
                return Response({"status":False, "msg": SaveLocationsMsgMod.Msg(lang, 'not-found'),
                 "data":dict(), 'no_of_records': ndSavedLocationsObj.count()})
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict()})
class SaveLocations( APIView ):
    def check_same_location_name(self, request, pk=None):
        recordCheck = NdSavedLocations.objects.filter(Q(location_name__iexact=sanitize(request.data.get('location_name'))), 
        Q(location__iexact=sanitize(request.data.get('location'))))

        # if pk:
        #   print(request.data.get('location'))
        #   print(pk)
        #   # recordCheck = recordCheck.filter(~Q(id=int(pk)))
        recordCheckab = recordCheck.count()
        if recordCheckab>0 :
            return False
        else:
            return True
    @transaction.atomic
    def post(self, request):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
             request.data.get('session_unique_uuid'))
            # is_same_location_name = self.check_same_location_name(request)
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            # elif not fieldEmptyCheck(request.data.get('location_name')):
            #   return Response({"status" : False,"msg" :  SaveLocationsMsgMod.Msg(lang, 'location_name'),
            #    "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('location')):
                return Response({"status" : False,"msg" :  SaveLocationsMsgMod.Msg(lang, 'location'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('latitude')):
                return Response({"status" : False,"msg" :  SaveLocationsMsgMod.Msg(lang, 'latitude'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('longitude')):
                return Response({"status" : False,"msg" :  SaveLocationsMsgMod.Msg(lang, 'longitude'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('user_id')):
                return Response({"status" : False,"msg" :  SaveLocationsMsgMod.Msg(lang, 'user_id'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            # elif not is_same_location_name:
            #   return Response({"status" : False,"msg" :  SaveLocationsMsgMod.Msg(lang, 'same_location_name'),
            #    "data" : dict(), 'loggedInStatus' : loggedInStatus})
            else:
                ndSavedLocationsObj = NdSavedLocations(user_id=request.data.get('user_id'),
                 location=sanitize(request.data.get('location')), 
                    location_name=sanitize(request.data.get('location_name')), latitude=request.data.get('latitude'), 
                    longitude=request.data.get('longitude'))
                ndSavedLocationsObj.save()  
                return Response({"status" : True,"msg" :  SaveLocationsMsgMod.Msg(lang, 'success-msg'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'),
             "data" : dict(), 'loggedInStatus' : True})

    @transaction.atomic
    def patch(self, request, pk):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
             request.data.get('session_unique_uuid'))
            # is_same_location_name = self.check_same_location_name(request, pk)
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
                     "data" : dict(), 'loggedInStatus' : loggedInStatus})
                # elif not fieldEmptyCheck(request.data.get('location_name')):
            #   return Response({"status" : False,"msg" :  SaveLocationsMsgMod.Msg(lang, 'location_name'),
            #    "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('location')):
                return Response({"status" : False,"msg" :  SaveLocationsMsgMod.Msg(lang, 'location'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('latitude')):
                return Response({"status" : False,"msg" :  SaveLocationsMsgMod.Msg(lang, 'latitude'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('longitude')):
                return Response({"status" : False,"msg" :  SaveLocationsMsgMod.Msg(lang, 'longitude'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('user_id')):
                return Response({"status" : False,"msg" :  SaveLocationsMsgMod.Msg(lang, 'user_id'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            # elif not is_same_location_name:
            #   return Response({"status" : False,"msg" :  SaveLocationsMsgMod.Msg(lang, 'same_location_name'),
            #    "data" : dict(), 'loggedInStatus' : loggedInStatus})
            else:
                NdSavedLocations.objects.filter(id=pk, user_id=int(request.data.get('user_id'))).update(location=sanitize(request.data.get('location')), 
                    location_name=sanitize(request.data.get('location_name')), latitude=request.data.get('latitude'), 
                    longitude=request.data.get('longitude'))
                return Response({"status" : True, "msg":SaveLocationsMsgMod.Msg(lang, 'update-success-msg'), 
                    "data" : dict(), 'loggedInStatus' : loggedInStatus})
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict(), 'loggedInStatus' : True})

    @transaction.atomic
    def delete(self, request, pk):
        lang = request.data.get('langC')
        try:
            NdSavedLocations.objects.filter(id=pk).update(is_deleted=True, date_updated=current_date_time())
            return Response({'status': True, 'msg' :  SaveLocationsMsgMod.Msg(lang, 'delete-success-msg'),
             "data" : dict(), 'loggedInStatus' : True})
        except Exception as E:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict(), 'loggedInStatus' : True})
class GetOtpByName(APIView):
    def post(self, request):
        record = NdUsers.objects.filter(phone_number=request.data.get('phone_number')).values('id',
         'phone_number', 'verification_code').first()
        return Response({"status":True, 'data': record})
#------------------------------------------------------------ Order Details By Order ID --------------------------------------------------------------#
class OrderDetails(APIView):
    def post(self, request):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
             request.data.get('session_unique_uuid'))
            # is_same_location_name = self.check_same_location_name(request, pk)
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
                     "data" : dict(), 'loggedInStatus' : loggedInStatus})
            else:
                orderInstance = NdOrder.objects.filter(id=int(request.data.get("order_id")), driver_id__isnull=False)
                if orderInstance.count()>0:
                    orderObj = OrderDetailsSE(orderInstance.first(), many=False, context = { 'currentLang': lang })
                    return Response({"status":True, "msg": OrderDetailsMsgMod.Msg(lang, 'found'), 
                        "data":orderObj.data, 'loggedInStatus' : loggedInStatus})
                else:
                    return Response({"status":False, "msg": OrderDetailsMsgMod.Msg(lang, 'not-found'),
                     "data":dict(), 'loggedInStatus' : loggedInStatus})
        except Exception as e:
            return Response({'status': False, 'msg' :  GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict(), 'loggedInStatus':True})
class AllVehicleTypes(APIView):
    def get(self, request):
        try:
            ndVehicleTypeInstance = NdVehicleType.objects.filter(Q(is_status=True), Q(is_deleted=False), ~Q(vehicletype__id=None), 
                Q(vehicletype__is_status=True), Q(vehicletype__is_deleted=False)).distinct()
            ndVehicleTypeObj = NdVehicleTypeSE(ndVehicleTypeInstance, many=True)
            return Response({"status":True, "msg": "", "data":ndVehicleTypeObj.data})
        except Exception as e:
            return Response({'status': False, 'msg':"Something went wrong", "data" : dict()})
#---------------------------------------- Check loggedin status ---------------------------------------------------------#
class CheckLoggedInStatus(APIView):
    def post(self, request):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
             request.data.get('session_unique_uuid'))
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            else:
                return Response({"status" : True,"msg" :  "",
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
        except Exception as e:
            return Response({'status': False, 'msg': GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict(), 'loggedInStatus' : True})
#-----------------------------------------------------Change phone number-------------------------------------------------#
class ChangePhoneNumber(APIView):
    def randomPassword( self, request ):
        random_code = get_random_string(length=4, allowed_chars='123456789')
        randomKeycheck = NdUsers.objects.filter(verification_code=random_code, is_deleted=False).count()
        if randomKeycheck >0 :
            self.randomPassword( request )
        else:
            return random_code
    def get_unique_phone(self, request, user_id):
        lang = request.data['langC']
        # try:
        if not fieldEmptyCheck(request.data.get('phone_number')):
            return {'status': False, 'msg': ChangePhoneNumberMsgMod.Msg(lang, 'phone_number')}
        is_exists = NdUsers.objects.filter(Q(phone_number=request.data.get('phone_number')), Q(role_id=int(request.data.get('role_id'))), 
            Q(is_deleted=False), ~Q(id=user_id)).count()
        if is_exists >0 :
            return {'status': False, 'msg': DriverRegistrationMsgMod.Msg(lang, 'phone_number_already_reg')}
        else:
            return {'status': True}
        # except Exception as e:
        #   return {'status': False, 'msg': GenericMsgMod.Msg(lang, 'error-msg')}
    @transaction.atomic
    def post(self, request):
        lang = request.data['langC']
        try:
            loggedInStatus = get_latest_device_uuid_by_userid(int(request.data.get('session_user_id')),
             request.data.get('session_unique_uuid'))
            
            if not loggedInStatus:
                return Response({"status" : False,"msg" :  GenericMsgMod.Msg(lang, 'session_out'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            
            elif not fieldEmptyCheck(request.data.get('country_id')):
                return Response({"status" : False,"msg" :  ChangePhoneNumberMsgMod.Msg(lang, 'country_id'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('isd_code')):
                return Response({"status" : False,"msg" :  ChangePhoneNumberMsgMod.Msg(lang, 'isd_code'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
            elif not fieldEmptyCheck(request.data.get('role_id')):
                return Response({"status" : False,"msg" :  ChangePhoneNumberMsgMod.Msg(lang, 'role_id'),
                 "data" : dict(), 'loggedInStatus' : loggedInStatus})
        
            else:
                records = NdUsers.objects.filter(Q(phone_number=sanitize(request.data.get('phone_number'))), Q(role_id=int(request.data.get('role_id'))))    
                if records.count() >0:
                    random_code = self.randomPassword( request )
                    userDetails = records.values('id').first()
                    get_unique_phone = self.get_unique_phone(request, userDetails['id'])
                    if not get_unique_phone['status']:
                        return Response({"status" : False,"msg" :  get_unique_phone['msg'],
                         "data" : dict(), 'loggedInStatus' : loggedInStatus})
                    temp_phone_number = str(request.data.get('country_id')) + "~"+ str(request.data.get('phone_number'))
                    NdUsers.objects.filter(id=int(userDetails['id'])).update( verification_code=random_code,
                     temp_phone_number= temp_phone_number ) 
                    phone_no = request.data.get('phone_number')
                    firstChar =  phone_no[0]
                    
                    if firstChar == '0':
                        phone_no = phone_no.lstrip('0')
                    client.publish(
                        PhoneNumber=request.data.get('isd_code') + phone_no,
                        Message="Your Need Deliver verification code is " + random_code + "."
                    )
                    return Response({"status" : True,"msg":ChangePhoneNumberMsgMod.Msg(lang, 'otp_send'), "data" : dict(), 'loggedInStatus' : loggedInStatus})
                else:
                    return Response({"status" : False,"msg":ChangePhoneNumberMsgMod.Msg(lang, 'not_found'),
                        "data" : dict(), 'loggedInStatus' : loggedInStatus})
                
        except Exception as e:
          return Response({'status': False, 'msg': GenericMsgMod.Msg(lang, 'error-msg'), "data" : dict(), 'loggedInStatus' : loggedInStatus})
class DeleteRecord(APIView):
    def delete(self,request, pk):
        NdUsers.objects.filter(id=int(pk)).delete()
        return Response({"status" : False,"msg":"deleted"})

class TestSms(APIView):
    def sendPushToOlderLoggedInUser(self, request, customParam, dataFields):
        userIDS = dataFields['userIDS']
        if dataFields['deviceIDS']:
            deviceIDS = dataFields['deviceIDS']
        pushNotificationFCM.send_push_notification( deviceIDS, userIDS, 
            {"title": dataFields['title'], "body": dataFields['body'], "notification_type_id" : 4}, customParam)
        return True
    def post(self, request):
        if request.data.get('type') == 'sms':
            msg = "Need Deliver Test SMS"
            isd = request.data.get('isd')
            phone_num = request.data.get('phone_number')
            isMsgSend = sendGenericMessage( isd+phone_num, msg )
            return Response({"status" : False,"msg":"sms send"})
        else:
            message_title = 'Test Push'
            message_body = "Its for testing purpose"
            customParam = {}
            customParam['push_type'] = 100
            customParam['body'] = message_body
            customParam['title'] = message_title
            deviceIDs = [request.data.get('device_token')]
            result = push_service.notify_multiple_devices(registration_ids=deviceIDs, message_title=message_title, sound='notification.mp3', message_body=message_body, 
                data_message=customParam, content_available=True)
            return Response({"status" : False,"msg":"Push send", "result": str(result)})

class AppVersionChecker(APIView):
    def post(self, request): 
        lang = request.data.get('langC')
        try:
            if request.data.get('app_type') == 'DRIVER':
                device_type = request.data.get('device_type');
                settingData = NdSettings.objects.filter(alias_name=device_type, is_status=True, is_deleted=False).values('field_val')
                if settingData.count()>0:
                    recordObj = settingData.first()
                    if device_type == "driver_android_version":

                        if float(request.data.get('current_version')) < float(recordObj['field_val']):
                            return Response({"status": True, "latest_version": recordObj['field_val']})
                        else:
                            return Response({"status": False})
                    elif request.data.get('device_type') == "driver_ios_version":
                        
                        if float(request.data.get('current_version')) < float(recordObj['field_val']):
                            return Response({"status": True, "latest_version": recordObj['field_val']}) 
                        else:
                            return Response({"status": False})       
                    else:
                        return Response({"status": False})
                else:
                    return Response({"status": False})
            else:
                device_type = request.data.get('device_type');
                settingData = NdSettings.objects.filter(alias_name=device_type, is_status=True, is_deleted=False).values('field_val')
                if settingData.count()>0:
                    recordObj = settingData.first()
                    if device_type == "supplier_android_version":
                        if float(request.data.get('current_version')) < float(recordObj['field_val']):
                            return Response({"status": True, "latest_version": recordObj['field_val']})
                        else:
                            return Response({"status": False})
                    elif request.data.get('device_type') == "supplier_ios_version":

                        if float(request.data.get('current_version')) < float(recordObj['field_val']):
                            return Response({"status": True, "latest_version": recordObj['field_val']}) 
                        else:
                            return Response({"status": False})       
                    else:
                        return Response({"status": False})
                else:
                    return Response({"status": False})
        except Exception as e:
            return Response({'status' : False,  'msg': GenericMsgMod.Msg(lang, 'error-msg')})  
class Logout(APIView):
    def post(self, request):
        lang = request.data.get('langC')
        try:
            NdUsers.objects.filter(id=int(request.data.get('user_id'))).update(device_token=None)
            return Response({"status": True, "msg":"" })
        except Exception as e:
            return Response({'status' : False,  'msg': GenericMsgMod.Msg(lang, 'error-msg')})
class RemoveDeviceToken(APIView):
    def post(self, request):
        lang = request.data.get('langC')
        try:
            userDetails = NdUsers.objects.filter(device_token__icontains=request.data.get('device_token'), 
                role_id=int(request.data.get('role_id')))
            if userDetails.exists():
                NdUsers.objects.filter(device_token__icontains=request.data.get('device_token'), 
                    role_id=int(request.data.get('role_id'))).update(device_token=None)
                return Response({"status": True, "msg":"" })
            else:
                return Response({"status": True, "msg":"" })
        except Exception as e:
            return Response({'status' : False,  'msg': GenericMsgMod.Msg(lang, 'error-msg')})
class VersionCheckAutomatic(APIView):
    def post(self, request):
        import urllib3
        import json

        packageName = 'com.whatsapp'      # package com.whatsapp for WhatsApp
        apiKey      = 'wij5czxu3mxkzkt9'  # your API key

        url = 'http://api.playstoreapi.com/v1.1/apps/{0}?key={1}'
        http = urllib3.PoolManager()
        response = http.request('GET', 'http://api.playstoreapi.com/v1.1/apps/{0}?key={1}')
        # response = urllib2.urlopen(url.format(packageName, apiKey))

        print (response)
        return Response({'status' : False,  'msg': response})
class AutoDeviceTokenUpdate(APIView):
    def post(self, request):
        lang = request.data.get('langC')
        try:
            if not fieldEmptyCheck(request.data.get('device_token')):
                return Response({'status' : False, 'msg': GenericMsgMod.Msg(lang, 'error-msg')})
            else:
                userDetails = NdUsers.objects.filter(id=int(request.data.get('user_id'))).values('device_token').first()
                if not fieldEmptyCheck(userDetails['device_token']):
                    NdUsers.objects.filter(id=int(request.data.get('user_id'))).update(device_token=request.data.get('device_token'))
                if userDetails['device_token'] != request.data.get('device_token'):
                    NdUsers.objects.filter(id=int(request.data.get('user_id'))).update(device_token=request.data.get('device_token'))   
                return Response({"status": True, "msg":"" })
        except Exception as e:
            return Response({'status' : False,  'msg': GenericMsgMod.Msg(lang, 'error-msg')})

class CheckAccountStatus(APIView):
    def post(self, request):
        lang = request.data.get('langC')
        try:
            userDetails = NdUsers.objects.filter(id=request.data.get('user_id')).values('is_status', 'is_deleted').first()
            if not userDetails['is_status']:
                    return {"status": False, "msg": DriverLoginMsgMod.Msg(lang, 'deactivated')}
            elif userDetails['is_deleted']:
                return {"status": False, "msg": DriverLoginMsgMod.Msg(lang, 'deleted')}
            else:
                return {"status": True, "msg": ""}
        except Exception as e:
            return Response({'status' : False,  'msg': GenericMsgMod.Msg(lang, 'error-msg')})