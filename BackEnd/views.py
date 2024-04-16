from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from FrontEnd.views import *
from BackEnd.models import *
from FrontEnd.models import *
from django.views.decorators.cache import never_cache
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_POST



# Create your views here.
@never_cache
def index_page(request):
    return render(request, "index.html")


def paintings_form(request):
    data = painting_type_Db.objects.all()
    return render(request, "paintings_form.html", {"data": data})

def paintings_save(request):
    if request.method == "POST":
        z = request.POST.get("username")
        a = request.POST.get("pname")
        b = request.FILES['picture']
        c = request.POST.get("price")
        d = request.POST.get("location")
        e = request.POST.get("description")
        f = request.POST.get("painting_type")
        g = request.POST.get("no_copies")
        h = request.POST.get("artist_name")
        i = request.FILES.get('image', 'Images/usericon11.png')

        obj = paintings_Db(username=z, pname=a, picture=b, price=c, location=d, description=e, picture_type=f,
                           no_copies=g, artist_name=h,artist_picture=i)
        obj.save()
    return redirect(paintings_form)

def paintings_table(request):
    data = paintings_Db.objects.all()
    return render(request, "paintings_table.html", {"data": data})

def paintings_edit(req,p_id):
    painting = paintings_Db.objects.get(id=p_id)
    data = painting_type_Db.objects.all()
    return render(req,"paintings_edit.html",{"data":data,"painting":painting})

def paintings_update(request, p_id):
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
            
        return redirect(paintings_table)

def paintings_delete(req,p_id):
    data=paintings_Db.objects.get(id=p_id)
    data.delete()
    return redirect(paintings_table)


def paintings_type_form(request):
    return render(request, "paintings_type_form.html")

def paintings_type_save(request):
    if request.method == "POST":
        a = request.POST.get("painting_type")
        obj = painting_type_Db(type=a)
        obj.save()
    return redirect(paintings_type_form)

def paintings_type_table(request):
    data = painting_type_Db.objects.all()
    return render(request, "paintings_type_table.html", {"data": data})

def paintings_type_delete(req,p_id):
    data=painting_type_Db.objects.get(id=p_id)
    data.delete()
    return redirect(paintings_type_table)


def artist_form(request):
    return render(request, "artist_form.html")

def artist_save(request):
    if request.method=="POST":
        b = request.POST.get("name")
        a = request.POST.get("link")
        d = request.POST.get("year")
        c = request.FILES['picture']
        obj = artist_Db(name=b,link=a, picture=c,year=d)
        obj.save()
        return redirect(artist_form)


def artist_table(request):
    data = artist_Db.objects.all()
    return render(request, "artist_table.html", {"data": data})


def artist_edit(req,a_id):
    artist = artist_Db.objects.get(id=a_id)
    data = artist_Db.objects.all()
    return render(req,"artist_edit.html",{"data":data,"artist":artist})

def artist_update(request, a_id):
    if request.method == "POST":
        b = request.POST.get("name")
        a = request.POST.get("link")
        c = request.POST.get("year")

        try:
            img = request.FILES['picture']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = artist_Db.objects.get(id=a_id).picture


        artist_Db.objects.filter(id=a_id).update(
            name=b,
            link=a,
            picture=file,
            year=c,

        )
        return redirect(artist_table)

def artist_delete(req,a_id):
    data=artist_Db.objects.get(id=a_id)
    data.delete()
    return redirect(artist_table)




def contact_save(request):
    if request.method=="POST":
        b = request.POST.get("username")
        c = request.POST.get("name")
        d = request.POST.get("email")
        e = request.POST.get("phone")
        f = request.POST.get("subject")
        g = request.POST.get("message")
        obj = contact_Db(username=b, name=c,email=d,phone=e,subject=f,message=g)
        obj.save()
        messages.success(request, 'Your message has been sended sucessfully.')
        return redirect(Contact_page)

def contact_table(request):
    data = contact_Db.objects.all()
    return render(request, "contact_table.html", {"data": data})

def contact_delete(req,c_id):
    data=contact_Db.objects.get(id=c_id)
    data.delete()
    return redirect(contact_table)

def Coupon(request):
    return render(request,"add_coupon.html")


def save_coupon(request):
    if request.method == "POST":
        cd = request.POST.get('code')
        min = request.POST.get('min_price')
        dis = request.POST.get('discount')
        v_from = request.POST.get('valid_from')
        v_to = request.POST.get('valid_to')
        status_str = request.POST.get('status', '').lower()
        status = status_str == 'true'
        if status:
            CouponDb.objects.exclude(code=cd).update(status=False)
        obj = CouponDb(code=cd, minimum_price=min, discount_percentage=dis, valid_from=v_from, valid_to=v_to,
                       status=status)
        obj.save()
        return redirect(Coupon)


def display_coupon(request):
    data = CouponDb.objects.all()
    return render(request, "view_coupon.html", {'data': data})


def edit_coupon(request, c_id):
    data = CouponDb.objects.get(id=c_id)
    return render(request, "Edit_coupon.html", {'data': data})


def update_coupon(request, c_id):
    if request.method == "POST":
        cd = request.POST.get('code')
        min = request.POST.get('min_price')
        dis = request.POST.get('discount')
        v_from = request.POST.get('valid_from')
        v_to = request.POST.get('valid_to')
        CouponDb.objects.filter(id=c_id).update(code=cd, minimum_price=min, discount_percentage=dis, valid_from=v_from,
                                                valid_to=v_to)
        return redirect(display_coupon)


def delete_coupon(req, c_id):
    data = CouponDb.objects.get(id=c_id)
    data.delete()
    return redirect(display_coupon)


@require_POST
def deactivate_coupon(request):
    try:
        active_coupon = CouponDb.objects.get(status=True)
        active_coupon.status = False
        active_coupon.save()
        return JsonResponse({'success': True, 'message': 'Active coupon deactivated successfully'})
    except CouponDb.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'No active coupon found'})


@require_POST
def activate_coupon(request):
    coupon_id = request.POST.get('coupon_id')
    try:
        # Deactivate all other active coupons
        CouponDb.objects.exclude(id=coupon_id).update(status=False)

        # Activate the selected coupon
        selected_coupon = CouponDb.objects.get(id=coupon_id)
        selected_coupon.status = True
        selected_coupon.save()

        return JsonResponse({'success': True, 'message': 'Coupon activated successfully'})
    except CouponDb.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Selected coupon does not exist'})


def check_coupon_status(request):
    if request.method == 'POST':
        # Get the coupon ID from the POST data
        coupon_id = request.POST.get('coupon_id')
        if coupon_id:
            # Query the database to get the coupon object
            coupon = get_object_or_404(CouponDb, pk=coupon_id)
            # Check the status of the coupon
            if coupon.status:
                # Coupon is active
                return JsonResponse({'active': True})
            else:
                # Coupon is inactive
                return JsonResponse({'active': False})
        else:
            return JsonResponse({'error': 'Coupon ID not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)







def user_orders(request):
    users = SignUp_Db.objects.all()
    return render(request, "user_orders.html", {"users": users})

from django.shortcuts import render, get_object_or_404

def order_details(request, username):
    user = get_object_or_404(SignUp_Db, Username=username)
    orders = Order.objects.filter(Username=username, is_deleted=False)
    return render(request, "order_status.html", {"user": user, "orders": orders})




def learning_art_form(request):
    return render(request, "learning_art_form.html")


def learning_art_save(request):
    if request.method == "POST":
        mimage = request.FILES['mainimage']
        mheading = request.POST.get("mainheading")
        img1 = request.FILES['image1']
        link1 = request.POST.get("link1")
        sub1 = request.POST.get("subheading1")
        des1 = request.POST.get("description1")
        img2 = request.FILES['image2']
        link2 = request.POST.get("link2")
        sub2 = request.POST.get("subheading2")
        des2 = request.POST.get("description2")
        img3 = request.FILES['image3']
        link3 = request.POST.get("link3")
        sub3 = request.POST.get("subheading3")
        des3 = request.POST.get("description3")
        img4 = request.FILES['image4']
        link4 = request.POST.get("link4")
        sub4 = request.POST.get("subheading4")
        des4 = request.POST.get("description4")
        img5 = request.FILES['image5']
        link5 = request.POST.get("link5")
        sub5 = request.POST.get("subheading5")
        des5 = request.POST.get("description5")


        obj = Artclasses_Db(mainimage=mimage,mainheading=mheading,image1=img1,link1=link1,subheading1=sub1,description1=des1,image2=img2,link2=link2,subheading2=sub2,description2=des2,image3=img3,link3=link3,subheading3=sub3,description3=des3,image4=img4,link4=link4,subheading4=sub4,description4=des4,image5=img5,link5=link5,subheading5=sub5,description5=des5)
        obj.save()
    return redirect(learning_art_form)

def paintings_table(request):
    data = paintings_Db.objects.all()
    return render(request, "paintings_table.html", {"data": data})