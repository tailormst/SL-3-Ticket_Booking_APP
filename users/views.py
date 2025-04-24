from django.views.generic import View, DetailView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile

class RegisterView(View):
    template_name = 'users/register.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        errors = {}
        
        # Validate inputs
        if not username:
            errors['username'] = 'Username is required'
        elif User.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists'
        
        if not email:
            errors['email'] = 'Email is required'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'Email already exists'
        
        if not password:
            errors['password'] = 'Password is required'
        elif len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        
        if not password2:
            errors['password2'] = 'Please confirm your password'
        elif password != password2:
            errors['password2'] = 'Passwords do not match'
        
        # If there are validation errors, return them
        if errors:
            return render(request, self.template_name, {
                'errors': errors,
                'username': username,
                'email': email
            })
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully. You can now log in.')
        return redirect('users:login')

class LoginView(View):
    template_name = 'users/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        errors = {}
        
        # Validate inputs
        if not username:
            errors['username'] = 'Username is required'
        
        if not password:
            errors['password'] = 'Password is required'
        
        # If there are validation errors, return them
        if errors:
            return render(request, self.template_name, {
                'errors': errors,
                'username': username
            })
        
        # Attempt authentication
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            messages.success(request, f'Welcome back, {username}!')
            return redirect(next_url)
        else:
            errors['login'] = 'Invalid username or password'
            return render(request, self.template_name, {
                'errors': errors,
                'username': username
            })

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully')
        return redirect('home')

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user_profile'
    
    def get_object(self):
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'users/profile_update.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        user = request.user
        
        # Update user information
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        # Update or create profile
        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.address = request.POST.get('address', profile.address)
        profile.save()
        
        messages.success(request, 'Profile updated successfully')
        return redirect('users:profile')