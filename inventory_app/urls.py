from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('items/', views.ItemListView.as_view(), name='items'), 
    path('items/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    path('items/create_item/', views.createItem, name='create_item'),
    path('items/update_item/<int:item_id>', views.updateItem, name='update_item'), 
    path('items/delete_item/<int:item_id>', views.deleteItem, name='delete_item'),
]
