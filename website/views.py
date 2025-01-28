from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from accounts.models import CustomUser, Property


# Create your views here.

def home(request):
    agents = CustomUser.objects.filter(user_type='agent')

    context = {
        'agents': agents,
    }
    return render(request, 'index.html', context)

@login_required
def dashboard(request):
    properties = Property.objects.all()  # Fetch all properties
    context = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'user_type': request.user.user_type,
        'properties': properties,  # Add the properties to the context
    }
    return render(request, 'dashboard/index2.html', context)



def property(request):
    # Get all properties from the database (or modify this to get specific properties if needed)
    properties = Property.objects.all()

    # Pass the properties to the template
    context = {
        'properties': properties
    }

    return render(request, 'properties.html', context)



def property_detail(request, property_id):
    # Fetch the property by its ID or return a 404 error if not found
    property = get_object_or_404(Property, id=property_id)
    property_images = property.images.all()  # Fetch all related images

    # Pass the property, agent, and images to the context
    context = {
        'property': property,
        'agent': property.agent,
        'images': property_images
    }
    return render(request, 'property-single.html', context)


def agent_list(request):
    # Fetch all users with user_type set to 'agent'
    agents = CustomUser.objects.filter(user_type='agent')

    context = {
        'agents': agents,
    }
    return render(request, 'agents.html', context)


@login_required
def dashboard_property_detail(request, property_id):
    """
    Fetches and displays the details of a specific property for the dashboard.
    """
    # Fetch the property by its ID or return a 404 error if not found
    property = get_object_or_404(Property, id=property_id)
    
    # Context to pass to the template
    context = {
        'property': property
    }
    
    # Render the template for property details
    return render(request, 'dashboard/lease_details.html', context)