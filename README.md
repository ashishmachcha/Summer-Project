# Loan Defaulter Prediction – Credit Risk Analysis Web App

This project is a **Django web application** that uses a **trained neural network (TensorFlow/Keras)** to predict whether a loan applicant is likely to **default (high risk)** or **repay (low risk)**.  
Users can sign up, log in, submit loan applications through a form, and see a **risk prediction** plus a history of their previous loans.

---

## Overview

- **Problem**: Estimate credit risk for new loan applications.
- **Solution**:
  - A **machine learning model** trained on historical lending data (in a Jupyter notebook).
  - A **Django app** that:
    - Collects loan data via a form.
    - Encodes and scales the inputs.
    - Calls the neural network model for prediction.
    - Saves each prediction to the database and shows it in a dashboard.

The ML training is done offline (in `Project.ipynb`), and the trained artifacts:
- `neural_network_model.h5`
- `neural_network_scaler.pkl`  
are loaded by the Django app at prediction time.

---

## Main Features

- **User Accounts**
  - Sign up with username, email, and password.
  - Log in / log out (Django authentication).
  - Every loan record is linked to the logged‑in user.

- **Loan Prediction**
  - Form backed by `LoanForm` / `LoanModel` with fields like:
    - `loan_amount`, `term`, `interest_rate`, `installment`, `grade`,
      `emp_length`, `home_ownership`, `annual_income`, `verification_status`,
      `dti`, `delinq_2yrs`, `open_acc`, `pub_rec`, `revol_util`,
      `purpose`, `initial_list_status`, `total_rec_late_fee`,
      `recoveries`, `acc_now_delinq`, `total_coll_amt`.
  - Categorical features are mapped to integers (same encoding as in training).
  - Features are scaled with the saved `StandardScaler`.
  - Neural network outputs a **default probability**.
  - If probability > **0.3** → **High Risk (defaulter = True)**, else **Low Risk**.

- **Dashboard & History**
  - **Dashboard** (for logged‑in user):
    - Last few loans.
    - Total loans.
    - Count of **safe** vs **risky** loans.
  - Separate pages for:
    - `/non-risky-loans/` – loans predicted as non‑defaulters.
    - `/risky-loans/` – loans predicted as defaulters.

---

## How It Works (Short Version)

1. **Model Training (offline)**
   - Notebook `Project.ipynb` (inside `project/Credit Risk Analysis/`) loads historical data (`XYZCorp_LendingData.txt`).
   - Cleans and preprocesses data.
   - Fits a neural network classifier.
   - Fits a `StandardScaler` on the features.
   - Saves:
     - `neural_network_model.h5`
     - `neural_network_scaler.pkl`

2. **Prediction in Django (online)**
   - User submits the loan form.
   - Django builds a `pandas.DataFrame` from the cleaned form data.
   - Categorical values (term, grade, emp_length, etc.) are mapped to numeric codes.
   - Columns are ordered to match the training feature order.
   - The scaler transforms the data.
   - The model predicts the default probability.
   - Probability is converted to a label (High / Low risk).
   - The `LoanModel` instance is saved with `defaulter=True/False`.
   - A result page shows the risk, probability, and input details.

---

## Project Structure (Simplified)

LoanDefaulter/
├── project/
│   ├── app/
│   │   ├── models.py      # LoanModel + choices
│   │   ├── forms.py       # LoanForm (ModelForm)
│   │   ├── views.py       # auth, dashboard, prediction logic
│   │   ├── urls.py        # routes for app
│   │   └── templates/     # HTML templates (login, dashboard, predict, result, etc.)
│   ├── Credit Risk Analysis/
│   │   ├── Project.ipynb
│   │   ├── neural_network_model.h5
│   │   └── neural_network_scaler.pkl
│   └── manage.py
└── .gitignore
