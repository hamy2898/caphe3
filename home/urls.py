from django.urls import path, include
from .views import IndexView, SignUpDoneView, SignUp,Product1, detail,AboutView,noidung_baiviet,addcart,Contact,productcat,comment,search
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from . import views



app_name = 'home'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', SignUp.as_view(success_url=reverse_lazy('home:signup_done')), name='signup'),
    path('signup/done/', SignUpDoneView.as_view(), name='signup_done'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),



    path('', IndexView.as_view(), name='home'),
    path('product/', Product1.as_view(), name='product'),
    path('<int:pk>/' , detail , name='detail'),
    path('about/', AboutView.as_view(), name='about'),
    path('about/<int:pk>', noidung_baiviet, name='noidung_baiviet'),
    path('productcat/<int:id>', productcat, name ='productcat'),
    path('addcart',views.addcart, name = 'addcart'),
    path('contact/', Contact.as_view(), name='contact'),
    path('shoppingcart/',views.shoppingcart,name = 'shoppingcart'),
    path('checkout/',views.checkout, name = 'checkout'),
    path('confirmCart',views.confirmCart, name = 'confirmCart'),
    path('new_comment/', comment, name ='comment'),
    path('search/', search, name = 'search'),
    path('updatecart',views.updatecart, name = 'updatecart')
]