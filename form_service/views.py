import datetime
import logging
from django.shortcuts import render , redirect
from form_service.models import ModelForm
from form_service.form import UserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum
from web_app.models import User_Profile
from datetime import datetime, timedelta
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.
@login_required
def service_user(req):
    if req.method == "POST":
        date_start = req.POST.get('date_start')
        date_end = (datetime.strptime(date_start, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # ตรวจสอบว่ามีฟอร์มครบ 10 สำหรับวันที่เลือกหรือไม่
        count = ModelForm.objects.filter(date_start=date_start).count()
        if count >= 10:
            messages.error(req, "ไม่สามารถเลือกวันนี้ได้แล้ว เนื่องจากมีผู้ใช้บริการครบ 10 คนแล้ว")
            return redirect('service')
        
        # ตรวจสอบจำนวนเสื้อผ้าไม่เกิน 100 ตัวต่อวัน
        total_clothes = ModelForm.objects.filter(date_start=date_start).aggregate(total_clothes=Sum('number_clothes'))['total_clothes'] or 0
        number_clothes = int(req.POST.get('number_clothes', 0))
        if total_clothes + number_clothes > 100:
            messages.error(req, "ไม่สามารถเลือกวันนี้ได้แล้ว เนื่องจากจำนวนเสื้อผ้าเกิน 100 ตัวแล้ว")
            return redirect('service')
        
        # ตรวจสอบจำนวนตะกร้าไม่เกิน 7 ตะกร้าต่อวัน
        total_baskets = ModelForm.objects.filter(date_start=date_start).aggregate(total_baskets=Sum('number_baskets'))['total_baskets'] or 0
        number_baskets = int(req.POST.get('number_baskets', 0))
        if total_baskets + number_baskets > 7:
            messages.error(req, "ไม่สามารถเลือกวันนี้ได้แล้ว เนื่องจากจำนวนตะกร้าเกิน 7 ตะกร้าแล้ว")
            return redirect('service')
        
        user_model = ModelForm.objects.create(
            first_name=req.POST.get('first_name'),
            last_name=req.POST.get('last_name'),
            email=req.POST.get('email'),
            phone_number=req.POST.get('phone_number'),
            Laundry=req.POST.get('Laundry'),
            date_start=date_start,
            date_end=date_end,
            clothes=req.POST.get('clothes'),
            number_clothes=number_clothes,
            number_baskets=number_baskets,
            note=req.POST.get('note'),
        )
        
        user_model.save()
        return redirect('table_list')
    else:
        form = UserForm()
        # ดึงวันที่ที่มีการส่งฟอร์มครบ 15 ฟอร์ม หรือมีเสื้อผ้าเกิน 150 ตัว หรือมีตะกร้าเกิน 9 ตะกร้า
        full_dates = ModelForm.objects.values('date_start').annotate(
            count=Count('id'),
            total_clothes=Sum('number_clothes'),
            total_baskets=Sum('number_baskets')
        ).filter(count__gte=15, total_clothes__gte=150, total_baskets__gte=9).values_list('date_start', flat=True)
    return render(req, "service.html", {"form": form, "full_dates": list(full_dates)})

@login_required
def edit_service(req,id):
    
    user = ModelForm.objects.get(pk = id)
    if req.method == "POST":
        form = UserForm(req.POST,instance=user)
        if form.is_valid():

            form.save()
            return redirect("table_list")

    else:
        form = UserForm(instance=user)
    return render(req,"edit_service.html",{"form":form , "model_form":user})


logger = logging.getLogger(__name__)
@login_required
def table_list(req):
    if req.method == 'POST':
        cancel_button_value = req.POST.get('cancel_button')
        if cancel_button_value:
            try:
                order_to_cancel = ModelForm.objects.get(id=cancel_button_value)
                order_to_cancel.status = '4'
                order_to_cancel.save()
            except ModelForm.DoesNotExist:
                pass
        return redirect('table_list')

    model_form = ModelForm.objects.filter(email=req.user.email)
    model_form = model_form.exclude(status='4')

    return render(req, "table_list.html", {"model_form": model_form })

def detail(req,id):
    order = ModelForm.objects.get(pk=id)
    return render(req,'detail.html',{'order':order})
