# Create your views here.
import uuid

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt

from FrontEnd.models import *
from BackEnd.models import *
from django.core.files.storage import FileSystemStorage
from BackEnd.views import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.core.mail import send_mail
from django.utils import timezone
import datetime
import secrets

from django.shortcuts import redirect, get_object_or_404

import re
from decimal import Decimal
from django.core.exceptions import ValidationError

from django.db import transaction

from django.http import HttpResponse

from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from .models import WishlistDb, CartDb, paintings_Db

from django.shortcuts import get_object_or_404

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from .models import WishlistDb, CartDb, paintings_Db

from django.shortcuts import redirect, get_object_or_404

from django.conf import settings
import razorpay

from django.db.models import Q
from random import sample

from django.views.decorators.cache import never_cache







@never_cache
def Login_page(request):
    artists = artist_Db.objects.all()
    return render(request, "Login_page.html",{"artists":artists})

@never_cache
def Signup_page(request):
    artists = artist_Db.objects.all()
    return render(request, "Signup_page.html",{"artists":artists})
@never_cache
def Forgot_page(request):
    artists = artist_Db.objects.all()
    return render(request, "Forgot_page.html",{"artists":artists})


@never_cache
def save_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('confirm_password')

        # Check email
        if SignUp_Db.objects.filter(Email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect(Signup_page)

        # Check username
        elif SignUp_Db.objects.filter(Username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect(Signup_page)


        # Check password length
        elif len(password) < 5:
            messages.error(request, 'Password is too short. It must be at least 5 characters long.')
            return redirect(Signup_page)

        # Check if password and confirm password match
        elif password != cpassword:
            messages.error(request, 'Passwords do not match.')
            return redirect(Signup_page)


        else:
            obj = SignUp_Db(Email=email, Username=username, Password=password, Cpassword=cpassword)
            obj.save()
            messages.success(request, 'Account registered successfully!')
        return redirect(Login_page)

@never_cache
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        superuser = User.objects.filter(email=email, is_superuser=True).first()

        if superuser and superuser.check_password(password):
            login(request, superuser)
            request.session['Username'] = superuser.username  # Set session variable
            return redirect(index_page)

        try:
            user = SignUp_Db.objects.get(Email=email)
        except SignUp_Db.DoesNotExist:
            user = None

        if user is not None and user.Password == password:
            login(request, user)
            request.session['Username'] = user.Username
            request.session['Email'] = user.Email
            request.session['Password'] = user.Password
            messages.success(request, f'Successfully logged in as "{user.Username}"')
            return redirect(Home_page)
        else:
            messages.error(request, 'Invalid email or password')
            return redirect(Login_page)
    else:
        return redirect(Login_page)


def user_logout(request):
    del request.session['Username']
    return redirect(Login_page)


TOKEN_EXPIRATION_MINUTES = 10  # Adjust as needed


def generate_token():
    return secrets.token_urlsafe(32)


def forgot_password(request):
    artists = artist_Db.objects.all()
    if request.method == 'POST':
        em = request.POST.get('email')
        user = SignUp_Db.objects.filter(Email=em).first()
        if user:
            # Generate a unique token
            token = generate_token()
            # Set the expiration time for the token
            token_expiration = timezone.now() + datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
            # Store the token and expiration time in the user object
            user.password_reset_token = token
            user.token_expiration = token_expiration
            user.save()
            # Send the email with the recovery link
            subject = "Password Reset"
            expiration_message = f"This link will expire in {TOKEN_EXPIRATION_MINUTES} minutes. Please reset your password before then."
            # Format the message with HTML for a clickable hyperlink
            message = f"Click the following link to reset your password: <a href='http://127.0.0.1:4040/FrontEnd/change_password/{token}/'>Reset Password</a><br><br>{expiration_message}"
            frm = 'spj13601@gmail.com'  # Sender email (change accordingly)
            to = em  # Recipient email
            send_mail(subject, '', frm, [to], html_message=message)
            # Extend session expiration
            request.session.set_expiry(TOKEN_EXPIRATION_MINUTES * 60)  # Convert minutes to seconds
            return render(request, 'Verification_page.html', {'expiration_minutes': TOKEN_EXPIRATION_MINUTES})
        else:
            messages.error(request, "Sorry, this email is not registered.")
            return redirect('forgot_password')
    return render(request, 'Forgot_page.html',{"artists":artists})


def change_password(request, token):
    user = SignUp_Db.objects.filter(password_reset_token=token).first()
    if user:
        # Check if the token is expired
        if user.token_expiration < timezone.now():
            return HttpResponse("Sorry, the password reset link has expired.")
        if request.method == 'POST':
            p1 = request.POST.get('password')
            p2 = request.POST.get('confirm_password')
            if p1 == p2:
                # Update user's password and clear the token
                user.Password = p1
                user.Cpassword = p1
                user.password_reset_token = None
                user.token_expiration = None
                user.save()
                messages.success(request, "Password changed successfully.")
                return redirect('Login_page')
            else:
                return HttpResponse('Passwords do not match.')
        return render(request, 'Change_password_page.html')
    else:
        return HttpResponse("Invalid or expired password reset link.")


def verification_page(request):
    return render(request, 'Verification_page.html')

@never_cache
def Home_page(request):
    artists=artist_Db.objects.all()
    try:
        user_profile = Profile.objects.filter(Username=request.session['Username'])
    except KeyError:
        user_profile=None

    paintings_list = paintings_Db.objects.all().order_by('id')[:12]  # Fetch only the first 10 paintings

    # Calculate the total_profiles count dynamically
    total_paintings = paintings_Db.objects.count()

    items_per_page = 12

    paginator = Paginator(paintings_list, items_per_page)
    page = request.GET.get('page')

    try:
        paintings = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page.
        paintings = paginator.page(1)
    except EmptyPage:
        # If the page is out of range (e.g., 9999), deliver the last page of results.
        paintings = paginator.page(paginator.num_pages)

    return render(request, "Home.html",
                  {"paintings": paintings, "total_paintings": total_paintings, 'user_profile': user_profile,"artists":artists})


@never_cache
def index_page(request):
    return render(request, "index.html")

@never_cache
def About_page(request):
    paintings=paintings_Db.objects.all()
    artists=artist_Db.objects.all()
    try:
        user_profile = Profile.objects.filter(Username=request.session['Username'])
    except KeyError:
        user_profile = None
    return render(request, "About.html",{"artists":artists,"paintings":paintings,"user_profile":user_profile})

@never_cache
def Contact_page(request):
    paintings=paintings_Db.objects.all()

    artists=artist_Db.objects.all()
    try:
        user_profile = Profile.objects.filter(Username=request.session['Username'])
    except KeyError:
        user_profile = None
    return render(request, "Contact.html",{"artists":artists,"paintings":paintings,"user_profile":user_profile})

@never_cache
def profile_page(request):
    paintings=paintings_Db.objects.all()
    artists=artist_Db.objects.all()
    try:
        user_profile = Profile.objects.filter(Username=request.session['Username'])
    except KeyError:
        user_profile = None
    return render(request, "profile_page.html", {'user_profile': user_profile,'paintings': paintings,"artists":artists})

@never_cache
def profile_create(request):
    artists=artist_Db.objects.all()
    try:
        user_profile = Profile.objects.filter(Username=request.session['Username'])
    except KeyError:
        user_profile = None
    return render(request, "add_profile_details.html", {'user_profile': user_profile,"artists":artists})


@never_cache
def save_profile(request):
    if request.method == "POST":
        un = request.POST.get('Username')
        na = request.POST.get('name')
        age = request.POST.get('age')
        mob = request.POST.get('mobile')
        st = request.POST.get('state')
        ct = request.POST.get('city')
        hb = request.POST.get('hobby')
        img = request.FILES.get('image', 'Images/usericon11.png')
        obj = Profile(Username=un, name=na, age=age, mobile=mob, state=st, city=ct, hobby=hb, profile_image=img)
        obj.save()
        return redirect(profile_page)
@never_cache
def profile_edit(request):
    artists=artist_Db.objects.all()
    user_profile = Profile.objects.filter(Username=request.session['Username'])

    try:
        profile = Profile.objects.get(Username=request.session['Username'])
    except ObjectDoesNotExist:
        return redirect('profile_create')
    return render(request, "profile_edit.html", {'profile': profile, 'user_profile': user_profile,"artists":artists})

def update_profile(request, p_id):
    if request.method == "POST":
        current_username = request.POST.get('Username')
        new_username = request.POST.get('new_username')
        current_email = request.POST.get('Email')
        new_email = request.POST.get('new_email')
        na=request.POST.get('name')
        age = request.POST.get('age')
        mob = request.POST.get('mobile')
        st = request.POST.get('state')
        ct = request.POST.get('city')
        hb = request.POST.get('hobby')
        try:
            if 'image' in request.FILES:
                img = request.FILES['image']
                fs = FileSystemStorage()
                file = fs.save(img.name, img)
            else:
                if 'image_removed' in request.POST and request.POST.get('image_removed') == 'True':
                    file = 'Images/usericon11.png'
                else:
                    file = Profile.objects.get(id=p_id).profile_image
        except:
            file = Profile.objects.get(id=p_id).profile_image
        request.session['Username'] = new_username
        request.session['Email'] = new_email
        SignUp_Db.objects.filter(Username=current_username,Email=current_email).update(Username=new_username,Email=new_email)
        Profile.objects.filter(id=p_id).update(Username=new_username,name=na, age=age, mobile=mob, state=st, city=ct, hobby=hb,
                                               profile_image=file)
        return redirect(profile_page)

def delete_profile(request):
    try:
        profile = Profile.objects.get(Username=request.session['Username'])
        profile.delete()
        messages.success(request, 'Your profile details has been successfully deleted.')
    except Profile.DoesNotExist:
        pass  # Profile doesn't exist, nothing to delete
    return redirect('profile_page')

@never_cache
def profile_user_paintings(request):
    artists=artist_Db.objects.all()
    user_profile = Profile.objects.filter(Username=request.session['Username'])

    # Filter paintings for the current user
    paintings_list = paintings_Db.objects.filter(username=request.session['Username'])

    # Calculate the total_profiles count dynamically
    total_paintings = paintings_list.count()

    items_per_page = 6

    paginator = Paginator(paintings_list, items_per_page)
    page = request.GET.get('page')

    try:
        paintings = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page.
        paintings = paginator.page(1)
    except EmptyPage:
        # If the page is out of range (e.g., 9999), deliver the last page of results.
        paintings = paginator.page(paginator.num_pages)

    return render(request, "profile_user_paintings.html",
                  {"paintings": paintings, "total_paintings": total_paintings, 'user_profile': user_profile,"artists":artists})



def delete_painting(request):
    if request.method == 'POST':
        painting_id = request.POST.get('painting_id')
        painting = get_object_or_404(paintings_Db, pk=painting_id)

        # Check if the painting belongs to the current user or has permission to delete
        if painting.username == request.session.get('Username'):
            painting_name = painting.pname  # Retrieve the name of the painting
            painting.delete()
            message = f'Your painting <span class="orange-text">"{painting_name}"</span> is deleted '
            messages.success(request, mark_safe(message))
        else:
            messages.error(request, 'You do not have permission to delete this painting.')
    return redirect('profile_user_paintings')


@never_cache
def wishlist(request):
    artists=artist_Db.objects.all()
    # Check if the 'Username' key exists in the session
    if 'Username' not in request.session:
        # Store the current page's URL in the session
        request.session['redirect_to'] = request.build_absolute_uri()
        # Add an info-level message
        messages.warning(request, 'You need to log in first before viewing your wishlist.')
        # Redirect back to the current page
        return redirect(
            request.META.get('HTTP_REFERER', '/'))  # Redirect to the referrer or home page if referrer not available

    user_profile = Profile.objects.filter(Username=request.session['Username'])

    username = request.session.get('Username')
    wishlist_items = WishlistDb.objects.filter(Username=username)

    # Calculate the total_profiles count dynamically
    total_paintings = wishlist_items.count()

    items_per_page = 6

    paginator = Paginator(wishlist_items, items_per_page)
    page = request.GET.get('page')

    try:
        paintings = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page.
        paintings = paginator.page(1)
    except EmptyPage:
        # If the page is out of range (e.g., 9999), deliver the last page of results.
        paintings = paginator.page(paginator.num_pages)

    return render(request, "Wishlist.html",
                  {"paintings": paintings, 'wishlist_items': wishlist_items, "total_paintings": total_paintings,
                   'user_profile': user_profile,"artists":artists})


def delete_wishlist(request):
    if request.method == 'POST':
        painting_id = request.POST.get('painting_id')
        painting = get_object_or_404(WishlistDb, pk=painting_id)

        # Check if the painting belongs to the current user
        if painting.Username == request.session.get('Username'):
            painting_name = painting.product.pname  # Retrieve the name of the painting
            painting.delete()
            message = f' The painting <span class="orange-text">"{painting_name}"</span> is removed'
            messages.success(request, mark_safe(message))
        else:
            # Add error message if the painting does not belong to the current user
            messages.error(request, 'You are not authorized to delete this painting.')

        return redirect('wishlist')

@never_cache
def addressbook(request):
    artists=artist_Db.objects.all()
    user_profile = Profile.objects.filter(Username=request.session['Username'])
    username = request.session.get('Username')
    address = Address.objects.filter(Username=username)
    return render(request,"profile_addressbook.html",{'address':address,'user_profile':user_profile,"artists":artists})


@never_cache
def addaddress(request):
    artists=artist_Db.objects.all()
    return render(request,"profile_addaddress.html",{"artists":artists})



def save_address(request):
    if request.method == "POST":
        un = request.POST.get('Username')
        fn = request.POST.get('firstname')
        ln = request.POST.get('lastname')
        phn = request.POST.get('phone')
        email = request.POST.get('email')
        addrs = request.POST.get('address_line_1')
        lnd = request.POST.get('address_line_2')
        ct = request.POST.get('city')
        st = request.POST.get('state')
        pin = request.POST.get('pincode')
        deflt_str = request.POST.get('default', '').lower()
        deflt = deflt_str == 'true'

        # If set as default is checked, update other default addresses
        if deflt:
            Address.objects.filter(default=True).update(default=False)

        obj = Address(Username=un,firstname=fn, lastname=ln, phone=phn, email=email, address_line_1=addrs,
                      address_line_2=lnd, city=ct, state=st, pincode=pin, default=deflt)
        obj.save()
        messages.success(request, 'New address created successfully')

        # Check if the referer is from the checkout page
        if 'Checkout_page' in request.META.get('HTTP_REFERER', ''):
            # Redirect to the checkout page
            return HttpResponseRedirect(reverse('Checkout_page'))
        else:
            # Redirect to the address book page
            return HttpResponseRedirect(reverse('addressbook'))

@never_cache
def Edit_address(request,a_id):
    artists=artist_Db.objects.all()
    address=Address.objects.get(id=a_id)
    return render(request,"profile_editaddress.html",{'address':address,"artists":artists})

def update_address(request,a_id):
    if request.method == "POST":
        un = request.POST.get('Username')
        fn = request.POST.get('firstname')
        ln = request.POST.get('lastname')
        phn = request.POST.get('phone')
        email = request.POST.get('email')
        addrs = request.POST.get('address_line_1')
        lnd = request.POST.get('address_line_2')
        ct = request.POST.get('city')
        st = request.POST.get('state')
        pin = request.POST.get('pincode')
        deflt_str = request.POST.get('default', '').lower()
        deflt = deflt_str == 'true'
        if deflt:
            Address.objects.filter(default=True,Username=un).update(default=False)
        Address.objects.filter(id=a_id).update(Username=un,firstname=fn, lastname=ln, phone=phn, email=email, address_line_1=addrs,
                      address_line_2=lnd, city=ct, state=st, pincode=pin, default=deflt)
        messages.success(request, 'Current address edited successfully')
        return redirect(addressbook)


def delete_selected_addresses(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        selected_addresses = request.POST.getlist('selected_addresses[]')
        # Perform deletion of selected addresses from the database
        deleted_count, _ = Address.objects.filter(id__in=selected_addresses).delete()
        if deleted_count > 0:
            messages.success(request, 'Selected addresses deleted successfully.')
        else:
            messages.warning(request, 'No addresses were deleted.')
        return HttpResponse()  # You can return an empty HttpResponse for AJAX requests
    else:
        messages.error(request, 'Invalid request.')
        return HttpResponse(status=400)


@never_cache
def ordersbook(request):
    orders=Order.objects.filter(Username=request.session['Username']).order_by('-created_at')
    user_profile = Profile.objects.filter(Username=request.session['Username'])
    return render(request,"profile_orders.html",{'orders': orders,'user_profile': user_profile})

def order_view(request,order_id):
    paintings=paintings_Db.objects.all()

    order=Order.objects.get(id=order_id)
    user_profile = Profile.objects.filter(Username=request.session['Username'])
    return render(request,"order_view.html",{'order': order,'user_profile': user_profile,'paintings': paintings})

def cancel_order(request, order_id):
    if request.method == "POST":
        order = Order.objects.get(id=order_id)
        order.order_status = 'Order Cancelled'
        order.save()
        messages.success(request, 'Order has been cancelled successfully.')
        return redirect(reverse('order_view', args=[order_id]))

from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST

@require_POST
def delete_selected_orders(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        selected_orders = request.POST.getlist('selected_orders[]')

        # Update the is_deleted flag instead of deleting the records
        updated_count = Order.objects.filter(id__in=selected_orders).update(is_deleted=True)

        if updated_count > 0:
            messages.success(request, f'Selected orders marked as deleted successfully.')
        else:
            messages.warning(request, 'No orders were marked as deleted.')

        return JsonResponse({'status': 'success'})  # Return JSON response for AJAX requests
    else:
        messages.error(request, 'Invalid request.')
        return JsonResponse({'status': 'error'}, status=400)

def delete_account(request):
    if request.method == 'POST':
        # Get the username or email of the logged-in user
        username = request.session.get('Username')
        email = request.session.get('Email')

        # Delete user data from SignUp_Db
        SignUp_Db.objects.filter(Username=username).delete()
        SignUp_Db.objects.filter(Email=email).delete()

        # Delete user profile
        Profile.objects.filter(Username=username).delete()

        # Delete user cart items
        CartDb.objects.filter(Username=username).delete()

        # Delete user wishlist items
        WishlistDb.objects.filter(Username=username).delete()

        # Delete user addresses
        Address.objects.filter(email=email).delete()

        paintings_Db.objects.filter(username=username).delete()

        # Clear session data
        request.session.flush()

        messages.success(request, "Current account deleted succesfully.")
        # Redirect to a page indicating successful account deletion
        return render(request, 'Home.html')

    # Handle cases where the request method is not POST
    return redirect('profile_page')

@never_cache
def profile_change_password(request):
    artists=artist_Db.objects.all()
    user_profile1 = SignUp_Db.objects.get(Username=request.session['Username'])
    user_profile = Profile.objects.filter(Username=request.session['Username'])


    if request.method == 'POST':
        oldpass = request.POST['currentpassword']
        newpass = request.POST['newpassword']
        confirm_newpass = request.POST['confirmpassword']

        # Check if old password matches
        if oldpass != user_profile1.Password:
            messages.error(request, "Incorrect current password")
            return redirect('profile_change_password')

        # Check if new password is the same as the old one
        if oldpass == newpass:
            messages.error(request, "New Password should not be the same as the Previous Password")
            return redirect('profile_change_password')

        # Check if new password and confirm password match
        if newpass != confirm_newpass:
            messages.error(request, "Password not matching")
            return redirect('profile_change_password')

        # Add more password complexity checks if needed
        # For example, you can use regular expressions to enforce specific patterns

        # If all conditions are met, update the password
        user_profile1.Password = newpass
        user_profile1.Cpassword = newpass
        user_profile1.save()

        messages.success(request, "Password changed successfully")
        return redirect('Login_page')  # Redirect to the login page after changing password

    return render(request, 'profile_change_password.html',{"artists":artists,"user_profile":user_profile})


@never_cache
def Single_page(request, p_id):
    paintings=paintings_Db.objects.all()

    artists = artist_Db.objects.all()

    if 'Username' not in request.session:
        request.session['redirect_to'] = request.build_absolute_uri()
        messages.warning(request, 'You need to log in first before viewing this product.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    pro = paintings_Db.objects.get(id=p_id)
    existing_item = CartDb.objects.filter(Username=request.session.get('Username'), painting=pro).first()
    user_profile = Profile.objects.filter(Username=request.session['Username'])

    # Get all paintings of the same type as the current painting
    paintings_same_type = paintings_Db.objects.filter(picture_type=pro.picture_type).exclude(id=p_id)

    # Randomly select 8 paintings from the queryset
    paintings = sample(list(paintings_same_type), min(8, paintings_same_type.count()))

    return render(request, "Single_product.html",
                  {'pro': pro, 'existing_item': existing_item, 'paintings': paintings,
                   'user_profile': user_profile, 'artists': artists, 'paintings': paintings})

@never_cache
def Shop(request):
    artists=artist_Db.objects.all()
    data = painting_type_Db.objects.all()
    try:
        user_profile = Profile.objects.filter(Username=request.session['Username'])
    except KeyError:
        user_profile = None
    paintings_list = paintings_Db.objects.all().order_by('id')

    # Calculate the total_profiles count dynamically
    total_paintings = paintings_Db.objects.count()

    items_per_page = 12

    paginator = Paginator(paintings_list, items_per_page)
    page = request.GET.get('page')

    try:
        paintings = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page.
        paintings = paginator.page(1)
    except EmptyPage:
        # If the page is out of range (e.g., 9999), deliver the last page of results.
        paintings = paginator.page(paginator.num_pages)

    return render(request, "Shop.html", {"paintings": paintings,"user_profile": user_profile, "total_paintings": total_paintings,"artists":artists,"data":data})



@never_cache
def shop_filter(request):
    artists = artist_Db.objects.all()
    data = painting_type_Db.objects.all()
    paintings_list = paintings_Db.objects.all().order_by('id')

    selected_type = request.GET.get('type')

    if selected_type:
        paintings_list = paintings_list.filter(picture_type=selected_type)

    total_paintings = paintings_list.count()

    items_per_page = 8

    paginator = Paginator(paintings_list, items_per_page)
    page = request.GET.get('page')

    try:
        paintings = paginator.page(page)
    except PageNotAnInteger:
        paintings = paginator.page(1)
    except EmptyPage:
        paintings = paginator.page(paginator.num_pages)

    # Render a partial template with the filtered paintings
    return render(request, "Shop_filter_paintings.html",
                  {"paintings": paintings, "total_paintings": total_paintings, "artists": artists, "data": data,
                   "selected_type": selected_type})


@never_cache
def Cart_page(request):
    paintings=paintings_Db.objects.all()

    artists=artist_Db.objects.all()

    # Check if the 'Username' key exists in the session
    if 'Username' not in request.session:
        # Store the current page's URL in the session
        request.session['redirect_to'] = request.build_absolute_uri()
        # Add an info-level message
        messages.warning(request, 'You need to log in first before viewing your cart.')
        # Redirect back to the current page
        return redirect(
            request.META.get('HTTP_REFERER', '/'))  # Redirect to the referrer or home page if referrer not available
    else:
        # If the user is logged in, proceed to render the cart page
        user_profile = Profile.objects.filter(Username=request.session['Username'])
        data = CartDb.objects.filter(Username=request.session['Username'])
        total_price = 0
        for i in data:
            total_price = total_price + i.tprice
        AppliedCoupon.objects.filter(Username=request.session['Username'], is_active=True).delete()
        return render(request, "Cart.html", {'data': data,'paintings': paintings, 'total_price': total_price, 'user_profile': user_profile,"artists":artists})


def save_cart(request):
    if request.method == "POST":
        un = request.POST.get('Username')
        painting_id = request.POST.get('painting_id')
        qty = int(request.POST.get('quantity', 0))
        pr = (request.POST.get('price', 0))
        tp = (request.POST.get('tprice', 0))
        action = request.POST.get('action')

        try:
            painting = paintings_Db.objects.get(id=painting_id)
            if painting.status == 'Out Of Stock':
                if action == 'cart':
                    messages.warning(request, 'The painting is out of stock')
                    return redirect('Single_page', p_id=painting_id)
            
        except paintings_Db.DoesNotExist:
            return HttpResponse("The specified painting does not exist.", status=404)

            

        if action == 'wishlist':  # Check if the action is 'wishlist'
            # Check if the product is already in the wishlist
            if WishlistDb.objects.filter(product_id=painting_id, Username=un).exists():
                messages.info(request, 'The painting is already in wishlist')
                return redirect('Single_page', p_id=painting_id)  # Redirect to the wishlist page

            # Add the product to the wishlist
            wishlist_item = WishlistDb(product_id=painting_id, Username=un)
            wishlist_item.save()
            messages.success(request, 'The painting is  added to wishlist')
            return redirect('Single_page', p_id=painting_id)  # Redirect to the wishlist page
        else:
            # Convert quantity to integer
            qty = int(qty) if qty else 0

            # Convert total price to float
            # Convert total price to float
            tp = float(tp) if tp else 0.0

            try:
                # Get the painting object based on its ID
                painting = paintings_Db.objects.get(id=painting_id)
            except paintings_Db.DoesNotExist:
                # Handle the case where the painting ID does not exist
                return HttpResponse("The specified painting does not exist.", status=404)

            # Check if the item already exists in the cart for the logged-in user
            existing_item = CartDb.objects.filter(Username=un, painting=painting).first()

            if existing_item:
                return redirect('Cart_page')

            else:
                
                obj = CartDb(Username=un, painting=painting, quantity=qty, price=pr, tprice=tp)
                obj.save()
                messages.success(request, 'The painting is  added to cart')

            return redirect('Single_page', p_id=painting_id)

    # Add a default return statement in case the method is not POST
    return HttpResponse("Invalid request method", status=405)


@transaction.atomic
def Update_cart(request):
    if request.method == "POST":
        # Create a set to keep track of product names for which quantity has been changed
        products_changed = set()

        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                cart_item_id = key.split('_')[1]
                try:
                    cart_item = CartDb.objects.get(id=cart_item_id)
                    old_quantity = cart_item.quantity  # Store old quantity
                    new_quantity = int(value)

                    if old_quantity != new_quantity:
                        # Check if the new quantity exceeds the maximum allowed quantity (e.g., 10)
                        if new_quantity > 10:  # Adjust the limit as per your requirement
                            message = f'Maximum quantity reached for this painting'
                            messages.warning(request, mark_safe(message))
                            # If the quantity exceeds the limit, set the quantity to the maximum allowed
                            new_quantity = 10  # Or any other limit you want
                            cart_item.quantity = new_quantity
                            cart_item.tprice = cart_item.price * new_quantity
                            cart_item.save()
                        else:
                            cart_item.quantity = new_quantity
                            cart_item.tprice = cart_item.price * new_quantity
                            cart_item.save()
                            # Add product name to the set if its quantity has been changed
                            products_changed.add(cart_item.painting.pname)
                except CartDb.DoesNotExist:
                    # Handle the case where the cart item does not exist
                    pass

        # Display alert message for each product whose quantity has been changed
        for product_name in products_changed:
            message = f'The quantity of painting <span class="orange-text">"{product_name}"</span> has been changed'
            messages.success(request, mark_safe(message)) # You can return a JSON response indicating success if needed
        return JsonResponse({"success": True})



def delete_cart(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        try:
            cart_item = CartDb.objects.get(id=cart_item_id)
            # Get the name of the painting before deleting it from the cart
            painting_name = cart_item.painting.pname
            cart_item.delete()
            # Add success message using Django's messages framework
            messages.success(request, f'The painting "{painting_name}" is deleted')
            return redirect('Cart_page')  # Redirect to the cart page after deletion
        except CartDb.DoesNotExist:
            messages.error(request, 'Cart item does not exist')
        return redirect('Cart_page')  # Redirect to the cart page after deletion
    else:
        # If request method is not POST, add an error message
        messages.error(request, 'Invalid request method')
        return redirect('Cart_page')  # Redirect to the cart page



@never_cache
def Checkout_page(request):
    paintings=paintings_Db.objects.all()

    artists = artist_Db.objects.all()
    user_profile = Profile.objects.filter(Username=request.session['Username'])
    username = request.session.get('Username')
    address = Address.objects.filter(Username=username)
    if username:
        active_coupons = AppliedCoupon.objects.filter(is_active=True).exists()
        applied_coupon = AppliedCoupon.objects.filter(Username=username, is_active=True).first()
        if applied_coupon:
            discounted_amount = applied_coupon.discounted_amount
            coupon_code = applied_coupon.coupon.code
            totalprice = applied_coupon.totalprice
        else:
            discounted_amount = None
            coupon_code = None
            totalprice = None
    else:
        discounted_amount = None
        coupon_code = None
        totalprice = None
    try:
        coupon = CouponDb.objects.get(status=True)
    except CouponDb.DoesNotExist:
        coupon = None

    data = CartDb.objects.filter(Username=request.session['Username'])
    total_price = 0
    for i in data:
        total_price = total_price + i.tprice

    if total_price <= 0:
        messages.warning(request, 'Your cart is empty. Please add any painting to continue. ')
        return redirect('Cart_page')  # Redirect back to the cart page if total amount exceeds the limit

    # Check if the total amount exceeds the maximum allowed amount (e.g., 50000)
    if total_price > 50000:
        messages.warning(request, 'Maximum amount should be less than 50000 in a single payment.')
        return redirect('Cart_page')  # Redirect back to the cart page if total amount exceeds the limit

    return render(request, "Check_Out.html",
                  {'data': data, 'total_price': total_price, 'totalprice': totalprice, 'active_coupons': active_coupons,
                   'coupon': coupon, 'discounted_amount': discounted_amount, 'coupon_code': coupon_code,
                   'username': username, 'address': address, 'user_profile': user_profile, "artists": artists, "paintings": paintings})


@transaction.atomic
def apply_coupon(request):
    username = request.session.get('Username')
    if username:
        data = CartDb.objects.filter(Username=username)
        if request.method == 'POST':
            coupon_code = request.POST.get('couponCode')
            try:
                # Check if the coupon exists
                coupon = CouponDb.objects.get(code=coupon_code)

                # Check if the coupon is active within the specified time range
                if not coupon.status:
                    return JsonResponse({'success': False, 'message': 'Coupon is inactive or expired'})

                # Coupon is valid, proceed to calculate discount
                total_price = sum(i.tprice for i in data)
                if total_price >= coupon.minimum_price:
                    # Check if the coupon has already been applied by the user
                    existing_coupon = AppliedCoupon.objects.filter(Username=username, coupon=coupon).first()
                    if existing_coupon:
                        return JsonResponse({'success': False, 'message': 'Coupon has already been applied'})

                    # Coupon has not been applied, proceed to apply it
                    coupon_discount = total_price * coupon.discount_decimal
                    total_price -= coupon_discount

                    # Save the applied coupon in the database
                    AppliedCoupon.objects.create(Username=username, coupon=coupon, discounted_amount=coupon_discount,
                                                 totalprice=total_price)

                    # Convert Decimal objects to float before sending as JSON
                    total_price = float(total_price)
                    coupon_discount = float(coupon_discount)

                    return JsonResponse({'success': True, 'total_price': total_price, 'discount': coupon_discount,
                                         'discount_amount': coupon_discount, 'totalprice': total_price})
                else:
                    return JsonResponse({'success': False, 'message': 'Minimum purchase amount not met'})
            except CouponDb.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Invalid coupon code'})

        return JsonResponse({'success': False, 'message': 'Invalid request'})
    else:
        return JsonResponse({'success': False, 'message': 'User not authenticated'})

def remove_active_coupon(request):
    if request.method == 'POST':
        # Get the username from the session
        username = request.session.get('Username')
        if username:
            # Delete active coupons for the user
            AppliedCoupon.objects.filter(Username=username, coupon__status=True).delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'User not authenticated'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'})


@never_cache
def payment_section(request):
    paintings=paintings_Db.objects.all()
    artists = artist_Db.objects.all()
    user_profile = Profile.objects.filter(Username=request.session['Username'])


    # Fetch user's selected address
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address_id')
        if selected_address_id:
            try:
                selected_address = Address.objects.get(id=selected_address_id)
            except Address.DoesNotExist:
                messages.warning(request, 'Selected address does not exist')
                return redirect('Checkout_page')
        else:
            messages.warning(request, 'Please select an address first')
            return redirect('Checkout_page')
    else:
        messages.error(request, 'Invalid request method')
        return redirect('Checkout_page')

    # Retrieve cart data
    data = CartDb.objects.filter(Username=request.session['Username'])
    total_price = sum(i.tprice for i in data)
    coupon_discount = 0
    total = total_price
    applied_coupon = AppliedCoupon.objects.filter(Username=request.session['Username']).first()
    if applied_coupon and applied_coupon.is_active:  # Check if coupon is active
        coupon_discount = applied_coupon.discounted_amount
        # Mark the coupon as deactivated after use
        applied_coupon.is_active = False
        applied_coupon.save()
        total -= coupon_discount
    tax = 70
    grand_total = total + tax
    if total_price <= 0:
        return redirect('Cart_page')  # Redirect back to the cart page if total amount exceeds the limit

    # Check if the total amount exceeds the maximum allowed amount (e.g., 50000)
    if total_price > 50000:
        messages.warning(request, 'Maximum amount should be less than 50000 in a single payment.')
        return redirect('Cart_page')  # Redirect back to the cart page if total amount exceeds the limit


    # Create Razorpay payment
    order_currency = 'INR'
    client = razorpay.Client(auth=('rzp_test_IzIBFTmzd3zzKk', 'mMvIdZd7a4EU1pMd9tSQEbE0'))

    payment = client.order.create({'amount': int(grand_total * 100), 'currency': "INR", 'payment_capture': '1'})

    # Get the order ID
    order_id = payment['id']

    # Render payment section template with necessary data
    return render(request, "payment_section.html", {
        "data": data,
        "payment": payment,
        "grand_total": grand_total,
        "coupon_discount": coupon_discount,
        "total_price": total_price,
        "selected_address": selected_address,
        "order_id": order_id,  # Pass the order ID to the template,
        "artists": artists,
        "user_profile": user_profile,
        "paintings": paintings
    })

@never_cache
@csrf_exempt
def place_order(request):
    if request.method == 'POST':
        # Retrieve selected address
        selected_address_id = request.POST.get('selected_address_id')
        try:
            selected_address = Address.objects.get(pk=selected_address_id)
        except Address.DoesNotExist:
            return render(request, "error_page.html", {"error_message": "Selected address does not exist"})

        applied_coupon = AppliedCoupon.objects.filter(Username=request.session['Username']).first()
        if applied_coupon and applied_coupon.is_active:  # Check if coupon is active
            applied_coupon.is_active = False
            applied_coupon.save()

        username = request.POST.get('Username')
        total_price = float(request.POST.get('total_price'))
        shipping = float(request.POST.get('shipping'))
        grand_total = float(request.POST.get('grand_total'))
        amount_to_be_paid = float(request.POST.get('amountToBePaid'))
        coupon_discount_str = request.POST.get('discount')
        coupon_discount = float(coupon_discount_str) if coupon_discount_str else 0

        payment_method = request.POST.get('payment_method')

        order_id = str(uuid.uuid4().hex)[:12]
        created_at = timezone.now().strftime("%B %d, %Y")

        order = Order.objects.create(
            Username=username,
            address=selected_address,
            total_price=total_price,
            shipping=shipping,
            grand_total=grand_total,
            discount=coupon_discount,
            amount_to_be_paid=amount_to_be_paid,
            payment_method=payment_method,
            order_id=order_id,
            order_status='Order Confirmed',
            created_at=created_at
        )
        selected_painting_name = request.POST.get('painting_name')
        quantity_purchased = request.POST.get('quantity')
        selected_painting = paintings_Db.objects.get(pname=selected_painting_name)
        new_quantity = selected_painting.no_copies - int(quantity_purchased)
        selected_painting.no_copies = new_quantity
        selected_painting.save()
        if new_quantity == 0:
                selected_painting.status = 'Out Of Stock'
                selected_painting.save()

        cart_items = CartDb.objects.filter(Username=username)

        # Add cart items to the order
        for cart_item in cart_items:
            item_total_price = cart_item.quantity * cart_item.price
            OrderItem.objects.create(
                order=order,
                picture=cart_item.painting.picture,
                pname=cart_item.painting.pname,
                quantity=cart_item.quantity,
                price=cart_item.price,
                total_price=item_total_price
            )
        

        # Clear the cart after placing the order
        cart_items.delete()
        messages.success(request, "Your order has been placed successfully!..")
        return redirect('order_confirmed', order_id=order_id)



@never_cache
def order_confirmed(request, order_id):
    order = Order.objects.get(order_id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, "order_complete.html", {"order": order, "order_items": order_items})


















def user_painting(request):
    artists=artist_Db.objects.all()
    paintings=paintings_Db.objects.all()

    data = painting_type_Db.objects.all()
    # Check if the 'Username' key exists in the session
    if 'Username' not in request.session:
        # Store the current page's URL in the session
        request.session['redirect_to'] = request.build_absolute_uri()
        # Add an info-level message
        messages.warning(request, 'You need to log in first before going to upload section.')
        # Redirect back to the current page
        return redirect(
            request.META.get('HTTP_REFERER', '/'))  # Redirect to the referrer or home page if referrer not available

    user_profile = Profile.objects.filter(Username=request.session['Username'])
    return render(request, "user_painting.html", {'user_profile': user_profile,"artists":artists,"data":data,"paintings":paintings})

def user_paintings_save(request):
    if request.method == "POST":
        z = request.POST.get("username")
        a = request.POST.get("pname")
        b = request.FILES['picture']
        c = request.POST.get("price")
        d = request.POST.get("description")
        e = request.POST.get("painting_type")
        f = request.POST.get("no_copies")
        g = request.POST.get("artist_name")
        i = request.POST.get("location")
        h = request.FILES.get('image', 'Images/usericon11.png')
        if int(c) > 10000:
            messages.warning(request, 'Allowded maximum price for a painting is 10000 .')
            return redirect(user_painting)
        if int(f) > 100:
            messages.warning(request, 'Allowded maximum copies for a painting is 100 .')
            return redirect(user_painting)


        obj = paintings_Db(username=z, pname=a, picture=b, price=c, description=d, picture_type=e, no_copies=f,location=i,
                           artist_name=g, artist_picture=h)
        obj.save()
    return redirect(user_painting)


def user_painting_edit(request,p_id):
    data = painting_type_Db.objects.all()
    artists=artist_Db.objects.all()
    paintings = paintings_Db.objects.get(id=p_id)
    paintingss = paintings_Db.objects.all()
    user_profile = Profile.objects.filter(Username=request.session['Username'])
    return render(request, "user_painting_edit.html",{"paintings":paintings,"paintingss":paintingss,"user_profile":user_profile,"artists":artists,"data":data})

def user_painting_update(request, p_id):
    if request.method == "POST":
        z = request.POST.get("username")
        a = request.POST.get("pname")
        c = request.POST.get("price")
        d = request.POST.get("location")
        e = request.POST.get("description")
        f = request.POST.get("painting_type")
        g = request.POST.get("no_copies")
        h = request.POST.get("artist_name")

        try:
            img = request.FILES['picture']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = paintings_Db.objects.get(id=p_id).picture

        try:
            artist_img = request.FILES['artist_picture']
            fs = FileSystemStorage()
            artist_file = fs.save(artist_img.name, artist_img)
        except MultiValueDictKeyError:
            artist_file = paintings_Db.objects.get(id=p_id).artist_picture

        if not h:
            h = 'Images/usericon1.png'


        paintings_Db.objects.filter(id=p_id).update(
            username=z,
            pname=a,
            picture=file,
            price=c,
            location=d,
            description=e,
            picture_type=f,
            no_copies=g,
            artist_name=h,
            artist_picture=artist_file,  # Update artist picture
        )
        if int(g) > 0:
            paintings_Db.objects.filter(id=p_id).update(status='In Stock')

        return redirect(profile_user_paintings)




def search(request):
    query = request.GET.get('query')
    try:
        item = paintings_Db.objects.get(pname__icontains=query)
        # Check if the searched product has a different id than the one found
        request_id = request.GET.get('id')
        if request_id is not None:
            if item.id != int(request_id):
                return redirect('Single_page', p_id=item.id)
        else:
            return redirect('Single_page', p_id=item.id)
        return render(request, 'Home.html')
    except paintings_Db.DoesNotExist:
        return render(request, 'Home.html')
    except ValueError:
        # Handle the case where the id parameter is not a valid integer
        raise Http404("Invalid productid")

from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import os

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)


def predict_artist(image_path):
    # Load the model
    model_path = os.path.join(settings.MEDIA_ROOT, 'ml code', 'keras_model.h5')  # Adjusted model path
    model = load_model(model_path, compile=False)

    # Load the labels
    labels_path = os.path.join(settings.MEDIA_ROOT, 'ml code', 'labels.txt')  # Adjusted labels path
    with open(labels_path, "r") as file:
        class_names = file.readlines()

    # Create the array of the right shape to feed into the keras model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Load and preprocess the image
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    # Predict using the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return class_name.strip(), confidence_score



def search_painting(request):
    paintings=paintings_Db.objects.all()
    user_profile = Profile.objects.filter(Username=request.session['Username'])
    artists = artist_Db.objects.all()
    uploaded_image_url = None
    predicted_artist = None  # Initialize predicted_artist to None
    confidence_score = None  # Initialize confidence_score to None

    if request.method == 'POST' and request.FILES.get('painting_picture'):
        painting_picture = request.FILES['painting_picture']
        file_name = painting_picture.name
        folder_name = 'ml'  # Specify the folder name where you want to save the images
        file_path = os.path.join(settings.MEDIA_ROOT, folder_name, file_name)

        # Create the folder if it doesn't exist
        os.makedirs(os.path.join(settings.MEDIA_ROOT, folder_name), exist_ok=True)

        with open(file_path, 'wb+') as destination:
            for chunk in painting_picture.chunks():
                destination.write(chunk)
        predicted_artist, confidence_score = predict_artist(file_path)
        uploaded_image_url = os.path.join(settings.MEDIA_URL, folder_name, file_name)

    return render(request, "search_painting.html", {
        "artists": artists,
        "predicted_artist": predicted_artist,
        "confidence_score": confidence_score,
        "uploaded_image_url": uploaded_image_url,
        "paintings": paintings,
        "user_profile": user_profile
    })


def learn_art(request):
    artists = artist_Db.objects.all()
    user_profile = Profile.objects.filter(Username=request.session['Username'])
    record = Artclasses_Db.objects.all()

    if 'Username' not in request.session:
        request.session['redirect_to'] = request.build_absolute_uri()
        messages.warning(request, 'You need to log in first before going to the tutorial section.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST':
        amount = request.POST.get('amount')  # Get the selected amount from the form
        # Perform necessary actions with the selected amount
        order_currency = 'INR'
        client = razorpay.Client(auth=('rzp_test_IzIBFTmzd3zzKk', 'mMvIdZd7a4EU1pMd9tSQEbE0'))
        payment = client.order.create({'amount': amount, 'currency': "INR", 'payment_capture': '1'})
        return render(request, "learn_art.html", {"payment": payment, "record": record, "artists": artists, "user_profile": user_profile})

    subscribed = Subscription_Db.objects.filter(Username=request.session.get('Username', '')).exists()
    if subscribed:
        return render(request, "learn_art.html", {"subscribed": True, "artists": artists, "user_profile": user_profile})

    return render(request, "learn_art.html", {"artists": artists, "user_profile": user_profile})


@csrf_exempt
def learn_art_save(request):
    if request.method == "POST":
        username = request.POST.get('username')
        package = request.POST.get('package')  # Get the selected package
        amount = request.POST.get(f'amount_{package.lower()}')  # Fetch amount based on the selected package
        obj = Subscription_Db(Username=username, amount=amount)
        obj.save()
        messages.success(request, 'Subscription completed successfully!')
        return redirect('learn_art')


def watercolour_painting(request):
    artists = artist_Db.objects.all()
    subscribed = Subscription_Db.objects.filter(Username=request.session.get('Username', '')).exists()
    record = Artclasses_Db.objects.filter(mainheading="Water Colour Painting").first()

    if record and subscribed:
        return render(request, "learn_watercolour_painting.html", {"record": record, "artists": artists})
    else:
        messages.warning(request, 'You need to subscribe to access this content.')
        return redirect('learn_art')
def digital_painting(request):
    artists = artist_Db.objects.all()

    subscribed = Subscription_Db.objects.filter(Username=request.session.get('Username', '')).exists()
    record = Artclasses_Db.objects.filter(mainheading="Digital Painting").first()
    if subscribed:
        return render(request, "learn_digital_painting.html",{"record":record,"artists":artists})
    else:
        messages.warning(request, 'You need to subscribe to access this content.')
        return redirect('learn_art')


def oil_painting(request):
    artists = artist_Db.objects.all()
    subscribed = Subscription_Db.objects.filter(Username=request.session.get('Username', '')).exists()
    record = Artclasses_Db.objects.filter(mainheading="Oil Painting").first()
    if subscribed:
        return render(request, "learn_oil_painting.html",{"record":record,"artists":artists})
    else:
        messages.warning(request, 'You need to subscribe to access this content.')
        return redirect('learn_art')

def encastic_painting(request):
    artists = artist_Db.objects.all()

    subscribed = Subscription_Db.objects.filter(Username=request.session.get('Username', '')).exists()
    record = Artclasses_Db.objects.filter(mainheading="Encaustic Painting").first()
    if subscribed:
        return render(request, "learn_encastic_painting.html",{"record":record,"artists":artists})
    else:
        messages.warning(request, 'You need to subscribe to access this content.')
        return redirect('learn_art')


def acrylic_painting(request):
    artists = artist_Db.objects.all()

    subscribed = Subscription_Db.objects.filter(Username=request.session.get('Username', '')).exists()
    record = Artclasses_Db.objects.filter(mainheading="Acrylic Painting").first()
    if subscribed:
        return render(request, "learn_acrylic_painting.html",{"record":record,"artists":artists})
    else:
        messages.warning(request, 'You need to subscribe to access this content.')
        return redirect('learn_art')


def mixedmedia_painting(request):
    artists = artist_Db.objects.all()

    subscribed = Subscription_Db.objects.filter(Username=request.session.get('Username', '')).exists()
    record = Artclasses_Db.objects.filter(mainheading="Mixed Media Painting").first()
    if subscribed:
        return render(request, "learn_mixedmedia_painting.html",{"record":record,"artists":artists})
    else:
        messages.warning(request, 'You need to subscribe to access this content.')
        return redirect('learn_art')




