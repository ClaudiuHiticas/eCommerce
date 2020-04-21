from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, View
from .models import Item, BillingAddress
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from core.models import Order, OrderItem
from django.contrib import messages
from django.utils import timezone
from .forms import CheckoutForm


def item_list(request):
    context = {
        "items": Item.objects.all()
    }
    return render(request, "home.html", context)


def products(request):
    context = {
        "items": Item.objects.all()
    }
    return render(request, "product.html", context)


class CheckoutView(View):

    def get(self, *arg, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "checkout.html", context)

    def post(self, *arg, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                first_name = form.cleaned_data('first_name')
                last_name = form.cleaned_data('last_name')
                email = form.cleaned_data('email')
                phone = form.cleaned_data('phone')
                adress = form.cleaned_data('adress')
                city = form.cleaned_data('city')
                county = form.cleaned_data('county')
                # TODO: add functionality for those
                # same_shipping_address = form.cleaned_data(
                #     'same_shipping_address')
                # save_info = form.cleaned_data('save_info')
                payment_option = form.cleaned_data('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    adress=adress,
                    city=city,
                    county=county,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: add redirect ti the selected payment option
                return redirect('core:checkout')
            else:
                print('Form is not valid')
            messages.warning(self.request, "Failed checkout")
            return redirect('core:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order!")
            return redirect('core:order-summary')


class HomeView(ListView):
    model = Item
    paginate_by = 12
    template_name = "home.html"


class OrderSummatyView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order!")
            return redirect('/')


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity = 1
            order.items.remove(order_item)
            order_item.save()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
            else:
                order.items.remove(order_item)
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)
