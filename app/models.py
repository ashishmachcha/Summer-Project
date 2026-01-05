from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



term_choices = [
    ('36 months', '36 months'),
    ('60 months', '60 months'),
]

grade_choices = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
    ('G', 'G'),
]

emp_length_choices = [
    ('10+ years', '10+ years'),
    ('9 years', '9 years'),
    ('8 years', '8 years'),
    ('7 years', '7 years'),
    ('6 years', '6 years'),
    ('5 years', '5 years'),
    ('4 years', '4 years'),
    ('3 years', '3 years'),
    ('2 years', '2 years'),
    ('1 year', '1 year'),
    ('< 1 year', '< 1 year')
]

home_ownership_choices = [
    ('RENT', 'RENT'),
    ('MORTGAGE', 'MORTGAGE'),
    ('OWN', 'OWN'),
    ('OTHER', 'OTHER'),
]

verification_status_choices = [
    ('Not Verified', 'Not Verified'),
    ('Verified', 'Verified'),
    ('Source Verified', 'Source Verified')
    
]
purpose_choices = [
    ('credit_card', 'credit_card'),
    ('debt_consolidation', 'debt_consolidation'),
    ('home_improvement', 'home_improvement'),
    ('major_purchase', 'major_purchase'),
    ('small_business', 'small_business'),
    ('vacation', 'vacation'),
    ('wedding', 'wedding'),
    ('other', 'other'),
    ('car', 'car'),
    ('medical', 'medical'),
    ('moving', 'moving'),
    ('renewable_energy', 'renewable_energy'),
    ('vacation', 'vacation'),
    ('wedding', 'wedding'),
    ('other', 'other'),
]

initial_list_status_choices = [
    ('f', 'f'),
    ('w', 'w'),
]

class LoanModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans', null=True, blank=True)
    loan_amount = models.IntegerField()
    term = models.CharField(max_length=20, choices=term_choices)
    interest_rate = models.FloatField()
    installment = models.FloatField()
    grade = models.CharField(max_length=20, choices=grade_choices)
    emp_length = models.CharField(max_length=20, choices=emp_length_choices)
    home_ownership = models.CharField(max_length=20, choices=home_ownership_choices)
    annual_income = models.IntegerField()
    verification_status = models.CharField(max_length=20, choices=verification_status_choices)
    dti = models.IntegerField()
    delinq_2yrs = models.IntegerField()
    open_acc = models.IntegerField()
    pub_rec = models.IntegerField()
    revol_util = models.IntegerField()
    purpose = models.CharField(max_length=20, choices=purpose_choices)
    initial_list_status = models.CharField(max_length=20, choices=initial_list_status_choices)
    total_rec_late_fee = models.IntegerField()
    recoveries = models.IntegerField()
    acc_now_delinq = models.IntegerField()
    total_coll_amt = models.IntegerField()
    defaulter = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        username = getattr(self.user, 'username', 'Unknown')
        return f"Loan {self.pk} - {username} - ${self.loan_amount}"

