from django.db import models
from django.contrib.auth.models import User
from chamas.models import Chama

class Contribution(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    chama = models.ForeignKey(Chama, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.member.username} - KES {self.amount} to {self.chama.name}"

class Loan(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('repaid', 'Repaid'),
    )

    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    chama = models.ForeignKey(Chama, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 12.5%
    duration_months = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Loan of KES {self.amount} by {self.borrower.username} - {self.status}"
    
class LoanRepayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Repayment of KES {self.amount} for Loan ID {self.loan.id}"

class Expense(models.Model):
    chama = models.ForeignKey(Chama, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    incurred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    incurred_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - KES {self.amount}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('loan', 'Loan'),
        ('repayment', 'Repayment'),
        ('expense', 'Expense'),
    )

    chama = models.ForeignKey(Chama, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type.title()} - KES {self.amount} ({self.chama.name})"
