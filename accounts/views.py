from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from .forms import LeasePropertyForm, PropertySearchForm, SignUpForm
from paystackapi.paystack import Paystack
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
from .models import CustomUser, Property
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from web3 import Web3
from django.db.models import Q 
from .forms import ProfileUpdateForm, PasswordUpdateForm



# Connect to Ethereum node
ganache_url = "http://127.0.0.1:9545"  # Default Ganache URL
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Load the smart contract
contract_address = "0xb28FA2b2Ca603fbf2ddE1Da58B04db913d7587e7"
contract_abi = [
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "propertyId",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "address",
          "name": "renter",
          "type": "address"
        }
      ],
      "name": "PropertyRented",
      "type": "event"
    },
    {
      "inputs": [],
      "name": "owner",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "properties",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "id",
          "type": "uint256"
        },
        {
          "internalType": "address payable",
          "name": "agent",
          "type": "address"
        },
        {
          "internalType": "string",
          "name": "title",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "location",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "price",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "isRented",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "id",
          "type": "uint256"
        },
        {
          "internalType": "address payable",
          "name": "agent",
          "type": "address"
        },
        {
          "internalType": "string",
          "name": "title",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "location",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "price",
          "type": "uint256"
        }
      ],
      "name": "addProperty",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "propertyId",
          "type": "uint256"
        }
      ],
      "name": "rentProperty",
      "outputs": [],
      "stateMutability": "payable",
      "type": "function",
      "payable": True
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "propertyId",
          "type": "uint256"
        }
      ],
      "name": "getProperty",
      "outputs": [
        {
          "internalType": "address",
          "name": "agent",
          "type": "address"
        },
        {
          "internalType": "string",
          "name": "title",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "location",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "price",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "isRented",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    }
]  # Replace with your contract's ABI
contract = web3.eth.contract(address=contract_address, abi=contract_abi)




def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            login(request, user)  # Log the user in immediately after signing up
            messages.success(request, "You have successfully signed up and logged in!")
            return redirect('home')  # Redirect to home or dashboard
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to the home page after successful login
            else:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Invalid form data")

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Your profile has been updated successfully!")
                return redirect('profile')
        elif 'change_password' in request.POST:
            password_form = PasswordUpdateForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important for keeping the user logged in
                messages.success(request, "Your password has been updated successfully!")
                return redirect('profile')
    else:
        profile_form = ProfileUpdateForm(instance=user)
        password_form = PasswordUpdateForm(user)

    context = {
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'dashboard/profile.html', context)



# @login_required
# def lease_property(request):
#     # Check if the logged-in user is an agent
#     if not request.user.is_agent:
#         return redirect('dashboard')  # Redirect non-agents to an unauthorized page

#     if request.method == 'POST':
#         form = LeasePropertyForm(request.POST, request.FILES)
#         if form.is_valid():
#             property = form.save(commit=False)
#             property.agent = request.user  # Assign the logged-in user as the agent for the property
#             property.save()
#             return redirect('dashboard')  # Redirect to the property list or dashboard
#     else:
#         form = LeasePropertyForm()

#     context = {'form': form}
#     return render(request, 'dashboard/lease_property.html', context)


@login_required
def lease_property(request):
    if not request.user.is_agent:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LeasePropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.agent = request.user
            property.save()

            # Add property to the smart contract
            property_id = property.id  # Use Django's auto-generated ID
            agent_address = request.user.eth_address  # Ensure this field exists and is valid
            if not agent_address:
                return HttpResponse("Error: Agent does not have an Ethereum address set.")

            title = property.title
            location = property.location
            price = Web3.to_wei(property.price, 'ether')  # Convert price to Wei

            # Call the smart contract's addProperty function
            try:
                tx = contract.functions.addProperty(
                    property_id,
                    Web3.to_checksum_address(agent_address),
                    title,
                    location,
                    price
                ).transact({
                    'from': Web3.to_checksum_address(agent_address),  # Ensure address is valid
                    'gas': 2000000  # Adjust gas if necessary
                })

                # Wait for the transaction receipt
                receipt = web3.eth.wait_for_transaction_receipt(tx)

            except ValueError as e:
                return HttpResponse(f"Error during transaction: {str(e)}")

            return redirect('dashboard')
    else:
        form = LeasePropertyForm()

    context = {'form': form}
    return render(request, 'dashboard/lease_property.html', context)


@login_required
def rent_property(request, property_id):
    try:
        print(f"Contract Address: {contract_address}")  # Debug contract address
        print(f"Property ID: {property_id}")  # Debug property ID

        # Check if contract is deployed
        contract_code = web3.eth.get_code(contract_address)
        if contract_code == b'0x':
            print("Contract not deployed at this address!")
            return HttpResponse("Smart contract not deployed correctly.", status=500)

        # Fetch property details from the contract
        property_details = contract.functions.getProperty(property_id).call()
        print(f"Property Details: {property_details}")  # Debug response
    except Exception as e:
        print(f"Error calling smart contract: {e}")
        return HttpResponse("Error interacting with the smart contract.", status=500)

    # Check if property is already rented
    is_rented = property_details[4]  # isRented field
    if is_rented:
        return redirect('property_detail', property_id=property_id)

    # Redirect to payment page
    return render(request, 'dashboard/payment.html', {
        'property': get_object_or_404(Property, id=property_id),
        'contract_address': contract_address,
        'price_eth': web3.from_wei(property_details[3], 'ether')  # Price in ETH
    })



@login_required
def rent_success(request):
    property_id = request.GET.get('property_id')
    if property_id:
        property = Property.objects.get(id=property_id)
        property.is_rented = True
        property.save()
    return render(request, 'rent_success.html')



def property_list(request):
    form = PropertySearchForm(request.GET)
    properties = Property.objects.all()  # Start with all properties

    if form.is_valid():
        # Create a Q object to combine filters with AND conditions
        filters = Q()

        # Apply filters based on form inputs
        if form.cleaned_data['beds']:
            filters &= Q(beds=form.cleaned_data['beds'])  # AND condition for beds
        if form.cleaned_data['bath']:
            filters &= Q(bath=form.cleaned_data['bath'])  # AND condition for bath
        if form.cleaned_data['area']:
            filters &= Q(area__gte=form.cleaned_data['area'])  # AND condition for area
        if form.cleaned_data['location']:
            filters &= Q(location__icontains=form.cleaned_data['location'])  # Case-insensitive location search
        if form.cleaned_data['min_price']:
            filters &= Q(price__gte=form.cleaned_data['min_price'])  # Minimum price
        if form.cleaned_data['max_price']:
            filters &= Q(price__lte=form.cleaned_data['max_price'])  # Maximum price
        if form.cleaned_data['garage']:
            filters &= Q(garage=form.cleaned_data['garage'])  # AND condition for garage

        # Apply the combined filters
        properties = properties.filter(filters)

    # Render the results on the same page
    return render(request, 'property_list.html', {'properties': properties, 'form': form})


def get_eth_to_ngn_conversion_rate():
    # Fetch the conversion rate from an external API (e.g., CoinGecko)
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
    if response.status_code == 200:
        data = response.json()
        eth_to_usd = data.get('ethereum', {}).get('usd', 0)
        
        # Convert USD to NGN (you can use a fixed exchange rate or fetch it from another API)
        usd_to_ngn = 800  # Example exchange rate for USD to NGN
        eth_to_ngn = eth_to_usd * usd_to_ngn
        return eth_to_ngn
    return 0  # In case of error, return 0



@csrf_exempt
def paystack_callback(request):
    if request.method == "POST":
        # Get the Paystack reference from the request
        payment_reference = request.POST.get("reference")
        
        # Check if we have a reference and verify the payment
        if not payment_reference:
            return JsonResponse({"status": "failed", "message": "Reference not provided"}, status=400)
        
        # Set up Paystack API
        paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)
        
        # Verify the payment using the Paystack verify API
        verification = paystack.transaction.verify(reference=payment_reference)
        
        # Check if the payment verification was successful
        if verification['status'] and verification['data']['status'] == "success":
            # Get the property ID from session (assuming it's been saved there during payment initiation)
            property_id = request.session.get('property_id')
            
            if not property_id:
                return JsonResponse({"status": "failed", "message": "Property ID not found in session"}, status=400)
            
            # Retrieve the property and update the rental status
            rental_property = get_object_or_404(Property, id=property_id)
            rental_property.is_rented = True  # Mark property as rented
            rental_property.save()

            # Optionally: Add any other logic (e.g., send email confirmation)
            return JsonResponse({"status": "success", "message": "Payment successful"})
        
        # If the payment verification fails
        return JsonResponse({"status": "failed", "message": "Payment failed"}, status=400)

    # In case of invalid request type
    return JsonResponse({"status": "failed", "message": "Invalid request"}, status=400)



def paystack_payment(request, property_id):
    property_obj = Property.objects.get(id=property_id)

    if request.method == "POST":
        # Get the ETH to NGN conversion rate
        eth_to_ngn = get_eth_to_ngn_conversion_rate()
        
        if eth_to_ngn == 0:
            # Handle conversion failure, maybe notify the user
            return render(request, 'error.html', {'message': 'Unable to fetch conversion rate.'})
        
        # Convert the ETH price to NGN
        eth_to_ngn = Decimal(eth_to_ngn) if isinstance(eth_to_ngn, float) else eth_to_ngn
        amount_ngn = property_obj.price * eth_to_ngn
        
        # Set up Paystack API
        paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)
        
        # Define the payment data
        email = request.user.email  # Assuming the user is logged in
        
        # Dynamically create the full callback URL
        callback_url = request.build_absolute_uri(reverse('paystack_callback'))  # Absolute URL to your callback

        # Store the property ID in session for use in the callback
        request.session['property_id'] = property_id

        # Initialize Paystack payment (pass data as keyword arguments)
        payment = paystack.transaction.initialize(
            amount=int(amount_ngn * 100),  # Amount in kobo (convert to integer)
            email=email,
            currency='NGN',
            callback_url=callback_url,  # Set the dynamically generated callback URL
        )
        
        # Check if the payment was successful
        if payment['status']:
            authorization_url = payment['data']['authorization_url']
            return redirect(authorization_url)  # Redirect user to Paystack's payment page

    return render(request, 'dashboard/rental_payment.html', {'property': property_obj})