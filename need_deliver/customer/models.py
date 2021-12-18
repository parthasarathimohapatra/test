from django.db import models

# from webAdmin.NdUsers import nd_users
from webAdmin.models import NdUsers


class NdPackageDetails(models.Model):
	id = models.AutoField(
		auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	package_name = models.TextField(null=True)
	description = models.TextField(null=True)
	customer_u_id = models.IntegerField(null=True)
	supplier_u_id = models.ForeignKey(NdUsers, on_delete=models.CASCADE, null=True, db_column='supplier_u_id')
	driver_u_id = models.IntegerField(null=True)
	# user = models.ForeignKey(NdUsers, on_delete=models.CASCADE, null=True, db_column='NdPackageDetails.driver_u_id')
	reg_date = models.DateField(auto_now_add=True, null=True, blank=True)
	is_status = models.BooleanField(default=True, blank=True)
	is_deleted = models.BooleanField(default=False, blank=True)
	def __str__(self):
		return self.email_id
	class Meta:
		db_table = 'nd_package_details'


