from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class TrekkingExpense(models.Model):
    # Basic Information
    client_name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    trekking_route = models.CharField(max_length=200)
    duration_days = models.IntegerField(validators=[MinValueValidator(1)])
    
    # Guide Information - simplified to just text fields
    trekking_guide = models.CharField(max_length=100)
    assistant_guide = models.CharField(max_length=100, blank=True, null=True)
    
    starting_date = models.DateField()
    ending_date = models.DateField()
    issue_date = models.DateField(default=timezone.now)
    
    # Standard Expenses (all optional)
    package_rate = models.IntegerField(null=True, blank=True)
    package_numbers = models.IntegerField(null=True, blank=True)
    package_days = models.IntegerField(null=True, blank=True)
    
    guide_salary_rate = models.IntegerField(null=True, blank=True)
    guide_salary_days = models.IntegerField(null=True, blank=True)
    
    porter_salary_rate = models.IntegerField(null=True, blank=True)
    porter_numbers = models.IntegerField(null=True, blank=True)
    porter_days = models.IntegerField(null=True, blank=True)
    
    assistant_guide_salary_rate = models.IntegerField(null=True, blank=True)
    assistant_guide_days = models.IntegerField(null=True, blank=True)
    
    extra_expenses = models.IntegerField(default=0)
    remarks = models.TextField(blank=True)
    
    advance_paid = models.IntegerField(default=0)
    balance_amount = models.IntegerField(default=0)

    # Signing fields - simplified to text fields
    received_by = models.CharField(max_length=100)
    approved_by = models.CharField(max_length=100)
    paid_by = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.client_name} - {self.starting_date}"

    def save(self, *args, **kwargs):
        # Calculate balance amount before saving
        self.balance_amount = self.total_amount - self.advance_paid
        super().save(*args, **kwargs)

    @property
    def package_total(self):
        if all(v is not None for v in [self.package_rate, self.package_numbers, self.package_days]):
            return self.package_rate * self.package_numbers * self.package_days
        return 0

    @property
    def guide_salary_total(self):
        if all(v is not None for v in [self.guide_salary_rate, self.guide_salary_days]):
            return self.guide_salary_rate * self.guide_salary_days
        return 0

    @property
    def porter_salary_total(self):
        if all(v is not None for v in [self.porter_salary_rate, self.porter_numbers, self.porter_days]):
            return self.porter_salary_rate * self.porter_numbers * self.porter_days
        return 0
    
    @property
    def assistant_guide_salary_total(self):
        if self.assistant_guide_salary_rate and self.assistant_guide_days:
            return self.assistant_guide_salary_rate * self.assistant_guide_days
        return 0

    @property
    def additional_expenses_total(self):
        return sum(expense.total_amount for expense in self.additional_expenses.all())

    @property
    def total_amount(self):
        return (
            self.package_total +
            self.guide_salary_total +
            self.porter_salary_total +
            self.assistant_guide_salary_total +
            self.extra_expenses +
            self.additional_expenses_total
        )

class AdditionalExpense(models.Model):
    trekking_expense = models.ForeignKey(TrekkingExpense, related_name='additional_expenses', on_delete=models.CASCADE)
    sn_no = models.IntegerField(help_text="Serial Number (e.g., 5, 6)")
    particular = models.CharField(max_length=200)
    rate = models.IntegerField(null=True, blank=True)
    numbers = models.IntegerField(null=True, blank=True)
    days = models.IntegerField(null=True, blank=True)
    total_amount = models.IntegerField()
    remarks = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        # Calculate total amount if rate, numbers, and days are provided
        if all(v is not None for v in [self.rate, self.numbers, self.days]):
            self.total_amount = self.rate * self.numbers * self.days
        super().save(*args, **kwargs)
        # Update parent TrekkingExpense's balance
        self.trekking_expense.save()

    class Meta:
        ordering = ['sn_no']