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
from webAdmin.models import NdUsers, NdOrder
from django.contrib.staticfiles.templatetags.staticfiles import static
from commonApp.views import fieldEmptyCheck, pushNotificationFCM
from pyfcm import FCMNotification
push_service = FCMNotification(api_key=settings.FCM_API_KEY)

def supplier_list( request ):
    if 'authSession' in request.session:
        data = {}
        data['title'] = "Supplier Management"
        data['page_title'] = "Supplier Management"
        #---------------------------------All Countries--------------------------#
        allCountries = NdCountries.objects.order_by('country_name') 
        ndCountriesSerializer = NdCountriesSerializer(allCountries, many=True)
        data['countries'] = ndCountriesSerializer.data

        allActiveCustomer = NdUsers.objects.filter(is_status=True, is_deleted= False,role=settings.IS_SUPPLIER).count() 
        data['totalActive'] = allActiveCustomer

        allDeactiveData = NdUsers.objects.filter(is_status=False, is_deleted= False,role=settings.IS_SUPPLIER).count() 
        data['totalDeactive'] = allDeactiveData

        today = datetime.datetime.today().strftime('%Y-%m-%d')
        allPromoCode = NdPromotions.objects.filter(is_status=True, is_deleted= False, end_date__gte = today).order_by('promotion_code')
        ndPromotionCodeSerializer = NdPromotionCodeSerializer(allPromoCode, many=True)
        
        data['promotion_codes'] = ndPromotionCodeSerializer.data

        data['WEBADMIN'] = settings.WEBADMIN_URL

        url = request.META['PATH_INFO'].split('/')
        urlSegments = list(filter(None, url)) 
        # print(urlSegments)
        data['current_url_segments'] = urlSegments
        data['app_name'] = "supplier"
        return render( request, 'lists/lists.html', data)
    else:
        return redirect("/")



class supplier(APIView):
  #------------------------ Get method to get all customer -------------------------------------# 
   
    #----- Method to check unique phone number -------#         
    def get_unique_phone(self, request):
        if(request.get('phone_number') == ""):
            return {'status': False, 'msg': "Phone Number can not be blank"}
        if(request.get('id') != ''):
            is_exists = NdUsers.objects.filter(Q(phone_number=request.get('phone_number')), ~Q(id=request.get('id')), Q(is_deleted=False)).count()
        else:
            is_exists = NdUsers.objects.filter(phone_number=request.get('phone_number'),is_deleted=False).count()
        if( is_exists>0 ):
            return {'status': False, 'msg': "Phone Number already exists"}
        else:
            return {'status': True}

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
        # if draw == "1" :
        #     sortingType = "desc"
        #     sortingColumn = 0
        totalRecords = NdUsers.objects.filter(is_deleted =False, role=settings.IS_SUPPLIER).count()
        totalFiltered = totalRecords
        allRecord = NdUsers.objects.filter(is_deleted =False, role=settings.IS_SUPPLIER).order_by(fieldSToSort[int(sortingColumn)])


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
               image = ''
               if item['profile_picture']:
                    image = '<img src="'+ item['profile_picture']+'?time='+ str(datetime.datetime.now())+' " class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               else:
                    image = '<img src="'+ static('images/avatar.jpg')+'" class="big-img-loader z-depth-1-half avatar-pic thumb-logo big-img-loader" >'
               

               recordDetails = NdAppliedCoupons.objects.filter(supplier=item['id']).first()
               couponDetails = NdAppliedCouponSerializer(recordDetails)
              

               promoCode = '<a href="#"" class="promoPopLink" data-action="promo_assign_view" data-id="'+str(item['id'])+'" style="color:#cc5200;"> Assign Promo</a>'
               if couponDetails.data['coupon']:
                if couponDetails.data['coupon']['promotion_code']:
                    promoCode = '<span style="color:#006600">'+couponDetails.data['coupon']['promotion_code']+'</span><a href="#"" class="promoPopLink" data-action="promo_assign_view" data-id="'+str(item['id'])+'"  style="color:#24248f"> Change </a>'
              
               statusMsg = '<img src="'+static('images/checked.png')+'" class="big-img-loader" >'
               if not item['is_status']:
                    statusMsg = '<img src="'+static('images/error.png')+'" class="big-img-loader" >'


                   

               # verified_icon = '<img src="'+ settings.BASE_URL + '/static/images/mobile-verified.png?time='+ str(datetime.datetime.now())+' " class="big-img-loader verification-img" >'
               # if not item['is_phone_validate']:
               #      verified_icon = '<img src="'+ settings.BASE_URL + '/static/images/not_verified.png?time='+ str(datetime.datetime.now())+' " class="big-img-loader verification-img" >'
               # action =  '<img data-target="#sendMailModal" data-toggle="modal" src="'+ settings.BASE_URL + '/static/images/send_mail.png" data-id="'+str(item['id'])+'" class="send_mail" data-rcv = "'+item['first_name']+' <'+item['email_id']+'>" title="Send Mail to '+item['first_name']+'" >'
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

               tmpRow.append(image) 
               tmpRow.append(firstName+" "+lastName)
               tmpRow.append(email_id)
               tmpRow.append(phone_number)

               tmpRow.append(promoCode)
               tmpRow.append(statusMsg)
               # tmpRow.append(action)
               ajaxData.append(tmpRow)
               i+=1
       
        return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        # return Response({"data": ajaxData, 'recordsTotal' : totalRecords, 'recordsFiltered' : totalFiltered})
        #------------------------ Put method to update customer details By ID -------------------------------------#     
    def put(self, request, pk, format=None):
        # try:

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
                NdUsers.objects.filter(id=pk).update( first_name=request.data['first_name'], last_name=request.data['last_name'])  

           
                return Response([{"status" : True, "msg" : "You have successfully updated the record"}])
        # except Exception as e:
        #     self.errorResult.append({"status" : False,"msg" : "Please check! There is some error", "field": "mainError"})
        #     return Response(self.errorResult)

    #------------------------ POST method to Insert customer details -------------------------------------# 
    def post(self, request, format=None):
        try:
            self.errorResult = list()
            # get_unique_email = self.get_unique_email(request.data)
            # get_unique_phone = self.get_unique_phone(request.data)
            if(request.data["first_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "First Name can not be blank", "field": "first_name"})
            if(request.data["last_name"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Last Name can not be blank", "field": "last_name"})
            
            else:
                
                ndUsersCreateSerializer = NdUsersCreateSerializer(data=request.data)

                # Creating role instace
               
                user_role_id =  settings.IS_SUPPLIER
                role_instance = NdRoles.objects.filter(id=user_role_id).first()

                country_id =  request.data['country']
                country_instance = NdCountries.objects.filter(id=country_id).first()

                state_id =  request.data['state']
                state_instance = NdStates.objects.filter(id=state_id).first()
               
                if ndUsersCreateSerializer.is_valid():
                    ndUsersCreateSerializer.save(role=role_instance, country=country_instance, state=state_instance)
                else:
                    # ndUsersCreateSerializer.errors
                    print("===========================================")
                    print(ndUsersCreateSerializer.errors)
                    print("===========================================")
               
                return Response([{"status" : True,  "msg" : "You have successfully created the profile", 'updated_record' : data}])
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Sorry! Data not uploaded", "field": "mainError"})
            return Response(self.errorResult)

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
    def sendPushToOlderLoggedInUser(self, request, customParam, dataFields):
        userIDS = dataFields['userIDS']
        if dataFields['deviceIDS']:
            deviceIDS = dataFields['deviceIDS']
            pushNotificationFCM.send_push_notification( deviceIDS, userIDS, 
            {"title": dataFields['title'], "body": dataFields['body'], "notification_type_id" : 4}, customParam)
        return True
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
           
            
            if value == False:
                deviceTokenArr = []
                userIDSArr = []
                if id_list:
                    for item in id_list:
                        userDetailsIns = NdUsers.objects.filter(Q(id=int(item))).values('device_token', 'id')
                        if userDetailsIns.exists():
                            userDetailsObj = userDetailsIns.first()
                            bookingStatus = NdOrder.objects.filter(Q(booking_status=settings.BOOKING_STATUS_PLACED), Q(supplier_id=int(item)))
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
                        print("dfsfsdfsdfsdf", str(userDetailsIns.count()))
                        if userDetailsIns.exists():
                            userDetailsObj = userDetailsIns.first()
                            bookingStatus = NdOrder.objects.filter(Q(booking_status=settings.BOOKING_STATUS_PLACED), Q(supplier_id=int(item)))
                            print(userDetailsObj['device_token'])
                            if fieldEmptyCheck(userDetailsObj['device_token']) :
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
                    if deviceIDS:
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
                

class assignPromoCode(APIView):
    def get(self, request, id, format =None):
        recordDetails = NdAppliedCoupons.objects.filter(supplier=id).first()
        ndAppliedCouponSerializer = NdAppliedCouponSerializer(recordDetails)

        userDetails = NdUsers.objects.filter(id=id).first()
        ndUsersSerializer = NdUsersSerializer(userDetails)
        if ndUsersSerializer.data:
            return Response([{"status" : True, "data" : ndAppliedCouponSerializer.data,"user":ndUsersSerializer.data}])
        else:
            return Response([{"status" : False, "msg" : "Sorry! No record is found"}])
    
    #------------ POST method to Insert and update details --------------------# 
    def post(self, request, format=None):
        try:
            self.errorResult = list()
            if(request.data["coupon"] == ""):
                self.errorResult.append({"status" : False,"msg" : "Coupon can not be blank", "field": "coupon"})
            
            if self.errorResult:
                return Response(self.errorResult)

            else:
               
                supplier_id = request.data['sup_id']
                promotion_code_id = request.data['coupon']
                supplierOfCoupon = NdAppliedCoupons.objects.filter(supplier=supplier_id).count() 

                supplier_instance = NdUsers.objects.filter(id=supplier_id).first()
                coupon_instance = NdPromotions.objects.filter(id=promotion_code_id).first()
                app = NdPromotionCodeSerializer(coupon_instance)
                # countOfCoupon = NdAppliedCoupons.objects.filter(supplier=supplier_instance).count
                recordDetails = NdAppliedCoupons.objects.filter(supplier=supplier_id).first()
                couponDetails = NdAppliedCouponSerializer(recordDetails)
                # Creating role instace
                
                if supplierOfCoupon > 0 :
                    applied_coupon_id = couponDetails.data['id']
                    NdAppliedCoupons.objects.filter(id=applied_coupon_id).update( coupon=coupon_instance)  

                else:
                    ndAppliedCouponSerializer = NdAppliedCouponSerializer(data=request.data)
                    if ndAppliedCouponSerializer.is_valid():
                        ndAppliedCouponSerializer.save(coupon=coupon_instance, supplier=supplier_instance)
                        
                    else:
                        # ndUsersCreateSerializer.errors
                        print("=======================Error====================")
                        print(ndAppliedCouponSerializer.errors)
                        print("===========================================")
            return Response([{"status" : True, "msg" : "You have successfully updated the record"}])  
                
        except Exception as e:
            self.errorResult.append({"status" : False,"msg" : "Sorry! Data not uploaded", "field": "mainError"})
            return Response(self.errorResult)
class AssignPromoCodeToMultiSuppliers(APIView):
    errorResult = []
    def post(self, request):
        # try:
        self.errorResult = list()
        if(request.data["coupon"] == ""):
            self.errorResult.append({"status" : False,"msg" : "Coupon can not be blank", "field": "coupon"})
        
        if self.errorResult:
            return Response(self.errorResult)

        else:
           
            promotion_code_id = request.data['coupon']
            id_list = json.loads(request.data['ids'])
            updatedSupplier = [] 
            insertSupplier = [] 
            if id_list:
                for item in id_list:
                    supplierOfCoupon = NdAppliedCoupons.objects.filter(supplier_id=int(item)).count() 
                    if supplierOfCoupon>0:
                        updatedSupplier.append(item)
                    else:
                        insertSupplier.append(item)
            print("ufudufgdfg", str(id_list))            
            print("&&&&&&&&&&&&&&&&&&&&&&&",str(updatedSupplier))
            print("dfgdfdfgdfg",str(insertSupplier))
            
            if updatedSupplier :
                NdAppliedCoupons.objects.filter(supplier_id__in=id_list).update(coupon_id=int(promotion_code_id))  
            # return Response([{"status" : True, "msg" : id_list}])    
            if insertSupplier:
                tmpSaveData = list()
                for item2 in insertSupplier:
                    ndAppliedCouponsObj = NdAppliedCoupons(coupon_id=int(promotion_code_id), supplier_id=int(item2))
                    tmpSaveData.append(ndAppliedCouponsObj)
                NdAppliedCoupons.objects.bulk_create(tmpSaveData)

            return Response([{"status" : True, "msg" : "You have successfully updated the record"}])  
        # except Exception as e:
        #     self.errorResult.append({"status" : False,"msg" : "Sorry! Data not uploaded", "field": "mainError"})
        #     return Response(self.errorResult)
