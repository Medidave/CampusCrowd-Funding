from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import ProfileForm 
from .models import *
from CampusCrowd.models import Suggestions

from PIL import Image
from io import BytesIO
from django.http import JsonResponse

from django.utils.timesince import timesince


def login_view(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            # return redirect('dashboard')
            return redirect(request.GET['next'] if 'next' in request.GET else 'dashboard')
        else:
            messages.error(request, "The email address and/or password you specified are not correct.")
       
    else:
       #  Display a message if redirected due to login required
        if request.GET.get('next') == '/create-campaigns':
            messages.error(request, 'You need to login to create a campaign.')
            # print(request.GET.get('next'))     

        else:
           messages.error(request, 'You need to login to view this page.')
        #    print(request.GET.get('next'))    
        #    print("\n\n") 

       
            
            
    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    
    return render(request, 'account/login.html')


def editProfile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
       

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        if form.is_valid():
           
            if 'profile_image' in request.FILES:
                image_file = request.FILES['profile_image']
                image = Image.open(image_file)

                if image.height > 200 or image.width > 200:
                    size = (1000, 1000)
                    image.thumbnail(size)

                    quality = 85
                    # Save the resized image to a BytesIO buffer
                    image_buffer = BytesIO()
                    image.save(image_buffer, format=image.format, quality=quality)
                    # Save the resized image back to the request.FILES
                    image_file.file = image_buffer
                    image_file.size = len(image_buffer.getvalue())

            form = form.save()

            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.save()

            form.name = request.user.first_name + " " + request.user.last_name
            form.save()

            return redirect('dashboard')


    context = {
        'form': form,
        'profile': True
    }

    return render(request, 'users/profile_form.html', context)


def view_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    user_projects = Project.objects.filter(project_owner=profile)
    
    context = {
        'profile': profile,
        'projects': user_projects
        }
    
    return render(request, 'CampusCrowd/dashboard.html', context)


#The view that handles the creation of project
def createProject(request, pk):
    project = Project.objects.get(id=pk)
    
    
    if request.method == "POST":
        title = request.POST.get('title')
        update = request.POST.get('update')
        number = request.POST.get('number')
        
        ProjectUpdate.objects.create(
            project=project,
            title=title,
            update=update,
            update_number=number
        )
        project.has_update = True
        project.save()
        return redirect('updates', pk=pk)

    
    return render(request, 'users/project_update.html')


#Handles project update 
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    project_to_update = ProjectUpdate.objects.get(project=project)
    
    if request.method == "POST":
        title = request.POST.get('title')
        update = request.POST.get('update')
        number = request.POST.get('number')
        
        project_to_update.title = title
        project_to_update.update = update
        project_to_update.update_number = number
        project_to_update.save()
        
        return redirect('updates', pk=pk)
    
    context = {
        'project_to_update': project_to_update
    }
    
    return render(request, 'users/project_update.html', context)


def createProjectDetail(request, pk):
    project = Project.objects.get(id=pk)
    
    
    if request.method == "POST":
        problem_statment = request.POST.get('problem_statment')
        proposed_solution = request.POST.get('proposed_solution')
        market = request.POST.get('market')
        competition = request.POST.get('competition')
        Why_you = request.POST.get('Why_you')
        financing = request.POST.get('financing')

        
        ProjectDetail.objects.create(
            project = project,
            problem_statment = problem_statment,
            proposed_solution = proposed_solution,
            market = market,
            competition = competition,
            Why_you = Why_you,
            financing = financing,
        )
        project.has_details = True
        project.save()
        return redirect('campaign', pk=pk)

    context = {
        'project_detail': 'project_detail'
    }
    
    return render(request, 'users/project_update.html', context)


def updateProjectDetail(request, pk):
    project = Project.objects.get(id=pk)
    project_detail_to_update = ProjectDetail.objects.get(project=project)
    
    if request.method == "POST":
        problem_statment = request.POST.get('problem_statment')
        proposed_solution = request.POST.get('proposed_solution')
        market = request.POST.get('market')
        competition = request.POST.get('competition')
        Why_you = request.POST.get('Why_you')
        financing = request.POST.get('financing')

        
        project_detail_to_update.problem_statment = problem_statment
        project_detail_to_update.proposed_solution = proposed_solution
        project_detail_to_update.market = market
        project_detail_to_update.competition = competition
        project_detail_to_update.Why_you = Why_you
        project_detail_to_update.financing = financing
        project_detail_to_update.save()
        
        return redirect('campaign', pk=pk)
    
    context = {
        'project_to_update': project_detail_to_update,
        'project_detail': 'project_detail',
    }
    
    return render(request, 'users/project_update.html', context)



def send_mail(request, pk):
    print(pk)
    print("This is Dave the ceo\n\n")
    
    return JsonResponse({'status': 'success'})
    # return JsonResponse({'project_data': 'project_data'})
    
    
#Handle the creation of suggestions throgh the ajax call
def suggestions(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user if request.user.is_authenticated else None
    content = request.POST.get('content')
    
    if content:
        suggestions_list = []

        Suggestions.objects.create(
            user=user,
            project=project,
            content=content,
        )

        suggestions = Suggestions.objects.filter(project=project)

        for suggestion in suggestions:
            suggestions_list.append(
               {
                "first_name": suggestion.user.first_name if suggestion.user else "Anonymous",
                "last_name": suggestion.user.last_name if suggestion.user else "",
                'user_image': suggestion.user.profile.profile_image.url if suggestion.user else 'https://epsu-knust-s3-bucket.s3.eu-north-1.amazonaws.com/profiles/user-default.png',
                "content": suggestion.content,
                "timestamp": timesince(suggestion.created_at) + " ago",
               }

            )
        

        return JsonResponse({'status': 'success', 'suggestions': suggestions_list})
    return JsonResponse({'status': 'fail'})

