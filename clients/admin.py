from django.contrib import admin
from .models import Client, PriceItem
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import csv
import xlsxwriter
from io import BytesIO
from datetime import datetime

class PriceItemInline(admin.TabularInline):
    model = PriceItem
    extra = 1

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'country', 'package_and_guide', 'active_services',
                   'starting_date', 'number_of_days', 'ending_date', 'payment_status')
    list_filter = ('payment_status', 'trekking', 'peak_climbing', 'tour', 
                  'adventure_day_activities', 'flight', 'country', 'guide', 'package')
    search_fields = ('client_name', 'email', 'country', 'passport', 'phone_number', 'quick_notes', 'guide', 'package')
    date_hierarchy = 'starting_date'
    inlines = [PriceItemInline]
    actions = ['export_as_csv', 'export_as_xlsx']
    
    # Include JavaScript for date calculation
    class Media:
        js = ('admin/js/calendar.js', 'admin/js/admin/DateTimeShortcuts.js', 'js/client_admin.js')
    
    def package_and_guide(self, obj):
        """Display package and guide details with styling"""
        if not obj.package and not obj.guide:
            return mark_safe('-')
            
        output_html = ""
        
        # Package with color based on type
        if obj.package:
            if obj.peak_climbing:
                output_html += f'<strong style="color: #d9534f; font-size: 14px;">{obj.package}</strong>'
            elif obj.trekking:
                output_html += f'<strong style="color: #5bc0de; font-size: 14px;">{obj.package}</strong>'
            elif obj.tour:
                output_html += f'<strong style="color: #5cb85c; font-size: 14px;">{obj.package}</strong>'
            else:
                output_html += f'<strong>{obj.package}</strong>'
        
        # Guide with better visibility
        if obj.guide:
            guide_color = "#ffc107"  # Yellow/gold for better visibility
            output_html += f'<br><span style="color: {guide_color}; font-weight: 500;">{obj.guide}</span>'
        
        return mark_safe(output_html)
    
    package_and_guide.short_description = 'Trek / Guide'
    package_and_guide.admin_order_field = 'package'
    
    def active_services(self, obj):
        """Display only the active services for each client"""
        services = []
        
        # Only add services that are active
        if obj.trekking:
            services.append('<span style="background-color: #5bc0de; color: white; padding: 2px 6px; border-radius: 3px; margin-right: 4px;">🥾 Trek</span>')
        
        if obj.peak_climbing:
            services.append('<span style="background-color: #d9534f; color: white; padding: 2px 6px; border-radius: 3px; margin-right: 4px;">🏔️ Climb</span>')
        
        if obj.tour:
            services.append('<span style="background-color: #5cb85c; color: white; padding: 2px 6px; border-radius: 3px; margin-right: 4px;">🚌 Tour</span>')
        
        if obj.adventure_day_activities:
            services.append('<span style="background-color: #f0ad4e; color: white; padding: 2px 6px; border-radius: 3px; margin-right: 4px;">🧗 Adv</span>')
        
        if obj.flight:
            services.append('<span style="background-color: #0275d8; color: white; padding: 2px 6px; border-radius: 3px; margin-right: 4px;">✈️ Flight</span>')
        
        # Add misc service if present
        if obj.misc_service:
            misc_text = obj.misc_service[:15] + ('...' if len(obj.misc_service) > 15 else '')
            services.append(f'<span style="background-color: #6c757d; color: white; padding: 2px 6px; border-radius: 3px;">🔧 {misc_text}</span>')
        
        if not services:
            return mark_safe('<span style="color: #6c757d;">-</span>')
            
        return mark_safe('<div>' + ''.join(services) + '</div>')
        
    active_services.short_description = 'Services'
    
    def export_as_csv(self, request, queryset):
        """Export selected clients as CSV file."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="clients_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
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
    export_as_csv.short_description = "Export selected clients as CSV"
    
    def export_as_xlsx(self, request, queryset):
        """Export selected clients as Excel XLSX file."""
        # Create output buffer
        output = BytesIO()
        
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
        response['Content-Disposition'] = f'attachment; filename="clients_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
        
        return response
    export_as_xlsx.short_description = "Export selected clients as Excel"

@admin.register(PriceItem)
class PriceItemAdmin(admin.ModelAdmin):
    list_display = ('client', 'description', 'amount', 'notes')
    list_filter = ('client',)
    search_fields = ('description', 'notes')