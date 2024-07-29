from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from users.models import *
from .models import Suggestions
from django.contrib import messages

from users.forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

import json
import requests
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import uuid
from .models import Payment

from django.db.models import F, ExpressionWrapper, FloatField, Value
from django.db.models import Case, When

from django.db.models import Q

from PIL import Image
from io import BytesIO



# Create your views here.
def home(request):
    projects = Project.objects.all()[:6]
    project_data = []
    
    for project in projects:
       if project.project_target_amount > 0:
           percentage_funded = (project.amount_raised / project.project_target_amount) * 100
        #    if percentage_funded > 100:
        #        percentage_funded = 100
       else:
           percentage_funded = 0
           
       payment = Payment.objects.filter(project=project, status='success').count()
       project_data.append({
           'project': project,
           'percentage_funded': percentage_funded,
            'payment_count': payment,
       })

    
    if request.user.is_authenticated:
        liked_projects = Likes.objects.filter(user=request.user).values_list('project_id', flat=True)
    else:
        liked_projects = None

    context = {
        'projects_data': project_data,
        'liked_projects': liked_projects,
    }

    return render(request, 'CampusCrowd/home.html', context)


def all_campaigns(request):
    projects = Project.objects.all()
    project_data = []
    
    for project in projects:
       if project.project_target_amount > 0:
           percentage_funded = (project.amount_raised / project.project_target_amount) * 100
        #    if percentage_funded > 100:
        #        percentage_funded = 100
       else:
           percentage_funded = 0
           
       payment = Payment.objects.filter(project=project, status='success').count()
       project_data.append({
           'project': project,
           'percentage_funded': percentage_funded,
            'payment_count': payment,
       })

    
    if request.user.is_authenticated:
        liked_projects = Likes.objects.filter(user=request.user).values_list('project_id', flat=True)
    else:
        liked_projects = None
        
    
    context = {
        'projects_data': project_data,
        'liked_projects': liked_projects,
    }

    return render(request, 'CampusCrowd/all_campaigns.html', context)


@login_required(login_url='login')
def create_campaign(request):
    
    if request.method == "POST":
        project_title = request.POST.get('project_title')
        brief_description = request.POST.get('brief_description')
        project_target_amount = request.POST.get('project_target_amount')
        target_funding_period_in_days = request.POST.get('target_funding_period_in_days')
        about_project = request.POST.get('about_project')
        project_image = request.FILES.get('project_image')
        project_short_demo_video = request.FILES.get('project_short_demo_video')
        
        image = Image.open(project_image)
        if image.height > 200 or image.width > 200:
            size = (700, 700)
            image.thumbnail(size)
            quality = 70
            # Save the resized image to a BytesIO buffer
            image_buffer = BytesIO()
            image.save(image_buffer, format=image.format, quality=quality)
            # Save the resized image back to the request.FILES
            project_image.file = image_buffer
            project_image.size = len(image_buffer.getvalue())

        Project.objects.create(
            project_owner = request.user.profile,
            project_title = project_title,
            brief_description = brief_description,
            project_target_amount = project_target_amount,
            target_funding_period_in_days = target_funding_period_in_days,
            about_project = about_project,
            project_image = project_image,
            project_short_demo_video = project_short_demo_video,
        )
        
        messages.success(request, "You have successfully launched a new campaign with the title " + project_title + ".")
        return redirect('dashboard')


    return render(request, 'CampusCrowd/create_campaign.html')


def edit_campaign(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
       form = ProjectForm(request.POST, request.FILES, instance=project)
       if form.is_valid():
           project = form.save(commit=False)
           
           if 'project_image' in request.FILES:
               # Open the uploaded image using Pillow
               image = Image.open(request.FILES['project_image'])
               
               # Convert image to RGB if it has an alpha channel (RGBA)
               if image.mode == 'RGBA':
                   image = image.convert('RGB')
                    
               # Calculate aspect ratio and determine new dimensions
               max_width = 800
               max_height = 800
               width_ratio = max_width / image.width
               height_ratio = max_height / image.height
               new_ratio = min(width_ratio, height_ratio)
               new_width = int(image.width * new_ratio)
               new_height = int(image.height * new_ratio)
                
                # Resize the image while maintaining aspect ratio
               image = image.resize((new_width, new_height), Image.LANCZOS)
               
               # Save the image to a BytesIO buffer with the desired quality (DAVE THE CEO)
               image_buffer = BytesIO()
               image.save(image_buffer, format='JPEG', quality=80)  
               
               # Save the image to the project instance
               project.project_image.save(request.FILES['project_image'].name, image_buffer)
               
       project.save()   
       return redirect('dashboard')

    context = {
        'project': project
    }
    
    return render(request, 'CampusCrowd/create_campaign.html', context)


def campaign(request, pk):
    project = Project.objects.get(id=pk)
    payment = Payment.objects.filter(project=project, status='success').count()
    
    try:
        project_detail = ProjectDetail.objects.get(project=project)
    except:
        project_detail = None
    
    if project.project_target_amount > 0:
           percentage_funded = (project.amount_raised / project.project_target_amount) * 100
        #    if percentage_funded > 100:
        #        percentage_funded = 100
    else:
        percentage_funded = 0
    

    context = {
        'project': project,
        'payment_count': payment,
        'percentage_funded': percentage_funded,
        'project_detail': project_detail,
    }

    return render(request, 'CampusCrowd/campaign.html', context)


def perks(request, pk):
    project = Project.objects.get(id=pk)
    payments = Payment.objects.filter(project=project, status='success')
    payment_count = payments.count()
    
    if project.project_target_amount > 0:
           percentage_funded = (project.amount_raised / project.project_target_amount) * 100
        #    if percentage_funded > 100:
        #        percentage_funded = 100
    else:
        percentage_funded = 0
    
    context = {
        'project': project,
        'payments': payments,
        'payment_count': payment_count,
        'percentage_funded': percentage_funded,
    }

    return render(request, 'CampusCrowd/perks.html', context)


def updates(request, pk):
    project = Project.objects.get(id=pk)
    try:
        update = ProjectUpdate.objects.get(project=project)
    except:
        update = None
    payment = Payment.objects.filter(project=project, status='success').count()
    
    if project.project_target_amount > 0:
           percentage_funded = (project.amount_raised / project.project_target_amount) * 100
        #    if percentage_funded > 100:
        #        percentage_funded = 100
    else:
        percentage_funded = 0

    
    context = {
        'project': project,
        'payment_count': payment,
        'update': update,
        'percentage_funded': percentage_funded,
    }

    return render(request, 'CampusCrowd/updates.html', context)


@login_required(login_url='login')
def dashboard(request):
    profile = request.user.profile
    user_projects = Project.objects.filter(project_owner=profile)
    
    context = {
        'profile': profile,
        'projects': user_projects
        }

    return render(request, 'CampusCrowd/dashboard.html', context)



def about_us(request):

    return render(request, 'CampusCrowd/about_us.html')


# View function responsible for increasing the likes of a project based on ajax input request from user
def like_project(request, pk):
    project = get_object_or_404(Project, id=pk)
    user = request.user
    
    if Likes.objects.filter(user=user, project=project).exists():
        project.project_stars -= 1
        project.save()
        delete_star = Likes.objects.get(user=user, project=project)
        delete_star.delete()
        return JsonResponse({'status': 'success', 'message': 'Project usstared', 'stars': project.project_stars})
        # return JsonResponse({'status': 'error', 'message': 'You have already liked this project.'})
    
    else:
        # Create a like record
        Likes.objects.create(user=user, project=project)
        project.project_stars += 1
        project.save()
        return JsonResponse({'status': 'success', 'message': 'Project stared', 'stars': project.project_stars})


    

# PAYMENT INTEGRATION STARTS HERE------ PAYMENT WITH PAYSTACK---------
def initiate_payment(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        email = request.POST.get('email')      
        name = request.POST.get('name') if request.POST.get('name') else "Anonymous Donor"
        amount = float(request.POST.get('amount'))
        
        if request.POST.get('is_anonymous') == 'on':
            is_anonymous = True
        else:
            is_anonymous = False
        # is_anonymous = request.POST.get('is_anonymous', False)
        
        payment = Payment.objects.create(
            user=request.user if request.user.is_authenticated else None,
            project=project,
            amount=amount,
            email=email,
            payer_name=name,
            is_anonymous=is_anonymous,
            reference=str(uuid.uuid4())
        )

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        data = {
            "email": email,
            "amount": int(amount * 100),  
            "reference": payment.reference,
            "callback_url": request.build_absolute_uri(reverse('verify', args=[payment.reference]))
        }

        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, data=json.dumps(data))
        res = response.json()
        if res['status']:
            return redirect(res['data']['authorization_url'])
        else:
            payment.status = 'failed'
            payment.save()
            payments = Payment.objects.filter(project=payment.project, status='success')
            payment_count = payments.count()
            error = res['message']
            
            if payment.project.project_target_amount > 0:
                percentage_funded = (payment.project.amount_raised / payment.project.project_target_amount) * 100
                # if percentage_funded > 100:
                #     percentage_funded = 100
            else:
                 percentage_funded = 0

            context = {
                'project': payment.project,
                'payments': payments,
                'payment_count': payment_count,
                'error': error,
                'percentage_funded': percentage_funded,
            }
            return render(request, 'CampusCrowd/perks.html', context)
    return render(request, 'CampusCrowd/initiate.html', {'project': project})


#The below code is responsible for hooking into the paystack api to check the validity of the transaction
@csrf_exempt
def verify_payment(request, reference):
    payment = get_object_or_404(Payment, reference=reference)
    
    if payment.status == 'success':
        process_amount_raised = False 
    else:
        process_amount_raised = True 

    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)
    res = response.json()
    if res['status']:
        payment.status = res['data']['status']
        if res['data']['status'] == 'success':
            if process_amount_raised:
                payment.project.amount_raised += payment.amount
                payment.project.save()
        payment.save()
        
        payments = Payment.objects.filter(project=payment.project, status='success')
        payment_count = payments.count()
        
        if payment.project.project_target_amount > 0:
           percentage_funded = (payment.project.amount_raised / payment.project.project_target_amount) * 100
        #    if percentage_funded > 100:
        #        percentage_funded = 100
        else:
            percentage_funded = 0

    
        context = {
            'project': payment.project,
            'payment': payment,
            'payments': payments,
            'payment_count': payment_count,
            'percentage_funded': percentage_funded,
        }
        return render(request, 'CampusCrowd/perks.html', context)
    else:
        payment.status = 'failed'
        payment.save()
        
        payments = Payment.objects.filter(project=payment.project, status='success')
        payment_count = payments.count()
        error = res['message']
        
        
        if payment.project.project_target_amount > 0:
           percentage_funded = (payment.project.amount_raised / payment.project.project_target_amount) * 100
        #    if percentage_funded > 100:
        #        percentage_funded = 100
        else:
            percentage_funded = 0
    
        context = {
            'project': payment.project,
            'payments': payments,
            'payment_count': payment_count,
            'error': error,
            'percentage_funded': percentage_funded,
        }
        return render(request, 'CampusCrowd/perks.html', context)



# THE SORTING OF PROJECT VIEW STARTS HERE
def sort_campaigns(request, value):
    print(value)
    
    project =  Project.objects.all()[:1]
    project_data = []
    
    if value == 'Percent Funded': # When the sort value from the user is Percent funded, Get the project and calculat the percentage funded before appending it to the list  
        projects = Project.objects.annotate(
        percentage_funded=ExpressionWrapper(
            Case(
                When(project_target_amount__gt=0, then=(F('amount_raised') * 100.0) / F('project_target_amount')),
                default=Value(0),
                output_field=FloatField()
            ),
            output_field=FloatField()  # This is the required argument that was missing
        )
        ).order_by('-percentage_funded')
    elif value == 'Most Starred':
        projects = Project.objects.all().order_by('-project_stars')
    elif value == 'Least Starred':
        projects = Project.objects.all().order_by('project_stars')
    elif value == 'Oldest Project':
        projects = Project.objects.all().order_by('created')
    elif value == 'Newest Project':
       projects = Project.objects.all().order_by('-created')
    elif value == 'Most Funded':
       projects = Project.objects.all().order_by('-amount_raised')
    elif value == 'Least Funded':
      projects = Project.objects.all().order_by('amount_raised')
    else:
        projects = Project.objects.all()



        
    for project in projects:
       if project.project_target_amount > 0:
           percentage_funded = (project.amount_raised / project.project_target_amount) * 100
        #    if percentage_funded > 100:
        #        percentage_funded = 100
       else:
           percentage_funded = 0
           
       if request.user.is_authenticated:
            liked_projects = Likes.objects.filter(user=request.user).values_list('project_id', flat=True)
            if project.id in liked_projects:
                liked_project = True
                # print(True)
            else:
                liked_project = False
                # print(False)
       else:
        liked_project = None
        
       payment = Payment.objects.filter(project=project, status='success').count()    
       authenticated = request.user.is_authenticated #Dave this returns either True or False in order to make the star green on not
       
       project_data.append({
            'id': str(project.id),
            'project_title': project.project_title,
            'brief_description': project.brief_description,
            'project_image': project.project_image.url if project.project_image else None,
            'project_stars': project.project_stars,
            'project_owner_name': project.project_owner.user.first_name + " " + project.project_owner.user.last_name,
            'project_owner_program': project.project_owner.programme_of_study,
            'project_owner_Abbr': project.project_owner.abbreviation_of_institution,
            'project_owner_image': project.project_owner.profile_image.url,
            'percentage_funded': percentage_funded,
            'payment_count': payment,
            'amount_raised': project.amount_raised,
            'project_target_amount': project.project_target_amount,
            'target_funding_period_in_days': project.target_funding_period_in_days,
            'brief_description': project.brief_description,
            'authenticated':authenticated,
            'liked_project': liked_project,
            
        })
       

    # redirect_url = reverse('home')
    return JsonResponse({'project_data': project_data})
    
    
def search_projects(request):
    project_data = []

    if request.method == 'POST': #Filter project based on the impot recieved from the ajax request 
        what_to_search = request.POST.get('search')
        projects = Project.objects.filter(
            Q(project_title__icontains = what_to_search)|
            Q(brief_description__icontains = what_to_search)|
            # Q(about_project__icontains = what_to_search)|
            Q(project_owner__user__first_name__icontains = what_to_search)|
            Q(project_owner__user__last_name__icontains = what_to_search)|
            Q(project_owner__programme_of_study__icontains = what_to_search)|
            Q(project_owner__name_of_institution__icontains = what_to_search)|
            Q(project_owner__abbreviation_of_institution__icontains = what_to_search)|
            Q(project_owner__college_name__icontains = what_to_search)
            )
    
    
    for project in projects:
       if project.project_target_amount > 0:
           percentage_funded = (project.amount_raised / project.project_target_amount) * 100
        #    if percentage_funded > 100:
        #        percentage_funded = 100
       else:
           percentage_funded = 0
           
       payment = Payment.objects.filter(project=project, status='success').count()
       project_data.append({
           'project': project,
           'percentage_funded': percentage_funded,
            'payment_count': payment,
       })

    
    if request.user.is_authenticated:
        liked_projects = Likes.objects.filter(user=request.user).values_list('project_id', flat=True)
    else:
        liked_projects = None
        
    
    context = {
        'projects_data': project_data,
        'liked_projects': liked_projects,
    }
    
    return render(request, 'CampusCrowd/all_campaigns.html', context)


#This view handles the suggestion of a project 
def hints(request, pk):
    project = Project.objects.get(id=pk)
    payments = Payment.objects.filter(project=project, status='success')
    payment_count = payments.count()
    suggestions = Suggestions.objects.filter(project=project)
    
    if project.project_target_amount > 0:
           percentage_funded = (project.amount_raised / project.project_target_amount) * 100
        #    if percentage_funded > 100:
            #    percentage_funded = 100
    else:
        percentage_funded = 0
    
    context = {
        'project': project,
        'payments': payments,
        'payment_count': payment_count,
        'percentage_funded': percentage_funded,
        'suggestions': suggestions,
    }
    
    return render(request, 'CampusCrowd/hints.html', context)
