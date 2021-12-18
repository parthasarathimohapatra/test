from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect
from webAdmin.serializers import *
from django.template import RequestContext
from rest_framework.views import APIView
from django.utils.crypto import get_random_string
import json
from django.db.models import Value
from django.db.models.functions import Concat

from django.conf import settings
from webAdmin.models import NdUsers, NdOrder
from django.contrib.staticfiles.templatetags.staticfiles import static
import os
from webAdmin.views import encrypt, decrypt, encrypt_val, decrypt_val
from commonApp.views import fieldEmptyCheck, pushNotificationFCM
from dateutil import parser
import datetime
from pyfcm import FCMNotification
push_service = FCMNotification(api_key=settings.FCM_API_KEY)

def file_path_ext(file_path):
    filename, file_extension = os.path.splitext(file_path)
    return file_extension

def driver_list( request ):
    
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Driver Management"
        data['page_title'] = "Driver Management"
        #---------------------------------All Countries--------------------------#
        allModel = NdVehicleModel.objects.filter(is_status=True, is_deleted= False).order_by('model_name') 
        ndVehiclModelSerializer = NdVehiclModelSerializer(allModel, many=True)
        data['vehicleModels'] = ndVehiclModelSerializer.data

        allVehicleType = NdVehicleType.objects.filter(is_status=True, is_deleted= False).order_by('vehicle_type_name') 
        
        ndVehicleTypeSerializer = NdVehicleTypeSerializer(allVehicleType, many=True)
        data['vehicleTypes'] = ndVehicleTypeSerializer.data

        allCountries = NdCountries.objects.all().order_by('country_name') 
        ndCountriesSerializer = NdCountriesSerializer(allCountries, many=True)
        data['countries'] = ndCountriesSerializer.data

        # allActiveCustomer = NdVehicleType.objects.filter(is_status=True, is_deleted= False,role=settings.IS_DRIVER).count() 
        # data['totalActive'] = allActiveCustomer

        year_dropdown = []
        for y in range((datetime.datetime.now().year - 9), (datetime.datetime.now().year + 1)):
            year_dropdown.append((y))

        allDeactiveData = NdUsers.objects.filter(is_status=False, is_deleted= False,role=settings.IS_DRIVER).count() 
        data['totalDeactive'] = allDeactiveData

        data['WEBADMIN'] = settings.WEBADMIN_URL
        data['year_dropdown'] = year_dropdown

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        # print(urlSegments)
        data['current_url_segments'] = urlSegments
        data['app_name'] = "driver"
        return render( request, './lists/lists.html', data)
    else:
        return redirect("/")



class driver(APIView):
  #------------------------ Get method to get all customer -------------------------------------# 
    tmpSaveData = []
    #------------------------ Method to check unique email -------------------------------------# 
    def get_unique_email(self, request):
        
        if(request.get('email_id') == ""):
            return {'status': False, 'msg': "Email Id can not be blank"}
        if(request.get('id') != ''):
            # return "aaa"
            is_exists = NdUsers.objects.filter(Q(email_id__iexact=request.get('email_id')), ~Q(id=request.get('id')), Q(is_deleted=False)).count()
        else:
            is_exists = NdUsers.objects.filter(email_id__iexact=request.get('email_id'), is_deleted=False).count()
        if( is_exists>0 ):
            return {'status': False, 'msg': "Email Id already exists"}
        else:
            return {'status': True}
    #------------------------ Method to check unique phone number -------------------------------------#         
    def get_unique_phone(self, request):
        if(request.get('phone_number') == ""):
            return {'status': False, 'msg': "Phone Number can not be blank"}
        if(request.get('id') != ''):
            is_exists = NdUsers.objects.filter(Q(phone_number=request.get('phone_number')), ~Q(id=request.get('id')), Q(is_deleted=False)).count()
        else:
            is_exists = NdUsers.objects.filter(phone_number=request.get('phone_number'),role=settings.IS_DRIVER,is_deleted=False).count()
        if( is_exists>0 ):
            return {'status': False, 'msg': "Phone Number already exists"}
        else:
            return {'status': True}
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'first_name',
            2 : 'last_name'
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]

        print("=============sortingColumn==============")
        print(sortingColumn)
        print("===========sortingType================")
        print(sortingType)
       
        # if draw == "1" :
        #     sortingType = "desc"
        #     sortingColumn = 0
        totalRecords = NdUsers.objects.filter(is_deleted =False, role=settings.IS_DRIVER).count()
        totalFiltered = totalRecords
        allRecord = NdUsers.objects.filter(is_deleted =False, role=settings.IS_DRIVER)

        if searchQ:
            allRecord = allRecord.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).filter(Q(first_name__icontains=searchQ) | Q(last_name__icontains=searchQ)|\
             Q(email_id__icontains=searchQ)
             | Q(phone_number__icontains=searchQ)
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

               
               
               vehicle_details = NdVehicleDetails.objects.filter(user__id=item['id']).first()
               ndVehicleDetailsSerializer = NdVehicleDetailsSerializer(vehicle_details)
              
               tmpRow = []
               featuredMode = ''
               logo = ''
               plate_number = ''
                
               image = ''
               if item['profile_picture']:
                    image = '<img src="'+ item['profile_picture']+'?time='+ str(datetime.datetime.now())+' " class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               else:
                    image = '<img src="'+static("images/avatar.jpg")+'" class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               
               statusMsg = '<img src="'+static("images/checked.png")+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static("images/error.png")+' " class="big-img-loader" >'
               
               viewMsg =   ' <a href="details/'+str(item['id'])+'" class="btn-round-primary"> <i class="fa fa-eye" aria-hidden="true"></i></a> '

               if ndVehicleDetailsSerializer.data :
                    plate_number = ndVehicleDetailsSerializer.data['plate_number']


               tmpRow.append(item['id'])
               tmpRow.append(image)
               tmpRow.append(item['first_name'] + " "  + item['last_name'])
               tmpRow.append(item['email_id'])
               tmpRow.append(item['phone_number'])
               tmpRow.append(plate_number)
               tmpRow.append(statusMsg)
               tmpRow.append(viewMsg)
               # tmpRow.append(action)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        # return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        #------------------------ Put method to update customer details By ID -------------------------------------#     
    def put(self, request, pk, format=None):
        try:

            self.errorResult = list()
            get_unique_email = self.get_unique_email(request.data)
            get_unique_phone = self.get_unique_phone(request.data)
            
            self.tmpSaveData = list()
            if(request.data["first_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "First Name can not be blank", "field": "first_name"})
            if(request.data["last_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Last Name can not be blank", "field": "last_name"})

      
            
            # if(get_unique_email['status'] == False):
            #     self.errorResult.append({"status" : False,"msg" : get_unique_email['msg'], "field": "email_id"})
            # if(get_unique_phone['status'] == False):
            #     self.errorResult.append({"status" : False,"msg" : get_unique_phone['msg'], "field": "phone_number"})
            
            if self.errorResult:
                return Response(self.errorResult)
                # return Response({"o":request.data["country_id"]})
            else:
                request.POST._mutable = True

                driver_instance = NdUsers.objects.filter(id=pk).first()
                
                # if bool(request.FILES.get('profile_picture', False)) == True:
                #     u = NdUsers.objects.get(id = pk)
                #     ndUsersProfileImage = NdUsersProfilePicture(u, data={'profile_picture' : request.FILES['profile_picture']})
                #     if ndUsersProfileImage.is_valid():
                #         ndUsersProfileImage.save()
                wheel_chair_support = False
                booster_seat_support = False
                
               
                # if request.data['wheel_chair_support'] :
                # if 'wheel_chair_support' in request.GET:
                # id_list = json.loads(request.data['ids']) 
                if 'wheel_chair_support' in request.data:
                    wheel_chair_support = True
                # if request.data['booster_seat_support'] :
                if 'booster_seat_support' in request.data:
                    booster_seat_support = True


                country_instance = NdCountries.objects.filter(id=request.data['country']).first()

                if request.data['registration_expiry_date']:
                    registration_expiry_date = request.data['registration_expiry_date']

                if request.data['insurance_expiry_date']:
                    insurance_expiry_date = request.data['insurance_expiry_date']

                if request.data['dob']:
                    NdUsers.objects.filter(id=pk).update( dob=request.data['dob'] )  
                NdUsers.objects.filter(id=pk).update( first_name=request.data['first_name'], last_name=request.data['last_name'], gender=request.data['gender'], country=country_instance, is_phone_no_verified=True, password=str(encrypt_val(request.data["password"])))  
                
                if bool(request.FILES.get('profile_picture', False)) == True:
                    u = NdUsers.objects.get(id = pk)
                    ndUserImage = NdUsersProfilePicture(u, data={'profile_picture' : request.FILES['profile_picture']})
                    if ndUserImage.is_valid():
                        ndUserImage.save()

                # request.data['password'] = str(encrypt_val(request.data["password"]))        
                # Driver details update
                vehicle_type_instance = NdVehicleType.objects.filter(id=request.data['vehicle_type']).first()
                if request.data['driving_licence_expiry_date']:
                    NdDriverDetails.objects.filter(user=pk).update( driving_licence_expiry_date=request.data['driving_licence_expiry_date'], vehicle_type=vehicle_type_instance)  
                else :
                    NdDriverDetails.objects.filter(user=pk).update(vehicle_type=vehicle_type_instance) 
                # Vehicle details update
                if request.data['registration_expiry_date']:
                     NdVehicleDetails.objects.filter(user=pk).update(registration_expiry_date=registration_expiry_date) 
                if request.data['insurance_expiry_date']:
                     NdVehicleDetails.objects.filter(user=pk).update(insurance_expiry_date=insurance_expiry_date) 

                vehicle_model_instance = NdVehicleModel.objects.filter(id=request.data['vehicle_model']).first()
                NdVehicleDetails.objects.filter(user=pk).update( plate_number=request.data['plate_number'], year=request.data['year'], vehicle_model=vehicle_model_instance)  

                if bool(request.FILES.get('image_file', False)) == True:
                    v = NdVehicleDetails.objects.get(user_id = pk)
                    ndVehicleImage = NdVehicleDetailsSerializer(v, data={'image_file' : request.FILES['image_file']})
                    if ndVehicleImage.is_valid():
                        ndVehicleImage.save()

                # ************* START Attachment save ******************
                for dl in request.FILES.getlist('driver_licence'):
                    NdAttachments.objects.create(user=driver_instance, attached_file=dl, object_type_id=int(3))

                for vi in request.FILES.getlist('vehicle_insurance'):
                    NdAttachments.objects.create(user=driver_instance, attached_file=vi, object_type_id=int(5))

                for vr in request.FILES.getlist('vehicle_registration'):
                    NdAttachments.objects.create(user=driver_instance, attached_file=vr, object_type_id=int(4))

                # ************* END Attachment save ******************
                    
           
                return Response([{"status" : True, "msg" : "You have successfully updated the record"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Please check all field properly", "field": "mainError"})
            return Response(self.errorResult)

    #------------------------ POST method to Insert customer details -------------------------------------# 
    def post(self, request, format=None):
        try:
            self.errorResult = list()
            get_unique_email = self.get_unique_email(request.data)
            get_unique_phone = self.get_unique_phone(request.data)
            
            self.tmpSaveData = list()
            if(request.data["first_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "First Name can not be blank", "field": "first_name"})

            if(request.data["last_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Last Name can not be blank", "field": "last_name"})
            if(request.data["driving_licence_expiry_date"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Driving licence expiry_date can not be blank", "field": "driving_licence_expiry_date"})
            if(request.data['email_id']!=""):
                if(get_unique_email['status'] == False):
                    self.errorResult.append({"status" : False,"msg" : get_unique_email['msg'], "field": "email_id"})
            if(get_unique_phone['status'] == False):
                self.errorResult.append({"status" : False,"msg" : get_unique_phone['msg'], "field": "phone_number"})
             
            
            if self.errorResult:
                return Response(self.errorResult)
            else:
                request.POST._mutable = True
                
                # request.data['dob'] = parse_date(request.data['dob'])
                # request.POST['registration_method'] = 'app_reg'
                # random_code = self.randomPassword( request )
                # request.POST._mutable = True
                request.data['password'] = str(encrypt_val(request.data["password"]))

                # profile_picture = request.FILES.get('profile_picture', False) NdVehicleDetailsWithoutImageSerializer
                if bool(request.FILES.get('profile_picture', False)) == True:
                    ndUsersCreateSerializer = NdUsersCreateSerializer(data=request.data)
                else:
                    ndUsersCreateSerializer = NdUsersCreateWithoutDPSerializer(data=request.data)

                if bool(request.FILES.get('image_file', False)) == True:
                    ndVehicleCreateSerializer = NdVehicleDetailsSerializer(data=request.data)
                else:
                    ndVehicleCreateSerializer = NdVehicleDetailsWithoutImageSerializer(data=request.data)

                # ndUsersCreateSerializer = NdUsersCreateSerializer(data=request.data) 
                # ndVehicleCreateSerializer = NdVehicleDetailsSerializer(data=request.data)
                ndDriverDetailsSerializer = NdDriverDetailsSerializer(data=request.data)


                # Creating role instace
               
                user_role_id =  settings.IS_DRIVER
                role_instance = NdRoles.objects.filter(id=user_role_id).first()


                country_id =  request.data['country']
                country_instance = NdCountries.objects.filter(id=country_id).first()

                # state_id =  request.data['state']
                # state_instance = NdStates.objects.filter(id=state_id).first()
               
               

                if ndUsersCreateSerializer.is_valid():
                    # driver = ndUsersCreateSerializer.save(role=role_instance, country=country_instance, state=state_instance)
                    driver = ndUsersCreateSerializer.save(role=role_instance, country=country_instance)
                    
                    
                    driver_id =  driver.id
                    driver_instance = NdUsers.objects.filter(id=driver_id).first()

                    vehicle_type_instance = NdVehicleType.objects.filter(id=request.data['vehicle_type']).first()

                    vehicle_model_instance = NdVehicleModel.objects.filter(id=request.data['vehicle_model']).first()

                    if ndVehicleCreateSerializer.is_valid():
                        ndVehicleCreateSerializer.save(user=driver_instance,vehicle_model = vehicle_model_instance)
                    
                    if ndDriverDetailsSerializer.is_valid():
                        ndDriverDetailsSerializer.save(user=driver_instance,vehicle_type = vehicle_type_instance)
                    
                    # ************* START Attachment save ******************
                    for dl in request.FILES.getlist('driver_licence'):
                        NdAttachments.objects.create(user=driver_instance, attached_file=dl, object_type_id=int(3))

                    for vi in request.FILES.getlist('vehicle_insurance'):
                        NdAttachments.objects.create(user=driver_instance, attached_file=vi, object_type_id=int(5))

                    for vr in request.FILES.getlist('vehicle_registration'):
                        NdAttachments.objects.create(user=driver_instance, attached_file=vr, object_type_id=int(4))

                     # ************* END Attachment save ******************

                else:
                    print("===========================================")
                    print(ndUsersCreateSerializer.errors)
                    print("===========================================")
                data = {};
                allActiveCustomer = NdUsers.objects.filter(is_status=True, is_deleted= False,role=settings.IS_CUSTOMER).count() 
                data['totalActive'] = allActiveCustomer

                allDeactiveCustomer = NdUsers.objects.filter(is_status=False, is_deleted= False,role=settings.IS_CUSTOMER).count() 
                data['totalDeactive'] = allDeactiveCustomer

                return Response([{"status" : True, "data" : data, "msg" : "You have successfully created the profile", 'updated_record' : data}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Please check all field properly", "field": "mainError"})
            return Response(self.errorResult)
    def randomPassword( self, request ):
        # return "1111"
        random_code = get_random_string(length=4, allowed_chars='123456789')
        randomKeycheck = NdUsers.objects.filter(verification_code=random_code, is_deleted=False).count()
        if randomKeycheck >0 :
            self.randomPassword( request )
        else:
            return random_code
#------------------------ Single User Details by ID BY GET -------------------------------------#
class RecordDetailsDriver(APIView):
    def get(self, request, id, format =None):
      data = {}
      locationWiseParcelArr = []
      recordDetails = NdUsers.objects.filter(id=id).first()
      ndSerializer = NdUsersDriverSerializer(recordDetails)

      driverDetails = NdDriverDetails.objects.filter(user__id=id).first()
      ndDriverDetailsSerializer = NdDriverDetailsSerializer(driverDetails)
      
      vehicleDetails = NdVehicleDetails.objects.filter(user__id=id).first()
      ndVehicleDetailsSerializer = NdVehicleDetailsSerializer(vehicleDetails)

      #Driving licence attacments

      drivingLicenceAttachments = NdAttachments.objects.filter(user__id=id, object_type__id=3)
      driverAttachments = []
      drivingLicence = {}
      pdf_files = []
      img_files = []
      for single_data in drivingLicenceAttachments :
       
        
        filename = single_data.attached_file.name
        fileurl = single_data.attached_file.url
        ext = file_path_ext(filename)
        if ext.lower() == '.pdf':
            pdf_files.append(fileurl)
        else :
            img_files.append(fileurl)
      driverAttachments = [['pdf',pdf_files],['img',img_files]]
      #Driving licence attacments

      #Vehicle Registration attacments
      vehicleRegistrationAttachments = NdAttachments.objects.filter(user__id=id, object_type__id=4)
      vehicleRegistration = []
      pdf_files = []
      img_files = []
      for single_data in vehicleRegistrationAttachments :
       
        filename = single_data.attached_file.name
        fileurl = single_data.attached_file.url
        ext = file_path_ext(filename)
        if ext.lower() == '.pdf':
            pdf_files.append(fileurl)
        else :
            img_files.append(fileurl)
      vehicleRegistration = [('pdf',pdf_files),('img',img_files)]
      #Vehicle Registration attacments

      #Vehicle insurance attacments
      vehicleInsuranceAttachments = NdAttachments.objects.filter(user__id=id, object_type__id=5)
      vehicleInsurance = []
      pdf_files = []
      img_files = []
      for single_data in vehicleInsuranceAttachments :
       
        filename = single_data.attached_file.name
        fileurl = single_data.attached_file.url
        ext = file_path_ext(filename)
        if ext.lower() == '.pdf':
            pdf_files.append(fileurl)
        else :
            img_files.append(fileurl)
      vehicleInsurance = [('pdf',pdf_files),('img',img_files)]
      #Vehicle Registration attacments

       
      data['details_data'] = ndSerializer.data
      data['vehicle_details'] = ndVehicleDetailsSerializer.data
      data['driver_details'] = ndDriverDetailsSerializer.data
      data['driverAttachments'] = driverAttachments
      data['vehicleRegistration'] = vehicleRegistration
      data['vehicleInsurance'] = vehicleInsurance
      # data['location_wise_parcel_data'] = locationWiseParcelArr
      if ndSerializer.data:
          # return Response([{"status" : True, "data" : ndSerializer.data}])
           return render( request, './lists/driver-details.html', data)
      else:
           return redirect("/")

#------------------------ Single User Details by ID BY GET -------------------------------------#
class RecordDetailsDriverPopUp(APIView):
    def get(self, request, id, format =None):
      data = {}
      locationWiseParcelArr = []
      recordDetails = NdUsers.objects.filter(id=id).first()
      ndSerializer = NdUsersDriverSerializer(recordDetails)

      driverDetails = NdDriverDetails.objects.filter(user__id=id).first()
      ndDriverDetailsSerializer = NdDriverDetailsSerializer(driverDetails)
      
      vehicleDetails = NdVehicleDetails.objects.filter(user__id=id).first()
      ndVehicleDetailsSerializer = NdVehicleDetailsSerializer(vehicleDetails)

      #Driving licence attacments

      drivingLicenceAttachments = NdAttachments.objects.filter(user__id=id, object_type__id=3,is_deleted=False)
      driverAttachments = []
      drivingLicence = {}
      pdf_files = []
      img_files = []
      for single_data in drivingLicenceAttachments :
       
        
        filename = single_data.attached_file.name
        fileurl = single_data.attached_file.url
        ext = file_path_ext(filename)
        if ext.lower() == '.pdf':
            pdf_files.append(fileurl)
        else :
            img_files.append(fileurl)
      driverAttachments = [['pdf',pdf_files],['img',img_files]]
      #Driving licence attacments

      #Vehicle Registration attacments
      vehicleRegistrationAttachments = NdAttachments.objects.filter(user__id=id, object_type__id=4, is_deleted=False)
      vehicleRegistration = []
      pdf_files = []
      img_files = []
      for single_data in vehicleRegistrationAttachments :
       
        filename = single_data.attached_file.name
        fileurl = single_data.attached_file.url
        ext = file_path_ext(filename)
        if ext.lower() == '.pdf':
            pdf_files.append(fileurl)
        else :
            img_files.append(fileurl)
      vehicleRegistration = [('pdf',pdf_files),('img',img_files)]
      #Vehicle Registration attacments

      #Vehicle insurance attacments
      vehicleInsuranceAttachments = NdAttachments.objects.filter(user__id=id, object_type__id=5,is_deleted=False)
      vehicleInsurance = []
      pdf_files = []
      img_files = []
      for single_data in vehicleInsuranceAttachments :
       
        filename = single_data.attached_file.name
        fileurl = single_data.attached_file.url
        ext = file_path_ext(filename)
        if ext.lower() == '.pdf':
            pdf_files.append(fileurl)
        else :
            img_files.append(fileurl)
      vehicleInsurance = [('pdf',pdf_files),('img',img_files)]
      #Vehicle Registration attacments
      
      data['password'] = decrypt_val(ndSerializer.data['password'])
      data['details_data'] = ndSerializer.data
      data['vehicle_details'] = ndVehicleDetailsSerializer.data
      data['driver_details'] = ndDriverDetailsSerializer.data
      data['driverAttachments'] = driverAttachments
      data['vehicleRegistration'] = vehicleRegistration
      data['vehicleInsurance'] = vehicleInsurance
      # data['location_wise_parcel_data'] = locationWiseParcelArr
      
      if ndSerializer.data:
          # return Response([{"status" : True, "data" : ndSerializer.data}])
          return Response([{"status" : True, "data" : data}])
           # return render( request, './lists/driver-details.html', data)
      else:
           return redirect("/")

def driverAddForm(request) :
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Driver Registration"
        data['page_title'] = "Driver Registration"
        #---------------------------------All Countries--------------------------#
 

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        # print(urlSegments)
        data['current_url_segments'] = urlSegments
        data['app_name'] = "driver"
        return render( request, './lists/driver-form.html', data)
    else:
        return redirect("/")
#------------------------ Update multiple records BY LIST ID -------------------------------------#
class UpdateMultiRecordUsers(APIView):
    def sendPushToOlderLoggedInUser(self, request, customParam, dataFields):
        userIDS = dataFields['userIDS']
  
        if dataFields['deviceIDS']:
            deviceIDS = dataFields['deviceIDS']
            pushNotificationFCM.send_push_notification( deviceIDS, userIDS, 
            {"title": dataFields['title'], "body": dataFields['body'], "notification_type_id" : 4}, customParam)
        return True
    # tblArray = { }
    def post(self, request, format=None):
       
        countingInfo = []
        if request.data['action'] == 'is_status' :
            id_list = json.loads(request.data['ids']) 
            value = True
            if( request.data['value'] != '1'):
                value = False
          
            
            if value == False:
                deviceTokenArr = []
                userIDSArr = []
                if id_list:
                    for item in id_list:
                        userDetailsIns = NdUsers.objects.filter(Q(id=int(item))).values('device_token', 'id')
                        if userDetailsIns.exists():
                            userDetailsObj = userDetailsIns.first()
                            bookingStatus = NdOrder.objects.filter(Q(booking_status=settings.BOOKING_STATUS_PLACED), Q(driver_id=int(item)))
                            if fieldEmptyCheck(userDetailsObj['device_token']) :
                                deviceTokenArr.append(userDetailsObj['device_token'])
                                userIDSArr.append(userDetailsObj['id'])
                            if bookingStatus.count()==0:
                                NdUsers.objects.filter(id=int(item)).update(is_status=value)
                
                    title = 'Account Deactivated'
                    body = "Your account has been deactivated by Admin"
                    deviceIDS = deviceTokenArr
                    userIDS = userIDSArr
                    dataFields = {"title":title, "body":body, "deviceIDS":deviceIDS, "userIDS":userIDS }    
                    customParam = {}
                    customParam['push_type'] = settings.NOTIFICATION_TYPE['session_expired']
                    customParam['body'] = body
                    customParam['title'] = title
                    if deviceIDS:
                        self.sendPushToOlderLoggedInUser(request, customParam, dataFields)   
            else:
                NdUsers.objects.filter(id__in=id_list).update(is_status=value)
            allActiveCustomer = NdUsers.objects.filter(is_status=True, is_deleted= False).count() 
            totalActiveCustomers = allActiveCustomer
            countingInfo.append({'totalActiveCustomers' : totalActiveCustomers})

            allDeactiveCustomer = NdUsers.objects.filter(is_status=False, is_deleted= False).count() 
            allDeactiveCustomer = allDeactiveCustomer
            countingInfo.append({'allDeactiveCustomer' : allDeactiveCustomer})

            allCustomer = NdUsers.objects.filter(is_deleted= False).count() 
            
            countingInfo.append({'allCustomer' : allCustomer})
  
            return Response([{"status" : True, "countingInfo" : countingInfo}])
        if request.data['action'] == 'rm' :
            id_list = json.loads(request.data['ids']) 
            value = True
            # if( request.data['value'] != '1'):
            #     value = False
           
            
            if value == True:
                deviceTokenArr = []
                userIDSArr = []
                if id_list:
                    for item in id_list:
                        userDetailsIns = NdUsers.objects.filter(Q(id=int(item))).values('device_token', 'id')
                        if userDetailsIns.exists():
                            userDetailsObj = userDetailsIns.first()
                            bookingStatus = NdOrder.objects.filter(Q(booking_status=settings.BOOKING_STATUS_PLACED), Q(driver_id=int(item)))
                            if fieldEmptyCheck(userDetailsObj['device_token']):
                                deviceTokenArr.append(userDetailsObj['device_token'])
                                userIDSArr.append(userDetailsObj['id'])
                            if bookingStatus.count()==0:  
                                NdUsers.objects.filter(id=int(item)).update(is_deleted=value)
                    title = 'Account Deleted'
                    body = "Your account has been deleted by Admin"
                    deviceIDS = deviceTokenArr
                    userIDS = userIDSArr
                    dataFields = {"title":title, "body":body, "deviceIDS":deviceIDS, "userIDS":userIDS }    
                    customParam = {}
                    customParam['push_type'] = settings.NOTIFICATION_TYPE['session_expired']
                    customParam['body'] = body
                    customParam['title'] = title
                    self.sendPushToOlderLoggedInUser(request, customParam, dataFields)

            else:
                NdUsers.objects.filter(id__in=id_list).update(is_deleted=value)
           
            allActiveCustomer = NdUsers.objects.filter(is_status=True, is_deleted= False).count() 
            totalActiveCustomers = allActiveCustomer
            countingInfo.append({'totalActiveCustomers' : totalActiveCustomers})

            allDeactiveCustomer = NdUsers.objects.filter(is_status=False, is_deleted= False).count() 
            allDeactiveCustomer = allDeactiveCustomer
            countingInfo.append({'allDeactiveCustomer' : allDeactiveCustomer})

            allCustomer = NdUsers.objects.filter(is_deleted= False).count() 
            
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


#------------------------ Driver joining month and location wise  -------------------------------------#
class DriverJoiningReport(APIView):
    def get(self, request,  format =None):
        if 'authSession' in request.session:
            data = {}
            data['title'] = "Driver joining report"
            data['page_title'] = "Driver joining report"
            #---------------------------------All Countries--------------------------#
            # allCountries = NdCountries.objects.order_by('country_name') 
            # ndCountriesSerializer = NdCountriesSerializer(allCountries, many=True)
            # data['countries'] = ndCountriesSerializer.data

            # allActiveCustomer = NdUsers.objects.filter(is_status=True, is_deleted= False,role=settings.IS_DRIVER).count() 
            # data['totalActive'] = allActiveCustomer

            # allDeactiveData = NdUsers.objects.filter(is_status=False, is_deleted= False,role=settings.IS_DRIVER).count() 
            # data['totalDeactive'] = allDeactiveData

            data['WEBADMIN'] = settings.WEBADMIN_URL

            url = request.META['PATH_INFO'].split('/')
            urlSegments = list(filter(None, url)) 
            # print(urlSegments)
            data['current_url_segments'] = urlSegments
            data['app_name'] = "driver"
            # return render( request, './lists/lists.html', data)
            return render( request, './report/driver_joining_report.html', data)

        else:
         return redirect("/")

# ------------------ Delete attachment file -----------------------
class deleteAttachmentFile(APIView):
    
    # tblArray = { }
    def post(self, request, format=None):
        try:
            if request.data['attached_file']:
                NdAttachments.objects.filter(attached_file=request.data['attached_file']).update(is_deleted=True)
                return Response([{"status" : True, "msg" : "Deleted successfully"}])
            else:
                return Response([{'status': False, 'msg' : 'Something went wrong'}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Please check all field properly", "field": "mainError"})
            return Response(self.errorResult)


# ------------------ Unique phone -----------------------
class checkUniquePhoneNumber(APIView):
    def post(self, request, format=None):
        try:
            is_exists = NdUsers.objects.filter(phone_number=request.data['phone_number'],role=settings.IS_DRIVER,is_deleted=False).count()
           
            if( is_exists>0 ):
                return Response([{"status" : False, "msg" : "Phone Number already exists"}])
            else:
                return Response([{'status': True, 'msg' : 'Not exists'}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Please check all field properly", "field": "mainError"})
            return Response(self.errorResult)

# =============================== Driver cancelled trip ===================
def driver_cancelled_trip_list( request ):
    
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Driver Cancelled Trip"
        data['page_title'] = "Driver Cancelled Trip"
        #---------------------------------All Countries--------------------------#
        allModel = NdVehicleModel.objects.filter(is_status=True, is_deleted= False).order_by('model_name') 
        ndVehiclModelSerializer = NdVehiclModelSerializer(allModel, many=True)
        data['vehicleModels'] = ndVehiclModelSerializer.data

        allVehicleType = NdVehicleType.objects.filter(is_status=True, is_deleted= False).order_by('vehicle_type_name') 
        
        ndVehicleTypeSerializer = NdVehicleTypeSerializer(allVehicleType, many=True)
        data['vehicleTypes'] = ndVehicleTypeSerializer.data

        allCountries = NdCountries.objects.all().order_by('country_name') 
        ndCountriesSerializer = NdCountriesSerializer(allCountries, many=True)
        data['countries'] = ndCountriesSerializer.data

        # allActiveCustomer = NdVehicleType.objects.filter(is_status=True, is_deleted= False,role=settings.IS_DRIVER).count() 
        # data['totalActive'] = allActiveCustomer

        year_dropdown = []
        for y in range((datetime.datetime.now().year - 9), (datetime.datetime.now().year + 1)):
            year_dropdown.append((y))

        allDeactiveData = NdUsers.objects.filter(is_status=False, is_deleted= False,role=settings.IS_DRIVER).count() 
        data['totalDeactive'] = allDeactiveData

        data['WEBADMIN'] = settings.WEBADMIN_URL
        data['year_dropdown'] = year_dropdown

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        # print(urlSegments)
        data['current_url_segments'] = urlSegments
        data['app_name'] = "driver"
        return render( request, './report/driver_cancelled_trip.html', data)
    else:
        return redirect("/")



class driver_cancelled_trip(APIView):
  #------------------------ Get method to get all customer -------------------------------------# 
    tmpSaveData = []
    def get(self, request, format =None):
        searchQ = request.GET["search[value]"]
        fieldSToSort = {
            0 : 'id',
            1 : 'first_name',
            2 : 'last_name'
        }
        sortingColumn = request.GET["order[0][column]"]
        sortingType = request.GET["order[0][dir]"]
        draw = request.GET["draw"]

        
       
        # if draw == "1" :
        #     sortingType = "desc"
        #     sortingColumn = 0
        totalRecords = NdBookingRequests.objects.values('driver','driver__first_name','driver__last_name','driver__phone_number','driver__profile_picture').filter(is_deleted =True, is_booked =False).annotate(reject_count=Count('driver_id')).count()
        totalFiltered = totalRecords
        allRecord = NdBookingRequests.objects.values('driver','driver__first_name','driver__last_name','driver__phone_number','driver__profile_picture').filter(is_deleted =True, is_booked =False).annotate(reject_count=Count('driver_id'))
        if searchQ:
            allRecord = allRecord.filter(Q(driver__first_name__icontains=searchQ) | Q(driver__last_name__icontains=searchQ) | Q(driver__phone_number__icontains=searchQ) )
        
        totalRecords = allRecord.count()
        totalFiltered = totalRecords
        allRecord = allRecord[int(request.GET['start']): (int(request.GET['start']) + int(request.GET['length']))]
        ajaxData = []
        i = 1
        if allRecord.count()>0:
            tmpArray = []

            for item in allRecord:
                tmpRow = []
                featuredMode = ''
                logo = ''
                full_name = ''
                phone_number = "" 
                image = ''

                if item['driver__profile_picture']:
                    image = '<img src="'+ static(item['driver__profile_picture'])+'?time='+ str(datetime.datetime.now())+' " class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
                else:
                    image = '<img src="'+static("images/avatar.jpg")+'" class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'

                if item['driver__first_name']:
                    full_name += item['driver__first_name']
                if item['driver__last_name']:
                    full_name += item['driver__last_name'] 
                if item['driver__phone_number']:
                    phone_number = item['driver__phone_number'] 

                viewMsg =   ' <a href="cancel-trip-details/'+str(item['driver'])+'" class="btn-round-primary"> <i class="fa fa-eye" aria-hidden="true"></i></a> '

               
                tmpRow.append(i)
                tmpRow.append(image)
                tmpRow.append(full_name)
                tmpRow.append(phone_number)
                tmpRow.append(item['reject_count'])
                tmpRow.append(viewMsg)
                
                ajaxData.append(tmpRow)
                i+=1

        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})

#------------------------ Single User Details by ID BY GET -------------------------------------#
class RecordCancelTripDetails(APIView):
    def get(self, request, id, format =None):
      data = {}
      data['title'] = "Driver Cancelled Trip Details"
      data['page_title'] = "Driver Cancelled Trip Details"
      locationWiseParcelArr = []
      recordDetails = NdBookingRequests.objects.filter(driver__id=id,is_deleted =True, is_booked =False).values('date_created','id','order').order_by('-date_created') 
      ndSerializer = NdBookingRequestsSerializer(recordDetails, many=True)

      recordUserDetails = NdUsers.objects.filter(id=id).values('first_name','last_name','phone_number').first()

      tmpRow = []
      for item in ndSerializer.data:
            singleRowData = []
            if item['date_created']:
                cancelDate = parser.parse(item['date_created']).date()
                cancelTime = parser.parse(item['date_created']).time()
                singleRowData.append(cancelDate)
                singleRowData.append(cancelTime)
            # tmpRow.append(item['id'])
            tmpRow.append(singleRowData)
          

      
      data['details_data'] = tmpRow
      data['user_details'] = recordUserDetails
      
      url = request.META['PATH_INFO'].split('/')
      urlSegments = list(filter(None, url)) 
      # print(urlSegments)
      data['current_url_segments'] = urlSegments
      if ndSerializer.data:
          # return Response([{"status" : True, "data" : ndSerializer.data}])
           # return render( request, './report/driver_cancel_trip_details.html',data)
           return render( request, './report/driver_cancelled_trip_details.html', data)
           # return render( request, './lists/driver-details.html', data)
      else:
           return redirect("/")

#------------------------ Vehicle model by vehicle type -------------------------------------#
class getVehicleModelByVehicleType(APIView):
    def get(self, request, id, format =None):
        data = {}
        allModel = NdVehicleModel.objects.filter(is_status=True, is_deleted= False, vehicle_type__id=id).order_by('model_name') 
        ndVehiclModelSerializer = NdVehiclModelSerializer(allModel, many=True)
        
        if ndVehiclModelSerializer.data:
            return Response([{"status" : True, "data" : ndVehiclModelSerializer.data
}])
        # return render( request, './lists/driver-details.html', data)
        else:
            return Response([{"status" : True, "data" : data, "msg":"No data found"}])

