from django.shortcuts import render, redirect
from .forms import LoanForm
from .models import LoanModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import pandas as pd
import joblib
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from django.contrib.auth.models import User, auth
from tensorflow.keras.models import load_model


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        if password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, "email already exist try new email id")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"username already exist try another username")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email,password=password)
                user.save()
                messages.info(request, "user created successfully")
                return redirect('login')
        else:
            messages.info(request, "password does not match")
            return redirect('signup')
    else:
        return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']  
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, "credential invalid")
            return redirect('login')
    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def dashboard(request):
    recent_loans = LoanModel.objects.filter(user=request.user).order_by('-created_at')[:5] 
    
    total_loans = LoanModel.objects.filter(user=request.user).count()
    safe_loans_count = LoanModel.objects.filter(user=request.user, defaulter=False).count()
    risky_loans_count = LoanModel.objects.filter(user=request.user, defaulter=True).count()
    
    context = {
        'recent_loans': recent_loans, 
        'total_loans': total_loans,
        'safe_loans_count': safe_loans_count,
        'risky_loans_count': risky_loans_count,
        'username': request.user.username,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def predict(request):
    form = LoanForm()
    return render(request, 'predict.html', {'form': form})


def logout_view(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def predict_loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan_instance = form.save(commit=False)
            loan_instance.user = request.user
            data = form.cleaned_data

            selected_data = {
                'loan_amount': data['loan_amount'],
                'term': data['term'],
                'interest_rate': data['interest_rate'],
                'installment': data['installment'],
                'grade': data['grade'],
                'emp_length': data['emp_length'],
                'home_ownership': data['home_ownership'],
                'annual_income': data['annual_income'],
                'verification_status': data['verification_status'],
                'dti': data['dti'],
                'delinq_2yrs': data['delinq_2yrs'],
                'open_acc': data['open_acc'],
                'pub_rec': data['pub_rec'],
                'revol_util': data['revol_util'],
                'purpose': data['purpose'],
                'initial_list_status': data['initial_list_status'],
                'total_rec_late_fee': data['total_rec_late_fee'],
                'recoveries': data['recoveries'],
                'acc_now_delinq': data['acc_now_delinq'],
                'total_coll_amt': data['total_coll_amt'],
            }

            
            df = pd.DataFrame([selected_data])

            
            emp_dict = {
                "< 1 year": 0, "1 year": 1, "2 years": 2, "3 years": 3, 
                "4 years": 4, "5 years": 5, "6 years": 6, "7 years": 7, 
                "8 years": 8, "9 years": 9, "10+ years": 10
            }
            

            term_dict = {'36 months': 0, '60 months': 1}
            grade_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6}
            emp_dict = {
                '< 1 year': 0, '1 year': 1, '2 years': 2, '3 years': 3, '4 years': 4,
                '5 years': 5, '6 years': 6, '7 years': 7, '8 years': 8, '9 years': 9, '10+ years': 10
            }
            home_ownership_dict = {'RENT': 0, 'MORTGAGE': 1, 'OWN': 2, 'OTHER': 3}
            verification_status_dict = {'Not Verified': 0, 'Verified': 1, 'Source Verified': 2}
            purpose_dict = {
                'credit_card': 0, 'debt_consolidation': 1, 'home_improvement': 2, 'major_purchase': 3,
                'small_business': 4, 'vacation': 5, 'wedding': 6, 'other': 7, 'car': 8, 'medical': 9,
                'moving': 10, 'renewable_energy': 11
            }
            initial_list_status_dict = {'f': 0, 'w': 1}


            df['term'] = df['term'].map(term_dict)
            df['grade'] = df['grade'].map(grade_dict)
            df['emp_length'] = df['emp_length'].map(emp_dict)
            df['home_ownership'] = df['home_ownership'].map(home_ownership_dict)
            df['verification_status'] = df['verification_status'].map(verification_status_dict)
            df['purpose'] = df['purpose'].map(purpose_dict)
            df['initial_list_status'] = df['initial_list_status'].map(initial_list_status_dict)

            
            
            expected_features = [
                'loan_amount', 'term', 'interest_rate', 'installment', 'grade', 'emp_length',
                'home_ownership', 'annual_income', 'verification_status', 'dti', 'delinq_2yrs',
                'open_acc', 'pub_rec', 'revol_util', 'purpose', 'initial_list_status',
                'total_rec_late_fee', 'recoveries', 'acc_now_delinq', 'total_coll_amt'
            ]
            
            df = df[expected_features]

            loan_instance.save()
            
            try:
                
                model = load_model('Credit Risk Analysis/neural_network_model.h5')
                scaler = joblib.load('Credit Risk Analysis/neural_network_scaler.pkl')
                
                df_scaled = scaler.transform(df)
                
                probability = float(model.predict(df_scaled)[0][0])

                loan_instance.defaulter = probability > 0.3
                loan_instance.save()  

                if probability > 0.3:
                    prediction_message = "High Risk - Loan application is likely to default"
                    risk_level = "High Risk"
                    risk_color = "danger"
                else:
                    prediction_message = "Low Risk - Loan application is likely to be approved"
                    risk_level = "Low Risk"
                    risk_color = "success"

                
                request.session['prediction_data'] = {
                    'loan_id': loan_instance.id,
                    'prediction': probability,
                    'prediction_message': prediction_message,
                    'risk_level': risk_level,
                    'risk_color': risk_color,
                    'form_data': selected_data,
                }

                return redirect('prediction_result')

            except Exception as e:
                loan_instance.defaulter = False
                loan_instance.save()  
                
                
                request.session['prediction_data'] = {
                    'loan_id': loan_instance.id,
                    'prediction': None,
                    'prediction_message': f"Data saved successfully, but prediction failed: {str(e)}",
                    'risk_level': "Unknown",
                    'risk_color': "warning",
                    'form_data': selected_data,
                }
                
                return redirect('prediction_result')
    else:
        form = LoanForm()

    return render(request, 'predict.html', {'form': form})

@login_required(login_url='login')
def non_risky_loans(request):
    loans = LoanModel.objects.filter(user=request.user, defaulter=False).order_by('-created_at')
    return render(request, 'non_risky_loans.html', {'loans': loans})


@login_required(login_url='login')
def risky_loans(request):
    loans = LoanModel.objects.filter(user=request.user, defaulter=True)
    return render(request, 'risky_loans.html', {'loans': loans})


def home(request):
    return redirect('login')


def ask_questions(request):
    pass

@login_required(login_url='login')
def prediction_result(request):
    prediction_data = request.session.get('prediction_data')
    
    if not prediction_data:
        return redirect('predict_form')
    
    try:
        loan = LoanModel.objects.get(id=prediction_data['loan_id'])
    except LoanModel.DoesNotExist:
        return redirect('predict_form')
    
    if 'prediction_data' in request.session:
        del request.session['prediction_data']
    
    return render(request, 'prediction_result.html', {
        'loan': loan,
        'prediction': prediction_data['prediction'],
        'prediction_message': prediction_data['prediction_message'],
        'risk_level': prediction_data['risk_level'],
        'risk_color': prediction_data['risk_color'],
        'form_data': prediction_data['form_data'],
    })

