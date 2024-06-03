from django.shortcuts import render, get_object_or_404, redirect

# Import model

from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json
from .models import Product, Member, Loai
from django.http import HttpResponse
from .models import Order, OrderItem,Orders
from django.views.decorators.http import require_POST
# Create your views here.
#Đăng ký
def register(request):
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')    
    context = {'form':form}
    return render(request, 'pages/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Tài khoản hoặc mật khẩu không đúng!')
    context = {}
    return render(request, 'pages/login.html', context)
def logoutPage(request):
    logout(request)
    return redirect('login')    

# Thành viên
def Member_list(request):
    data={
		'DM_ThanhVien':Customer.objects.all(),

	} 
    return render(request, 'pages/thanhviennhom.html', data)

# Danh sách sản phẩm theo bảng
def product_list_f(request):
    data={
		'DM_SanPham':Product.objects.all(),
	} 
    return render(request, 'pages/DanhSachSanPham.html', data)
# Danh sách sản phẩm theo card
def product_f(request):
    data={
		'DM_SanPham':Product.objects.all(),
	} 
    return render(request, 'pages/index.html', data)

# Tìm kiếm thông tin
def search_product(request):
    query = request.GET.get('q')
    product = None
    if query:
        product = Product.objects.filter(name__icontains=query).first()
    return render(request, 'pages/ChiTietSanPham.html', {'product': product})

#Loai
def Loai_list(request):
    data={
		'DM_Loai':Category.objects.all(),
	} 
    return render(request, 'pages/DanhSachLoai.html', data)

#Chi tiết sản phẩm
def product_detail(request, product_id):
    # Retrieve the product object from the database
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'pages/ChiTietSanPham.html', {'product': product})



def ThemGioHang(request, msp):
    # Initialize the cart if it does not exist
    cart = request.session.get('cart', {})
    # Add or update the item in the cart
    sp = Product.objects.get(id=msp)
    if msp in cart:
        cart[msp]['quantity'] += 1
    else:
        cart[msp] = {
            'name': sp.name,
            'price': str(sp.price),
            'quantity': 1,
        }
    # Save the updated cart back to the session
    request.session['cart'] = cart
    return redirect('xem_gio_hang') 

@require_POST
def CapNhatGioHang(request):
    cart = request.session.get('cart', {})
    for item_id, quantity in request.POST.items():
        if item_id.startswith('quantity_'):
            item_id = item_id.replace('quantity_', '')
            if item_id in cart:
                cart[item_id]['quantity'] = int(quantity)
    request.session['cart'] = cart
    return redirect('xem_gio_hang')
# Xem giỏ hàng
def XemGioHang(request):
    cart = request.session.get('cart', {})
    total_tong = 0
    gio = {}
    for item_id, item in cart.items():
        product = Product.objects.get(id=item_id)
        item['product'] = product  # Thêm thông tin sản phẩm vào từng item
        total_tong += int(item['price']) * item['quantity']
        gio[item_id] = item

    data = {
        'gio': gio,
        'total_tong': total_tong,
    }
    return render(request, 'pages/XemGioHang.html', data)

def XoaGioHang(request):
    request.session['cart'] = {}  # Clear the cart by setting it to an empty dictionary
    return redirect('xem_gio_hang')

def CapNhatGioHang(request):
    cart = request.session.get('cart', {})
    for item_id, quantity in request.POST.items():
        if item_id.startswith('quantity_'):
            item_id = item_id.replace('quantity_', '')
            if item_id in cart:
                cart[item_id]['quantity'] = int(quantity)
    request.session['cart'] = cart
    return redirect('xem_gio_hang')
def XoaSanPhamGioHang(request, item_id):
    cart = request.session.get('cart', {})
    if item_id in cart:
        del cart[item_id]
        request.session['cart'] = cart
    return redirect('xem_gio_hang')


def dat_hang(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        # Lưu thông tin hóa đơn
        orders = Orders.objects.create(name=name, email=email, address=address, phone=phone, total=0)

        # Lưu chi tiết hóa đơn
        cart = request.session.get('cart', {})
        total = 0
        for item_id, item in cart.items():
            product = Product.objects.get(id=item_id)
            quantity = item['quantity']
            price = product.price
            total += price * quantity

            OrderItem.objects.create(orders=orders, product=product, quantity=quantity, price=price)

        orders.total = total
        orders.save()

        # Xóa giỏ hàng sau khi đặt hàng thành công
        request.session['cart'] = {}

        # Chuyển hướng đến trang cảm ơn hoặc trang khác
        return render(request, 'pages/CamOn.html', {'orders': orders})

    # Nếu là phương thức GET, bạn có thể render template đặt hàng
    return render(request, 'pages/DatHang.html')
