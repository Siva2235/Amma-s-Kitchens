from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CartItem,Order, Payment
import uuid
from .models import Exclusive,Choose,Special_categories,Special_Festivals
from .models import BreakFast,Veg,Non_Veg,Soups,Pasta,Snacks,Starters
from .models import Family_Packages,Chef,Refreshing_Drinks,Quick_Bites,Combo_Offers

# Create your views here.
def home(request):
    exclusive_offers = Exclusive.objects.all()
    wcu = Choose.objects.all()
    popular_foods = Special_categories.objects.all()
    return render(request,'index.html',{'exclusive_offers':exclusive_offers,'wcu': wcu,'popular_foods':popular_foods})

def menu(request):
    break_fast = BreakFast.objects.all()
    veg = Veg.objects.all()
    non_veg = Non_Veg.objects.all()
    soups = Soups.objects.all()
    pasta = Pasta.objects.all()
    snacks = Snacks.objects.all()
    starters = Starters.objects.all()
    return render(request,'menu.html',{'break_fast':break_fast,'veg':veg,'non_veg':non_veg,'soups':soups,'pasta':pasta,'snacks':snacks,'starters':starters})

def special(request):
    festival_specials = Special_Festivals.objects.all()
    family_packages = Family_Packages.objects.all()
    chef = Chef.objects.all()
    refreshing_drinks = Refreshing_Drinks.objects.all()
    quick_bites = Quick_Bites.objects.all()
    combo_offers = Combo_Offers.objects.all()
    return render(request,'special-categories.html',{'festival_specials':festival_specials,'family_packages':family_packages,'chef':chef,'refreshing_drinks':refreshing_drinks,'quick_bites':quick_bites,'combo_offers':combo_offers})

def payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            payment_method = data.get('paymentMethod', '')

            # If payment method is COD, set status to "pending", else set it to "success"
            order_status = "pending" if payment_method.lower() == "cod" else "success"

            # Create the order
            order = Order.objects.create(
                user=request.user,
                delivery_address=data.get('address', ''),
                phone_number=data.get('phone', ''),
                delivery_instructions=data.get('instructions', ''),
                payment_method=payment_method,
                total_amount=float(data.get('total', 0)),
                items=json.dumps(data.get('cartItems', [])),
                status=order_status  # Set status based on payment method
            )

            # Create payment record only if it's not COD
            if payment_method.lower() != "cod":
                Payment.objects.create(
                    order=order,
                    payment_method=order.payment_method,
                    amount=order.total_amount,
                    status="completed",  # Mark payment as completed for UPI/Card
                )

            return JsonResponse({'message': 'Order placed successfully!', 'order_id': order.id, 'status': order.status}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'checkout.html')


@login_required
@csrf_exempt  # Allows JavaScript to send data
def update_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)  # Get cart data from JavaScript
        name = data.get("name")
        price = data.get("price")
        quantity = data.get("quantity")
        image = data.get("image")  

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, name=name, price=price
        )

        cart_item.quantity = quantity # Update quantity
        cart_item.image = image  
        cart_item.save()

        return JsonResponse({"message": "Cart updated"})

    return JsonResponse({"message": "Invalid request"}, status=400)
@login_required
def load_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_data = [
        {"name": item.name, "price": item.price, "quantity": item.quantity,"image": item.image}
        for item in cart_items
    ]
    return JsonResponse({"cart": cart_data})
@login_required
@csrf_exempt
def remove_from_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")

        CartItem.objects.filter(user=request.user, name=name).delete()
        return JsonResponse({"message": "Item removed"})

    return JsonResponse({"message": "Invalid request"}, status=400)

def order_success(request):
    # Get the latest order placed by the user
    order = Order.objects.filter(user=request.user).order_by('-id').first()

    if not order:
        return render(request, 'order_success.html', {'error': 'No recent order found.'})

    # Convert JSON cart items to Python list
    order_items = json.loads(order.items)

    return render(request, 'order_success.html', {'order': order, 'order_items': order_items})

