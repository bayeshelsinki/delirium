from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Bar, Team, DrinkLog, Profile, Status
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Profile
from django.db.models import Sum
from django.contrib import messages  # Import messages


def landing_page(request):
    return render(request, 'crawl/landing_page.html')

@login_required
def log_drink(request):
    if request.method == 'POST':
        bar = Bar.objects.get(id=request.POST['bar'])
        portions = int(request.POST['portions'])
        DrinkLog.objects.create(user=request.user, bar=bar, portions=portions)
        return redirect('dashboard')
    bars = Bar.objects.all()
    return render(request, 'crawl/log_drink.html', {'bars': bars})

@login_required
def delete_drink(request, drink_id):
    drink_log = get_object_or_404(DrinkLog, id=drink_id)
    
    # Check if the logged-in user owns the drink log
    if drink_log.user == request.user:
        drink_log.delete()
    
    return redirect('feed')  # Redirect back to the feed page after deletion

@login_required
def feed(request):
    # Fetch both drink logs and statuses
    drink_logs = DrinkLog.objects.select_related('user', 'bar').order_by('-timestamp')
    statuses = Status.objects.select_related('user').order_by('-created_at')

    # Combine them into a single list, ensuring the statuses and logs are ordered by time
    feed_items = list(drink_logs) + list(statuses)
    feed_items.sort(key=lambda x: x.timestamp if hasattr(x, 'timestamp') else x.created_at, reverse=True)

    return render(request, 'crawl/feed.html', {'feed_items': feed_items})

@login_required
def profile(request):
    if request.method == 'POST':
        new_team_name = request.POST.get('new_team').strip()
        team_name = request.POST.get('team').strip()
        selected_name = request.POST.get('name').strip()
        
        profile = request.user.profile

        # Handle team selection or creation
        if new_team_name:
            team, created = Team.objects.get_or_create(name=new_team_name)
            profile.team = team
        elif team_name:
            try:
                team = Team.objects.get(name=team_name)
                profile.team = team
            except Team.DoesNotExist:
                profile.team = None

        # Handle display name input
        if selected_name:
            profile.display_name = selected_name
        
        profile.save()

        # Set a success message
        messages.success(request, 'Profile updated successfully!')
        
        # Redirect to the same page to avoid resubmission
        return redirect('profile')

    teams = Team.objects.all()

    return render(request, 'crawl/profile.html', {
        'teams': teams,
    })

@login_required
def dashboard(request):
    # Total drinks by each individual user, excluding superuser
    user_drinks = (
        DrinkLog.objects
        .filter(user__is_superuser=False)
        .values('user__profile__display_name', 'user__profile__team__name')
        .annotate(total_drinks=Sum('portions'))
        .order_by('-total_drinks')
    )

    # Add ranks to the user_drinks queryset
    user_drinks = list(user_drinks)  # Convert to list to add ranks

    # Rank the users based on total drinks
    for rank, item in enumerate(user_drinks, start=1):
        item['rank'] = rank

    # Total drinks by each team, excluding teams where all members are superusers
    team_drinks = (
        DrinkLog.objects
        .filter(user__is_superuser=False)
        .values('user__profile__team__name')
        .annotate(total_drinks=Sum('portions'))
        .order_by('-total_drinks')
    )

    # Total drinks in each bar, excluding drinks logged by superusers
    bar_drinks = (
        DrinkLog.objects
        .filter(user__is_superuser=False)
        .values('bar__name')
        .annotate(total_drinks=Sum('portions'))
        .order_by('-total_drinks')
    )

    return render(request, 'crawl/dashboard.html', {
        'user_drinks': user_drinks,
        'team_drinks': team_drinks,
        'bar_drinks': bar_drinks
    })

@login_required
def admin_view(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            DrinkLog.objects.filter(id=request.POST['drink_id']).delete()
        drinks = DrinkLog.objects.all()
        return render(request, 'crawl/admin_view.html', {'drinks': drinks})
    return redirect('dashboard')

def qr_login(request, token):
    profile = get_object_or_404(Profile, token=token)
    user = profile.user
    login(request, user)
    return redirect('dashboard')  # Redirect to the dashboard after login

@login_required
def post_status(request):
    if request.method == 'POST':
        content = request.POST.get('status')
        if content:
            Status.objects.create(user=request.user, content=content)
        return redirect('feed')
    return render(request, 'crawl/feed.html')  # You may want to return a template or handle GET request here

@login_required
def delete_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)
    if status.user == request.user:
        status.delete()
    return redirect('feed')

from django.http import JsonResponse

@login_required
def map(request):
    # Fetch all bars with their latitude and longitude
    bars = Bar.objects.all()
    
    # Serialize data
    bars_data = list(bars.values('name', 'latitude', 'longitude'))
    
    # Render template with JSON data
    return render(request, 'crawl/map.html', {'bars_data': bars_data})


from django.shortcuts import render

def custom_404(request, exception):
    return render(request, 'crawl/404.html', status=404)