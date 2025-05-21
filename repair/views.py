from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login
from .forms import RepairRequestForm
from django.contrib.auth.decorators import login_required
from .models import RepairRequest
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('send')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def send_request_view(request):
    if request.method == 'POST':
        form = RepairRequestForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('my_requests')
    else:
        form = RepairRequestForm()
    return render(request, 'send_request.html', {'form': form})




@login_required
def my_requests_view(request):
    my_requests = RepairRequest.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'my_requests.html', {'requests': my_requests})



@login_required
def admin_panel_view(request):
    if request.user.username != 'admin':
        return render(request, 'no_access.html')

    if request.method == 'POST':
        req_id = request.POST.get('req_id')
        new_status = request.POST.get('new_status')
        request_obj = get_object_or_404(RepairRequest, id=req_id)
        if request_obj.status == 'new':
            request_obj.status = new_status
            request_obj.save()

    all_requests = (
        list(RepairRequest.objects.filter(status='new')) +
        list(RepairRequest.objects.filter(status='confirmed')) +
        list(RepairRequest.objects.filter(status='rejected'))
    )

    return render(request, 'admin_panel.html', {'requests': all_requests})