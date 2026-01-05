from django import forms
from .models import LoanModel

class LoanForm(forms.ModelForm):
    class Meta:
        model = LoanModel
        fields = [
            'loan_amount', 'term', 'interest_rate', 'installment', 'grade', 'emp_length',
            'home_ownership', 'annual_income', 'verification_status', 'dti', 'delinq_2yrs',
            'open_acc', 'pub_rec', 'revol_util', 'purpose', 'initial_list_status',
            'total_rec_late_fee', 'recoveries', 'acc_now_delinq', 'total_coll_amt'
        ]


