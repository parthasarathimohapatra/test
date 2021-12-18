from django.contrib import admin

from django.urls import path, include

from supplier import views
from .views import supplier_list
# from django.views.decorators.csrf import csrf_exempt
# from .views import login
# from other_app.views import Home
urlpatterns = [ 
    path('supplier-list', views.supplier_list, name='supplier-list'),
    path('supplier_list_json', views.supplier.as_view(), name='supplier_list_json'),
    path( 'details/<int:id>/', views.RecordDetailsUsers.as_view(), name='supplier_record_details'),
    path( 'updateSupplierRecords/<int:pk>/', views.supplier.as_view(),name="updateSupplier"),
    path( 'updateSupplierRecords/', views.supplier.as_view(),name="updateSupplier"),
    path( 'updateSupplierRecords', views.UpdateMultiRecordUsers.as_view()),

    path( 'assignPromocodeToSupplierDetails/<int:id>/', views.assignPromoCode.as_view(),name="assignPromocodeToSupplierDetails"),
    path( 'assignPromocodeToSupplier/', views.assignPromoCode.as_view(),name="assignPromocodeToSupplier"),
    path( 'assignPromocodeToMultiSuppliers', views.AssignPromoCodeToMultiSuppliers.as_view(), name="assignPromocodeToMultiSuppliers"),
]

