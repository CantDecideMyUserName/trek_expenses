from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import timedelta
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
import csv
import xlsxwriter
from io import BytesIO

from .models import Client, PriceItem

# View for listing clients
def client_list(request):
    # Get filter parameters
    search = request.GET.get('search', '')
    trek = request.GET.get('trek', '')
    guide = request.GET.get('guide', '')
    country = request.GET.get('country', '')
    service = request.GET.get('service', '')
    
    # Start with all clients
    clients = Client.objects.all()
    
    # Apply filters
    if search:
        clients = clients.filter(
            Q(client_name__icontains=search) | 
            Q(email__icontains=search) | 
            Q(country__icontains=search) |
            Q(passport__icontains=search) |
            Q(phone_number__icontains=search) |
            Q(quick_notes__icontains=search)
        )
    
    if trek:
        clients = clients.filter(package__icontains=trek)
    
    if guide:
        clients = clients.filter(guide__icontains=guide)
    
    if country:
        clients = clients.filter(country__icontains=country)
    
    if service:
        if service == 'trekking':
            clients = clients.filter(trekking=True)
        elif service == 'peak_climbing':
            clients = clients.filter(peak_climbing=True)
        elif service == 'tour':
            clients = clients.filter(tour=True)
        elif service == 'adventure':
            clients = clients.filter(adventure_day_activities=True)
        elif service == 'flight':
            clients = clients.filter(flight=True)
    
    # Get unique values for filter dropdowns
    all_guides = Client.objects.values_list('guide', flat=True).distinct()
    all_countries = Client.objects.values_list('country', flat=True).distinct()
    
    context = {
        'clients': clients,
        'guides': all_guides,
        'countries': all_countries
    }
    
    return render(request, 'clients/client_list.html', context)

# View for client details
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    price_items = client.price_items.all()
    return render(request, 'clients/client_detail.html', {
        'client': client,
        'price_items': price_items
    })

# Client creation view
def client_create(request):
    if request.method == 'POST':
        try:
            # Get data directly from POST
            client = Client(
                client_name=request.POST.get('client_name', ''),
                email=request.POST.get('email', ''),
                country=request.POST.get('country', ''),
                passport=request.POST.get('passport', ''),
                phone_number=request.POST.get('phone_number', ''),
                quick_notes=request.POST.get('quick_notes', ''),
                starting_date=request.POST.get('starting_date'),
                ending_date=request.POST.get('ending_date'),
                trekking='trekking' in request.POST,
                peak_climbing='peak_climbing' in request.POST,
                tour='tour' in request.POST,
                adventure_day_activities='adventure_day_activities' in request.POST,
                flight='flight' in request.POST,
                misc_service=request.POST.get('misc_service', ''),
                guide=request.POST.get('guide', ''),
                porter=request.POST.get('porter', ''),
                package=request.POST.get('package', ''),
                transport=request.POST.get('transport', ''),
                accommodation=request.POST.get('accommodation', ''),
                price=request.POST.get('price') if request.POST.get('price') else None,
                additional_charges=request.POST.get('additional_charges') if request.POST.get('additional_charges') else 0,
                discount=request.POST.get('discount') if request.POST.get('discount') else 0,
                payment_status=request.POST.get('payment_status', 'pending')
            )
            
            # Handle number_of_days
            number_of_days = request.POST.get('number_of_days')
            if number_of_days:
                client.number_of_days = int(number_of_days)
                
                # Calculate ending_date if not provided
                if client.starting_date and not client.ending_date:
                    client.ending_date = client.starting_date + timedelta(days=client.number_of_days - 1)
            
            client.save()
            
            # Handle price items
            descriptions = request.POST.getlist('price_item_description[]')
            amounts = request.POST.getlist('price_item_amount[]')
            notes = request.POST.getlist('price_item_notes[]')
            
            for i in range(len(descriptions)):
                if descriptions[i] and amounts[i]:
                    PriceItem.objects.create(
                        client=client,
                        description=descriptions[i],
                        amount=amounts[i],
                        notes=notes[i] if i < len(notes) else ''
                    )
            
            messages.success(request, "Client created successfully.")
            
            # Handle different save actions
            if 'save_and_add' in request.POST:
                return redirect('clients:client_create')
            elif 'save_and_continue' in request.POST:
                return redirect('clients:client_update', pk=client.pk)
            else:
                return redirect('clients:client_list')
                
        except Exception as e:
            messages.error(request, f"Error creating client: {str(e)}")
    
    # For GET requests, just render the empty template
    return render(request, 'clients/client_form.html')

# Client update view
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    price_items = client.price_items.all()
    
    if request.method == 'POST':
        try:
            # Update client fields from POST
            client.client_name = request.POST.get('client_name', client.client_name)
            client.email = request.POST.get('email', client.email)
            client.country = request.POST.get('country', client.country)
            client.passport = request.POST.get('passport', client.passport)
            client.phone_number = request.POST.get('phone_number', client.phone_number)
            client.quick_notes = request.POST.get('quick_notes', client.quick_notes)
            
            if request.POST.get('starting_date'):
                client.starting_date = request.POST.get('starting_date')
            
            if request.POST.get('ending_date'):
                client.ending_date = request.POST.get('ending_date')
            
            client.trekking = 'trekking' in request.POST
            client.peak_climbing = 'peak_climbing' in request.POST
            client.tour = 'tour' in request.POST
            client.adventure_day_activities = 'adventure_day_activities' in request.POST
            client.flight = 'flight' in request.POST
            client.misc_service = request.POST.get('misc_service', '')
            
            client.guide = request.POST.get('guide', '')
            client.porter = request.POST.get('porter', '')
            client.package = request.POST.get('package', '')
            client.transport = request.POST.get('transport', '')
            client.accommodation = request.POST.get('accommodation', '')
            
            # Handle number_of_days
            number_of_days = request.POST.get('number_of_days')
            if number_of_days:
                client.number_of_days = int(number_of_days)
                
                # Calculate ending_date if not provided
                if client.starting_date and not client.ending_date:
                    client.ending_date = client.starting_date + timedelta(days=client.number_of_days - 1)
            
            # Handle financial fields
            client.price = request.POST.get('price') if request.POST.get('price') else None
            client.additional_charges = request.POST.get('additional_charges') if request.POST.get('additional_charges') else 0
            client.discount = request.POST.get('discount') if request.POST.get('discount') else 0
            client.payment_status = request.POST.get('payment_status', 'pending')
            
            client.save()
            
            # Handle price items - first clear existing ones
            client.price_items.all().delete()
            
            # Then add new ones
            descriptions = request.POST.getlist('price_item_description[]')
            amounts = request.POST.getlist('price_item_amount[]')
            notes = request.POST.getlist('price_item_notes[]')
            
            for i in range(len(descriptions)):
                if descriptions[i] and amounts[i]:
                    PriceItem.objects.create(
                        client=client,
                        description=descriptions[i],
                        amount=amounts[i],
                        notes=notes[i] if i < len(notes) else ''
                    )
            
            messages.success(request, "Client updated successfully.")
            
            # Handle different save actions
            if 'save_and_add' in request.POST:
                return redirect('clients:client_create')
            elif 'save_and_continue' in request.POST:
                return redirect('clients:client_update', pk=client.pk)
            else:
                return redirect('clients:client_list')
                
        except Exception as e:
            messages.error(request, f"Error updating client: {str(e)}")
    
    # For GET requests, render template with client data
    return render(request, 'clients/client_form.html', {
        'form': client,
        'price_items': price_items
    })

# CSV Export View
@staff_member_required
def export_clients_csv(request):
    """Export clients to CSV, respecting any applied filters."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clients.csv"'
    
    # Get filter parameters from request
    search = request.GET.get('search', '')
    trek = request.GET.get('trek', '')
    guide = request.GET.get('guide', '')
    country = request.GET.get('country', '')
    service = request.GET.get('service', '')
    
    # Build queryset with filters
    queryset = Client.objects.all()
    
    # Apply the same filters as in client_list view
    if search:
        queryset = queryset.filter(
            Q(client_name__icontains=search) | 
            Q(email__icontains=search) | 
            Q(country__icontains=search) |
            Q(passport__icontains=search) |
            Q(phone_number__icontains=search) |
            Q(quick_notes__icontains=search)
        )
    
    if trek:
        queryset = queryset.filter(package__icontains=trek)
    
    if guide:
        queryset = queryset.filter(guide__icontains=guide)
    
    if country:
        queryset = queryset.filter(country__icontains=country)
    
    if service:
        if service == 'trekking':
            queryset = queryset.filter(trekking=True)
        elif service == 'peak_climbing':
            queryset = queryset.filter(peak_climbing=True)
        elif service == 'tour':
            queryset = queryset.filter(tour=True)
        elif service == 'adventure':
            queryset = queryset.filter(adventure_day_activities=True)
        elif service == 'flight':
            queryset = queryset.filter(flight=True)
    
    # Create CSV writer
    writer = csv.writer(response)
    
    # Write header row
    writer.writerow([
        'Client Name', 'Email', 'Country', 'Passport', 'Phone Number', 
        'Starting Date', 'Ending Date', 'Total Days', 'Trekking Days',
        'Services', 'Payment Status', 'Price', 'Additional Charges', 
        'Discount', 'Total Amount', 'Guide', 'Porter', 'Package', 
        'Transport', 'Accommodation', 'Notes'
    ])
    
    # Write data rows
    for client in queryset:
        # Determine services provided
        services = []
        if client.trekking:
            services.append('Trekking')
        if client.peak_climbing:
            services.append('Peak Climbing')
        if client.tour:
            services.append('Tour')
        if client.adventure_day_activities:
            services.append('Adventure')
        if client.flight:
            services.append('Flight')
        if client.misc_service:
            services.append(client.misc_service)
        
        # Calculate total amount
        total_amount = (client.price or 0) + (client.additional_charges or 0) - (client.discount or 0)
        
        writer.writerow([
            client.client_name,
            client.email,
            client.country,
            client.passport,
            client.phone_number,
            client.starting_date,
            client.ending_date,
            client.number_of_days,
            client.trekking_days,
            ', '.join(services),
            client.payment_status,
            client.price,
            client.additional_charges,
            client.discount,
            total_amount,
            client.guide,
            client.porter,
            client.package,
            client.transport,
            client.accommodation,
            client.quick_notes
        ])
    
    return response

# Excel Export View
@staff_member_required
def export_clients_xlsx(request):
    """Export clients to Excel XLSX format, respecting any applied filters."""
    # Create output buffer
    output = BytesIO()
    
    # Get filter parameters from request
    search = request.GET.get('search', '')
    trek = request.GET.get('trek', '')
    guide = request.GET.get('guide', '')
    country = request.GET.get('country', '')
    service = request.GET.get('service', '')
    
    # Build queryset with filters
    queryset = Client.objects.all()
    
    # Apply the same filters as in client_list view
    if search:
        queryset = queryset.filter(
            Q(client_name__icontains=search) | 
            Q(email__icontains=search) | 
            Q(country__icontains=search) |
            Q(passport__icontains=search) |
            Q(phone_number__icontains=search) |
            Q(quick_notes__icontains=search)
        )
    
    if trek:
        queryset = queryset.filter(package__icontains=trek)
    
    if guide:
        queryset = queryset.filter(guide__icontains=guide)
    
    if country:
        queryset = queryset.filter(country__icontains=country)
    
    if service:
        if service == 'trekking':
            queryset = queryset.filter(trekking=True)
        elif service == 'peak_climbing':
            queryset = queryset.filter(peak_climbing=True)
        elif service == 'tour':
            queryset = queryset.filter(tour=True)
        elif service == 'adventure':
            queryset = queryset.filter(adventure_day_activities=True)
        elif service == 'flight':
            queryset = queryset.filter(flight=True)
    
    # Create a workbook and add a worksheet
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Clients')
    
    # Add formats
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#3366CC',
        'color': 'white',
        'border': 1
    })
    
    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
    number_format = workbook.add_format({'num_format': '#,##0.00'})
    
    # Write header row
    headers = [
        'Client Name', 'Email', 'Country', 'Passport', 'Phone Number', 
        'Starting Date', 'Ending Date', 'Total Days', 'Trekking Days',
        'Services', 'Payment Status', 'Price', 'Additional Charges', 
        'Discount', 'Total Amount', 'Guide', 'Porter', 'Package', 
        'Transport', 'Accommodation', 'Notes'
    ]
    
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)
    
    # Write data rows
    for row, client in enumerate(queryset, start=1):
        # Determine services provided
        services = []
        if client.trekking:
            services.append('Trekking')
        if client.peak_climbing:
            services.append('Peak Climbing')
        if client.tour:
            services.append('Tour')
        if client.adventure_day_activities:
            services.append('Adventure')
        if client.flight:
            services.append('Flight')
        if client.misc_service:
            services.append(client.misc_service)
        
        # Calculate total amount
        total_amount = (client.price or 0) + (client.additional_charges or 0) - (client.discount or 0)
        
        worksheet.write(row, 0, client.client_name)
        worksheet.write(row, 1, client.email)
        worksheet.write(row, 2, client.country)
        worksheet.write(row, 3, client.passport)
        worksheet.write(row, 4, client.phone_number)
        
        # Date fields
        if client.starting_date:
            worksheet.write_datetime(row, 5, client.starting_date, date_format)
        if client.ending_date:
            worksheet.write_datetime(row, 6, client.ending_date, date_format)
        
        worksheet.write(row, 7, client.number_of_days)
        worksheet.write(row, 8, client.trekking_days)
        worksheet.write(row, 9, ', '.join(services))
        worksheet.write(row, 10, client.payment_status)
        
        # Financial fields with number format
        if client.price is not None:
            worksheet.write_number(row, 11, float(client.price), number_format)
        if client.additional_charges is not None:
            worksheet.write_number(row, 12, float(client.additional_charges), number_format)
        if client.discount is not None:
            worksheet.write_number(row, 13, float(client.discount), number_format)
        worksheet.write_number(row, 14, float(total_amount), number_format)
        
        worksheet.write(row, 15, client.guide)
        worksheet.write(row, 16, client.porter)
        worksheet.write(row, 17, client.package)
        worksheet.write(row, 18, client.transport)
        worksheet.write(row, 19, client.accommodation)
        worksheet.write(row, 20, client.quick_notes)
    
    # Auto-fit columns
    for col in range(len(headers)):
        worksheet.set_column(col, col, 15)  # Set column width to 15 as a starting point
    
    workbook.close()
    
    # Create response with Excel file
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="clients.xlsx"'
    
    return response