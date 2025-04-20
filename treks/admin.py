from django.contrib import admin
from .models import TrekkingExpense, AdditionalExpense, AssistantGuide, Porter

class AssistantGuideInline(admin.TabularInline):
    model = AssistantGuide
    extra = 1
    fields = ['name', 'role', 'salary_rate', 'salary_days', 'count']

class PorterInline(admin.TabularInline):
    model = Porter
    extra = 1
    fields = ['name', 'salary_rate', 'salary_days']

class AdditionalExpenseInline(admin.TabularInline):
    model = AdditionalExpense
    extra = 1
    fields = ['sn_no', 'particular', 'rate', 'numbers', 'days', 'total_amount', 'remarks']

from django.utils.html import format_html
from django.urls import reverse

@admin.register(TrekkingExpense)
class TrekkingExpenseAdmin(admin.ModelAdmin):
    inlines = [AssistantGuideInline, PorterInline, AdditionalExpenseInline]
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
            'description': 'Enter the main guide salary details here. For assistant/additional guides, use the section below.'
        }),
        ('Assistant Guide Details', {
            'fields': (('assistant_guide_salary_rate', 'assistant_guide_days'),),
            'classes': ('collapse',),
        }),
        ('Porter Details', {
            'fields': (('porter_salary_rate', 'porter_numbers', 'porter_days'),),
            'classes': ('collapse',),
            'description': 'Add individual porters below'
        }),
        ('Payment Information', {
            'fields': (
                ('guide_advance_amount', 'guide_advance_remark'),
                ('porter_advance_amount', 'porter_advance_remark'),
                ('package_advance_amount', 'package_advance_remark'),
                ('misc_advance_amount', 'misc_advance_remark'),
                ('assistant_guide_amount', 'assistant_advance_remark'),
                ('advance_paid', 'balance_amount'),
            ),
        }),
        ('Signatures', {
            'fields': (
                ('received_by', 'approved_by', 'paid_by'),
            ),
        }),
    )

    # Override to control where inlines appear
    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        for inline_class in self.inlines:
            inline = inline_class(self.model, self.admin_site)
            if request:
                if not inline.has_add_permission(request, obj):
                    continue
                if not inline.has_change_permission(request, obj):
                    continue
                if not inline.has_delete_permission(request, obj):
                    continue
            inline_instances.append(inline)
        return inline_instances

    class Media:
        css = {
            'all': ('admin/css/widgets.css', 'css/admin.css',)
        }
        js = ('admin/js/calendar.js', 'admin/js/admin/DateTimeShortcuts.js', 'js/trek_admin.js',)
    list_display = (
        'client_name', 'trekking_route', 'starting_date',
        'print_button', 'guide_porter_print_button'
    )

    def print_button(self, obj):
        return format_html(
            '<a class="button" href="{}" target="_blank">Print</a>',
            reverse('treks:print_expense', args=[obj.pk])
        )
    print_button.short_description = 'Print'

    def guide_porter_print_button(self, obj):
        return format_html(
            '<a class="button" href="{}" target="_blank">Guide/Porter Print</a>',
            reverse('treks:guide_porter_print', args=[obj.pk])
        )
    guide_porter_print_button.short_description = 'Guide/Porter Print'

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if isinstance(instance, AdditionalExpense) and not instance.sn_no:
                max_sn = instance.trekking_expense.additional_expenses.aggregate(
                    models.Max('sn_no'))['sn_no__max'] or 4
                instance.sn_no = max_sn + 1
            instance.save()
        formset.save_m2m()