from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from inventory import views

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/items/', views.ItemListCreateView.as_view(), name='item-list-create'),
    path('api/items/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
]
