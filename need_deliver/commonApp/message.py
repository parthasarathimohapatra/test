class GenericMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"error-msg" : "Something went wrong",
				"data-save-success" : "Data has been successfully saved",
				"session_out"   : "Sorry!! your session has been expired",
				"device_type": "Device type is missing",
				"data-fetched" : "Data fetched",
				"data-not-found" : "No record found",
			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"error-msg" : "ប្រព័ន្ធនៅមានបញ្ហា",
				"data-save-success" : "ទិន្នន័យត្រូវបានរក្សាទុកដោយជោគជ័យ",
				"session_out"   : "សូមអភ័យទោស ការប្រើប្រាស់អស់សពុលភាព សូមព្យាយាមម្តងទៀត",
				"device_type": "សូមបំពេញប្រភេទនៃទូរស័ព្ទរបស់លោកអ្នក",
				"data-fetched" : "ទិន្នន័យត្រូវបានបញ្ចូល",
				"data-not-found" : "គ្មានព័ត៌មាននេះទេ",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"error-msg" : "Something went wrong",
				"data-save-success" : "Data has been successfully saved",
				"session_out"   : "Sorry!! your session has been expired",
				"device_type": "Device type is missing",
				"data-fetched" : "Data fetched",
				"data-not-found" : "No record found",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False

class LoginMsgMod():
	def Msg( lang, key ):
		    #------------------------------------------------ English ----------------------------------------#
		List = {
			'en' : {
					"verification_code" : "Verification code can not be blank",
					"login-success-msg" : "You have successfully logged into your profile",
					"phone_no_not_verified" : "Sorry!! Your given phone number is not yet verified",
					"device_token" : "Device token is missing",
					"not_match" : "Invalid OTP",
					"ac_deactivate" : "Your profile has been deactivated",
					"ac_not_exists" : "Your profile does not exists",
					"role_id"  : "Role is missing",
					"login_otp_generate"  : "Login OTP has been sent",
					"first_name" : "First name can not be blank",
					"last_name" : "Last name can not be blank",
					"phone_number" : "Phone no can not be blank",
					"basic-info-save-msg" : "Basic info has been saved",
					"phone_number_already_reg" : "Sorry!! Phone no has already been registared",
					"email_id" : "Email ID can not be blank",
					"email_already_reg" : "Sorry!! Email ID has already been registared",
					"confirm_not_match":"Confirm Password doesn't match",

			},
			#------------------------------------------------ Cambodia ----------------------------------------#
			'km-KH' : {
					"verification_code" : "សូមបំពេញលេខកូដនេះម្តងទៀត",
					"login-success-msg" : "អ្នកអាចចូលកម្មវិធីបានដោយជោគជ័យ",
					"phone_no_not_verified" : "សុំអភ័យទោស លេខទូរស័ព្ទលោកអ្នកមិនទានបានផ្ទៀងផ្ទាត់នៅទ្បើយទេ",
					"device_token" : "នៅមានបញ្ហា",
					"not_match" : "លេខកូដ៤ខ្ទង់អស់សុពលភាព",
					"ac_deactivate" : "គណនីរបស់លោកអ្នកត្រូវបានផ្អាកដំណើរការ",
					"role_id"  : "Role is missing",
					"login_otp_generate"  : "លេខកូដត្រូវបានផ្ញើទៅ",
					"first_name" : "ចូរបំពេញឈ្មោះ",
					"last_name" : "ចូរបំពេញនាមត្រកូល",
					"phone_number" : "ចូរបំពេញលេខទូរស័ព្ទរបស់អ្នក",
					"basic-info-save-msg" : "ព័ត៌មានបឋមត្រូវបានរក្សាទុកដោយជោគជ័យ",
					"phone_number_already_reg" : "សូមអភ័យទោស លេខទូរស័ព្ទលោកអ្នកត្រូវបានប្រើប្រាស់រួចម្តងហើយ",
					"email_id" : "ចូរបំពេញសារអេទ្បិចត្រូនិករបស់លោកអ្នក",
					"email_already_reg" : "សូមអភ័យទោស អ៊ីម៉ែលនេះធ្លាប់បានប្រើប្រាស់រួចហើយ",
					"confirm_not_match":"Confirm Password doesn't match",
					"ac_not_exists" : "Your profile does not exists",

			},
			#------------------------------------------------ Simplified Chinese  ----------------------------------------#
			'zh-Hans' : {
				"verification_code" : "Verification code can not be blank",
				"login-success-msg" : "You have successfully logged into your profile",
				"phone_no_not_verified" : "Sorry!! Your given phone number is not yet verified",
				"device_token" : "Device token is missing",
				"not_match" : "Invalid OTP",
				"ac_deactivate" : "Your profile has been deactivated",
				"role_id"  : "Role is missing",
				"login_otp_generate"  : "Login OTP has been sent",
				"first_name" : "First name can not be blank",
				"last_name" : "Last name can not be blank",
				"phone_number" : "Phone no can not be blank",
				"basic-info-save-msg" : "Basic info has been saved",
				"phone_number_already_reg" : "Sorry!! Phone no has already been registared",
				"email_id" : "Email ID can not be blank",
				"email_already_reg" : "Sorry!! Email ID has already been registared",
				"confirm_not_match":"Confirm Password doesn't match",
				"ac_not_exists" : "Your profile does not exists",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False

class UpdateProfilePictureMsgMod():
	def Msg( lang, key ):
		    #------------------------------------------------ English ----------------------------------------#
		List = {
			'en' : {
				"profile_picture" : "Please select any picture",
				"success-msg"   : "Profile picture has been updated successfully",
				
			},
			#------------------------------------------------ English ----------------------------------------#
			'km-KH' : {
				"profile_picture" : "សូមជ្រើសរើសរូបភាព",
				"success-msg"   : "រូបថតរបស់លោកអ្នកត្រូវបានប្តូរដោយជោគជ័យ",
			},
			#------------------------------------------------ Simplified Chinese  ----------------------------------------#
			'zh-Hans' : {
				"profile_picture" : "Please select any picture",
				"success-msg"   : "Profile picture has been updated successfully",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class SaveLocationsMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"location_name" : "Location name can not be blank",
				"location" : "Address can not be blank",
				"latitude"   : "Latitude is missing",
				"longitude"   : "Longitude is missing",
				"user_id"   : "User ID is missing",
				"success-msg"   : "New location has been saved",
				"same_location_name" : "Given location is already saved",
				"record-found" : "Records are fetched",
				"not-found" : "No record found",
				"update-success-msg" : "Location updated",
				"delete-success-msg" : "Location has been deleted",
			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"location_name" : "សូមបំពេញឈ្មោះទីតាំង",
				"location" : "សូមបំពេញទីតាំងអាស័យដ្ឋាន",
				"latitude"   : "សូមបំពេញរយៈទទឹងនៃទីតាំង",
				"longitude"   : "សូមបំពេញរយៈបណ្តោយនៃទីតាំង",
				"user_id"   : "សូមបំពេញឈ្មោះរបស់លោកអ្នក",
				"success-msg"   : "ទីតាំងថ្មីត្រូវបានរក្សាទុក",
				"same_location_name" : "ទីតាំងដែលលោកអ្នកផ្លល់អោយត្រូវបានរក្សាទុក",
				"record-found" : "ព័ត៌មានត្រូវបានបញ្ចូល",
				"not-found" : "គ្មានព័ត៌មាននេះទេ",
				"update-success-msg" : "បច្ចុប្បន្នភាពទីតាំង",
				"delete-success-msg" : "ទីតាំងត្រូវបានលុបចេញ",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"location_name" : "Location name can not be blank",
				"location" : "Address can not be blank",
				"latitude"   : "Latitude is missing",
				"longitude"   : "Longitude is missing",
				"user_id"   : "User ID is missing",
				"success-msg"   : "New location has been saved",
				"same_location_name" : "Given location is already saved",
				"record-found" : "Records are fetched",
				"not-found" : "No record found",
				"update-success-msg" : "Location updated",
				"delete-success-msg" : "Location has been deleted",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class OrderDetailsMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"not-found" : "No record found",
				"found" : "Records fetched",
			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"not-found" : "គ្មានព័ត៌មាននេះទេ",
				"found" : "ព័ត៌មានត្រូវបានបញ្ចូល",
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
class ChangePhoneNumberMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"phone_number" : "No record found",
				"country_id" : "Records fetched",
				"isd_code":"ISD Code is missing",
				"role_id":"Role ID is missing",
				"not_found":"Record not found",
				"otp_send": "Login OTP has been sent",
				"phone_number_already_reg": "Sorry!! Phone no has already been registered",
			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"phone_number" : "គ្មានព័ត៌មាននេះទេ",
				"country_id" : "ព័ត៌មានត្រូវបានបញ្ចូល",
				"isd_code":"ISD Code is missing",
				"role_id":"Role ID is missing",
				"not_found":"គ្មានព័ត៌មាននេះទេ",
				"otp_send": "លេខកូដ៤ខ្ទង់ត្រូវបានបញ្ជូន",
				"phone_number_already_reg": "សូមអភ័យទោស អ៊ីម៉ែលនេះធ្លាប់បានប្រើប្រាស់រួចហើយ",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"phone_number" : "No record found",
				"country_id" : "Records fetched",
				"isd_code":"ISD Code is missing",
				"role_id":"Role ID is missing",
				"not_found":"Record not found",
				"otp_send": "Login OTP has been sent",
				"phone_number_already_reg": "Sorry!! Phone no has already been registered",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
