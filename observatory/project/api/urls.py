from django.urls import path

from . import views

urlpatterns = [

	path('products', views.funcProducts, name='funcProducts'),
	path('products/', views.funcProducts, name='funcProducts'),
	path('products/<int:pid>', views.funcProductsId, name='funcProductsId'),
	path('products/<int:pid>/', views.funcProductsId, name='funcProductsId'),
	path('shops', views.funcShops, name='funcShops'),
	path('shops/', views.funcShops, name='funcShops'),
	path('shops/<int:sid>', views.funcShopsId, name='funcShopsId'),
	path('shops/<int:sid>/', views.funcShopsId, name='funcShopsId'),
	path('login', views.funcLogin, name='funcLogin'),
	path('login/', views.funcLogin, name='funcLogin'),
	path('logout', views.funcLogout, name='funcLogout'),
	path('logout/', views.funcLogout, name='funcLogout'),
	path('signup', views.funcSignup, name='funcSignup'),
	path('signup/', views.funcSignup, name='funcSignup'),
	path('prices/', views.funcPrices, name='funcPrices'),
	path('prices', views.funcPrices, name='funcPrices'),
]
