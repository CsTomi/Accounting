from django.shortcuts import render

def accounting_proba(request):
    return render(request, 'circle/bills.html', {})