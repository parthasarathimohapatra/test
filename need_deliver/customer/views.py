from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect
from webAdmin.serializers import *
from django.template import RequestContext
from rest_framework.views import APIView

import json
from django.db.models import Value
from django.db.models.functions import Concat

from django.conf import settings
from webAdmin.models import NdUsers

def cust_list( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Customer Management"
        data['page_title'] = "Customer Management"
        #---------------------------------All Countries--------------------------#
        allCountries = NdCountries.objects.order_by('country_name') 
        ndCountriesSerializer = NdCountriesSerializer(allCountries, many=True)
        data['countries'] = ndCountriesSerializer.data

        allActiveCustomer = NdUsers.objects.filter(is_status=True, is_deleted= False,role=settings.IS_CUSTOMER).count() 
        data['totalActive'] = allActiveCustomer

        allDeactiveData = NdUsers.objects.filter(is_status=False, is_deleted= False,role=settings.IS_CUSTOMER).count() 
        data['totalDeactive'] = allDeactiveData

        data['WEBADMIN'] = settings.WEBADMIN_URL

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        # print(urlSegments)
        data['current_url_segments'] = urlSegments
        data['app_name'] = "customer"
        return render( request, 'lists/lists.html', data)
    else:
        return redirect("/")



class customer(APIView):
  #------------------------ Get method to get all customer -------------------------------------# 
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
        if draw == "1" :
            sortingType = "desc"
            sortingColumn = 0
        totalRecords = NdUsers.objects.filter(is_deleted =False, role=settings.IS_CUSTOMER).count()
        totalFiltered = totalRecords
        allRecord = NdUsers.objects.filter(is_deleted =False, role=settings.IS_CUSTOMER)
        if searchQ:
            allRecord = allRecord.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).filter(Q(first_name__icontains=searchQ) | Q(last_name__icontains=searchQ)|\
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
               
               # if item['profile_img']:
               #      logo = '<img src="'+  settings.AWS_S3_BUCKET_URL + settings.AWS_USERS_IMAGES +item['profile_img']+'?time='+ str(datetime.datetime.now())+' " class="big-img-loader rounded-circle z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               # else:
               #      logo = '<img src="'+ settings.BASE_URL + '/static/images/avatar.jpg" class="big-img-loader rounded-circle z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               statusMsg = '<img src="'+ settings.BASE_URL + '/static/images/checked.png?time='+ str(datetime.datetime.now())+' " class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+ settings.BASE_URL + '/static/images/error.png?time='+ str(datetime.datetime.now())+' " class="big-img-loader" >'
               # verified_icon = '<img src="'+ settings.BASE_URL + '/static/images/mobile-verified.png?time='+ str(datetime.datetime.now())+' " class="big-img-loader verification-img" >'
               # if not item['is_phone_validate']:
               #      verified_icon = '<img src="'+ settings.BASE_URL + '/static/images/not_verified.png?time='+ str(datetime.datetime.now())+' " class="big-img-loader verification-img" >'
               action =  '<img data-target="#sendMailModal" data-toggle="modal" src="'+ settings.BASE_URL + '/static/images/send_mail.png" data-id="'+str(item['id'])+'" class="send_mail" data-rcv = "'+item['first_name']+' <'+item['email_id']+'>" title="Send Mail to '+item['first_name']+'" >'
               tmpRow.append(item['id'])
               # tmpRow.append(logo)
               tmpRow.append(item['first_name'] + " "  + item['last_name'])
               tmpRow.append(item['email_id'])
               tmpRow.append(item['phone_number'])

               
               tmpRow.append(statusMsg)
               tmpRow.append(action)
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
           
            if self.errorResult:
                return Response(self.errorResult)
                # return Response({"o":request.data["country_id"]})
            else:
                request.POST._mutable = True
                
                recordDetails = NdUsers.objects.filter(id=pk).first()
                details = NdUsersSerializer(recordDetails)
            # file_name_with_ext = details.data['profile_img']
            # if request.data.get('profile_img'):
            #     image_b64 = request.data.get('profile_img')
            #     format, imgstr = image_b64.split(';base64,')
            #     ext = format.split('/')[-1]
            #     file_name = shaEncode( str(datetime.datetime.now())) 
                
            #     file_name_with_ext = file_name + "."+ ext
            #     connection =boto.connect_s3(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_ACCESS_KEY)
            #     bucket = connection.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
            #     cloudfile = Key(bucket)
            #     path = "/" +settings.AWS_USERS_IMAGES + file_name_with_ext
            #     cloudfile.key = path
            #     if details.data['profile_img']:
            #         bucketDel = Bucket(connection, settings.AWS_STORAGE_BUCKET_NAME)
            #         bucketDel.delete_key("/" +settings.AWS_USERS_IMAGES + details.data['profile_img'])

            #     cloudfile.set_contents_from_string(base64.b64decode(imgstr))
            #     cloudfile.set_metadata('Content-Type', 'image/' + ext) # from https://stackoverflow.com/a/22730676 and https://stackoverflow.com/questions/16156062/using-amazon-s3-boto-library-how-can-i-get-the-url-of-a-saved-key
            #     cloudfile.set_acl('public-read')      
                NdUsers.objects.filter(id=pk).update( first_name=request.data['first_name'], last_name=request.data['last_name'], country= request.data['country'], state= request.data['state'], city= request.data['city'], zipcode= request.data['zipcode'], description= request.data['description'])  

           
                return Response([{"status" : True, "msg" : "You have successfully updated the record"}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Please resize the image before upload", "field": "mainError"})
            return Response(self.errorResult)

    #------------------------ POST method to Insert customer details -------------------------------------# 
    def post(self, request, format=None):
        # try:
            self.errorResult = list()
            # get_unique_email = self.get_unique_email(request.data)
            # get_unique_phone = self.get_unique_phone(request.data)
            if(request.data["first_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "First Name can not be blank", "field": "first_name"})
            if(request.data["last_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Last Name can not be blank", "field": "last_name"})
            # if(get_unique_email['status'] == False):
            #     self.errorResult.append({"status" : False,"msg" : get_unique_email['msg'], "field": "email_id"})
            # if(get_unique_phone['status'] == False):
            #     self.errorResult.append({"status" : False,"msg" : get_unique_phone['msg'], "field": "phone_number"})
            # if(request.data["country"] == "0" ):
            #     self.errorResult.append({"status" : False,"msg" : "Country Name can not be blank", "field": "country"})
            # if(request.data["state"] == "0"):
            #     self.errorResult.append({"status" : False,"msg" : "State Id can not be blank", "field": "state"})
            # if(request.data["city"] == ""):
            #     self.errorResult.append({"status" : False,"msg" : "City Name can not be blank", "field": "city"})
            
            # if(request.data["dob"] == ""):
            #     self.errorResult.append({"status" : False,"msg" : "Date of Birth can not be blank", "field": "dob"})
            # if(request.data["language"] == ""):
            #     self.errorResult.append({"status" : False,"msg" : "Language can not be blank", "field": "language"})
            # if(request.data["password"] == ""):
            #     self.errorResult.append({"status" : False,"msg" : "password can not be blank", "field": "password"})
            # if(request.data["cpassword"] == ""):
            #     self.errorResult.append({"status" : False,"msg" : "Confirm password can not be blank", "field": "cpassword"})
            # if(request.data["cpassword"] != request.data["password"]):
            #     self.errorResult.append({"status" : False,"msg" : "Sorry! Please check confirm password", "field": "cpassword"})
            # if self.errorResult:
            #     return Response(self.errorResult)
                # return Response({"o":request.data["country_id"]})
            else:
                # request.POST._mutable = True
                # encodePass =  encrypt_val(request.data.get('password'));
                # request.POST['password'] = encodePass

                # image_b64 = request.data.get('profile_img')
                # return Response({'i' :})
                # if image_b64 != '':
              
                #     format, imgstr = image_b64.split(';base64,')
                #     ext = format.split('/')[-1]
                #     file_name = shaEncode( str(datetime.datetime.now())) 
                #     file_name_with_ext = file_name + "."+ ext
                #     connection =boto.connect_s3(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_ACCESS_KEY)
                #     bucket = connection.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
                #     cloudfile = Key(bucket)
                #     path = "/" +settings.AWS_USERS_IMAGES + file_name_with_ext
                #     cloudfile.key = path
                #     cloudfile.set_contents_from_string(base64.b64decode(imgstr))
                #     cloudfile.set_metadata('Content-Type', 'image/' + ext) # from https://stackoverflow.com/a/22730676 and https://stackoverflow.com/questions/16156062/using-amazon-s3-boto-library-how-can-i-get-the-url-of-a-saved-key
                #     cloudfile.set_acl('public-read')   
                #     request.POST['profile_img'] = file_name_with_ext  
                
                u = NdUsers(role_id=settings.IS_CUSTOMER)
                # return Response({"s":u})
                # request.data['password'] = encodePass 
                # request.data['dob'] = parse_date(request.data['dob'])
                # request.POST['registration_method'] = 'app_reg'

               
                ndUsersCreateSerializer = NdUsersCreateSerializer(data=request.data)

                # Creating role instace
               
                user_role_id =  settings.IS_CUSTOMER
                role_instance = NdRoles.objects.filter(id=user_role_id).first()

                country_id =  request.data['country']
                country_instance = NdCountries.objects.filter(id=country_id).first()

                state_id =  request.data['state']
                state_instance = NdStates.objects.filter(id=state_id).first()
               
                print("===========================================")
                print(request.data)
                print("===========================================")

                if ndUsersCreateSerializer.is_valid():
                    ndUsersCreateSerializer.save(role=role_instance, country=country_instance, state=state_instance)
                else:
                    # ndUsersCreateSerializer.errors
                    print("===========================================")
                    print(ndUsersCreateSerializer.errors)
                    print("===========================================")
                data = {};
                allActiveCustomer = NdUsers.objects.filter(is_status=True, is_deleted= False,role=settings.IS_CUSTOMER).count() 
                data['totalActiveCustomer'] = allActiveCustomer

                allDeactiveCustomer = NdUsers.objects.filter(is_status=False, is_deleted= False,role=settings.IS_CUSTOMER).count() 
                data['totalDeactiveCustomer'] = allDeactiveCustomer

                # allStudent = NdUsers.objects.filter(is_deleted= False,role=settings.IS_CUSTOMER).count() 
                # data['allTeachers'] = allStudent 
                # ndUsersObjects = NdUsersObjects( user_id= ndUsersCreateSerializer.data['id'])
                # ndUsersObjects.save()
                return Response([{"status" : True, "data" : data, "msg" : "You have successfully created the profile", 'updated_record' : data}])
        # except Exception as e:
        #     self.errorResult.append({"status" : False,"msg" : "Please resize the image before upload", "field": "mainError"})
        #     return Response(self.errorResult)

#------------------------ Single User Details by ID BY GET -------------------------------------#
class RecordDetailsUsers(APIView):
    def get(self, request, id, format =None):
      recordDetails = NdUsers.objects.filter(id=id).first()
      ndStatesSerializer = NdUsersCreateSerializer(recordDetails)
      if ndStatesSerializer.data:
          return Response([{"status" : True, "data" : ndStatesSerializer.data}])
      else:
          return Response([{"status" : False, "msg" : "Sorry! No record is found"}])
#------------------------ Update multiple records BY LIST ID -------------------------------------#
class UpdateMultiRecordUsers(APIView):
    
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

                # allDeactiveCustomer = NdUsers.objects.filter(is_status=False, is_deleted= False,role=request.data['role']).count() 
                # allDeactiveCustomer = allDeactiveCustomer
                # countingInfo.append({'allDeactiveCustomer' : allDeactiveCustomer})

                # allCustomer = NdUsers.objects.filter(is_deleted= False,role=request.data['role']).count() 
                # # allTeacherallTeacher = allCustomer
                # countingInfo.append({'allCustomer' : allCustomer})

            return Response([{"status" : True, "countingInfo" : countingInfo}])
        # elif request.data['action'] == 'send_cred' :
        #     if json.loads(request.data['ids']):
        #         for ID in json.loads(request.data['ids']):
        #             recordDetails = FlntUsers.objects.filter(id=ID).first()
        #             details = FlntUsersCredSerializer(recordDetails)
        #             html_message = loader.render_to_string(
        #                 'email_templates/cred_details.html',
        #                 {
        #                     'users_name': details.data['first_name'],
        #                     'email': details.data['email_id'],
        #                     'password': decrypt_val(details.data['password']) 
        #                 }
        #             )
        #             # res = send_mail("hello paul", "commendt tu vas?", "arijit.chandra@navsoft.in", ['arijit.chandra@navsoft.in'])         
        #             # return Response({'status' : True,'sss': '1'})
        #             try:
        #                 send_mail('Login Credentials', html_message,settings.NO_REPLY_MAIL,[details.data['email_id']],fail_silently=False,html_message=html_message) 
        #                 return Response([{'status': True, 'msg' : 'Login details has been sent to all selected persons'}])
        #             except Exception as e:
        #                 return Response([{'status': False, 'msg' : 'Something went wrong'}])
        #     else:
        #         return Response([{'status': False, 'msg' : 'Please select minimum one teacher'}])
        else:
            return Response([{'status': False, 'msg' : 'Something went wrong1'}])

