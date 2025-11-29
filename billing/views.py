from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Bill, Payment

@login_required
def bill_list(request):
    status_filter = request.GET.get('status', '')
    bills = Bill.objects.select_related('patient')
    
    if status_filter:
        bills = bills.filter(status=status_filter)
    
    return render(request, 'billing/bill_list.html', {
        'bills': bills,
        'status_choices': Bill.STATUS_CHOICES,
    })

@login_required
def bill_detail(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    items = bill.items.all()
    payments = bill.payments.all()
    return render(request, 'billing/bill_detail.html', {
        'bill': bill,
        'items': items,
        'payments': payments,
    })

@login_required
def add_payment(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)
    
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        payment_method = request.POST.get('payment_method')
        
        payment = Payment.objects.create(
            bill=bill,
            amount=amount,
            payment_method=payment_method,
            transaction_id=request.POST.get('transaction_id', '')
        )
        
        bill.paid_amount += amount
        if bill.paid_amount >= bill.total_amount:
            bill.status = 'paid'
        else:
            bill.status = 'partial'
        bill.save()
        
        messages.success(request, 'Payment recorded successfully!')
        return redirect('bill_detail', pk=bill.pk)
    
    return render(request, 'billing/add_payment.html', {'bill': bill})
