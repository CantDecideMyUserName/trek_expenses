from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db import models
from .models import TrekkingExpense, AdditionalExpense

class AdditionalExpenseInline(admin.TabularInline):
    model = AdditionalExpense
    extra = 1
    fields = ['sn_no', 'particular', 'rate', 'numbers', 'days', 'total_amount', 'remarks']
    
    def get_queryset(self, request):
        # Override to ensure proper ordering
        queryset = super().get_queryset(request)
        return queryset.order_by('sn_no')

    def get_extra(self, request, obj=None, **kwargs):
        # If this is an existing object, look at existing expenses
        if obj:
            expenses_count = obj.additional_expenses.count()
            if expenses_count > 0:
                # Get the last serial number and add 1
                last_sn = obj.additional_expenses.order_by('-sn_no').first().sn_no
                # Set initial value for the next item
                self.initial = [{'sn_no': last_sn + 1}]
            else:
                # If no expenses yet, start with 5 (since 1-4 are reserved for standard expenses)
                self.initial = [{'sn_no': 5}]
        return 1

@admin.register(TrekkingExpense)
class TrekkingExpenseAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'starting_date', 'trekking_route', 'total_amount', 'print_button']
    list_filter = ['starting_date', 'nationality']
    search_fields = ['client_name', 'trekking_route']
    inlines = [AdditionalExpenseInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('client_name', 'nationality'),
                ('trekking_route', 'duration_days'),
                ('trekking_guide', 'assistant_guide'),
                ('starting_date', 'ending_date', 'issue_date'),
            )
        }),
        ('Package Details', {
            'fields': (('package_rate', 'package_numbers', 'package_days'),),
            'classes': ('collapse',),
        }),
        ('Guide Details', {
            'fields': (('guide_salary_rate', 'guide_salary_days'),),
            'classes': ('collapse',),
        }),
        ('Assistant Guide Details', {
            'fields': (('assistant_guide_salary_rate', 'assistant_guide_days'),),
            'classes': ('collapse',),
        }),
        ('Porter Details', {
            'fields': (('porter_salary_rate', 'porter_numbers', 'porter_days'),),
            'classes': ('collapse',),
        }),
        # ('Additional Details', {
        #     'fields': ('extra_expenses', 'remarks'),
        # }),
        ('Payment Information', {
            'fields': (('advance_paid', 'balance_amount'),),
        }),
        ('Signatures', {
            'fields': (
                ('received_by', 'approved_by', 'paid_by'),
            ),
        }),
    )

    def print_button(self, obj):
        return format_html(
            '<a class="button" href="{}" target="_blank">Print</a>',
            reverse('treks:print_expense', args=[obj.pk])
        )
    print_button.short_description = 'Print'

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        # Delete marked for deletion
        for obj in formset.deleted_objects:
            obj.delete()
        # Save new/updated instances
        for instance in instances:
            # If it's an AdditionalExpense and no sn_no is set
            if isinstance(instance, AdditionalExpense) and not instance.sn_no:
                # Get the highest sn_no currently in use
                max_sn = instance.trekking_expense.additional_expenses.aggregate(
                    models.Max('sn_no'))['sn_no__max'] or 4
                instance.sn_no = max_sn + 1
            instance.save()
        formset.save_m2m()

    class Media:
        css = {
            'all': ('admin/css/widgets.css', 'css/admin.css',)  # Your custom CSS)
        }
        js = ('admin/js/calendar.js', 'admin/js/admin/DateTimeShortcuts.js', 'js/trek_admin.js',)