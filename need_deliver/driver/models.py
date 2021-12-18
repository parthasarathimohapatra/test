from django.db import models
import uuid
# from webAdmin.NdUsers import nd_users
from webAdmin.models import NdUsers, NdVehicleType, NdSubscriptionPlan, NdCurrencies
import datetime
import os
def get_file_path_driver_obj(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploaded_attachments', filename)
    
class NdObjectTypeModel(models.Model):
	id = models.AutoField(
		auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	object_name = models.TextField(null=True, max_length=100)
	is_status = models.BooleanField(default=True, blank=True)
	is_deleted = models.BooleanField(default=False, blank=True)
	class Meta:
		db_table = 'nd_object_type'

class NdCityModel(models.Model):
	id = models.AutoField(
		auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	city_name = models.TextField(null=True, max_length=100)
	is_status = models.BooleanField(default=True, blank=True)
	is_deleted = models.BooleanField(default=False, blank=True)
	class Meta:
		db_table = 'nd_city'

# class NdVehicleMake(models.Model):
# 	id = models.AutoField(
# 		auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
# 	vehicle_type = models.ForeignKey(NdVehicleType, on_delete=models.CASCADE, related_name='make_type_details', null=True)
# 	make_name = models.TextField(null=True, max_length=100)
# 	is_status = models.BooleanField(default=True, blank=True)
# 	is_deleted = models.BooleanField(default=False, blank=True)
	
# 	class Meta:
# 		db_table = 'nd_vehicle_make'

class NdVehicleModel(models.Model):
	id = models.AutoField(
		auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	vehicle_type = models.ForeignKey(NdVehicleType, on_delete=models.CASCADE, null=True, related_name='vehicletype')
	# vehicle_make = models.ForeignKey(NdVehicleMake, on_delete=models.CASCADE, null=True, related_name='make_details')
	model_name = models.TextField(null=True, max_length=100)
	is_status = models.BooleanField(default=True, blank=True)
	is_deleted = models.BooleanField(default=False, blank=True)
	class Meta:
		db_table = 'nd_vehicle_model'

# class NdServicesModel(models.Model):
# 	id = models.AutoField(
# 		auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
# 	vehicle_type = models.ForeignKey(NdVehicleType, on_delete=models.CASCADE, null=True, related_name='service_vehicle_type_details')
	
# 	services = models.TextField(null=True, max_length=100)
# 	is_status = models.BooleanField(default=True, blank=True)
# 	is_deleted = models.BooleanField(default=False, blank=True)
# 	class Meta:
# 		db_table = 'nd_vehicle_services'

class NdVehicleDetails(models.Model):
	id = models.AutoField(
		auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	image_file = models.ImageField(upload_to='uploaded_images/vehicle_image', null=True, blank=True)
	registration_expiry_date = models.DateField(null=True,blank=True)
	insurance_expiry_date = models.DateField(null=True,blank=True)
	plate_number = models.TextField(null=True)
	city = models.TextField(null=True, max_length=100)
	year = models.IntegerField(null=True)
	vehicle_model = models.ForeignKey(NdVehicleModel, on_delete=models.CASCADE, null=True, related_name='model_details')
	user = models.ForeignKey(NdUsers, on_delete=models.CASCADE, null=True, related_name='driver_vehicle_details')
	wheel_chair_support = models.BooleanField(default=True, blank=True)
	booster_seat_support = models.BooleanField(default=True, blank=True)

	is_status = models.BooleanField(default=True, blank=True)
	is_deleted = models.BooleanField(default=False, blank=True)
	class Meta:
		db_table = 'nd_vehicle_details' 

class NdDriverDetails(models.Model):
	id = models.AutoField(
		auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	driving_licence_expiry_date = models.DateField(null=True,blank=True)
	user = models.ForeignKey(NdUsers, on_delete=models.CASCADE, null=True, related_name='driver_uu_id')
	# vehicle_model = models.ForeignKey(NdVehicleModel, on_delete=models.CASCADE, null=True, related_name='model_deutails')
	
	account_balance = models.DecimalField(max_digits=20, decimal_places=2, null=True, default=0.00)
	account_balance_currency = models.ForeignKey(NdCurrencies, on_delete=models.CASCADE, null=True, related_name='account_balance')
	subscription_plan = models.ForeignKey(NdSubscriptionPlan, on_delete=models.CASCADE, null=True, related_name='dd_subscription_plan')
	vehicle_type = models.ForeignKey(NdVehicleType, on_delete=models.CASCADE, null=True, related_name='typeDetails')
	
	is_status = models.BooleanField(default=True, blank=True)
	is_deleted = models.BooleanField(default=False, blank=True)
	class Meta:
		db_table = 'nd_driver_details' 

class NdAttachments(models.Model):
	id = models.AutoField(
		auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	object_type = models.ForeignKey(NdObjectTypeModel, on_delete=models.CASCADE, null=True, related_name='object_type_details')
	user = models.ForeignKey(NdUsers, on_delete=models.CASCADE, null=True, related_name='driver_user_id')	
	attached_file = models.FileField(upload_to=get_file_path_driver_obj, null=True, blank=True)
	record_number = models.IntegerField(null=True, blank=True, default=1)
	is_status = models.BooleanField(default=True, blank=True)
	is_deleted = models.BooleanField(default=False, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	class Meta:
		db_table = 'nd_attachments'





