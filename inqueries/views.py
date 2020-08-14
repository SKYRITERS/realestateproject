from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Inquery

def inquery(request):
    if request.method == 'POST':
        # If the request is POST, then we want to capture the fields. 
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        #Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
  
            has_contacted =Inquery.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted: 
                messages.error(request, 'You have already made an inquiry for this listing')
                return redirect('/listings/'+listing_id)
       
        inquery = Inquery(listing=listing, name=name, listing_id=listing_id, email=email, phone=phone, message=message, user_id=user_id )
        
        inquery.save()
        #Send email
        """ send_mail(
            'Property Listing Inquiry', 
            'There has been an inquiry for' +listing+ '.Sign into the admin panel for more info',
            'skriters@gmail.com',
            [realtor_email, 'abasmuhindi@gmail.com'],
            fail_silently=False
        )"""

        messages.success(request,'Your request has been submitted, a realtor will get back to you soon')
        return redirect('/listings/'+listing_id)