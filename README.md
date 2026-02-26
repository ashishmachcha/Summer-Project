# Credit Risk Analysis – Loan Defaulter Prediction Web App

This project is a **Django-based web application** that helps lending institutions and analysts **predict whether a loan applicant is likely to default** (high risk) or not (low risk).

Behind the scenes, the app uses a **trained neural network model** (TensorFlow/Keras) and a **scaler** (from `scikit-learn`) that were built in an offline **Credit Risk Analysis** notebook. Users can create accounts, log in, submit detailed loan application information, and receive an immediate **risk assessment** for the loan. Each prediction is saved to the authenticated user’s account so they can review their **history of risky and non‑risky loans**.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
  - [Django App](#django-app)
  - [Machine Learning Model](#machine-learning-model)
- [Data & Features Used](#data--features-used)
- [How the Prediction Works](#how-the-prediction-works)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create & Activate Virtual Environment](#2-create--activate-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Place the Trained Model and Scaler](#4-place-the-trained-model-and-scaler)
  - [5. Run Database Migrations](#5-run-database-migrations)
  - [6. Create a Superuser (Optional)](#6-create-a-superuser-optional)
  - [7. Run the Development Server](#7-run-the-development-server)
- [Usage Guide](#usage-guide)
  - [Authentication Flow](#authentication-flow)
  - [Dashboard](#dashboard)
  - [Loan Prediction Flow](#loan-prediction-flow)
  - [Viewing Risky & Non-Risky Loans](#viewing-risky--non-risky-loans)
- [Important Files Explained](#important-files-explained)
- [Limitations & Future Improvements](#limitations--future-improvements)
- [License](#license)

---

## Project Overview

The goal of this project is to **predict loan default risk** for new loan applications using historical loan data and a machine learning model.

The workflow is:

1. A user signs up and logs into the web application.
2. The user fills a **loan application form** with financial and categorical information (loan amount, term, grade, employment length, home ownership, DTI, etc.).
3. The server:
   - Encodes and scales the input features.
   - Sends them to a **pre-trained neural network model**.
   - Receives a **probability of default**.
4. Based on this probability, the app classifies the loan as:
   - **High Risk (likely to default)**, or
   - **Low Risk (likely to be repaid)**.
5. The result is **saved in the database** and shown in:
   - A detailed **prediction result page**, and
   - The user’s **dashboard and history** pages (risky vs non‑risky loans).

---

## Key Features

- **User Authentication**
  - User registration (`signup`)
  - Login / Logout
  - Authenticated-only views for dashboard and predictions

- **Loan Prediction Form**
  - Captures detailed loan attributes such as:
    - `loan_amount`, `term`, `interest_rate`, `installment`, `grade`, `emp_length`,
      `home_ownership`, `annual_income`, `verification_status`, `dti`, `delinq_2yrs`,
      `open_acc`, `pub_rec`, `revol_util`, `purpose`, `initial_list_status`,
      `total_rec_late_fee`, `recoveries`, `acc_now_delinq`, `total_coll_amt`
  - Backed by a Django `ModelForm` to ensure validation and easy saving.

- **Machine Learning Integration**
  - Uses a **TensorFlow/Keras neural network** stored in `neural_network_model.h5`.
  - Uses a **`StandardScaler` (scikit-learn)** stored in `neural_network_scaler.pkl`.
  - Encodes categorical variables to numeric codes before prediction.

- **Dashboard & Loan History**
  - Shows recent loans and summary metrics:
    - Total loans created by the user.
    - Number of **safe (non‑defaulter)** loans.
    - Number of **risky (defaulter)** loans.
  - Separate pages for:
    - Non‑risky loans (`non_risky_loans`)
    - Risky loans (`risky_loans`)

- **Clean UX**
  - After each prediction, user is redirected to a **prediction result page** with:
    - Risk probability
    - Risk label (High / Low)
    - Color-coded risk (e.g. red for high risk, green for low risk)
    - Echo of the form inputs for review

---

## Architecture

### Django App

The Django application is located in the `project/app` folder and consists of:

- `models.py` – Defines the `LoanModel` used to store each loan instance and its prediction.
- `forms.py` – Defines `LoanForm`, a `ModelForm` based on `LoanModel` fields.
- `views.py` – Contains all the view functions that handle:
  - User registration, login, logout
  - Dashboard
  - Loan prediction form and prediction processing
  - Risky/non-risky loans list
  - Prediction result page
- `urls.py` – Maps URL paths to the appropriate view functions.

User accounts are provided by Django’s built-in `User` model, and each `LoanModel` instance is related to a `User` via a `ForeignKey`.

### Machine Learning Model

The ML part of the project lives in the `project/Credit Risk Analysis` folder:

- `Project.ipynb` – Jupyter notebook where the **credit risk analysis** and **model training** were performed.
- `XYZCorp_LendingData.txt` – Original dataset used for training (large file, typically not pushed to GitHub).
- `neural_network_model.h5` – Trained neural network model file.
- `neural_network_scaler.pkl` – Scaler fitted on the training data to normalize numeric features.

The Django app **does not train the model**; it **only loads the pre-trained model and scaler** to perform predictions on new inputs.

---

## Data & Features Used

The application uses the following key fields from the loan application:

- **Numeric features**
  - `loan_amount`
  - `interest_rate`
  - `installment`
  - `annual_income`
  - `dti` (Debt-to-Income ratio)
  - `delinq_2yrs` (Number of delinquencies in the past 2 years)
  - `open_acc` (Number of open accounts)
  - `pub_rec` (Number of derogatory public records)
  - `revol_util` (Revolving line utilization rate)
  - `total_rec_late_fee`
  - `recoveries`
  - `acc_now_delinq` (Number of accounts currently delinquent)
  - `total_coll_amt` (Total collection amounts)

- **Categorical features (encoded to integers)**
  - `term` (e.g., `36 months`, `60 months`)
  - `grade` (loan grade `A`–`G`)
  - `emp_length` (employment length, e.g., `< 1 year` to `10+ years`)
  - `home_ownership` (e.g., `RENT`, `MORTGAGE`, `OWN`, `OTHER`)
  - `verification_status` (`Not Verified`, `Verified`, `Source Verified`)
  - `purpose` (loan purpose such as `credit_card`, `debt_consolidation`, `car`, etc.)
  - `initial_list_status` (`f` or `w`)

These features are stored in the `LoanModel` and are transformed exactly in the same way as during training.

---

## How the Prediction Works

The core prediction logic is implemented in `project/app/views.py` inside `predict_loan`:

1. **Form submission**
   - The user submits the loan form (`LoanForm`) from the `predict.html` page.
   - Django validates the form and builds a `LoanModel` instance (`loan_instance`) without saving immediately.

2. **Extract and organize data**
   - A dictionary `selected_data` is created from the cleaned form fields.
   - Example keys: `loan_amount`, `term`, `interest_rate`, `grade`, `emp_length`, etc.

3. **Convert to DataFrame**
   - `selected_data` is wrapped in a `pandas.DataFrame` so it can be processed like the training data:
     df = pd.DataFrame([selected_data])
     
