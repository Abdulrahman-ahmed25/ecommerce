from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from products.models import Variation
from .models import Cart, CartItem
# Create your views here.

class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = 'carts/view.html'
    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0) #value is 0,thats meaning the user’s session cookie will expire when the user’s Web browser is closed.
        cart_id = self.request.session.get('cart_id')
        if cart_id == None:
            cart = Cart() #create new cart
            cart.save()
            cart_id = cart.id
            self.request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated:
            cart.user = self.request.user  
            cart.save()
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        item_id = request.GET.get('item')
        delete_item = request.GET.get('delete')
        if item_id:
            item_instance = get_object_or_404(Variation, id= item_id)
            #quantity
            qty = request.GET.get('qty', 1)
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                raise Http404

            cart_item = CartItem.objects.get_or_create(cart= cart, item= item_instance)[0]
            if delete_item:
                cart_item.delete()
            else:
                cart_item.quantity = qty
                cart_item.save()
        context = {
            "object":self.get_object()
        }
        template = self.template_name 
        return render(request, template, context)