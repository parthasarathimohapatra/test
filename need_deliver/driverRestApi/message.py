from commonApp.message import GenericMsgMod
from commonApp.message import LoginMsgMod
class DriverRegistrationMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"first_name" : "First name can not be blank",
				"last_name" : "Last name can not be blank",
				"isd_code" : "ISD code can not be blank",
				"country_id" : "Country ID is missing", 
				"phone_number" : "Phone number can not be blank",
				"phone_number_already_reg": "Sorry!! Phone no has already been registered",
				"email_id" : "Email ID can not be blank",
				"email_already_reg" : "Sorry!! Email ID has already been registered",
				"gender" : "Gender must be selected",
				"dob" : "Date of birth must be selected",
				"state_id" : "State name must be selected",
				"zipcode" : "Postal code can not be blank",
				"password" : "Password can not be blank",
				"confirm_password" : "Confirm Password can not be blank",
				"wrong_confirm_password" : "Please check your confirm password",
				"success-msg" : "Your account has been successfully created",
			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"first_name" : "ចូរបំពេញឈ្មោះ",
				"last_name" : "ចូរបំពេញនាមត្រកូល",
				"isd_code" : "ISD code can not be blank",
				"country_id" : "Country ID is missing", 
				"phone_number" : "ចូរបំពេញលេខទូរស័ព្ទរបស់អ្នក",
				"phone_number_already_reg": "សូមអភ័យទោស លេខទូរស័ព្ទលោកអ្នកត្រូវបានប្រើប្រាស់រួចម្តងហើយ",
				"email_id" : "ចូរបំពេញអ៊ីម៉ែលរបស់លោកអ្នក",
				"email_already_reg" : "សូមអភ័យទោស អ៊ីម៉ែលនេះធ្លាប់បានប្រើប្រាស់រួចហើយ",
				"gender" : "សូមជ្រើសរើសភេទ",
				"dob" : "សូមជ្រើសរើសថ្ងៃខែឆ្នាំកំណើតរបស់លោកអ្នក",
				"state_id" : "សូមជ្រើសរើសឈ្មោះរដ្ឋ",
				"zipcode" : "សូមបំពេញលេខកូដតំបន់",
				"password" : "សូមបំពេញលេខសម្ងាត់របស់លោកអ្នក",
				"confirm_password" : "សូមបញ្ជាក់លេខសម្ងាត់ម្តងទៀត",
				"wrong_confirm_password" : "សូមពិនិត្យលេខសម្ងាត់របស់លោកអ្នក",
				"success-msg" : "គណនីរបស់លោកអ្នកត្រូវបានបង្កើតដោយជោគជ័យ",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"first_name" : "First name can not be blank",
				"last_name" : "Last name can not be blank",
				"isd_code" : "ISD code can not be blank",
				"country_id" : "Country ID is missing", 
				"phone_number" : "Phone number can not be blank",
				"phone_number_already_reg": "Sorry!! Phone no has already been registered",
				"email_id" : "Email ID can not be blank",
				"email_already_reg" : "Sorry!! Email ID has already been registered",
				"gender" : "Gender must be selected",
				"dob" : "Date of birth must be selected",
				"state_id" : "State name must be selected",
				"zipcode" : "Postal code can not be blank",
				"password" : "Password can not be blank",
				"confirm_password" : "Confirm Password can not be blank",
				"wrong_confirm_password" : "Please check your confirm password",
				"success-msg" : "Your account has been successfully created",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class DriverAndVehicleDocumentsMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"driver_id" : "Driver ID is missing",
				"already_added" : "Driver details are already added",
				"success-msg" : "All documents and details are saved",
			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"driver_id" : "សូមបំពេញអត្តលេខ(អ្នកបើកបរ)",
				"already_added" : "ព័ត៌មានលម្អិតរបស់អ្នកបើកបរត្រូវបានបញ្ចូលក្នុងប្រព័ន្ធ",
				"success-msg" : "រាល់ឯកសារ និងព័ត៌មានលម្អិតនានាត្រូវបានរក្សាទុក",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"driver_id" : "Driver ID is missing",
				"already_added" : "Driver details are already added",
				"success-msg" : "All documents and details are saved",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class DriverLoginMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"password" : "Password can not be blank",
				"deactivated" : "Your account has been deactivated by Admin",
				"deleted":"Your account does not exist",
				"phone_number" : "Phone no can not be blank",
				"phone_no_not_verified" : "Your phone no is not yet verified",
				"wrong_credential" : "Please check your given credential",
				"success-msg" : "You are successfully logged into our system",
			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"password" : "សូមបំពេញលេខសម្ងាត់របស់លោកអ្នក",
				"phone_number" : "សូមបំពេញលេខទូរស័ព្ទរបស់លោកអ្នក",
				"phone_no_not_verified" : "លេខទូរស័ព្ទរបស់លោកអ្នកមិនទាន់បានត្រួតពិនិត្យទេ",
				"wrong_credential" : "សូមត្រួតពិនិត្យព័ត៌មានដែលបានផ្តល់ឲ្យលោកអ្នក",
				"success-msg" : "អបអរសាទរ លោកអ្នកអាចធ្វើប្រតិបត្តិការក្នុងប្រព័ន្ធយើងខ្ញុំបាន",
				"deactivated" : "គណនីរបស់លោកអ្នកត្រូវបានផ្អាកដំណើរការ​ដោយក្រុមហ៊ុន",
				"deleted":"មិនមែនគណនីនេះទេ",

			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"password" : "Password can not be blank",
				"phone_number" : "Phone no can not be blank",
				"phone_no_not_verified" : "Your phone no is not yet verified",
				"wrong_credential" : "Please check your given credential",
				"success-msg" : "You are successfully logged into our system",
				"deactivated" : "Your account has been deactivated by Admin",
				"deleted":"Your account does not exist",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class AllVehicleModelsMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"not-found" : "No record found",
				"found" : "Records fetched",
			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"not-found" : "គ្មានព័ត៌មានដែលលោកអ្នកកំពុងស្វែងរកទេ",
				"found" : "ទិន្នន័យត្រូវបានបញ្ចូល",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"not-found" : "No record found",
				"found" : "Records fetched",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class ForgotPasswordMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"OTP-send" : "OTP has been send to your phone no.",
				"not-found" : "No record found",
				"OTP-match" : "OTP Verification is confirmed",
				"OTP-not-match" : "OTP invalid",
				"password": "Password can not be blank",
				"confirm_password": "Confirm Password can not be blank",
				"confirm_not_match":"Confirm Password doesn't match",
				"password-changed" : "Password has been successfully changed",
				"account_deactivated":"Your account has been deactivated by Admin",
 			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"OTP-send" : "លេខកូដ៤ខ្ទង់ត្រូវបានបញ្ជូនទៅលេខទូរស័ព្ទរបស់លោកអ្នក",
				"not-found" : "គ្មានព័ត៌មានដែលលោកអ្នកកំពុងស្វែងរកទេ",
				"OTP-match" : "សូមធ្វើការបញ្ជាក់លេខកូដ៤ខ្ទង់របស់លោកអ្នក",
				"OTP-not-match" : "លេខកូដ៤ខ្ទង់នេះអស់សពុលភាព",
				"password": "សូមបំពេញលេខសម្ងាត់របស់លោកអ្នក",
				"confirm_password": "សូមបញ្ជាក់លេខសម្ងាត់ម្តងទៀត",
				"confirm_not_match":"លេខសម្ងាត់មិនដូចគ្នាទេ",
				"password-changed" : "លេខសម្ងាត់ត្រូវបានប្តូរដោយជោគជ័យ",
				"account_deactivated":"គណនីរបស់លោកអ្នកត្រូវបានផ្អាកដំណើរការ​ដោយក្រុមហ៊ុន",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"OTP-send" : "OTP has been send to your phone no.",
				"not-found" : "No record found",
				"OTP-match" : "OTP Verification is confirmed",
				"OTP-not-match" : "OTP invalid",
				"password": "Password can not be blank",
				"confirm_password": "Confirm Password can not be blank",
				"confirm_not_match":"Confirm Password doesn't match",
				"password-changed" : "Password has been successfully changed",
				"account_deactivated":"You account has been deactivated",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class DeliveryAcknowledgementMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"driver_id" : "Driver ID is missing",
				"location_type" : "Dropping location type is missing",
				"latitude" : "Droping latitude can not be blank",
				"longitude" : "Droping longitude can not be blank",
				"order_id": "Order ID is missing",
				"already_arrived":"You have already arrived",
				"dropped_at_first_location":"Parcel was delivered to the first drop off location",
				"dropped_at_second_location":"Parcel was delivered to the second drop off location",
				"trip_completed": "Your trip has been completed.",
				"arrived_pickup_location": "Driver is arrived at pick up location",
				"already_cancelled": "Your trip was already cancelled.",
				"already_completed": "Your trip was already completed.",
 			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"driver_id" : "ចូរបំពេញអត្តលេខរបស់លោកអ្នក (អ្នកបើកបរ)",
				"location_type" : "ចូរកំណត់ទីតាំងរបស់លោកអ្នក",
				"latitude" : "ចូរបំពេញរយៈទទឹង",
				"longitude" : "ចូរបំពេញរយៈបណ្តោយ",
				"order_id": "សូមបំពេញអត្តលេខនៃការបញ្ជាដឹក",
				"already_arrived":"លោកអ្នកបានមកដល់គោលដៅហើយ",
				"dropped_at_first_location":"ទំនិញត្រូវបានដឹកជញ្ជូនដល់ទីតាំងទីមួយហើយ",
				"dropped_at_second_location":"ទំនិញត្រូវបានដឹកជញ្ជូនដល់ទីតាំងទីពីរហើយ",
				"trip_completed": "ការដឹកជញ្ជូនរបស់លោកអ្នកត្រូវបានបញ្ចប់ដោយជោគជ័យ",
				"arrived_pickup_location": "អ្នកបើកបរ បានទៅដល់ទីតាំងទទួលទំនិញហើយ",
				"already_cancelled": "ការបញ្ជាដឹកនេះ ត្រូវបានលុបចោលវិញ",
				"already_completed": "ការដឹកជញ្ជូនរបស់លោកអ្នកត្រូវបានបញ្ចប់ដោយជោគជ័យ",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"driver_id" : "Driver ID is missing",
				"location_type" : "Dropping location type is missing",
				"latitude" : "Droping latitude can not be blank",
				"longitude" : "Droping longitude can not be blank",
				"order_id": "Order ID is missing",
				"already_arrived":"You have already arrived",
				"dropped_at_first_location":"Parcel was delivered to the first drop off location",
				"dropped_at_second_location":"Parcel was delivered to the second drop off location",
				"trip_completed": "Your trip has been completed.",
				"arrived_pickup_location": "Driver is arrived at pick up location",
				"already_cancelled": "Your trip was already cancelled.",
				"already_completed": "Your trip was already completed.",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class BookingRequestsByDriverMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"fetched" : "Booking list is generated",
				"no_booking" : "No booking is available",
				"driver_id": "Driver ID is missing",
				"order_id" : "Order ID is missing",
 			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"fetched" : "កំពុងទាញយកព័ត៌មាននៃការកក់ទុក",
				"no_booking" : "គ្មានព័ត៌មាននៃការកក់ទុកទ្បើយ",
				"driver_id": "ចូរបំពេញអត្តលេខរបស់លោកអ្នក (អ្នកបើកបរ)",
				"order_id" : "សូមបំពេញអត្តលេខនៃការបញ្ជាដឹក",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"fetched" : "Booking list is generated",
				"no_booking" : "No booking is available",
				"driver_id": "Driver ID is missing",
				"order_id" : "Order ID is missing",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class CancelBookingByDriverMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"driver_id": "Driver ID is missing",
				"order_id" : "Order ID is missing",
				"success-msg" : "Your trip has been completed.",
				"cancel-success" : "Your trip has been cancelled successfully",
				"already-deleted" : "Your booking is already cancelled",
 			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"driver_id": "សូមបំពេញអត្តលេខ(អ្នកបើកបរ)",
				"order_id" : "សូមបំពេញអត្តលេខនៃការបញ្ជាដឹក",
				"success-msg" : "ការដឹកជញ្ជូនរបស់លោកអ្នកត្រូវបានបញ្ចប់ដោយជោគជ័យ",
				"cancel-success" : "ការបញ្ជាដឹកនេះ ត្រូវបានលុបចោលវិញដោយជោគជ័យ",
				"already-deleted" : "ការកក់ទុកសម្រាប់ការដឹកទំនិញនេះ ត្រូវបានលុបចោលវិញ",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"driver_id": "Driver ID is missing",
				"order_id" : "Order ID is missing",
				"success-msg" : "Your trip has been completed.",
				"cancel-success" : "Your trip has been cancelled successfully",
				"already-deleted" : "Your booking is already cancelled",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class CalculateCostingAtAnyTimeMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"base_price": "Base fare is not set by Admin",
 			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"base_price": "មិនទាន់មានតម្លៃ",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"base_price": "Base fare is not set by Admin",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class DriverLocationSaveToDBMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"order_id": "Order ID is missing",
				"driver_id": "Driver ID is missing",
				"latlong": "Location Object is missing",
				"current_locations_saved" : "Driver Bulk location data saved",
				"no_new_data":"No new data is Available to save",
				"real_distance": "Distance is not given",
 			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"order_id": "សូមបំពេញអត្តលេខនៃការបញ្ជាដឹក",
				"driver_id": "សូមបំពេញអត្តលេខ(អ្នកបើកបរ)",
				"latlong": "សូមបញ្ជាក់ទីតាំង",
				"current_locations_saved" : "ទីតាំងរបស់អ្នកបើកបរត្រូវបានរក្សាទុក",
				"no_new_data":"ទិន្នន័យថ្មីនេះ អាចរក្សាទុកបាន",
				"real_distance": "សូមបំពេញរយៈចម្ងាយ",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"order_id": "Order ID is missing",
				"driver_id": "Driver ID is missing",
				"latlong": "Location Object is missing",
				"current_locations_saved" : "Driver Bulk location data saved",
				"no_new_data":"No new data is Available to save",
				"real_distance": "Distance is not given",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class CurrentBookingDetailsMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"order_id": "Order ID is missing",
				"driver_id": "Driver ID is missing",
				"not_current_booking": "No booking is available"
 			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"order_id": "សូមបំពេញអត្តលេខនៃការបញ្ជាដឹក",
				"driver_id": "ចូរបំពេញអត្តលេខរបស់លោកអ្នក (អ្នកបើកបរ)",
				"not_current_booking": "គ្មានព័ត៌មាននៃការកក់ទុកទ្បើយ"
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"order_id": "Order ID is missing",
				"driver_id": "Driver ID is missing",
				"not_current_booking": "No booking is available"
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
			return False
class CheckOrderStatusBeforeAcceptMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"order_id": "Order ID is missing",
				"driver_id": "Driver ID is missing",
				"not_current_booking": "No booking is available",
				"booking_expired": "Your booking has already expired",
 			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"order_id": "សូមបំពេញអត្តលេខនៃការបញ្ជាដឹក",
				"driver_id": "សូមបំពេញអត្តលេខ(អ្នកបើកបរ)",
				"not_current_booking": "គ្មានព័ត៌មាននៃការកក់ទុកទ្បើយ",
				"booking_expired": "Your booking has already expired",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"order_id": "Order ID is missing",
				"driver_id": "Driver ID is missing",
				"not_current_booking": "No booking is available",
				"booking_expired": "Your booking has already expired",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
