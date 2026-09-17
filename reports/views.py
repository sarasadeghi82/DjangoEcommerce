from django.shortcuts import render
from django.db.models import Sum , F
from django.utils import timezone
from datetime import timedelta
from orders.models import OrderItem
from accounts.decorators import role_required
import json
from datetime import datetime, date



def parse_date_param(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None


@role_required('admin')
def sales_report(request):

    # خواندن فیلتر بازه زمانی از URL (مثلاً ?start=2024-01-01&end=2024-01-31)
    start_date = parse_date_param(request.GET.get('start'))
    end_date = parse_date_param(request.GET.get('end')) 


    items = OrderItem.objects.all()
    # order__status__in=['processing', 'shipped', 'completed'] )

    if start_date:
        items = items.filter(order__created_at__date__gte=start_date)
    if end_date:
        items = items.filter(order__created_at__date__lte=end_date)

    #--------------------------------------------------------------------------------------------------------

    # گزارش ۱: پرفروش‌ترین محصولات (نمودار میله‌ای)   «برو تو دیتابیس، محصولات رو بر اساس اسم دسته‌بندی کن، و برای هر دسته، مجموع تعدادشون رو هم بهم بگو»
    top_products = (
        items.values('product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    )

    product_labels = [item['product__name'] for item in top_products]    #list comprehension --> list 
    product_data   = [item['total_quantity'] for item in top_products]

    #---------------------------------------------------------------------------------------------------------

    # گزارش ۲: فروش بر اساس دسته‌بندی (نمودار دایره‌ای)
    category_sales = (
        items
        .values('product__category__name')                      
        .annotate(total_sales=Sum(F('price') * F('quantity')))    # F=field  use when we want to operate between fileds 
        .order_by('-total_sales')
    ) 
    category_labels = [item['product__category__name'] or 'بدون دسته' for item in category_sales]
    category_data   = [float(item['total_sales']) for item in category_sales]

    #-----------------------------------------------------------------------------------------------------------

    # گزارش ۳: فروش بر اساس مشتری (نمودار میله‌ای)
    customer_sales = (
        items
        .values('order__user__username')
        .annotate(total_spent=Sum(F('price') * F('quantity')))
        .order_by('-total_spent')[:5]
    )
    customer_labels = [item['order__user__username'] for item in customer_sales]
    customer_data   = [float(item['total_spent']) for item in customer_sales]

    #--------------------------------------------------------------------------------------------------------------

    context = {
        'product_labels':  json.dumps(product_labels, ensure_ascii=False),
        'product_data':    json.dumps(product_data),
        'category_labels': json.dumps(category_labels, ensure_ascii=False),
        'category_data':   json.dumps(category_data),
        'customer_labels': json.dumps(customer_labels, ensure_ascii=False),
        'customer_data':   json.dumps(customer_data),
        'start_date': start_date or '',
        'end_date': end_date or '',
    }
    return render(request, 'reports/sales_report.html', context)