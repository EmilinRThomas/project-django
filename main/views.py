from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.admin.views.decorators import staff_member_required
from .models import Package 

# Create your views here.

#Home

def home(request):
    packages = Package.objects.filter(approved=True)  # Only show approved ones
    return render(request, 'main/index.html', {'packages': packages})

def index(request):
    packages = Package.objects.filter(approved=True,expiry_date__gte=timezone.now().date())
    return render(request, 'main/index.html', {'packages': packages})

#package

def package_list(request):
    packages = Package.objects.filter(approved=True)
    return render(request, 'main/packages.html', {'packages': packages})

def package_detail(request, pk):
    package = get_object_or_404(Package, pk=pk)
    return render(request, 'main/package_detail.html', {'package': package})

@login_required
def book_package(request, pk):
    package = get_object_or_404(Package, pk=pk)
    Booking.objects.create(user=request.user, package=package, booked_at=timezone.date())
    return redirect('home')

@login_required
def create_package(request):
    if not hasattr(request.user, 'vendor'):
        return redirect('home')

    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.vendor = request.user.vendor
            package.approved = False
            package.save()
            return redirect('vendor_dashboard')
    else:
        form = PackageForm()
    return render(request, 'main/package_form.html', {'form': form, 'action': 'Create'})

@login_required
def edit_package(request, pk):
    package = get_object_or_404(Package, pk=pk, vendor=request.user.vendor)
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    else:
        form = PackageForm(instance=package)
    return render(request, 'main/package_form.html', {'form': form, 'action': 'Edit'})

@login_required
def delete_package(request, pk):
    package = get_object_or_404(Package, pk=pk, vendor=request.user.vendor)
    if request.method == 'POST':
        package.delete()
        return redirect('vendor_dashboard')
    return redirect('vendor_dashboard')

#register

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.role == 'vendor':
                Vendor.objects.create(user=user, company_name=f"{user.username} Co")
            return redirect('login')
        
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})


#Login

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            elif user.role == 'vendor':
                return redirect('vendor_dashboard')
            elif user.role == 'user':
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

#Logout

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def redirect_dashboard(request):
    user = request.user
    if user.is_superuser:
        return redirect('/admin/')
    elif user.is_staff:
        return redirect('vendor_dashboard')
    else:
        return redirect('home')

def custom_logout(request):
    logout(request)
    return redirect('home')

#Dashboards

@login_required
def vendor_dashboard(request):
    if not hasattr(request.user, 'vendor'):
        return redirect('home')

    vendor = request.user.vendor
    packages = Package.objects.filter(vendor=vendor)
    bookings = Booking.objects.filter(package__vendor=vendor)
    return render(request, 'main/vendor_dashboard.html', {
        'packages': packages,
        'bookings': bookings
    })

@login_required
def dashboard_view(request):
    if request.user.role == 'admin':
        return redirect('/admin/')
    elif request.user.role == 'vendor':
        return redirect('vendor_dashboard')
    else:
        return redirect('home')

@staff_member_required
def admin_dashboard(request):
    users = CustomUser.objects.filter(role='user')
    vendors = CustomUser.objects.filter(role='vendor')
    packages = Package.objects.all()
    return render(request, 'main/admin_dashboard.html', {
        'users': users,
        'vendors': vendors,
        'packages': packages,
    })

#Admin- Approve, Reject

@staff_member_required
def approve_package(request, pk):
    package = get_object_or_404(Package, pk=pk)
    package.approved = True
    package.save()
    return redirect('admin_dashboard')

@staff_member_required
def reject_package(request, pk):
    package = get_object_or_404(Package, pk=pk)
    package.approved = False
    package.save()
    return redirect('admin_dashboard')

