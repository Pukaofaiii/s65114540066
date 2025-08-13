import logging
from django.shortcuts import render , redirect
from form_service.models import ORDER_CHOICE, ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from admin_app.form import UserService
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from form_service.models import ModelForm
from django.db.models import Count , Sum
from django.db.models.functions import TruncDay, TruncMonth
from collections import OrderedDict
import calendar
from django import forms
import json

# Create your views here.
@user_passes_test(lambda u: u.is_superuser)
@login_required
def admin_home(req):
    list_user = ModelForm.objects.all().order_by('date_start')
    return render(req, "admin_home.html", {"list_user": list_user})

def admin_member(req):
    list_user = ModelForm.objects.filter(membermodel__status_member=2)
    return render(req, "admin_member.html", {"list_user": list_user})




def admin_detail(req,id):
    order = ModelForm.objects.get(pk=id)
    return render(req,'admin_detail.html',{'order':order})



def update_status(req, id):
    order = ModelForm.objects.get(pk=id)
    if req.method == "POST":
        order.status = req.POST['status']
        order.save()
        return redirect("/admin_home")
    
@login_required
def user_service(req,id):
    
    user = ModelForm.objects.get(pk = id)
    if req.method == "POST":
        form = UserService(req.POST,instance=user)
        if form.is_valid():

            form.save()
            
            return redirect("admin_home")

    else:
        form = UserService(instance=user)
    return render(req,"user_service.html",{"form":form , "model_form":user})

    
def admin_delete(req ,id):
    form = ModelForm.objects.get(pk = id)
    form.delete()
    return redirect(admin_home)
        
class DateFilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

def dashboard_view(req):
    form = DateFilterForm(req.GET or None)
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        orders = ModelForm.objects.filter(date_start__gte=start_date)
        daily_orders = ModelForm.objects.filter(date_start__gte=start_date).annotate(day=TruncDay('date_start')).values('day').annotate(count=Count('id')).order_by('day')
    else:
        orders = ModelForm.objects.all()
        daily_orders = ModelForm.objects.annotate(day=TruncDay('date_start')).values('day').annotate(count=Count('id')).order_by('day')

    # จำนวนคำสั่งซักทั้งหมด
    total_orders = orders.count()

    # จำนวนเสื้อผ้าทั้งหมด
    total_clothes = orders.aggregate(total_clothes=Sum('number_clothes'))['total_clothes'] or 0

    # จำนวนตะกร้าทั้งหมด
    total_baskets = orders.aggregate(total_baskets=Sum('number_baskets'))['total_baskets'] or 0

    # จำนวนลูกค้าทั้งหมด
    total_customers = orders.values('email').distinct().count()

    # จำนวนคำสั่งซักแต่ละสถานะ
    status_data = orders.values('status').annotate(count=Count('status'))
    status_labels = [choice[1] for choice in ORDER_CHOICE]
    status_counts = [status['count'] for status in status_data]

    # จำนวนการส่งซักในแต่ละเดือน
    monthly_orders = orders.annotate(month=TruncMonth('date_start')).values('month').annotate(count=Count('id')).order_by('month')
    months = [calendar.month_name[i] for i in range(1, 13)]
    monthly_counts = OrderedDict((month, 0) for month in months)
    for order in monthly_orders:
        month_name = order['month'].strftime('%B')
        monthly_counts[month_name] = order['count']

    context = {
        'form': form,
        'total_orders': total_orders,
        'total_clothes': total_clothes,
        'total_baskets': total_baskets,
        'total_customers': total_customers,
        'status_labels': json.dumps(status_labels),
        'status_counts': json.dumps(status_counts),
        'monthly_labels': json.dumps(list(monthly_counts.keys())),
        'monthly_data': json.dumps(list(monthly_counts.values())),
        'daily_orders': daily_orders,
    }

    return render(req, 'dashboard.html', context)

def reset_date_filter(req):
    return redirect('dashboard')