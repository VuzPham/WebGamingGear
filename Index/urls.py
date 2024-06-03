from django.urls import path


from . import views # call to url_shortener/views.py 
urlpatterns = [ 
    path('', views.product_f, name='index'), 
    path('Member_list/', views.Member_list, name='Member_list'),
    path('products_list/', views.product_list_f, name='products_list'),
    path('products/', views.product_f, name='products'),
    path('loai_list/', views.Loai_list, name='loai_list'),
    path('product/<str:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.search_product, name='search_product'),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('them_gio_hang/<int:msp>/', views.ThemGioHang, name='them_gio_hang'),
    path('xem_gio_hang/', views.XemGioHang, name='xem_gio_hang'),
    path('xoa_gio_hang/', views.XoaGioHang, name='xoa_gio_hang'),
    path('cap_nhat_gio_hang/', views.CapNhatGioHang, name='cap_nhat_gio_hang'),
    path('xoa_san_pham_gio_hang/<str:item_id>/', views.XoaSanPhamGioHang, name='xoa_san_pham_gio_hang'),
    path('dat-hang/', views.dat_hang, name='dat_hang'),
    path('cap_nhat_gio_hang/', views.CapNhatGioHang, name='cap_nhat_gio_hang'),
] 