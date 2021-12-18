class Users():
	
	def addMsg(lang, key):
		#------------------------------------------------English----------------------------------------#
		addMsgList = {
			'en' : {
					"first_name": "First Name can not be blank" ,
					"last_name" : "Last Name can not be blank",
					"email_id" : "Email Id can not be blank",
					"email_id_exists" : "Email Id already exists",
					"phone_number" : "Phone Number can not be blank",
					"phone_number_exists" : "Phone Number already exists",
					"role" : "Role can not be blank",
					"language" : "Language can not be blank",
					"registration_method" : "Something went wrong",
					"password" : "Password can not be blank",
					"cpassword" : "Confirm password can not be blank",
					"cpassword_not_match" : "Confirm Password does not match",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully created your profile"

			},
			'es' : {
					"first_name": "First Name can not be blank1" ,
					"last_name" : "Last Name can not be blank1",
					"email_id" : "Email Id can not be blank",
					"email_id_exists" : "Email Id already exists",
					"role" : "Role can not be blank",
					"language" : "Language can not be blank",
					"registration_method" : "Something went wrong",
					"password" : "Password can not be blank",
					"cpassword" : "Confirm password can not be blank",
					"cpassword_not_match" : "Confirm Password does not match",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully created your profile"

			},
			'fr': {
					"first_name": "First Name can not be blank2" ,
					"last_name" : "Last Name can not be blank2",
					"email_id" : "Email Id can not be blank",
					"email_id_exists" : "Email Id already exists",
					"role" : "Role can not be blank",
					"language" : "Language can not be blank",
					"registration_method" : "Something went wrong",
					"password" : "Password can not be blank",
					"cpassword" : "Confirm password can not be blank",
					"cpassword_not_match" : "Confirm Password does not match",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully created your profile"

			},
			'zh-Hans': {
					"first_name": "First Name can not be blank3" ,
					"last_name" : "Last Name can not be blank3",
					"email_id" : "Email Id can not be blank",
					"email_id_exists" : "Email Id already exists",
					"role" : "Role can not be blank",
					"language" : "Language can not be blank",
					"registration_method" : "Something went wrong",
					"password" : "Password can not be blank",
					"cpassword" : "Confirm password can not be blank",
					"cpassword_not_match" : "Confirm Password does not match",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully created your profile"
			},
			'de': {
					"first_name": "First Name can not be blank4" ,
					"last_name" : "Last Name can not be blank4",
					"email_id" : "Email Id can not be blank",
					"email_id_exists" : "Email Id already exists",
					"role" : "Role can not be blank",
					"language" : "Language can not be blank",
					"registration_method" : "Something went wrong",
					"password" : "Password can not be blank",
					"cpassword" : "Confirm password can not be blank",
					"cpassword_not_match" : "Confirm Password does not match",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully created your profile"
			} 		
		}
		
		try:
			return  addMsgList[lang][key]
		except Exception as e:
			return False

class LoginMsgMod():
	def loginMsg( lang, key ):
		#------------------------------------------------English----------------------------------------#
		loginList = {
			'en' : {
					"registration_method_error" : "Please check your given credentials",
					"username" : "Username can not be blank",
					"password" : "Password can not be blank",
					"success-msg" : "You have successfully created your profile",
					"error-msg"  : "Your given id does not exists",
					"phone_no_not_verified" : "Sorry!! Your given phone number is not yet verified"

			},
			'es' : {
					"registration_method_error" : "Please check your given credentials",
					"username" : "Username can not be blank2",
					"password" : "Password can not be blank",
					"success-msg" : "You have successfully created your profile",
					"error-msg"  : "Your given id does not exists",
					"phone_no_not_verified" : "Sorry!! Your given phone number is not yet verified"

			},
			'fr': {
					"registration_method_error" : "Please check your given credentials",
					"username" : "Username can not be blank3",
					"password" : "Password can not be blank",
					"success-msg" : "You have successfully created your profile",
					"error-msg"  : "Your given id does not exists",
					"phone_no_not_verified" : "Sorry!! Your given phone number is not yet verified"

			},
			'zh-Hans': {
					"registration_method_error" : "Please check your given credentials",
					"username" : "Username can not be blank4",
					"password" : "Password can not be blank",
					"success-msg" : "You have successfully created your profile",
					"error-msg"  : "Your given id does not exists",
					"phone_no_not_verified" : "Sorry!! Your given phone number is not yet verified"
			},
			'de': {
					"registration_method_error" : "Please check your given credentials",
					"username" : "Username can not be blank5",
					"password" : "Password can not be blank",
					"success-msg" : "You have successfully created your profile",
					"error-msg"  : "Your given id does not exists",
					"phone_no_not_verified" : "Sorry!! Your given phone number is not yet verified"
			} 		
		}
		
		try:
			return  loginList[lang][key]
		except Exception as e:
			return False

class ChangePasswordMsgMod():
	def Msg( lang, key ):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"old_password" : "Old Password can not be blank",
					"old_password_not_matched" : "Old Password does not match",
					"new_password" : "New Password can not be blank",
					"confirm_password" : "Confirm Password can not be blank",
					"same_as_old" : "New Password is same as old",
					"cpassword_not_matched" : "Confirm Password does not match",
					"success-msg" : "You have successfully reset your password"

			},
			'es' : {
					"old_password" : "Old Password can not be blank",
					"old_password_not_matched" : "Old Password does not match",
					"new_password" : "New Password can not be blank",
					"confirm_password" : "Confirm Password can not be blank",
					"same_as_old" : "New Password is same as old",
					"cpassword_not_matched" : "Confirm Password does not match",
					"success-msg" : "You have successfully reset your password"

			},
			'fr': {
					"old_password" : "Old Password can not be blank",
					"old_password_not_matched" : "Old Password does not match",
					"new_password" : "New Password can not be blank",
					"confirm_password" : "Confirm Password can not be blank",
					"same_as_old" : "New Password is same as old",
					"cpassword_not_matched" : "Confirm Password does not match",
					"success-msg" : "You have successfully reset your password"

			},
			'zh-Hans': {
					"old_password" : "Old Password can not be blank",
					"old_password_not_matched" : "Old Password does not match",
					"new_password" : "New Password can not be blank",
					"confirm_password" : "Confirm Password can not be blank",
					"same_as_old" : "New Password is same as old",
					"cpassword_not_matched" : "Confirm Password does not match",
					"success-msg" : "You have successfully reset your password"
			},
			'de': {
					"old_password" : "Old Password can not be blank",
					"old_password_not_matched" : "Old Password does not match",
					"new_password" : "New Password can not be blank",
					"confirm_password" : "Confirm Password can not be blank",
					"same_as_old" : "New Password is same as old",
					"cpassword_not_matched" : "Confirm Password does not match",
					"success-msg" : "You have successfully reset your password"
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class ForgotPasswordMailSendMsgMod():
	def Msg( lang, key ):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"forgot_username" : "Email ID field can not be blank",
					"forgot_username_not_exists" : "Email ID does not exists",
					"success-msg" : "A verification code has been sent to your email id. Please check.",
					"error-msg" : "Something went wrong",
					"social_not_applicable" : "Your mail id has been registared with social media. You are not allowed",
					"deactive_account" : "Sorry!! your account is deactivated",
					"deleted_account"  : "Sorry!! your account is deleted",

			},
			'es' : {
					"forgot_username" : "Email ID field can not be blank",
					"forgot_username_not_exists" : "La identificación del correo electrónico no existe",
					"success-msg" : "A verification code has been sent to your email id. Please check.",
					"error-msg" : "Something went wrong",
					"social_not_applicable" : "Your mail id has been registared with social media. You are not allowed",
					"deactive_account" : "Sorry!! your account is deactivated",
					"deleted_account"  : "Sorry!! your account is deleted",

			},
			'fr': {
					"forgot_username" : "Email ID field can not be blank",
					"forgot_username_not_exists" : "L'ID e-mail n'existe pas",
					"success-msg" : "A verification code has been sent to your email id. Please check.",
					"error-msg" : "Something went wrong",
					"social_not_applicable" : "Your mail id has been registared with social media. You are not allowed",
					"deactive_account" : "Sorry!! your account is deactivated",
					"deleted_account"  : "Sorry!! your account is deleted",

			},
			'zh-Hans': {
					"forgot_username" : "Email ID field can not be blank",
					"forgot_username_not_exists" : "电子邮件ID不存在",
					"success-msg" : "A verification code has been sent to your email id. Please check.",
					"error-msg" : "Something went wrong",
					"social_not_applicable" : "Your mail id has been registared with social media. You are not allowed",
					"deactive_account" : "Sorry!! your account is deactivated",
					"deleted_account"  : "Sorry!! your account is deleted",
			},
			'de': {
					"forgot_username" : "Email ID field can not be blank",
					"forgot_username_not_exists" : "E-Mail-ID existiert nicht",
					"success-msg" : "A verification code has been sent to your email id. Please check.",
					"error-msg" : "Something went wrong",
					"social_not_applicable" : "Your mail id has been registared with social media. You are not allowed",
					"deactive_account" : "Sorry!! your account is deactivated",
					"deleted_account"  : "Sorry!! your account is deleted",
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class ResetPasswordMsgMod():
	def Msg( lang, key ):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"new_password" : "New Password can not be blank",
					"confirm_password" : "Confirm Password can not be blank",
					"confirm_password_not_matched" : "Confirm Password does not match",
					"success-msg" : "You have successfully reset your password",
					"error-msg" : "Something went wrong",
					"not-found"  : "Sorry! you are not authorized to reset your password"

			},
			'es' : {
					"new_password" : "New Password can not be blank",
					"confirm_password" : "Confirm Password can not be blank",
					"confirm_password_not_matched" : "Confirm Password does not match",
					"success-msg" : "You have successfully reset your password",
					"error-msg" : "Something went wrong",
					"not-found"  : "Sorry! you are not authorized to reset your password"

			},
			'fr': {
					"new_password" : "New Password can not be blank",
					"confirm_password" : "Confirm Password can not be blank",
					"confirm_password_not_matched" : "Confirm Password does not match",
					"success-msg" : "You have successfully reset your password",
					"error-msg" : "Something went wrong",
					"not-found"  : "Sorry! you are not authorized to reset your password"
			},
			'zh-Hans': {
					"new_password" : "New Password can not be blank",
					"confirm_password" : "Confirm Password can not be blank",
					"confirm_password_not_matched" : "Confirm Password does not match",
					"success-msg" : "You have successfully reset your password",
					"error-msg" : "Something went wrong",
					"not-found"  : "Sorry! you are not authorized to reset your password"
			},
			'de': {
					"new_password" : "New Password can not be blank",
					"confirm_password" : "Confirm Password can not be blank",
					"confirm_password_not_matched" : "Confirm Password does not match",
					"success-msg" : "You have successfully reset your password",
					"error-msg" : "Something went wrong",
					"not-found"  : "Sorry! you are not authorized to reset your password"
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False

class DeleteUserMsgMod():
	def Msg( lang, key ):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"success-msg" : "You have successfully deleted your account",
					"error-msg" : "Something went wrong",
					"not-found"  : "Something went wrong"

			},
			'es' : {
					"success-msg" : "You have successfully deleted your account",
					"error-msg" : "Something went wrong",
					"not-found"  : "Something went wrong"

			},
			'fr': {
					"success-msg" : "You have successfully deleted your account",
					"error-msg" : "Something went wrong",
					"not-found"  : "Something went wrong"
			},
			'zh-Hans': {
					"success-msg" : "You have successfully deleted your account",
					"error-msg" : "Something went wrong",
					"not-found"  : "Something went wrong"
			},
			'de': {
					"success-msg" : "You have successfully deleted your account",
					"error-msg" : "Something went wrong",
					"not-found"  : "Something went wrong"
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False

class BlockUserMsgMod():
	def Msg( lang, key ):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"success-msg" : "You have successfully deactivated your account",
					"error-msg" : "Something went wrong",
					"not-found"  : "Something went wrong"

			},
			'es' : {
					"success-msg" : "You have successfully deactivated your account",
					"error-msg" : "Something went wrong",
					"not-found"  : "Something went wrong"

			},
			'fr': {
					"success-msg" : "You have successfully deactivated your account",
					"error-msg" : "Something went wrong",
					"not-found"  : "Something went wrong"
			},
			'zh-Hans': {
					"success-msg" : "You have successfully deactivated your account",
					"error-msg" : "Something went wrong",
					"not-found"  : "Something went wrong"
			},
			'de': {
					"success-msg" : "You have successfully deactivated your account",
					"error-msg" : "Something went wrong",
					"not-found"  : "Something went wrong"
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False

class PhoneVerificationSmsSendMsgMod():
	def Msg( lang, key ):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"phone_number" : "Phone number can not be blank",
					"isd_code" : "ISD code can not be blank",
					"phone_number_already_exists" : "Phone number is already exists",
					"success-msg" : "A verification code has been sent to your phone number. Please check.",
					"error-msg" : "Something went wrong",
					"already_validated" : "Your phone number has already verified"

			},
			'es' : {
					"phone_number" : "Phone number can not be blank",
					"isd_code" : "ISD code can not be blank",
					"phone_number_already_exists" : "Phone number is already exists",
					"success-msg" : "A verification code has been sent to your phone number. Please check.",
					"error-msg" : "Something went wrong",
					"already_validated" : "Your phone number has already verified"

			},
			'fr': {
					"phone_number" : "Phone number can not be blank",
					"isd_code" : "ISD code can not be blank",
					"phone_number_already_exists" : "Phone number is already exists",
					"success-msg" : "A verification code has been sent to your phone number. Please check.",
					"error-msg" : "Something went wrong",
					"already_validated" : "Your phone number has already verified"

			},
			'zh-Hans': {
					"phone_number" : "Phone number can not be blank",
					"isd_code" : "ISD code can not be blank",
					"phone_number_already_exists" : "Phone number is already exists",
					"success-msg" : "A verification code has been sent to your phone number. Please check.",
					"error-msg" : "Something went wrong",
					"already_validated" : "Your phone number has already verified"
			},
			'de': {
					"phone_number" : "Phone number can not be blank",
					"isd_code" : "ISD code can not be blank",
					"phone_number_already_exists" : "Phone number is already exists",
					"success-msg" : "A verification code has been sent to your phone number. Please check.",
					"error-msg" : "Something went wrong",
					"already_validated" : "Your phone number has already verified"
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False
		


class PhoneVerificationWithOtpMsgMod():
	def Msg( lang, key ):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"otp_code" : "OTP can not be blank",
					"invalid_otp" : "Sorry!! invalid OTP",
					"success-msg" : "Your phone number has been successfully verified",
					"error-msg" : "Something went wrong",
					"already_validated" : "Your phone number has already verified"

			},
			'es' : {
					"otp_code" : "OTP can not be blank",
					"invalid_otp" : "Sorry!! invalid OTP",
					"success-msg" : "Your phone number has been successfully verified",
					"error-msg" : "Something went wrong",
					"already_validated" : "Your phone number has already verified"

			},
			'fr': {
					"otp_code" : "OTP can not be blank",
					"invalid_otp" : "Sorry!! invalid OTP",
					"success-msg" : "Your phone number has been successfully verified",
					"error-msg" : "Something went wrong",
					"already_validated" : "Your phone number has already verified"

			},
			'zh-Hans': {
					"otp_code" : "OTP can not be blank",
					"invalid_otp" : "Sorry!! invalid OTP",
					"success-msg" : "Your phone number has been successfully verified",
					"error-msg" : "Something went wrong",
					"already_validated" : "Your phone number has already verified"
			},
			'de': {
					"otp_code" : "OTP can not be blank",
					"invalid_otp" : "Sorry!! invalid OTP",
					"success-msg" : "Your phone number has been successfully verified",
					"error-msg" : "Something went wrong",
					"already_validated" : "Your phone number has already verified"
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class TeacherBookingMsgMod():
	def Msg( lang, key ):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",

			},
			'en' : {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",

			},
			'en' : {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",

			},
			'en' : {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",

			},
			'en' : {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",

			},	
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False		
class UpdateProfileMsgMod():
	def Msg(lang, key):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"first_name": "First Name can not be blank" ,
					"last_name" : "Last Name can not be blank",
					"language" : "Language can not be blank",
					"success-msg" : "Your profile has been updated"

			},
			'es' : {
					"first_name": "First Name can not be blank" ,
					"last_name" : "Last Name can not be blank",
					"language" : "Language can not be blank",
					"success-msg" : "Your profile has been updated"

			},
			'fr': {
					"first_name": "First Name can not be blank" ,
					"last_name" : "Last Name can not be blank",
					"language" : "Language can not be blank",
					"success-msg" : "Your profile has been updated"

			},
			'zh-Hans': {
					"first_name": "First Name can not be blank" ,
					"last_name" : "Last Name can not be blank",
					"language" : "Language can not be blank",
					"success-msg" : "Your profile has been updated"
			},
			'de': {
					"first_name": "First Name can not be blank" ,
					"last_name" : "Last Name can not be blank",
					"language" : "Language can not be blank",
					"success-msg" : "Your profile has been updated"
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False

class UpdateProfileImageMsgMod():
	def Msg(lang, key):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"error-msg" : "Something went wrong",
					"success-msg" : "Your profile picture has been updated"

			},
			'es' : {
					"error-msg" : "Something went wrong",
					"success-msg" : "Your profile picture has been updated"

			},
			'fr': {
					"error-msg" : "Something went wrong",
					"success-msg" : "Your profile picture has been updated"

			},
			'zh-Hans': {
					"error-msg" : "Something went wrong",
					"success-msg" : "Your profile picture has been updated"
			},
			'de': {
					"error-msg" : "Something went wrong",
					"success-msg" : "Your profile picture has been updated"
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False

class BookingsMsgMod():
	def Msg(lang, key):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : { 
					"student_id": "Something went wrong" ,
					"teacher_id" : "Teacher must be selected",
					"lang_id": "Language must be selected" ,
					"booking_duration" : "Booking duration must be provided",
					"student_phone_number" : "Student number must be provided",
					"teacher_phone_number" : "Teacher number must be provided",
					"duration-not-available" : "Sorry!! Not available for selected duration",
					"call_establish_failed" : "Number not reachable",
					"error-msg" : "Something went wrong",
					"success-msg" : "Call Established"

			},
			'es' : {
					"student_id": "Something went wrong" ,
					"teacher_id" : "Teacher must be selected",
					"lang_id": "Language must be selected" ,
					"booking_duration" : "Booking duration must be provided",
					"student_phone_number" : "Student number must be provided",
					"teacher_phone_number" : "Teacher number must be provided",
					"duration-not-available" : "Sorry!! Not available for selected duration",
					"call_establish_failed" : "Number not reachable",
					"error-msg" : "Something went wrong",
					"success-msg" : "Call Established"

			},
			'fr': {
					"student_id": "Something went wrong" ,
					"teacher_id" : "Teacher must be selected",
					"lang_id": "Language must be selected" ,
					"booking_duration" : "Booking duration must be provided",
					"student_phone_number" : "Student number must be provided",
					"teacher_phone_number" : "Teacher number must be provided",
					"duration-not-available" : "Sorry!! Not available for selected duration",
					"call_establish_failed" : "Number not reachable",
					"error-msg" : "Something went wrong",
					"success-msg" : "Call Established"

			},
			'zh-Hans': {
					"student_id": "Something went wrong" ,
					"teacher_id" : "Teacher must be selected",
					"lang_id": "Language must be selected" ,
					"booking_duration" : "Booking duration must be provided",
					"student_phone_number" : "Student number must be provided",
					"teacher_phone_number" : "Teacher number must be provided",
					"duration-not-available" : "Sorry!! Not available for selected duration",
					"call_establish_failed" : "Number not reachable",
					"error-msg" : "Something went wrong",
					"success-msg" : "Call Established"
			},
			'de': {
					"student_id": "Something went wrong" ,
					"teacher_id" : "Teacher must be selected",
					"lang_id": "Language must be selected" ,
					"booking_duration" : "Booking duration must be provided",
					"student_phone_number" : "Student number must be provided",
					"teacher_phone_number" : "Teacher number must be provided",
					"duration-not-available" : "Sorry!! Not available for selected duration",
					"call_establish_failed" : "Number not reachable",
					"error-msg" : "Something went wrong",
					"success-msg" : "Call Established"
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False

				
class DurationMsgMod():
	def Msg(lang, key):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"call_establish_failed" : "Number not reachable",
					"error-msg" : "Something went wrong",
					"success-msg" : "Call Established"

			},
			'es' : {
					"call_establish_failed" : "Number not reachable",
					"error-msg" : "Something went wrong",
					"success-msg" : "Call Established"

			},
			'fr': {
					"call_establish_failed" : "Number not reachable",
					"error-msg" : "Something went wrong",
					"success-msg" : "Call Established"

			},
			'zh-Hans': {
					"call_establish_failed" : "Number not reachable",
					"error-msg" : "Something went wrong",
					"success-msg" : "Call Established"
			},
			'de': {
					"call_establish_failed" : "Number not reachable",
					"error-msg" : "Something went wrong",
					"success-msg" : "Call Established"
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class BrainTreePaymentGatewayMsgMod():
	def Msg(lang, key):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"nonce" : "Nonce is wrong formated",
					"amount_blank" : "Amount can not be blank",
					"amount_invalid" : "Amount value is invalid",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully done your payment",
					"failed-trans" : "Sorry!! Transaction has been declined"

			},
			'es' : {
					"nonce" : "Nonce is wrong formated",
					"amount_blank" : "Amount can not be blank",
					"amount_invalid" : "Amount value is invalid",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully done your payment",
					"failed-trans" : "Sorry!! Transaction has been declined"
			},
			'fr': {
					"nonce" : "Nonce is wrong formated",
					"amount_blank" : "Amount can not be blank",
					"amount_invalid" : "Amount value is invalid",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully done your payment",
					"failed-trans" : "Sorry!! Transaction has been declined"

			},
			'zh-Hans': {
					"nonce" : "Nonce is wrong formated",
					"amount_blank" : "Amount can not be blank",
					"amount_invalid" : "Amount value is invalid",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully done your payment",
					"failed-trans" : "Sorry!! Transaction has been declined"
			},
			'de': {
					"nonce" : "Nonce is wrong formated",
					"amount_blank" : "Amount can not be blank",
					"amount_invalid" : "Amount value is invalid",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully done your payment",
					"failed-trans" : "Sorry!! Transaction has been declined"
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class ReviewsMsgMod():
	def Msg(lang, key):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"star_count" : "Rate must be selected",
					"call_sid" : "Booking ID is missing",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully done your payment",
					"delete_review" : "Successfully deleted",

			},
			'es' : {
					"star_count" : "Rate must be selected",
					"call_sid" : "Booking ID is missing",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully done your payment",
					"delete_review" : "Successfully deleted",
			},
			'fr': {
					"star_count" : "Rate must be selected",
					"call_sid" : "Booking ID is missing",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully done your payment",
					"delete_review" : "Successfully deleted",

			},
			'zh-Hans': {
					"star_count" : "Rate must be selected",
					"call_sid" : "Booking ID is missing",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully done your payment",
					"delete_review" : "Successfully deleted",
			},
			'de': {
					"star_count" : "Rate must be selected",
					"call_sid" : "Booking ID is missing",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully done your payment",
					"delete_review" : "Successfully deleted",
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class PaymentStatusChangeMsgMod():
	def Msg(lang, key):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"call_sid" : "Call sid is missing",
					"gateway_id" : "Gateway id is missing",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully done your payment",

			},
			'es' : {
					"call_sid" : "Call sid is missing",
					"gateway_id" : "Gateway id is missing",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully done your payment",
			},
			'fr': {
					"call_sid" : "Call sid is missing",
					"gateway_id" : "Gateway id is missing",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully done your payment",

			},
			'zh-Hans': {
					"call_sid" : "Call sid is missing",
					"gateway_id" : "Gateway id is missing",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully done your payment",
			},
			'de': {
					"call_sid" : "Call sid is missing",
					"gateway_id" : "Gateway id is missing",
					"error-msg" : "Something went wrong",
					"success-msg" : "You have successfully done your payment",
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class allFeaturedTeacherMsgMod():
	def Msg(lang, key):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",

			},
			'es' : {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",
			},
			'fr': {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",
			},
			'zh-Hans': {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",
			},
			'de': {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class allReviewsMsgMod():
	def Msg(lang, key):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",

			},
			'es' : {
					"not-found" : "No record found",
					"error-msg" : "Something went wrongs",
			},
			'fr': {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",
			},
			'zh-Hans': {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",
			},
			'de': {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class earningStatisticsMsgMod():
	def Msg(lang, key):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",

			},
			'es' : {
					"not-found" : "No record found",
					"error-msg" : "Something went wrongs",
			},
			'fr': {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",
			},
			'zh-Hans': {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",
			},
			'de': {
					"not-found" : "No record found",
					"error-msg" : "Something went wrong",
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False

class earningStatisticsFilterMsgMod():
	def Msg(lang, key):
		#------------------------------------------------English----------------------------------------#
		List = {
			'en' : {
					"id" : "ID is missing",
					"type" : "Type is missing",
					"start_date" : "Start date is missing",
					"end_date" : "End date is missing",
					"no_of_days" : "Min 7 days and max 12 months",
					"no_record"	: "No record found"	,
					"error-msg" : "Something went wrong",

			},
			'es' : {
					"id" : "ID is missing",
					"type" : "Type is missing",
					"start_date" : "Start date is missing",
					"end_date" : "End date is missing",
					"no_of_months" : "No of months is missing",
					"no_record"	: "No record found"	,
					"error-msg" : "Something went wrong",
			},
			'fr': {
					"id" : "ID is missing",
					"type" : "Type is missing",
					"start_date" : "Start date is missing",
					"end_date" : "End date is missing",
					"no_of_months" : "No of months is missing",
					"no_record"	: "No record found"	,
					"error-msg" : "Something went wrong",
			},
			'zh-Hans': {
					"id" : "ID is missing",
					"type" : "Type is missing",
					"start_date" : "Start date is missing",
					"end_date" : "End date is missing",
					"no_of_months" : "No of months is missing",
					"no_record"	: "No record found"	,
					"error-msg" : "Something went wrong",
			},
			'de': {
					"id" : "ID is missing",
					"type" : "Type is missing",
					"start_date" : "Start date is missing",
					"end_date" : "End date is missing",
					"no_of_months" : "No of months is missing",
					"no_record"	: "No record found"	,
					"error-msg" : "Something went wrong",
			} 		
		}
		
		try:
			return  List[lang][key]
		except Exception as e:
			return False