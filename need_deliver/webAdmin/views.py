from django.shortcuts import render, redirect

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .serializers import *
from .models import *
from rest_framework import *
# from django.views.decorators.csrf import requires_csrf_token
from django.template import RequestContext
from rest_framework.views import APIView
from Crypto.Cipher import AES
from django.utils.crypto import get_random_string
from Crypto.Cipher import XOR
import base64
from django.template import loader
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives

from django.db.models import Value
from django.db.models.functions import Concat
from .message import *
import json

from django.db.models import F, Q, Count, Min, Sum, Avg, FloatField, ExpressionWrapper

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static

from dateutil import parser
# from datetime import datetime
import datetime
import time
from commonApp.views import fieldEmptyCheck
from django.utils import timezone

from pyfcm import FCMNotification
push_service = FCMNotification(api_key=settings.FCM_API_KEY)
# import os
# from django.core.files.storage import default_storage
# import tempfile

# Create your views here. 
def encrypt( plaintext):
  key = settings.MASTER_KEY
  cipher = XOR.new(key)
  return base64.b64encode(cipher.encrypt(plaintext))

def decrypt( ciphertext):
  key = settings.MASTER_KEY
  cipher = XOR.new(key)
  return cipher.decrypt(base64.b64decode(ciphertext))
def encrypt_val(clear_text):
    clear_text = clear_text
    enc_secret = AES.new(settings.MASTER_KEY[:32])
    tag_string = (str(clear_text) +
                  (AES.block_size -
                   len(str(clear_text)) % AES.block_size) * "\0")
    cipher_text = base64.b64encode(enc_secret.encrypt(tag_string))
    return cipher_text.decode('utf-8')
def decrypt_val(cipher_text):
    dec_secret = AES.new(settings.MASTER_KEY[:32])
    raw_decrypted = dec_secret.decrypt(base64.b64decode(cipher_text))
    clear_val = raw_decrypted.decode().rstrip("\0")
    return clear_val
class user(APIView):
    	# @csrf_exempt
    def get( self, request ):
        data = {}
        if 'authSession' not in request.session:
            url = request.META['PATH_INFO'].split('/')
            urlSegments = list(filter(None, url)) 
            data['current_url_segments'] = urlSegments
            return render( request, 'user/login.html', data)
        else:
            return redirect("dashboard")
			# return render( request, 'dashboard/dashboard.html', data)

	#------------------------ POST method to login -------------------------------------#   
	# @requires_csrf_token
    def post(self, request, format=None):
        self.errorResult = list()
        user = self.get_user(request.data)
        # # data['csrfContext'] = csrfContext
        if self.errorResult:
            return Response(self.errorResult)
        else:
            if( user['role']['id'] != int(request.data["role"])):
                self.errorResult.append({"status" : False,"msg" : "Sorry! You are not authorised.", "field": "mainError"})
            # elif( user['is_status'] == False ):
            # 	self.errorResult.append({"status" : False,"msg" : "Sorry! Your a/c is deactivated.", "field": "mainError"})
            if not self.errorResult:
                
                self.setSession(request, user)
                data = {}
                data['title'] = "Dashboard"
                data['page_title'] = "Dashboard"
                url = request.META['PATH_INFO'].split('/')
                urlSegments = list(filter(None, url)) 
                return Response([{"status" : True, "data" : user, "msg" : "Congrats! You have successfully logged in"}])
            else:
                return Response(self.errorResult)

	# @csrf_exempt
    def get_user(self, request):
        try:
            if (request.get('email_id')==""):
                self.errorResult.append({"status" : False,"msg" : "Please enter your username", "field": "email_id"})
            if(request.get('password')==''):
                self.errorResult.append({"status" : False,"msg" : "Please enter your password", "field": "password"})
            if not self.errorResult:
                password = str(encrypt_val(request.get('password')))

                records = NdUsers.objects.get((Q(email_id=request.get('email_id')) | Q(username=request.get('email_id'))), password=password, role=request.get('role'), is_status=True)
                
                ndUsersSerializer = NdUsersSerializer(records)
                if ndUsersSerializer.data:
                    return ndUsersSerializer.data
                else:
                    self.errorResult.append({"status" : False,"msg" : "Please check your given details", "field": "mainError"})
            else:
                return self.errorResult     
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Please check your username and password", "field": "mainError"})
            return self.errorResult
		#------------------------ Set session and var name authSession -------------------------------------#
    def setSession(self, request, sessionVar):
        if sessionVar:
            request.session["authSession"] = sessionVar
            request.session.set_expiry(3000) # 60 for 1 minute
            

	#------------------------ Get method to logout -------------------------------------#   
	

def dashboard( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Dashboard"
        data['page_title'] = "Dashboard"
        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        # print(urlSegments)
        data['current_url_segments'] = urlSegments
       
        vehicleDetails = NdVehicleType.objects.filter(is_status=True, is_deleted=False)
        vehicleTypeSerializer = NdVehicleTypeSerializer(vehicleDetails, many=True)
        
        langNames = ""
        colorCodes = ""
        no_of_calls = ""
        i = 0
        tmpData = ""
        for item in vehicleTypeSerializer.data:
            orderCountRespectiveVehicle = NdOrder.objects.filter(is_status=True, is_deleted=False, vehicles_type__id=item['id']).count()
            tmpData = tmpData + str(orderCountRespectiveVehicle) + "~"+item['vehicle_type_name'] + "||"
        data['vehicleTypeName'] = tmpData.rstrip("||")
        # print( (tmpData))
        return render( request, 'dashboard/dashboard.html', data)
    else:
        return redirect("login")

@api_view(['GET', 'POST', ])
def logout(request, format=None):
    if 'authSession' in request.session:
        del request.session['authSession']
        return Response([{"status" : True, "msg" : "Congrats! You have successfully signed out from our system"}])
    # return redirect("login")

#------------------------------------------------------------ForgotPasswordMailSend--------------------------------------------------------#
class ForgotPasswordMailSend( APIView ):
    errorResult = []
    
    def checkUserNameExistance( self, request ):
        
        emailChecking = NdUsers.objects.filter(email_id=request.data.get('forgot_username'), is_deleted=False).count()
        if emailChecking > 0:
            return True
        else:
            return False
    
        # if request.
    def randomPassword( self, request ):
        random_code = get_random_string(length=6, allowed_chars='1234567890')
        randomKeycheck = NdUsers.objects.filter(random_key=random_code, is_deleted=False).count()
        if randomKeycheck >0 :
            self.randomPassword( request )
        else:
            return random_code
        # if request.
    def post( self, request ):
        self.errorResult = list()     
        checkUserNameExistance = self.checkUserNameExistance( request )
        if request.data['forgot_username'] == "":
            self.errorResult.append({'status' : False, 'msg' : "Email ID field can not be blank", 'field': "forgot_username"})
        elif not checkUserNameExistance :
            self.errorResult.append({'status' : False, 'msg' : "Email ID does not exists", 'field': "forgot_username"})
        if self.errorResult:
            return Response(self.errorResult)
        else:
            random_code = self.randomPassword( request )
            recordDetails = NdUsers.objects.get(email_id=request.data['forgot_username']) 
            ndUsersSerializer = NdUsersSerializer(recordDetails,many=False)
            NdUsers.objects.filter(email_id= request.data.get('forgot_username'), is_deleted=False).update( random_key=random_code ) 
            
            html_message = loader.render_to_string(
                'email_templates/forgot_password_code_admin.html',
                {
                    'users_name': ndUsersSerializer.data['first_name'],
                    'random_key': str(encrypt(random_code))
                }
            )
            # return Response({'from : ':settings.NO_REPLY_MAIL,'to mail : ':request.data['forgot_username']})
            
            
            try:
                send_mail('Verify your Identity', html_message, settings.NO_REPLY_MAIL,[request.data['forgot_username']],fail_silently=False,
    html_message=html_message,) 
                return Response([{'status': True, 'msg' : 'Security code has been sent'}])
            except Exception as e:
                return Response([{'status': False, 'msg' : 'Something went wrong'}])
            return Response([{"status" : True,"msg" : 'You have successfully reset your password'}]) 

class Change_password( APIView ):
    def checkOldPassword( self, request ,ID):

        checkOldPass = NdUsers.objects.filter(password=encrypt_val(request.get('old_password')), id=ID).count()
        if checkOldPass == 0:
            return False
        else:
            return True

    def post( self, request, format=None ):
        self.errorResult = list()
        ID = int(request.session['authSession']['id'])
        if request.data['old_password'] == "" :
             self.errorResult.append({"status" : False,"msg" : "Old Password can not be blank", "field": "old_password"})
        elif not self.checkOldPassword( request.data , ID) :
             self.errorResult.append({"status" : False,"msg" : "Old Password does not match", "field": "old_password"})
        if request.data['new_password'] == "" :
             self.errorResult.append({"status" : False,"msg" : "New Password can not be blank", "field": "new_password"})
        elif request.data['new_password'] == request.data['old_password'] :
             self.errorResult.append({"status" : False,"msg" : "New Password is same as old", "field": "new_password"})
        if request.data['confirm_password'] == "" :
             self.errorResult.append({"status" : False,"msg" : "Confirm Password can not be blank", "field": "confirm_password"})  
        elif request.data['new_password'] != request.data['confirm_password'] :
             self.errorResult.append({"status" : False,"msg" : "Confirm Password does not match", "field": "confirm_password"})
        if self.errorResult:
            return Response(self.errorResult)
        else:
            NdUsers.objects.filter(Q(id = ID)).update( password=encrypt_val(request.data['new_password'])) 
            return Response([{"status" : True,"msg" : 'You have successfully reset your password'}])


class ResetPassword( APIView ):
    errorResult = []
    # print('ddddd');
    def post( self, request ):
        self.errorResult = list()     
        if request.data['new_password'] == "":
            self.errorResult.append({'status' : False, 'msg' : "New password can not be blank", 'field' : "new_password"})
        if request.data['confirm_password'] == "":
            self.errorResult.append({'status' : False, 'msg' : "Confirm password can not be blank", 'field' : "confirm_password"})
        if request.data['confirm_password'] != request.data['new_password'] :
            self.errorResult.append({'status' : False, 'msg' : "Confirm Password does not match", 'field' : "confirm_password"})
        if request.data['token'] =="" :
            self.errorResult.append({'status' : False, 'msg' : "Something went wrong", 'field' : "mainError"})
        if self.errorResult:
            return Response(self.errorResult)
        else:
            token = request.data['token']
            # token = token.split("b'")[1] 
            # token = token.replace("'",'')

            token = decrypt(token).decode('utf-8')
            
            # return Response({'d': decryptToken})
            decryptToken = int(token)

            try:
                recordDetails = NdUsers.objects.filter(random_key=decryptToken, is_deleted=False).count() 
                if recordDetails >0 :
                    NdUsers.objects.filter(random_key= decryptToken,is_deleted=False).update( password=encrypt_val(request.data['new_password']), random_key=None) 
                    return Response([{'status' : True, 'msg' : "Your password has been changed"}])
                else:
                    return Response([{'status' : False, 'msg' : "You are not authorized to reset password", 'field' : "mainError"}])
            except Exception as e:
                return Response([{'status' : False, 'msg' : "You are not authorized to reset password", 'field' : "mainError"}])
def reset_password(  request ):
    data = {}
    data['title'] = "Reset Password"
    data['page_title'] = "Reset Password"
    url = request.META['PATH_INFO'].split('/')
    urlSegments = list(filter(None, url)) 
    data['current_url_segments'] = urlSegments
    data['error'] = False
    try:
        encriptCode = request.GET['token']
        decodes = encriptCode.split("'")[1] 
        data['decodes'] = decodes
        decodes = decrypt(decodes).decode('utf-8')
        
    
        if not decodes:

            return redirect("/")
        elif encriptCode == "":

            return redirect("/")
        if 'authSession' not in request.session:

            recordDetails = NdUsers.objects.filter(random_key= decodes).count() 

            if recordDetails == 0:
                return redirect("/")
            else:

                return render( request, 'reset/reset.html', data)
        
        else:
            return redirect("dashboard")
    except Exception as e:
        data['error'] = "Sorry!! this link has been expired."
        return render( request, 'reset/reset.html', data)

# def languages( request ):
#     if 'authSession' in request.session:
#         data = {}
#         data['title'] = "Language Management"
#         data['page_title'] = "Language Management"
#         #---------------------------------All Countries--------------------------#

#         # allActiveStudent = NdLanguages.objects.filter(is_status=True, is_deleted= False).count() 
#         # data['totalActive'] = allActiveStudent

#         url = request.META['PATH_INFO'].split('/')
#         urlSegments = list(filter(None, url)) 
#         # print(urlSegments)
#         data['current_url_segments'] = urlSegments
#         return render( request, 'languages/lists/lists.html', data)
#     else:
#         return redirect("/")

#-------------------------------------------------------------- States Management START -----------------------------------------------------------------------#
# class States( APIView ):
#     errorResult = []
   
#     #------------------------ GET method to get list of States -------------------------------------#     
#     def get(self, request, id, format=None):
              
#         allRecord = NdStates.objects.filter(country_id=id).order_by('state_name')
#         ndStatesSerializer = NdStatesSerializer(allRecord, many=True)
#         if ndStatesSerializer.data:
#             return Response([{"status" : True, "data" : ndStatesSerializer.data}])
#         else:
#             return Response([{"status" : False}])
#     def get_query(self, request,hh):
#         '''
#         Returns query with all the objects
#         :return:
#         '''
#         if not self.query:
#             self.query = self.session.query(self.model_class)
#         return self.query
    
#     #------------------------ PUT method to update States by ID -------------------------------------#
#     def put(self, request, pk, format=None):
#         self.errorResult = list()
#         get_unique = self.get_unique(request.data)
#         if(get_unique['status'] == False):
#             self.errorResult.append({"status" : False,"msg" : get_unique['msg'], "field": "state_name"})
        
#         if self.errorResult:
#             return Response(self.errorResult)
#         else:
#             u = NdStates(id=int(request.data.get('id')), country_id= int(request.data.get('country')))
#             flntStatesSerializer = FlntStatesSerializer( u, data=request.data )

#             if flntStatesSerializer.is_valid():
#                 flntStatesSerializer.save()
#             return Response([{"status" : True, "data" : flntStatesSerializer.data, "msg" : "You have successfully updated the record"}])
#------------------------ Single States Details by ID BY GET -------------------------------------#
# class RecordDetailsStates(APIView):
#     def get(self, request, pk, format =None):
#         recordDetails = NdStates.objects.filter(id=pk).first()
#         flntStatesSerializer = FlntStatesSerializer(recordDetails)
#         if flntStatesSerializer.data:
#             return Response([{"status" : True, "data" : flntStatesSerializer.data}])
#         else:
#             return Response([{"status" : False, "msg" : "Sorry! No record is found"}])

#---------------------- Vehicle type ----------------------------
def vehicletype_list( request ):
    
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Vehicle type Management"
        data['page_title'] = "Vehicle type Management"
        #---------------------------------All Countries--------------------------#
        

        allActiveData = NdUsers.objects.filter(is_status=True, is_deleted= False,role=settings.IS_DRIVER).count() 
        data['totalActive'] = allActiveData

        allDeactiveData = NdVehicleType.objects.filter(is_status=False, is_deleted= False).count() 
        data['totalDeactive'] = allDeactiveData

        data['WEBADMIN'] = settings.WEBADMIN_URL

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        # print(urlSegments)
        data['current_url_segments'] = urlSegments
        data['app_name'] = "vehicle_type"
        return render( request, './vehicle_type/vehicle_lists.html', data)
    else:
        return redirect("/")

class vehicletype(APIView):
  #------------------------ Get method to get all customer -------------------------------------# 
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'vehicle_type_name',
            2 : 'khr',
            3 : 'person_capcity'
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]
        if draw == "1" :
            sortingType = "desc"
            sortingColumn = 0
        totalRecords = NdVehicleType.objects.filter(is_deleted =False).count()
        totalFiltered = totalRecords
        allRecord = NdVehicleType.objects.filter(is_deleted =False)
        
        if searchQ:
            allRecord = allRecord.filter(Q(vehicle_type_name__icontains=searchQ) )

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndSerializer = NdVehicleTypeSerializer(allRecord, many=True)
        
        # return Response({ 'recordsFiltered' : flntUsersSerializer.data})
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               tmpRow = []
               featuredMode = ''
               logo = ''
               if item['vehicle_logo']:
                    image = '<img src="'+ item['vehicle_logo']+'?time='+ str(datetime.datetime.now())+' " class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               else:
                    image = '<img src="'+ static('images/avatar.jpg')+'" class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               
               if item['top_view_logo']:
                    top_view_logo = '<img src="'+ item['top_view_logo']+'?time='+ str(datetime.datetime.now())+' " class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               else:
                    top_view_logo = '<img src="'+ static('images/avatar.jpg')+'" class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               

               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
                   
               
               tmpRow.append(item['id'])
               tmpRow.append(image)
               tmpRow.append(top_view_logo)
               tmpRow.append(item['vehicle_type_name'])
               tmpRow.append(item['base_fare'])
               tmpRow.append(item['khr'])
               tmpRow.append(item['person_capcity'])

               
               tmpRow.append(statusMsg)
               # tmpRow.append(action)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        # return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        #------------------------ Put method to update details By ID -------------------------------------#     
    def put(self, request, pk, format=None):
        try:
            self.errorResult = list()
            if(request.data["vehicle_type_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Vehicletype Name can not be blank", "field": "first_name"})
           
            if self.errorResult:
                return Response(self.errorResult)
                # return Response({"o":request.data["country_id"]})
            else:
                print(request.data)
                if bool(request.FILES.get('vehicle_logo', False)) == True:
                    v = NdVehicleType.objects.get(id = pk)
                    ndVehicleTypeLogoSerializer = NdVehicleTypeLogoSerializer(v, data={'vehicle_logo' : request.FILES['vehicle_logo']})
                    if ndVehicleTypeLogoSerializer.is_valid():
                        ndVehicleTypeLogoSerializer.save()

                if bool(request.FILES.get('top_view_logo', False)) == True:
                    v = NdVehicleType.objects.get(id = pk)
                    ndVehicleTypeTopViewLogoSerializer = NdVehicleTypeTopViewLogoSerializer(v, data={'top_view_logo' : request.FILES['top_view_logo']})
                    if ndVehicleTypeTopViewLogoSerializer.is_valid():
                        ndVehicleTypeTopViewLogoSerializer.save()
                            
                if request.data['vehicle_logo'] == 'undefined':
                    NdVehicleType.objects.filter(id=pk).update( vehicle_type_name=request.data['vehicle_type_name'], base_fare=request.data['base_fare'], khr=request.data['khr'], person_capcity= request.data['person_capcity'])
                 

                    
                    
                return Response([{"status" : True, "msg" : "You have successfully updated the record"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Please check not saved yet", "field": "mainError"})
            return Response(self.errorResult)

    #------------------------ POST method to Insert  details -------------------------------------# 
    def post(self, request, format=None):
        try:
            self.errorResult = list()
            
            if(request.data["vehicle_type_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Vehicle type name can not be blank", "field": "vehicle_type_name"})
            
            else:
                NdVehicleTypeObj = NdVehicleType(vehicle_type_name=request.data['vehicle_type_name'], base_fare=request.data['base_fare'], khr=request.data['khr'], person_capcity= request.data['person_capcity'],top_view_logo=request.FILES.get('top_view_logo'),vehicle_logo=request.FILES.get('vehicle_logo'))
                NdVehicleTypeObj.save()
                

                data = {};
                allActiveData = NdVehicleType.objects.filter(is_status=True, is_deleted= False).count() 
                data['totalActive'] = allActiveData

                allDeactiveData = NdVehicleType.objects.filter(is_status=False, is_deleted= False).count() 
                data['totalDeactive'] = allDeactiveData

                return Response([{"status" : True, "data" : data, "msg" : "You have successfully created", 'updated_record' : data}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Sorry! failed to save data", "field": "mainError"})
            return Response(self.errorResult)

#------------------------ Single User Details by ID BY GET -------------------------------------#
class RecordDetailsVehicleType(APIView):
    def get(self, request, id, format =None):
      recordDetails = NdVehicleType.objects.filter(id=id).first()
      ndSerializer = NdVehicleTypeSerializer(recordDetails)
      if ndSerializer.data:
          return Response([{"status" : True, "data" : ndSerializer.data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])
#------------------------ Update multiple records BY LIST ID -------------------------------------#
class UpdateMultiRecordVehicleType(APIView):
    
    # tblArray = { }
    def post(self, request, format=None):
        # send_mail("hello paul", "comment tu vas?", "arijit.chandra@navsoft.in", ['arijit.chandra@navsoft.in'],fail_silently=False,)         
        # return Response({'status' : True,'sss': '1'})
       
        countingInfo = []
        if request.data['action'] == 'is_status' or request.data['action'] == 'rm':
            id_list = json.loads(request.data['ids']) 
            value = True
            if( request.data['value'] != '1'):
                value = False
           
            if request.data['action'] == 'is_status':
                NdVehicleType.objects.filter(id__in=id_list).update(is_status=value)

            if request.data['action'] == 'rm':
                NdVehicleType.objects.filter(id__in=id_list).update(is_deleted=value)
           
            allActivedata = NdVehicleType.objects.filter(is_status=True, is_deleted= False).count() 
           
            countingInfo.append({'totalActiveCustomers' : allActivedata})

            allDeactiveData = NdVehicleType.objects.filter(is_status=False, is_deleted= False).count() 
            
            countingInfo.append({'allDeactiveCustomer' : allDeactiveData})

            allCustomer = NdVehicleType.objects.filter(is_deleted= False).count() 
            # allTeacherallTeacher = allCustomer
            countingInfo.append({'allCustomer' : allCustomer})
                
            return Response([{"status" : True, "countingInfo" : countingInfo}])
        else:
            return Response([{'status': False, 'msg' : 'Something went wrong'}])
# ------------------------Banner image --------------------------------------------------

def image_list( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Banner Management"
        data['page_title'] = "Banner Management"

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        totalImageRecords = NdImage.objects.filter(is_deleted =False).count()
        data['total_image_records'] = totalImageRecords
        data['current_url_segments'] = urlSegments
        data['BASE_URL'] = settings.BASE_URL
        return render( request, './image/image_files.html', data)
    else:
        return redirect("/")


class imagefile(APIView):
  #------------------------ Get method to get all customer -------------------------------------# 
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'title',
            2 : 'applied_to',
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]
        if draw == "1" :
            sortingType = "desc"
            sortingColumn = 0
        totalRecords = NdImage.objects.filter(is_deleted =False).count()
        totalFiltered = totalRecords
        allRecord = NdImage.objects.filter(is_deleted =False)
        if searchQ:
            allRecord = allRecord.filter(Q(title__icontains=searchQ) | Q(applied_to__icontains=searchQ))

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndSerializer = NdImageSerializer(allRecord, many=True)
        # return Response({ 'recordsFiltered' : flntUsersSerializer.data})
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               tmpRow = []
               featuredMode = ''
               image = ''
               
               if item['image_file']:
                    image = '<img src="'+ item['image_file']+ '" class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               else:
                    image = '<img src="'+ static('/static/images/avatar.jpg')+'" class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               
               

               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
                   
             
               tmpRow.append(item['id'])
               tmpRow.append(image)
               # tmpRow.append(item['title'])
               tmpRow.append(item['title'])
               tmpRow.append(item['applied_to'])

               tmpRow.append(statusMsg)
               # tmpRow.append(action)
               ajaxData.append(tmpRow)
               i+=1
               
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        # return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        #------------------------ Put method to update customer details By ID -------------------------------------#     
    def put(self, request, pk, format=None):
        try:
            self.errorResult = list()
            if(request.data["title"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Title can not be blank", "field": "title"})
            
            if self.errorResult:
                return Response(self.errorResult)
            else:
                request.POST._mutable = True
                
                recordDetails = NdImage.objects.filter(id=pk).first()
                details = NdImageSerializer(recordDetails)
                if request.data['image_file'] == 'undefined':
                    NdImage.objects.filter(id=pk).update(title=request.data['title'])
                else:     
                    ndImageSerializer = NdImageSerializer(data=request.data)

                    if ndImageSerializer.is_valid():
                        # Making the is_deleted true and inserting a new record 
                        NdImage.objects.filter(id=pk).update(is_deleted=True)
                        ndImageSerializer.save()
                    else:
                        print(ndImageSerializer.errors)
               
                
                return Response([{"status" : True, "msg" : "You have successfully updated the record"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Sorry! data not updated", "field": "mainError"})
            return Response(self.errorResult)

    #------------------------ POST method to Insert customer details -------------------------------------# 
    def post(self, request, format=None):
        try:
            self.errorResult = list()
            title = request.POST.get('title', False)
            
            if(title == ""):
                self.errorResult.append({"status" : False,"msg" : "Title can not be blank", "field": "title"})
            
            else:
                ndImageSerializer = NdImageSerializer(data=request.data)

                if ndImageSerializer.is_valid():
                    ndImageSerializer.save()
                else:
                    # ndUsersCreateSerializer.errors
                    print("===========================================")
                    print(ndImageSerializer.errors)
                    print("===========================================")
                return Response([{"status" : True,  "msg" : "You have successfully created"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Sorry! Data not saved", "field": "mainError"})
            return Response(self.errorResult)

#------------------------ Single User Details by ID BY GET -------------------------------------#
class RecordDetailsImage(APIView):
    def get(self, request, id, format =None):
      recordDetails = NdImage.objects.filter(id=id).first()
      ndSerializer = NdImageSerializer(recordDetails)
      if ndSerializer.data:
          return Response([{"status" : True, "data" : ndSerializer.data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])
#------------------------ Update multiple records BY LIST ID -------------------------------------#
class UpdateMultiRecordImage(APIView):
    
    # tblArray = { }
    def post(self, request, format=None):
        countingInfo = []
        if request.data['action'] == 'is_status' or request.data['action'] == 'rm':
            id_list = json.loads(request.data['ids']) 
            value = True
            if( request.data['value'] != '1'):
                value = False
           
            if request.data['action'] == 'is_status':
                NdImage.objects.filter(id__in=id_list).update(is_status=value)

            if request.data['action'] == 'rm':
                NdImage.objects.filter(id__in=id_list).update(is_deleted=value)

            totalImageRecords = NdImage.objects.filter(is_deleted =False).count()
            
           
            return Response([{"status" : True, "total_image_records" : totalImageRecords,'msg' : 'Data updated successfully'}])
        else:
            return Response([{'status': False, 'msg' : 'Something went wrong1'}])


# ----------------- Splash screen management -------------------------------------

def splah_screen_list( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Splash Screen Management"
        data['page_title'] = "Splash Screen Management"

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        data['current_url_segments'] = urlSegments
        return render( request, './splash_screen/splash_screen.html', data)
    else:
        return redirect("/")

class splash_screen(APIView):
  #------------------------ Get method to get all data list -------------------------------------# 
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'heading',
            2 : 'splash_text'
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]
        if draw == "1" :
            sortingType = "desc"
            sortingColumn = 0
        totalRecords = NdSplashScreen.objects.filter(is_deleted =False).count()
        totalFiltered = totalRecords
        allRecord = NdSplashScreen.objects.filter(is_deleted =False)
        if searchQ:
            allRecord = allRecord.filter(Q(heading__icontains=searchQ) | Q(splash_text__icontains=searchQ))

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndSerializer = NdSplashScreenSerializer(allRecord, many=True)
        
        # return Response({ 'recordsFiltered' : flntUsersSerializer.data})
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               tmpRow = []
               featuredMode = ''
               image = ''
               if item['image_file']:
                    image = '<img src="'+ item['image_file']+'?time='+ str(datetime.datetime.now())+' " class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               else:
                    image = '<img src="'+ static('images/avatar.jpg')+'" class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               
               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
                   
               
               
               tmpRow.append(item['id'])
               tmpRow.append(image)
               tmpRow.append(item['heading'])
               tmpRow.append(item['splash_text'])
               tmpRow.append(statusMsg)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        
        #------------------------ Put method to update customer details By ID -------------------------------------#     
    def put(self, request, pk, format=None):
        try:
            self.errorResult = list()
            
            if(request.data["heading"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Heading can not be blank", "field": "heading"})
           
            if self.errorResult:
                return Response(self.errorResult)
            else:
                if request.data['image_file'] == 'undefined':
                    NdSplashScreen.objects.filter(id=pk).update(heading=request.data['heading'], splash_text=request.data['splash_text'])
                else:     
                    ndSerializer = NdSplashScreenSerializer(data=request.data)

                    if ndSerializer.is_valid():
                        # Making the is_deleted true and inserting a new record 
                        NdSplashScreen.objects.filter(id=pk).update(is_deleted=True)
                        ndSerializer.save()
                    else:
                        print("===========================================")
                        print(ndSerializer.errors)
                        print("===========================================")
                return Response([{"status" : True, "msg" : "You have successfully updated the record"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Please resize the image before upload", "field": "mainError"})
            return Response(self.errorResult)

    #------------------------ POST method to Insert customer details -------------------------------------# 
    def post(self, request, format=None):
        try:
            self.errorResult = list()
            if(request.data["heading"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Heading can not be blank", "field": "heading"})
            
            else:
                ndSerializer = NdSplashScreenSerializer(data=request.data)
                if ndSerializer.is_valid():
                    ndSerializer.save()
                else:
                    print("===========================================")
                    print(ndSerializer.errors)
                    print("===========================================")
                data = {};
                allActiveData = NdSplashScreen.objects.filter(is_status=True, is_deleted= False).count() 
                data['totalActive'] = allActiveData

                allDeactiveData = NdSplashScreen.objects.filter(is_status=False, is_deleted= False).count() 
                data['totalDeactive'] = allDeactiveData

                return Response([{"status" : True, "data" : data, "msg" : "You have successfully created", 'updated_record' : data}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Sorry! Data not saved", "field": "mainError"})
            return Response(self.errorResult)

#------------------------ Single Details by ID BY GET -------------------------------------#
class RecordDetailsSplashscreen(APIView):
    def get(self, request, id, format =None):
      recordDetails = NdSplashScreen.objects.filter(id=id).first()
      ndSerializer = NdSplashScreenSerializer(recordDetails)
      if ndSerializer.data:
          return Response([{"status" : True, "data" : ndSerializer.data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])
#------------------------ Update multiple records BY LIST ID -------------------------------------#
class UpdateMultiRecordSplashScreen(APIView):
    def post(self, request, format=None):
        countingInfo = []
        if request.data['action'] == 'is_status' or request.data['action'] == 'rm':
            id_list = json.loads(request.data['ids']) 
            value = True
            if( request.data['value'] != '1'):
                value = False
           
            if request.data['action'] == 'is_status':
                NdSplashScreen.objects.filter(id__in=id_list).update(is_status=value)

            if request.data['action'] == 'rm':
                NdSplashScreen.objects.filter(id__in=id_list).update(is_deleted=value)
            
            return Response([{"status" : True, "msg" : 'Updated record successfully'}])
        else:
            return Response([{'status': False, 'msg' : 'Something went wrong'}])

# **************** Cancellation request management **************************

def cancellation_reason_list( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Cancellation Reason Management"
        data['page_title'] = "Cancellation Reason Management"

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        data['current_url_segments'] = urlSegments
        return render( request, './cancellation_reason/cancellation_reason.html', data)
    else:
        return redirect("/")

class cancellation_reason(APIView):
  #------------------------ Get method to get all data list -------------------------------------# 
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'reason'
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]
        if draw == "1" :
            sortingType = "desc"
            sortingColumn = 0
        totalRecords = NdCancellationReason.objects.filter(is_deleted =False).count()
        totalFiltered = totalRecords
        allRecord = NdCancellationReason.objects.filter(is_deleted =False)
        if searchQ:
            allRecord = allRecord.filter(Q(reason__icontains=searchQ))

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndSerializer = NdCancellationReasonSerializer(allRecord, many=True)
        
        # return Response({ 'recordsFiltered' : flntUsersSerializer.data})
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               tmpRow = []
               featuredMode = ''
               
               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
                                  
               
               tmpRow.append(item['id'])
               tmpRow.append(item['reason'])
               tmpRow.append(statusMsg)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        
        #------------------------ Put method to update customer details By ID -------------------------------------#     
    def put(self, request, pk, format=None):
        try:
            self.errorResult = list()
       
            if(request.data["reason"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Reason can not be blank", "field": "heading"})
           
            if self.errorResult:
                return Response(self.errorResult)
            else:
                request.POST._mutable = True
                
                recordDetails = NdCancellationReason.objects.filter(id=pk).first()
                details = NdCancellationReasonSerializer(recordDetails)
            
                NdCancellationReason.objects.filter(id=pk).update( reason=request.data['reason'])  

           
                return Response([{"status" : True, "msg" : "You have successfully updated the record"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Sorry! Data not updated", "field": "mainError"})
            return Response(self.errorResult)

    #------------------------ POST method to Insert customer details -------------------------------------# 
    def post(self, request, format=None):
        try:
            self.errorResult = list()
            if(request.data["reason"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Reason can not be blank", "field": "heading"})
            
            else:
                ndSerializer = NdCancellationReasonSerializer(data=request.data)
                if ndSerializer.is_valid():
                    ndSerializer.save()
                else:
                    print("===========================================")
                    print(ndSerializer.errors)
                    print("===========================================")
                data = {};
                allActiveData = NdCancellationReason.objects.filter(is_status=True, is_deleted= False).count() 
                data['totalActive'] = allActiveData

                allDeactiveData = NdCancellationReason.objects.filter(is_status=False, is_deleted= False).count() 
                data['totalDeactive'] = allDeactiveData

                return Response([{"status" : True, "data" : data, "msg" : "You have successfully created cancellation reason", 'updated_record' : data}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Sorry! Data not saved", "field": "mainError"})
            return Response(self.errorResult)

#------------------------ Single Details by ID BY GET -------------------------------------#
class RecordDetailsCancellationReason(APIView):
    def get(self, request, id, format =None):
      recordDetails = NdCancellationReason.objects.filter(id=id).first()
      ndSerializer = NdCancellationReasonSerializer(recordDetails)
      if ndSerializer.data:
          return Response([{"status" : True, "data" : ndSerializer.data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])
#------------------------ Update multiple records BY LIST ID -------------------------------------#
class UpdateMultiRecordCancellationReason(APIView):
    def post(self, request, format=None):
        countingInfo = []
        if request.data['action'] == 'is_status' or request.data['action'] == 'rm':
            id_list = json.loads(request.data['ids']) 
            value = True
            if( request.data['value'] != '1'):
                value = False
           
            if request.data['action'] == 'is_status':
                NdCancellationReason.objects.filter(id__in=id_list).update(is_status=value)

            if request.data['action'] == 'rm':
                NdCancellationReason.objects.filter(id__in=id_list).update(is_deleted=value)
            
            return Response([{"status" : True, "msg" : 'Updated record successfully'}])
        else:
            return Response([{'status': False, 'msg' : 'Something went wrong'}])

# **************** Parcel info management **************************

def parcel_info_list( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Parcel informations Management"
        data['page_title'] = "Parcel informations Management"

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        data['current_url_segments'] = urlSegments
        return render( request, './parcel_information/parcel_information.html', data)
    else:
        return redirect("/")

class parcel_information(APIView):
  #------------------------ Get method to get all data list -------------------------------------# 
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'item_name'
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]
        if draw == "1" :
            sortingType = "desc"
            sortingColumn = 0
        totalRecords = NdParcelInformations.objects.filter(is_deleted =False).count()
        totalFiltered = totalRecords
        allRecord = NdParcelInformations.objects.filter(is_deleted =False)
        if searchQ:
            allRecord = allRecord.filter(Q(item_name__icontains=searchQ))

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndSerializer = NdParcelInformationsSerializer(allRecord, many=True)
        
        # return Response({ 'recordsFiltered' : flntUsersSerializer.data})
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               tmpRow = []
               featuredMode = ''
               
               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
                                  
               
               tmpRow.append(item['id'])
               tmpRow.append(item['item_name'])
               tmpRow.append(statusMsg)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
#------------------------ Single Details by ID BY GET -------------------------------------#
class RecordDetailsParcelInfo(APIView):
    def get(self, request, id, format =None):
      recordDetails = NdParcelInformations.objects.filter(id=id).first()
      ndSerializer = NdParcelInformationsSerializer(recordDetails)
      if ndSerializer.data:
          return Response([{"status" : True, "data" : ndSerializer.data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])   


# **************** Pickup request management **************************

def pickup_request_list( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "View pickup request"
        data['page_title'] = "View pickup request"

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        data['current_url_segments'] = urlSegments
        return render( request, './pickup_request/pickup_request.html', data)
    else:
        return redirect("/")

class pickup_request(APIView):
  #------------------------ Get method to get all data list -------------------------------------# 
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'contact_name',
            2 : 'supplier__first_name',
            3 : 'driver__first_name',
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]
        # if draw == "1" :
        #     sortingType = "desc"
        #     sortingColumn = 0
        totalRecords = NdOrder.objects.filter(is_deleted =False).count()
        totalFiltered = totalRecords
        allRecord = NdOrder.objects.filter(is_deleted =False)
        if searchQ:
            allRecord = allRecord.filter(Q(contact_name__icontains=searchQ) | Q(supplier__first_name__icontains=searchQ)|\
             Q(driver__first_name__icontains=searchQ))

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndSerializer = NdPickupRequestSerializer(allRecord, many=True)
        
        # return Response({ 'recordsFiltered' : flntUsersSerializer.data})
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               tmpRow = []
               featuredMode = ''
               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
               
               
               supplierFirstName = ""
               supplierLastName = ""
               driverFirstName = ""
               driverLastName = ""
               contact_name = ""
               contact_number = ""
               if (item['supplier']) is not None: 
                   if (item['supplier']['first_name']) is not None: 
                    supplierFirstName = str(item['supplier']['first_name'])
                   if item['supplier']['last_name'] is not None:
                    supplierLastName =  str(item['supplier']['last_name'])
               if (item['driver']) is not None:       
                   if (item['driver']['first_name']) is not None: 
                    driverFirstName = str(item['driver']['first_name'])
                   if item['driver']['last_name'] is not None:
                    driverLastName =  str(item['driver']['last_name'])


               if item['contact_name'] is not None:
                contact_name = item['contact_name']

               if item['contact_number'] is not None:
                contact_number = item['contact_number']


               
               tmpRow.append(item['id'])
               tmpRow.append(supplierFirstName + " " + supplierLastName)
               tmpRow.append(driverFirstName + " " + driverLastName)
               tmpRow.append(contact_name)
               tmpRow.append(contact_number)
               tmpRow.append(statusMsg)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
#------------------------ Single Details by ID BY GET -------------------------------------#
class RecordDetailsPickupRequest(APIView):
    def get(self, request, id, format =None):
      recordDetails = NdOrder.objects.filter(id=id).first()
      ndSerializer = NdPickupRequestSerializer(recordDetails)

      recordDropoffLocationDetails = NdDropOffLocation.objects.filter(order_id=id)
      ndDropoffSerializer = NdDropOffLocationSerializer(recordDropoffLocationDetails)


      print("=====================location ===================")
      print(ndDropoffSerializer.data)
      print("=====================location ===================")
      if ndSerializer.data:
          return Response([{"status" : True, "data" : ndSerializer.data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])   

# ------------------------ Language --------------------------------------------------

def language_list( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Language Management"
        data['page_title'] = "Language Management"

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        data['current_url_segments'] = urlSegments
        data['BASE_URL'] = settings.BASE_URL
        return render( request, './language/list.html', data)
    else:
        return redirect("/")
class language(APIView):

    def get(self, request, format =None):

        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'lang_name',
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]
        # if draw == "1" :
        #     sortingType = "desc"
        #     sortingColumn = 0
        totalRecords = NdLanguages.objects.filter(is_deleted =False).count()
        totalFiltered = totalRecords
        allRecord = NdLanguages.objects.filter(is_deleted =False)
        if searchQ:
            allRecord = allRecord.filter(Q(lang_name__icontains=searchQ))

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndSerializer = NdLanguagesSerializer(allRecord, many=True)
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               tmpRow = []
               featuredMode = ''
               image = ''
               
               # if item['image_file']:
               #      image = '<img src="'+ item['image_file']+'?time='+ str(datetime.datetime.now())+' " class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               # else:
               #      image = '<img src="'+ static('/static/images/avatar.jpg')+'" class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               
               

               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
                   
             
               tmpRow.append(item['id'])
               # tmpRow.append(image)
               # tmpRow.append(item['title'])
               tmpRow.append(item['lang_name'])

               tmpRow.append(statusMsg)
               # tmpRow.append(action)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        # return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
class UpdateMultiRecordLanguage(APIView):
    
    # tblArray = { }
    def post(self, request, format=None):
        countingInfo = []
        if request.data['action'] == 'is_status' or request.data['action'] == 'rm':
            id_list = json.loads(request.data['ids']) 
            value = True
            if( request.data['value'] != '1'):
                value = False
           
            if request.data['action'] == 'is_status':
                NdLanguages.objects.filter(id__in=id_list).update(is_status=value)

            if request.data['action'] == 'rm':
                NdLanguages.objects.filter(id__in=id_list).update(is_deleted=value)
           
            return Response([{"status" : True, 'msg' : 'Data updated successfully'}])
        else:
            return Response([{'status': False, 'msg' : 'Something went wrong1'}])

# ------------------------ Currencies --------------------------------------------------

def currency_list( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Currency Settings"
        data['page_title'] = "Currency Settings"

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        data['current_url_segments'] = urlSegments
        data['BASE_URL'] = settings.BASE_URL
        data['totalRecords'] = NdCurrencies.objects.filter(is_deleted =False).order_by('id')

        return render( request, './currency/list.html', data)
    else:
        return redirect("/")


class currency(APIView):
        #------------------------ Put method to update customer details By ID -------------------------------------#     
    def put(self, request, pk, format=None):
        try:
            self.errorResult = list()
       
            if(request.data["conversion_rate"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Conversion rate can not be blank", "field": "heading"})
           
            if self.errorResult:
                return Response(self.errorResult)
            else:
                request.POST._mutable = True
                
                
            
                NdCurrencies.objects.filter(id=pk).update( conversion_rate=request.data['conversion_rate'],currency=request.data['currency'])  

           
                return Response([{"status" : True, "msg" : "You have successfully updated the record"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Sorry! Data not updated", "field": "mainError"})
            return Response(self.errorResult)
# **************** Order management **************************

def order_list( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "View orders"
        data['page_title'] = "View orders"

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        data['current_url_segments'] = urlSegments
        return render( request, './order/order.html', data)
    else:
        return redirect("/")

class order(APIView):
  #------------------------ Get method to get all data list -------------------------------------# 
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'order_uid',
            1 : 'booking_time',
            2 : 'supplier__first_name',
            3 : 'driver__first_name',
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]

        # sortingColumn = 0
        # sortingType = "desc"

        print("===============sortingColumn===============")
        print(sortingColumn)
        print("===============sortingColumn===============")
        # draw = request.GET["draw"]
        # if draw == "1" :
        #     sortingType = "desc"
        #     sortingColumn = 0

        print("===============Sorting type===============")
        print(sortingType)
        print("===============Sorting type===============")
        totalRecords = NdOrder.objects.filter(is_deleted =False).exclude(booking_status=1).count()
        totalFiltered = totalRecords
        # Booking status placed 2
        allRecord = NdOrder.objects.filter(is_deleted =False).exclude(booking_status=1)
        if request.GET["is_date_search"] == "yes" :
            # 2018-12-01 18:51:00.749969+05:30
            # startDate = request.GET["start_date"]+" "+"00:00:00.749969+05:30"
            # endDate = request.GET["end_date"]+" "+"23:59:59.749969+05:30"
            startDate = request.GET["start_date"]
            endDate = request.GET["end_date"]
            
            
            allRecord = allRecord.filter(Q(booking_time__lte=endDate) & Q(booking_time__gte=startDate))
        if searchQ:
            allRecord = allRecord.filter(Q(location__icontains=searchQ) | Q(supplier__first_name__icontains=searchQ)|\
             Q(driver__first_name__icontains=searchQ) | Q(order_uid__icontains=searchQ))

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndSerializer = NdOrderSerializer(allRecord, many=True)

        # return Response({ 'recordsFiltered' : flntUsersSerializer.data})
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               tmpRow = []
               featuredMode = ''
               # statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               # if not item['is_status']:
               #      statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
               
               statusMsg =   ' <a href="order-details/'+str(item['id'])+'" class="btn-round-primary"> <i class="fa fa-eye" aria-hidden="true"></i></a> '

               supplierFirstName = ""
               supplierLastName = ""
               driverFirstName = ""
               driverLastName = ""
               order_uid = ""
               location = ""
               booking_date = ""
               if (item['supplier']['first_name']) is not None: 
                supplierFirstName = str(item['supplier']['first_name'])
               if item['supplier']['last_name'] is not None:
                supplierLastName =  str(item['supplier']['last_name'])

               if (item['driver']) is not None: 
                   if (item['driver']['first_name']) is not None: 
                    driverFirstName = str(item['driver']['first_name'])
                   if item['driver']['last_name'] is not None:
                    driverLastName =  str(item['driver']['last_name'])


               if item['order_uid'] is not None:
                order_uid = item['order_uid']
               if item['location'] is not None:
                location = item['location']

               
               if item['booking_time']:
                booking_date = parser.parse(item['booking_time']).date()
               
               # tmpRow.append(item['id'])
               tmpRow.append(booking_date)
               tmpRow.append(order_uid)
               tmpRow.append(location)
               tmpRow.append(supplierFirstName + " " + supplierLastName)
               tmpRow.append(driverFirstName + " " + driverLastName)
               
               tmpRow.append(statusMsg)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
#------------------------ Single Details by ID BY GET -------------------------------------#
class RecordDetailsOrder(APIView):
    def get(self, request, id, format =None):
      data = {}
      locationWiseParcelArr = []
      recordDetails = NdOrder.objects.filter(id=id).first()
      ndSerializer = NdOrderSerializer(recordDetails)

      

      recordParcelDetails = NdParcelInformations.objects.filter(order__id=id)
      ndParcelSerializer = NdParcelInformationsSerializer(recordParcelDetails, many=True)
     
      recordDropoffDetails = NdDropOffLocation.objects.filter(order__id=id)
      ndDropoffSerializer = NdDropOffLocationSerializer(recordDropoffDetails, many=True)

      driverExists = False
      booking_date = ""
      if ndSerializer.data['driver'] is not None: 
        recordVehicleDetails = NdVehicleDetails.objects.filter(user__id=ndSerializer.data['driver']['id']).first()
        ndVehicleSerializer = NdVehicleDetailsSerializer(recordVehicleDetails)
        driverExists = True

      if ndSerializer.data['booking_time']:
                booking_date = parser.parse(ndSerializer.data['booking_time']).date()

      for x in recordDropoffDetails:    
        ndEachDropoffSerializer = NdDropOffLocationSerializer(x)

        location_wise_parcel_data = NdParcelInformations.objects.filter(location=x)
        locationWiseParcelSerializer = NdParcelInformationsSerializer(location_wise_parcel_data, many=True)
        
        location_wise_info = {}
        location_wise_info['drop_off_location_details'] = ndEachDropoffSerializer.data
        location_wise_info['parcel_files'] = locationWiseParcelSerializer.data
        locationWiseParcelArr.append(location_wise_info)
      data['order_details'] = ndSerializer.data
      data['order_parcel_info'] = ndParcelSerializer.data
      data['order_drop_off_locations'] = ndDropoffSerializer.data
      data['location_wise_parcel_data'] = locationWiseParcelArr
      data['booking_date'] = booking_date
      if driverExists == True :
        data['vehicle_details'] = ndVehicleSerializer.data
      if ndSerializer.data:
          # return Response([{"status" : True, "data" : ndSerializer.data}])
           return render( request, './order/order-details.html', data)
      else:
           return redirect("/")
          # return Response([{"status" : False, "msg" : "Sorry! No record is found"}]) 


        

#---------------------- Vehicle Model ----------------------------
def vehiclemodel_list( request ):
    
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Vehicle model Management"
        data['page_title'] = "Vehicle model Management"
        allActiveData = NdVehicleModel.objects.filter(is_status=True, is_deleted= False).count() 
        data['totalActive'] = allActiveData
        allDeactiveData = NdVehicleModel.objects.filter(is_status=False, is_deleted= False).count() 
        data['totalDeactive'] = allDeactiveData
        data['WEBADMIN'] = settings.WEBADMIN_URL

        allvehicle = NdVehicleType.objects.filter(is_status=True, is_deleted= False).order_by('vehicle_type_name') 
        ndVehicletypeSerializer = NdVehicleTypeSerializer(allvehicle, many=True)
        data['vehicle_types'] = ndVehicletypeSerializer.data

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        data['current_url_segments'] = urlSegments
        return render( request, './vehicle_model/vehicle_model.html', data)
    else:
        return redirect("/")

class vehiclemodel(APIView):
  #------------------------ Get method to get all customer -------------------------------------# 
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'model_name'
        }
       
        sortingColumn = request.GET["order[0][column]"]
        
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]
        # if draw == "1" :
        #     sortingType = "desc"
        #     sortingColumn = 1

        

        totalRecords = NdVehicleModel.objects.filter(is_deleted =False).count()
        totalFiltered = totalRecords
        allRecord = NdVehicleModel.objects.filter(is_deleted =False)
        
        if searchQ:
            allRecord = allRecord.filter(Q(model_name__icontains=searchQ) )

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        
        ndSerializer = NdVehiclModelSerializer(allRecord, many=True)
        
        # return Response({ 'recordsFiltered' : flntUsersSerializer.data})
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               tmpRow = []
               featuredMode = ''
               logo = ''
               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
                   
               
               tmpRow.append(item['id'])
               tmpRow.append(item['vehicle_type']['vehicle_type_name'])
               tmpRow.append(item['model_name'])
               tmpRow.append(statusMsg)
               # tmpRow.append(action)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        # return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        #------------------------ Put method to update details By ID -------------------------------------#     
    def put(self, request, pk, format=None):
        try:

        # return Response({'s':type(int(request.data["duration"]))})
            self.errorResult = list()
       
            if(request.data["model_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Vehicle model Name can not be blank", "field": "first_name"})
           
            if self.errorResult:
                return Response(self.errorResult)
                # return Response({"o":request.data["country_id"]})
            else:
                NdVehicleModel.objects.filter(id=pk).update( vehicle_type=request.data['vehicle_type'], model_name=request.data['model_name'])
                
                return Response([{"status" : True, "msg" : "You have successfully updated the record"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Please check not saved yet", "field": "mainError"})
            return Response(self.errorResult)

    #------------------------ POST method to Insert  details -------------------------------------# 
    def post(self, request, format=None):
        # try:
            self.errorResult = list()
            
            if(request.data["model_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Vehicle model Name can not be blank", "field": "model_name"})
            
            else:
               
                ndSerializer = NdVehiclModelSerializer(data=request.data )
                vehicle_type_instance = NdVehicleType.objects.filter(id=int(request.data.get('vehicle_type'))).first()

                if ndSerializer.is_valid():
                    ndSerializer.save(vehicle_type = vehicle_type_instance)








                # if ndSerializer.is_valid():
                #     ndSerializer.save()
                data = {};
                allActiveData = NdVehicleModel.objects.filter(is_status=True, is_deleted= False).count() 
                data['totalActive'] = allActiveData

                allDeactiveData = NdVehicleModel.objects.filter(is_status=False, is_deleted= False).count() 
                data['totalDeactive'] = allDeactiveData

                return Response([{"status" : True, "data" : data, "msg" : "You have successfully created", 'updated_record' : data}])
        # except Exception as e:
        #     self.errorResult.append({"status" : False,"msg" : "Sorry! failed to save data", "field": "mainError"})
        #     return Response(self.errorResult)

#------------------------ Single User Details by ID BY GET -------------------------------------#
class RecordDetailsVehicleModel(APIView):
    def get(self, request, id, format =None):
      recordDetails = NdVehicleModel.objects.filter(id=id).first()
      ndSerializer = NdVehiclModelSerializer(recordDetails)
      if ndSerializer.data:
          return Response([{"status" : True, "data" : ndSerializer.data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])
#------------------------ Update multiple records BY LIST ID -------------------------------------#
class UpdateMultiRecordVehicleModel(APIView):
    
    # tblArray = { }
    def post(self, request, format=None):
        # send_mail("hello paul", "comment tu vas?", "arijit.chandra@navsoft.in", ['arijit.chandra@navsoft.in'],fail_silently=False,)         
        # return Response({'status' : True,'sss': '1'})
       
        countingInfo = []
        if request.data['action'] == 'is_status' or request.data['action'] == 'rm':
            id_list = json.loads(request.data['ids']) 
            value = True
            if( request.data['value'] != '1'):
                value = False
           
            if request.data['action'] == 'is_status':
                NdVehicleModel.objects.filter(id__in=id_list).update(is_status=value)

            if request.data['action'] == 'rm':
                NdVehicleModel.objects.filter(id__in=id_list).update(is_deleted=value)
           
            allActivedata = NdVehicleModel.objects.filter(is_status=True, is_deleted= False).count() 
           
            countingInfo.append({'totalActiveCustomers' : allActivedata})

            allDeactiveData = NdVehicleModel.objects.filter(is_status=False, is_deleted= False).count() 
            
            countingInfo.append({'allDeactiveCustomer' : allDeactiveData})

            allCustomer = NdVehicleModel.objects.filter(is_deleted= False).count() 
            # allTeacherallTeacher = allCustomer
            countingInfo.append({'allCustomer' : allCustomer})
                
            return Response([{"status" : True, "countingInfo" : countingInfo}])
        else:
            return Response([{'status': False, 'msg' : 'Something went wrong1'}])


#---------------------- Subscription Management ----------------------------
def driver_subscription_list( request ):
    
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Driver Subscription Management"
        data['page_title'] = "Driver Subscription Management"
        allPlan = NdSubscriptionPlan.objects.order_by('plan_name') 
        ndPlanSerializer = NdSubscriptionPlanSerializer(allPlan, many=True)
        data['subscriptionPlans'] = ndPlanSerializer.data
        data['WEBADMIN'] = settings.WEBADMIN_URL
        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        data['current_url_segments'] = urlSegments
        return render( request, './driver_subscription/driver_subscription.html', data)
    else:
        return redirect("/")

class driver_subscription(APIView):
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'subscription_plan',
            2 : 'first_name',
            3 : 'last_name'
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]
        if draw == "1" :
            sortingType = "desc"
            sortingColumn = 0
        totalRecords = NdDriverDetails.objects.filter(is_deleted =False, user__is_status=True, user__is_deleted=False).count()
        totalFiltered = totalRecords
        allRecord = NdDriverDetails.objects.filter(is_deleted =False, user__is_status=True, user__is_deleted=False)
        if searchQ:
            allRecord = allRecord.filter(Q(subscription_plan__plan_name__icontains=searchQ) | Q(user__first_name__icontains=searchQ) |Q(user__last_name__icontains=searchQ))

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndSerializer = NdDriverDetailsSerializer(allRecord, many=True)
        
        # return Response({ 'recordsFiltered' : flntUsersSerializer.data})
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               # print("======================item==========")
               # print(item) 
               tmpRow = []
               featuredMode = ''
               logo = ''
               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
                   
               firstName = ""
               lastName = ""
               subscriptionPlan = ""
               if item['user']:
                   if item['user']['first_name']: 
                    firstName = item['user']['first_name']
                   if item['user']['last_name']:
                    lastName =  item['user']['last_name']
               if item['subscription_plan']:
                   subscriptionPlan = item['subscription_plan']['plan_name']
               tmpRow.append(item['id'])
               tmpRow.append(firstName+ " " +lastName)
               tmpRow.append(subscriptionPlan)
               tmpRow.append(item['account_balance'])
               
               # tmpRow.append(statusMsg)
               # tmpRow.append(action)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        # return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        #------------------------ Put method to update details By ID -------------------------------------#     
    def put(self, request, pk, format=None):
        try:
            self.errorResult = list()
       
            if(request.data["driver_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Vehicletype Name can not be blank", "field": "first_name"})
           
            if self.errorResult:
                return Response(self.errorResult)
                # return Response({"o":request.data["country_id"]})
            else:
                
                NdDriverDetails.objects.filter(id=pk).update( subscription_plan=request.data['plan_name'], account_balance= request.data['account_balance'], account_balance_currency_id= request.data['account_balance_currency'])
                
                return Response([{"status" : True, "msg" : "You have successfully updated the record"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Please check not saved yet", "field": "mainError"})
            return Response(self.errorResult)


#------------------------ Single User Details by ID BY GET -------------------------------------#
class RecordDetailsDriverSubscription(APIView):
    def get(self, request, id, format =None):
      recordDetails = NdDriverDetails.objects.filter(id=id).first()
      ndSerializer = NdDriverDetailsSerializer(recordDetails)
      if ndSerializer.data:
          return Response([{"status" : True, "data" : ndSerializer.data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])
#------------------------ Update multiple records BY LIST ID -------------------------------------#
class UpdateMultiRecordSubscriptionPlan(APIView):
    
    # tblArray = { }
    def post(self, request, format=None):
        # send_mail("hello paul", "comment tu vas?", "arijit.chandra@navsoft.in", ['arijit.chandra@navsoft.in'],fail_silently=False,)         
        # return Response({'status' : True,'sss': '1'})
       
        countingInfo = []
        print('++++++++++++++++++++=')
        if request.data['action'] == 'is_status' or request.data['action'] == 'rm':
            id_list = json.loads(request.data['ids']) 
            value = True
            if( request.data['value'] != '1'):
                value = False
            print(request.data['action'])
            if request.data['action'] == 'is_status':
                NdDriverDetails.objects.filter(id__in=id_list).update(is_status=value)

            if request.data['action'] == 'rm':
                NdDriverDetails.objects.filter(id__in=id_list).update(is_deleted=value)
           
            allActivedata = NdDriverDetails.objects.filter(is_status=True, is_deleted= False).count() 
           
            countingInfo.append({'totalActiveCustomers' : allActivedata})

            allDeactiveData = NdDriverDetails.objects.filter(is_status=False, is_deleted= False).count() 
            
            countingInfo.append({'allDeactiveCustomer' : allDeactiveData})

            allCustomer = NdDriverDetails.objects.filter(is_deleted= False).count() 
            # allTeacherallTeacher = allCustomer
            countingInfo.append({'allCustomer' : allCustomer})
                
            return Response([{"status" : True, "countingInfo" : countingInfo}])
        else:
            return Response([{'status': False, 'msg' : 'Something went wrong'}])

#---------------------- Vehicle type ----------------------------
def promotioncode_list( request ):
    
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Promotion Management"
        data['page_title'] = "Promotion Management"
        data['WEBADMIN'] = settings.WEBADMIN_URL

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        # print(urlSegments)
        data['current_url_segments'] = urlSegments
        return render( request, './promotion_code/promotion_code.html', data)
    else:
        return redirect("/")

class promotioncode(APIView):
  #------------------------ Get method to get all customer -------------------------------------# 
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'promotion_code'
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]
        if draw == "1" :
            sortingType = "desc"
            sortingColumn = 0
        totalRecords = NdPromotions.objects.filter(is_deleted =False).count()
        totalFiltered = totalRecords
        allRecord = NdPromotions.objects.filter(is_deleted =False)
        
        if searchQ:
            allRecord = allRecord.filter(Q(promotion_code__icontains=searchQ) )

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndSerializer = NdPromotionCodeSerializer(allRecord, many=True)
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               tmpRow = []
               featuredMode = ''
               logo = ''
              
               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
                   
               
               tmpRow.append(item['id'])
               
               tmpRow.append(item['promotion_code'])
               tmpRow.append(item['discount'])
               tmpRow.append(item['start_date'])
               tmpRow.append(item['end_date'])
               
               tmpRow.append(statusMsg)
               # tmpRow.append(action)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        # return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        #------------------------ Put method to update details By ID -------------------------------------#     
    def put(self, request, pk, format=None):
        try:
            self.errorResult = list()
            if(request.data["promotion_code"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Promotion code can not be blank", "field": "first_name"})
           
            if self.errorResult:
                return Response(self.errorResult)
            else:
                ndSerializer = NdPromotionCodeSerializer(data=request.data)
                if ndSerializer.is_valid():
                    NdPromotions.objects.filter(id=pk).update(is_deleted=True)
                    ndSerializer.save()
                else:
                    print("===========================================")
                    print(ndSerializer.errors)
                    print("===========================================")
                
                return Response([{"status" : True, "msg" : "You have successfully updated the record"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Please check not saved yet", "field": "mainError"})
            return Response(self.errorResult)

    #------------------------ POST method to Insert  details -------------------------------------# 
    def post(self, request, format=None):
        try:
            self.errorResult = list()
            
            if(request.data["promotion_code"] == ""):
                self.errorResult.append({"status" : False,"msg" : "First Name can not be blank", "field": "first_name"})
            
            else:
                ndSerializer = NdPromotionCodeSerializer(data=request.data)

                if ndSerializer.is_valid():
                    ndSerializer.save()
                data = {};
                allActiveData = NdPromotions.objects.filter(is_status=True, is_deleted= False).count() 
                data['totalActive'] = allActiveData

                allDeactiveData = NdPromotions.objects.filter(is_status=False, is_deleted= False).count() 
                data['totalDeactive'] = allDeactiveData

                return Response([{"status" : True, "data" : data, "msg" : "You have successfully created", 'updated_record' : data}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Sorry! failed to save data", "field": "mainError"})
            return Response(self.errorResult)

#------------------------ Single User Details by ID BY GET -------------------------------------#
class RecordDetailsPromotionCode(APIView):
    def get(self, request, id, format =None):
      recordDetails = NdPromotions.objects.filter(id=id).first()
      ndSerializer = NdPromotionCodeSerializer(recordDetails)
      if ndSerializer.data:
          return Response([{"status" : True, "data" : ndSerializer.data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])
#------------------------ Update multiple records BY LIST ID -------------------------------------#
class UpdateMultiRecordPromotionCode(APIView):
    
    # tblArray = { }
    def post(self, request, format=None):
        # send_mail("hello paul", "comment tu vas?", "arijit.chandra@navsoft.in", ['arijit.chandra@navsoft.in'],fail_silently=False,)         
        # return Response({'status' : True,'sss': '1'})
       
        countingInfo = []
        if request.data['action'] == 'is_status' or request.data['action'] == 'rm':
            id_list = json.loads(request.data['ids']) 
            value = True
            if( request.data['value'] != '1'):
                value = False
           
            if request.data['action'] == 'is_status':
                NdPromotions.objects.filter(id__in=id_list).update(is_status=value)

            if request.data['action'] == 'rm':
                NdPromotions.objects.filter(id__in=id_list).update(is_deleted=value)
           
            allActivedata = NdPromotions.objects.filter(is_status=True, is_deleted= False).count() 
           
            countingInfo.append({'totalActiveCustomers' : allActivedata})

            allDeactiveData = NdPromotions.objects.filter(is_status=False, is_deleted= False).count() 
            
            countingInfo.append({'allDeactiveCustomer' : allDeactiveData})

            allCustomer = NdPromotions.objects.filter(is_deleted= False).count() 
            # allTeacherallTeacher = allCustomer
            countingInfo.append({'allCustomer' : allCustomer})
                
            return Response([{"status" : True, "countingInfo" : countingInfo}])
        else:
            return Response([{'status': False, 'msg' : 'Something went wrong1'}])

#---------------------- Start Payment method  ----------------------------
def paymentmethod_list( request ):
    
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Payment method Management"
        data['page_title'] = "Payment method Management"
        
        data['WEBADMIN'] = settings.WEBADMIN_URL

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        # print(urlSegments)
        data['current_url_segments'] = urlSegments
        return render( request, './payment_method/payment_method.html', data)
    else:
        return redirect("/")

class paymentmethod(APIView):
  #------------------------ Get method to get all customer -------------------------------------# 
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'name'
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]
        if draw == "1" :
            sortingType = "desc"
            sortingColumn = 0
        totalRecords = NdPaymentMethod.objects.filter(is_deleted =False).count()
        totalFiltered = totalRecords
        allRecord = NdPaymentMethod.objects.filter(is_deleted =False)
        
        if searchQ:
            allRecord = allRecord.filter(Q(name__icontains=searchQ) )

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndSerializer = NdPaymentMethodSerializer(allRecord, many=True)
        
        # return Response({ 'recordsFiltered' : flntUsersSerializer.data})
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               tmpRow = []
               featuredMode = ''
               logo = ''
               if item['payment_logo']:
                    image = '<img src="'+ item['payment_logo']+'?time='+ str(datetime.datetime.now())+' " class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               else:
                    image = '<img src="'+ static('images/avatar.jpg')+'" class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               

               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
                   
               
               tmpRow.append(item['id'])
               tmpRow.append(image)
               tmpRow.append(item['name'])
               tmpRow.append(statusMsg)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        # return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        #------------------------ Put method to update details By ID -------------------------------------#     
    def put(self, request, pk, format=None):
        try:
            self.errorResult = list()
       
            if(request.data["name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Name can not be blank", "field": "name"})
           
            if self.errorResult:
                return Response(self.errorResult)
                # return Response({"o":request.data["country_id"]})
            else:
                if request.data['payment_logo'] == 'undefined':
                    NdPaymentMethod.objects.filter(id=pk).update( name=request.data['name'])
                else:     
                    ndSerializer = NdPaymentMethodSerializer(data=request.data)

                    if ndSerializer.is_valid():
                        # Making the is_deleted true and inserting a new record 
                        NdPaymentMethod.objects.filter(id=pk).update(is_deleted=True)
                        ndSerializer.save()
                    else:
                        print("===========================================")
                        print(ndSerializer.errors)
                        print("===========================================")
                # request.POST._mutable = True
                
                # recordDetails = NdPaymentMethod.objects.filter(id=pk).first()
                # details = NdPaymentMethodSerializer(recordDetails)
                # NdPaymentMethod.objects.filter(id=pk).update( vehicle_type_name=request.data['vehicle_type_name'], khr=request.data['khr'], person_capcity= request.data['person_capcity'])  

           
                return Response([{"status" : True, "msg" : "You have successfully updated the record"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Please check not saved yet", "field": "mainError"})
            return Response(self.errorResult)

    #------------------------ POST method to Insert  details -------------------------------------# 
    def post(self, request, format=None):
        try:
            self.errorResult = list()
            
            if(request.data["name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Name can not be blank", "field": "name"})
            
            else:
                ndSerializer = NdPaymentMethodSerializer(data=request.data)

                if ndSerializer.is_valid():
                    ndSerializer.save()
                data = {};
                allActiveData = NdPaymentMethod.objects.filter(is_status=True, is_deleted= False).count() 
                data['totalActive'] = allActiveData

                allDeactiveData = NdPaymentMethod.objects.filter(is_status=False, is_deleted= False).count() 
                data['totalDeactive'] = allDeactiveData

                return Response([{"status" : True, "data" : data, "msg" : "You have successfully created", 'updated_record' : data}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Sorry! failed to save data", "field": "mainError"})
            return Response(self.errorResult)

#------------------------ Single User Details by ID BY GET -------------------------------------#
class RecordDetailsPaymentMethod(APIView):
    def get(self, request, id, format =None):
      recordDetails = NdPaymentMethod.objects.filter(id=id).first()
      ndSerializer = NdPaymentMethodSerializer(recordDetails)
      if ndSerializer.data:
          return Response([{"status" : True, "data" : ndSerializer.data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])
#------------------------ Update multiple records BY LIST ID -------------------------------------#
class UpdateMultiRecordPaymentMethod(APIView):
    
    # tblArray = { }
    def post(self, request, format=None):
        # send_mail("hello paul", "comment tu vas?", "arijit.chandra@navsoft.in", ['arijit.chandra@navsoft.in'],fail_silently=False,)         
        # return Response({'status' : True,'sss': '1'})
       
        countingInfo = []
        if request.data['action'] == 'is_status' or request.data['action'] == 'rm':
            id_list = json.loads(request.data['ids']) 
            value = True
            if( request.data['value'] != '1'):
                value = False
           
            if request.data['action'] == 'is_status':
                NdPaymentMethod.objects.filter(id__in=id_list).update(is_status=value)

            if request.data['action'] == 'rm':
                NdPaymentMethod.objects.filter(id__in=id_list).update(is_deleted=value)
           
            allActivedata = NdPaymentMethod.objects.filter(is_status=True, is_deleted= False).count() 
           
            countingInfo.append({'totalActiveCustomers' : allActivedata})

            allDeactiveData = NdPaymentMethod.objects.filter(is_status=False, is_deleted= False).count() 
            
            countingInfo.append({'allDeactiveCustomer' : allDeactiveData})

            allCustomer = NdPaymentMethod.objects.filter(is_deleted= False).count() 
            # allTeacherallTeacher = allCustomer
            countingInfo.append({'allCustomer' : allCustomer})
                
            return Response([{"status" : True, "countingInfo" : countingInfo}])
        else:
            return Response([{'status': False, 'msg' : 'Something went wrong'}])

# **************** Driver trip management **************************

def driver_trip_list( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Driver Trip list"
        data['page_title'] = "Driver Trip list"

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        data['current_url_segments'] = urlSegments
        return render( request, './driver_trip/driver_trip.html', data)
    else:
        return redirect("/")

class drivertrip(APIView):
  #------------------------ Get method to get all data list -------------------------------------# 
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        
        fieldSToSort = {
            0 : 'id',
            1 : 'delivery_time',
            3 : 'supplier__first_name',
            2 : 'driver__first_name',
            4 : 'base_price',
            6 : 'distance',
            7 : 'total_time_taken',
            8 : 'booking_status',
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]



        # if draw == "1" :
        #     sortingType = "desc"
        #     sortingColumn = 0
        

        totalRecords = NdOrder.objects.filter(Q(is_deleted =False), ~Q(booking_status=settings.BOOKING_STATUS_PROCESSING)).count()
        totalFiltered = totalRecords
        allRecord = NdOrder.objects.filter(Q(is_deleted =False), ~Q(booking_status=settings.BOOKING_STATUS_PROCESSING) )

        if request.GET["is_date_search"] == "yes" :
            # 2018-12-01 18:51:00.749969+05:30
            # startDate = request.GET["start_date"]+" "+"00:00:00.749969+05:30"
            # endDate = request.GET["end_date"]+" "+"23:59:59.749969+05:30"
            startDate = request.GET["start_date"]
            endDate = request.GET["end_date"]
            
            
            allRecord = allRecord.filter(Q(delivery_time__gte = startDate) & Q(delivery_time__lte = endDate))
        if searchQ:
            allRecord = allRecord.annotate(supplier_full_name=Concat('supplier__first_name', Value(' '), 'supplier__last_name')).annotate(
                driver_full_name=Concat('driver__first_name', Value(' '), 'driver__last_name')).filter( Q(supplier__first_name__icontains=searchQ) | Q(supplier__last_name__icontains=searchQ)
                | Q(driver__first_name__icontains=searchQ) | Q(driver__last_name__icontains=searchQ) | Q(order_uid__icontains=searchQ) | Q(supplier_full_name__icontains=searchQ) |
                Q(driver_full_name__icontains=searchQ))

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndSerializer = NdDriverTripSerializer(allRecord, many=True)
        
        # return Response({ 'recordsFiltered' : flntUsersSerializer.data})
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               tmpRow = []
               featuredMode = ''
               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
               
               
               supplierFirstName = ""
               supplierLastName = ""
               driverFirstName = "Not Assigned"
               driverLastName = ""
               contact_name = ""
               contact_number = ""
               deliver_datetime = "N/A"
               if (item['supplier']) is not None: 
                   if (item['supplier']['first_name']) is not None: 
                    supplierFirstName = str(item['supplier']['first_name'])
                   if item['supplier']['last_name'] is not None:
                    supplierLastName =  str(item['supplier']['last_name'])
               if (item['driver']) is not None:       
                   if (item['driver']['first_name']) is not None: 
                    driverFirstName = str(item['driver']['first_name'])
                   if item['driver']['last_name'] is not None:
                    driverLastName =  str(item['driver']['last_name'])

               commission = NdSettings.objects.filter(field_name__icontains="Commission( % )", is_status=True, is_deleted=False).values('field_val').first()
               # print(commission)
               commissionAmt = "0.00"
               try:
                   comDivide = float(commission['field_val'])/100.00
                   commissionAmtq =  comDivide * float(item['base_price'])
                   # print("dddddddddddddddd",str(type(commissionAmt)))
                   commissionAmt = "{0:.2f}".format(commissionAmtq)
               except Exception as R:
                    commissionAmt = "0.00"
               if item['contact_name'] is not None:
                contact_name = item['contact_name']

               if item['contact_number'] is not None:
                contact_number = item['contact_number']

               if item['delivery_time'] is not None:
                    StartDateSplitTz = item['delivery_time'].split(".")
                    StartDate = StartDateSplitTz[0].replace("T"," ")
                    deliver_datetime = datetime.datetime.strptime(StartDate, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %I:%M:%S %p') 
               viewMsg =  ' <a href="completedtrip-details/'+str(item['id'])+'" class="btn-round-primary"> <i class="fa fa-eye" aria-hidden="true"></i></a> '
               # BOOKING_STATUS_PROCESSING = 1
               # BOOKING_STATUS_PLACED = 2
               # BOOKING_STATUS_CANCELLED = 3
               # BOOKING_STATUS_COMPLETED = 4
               if item['booking_status'] == settings.BOOKING_STATUS_PROCESSING:
                    statusImg = '<span class="badge badge-pill badge-light">Procressing</span>'
               elif item['booking_status'] == settings.BOOKING_STATUS_PLACED:
                    statusImg = '<span class="badge badge-pill badge-secondary">Ongoing</span>'
               elif item['booking_status'] == settings.BOOKING_STATUS_COMPLETED:
                    statusImg = '<span class="badge badge-pill badge-success">Completed</span>'
               elif item['booking_status'] == settings.BOOKING_STATUS_CANCELLED:
                    statusImg = '<span class="badge badge-pill badge-danger">Cancelled</span>'
               tmpRow.append(item['order_uid'])
               tmpRow.append(deliver_datetime)
               tmpRow.append(driverFirstName + " " + driverLastName)
               tmpRow.append(supplierFirstName + " " + supplierLastName)
               tmpRow.append(str(item['base_price']))
               tmpRow.append(commissionAmt)
               tmpRow.append(str(item['distance']))
               tmpRow.append(str(datetime.timedelta(seconds=item['total_time_taken']))) 
               tmpRow.append(statusImg)
               tmpRow.append(viewMsg)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
#------------------------ Single Details by ID BY GET -------------------------------------#

class OngoingBooking(APIView):
    def post(self, request):

        # try:
        if not fieldEmptyCheck(request.data.get('order_id')):
            return Response({"status":False, "msg":"Something went wrong",
             "data" : dict()})
        else:

            orderDetails = NdOrder.objects.filter(id=int(request.data.get('order_id')))
            print( orderDetails.count() )
            if orderDetails.exists():
                print(str(orderDetails.first()))
                orderDetailsObj = OngoingOrderDetailsSE(orderDetails.first(), many=False, context={'lang':'km-KH'})
                html_data = loader.render_to_string(
                        'driver_trip/booking_details.html',
                        {
                            'data': orderDetailsObj.data,
                            'base_url' : ""
                        }
                    )
                return Response({"status":True, "data" : orderDetailsObj.data, 'html_data': html_data}) 
            else:
                return Response({"status":True, "data" : dict()})
        # except Exception as e:
        #   return Response({'status': False,  "data" : dict()})
class RecordDetailsDriverTrip(APIView):
    def get(self, request, id, format =None):
      data = {}
      recordDetails = NdOrder.objects.filter(id=id).first()
      ndSerializer = NdPickupRequestSerializer(recordDetails)

     
      recordParcelDetails = NdParcelInformations.objects.filter(order__id=id)
      ndParcelSerializer = NdParcelInformationsSerializer(recordParcelDetails, many=True)
     
      recordDropoffDetails1 = NdDropOffLocation.objects.filter(Q(order__id=id) & Q(drop_location_type = 1)).first()
      ndDropoffSerializer1 = NdDropOffLocationSerializer(recordDropoffDetails1)

      recordDropoffDetails2 = NdDropOffLocation.objects.filter(Q(order__id=id) & Q(drop_location_type = 2)).first()
      ndDropoffSerializer2 = NdDropOffLocationSerializer(recordDropoffDetails2)

     
 
      data['order_details'] = ndSerializer.data
      data['order_parcel_info'] = ndParcelSerializer.data
      data['order_drop_off_location1'] = ndDropoffSerializer1.data
      data['order_drop_off_location2'] = ndDropoffSerializer2.data
     
      if ndSerializer.data:
          return Response([{"status" : True, "data" : data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])   

class regTimeInterval( APIView ):
    errorResult = []
    def post( self, request ):
        self.errorResult = list()
        if request.data.get('graph_type') == "":
            self.errorResult.append({"status" : False,"msg" : "End date not selected", "field": "endDate"})
        else:
            if request.data.get('graph_type') == "4":
                

                if request.data.get('startDate') == "":
                    self.errorResult.append({"status" : False,"msg" : "Start date not selected", "field": "startDate"})
                if request.data.get('endDate') == "":
                    self.errorResult.append({"status" : False,"msg" : "End date not selected", "field": "endDate"})
                if request.data.get('user_type') == "":
                    self.errorResult.append({"status" : False,"msg" : "user_type not selected", "field": "endDate"})
                if self.errorResult:
                    return Response(self.errorResult)
                else:
                    startDate = datetime.datetime.strptime(str(request.data.get('startDate')), "%Y-%m-%d")     
                    endDate = datetime.datetime.strptime(str(request.data.get('endDate')), "%Y-%m-%d")    
                    # print("===============start/end===================")
                    # print(startDate)
                    # print("===============start/end===================")
                    # print(endDate)
                    langs = []
                    daysDiff = endDate - startDate
                    
                    totalDays = daysDiff.days +1
                    
                    dateList = []
                    today = datetime.datetime.today()
                    arrDateCountData = []
                    arrDateData = []
                    if totalDays >1:
                        for x in range (0, totalDays):
                            # tmpDate = today - datetime.timedelta(days = x)
                            tmpDate = endDate - datetime.timedelta(days = x)

                            DateSplitTz = str(tmpDate).split(".")
                            StartDate = DateSplitTz[0].replace("T"," ")
                            tmpDate = datetime.datetime.strptime(str(StartDate), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                            dateList.append(tmpDate)
                    else:
                        # tmpDate = today 
                        tmpDate = startDate 

                        DateSplitTz = str(tmpDate).split(".")
                        StartDate = DateSplitTz[0].replace("T"," ")
                        tmpDate = datetime.datetime.strptime(str(StartDate), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                        dateList.append(tmpDate)
                    # print(dateList)
                    if dateList:
                        for item in dateList:

                            ndUsersCount = NdUsers.objects.filter(Q(is_status=True), Q(is_deleted=False), Q(reg_date__iexact=item), Q(role_id=int(request.data.get('user_type')))).count()
                            arrDateData.append({'name' : item, 'y' : ndUsersCount}) 

                        return Response([{"status" : True, "data" : arrDateData, "msg" : ""}])   
            else:
                self.errorResult.append({"status" : False,"msg" : "Something went wrong", "field": "mainError"})
                return Response(self.errorResult)

#------------------------ Settings -------------------------------------#

# def siteSettings( request ):
#     if 'authSession' in request.session:
#         data = {}
#         locationWiseParcelArr = []
#         recordDetails = NdSettings.objects.filter(id=id).first()
#         ndSerializer = NdSettingsSerializer(recordDetails)
#         data['details_data'] = ndSerializer.data
        
#           # return Response([{"status" : True, "data" : ndSerializer.data}])
#         return render( request, 'settings/settings-form.html', data)
        
    
#     else:
#        return redirect("/")
def siteSettings( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Settings"
        data['page_title'] = "Settings"
       
        allRecord = NdSettings.objects.filter(is_deleted =False)
        ndSerializer = NdSettingsSerializer(allRecord, many=True)
        print("==============================")
        print(ndSerializer.data)
        data['details_data_list'] = ndSerializer.data
        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        data['current_url_segments'] = urlSegments
        return render( request, 'settings/settings-form.html', data)
    else:
        return redirect("/")

class Settings(APIView):
    def post(self, request, format=None):
        try:
            # print("============All data===============")
            # print(request.data)
            for key, val in request.data.items():
                # print("===========key==============")
                # print(key)
                # print("===========val==============")
                # print(val)
                NdSettings.objects.filter(field_name=key).update( field_val=val)  
                
            

            
            # ndSerializer = NdVehicleTypeSerializer(data=request.data)

            # if ndSerializer.is_valid():
            #     ndSerializer.save()
            # data = {};
            # allActiveData = NdVehicleType.objects.filter(is_status=True, is_deleted= False).count() 
            # data['totalActive'] = allActiveData

            # allDeactiveData = NdVehicleType.objects.filter(is_status=False, is_deleted= False).count() 
            # data['totalDeactive'] = allDeactiveData

            return Response([{"status" : True,  "msg" : "You have successfully updated the record"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Sorry! failed to save data", "field": "mainError"})
            return Response(self.errorResult)


# ****************  Start completed trip **************************

def completedtrip_list( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Completed Trip List"
        data['page_title'] = "Completed Trip List"

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        data['current_url_segments'] = urlSegments
        return render( request, './completed_trip/completed_trip.html', data)
    else:
        return redirect("/")

class completedtrip(APIView):
  #------------------------ Get method to get all data list -------------------------------------# 
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'order_uid',
            1 : 'booking_time',
            2 : 'supplier__first_name',
            3 : 'driver__first_name',
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]

        # sortingColumn = 0
        # sortingType = "desc"

        # draw = request.GET["draw"]
        # if draw == "1" :
        #     sortingType = "desc"
        #     sortingColumn = 0

        
        totalRecords = NdOrder.objects.filter(is_deleted =False,booking_status=4).count()
        totalFiltered = totalRecords
        # Booking status placed 2
        allRecord = NdOrder.objects.filter(is_deleted =False, booking_status=4)
        if request.GET["is_date_search"] == "yes" :
            # 2018-12-01 18:51:00.749969+05:30
            # startDate = request.GET["start_date"]+" "+"00:00:00.749969+05:30"
            # endDate = request.GET["end_date"]+" "+"23:59:59.749969+05:30"
            startDate = request.GET["start_date"]
            endDate = request.GET["end_date"]
            
            
            allRecord = allRecord.filter(Q(booking_time__lte=endDate) & Q(booking_time__gte=startDate))
        if searchQ:
            allRecord = allRecord.filter(Q(location__icontains=searchQ) | Q(supplier__first_name__icontains=searchQ)|\
             Q(driver__first_name__icontains=searchQ) | Q(order_uid__icontains=searchQ))

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndSerializer = NdOrderSerializer(allRecord, many=True)

        # return Response({ 'recordsFiltered' : flntUsersSerializer.data})
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               tmpRow = []
               featuredMode = ''
               # statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               # if not item['is_status']:
               #      statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
               
               statusMsg =   ' <a href="completedtrip-details/'+str(item['id'])+'" class="btn-round-primary"> <i class="fa fa-eye" aria-hidden="true"></i></a> '

               supplierFirstName = ""
               supplierLastName = ""
               driverFirstName = ""
               driverLastName = ""
               order_uid = ""
               location = ""
               booking_date = ""
               if (item['supplier']['first_name']) is not None: 
                supplierFirstName = str(item['supplier']['first_name'])
               if item['supplier']['last_name'] is not None:
                supplierLastName =  str(item['supplier']['last_name'])

               if (item['driver']) is not None: 
                   if (item['driver']['first_name']) is not None: 
                    driverFirstName = str(item['driver']['first_name'])
                   if item['driver']['last_name'] is not None:
                    driverLastName =  str(item['driver']['last_name'])


               if item['order_uid'] is not None:
                order_uid = item['order_uid']
               if item['location'] is not None:
                location = item['location']

               
               if item['booking_time']:
                booking_date = parser.parse(item['booking_time']).date()
               
               # tmpRow.append(item['id'])
               tmpRow.append(booking_date)
               tmpRow.append(order_uid)
               tmpRow.append(location)
               tmpRow.append(supplierFirstName + " " + supplierLastName)
               tmpRow.append(driverFirstName + " " + driverLastName)
               
               tmpRow.append(statusMsg)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
#------------------------ Single Details by ID BY GET -------------------------------------#
class RecordDetailsCompletedtrip(APIView):
    def get(self, request, id, format =None):
      data = {}
      locationWiseParcelArr = []
      recordDetails = NdOrder.objects.filter(id=id).first()
      ndSerializer = NdOrderSerializer(recordDetails)

      

      recordParcelDetails = NdParcelInformations.objects.filter(order__id=id)
      ndParcelSerializer = NdParcelInformationsSerializer(recordParcelDetails, many=True)
     
      recordDropoffDetails = NdDropOffLocation.objects.filter(order__id=id)
      ndDropoffSerializer = NdDropOffLocationSerializer(recordDropoffDetails, many=True)

      # Travelled location
      actual_distance_obj = NdOrderCompletionDetails.objects.filter(order__id=id).order_by('-id').values('actual_distance').first()
      data['actual_distance'] = actual_distance_obj['actual_distance']
      # Travelled location

      driverExists = False
      booking_date = ""
      if ndSerializer.data['driver'] is not None: 
        recordVehicleDetails = NdVehicleDetails.objects.filter(user__id=ndSerializer.data['driver']['id']).first()
        ndVehicleSerializer = NdVehicleDetailsSerializer(recordVehicleDetails)
        driverExists = True

      if ndSerializer.data['booking_time']:
                booking_date = parser.parse(ndSerializer.data['booking_time']).date()

      for x in recordDropoffDetails:    
        ndEachDropoffSerializer = NdDropOffLocationSerializer(x)

        location_wise_parcel_data = NdParcelInformations.objects.filter(location=x)
        locationWiseParcelSerializer = NdParcelInformationsSerializer(location_wise_parcel_data, many=True)
        
        location_wise_info = {}
        location_wise_info['drop_off_location_details'] = ndEachDropoffSerializer.data
        location_wise_info['parcel_files'] = locationWiseParcelSerializer.data
        locationWiseParcelArr.append(location_wise_info)
      data['order_details'] = ndSerializer.data
      data['order_parcel_info'] = ndParcelSerializer.data
      data['order_drop_off_locations'] = ndDropoffSerializer.data
      data['location_wise_parcel_data'] = locationWiseParcelArr
      data['booking_date'] = booking_date
      if driverExists == True :
        data['vehicle_details'] = ndVehicleSerializer.data
      if ndSerializer.data:
          # return Response([{"status" : True, "data" : ndSerializer.data}])
           return render( request, './completed_trip/completed_trip_details.html', data)
      else:
           return redirect("/")
          # return Response([{"status" : False, "msg" : "Sorry! No record is found"}]) 

# ==================== Map route list ==========================
class maproute_list(APIView):
    def get(self, request, id, format =None):
      data = {}
     
      recordDetails = NdCurrentDriverLocation.objects.filter(order__id=id).order_by('id')
      ndSerializer = NdLatLngDriverLocationSerializer(recordDetails, many=True)
      data['latLngList'] = ndSerializer.data
      #  Single data fetch 
      recordDetails1 = NdCurrentDriverLocation.objects.filter(order__id=id).order_by('id').first()
      ndSingleSerializer = NdLatLngDriverLocationSerializer(recordDetails1)
      data['latLngSingle'] = ndSingleSerializer.data

      recordStartLoc = NdOrderCompletionDetails.objects.filter(order__id=id, location_type=0).first()
      ndStartSerializer = NdOrderCompletionDetailsSerializer(recordStartLoc)
      data['latLngStart'] = ndStartSerializer.data

      record1stDropoff = NdOrderCompletionDetails.objects.filter(order__id=id, location_type=1).first()
      ndFirstDropSerializer = NdOrderCompletionDetailsSerializer(record1stDropoff)
      data['latLngFirstDrop'] = ndFirstDropSerializer.data

      record2ndtDropoff = NdOrderCompletionDetails.objects.filter(order__id=id, location_type=2).first()
      ndSecDropSerializer = NdOrderCompletionDetailsSerializer(record2ndtDropoff)
      data['latLngSecDropoff'] = ndSecDropSerializer.data
      # print("=================== id =============")
      # print(ndSerializer.data)
      # print("=================== id =============")
      
      if ndSerializer.data:
          return Response([{"status" : True, "data" : data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])   
# ==================== Map route single ==========================
class maproute_single(APIView):
    def get(self, request, id, format =None):
      # data = {}
     
      recordDetails = NdCurrentDriverLocation.objects.filter(order__id=id).order_by('id').first()
      ndSerializer = NdCurrentDriverLocationSerializer(recordDetails)
      # print("=================== single data =============")
      # print(ndSerializer.data)
      # print("=================== single data =============")
      
      if ndSerializer.data:
          return Response([{"status" : True, "data" : ndSerializer.data }])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])   
# ==================== Plan price ==========================
class subscription_plan_data(APIView):
    def get(self, request, id, prev_plan_id, format =None):
      data = {}
     
      recordDetails = NdSubscriptionPlan.objects.filter(id=id).first()
      ndSerializer = NdSubscriptionPlanSerializer(recordDetails)

      recordDetailsPrev = NdSubscriptionPlan.objects.filter(id=prev_plan_id).first()
      ndSerializerPrev = NdSubscriptionPlanSerializer(recordDetailsPrev)
      # print("=================== single data =============")
      # print(ndSerializer.data)
      # print("=================== single data =============")
      data['current_plan'] = ndSerializer.data
      data['prev_plan'] = ndSerializerPrev.data
      
      if ndSerializer.data:
          return Response([{"status" : True, "data" : data }])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])  
#---------------------- Push notifications ----------------------------
def push_notification_list( request ):
    
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Push Notifications Management"
        data['page_title'] = "Push Notifications Management"
        #---------------------------------All Countries--------------------------#
        

        allActiveData = NdUsers.objects.filter(is_status=True, is_deleted= False,role=settings.IS_DRIVER).count() 
        data['totalActive'] = allActiveData

        allDeactiveData = NdVehicleType.objects.filter(is_status=False, is_deleted= False).count() 
        data['totalDeactive'] = allDeactiveData


        roleDetails = NdRoles.objects.filter(is_status=True, is_deleted=False).exclude(id=settings.IS_ADMIN)
        roleSerializer = NdRolesSerializer(roleDetails, many=True)
        data['roles'] = roleSerializer.data

        data['WEBADMIN'] = settings.WEBADMIN_URL

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        # print(urlSegments)
        data['current_url_segments'] = urlSegments
        return render( request, './push_notifications/push_notifications.html', data)
    else:
        return redirect("/")

class push_notification(APIView):
  #------------------------ Get method to get all customer -------------------------------------# 
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'message_title',
            2 : 'message_body'
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]
        if draw == "1" :
            sortingType = "desc"
            sortingColumn = 0
        totalRecords = NdAdminPushNotifications.objects.filter(is_deleted =False).count()
        totalFiltered = totalRecords
        allRecord = NdAdminPushNotifications.objects.filter(is_deleted =False)
        
        if searchQ:
            allRecord = allRecord.filter(Q(message_title__icontains=searchQ) | Q(message_body__icontains=searchQ) )

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndSerializer = NdAdminPushNotificationsSerializer(allRecord, many=True)
        
        # return Response({ 'recordsFiltered' : flntUsersSerializer.data})
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               
               tmpRow = []
               featuredMode = ''
               # print("============= item===============")
               # print(item["role"]['id'])

               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
               role_title=""    
               if item['role']['role_title'] is not None:
                    role_title=item['role']['role_title']
               tmpRow.append(item['id'])
              
               tmpRow.append(item['message_title'])
               tmpRow.append(item['message_body'])
               # tmpRow.append(item['role'].role_title)
               tmpRow.append(role_title)

               
               tmpRow.append(statusMsg)
               # tmpRow.append(action)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        # return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        #------------------------ Put method to update details By ID -------------------------------------#     
    def put(self, request, pk, format=None):
        try:
            self.errorResult = list()
       
            if(request.data["message_title"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Message title  can not be blank", "field": "message_title"})
           
            if self.errorResult:
                return Response(self.errorResult)
            else:
                role_instance = NdRoles.objects.filter(id=request.data['role']).first()
                NdAdminPushNotifications.objects.filter(id=pk).update( message_title=request.data['message_title'], message_body=request.data['message_body'], role= role_instance)
                return Response([{"status" : True, "msg" : "You have successfully updated the record"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Please check not saved yet", "field": "mainError"})
            return Response(self.errorResult)

    #------------------------ POST method to Insert  details -------------------------------------# 
    def post(self, request, format=None):
        try:
            self.errorResult = list()
            
            if(request.data["message_title"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Message title can not be blank", "field": "message_title"})
            
            else:
                ndSerializer = NdAdminPushNotificationsSerializer(data=request.data)
                role_instance = NdRoles.objects.filter(id=request.data['role']).first()

                if ndSerializer.is_valid():
                    ndSerializer.save(role=role_instance)
                data = {};
                allActiveData = NdAdminPushNotifications.objects.filter(is_status=True, is_deleted= False).count() 
                data['totalActive'] = allActiveData

                allDeactiveData = NdAdminPushNotifications.objects.filter(is_status=False, is_deleted= False).count() 
                data['totalDeactive'] = allDeactiveData

                return Response([{"status" : True, "data" : data, "msg" : "You have successfully created", 'updated_record' : data}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Sorry! failed to save data", "field": "mainError"})
            return Response(self.errorResult)

#------------------------ Single User Details by ID BY GET -------------------------------------#
class RecordDetailsPushNotification(APIView):
    def get(self, request, id, format =None):
      recordDetails = NdAdminPushNotifications.objects.filter(id=id).first()
      ndSerializer = NdAdminPushNotificationsSerializer(recordDetails)
      if ndSerializer.data:
          return Response([{"status" : True, "data" : ndSerializer.data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])
#------------------------ Update multiple records BY LIST ID -------------------------------------#
class UpdateMultiRecordPushNotification(APIView):
    
    # tblArray = { }
    def post(self, request, format=None):
        # send_mail("hello paul", "comment tu vas?", "arijit.chandra@navsoft.in", ['arijit.chandra@navsoft.in'],fail_silently=False,)         
        # return Response({'status' : True,'sss': '1'})
       
        countingInfo = []
        if request.data['action'] == 'is_status' or request.data['action'] == 'rm':
            id_list = json.loads(request.data['ids']) 
            value = True
            if( request.data['value'] != '1'):
                value = False
           
            if request.data['action'] == 'is_status':
                NdAdminPushNotifications.objects.filter(id__in=id_list).update(is_status=value)

            if request.data['action'] == 'rm':
                NdAdminPushNotifications.objects.filter(id__in=id_list).update(is_deleted=value)
           
            allActivedata = NdAdminPushNotifications.objects.filter(is_status=True, is_deleted= False).count() 
           
            countingInfo.append({'totalActiveCustomers' : allActivedata})

            allDeactiveData = NdAdminPushNotifications.objects.filter(is_status=False, is_deleted= False).count() 
            
            countingInfo.append({'allDeactiveCustomer' : allDeactiveData})

            allCustomer = NdAdminPushNotifications.objects.filter(is_deleted= False).count() 
            # allTeacherallTeacher = allCustomer
            countingInfo.append({'allCustomer' : allCustomer})
                
            return Response([{"status" : True, "countingInfo" : countingInfo}])

        elif request.data['action'] == 'send_cred' :
            if json.loads(request.data['ids']):
                for ID in json.loads(request.data['ids']):
                    recordDetails = NdAdminPushNotifications.objects.filter(id=ID).first()
                    details = NdAdminPushNotificationsSerializer(recordDetails)
                    result = pushNotifications(details)
               
                return Response([{'status': True, 'msg' : 'Push notification has been sent to selected roles'}])
              
            else:
                return Response([{'status': False, 'msg' : 'Please select minimum one topic'}])

                
        else:
            return Response([{'status': False, 'msg' : 'Something went wrong'}])


# ===================== Push Notifications ========================

def pushNotifications( details ):

    print("================Details===============")
    print(details.data['role']['role_title'])
    
    print("================Details===============")
    topic_name = details.data['role']['role_title']
    message_title = details.data['message_title']
    message_body = details.data['message_body']
    # records = NdUsers.objects.all().filter(role=3).exclude(device_token=None)
                
    # ndUsersSerializer = NdUsersSerializer(records, many=True)
    # if ndUsersSerializer.data:
        # registration_ids = []
        # for item in ndUsersSerializer.data:
               
               
               
        #        registration_ids.append(item['device_token'])
               
        # print("=========== User details =================")
        # print(registration_ids)
    customParam = {}
    customParam['push_type'] = "ADMIN_PUSH_NOTIFY"
    customParam['body'] = message_body
    customParam['title'] = message_title

    result = push_service.notify_topic_subscribers(topic_name=topic_name, message_title=message_title, message_body=message_body, sound='notification.mp3', data_message=customParam)
    return result
    
# **************** Review type management **************************

def review_reason_list( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Review Reason Management"
        data['page_title'] = "Review Reason Management"

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        data['current_url_segments'] = urlSegments
        return render( request, './review_type/review_type.html', data)
    else:
        return redirect("/")

class review_reason(APIView):
  #------------------------ Get method to get all data list -------------------------------------# 
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'reason'
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]
        if draw == "1" :
            sortingType = "desc"
            sortingColumn = 0
        totalRecords = NdReviewTypes.objects.filter(is_deleted =False).count()
        totalFiltered = totalRecords
        allRecord = NdReviewTypes.objects.filter(is_deleted =False)
        if searchQ:
            allRecord = allRecord.filter(Q(review_reason__icontains=searchQ))

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndSerializer = NdReviewTypesSerializer(allRecord, many=True)
        
        # return Response({ 'recordsFiltered' : flntUsersSerializer.data})
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               tmpRow = []
               featuredMode = ''
               
               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
                                  
               
               tmpRow.append(item['id'])
               tmpRow.append(item['review_reason'])
               tmpRow.append(statusMsg)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        
        #------------------------ Put method to update customer details By ID -------------------------------------#     
    def put(self, request, pk, format=None):
        try:
            self.errorResult = list()
       
            if(request.data["review_reason"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Review reason can not be blank", "field": "review_reason"})
           
            if self.errorResult:
                return Response(self.errorResult)
            else:
                request.POST._mutable = True
                
                recordDetails = NdReviewTypes.objects.filter(id=pk).first()
                details = NdReviewTypesSerializer(recordDetails)
            
                NdReviewTypes.objects.filter(id=pk).update( review_reason=request.data['review_reason'])  

           
                return Response([{"status" : True, "msg" : "You have successfully updated the record"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Sorry! Data not updated", "field": "mainError"})
            return Response(self.errorResult)

    #------------------------ POST method to Insert customer details -------------------------------------# 
    def post(self, request, format=None):
        # try:
            self.errorResult = list()
            if(request.data["review_reason"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Reason can not be blank", "field": "review_reason"})
            
            else:
                ndSerializer = NdReviewTypesSerializer(data=request.data)
                if ndSerializer.is_valid():
                    ndSerializer.save()
                else:
                    print("===========================================")
                    print(ndSerializer.errors)
                    print("===========================================")
                data = {};
                allActiveData = NdReviewTypes.objects.filter(is_status=True, is_deleted= False).count() 
                data['totalActive'] = allActiveData

                allDeactiveData = NdReviewTypes.objects.filter(is_status=False, is_deleted= False).count() 
                data['totalDeactive'] = allDeactiveData

                return Response([{"status" : True, "data" : data, "msg" : "You have successfully created review reason", 'updated_record' : data}])
        # except Exception as e:
        #     self.errorResult.append({"status" : False,"msg" : "Sorry! Data not saved", "field": "mainError"})
        #     return Response(self.errorResult)

#------------------------ Single Details by ID BY GET -------------------------------------#
class RecordDetailsReviewReason(APIView):
    def get(self, request, id, format =None):
      recordDetails = NdReviewTypes.objects.filter(id=id).first()
      ndSerializer = NdReviewTypesSerializer(recordDetails)
      if ndSerializer.data:
          return Response([{"status" : True, "data" : ndSerializer.data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])
#------------------------ Update multiple records BY LIST ID -------------------------------------#
class UpdateMultiRecordReviewReason(APIView):
    def post(self, request, format=None):
        countingInfo = []
        if request.data['action'] == 'is_status' or request.data['action'] == 'rm':
            id_list = json.loads(request.data['ids']) 
            value = True
            if( request.data['value'] != '1'):
                value = False
           
            if request.data['action'] == 'is_status':
                NdReviewTypes.objects.filter(id__in=id_list).update(is_status=value)

            if request.data['action'] == 'rm':
                NdReviewTypes.objects.filter(id__in=id_list).update(is_deleted=value)
            
            return Response([{"status" : True, "msg" : 'Updated record successfully'}])
        else:
            return Response([{'status': False, 'msg' : 'Something went wrong'}])

# **************** Subscription Plan management **************************

def subscription_plan_list( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Subscription Plan Management"
        data['page_title'] = "Subscription Plan Management"

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        data['current_url_segments'] = urlSegments
        return render( request, './subscription_plan/subscription_plan.html', data)
    else:
        return redirect("/")

class subscription_plan(APIView):
  #------------------------ Get method to get all data list -------------------------------------# 
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'plan_name'
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]
        if draw == "1" :
            sortingType = "desc"
            sortingColumn = 0
        totalRecords = NdSubscriptionPlan.objects.filter(is_deleted =False).count()
        totalFiltered = totalRecords
        allRecord = NdSubscriptionPlan.objects.filter(is_deleted =False)
        if searchQ:
            allRecord = allRecord.filter(Q(plan_name__icontains=searchQ))

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndSerializer = NdSubscriptionPlanSerializer(allRecord, many=True)
        
        # return Response({ 'recordsFiltered' : flntUsersSerializer.data})
        ajaxData = []
        i = 1
        if ndSerializer.data:
            
            for item in ndSerializer.data:
               tmpRow = []
               featuredMode = ''
               
               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'
                                  
               
               tmpRow.append(item['id'])
               tmpRow.append(item['plan_name'])
               if item['price']:
                    tmpRow.append(item['price']+""+item['currency'])
               else:
                    tmpRow.append("N/A")
               tmpRow.append(statusMsg)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        
        #------------------------ Put method to update customer details By ID -------------------------------------#     
    def put(self, request, pk, format=None):
        try:
            self.errorResult = list()
       
            if(request.data["plan_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Plan name can not be blank", "field": "plan_name"})
           
            if self.errorResult:
                return Response(self.errorResult)
            else:
                request.POST._mutable = True
               
                if request.data['price']:
                    NdSubscriptionPlan.objects.filter(id=pk).update( price=price)  

                NdSubscriptionPlan.objects.filter(id=pk).update( plan_name=request.data['plan_name'], currency="KHR", ndcurrency_id=int(1))  

           
                return Response([{"status" : True, "msg" : "You have successfully updated the record"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Sorry! Data not updated", "field": "mainError"})
            return Response(self.errorResult)

    #------------------------ POST method to Insert customer details -------------------------------------# 
    def post(self, request, format=None):
        try:
            self.errorResult = list()
            if(request.data["plan_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Plan name can not be blank", "field": "plan_name"})
            
            else:

                ndSerializer = NdSubscriptionPlanSerializer(data=request.data)

                # print("============================")
                # print(request.data['price'])
                
                # ndSubscriptionPlan = NdSubscriptionPlan(plan_name=request.data['plan_name'], currency="KHR", ndcurrency_id=int(1))
                # ndSubscriptionPlan.save()


                if ndSerializer.is_valid():
                    ndSerializer.save()


                else:
                    print("===========================================")
                    print(ndSerializer.errors)
                    print("===========================================")
                data = {};
                allActiveData = NdSubscriptionPlan.objects.filter(is_status=True, is_deleted= False).count() 
                data['totalActive'] = allActiveData

                allDeactiveData = NdSubscriptionPlan.objects.filter(is_status=False, is_deleted= False).count() 
                data['totalDeactive'] = allDeactiveData

                return Response([{"status" : True, "data" : data, "msg" : "You have successfully created cancellation reason", 'updated_record' : data}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Sorry! Data not saved", "field": "mainError"})
            return Response(self.errorResult)

#------------------------ Single Details by ID BY GET -------------------------------------#
class RecordDetailsSubscriptionPlan(APIView):
    def get(self, request, id, format =None):
      recordDetails = NdSubscriptionPlan.objects.filter(id=id).first()
      ndSerializer = NdSubscriptionPlanSerializer(recordDetails)
      if ndSerializer.data:
          return Response([{"status" : True, "data" : ndSerializer.data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])
#------------------------ Update multiple records BY LIST ID -------------------------------------#
class UpdateMultiRecordSubscriptionPlan(APIView):
    def post(self, request, format=None):
        print(33333333333)
        countingInfo = []
        if request.data['action'] == 'is_status' or request.data['action'] == 'rm':
            id_list = json.loads(request.data['ids']) 
            value = True
            if( request.data['value'] != '1'):
                value = False
            print(value)
            if request.data['action'] == 'is_status':
                NdSubscriptionPlan.objects.filter(id__in=id_list).update(is_status=value)

            if request.data['action'] == 'rm':
                NdSubscriptionPlan.objects.filter(id__in=id_list).update(is_deleted=value)
            
            return Response([{"status" : True, "msg" : 'Updated record successfully'}])
        else:
            return Response([{'status': False, 'msg' : 'Something went wrong'}])

# # ------------------ Delete attachment file -----------------------
# class checkPhoneExists(APIView):
    
#     # tblArray = { }
#     def get(self, request, format=None):
#         try:
#             if request.data['attached_file']:
#                 NdAttachments.objects.filter(attached_file=request.data['attached_file']).update(is_deleted=True)
#                 return Response([{"status" : True, "msg" : "Deleted successfully"}])
#             else:
#                 return Response([{'status': False, 'msg' : 'Something went wrong'}])
#         except Exception as e:
#             self.errorResult.append({"status" : False,"msg" : "Please check all field properly", "field": "mainError"})
#             return Response(self.errorResult)

def policyFile( request ):
    
	data = {}
	data['title'] = "Privacy Policy"
	data['page_title'] = "Privacy Policy"
   
	data['WEBADMIN'] = settings.WEBADMIN_URL

	url = request.META['PATH_INFO'].split('/')
	urlSegments = list(filter(None, url)) 
	# print(urlSegments)
	data['current_url_segments'] = urlSegments
	return render( request, 'policy.html', data)

# ======================== Admin user management ========================

def adminuser_list( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Admin User Management"
        data['page_title'] = "Admin User Management"
        
        data['WEBADMIN'] = settings.WEBADMIN_URL

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        # print(urlSegments)
        data['current_url_segments'] = urlSegments
        data['app_name'] = "admin"
        return render( request, 'lists/lists.html', data)
    else:
        return redirect("/")



class adminuser(APIView):
  #------------------------ Get method to get all customer -------------------------------------# 
    def clean_password(self):
        self.cleaned_data['password'] = new1
        return new1

    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'first_name',
            2 : 'last_name',
            3 : 'email_id',
            4 : 'phone_number',
            5 : 'is_status'
        }
        sortingColumn = request.GET["order[0][column]"]

        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]
        totalRecords = NdUsers.objects.filter(is_deleted =False, role=settings.IS_ADMIN).count()
        totalFiltered = totalRecords
        allRecord = NdUsers.objects.filter(is_deleted =False, role=settings.IS_ADMIN).order_by(fieldSToSort[int(sortingColumn)])

        if searchQ:
            allRecord = allRecord.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).filter(Q(first_name__icontains=searchQ) | Q(last_name__icontains=searchQ)| Q(phone_number__icontains=searchQ)|\
             Q(email_id__icontains=searchQ)
             | Q(full_name__icontains=searchQ)
             )

        totalFiltered = allRecord.count()
       
        if sortingType == 'asc':
            allRecord = allRecord.order_by(fieldSToSort[int(sortingColumn)])
        else:
            allRecord = allRecord.order_by("-" + fieldSToSort[int(sortingColumn)])
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        
        ndUsersSerializer = NdUsersCreateSerializer(allRecord, many=True)
        # return Response({ 'recordsFiltered' : flntUsersSerializer.data})
        ajaxData = []
        i = 1
        if ndUsersSerializer.data:
            
            for item in ndUsersSerializer.data:
               tmpRow = []
               featuredMode = ''
               logo = ''
             
               recordDetails = NdAppliedCoupons.objects.filter(supplier=item['id']).first()
               couponDetails = NdAppliedCouponSerializer(recordDetails)
              

               promoCode = '<a href="#"" class="promoPopLink" data-action="promo_assign_view" data-id="'+str(item['id'])+'" style="color:#cc5200;"> Assign Promo</a>'
               if couponDetails.data['coupon']:
                if couponDetails.data['coupon']['promotion_code']:
                    promoCode = '<span style="color:#006600">'+couponDetails.data['coupon']['promotion_code']+'</span><a href="#"" class="promoPopLink" data-action="promo_assign_view" data-id="'+str(item['id'])+'"  style="color:#24248f"> Change </a>'
              
               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'

               tmpRow.append(item['id'])
               # tmpRow.append(logo)
               firstName = ""
               lastName = ""
               email_id = ""
               phone_number = ""
               if item['first_name'] is not None: 
                firstName = item['first_name']
               if item['last_name'] is not None:
                lastName =  item['last_name']
               if item['email_id'] is not None:
                email_id = item['email_id']
               if item['phone_number'] is not None:
                phone_number = item['phone_number']

               # tmpRow.append(image) 
               tmpRow.append(firstName+" "+lastName)
               tmpRow.append(email_id)
               tmpRow.append(phone_number)

               # tmpRow.append(promoCode)
               tmpRow.append(statusMsg)
               # tmpRow.append(action)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        # return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        #------------------------ Put method to update customer details By ID -------------------------------------#     
    def put(self, request, pk, format=None):
        try:

        # return Response({'s':type(int(request.data["duration"]))})
            self.errorResult = list()
        # return Response(request.data)
        # get_unique_email = self.get_unique_email(request.data)
        # return Response({'s':get_unique_email})
        # get_unique_phone = self.get_unique_phone(request.data)
            if(request.data["first_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "First Name can not be blank", "field": "first_name"})
            if(request.data["last_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Last Name can not be blank", "field": "last_name"})
            # if(get_unique_phone['status'] == False):
            #     self.errorResult.append({"status" : False,"msg" : get_unique_phone['msg'], "field": "phone_number"})
            if self.errorResult:
                return Response(self.errorResult)
                # return Response({"o":request.data["country_id"]})
            else:
                request.POST._mutable = True
                
                recordDetails = NdUsers.objects.filter(id=pk).first()
                details = NdUsersSerializer(recordDetails)
                NdUsers.objects.filter(id=pk).update( first_name=request.data['first_name'], last_name=request.data['last_name'], password=str(encrypt_val(request.data["password"])))  

           
                return Response([{"status" : True, "msg" : "You have successfully updated the record"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Please check! There is some error", "field": "mainError"})
            return Response(self.errorResult)

    #------------------------ POST method to Insert customer details -------------------------------------# 
    def post(self, request, format=None):
        # try:
            self.errorResult = list()
            
            if(request.data["first_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "First Name can not be blank", "field": "first_name"})
            if(request.data["last_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Last Name can not be blank", "field": "last_name"})
            
            else:

                request.POST._mutable = True
                request.data['password'] = str(encrypt_val(request.data["password"]))

                ndUsersCreateSerializer = NdAdminUsersCreateSerializer(data=request.data)
               
                user_role_id =  settings.IS_ADMIN
                role_instance = NdRoles.objects.filter(id=user_role_id).first()

                # p = NdUsers(first_name=request.data['first_name'], last_name=request.data['last_name'], email_id=request.data['email_id'], phone_number=request.data["phone_number"], password=request.data["password"])
                # p.save(role=role_instance)
                data = {};
                if ndUsersCreateSerializer.is_valid():
                    ndUsersCreateSerializer.save(role=role_instance)
                else:
                    # ndUsersCreateSerializer.errors
                    print(ndUsersCreateSerializer.errors)
               
                return Response([{"status" : True,  "msg" : "You have successfully created the profile", 'updated_record' : data}])
        # except Exception as e:
        #     self.errorResult.append({"status" : False,"msg" : "Sorry! Data not uploaded", "field": "mainError"})
        #     return Response(self.errorResult)

#------------------------ Single User Details by ID BY GET -------------------------------------#
class RecordDetailsAdminUser(APIView):
    def get(self, request, id, format =None):
      recordDetails = NdUsers.objects.filter(id=id).first()
      ndStatesSerializer = NdUsersCreateSerializer(recordDetails)
      if ndStatesSerializer.data:
          return Response([{"status" : True, "data" : ndStatesSerializer.data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])
#------------------------ Update multiple records BY LIST ID -------------------------------------#
class UpdateMultiRecordAdminUsers(APIView):
    
    # tblArray = { }
    def post(self, request, format=None):
        # send_mail("hello paul", "comment tu vas?", "arijit.chandra@navsoft.in", ['arijit.chandra@navsoft.in'],fail_silently=False,)         
        # return Response({'status' : True,'sss': '1'})
       
        countingInfo = []
        if request.data['action'] == 'is_status' :
            id_list = json.loads(request.data['ids']) 
            value = True
            if( request.data['value'] != '1'):
                value = False
           
            NdUsers.objects.filter(id__in=id_list).update(is_status=value)
           
            allActiveCustomer = NdUsers.objects.filter(is_status=True, is_deleted= False).count() 
            totalActiveCustomers = allActiveCustomer
            countingInfo.append({'totalActiveCustomers' : totalActiveCustomers})

            allDeactiveCustomer = NdUsers.objects.filter(is_status=False, is_deleted= False).count() 
            allDeactiveCustomer = allDeactiveCustomer
            countingInfo.append({'allDeactiveCustomer' : allDeactiveCustomer})

            allCustomer = NdUsers.objects.filter(is_deleted= False).count() 
            # allTeacherallTeacher = allCustomer
            countingInfo.append({'allCustomer' : allCustomer})
                
            return Response([{"status" : True, "countingInfo" : countingInfo}])
        elif request.data['action'] != 'send_cred' :
            id_list = json.loads(request.data['ids']) 
            value = True
            if( request.data['value'] != '1'):
                value = False
            if( request.data.get('action') == 'rm'):
               
                NdUsers.objects.filter(id__in=id_list).update(is_deleted=value)
            else:
                NdUsers.objects.filter(id__in=id_list).update(is_status=value)
                allActiveCustomer = NdUsers.objects.filter(is_status=True, is_deleted= False).count() 
                totalActiveCustomers = allActiveCustomer
                countingInfo.append({'totalActiveCustomers' : totalActiveCustomers})

                
            return Response([{"status" : True, "countingInfo" : countingInfo}])
       
        else:
            return Response([{'status': False, 'msg' : 'Something went wrong1'}])


# ------------------ Unique phone -----------------------
class checkUniqueEmail(APIView):
    def post(self, request, format=None):
        try:
            is_exists = NdUsers.objects.filter(email_id=request.data['email_id'],role=settings.IS_ADMIN,is_deleted=False).count()
           
            if( is_exists>0 ):
                return Response([{"status" : False, "msg" : "Email id already exists"}])
            else:
                return Response([{'status': True, 'msg' : 'Not exists'}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Please check all field properly", "field": "mainError"})
            return Response(self.errorResult)
