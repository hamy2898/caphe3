from django.views.generic import TemplateView, CreateView, DetailView
from  django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Product, Category,BaiViet,Order,OrderDetail,Comment
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages


from django.contrib.auth import authenticate,login
from django.views import View

from django.http import HttpResponseRedirect

#View đăng ký người dùng
class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

#View đăng ký người dùng thành công
class SignUpDoneView(TemplateView):
    template_name = 'registration/signup_done.html'
    title = 'Signup successful'

#View hiển thị trang chủ (index.html)
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        categories = Category.objects.all()
        product = Product.objects.all()[:6]
        context = {
            'categorys': categories,
            'products' : product,
        }
        return context

class Product1(TemplateView):
    template_name = "shop.html"

    def get_context_data(self, **kwargs):
        categories = Category.objects.all()
        product = Product.objects.all()
        context = {
            'categorys1': categories,
            'products1': product,
        }
        return context



def productcat(request,id):
    categories = Category.objects.all()
    procat = Product.objects.filter(category_id=id)

    return render(request, 'productcat.html', {'procat': procat,'categorys2': categories})

def detail(request, pk):
    detail = Product.objects.get(pk=pk)
    product = Product.objects.all()[:3]
    context = {
        'detail': detail,
        'id': pk,
        'products2': product,
        }
    return render(request, 'product_detail.html', context)

class AboutView(TemplateView):
    template_name = "aboutus.html"

    def get_context_data(self, **kwargs):
        context = dict()
        baiviets = BaiViet.objects.all()
        context['baiviets'] = baiviets
        return context


def noidung_baiviet(request, pk):
    baiviet = BaiViet.objects.get(pk=pk)
    # print(binhluans)
    context = {
        'baiviet': baiviet,
        'baiviet_id':pk
        }
    return render(request, 'post.html', context)

class Contact(TemplateView):
    template_name = "contact.html"

cart = {}
def addcart(request):
    if request.is_ajax():
        id = request.POST.get('id')
        num = request.POST.get('num')
        proDetail = Product.objects.get(id = id)
        if id in cart.keys():
            itemCart = {

                'name':proDetail.title,
                'price':proDetail.price,
                'image': str(proDetail.product_img),
                'num': int(cart[id]['num']) +1
            }
        else:
            itemCart = {

                'name': proDetail.title,
                'price': proDetail.price,
                'image': str(proDetail.product_img),
                'num': num
            }
        #them vao cart
        cart[id] = itemCart
        #lưu vào cart
        request.session['cart'] = cart
        #khoi tao cart sang shopping cart
        cartInfo = request.session['cart']
        html = render_to_string('addcart.html',{'cart':cartInfo})
    return HttpResponse(html)

def updatecart(request):
    if request.is_ajax():
        id = request.POST.get('id')
        num = request.POST.get('num')
        if id in cart.keys():
            if(int(cart[id]['num']) > 0 ):
                cart[id] = {
                    'name': cart[id]['name'],
                    'price': cart[id]['price'],
                    'image': cart[id]['image'],
                    'num': num
                }
            else:
                del cart[id]

        request.session['cart'] = cart
        cartInfo = request.session['cart']
        html = render_to_string('addcart.html', {'cart': cartInfo})
    return HttpResponse(html)



def shoppingcart(request):
    total = 0;
    carts = request.session['cart']
    for key,value in carts.items():
        total += int(value['price'])* int(value['num'])
    return render(request,'cart.html',{'total':total})



def checkout(request):
    total = 0;
    carts = request.session['cart']
    for key, value in carts.items():
        total += int(value['price']) * int(value['num'])
    context = {'carts': carts,'total':total}
    return render(request, 'checkout.html', {'total': total,'carts':carts,})

def confirmCart(request):
    if request.method == 'POST':
        new_order = request.POST.get("order_id")
        address = request.POST.get("address")
        custom = request.POST.get("custom")
        note = request.POST.get("note")
        phone = request.POST.get("phone")

        total = 0;
        carts = request.session['cart']
        for key, value in carts.items():
            total += int(value['price']) * int(value['num'])
        context = {'carts': carts, 'total': total}
        orders = Order(order_id = new_order, address = address,custom = custom,note = note,phone = phone, total = total,payment_status = 0,status = 0,accept= False)
        orders.save()
        for key, value in carts.items():
            orderdetail = OrderDetail(orders = orders, pro_name = value['name'],pro_price = value['price'],pro_image = value['image'],quantity =value['num'],status = 0 )
            orderdetail.save()
        context = {
            'order_id': new_order,
            'address' :address,
            'custom':custom,
            'note':note,
            'phone':phone,
            'total': total,
            'orders': orders,
            'pro_name': value['name'],
            'pro_price':value['price'],
            'pro_image': value['image'],
            'quantity': value['num']

        }
        return render(request,'checkout.html',context)
def comment(request):
    if request.method == 'POST':
        name =request.POST.get("name")
        email = request.POST.get("email")
        new_comment = request.POST.get("noidung_binhluan")
        cmt = Comment( name = name,content = new_comment,email = email, accept = False)
        cmt.save()
        context = {
            'name':name,
            'new_comment':new_comment,
            'email': email
        }
        return render(request,'contact.html',context)


def search(request):
    categories = Category.objects.all()
    context = {
        'categorys3': categories,
    }
    if request.method == 'POST':
        srch = request.POST['srh']
        if srch:
            match = Product.objects.filter(Q(title__istartswith = srch))
            if match:
                return render(request,'result.html',{'sr': match})
            else:
                messages.error(request,'Không có kết quả tìm kiếm')
        else:
            return  HttpResponseRedirect('/search/')
    return render(request,'result.html',{'categorys3': categories})











