from commonApp.message import GenericMsgMod
class DistanceAndCostingCalculationMsgMod():
	def Msg( lang, key ):
		    #------------------------------------------------ English ----------------------------------------#
		List = {
			'en' : {
				"current_lat_long" : "Please provide current Lat Long",
				"drop_location_lat_long1" : "Provide Lat Long of first drop off location",
				"drop_location_lat_long2" : "Provide Lat Long of second drop off location",
				"distance_calculated" : "Distance successfully calculated",
				"route_not_found":"Route not available",
				
			},
			#------------------------------------------------ English ----------------------------------------#
			'km-KH' : {
				"current_lat_long" : "សូមផ្តល់រយៈបណ្តាយនិងទទឹង",
				"drop_location_lat_long1" : "សូមផ្តល់រយៈបណ្តាយនិងទទឹងនៃទីតាំងទី១ដែលត្រូវទម្លាក់ទំនិញ",
				"drop_location_lat_long2" : "សូមផ្តល់រយៈបណ្តាយនិងទទឹងនៃទីតាំងទី២ដែលត្រូវទម្លាក់ទំនិញ",
				"distance_calculated" : "រយៈចម្ងាយត្រូវបានគណនា",
				"route_not_found":"គ្មានផ្លូវនេះទេ",
			},
			#------------------------------------------------ Simplified Chinese  ----------------------------------------#
			'zh-Hans' : {
				"current_lat_long" : "Please provide current Lat Long",
				"drop_location_lat_long1" : "Provide Lat Long of first drop off location",
				"drop_location_lat_long2" : "Provide Lat Long of second drop off location",
				"distance_calculated" : "Distance successfully calculated",
				"route_not_found":"Route not available",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class CostCalculationMsgMod():
	def Msg( lang, key ):
		    #------------------------------------------------ English ----------------------------------------#
		List = {
			'en' : {
				"vehicle_type" : "Vehicle Type is missing",
				"distance" : "Total distance can not be blank",
				"cost_calculated" : "Total costing is calculated",
			},
			#------------------------------------------------ English ----------------------------------------#
			'km-KH' : {
				"vehicle_type" : "សូមបំពេញប្រភេទនៃទោចក្រយានយន្តរបស់លោកអ្នក",
				"distance" : "ចូរបំពេញរយៈចម្ងាយសរុប",
				"cost_calculated" : "ចំណាយសរុបត្រូវបានគណនា",
			},
			#------------------------------------------------ Simplified Chinese  ----------------------------------------#
			'zh-Hans' : {
				"vehicle_type" : "Vehicle Type is missing",
				"distance" : "Total distance can not be blank",
				"cost_calculated" : "Total costing is calculated",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False

class OrderProcessingMsgMod():
	def Msg( lang, key ):
		    #------------------------------------------------ English ----------------------------------------#
		List = {
			'en' : {
				"pick_up_data" : "Pick up location data not found",
				"drop_off_data1" : "First drop off location data not found",	
				"drop_off_data2" : "Second drop off location data not found",	
				"first_location_item_name" : "Item name of first location is missing",
				"second_location_item_name" : "Item name of second location is missing",
				"attach_files_first_location" : "You haven't choose any file for first location",
				"attach_files_second_location" : "You haven't choose any file for second location",
				"collection_payment_method"  : "Payment method for collection not selected",
				"base_fare_payment_method_first"  : "Payment method for base fare not selected",
				"distance" : "Calculated distance can not be blank",
				"base_price" : "Calculated base price can not be blank",
				"pick_up_pick_up_location" : "Pick up location can not be blank",
				"pick_up_contact_name" : "Pick up contact name can not be blank",
				"pick_up_contact_no" : "Pick up contact no can not be blank",
				"pick_up_driver_note" : "Pick up driver note can not be blank",
				"first_drop_off_location" : "First drop off location can not be blank",
				"first_drop_off_contact_name" : "First drop off contact name can not be blank",
				"first_drop_off_contact_number" : "First drop off contact no can not be blank",
				"first_drop_off_note_to_driver" : "First drop off driver note can not be blank",
				"second_drop_off_location" : "Second drop off location can not be blank",
				"second_drop_off_contact_name" : "Second drop off contact name can not be blank",
				"second_drop_off_contact_number" : "Second drop off contact no can not be blank",
				"second_drop_off_note_to_driver" : "Second drop off driver note can not be blank",
				"pick_up_latitude" : "Latitude of pick up location is missing",
				"pick_up_longitude" : "Longitude of pick up location is missing",
				"first_drop_off_latitude" : "Latitude of first drop off location is missing",
				"first_drop_off_longitude" : "Longitude of first drop off location is missing",
				"second_drop_off_latitude" : "Latitude of second drop off location is missing",
				"second_drop_off_longitude" : "Longitude of second drop off location is missing",
				"supplier_id"  : "Supplier ID is missing",
				"driver_id" : "Driver ID is missing",
				"success-msg" : "Order has been successfully placed",
				"cancel-success" : "Your booking has been successfully cancelled",
				"reason_id"  :  "Reason ID is missing",
				"reason_description" : "Reason description is missing",
				"already-deleted" : "Your booking is already cancelled",
				"record-found" : "Records are fetched",
				"not-found" : "Record not found",

			},
			#------------------------------------------------ English ----------------------------------------#
			'km-KH' : {
				
     			"pick_up_data" : "គ្មានព័ត៌មានទាក់ទងនឹងទីតាំងដែលត្រូវទៅយកទំនិញ",
				"drop_off_data1" : "គ្មានព័ត៌មានទាក់ទងនឹងទីតាំងទី១ដែលត្រូវទម្លាក់ទំនិញ",	
				"drop_off_data2" : "គ្មានព័ត៌មានទាក់ទងនឹងទីតាំងទី២ដែលត្រូវទម្លាក់ទំនិញ",	
				"first_location_item_name" : "សូមបំពេញឈ្មោះទំនិញសម្រាប់ទីតាំងទី១",
				"second_location_item_name" : "សូមបំពេញឈ្មោះទំនិញសម្រាប់ទីតាំងទី២",
				"attach_files_first_location" : "សូមបញ្ជាក់រូបភាពសម្រាប់ទីតាំងទី១",
				"attach_files_second_location" : "សូមបញ្ជាក់រូបភាពសម្រាប់ទីតាំងទី២",
				"collection_payment_method"  : "សូមបញ្ជាក់អំពីការទូទាត់ សម្រាប់ការប្រមូលប្រាក់ពីអតិថិជន",
				"base_fare_payment_method_first"  : "សូមជ្រើសរើសតម្លៃនៃការទូទាត់សម្រាប់ថ្លៃដឹកទំនិញ",
				"distance" : "សូមបំពេញរយៈចម្ងាយដើម្បីគណនា",
				"base_price" : "សូមបំពេញថ្លៃដឹកទំនិញ",
				"pick_up_location" : "សូមបំពេញទីតាំងដែលត្រូវទៅយកទំនិញ",
				"pick_up_note_to_driver" : "អធិប្បាយបន្ថែមទៅអ្នកបើកបរ",
				"pick_up_contact_name" : "សូមបំពេញឈ្មោះអ្នកទទួលទំនិញ",
				"pick_up_contact_no" : "សូមផ្តល់លេខទូរស័ព្ទអ្នកទទួលទំនិញ",
				"pick_up_driver_note" : "អធិប្បាយបន្ថែមទៅអ្នកបើកបរ",
				"first_drop_off_location" : "សូមបំពេញទីតាំងដែលត្រូវយកទំនិញទៅអោយអតិថិជន (ទីតាំងទី១)",
				"first_drop_off_contact_name" : "សូមបំពេញឈ្មោះអ្នកទទួលទំនិញ (ទីតាំងទី១)",
				"first_drop_off_contact_number" : "សូមផ្តល់លេខទូរស័ព្ទអ្នកទទួលទំនិញ (ទីតាំងទី១)",
				"first_drop_off_note_to_driver" : "សូមផ្តល់អធិប្បាយបន្ថែមទៅអ្នកបើកបរសម្រាប់ទីតាំងទី១ (ប្រសិនបើមាន)",
				"second_drop_off_location" : "សូមបំពេញទីតាំងដែលត្រូវយកទំនិញទៅអោយអតិថិជន (ទីតាំងទី២)",
				"second_drop_off_contact_name" : "សូមបំពេញឈ្មោះអ្នកទទួលទំនិញ (ទីតាំងទី២)",
				"second_drop_off_contact_number" : "សូមផ្តល់លេខទូរស័ព្ទអ្នកទទួលទំនិញ (ទីតាំងទី២)",
				"second_drop_off_note_to_driver" : "សូមផ្តល់អធិប្បាយបន្ថែមទៅអ្នកបើកបរសម្រាប់ទីតាំងទី២ (ប្រសិនបើមាន)",
				"pick_up_latitude" : "សូមបំពេញ រយៈទទឹងនៃទីតាំងទៅយកទំនិញ",
				"pick_up_longitude" : "សូមបំពេញ រយៈបណ្តោយនៃទីតាំងទៅយកទំនិញ",
				"first_drop_off_latitude" : "សូមបំពេញ រយៈទទឹងនៃទីតាំងដែលត្រូវប្រគល់ទំនិញ (ទីតាំងទី១)",
				"first_drop_off_longitude" : "សូមបំពេញ រយៈបណ្តោយនៃទីតាំងដែលត្រូវប្រគល់ទំនិញ (ទីតាំងទី១)",
				"second_drop_off_latitude" : "សូមបំពេញ រយៈទទឹងនៃទីតាំងដែលត្រូវប្រគល់ទំនិញ (ទីតាំងទី២)",
				"second_drop_off_longitude" : "សូមបំពេញ រយៈបណ្តោយនៃទីតាំងដែលត្រូវប្រគល់ទំនិញ (ទីតាំងទី២)",
				"supplier_id"  : "សូមបំពេញអត្តលេខរបស់លោកអ្នក",
				"driver_id" : "ចូរបំពេញអត្តលេខរបស់លោកអ្នក (អ្នកបើកបរ)",
				"success-msg" : "ការបញ្ជាដឹកត្រូវបានចាប់ផ្តើម",
				"cancel-success" : "Your booking has been successfully cancelled",
				"reason_id"  :  "សូមបំពេញមូលហេតុ",
				"reason_description" : "សូមបញ្ជាក់អំពីមូលហេតុ",
				"already-deleted" : "ការកក់ទុកសម្រាប់ការដឹកទំនិញនេះ ត្រូវបានលុបចោលវិញ",
				"record-found" : "ព័ត៌មានត្រូវបានបញ្ចូល",
				"not-found" : "គ្មានព័ត៌មាននេះទេ",
			},
			#------------------------------------------------ Simplified Chinese  ----------------------------------------#
			'zh-Hans' : {
				"pick_up_data" : "Pick up location data not found",
				"drop_off_data1" : "First drop off location data not found",	
				"drop_off_data2" : "Second drop off location data not found",	
				"first_location_item_name" : "Item name of first location is missing",
				"second_location_item_name" : "Item name of second location is missing",
				"attach_files_first_location" : "You haven't choose any file for first location",
				"attach_files_second_location" : "You haven't choose any file for second location",
				"collection_payment_method"  : "Payment method for collection not selected",
				"base_fare_payment_method_first"  : "Payment method for base fare not selected",
				"distance" : "Calculated distance can not be blank",
				"base_price" : "Calculated base price can not be blank",
				"pick_up_pick_up_location" : "Pick up location can not be blank",
				"pick_up_contact_name" : "Pick up contact name can not be blank",
				"pick_up_contact_no" : "Pick up contact no can not be blank",
				"pick_up_driver_note" : "Pick up driver note can not be blank",
				"first_drop_off_location" : "First drop off location can not be blank",
				"first_drop_off_contact_name" : "First drop off contact name can not be blank",
				"first_drop_off_contact_number" : "First drop off contact no can not be blank",
				"first_drop_off_note_to_driver" : "First drop off driver note can not be blank",
				"second_drop_off_location" : "Second drop off location can not be blank",
				"second_drop_off_contact_name" : "Second drop off contact name can not be blank",
				"second_drop_off_contact_number" : "Second drop off contact no can not be blank",
				"second_drop_off_note_to_driver" : "Second drop off driver note can not be blank",
				"pick_up_latitude" : "Latitude of pick up location is missing",
				"pick_up_longitude" : "Longitude of pick up location is missing",
				"first_drop_off_latitude" : "Latitude of first drop off location is missing",
				"first_drop_off_longitude" : "Longitude of first drop off location is missing",
				"second_drop_off_latitude" : "Latitude of second drop off location is missing",
				"second_drop_off_longitude" : "Longitude of second drop off location is missing",
				"supplier_id"  : "Supplier ID is missing",
				"driver_id" : "Driver ID is missing",
				"success-msg" : "Order has been successfully placed",
				"cancel-success" : "Your booking has been successfully cancelled",
				"reason_id"  :  "Reason ID is missing",
				"reason_description" : "Reason description is missing",
				"already-deleted" : "Your booking is already cancelled",
				"record-found" : "Records are fetched",
				"not-found" : "Record not found",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class VehicleTypesMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"max_distance" : "Max. distance is missing",
				"record-found" : "Records are fetched",
				"not-found" : "Record not found",
			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"max_distance" : "សូមបំពេញរយៈចម្ងាយគិតជាអតិប្បរមា",
				"record-found" : "ព័ត៌មានត្រូវបានបញ្ចូល",
				"not-found" : "គ្មានព័ត៌មាននេះទេ",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"max_distance" : "Max. distance is missing",
				"record-found" : "Records are fetched",
				"not-found" : "Record not found",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class NearestVehicleBookingMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"max_distance" : "Max. distance is missing",
				"record-found" : "Records are fetched",
				"not-found" : "Record not found",
				"not-available" : "Sorry!! No vehicle is available right now",
				"booking-confirmed" : "Your booking has been confirmed",
				"searching" : "Searching for a driver",
			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"max_distance" : "សូមបំពេញរយៈចម្ងាយគិតជាអតិប្បរមា",
				"record-found" : "ព័ត៌មានត្រូវបានបញ្ចូល",
				"not-found" : "គ្មានព័ត៌មាននេះទេ",
				"not-available" : "សូមអភ័យទោស ពុំមានសេវាទេ",
				"booking-confirmed" : "ការកក់ទុកសម្រាប់ការដឹកទំនិញរបស់លោកអ្នកត្រូវបានទទួល",
				"searching" : "កំពុងរកអ្នកដឹក",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"max_distance" : "Max. distance is missing",
				"record-found" : "Records are fetched",
				"not-found" : "Record not found",
				"not-available" : "Sorry!! No vehicle is available right now",
				"booking-confirmed" : "Your booking has been confirmed",
				"searching" : "Searching for a driver",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class DriverResponseMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"driver_id" : "Driver ID is missing",
				"driver_accepted" : "Drive has confirmed your booking",
				"driver_declined" : "Drive has declined your booking",
			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"driver_id" : "ចូរបំពេញអត្តលេខរបស់លោកអ្នក (អ្នកបើកបរ)",
				"driver_accepted" : "ការបញ្ជាដឹករបស់លោកអ្នក មានអ្នកទទួលហើយ",
				"driver_declined" : "ការបញ្ជាដឹករបស់លោកអ្នកត្រូវបានបដិសេធដោយអ្នកបើកបរ",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"driver_id" : "Driver ID is missing",
				"driver_accepted" : "Drive has confirmed your booking",
				"driver_declined" : "Drive has declined your booking",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class ReviewPostMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"posted_by" : "Posted by id is missing",
				"driver_id" : "Driver data is missing",
				"star_rate" : "Give a star rating",
				"order_id" : "Order ID is missing",
				"already_posted":"You have already given your rating",
				"success-msg" : "Rating & review posted",
			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"posted_by" : "Posted by id is missing",
				"driver_id" : "ចូរបំពេញទិន្នន័យរបស់អ្នកបើកបរ",
				"star_rate" : "សូមផ្តល់ពិន្ទុ ដោយសញ្ញាផ្កាយ",
				"order_id" : "សូមបំពេញអត្តលេខនៃការបញ្ជាដឹក",
				"already_posted":"លោកអ្នកផ្តល់ពិន្ទុរួចហើយ",
				"success-msg" : "ការផ្តល់ពិន្ទុ និង Review Posted",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"posted_by" : "Posted by id is missing",
				"driver_id" : "Driver data is missing",
				"star_rate" : "Give a star rating",
				"order_id" : "Order ID is missing",
				"already_posted":"You have already given your rating",
				"success-msg" : "Rating & review posted",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class FetchDriverDetailsMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"success-msg" : "Driver Details has been fetched",
				"driver_id": "Driver ID is missing",
				"order_id" : "Order ID is missing",
 			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"success-msg" : "ព័ត៌មានលម្អិតរបស់អ្នកបើកបរត្រូវបានបញ្ចូលក្នុងប្រព័ន្ធ",
				"driver_id": "ចូរបំពេញអត្តលេខរបស់លោកអ្នក (អ្នកបើកបរ)",
				"order_id" : "សូមបំពេញអត្តលេខនៃការបញ្ជាដឹក",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"success-msg" : "Driver Details has been fetched",
				"driver_id": "Driver ID is missing",
				"order_id" : "Order ID is missing",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class CancelBookingMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"success-msg" : "Driver Details has been fetched",
				"driver_accpted": "Booking could not be cancelled. Driver is already allocated",
				"cancel-success" : "Reason of cancellation is posted",
 			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"success-msg" : "ព័ត៌មានលម្អិតរបស់អ្នកបើកបរត្រូវបានបញ្ចូលក្នុងប្រព័ន្ធ",
				"driver_accpted": "Booking could not be cancelled. Driver is already allocated",
				"cancel-success" : "Reason of cancellation is posted",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"success-msg" : "Driver Details has been fetched",
				"driver_accpted": "Booking could not be cancelled. Driver is already allocated",
				"cancel-success" : "Reason of cancellation is posted",
			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
class CouponCalculationValidationMsgMod():
	def Msg( lang, key ):
		    #----------------------------------------------- English -----------------------------------------------------#
		List = {
			'en' : {
				"success-msg" : "Driver Details has been fetched",
				"applicable_soon": "This offer will applicable soon",
				"promotion_code" : "Please enter your promotion code",
				"delivery_fee" : "Delivery fee is missing",
				"supplier_id" : "Supplier ID is missing",
				"expired" : "Your coupon has been expired",
				"not_exists" : "Given coupon code does not exists",
				"coupon_applied_successfully":"Coupon applied successfully",
 			},
			#------------------------------------------------ Cambodia --------------------------------------------------#
			'km-KH' : {
				"success-msg" : "ព័ត៌មានលម្អិតរបស់អ្នកបើកបរត្រូវបានបញ្ចូលក្នុងប្រព័ន្ធ",
				"applicable_soon": "ការផ្តល់ជូននេះ​ នឹងមកដល់ក្នុងពេលឆាប់ៗខាងមុខនេះ",
				"promotion_code" : "សូមបញ្ចូលលេខកូដប្រូម៉ូសិន",
				"delivery_fee" : "សូមបំពេញថ្លៃដឹកទំនិញ",
				"supplier_id" : "សូមបំពេញអត្តលេខរបស់លោកអ្នក",
				"expired" : "លេខប័ណ្ណនេះអស់សពុលភាពហើយ",
				"not_exists" : "គ្មានលេខប័ណ្ណនេះទេ",
				"coupon_applied_successfully":"ប័ណ្ណនេះអាចប្រើប្រាស់ដោយជោគជ័យ",
			}, 
			#------------------------------------------------ Simplified Chinese ----------------------------------------#
			'zh-Hans' : {
				"success-msg" : "Driver Details has been fetched",
				"applicable_soon": "This offer will applicable soon",
				"promotion_code" : "Please enter your promotion code",
				"delivery_fee" : "Delivery fee is missing",
				"supplier_id" : "Supplier ID is missing",
				"expired" : "Your coupon has been expired",
				"not_exists" : "Given coupon code does not exists",
				"coupon_applied_successfully":"Coupon applied successfully",

			}
		}
		try:
			return  List[lang][key]
		except Exception as e:
			return False
