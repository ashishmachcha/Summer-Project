from django.contrib import admin
from .models import LoanModel
from .forms import LoanForm
# Register your models here.

admin.site.register(LoanModel)