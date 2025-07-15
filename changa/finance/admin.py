
from django.contrib import admin
from .models import Contribution, Loan, LoanRepayment, Expense, Transaction

admin.site.register(Contribution)
admin.site.register(Loan)
admin.site.register(LoanRepayment)
admin.site.register(Expense)
admin.site.register(Transaction)

