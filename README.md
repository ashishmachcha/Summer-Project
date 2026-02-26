# Loan Defaulter Prediction – Credit Risk Analysis Web App

An end‑to‑end **credit risk analysis** project that combines **machine learning** and a **Django web application** to predict whether a loan applicant is likely to **default (high risk)** or **repay (low risk)**.

The backend uses a **trained neural network model (TensorFlow/Keras)** and a **feature scaler (scikit‑learn)** built from historical lending data. The web app lets users sign up, log in, submit loan applications through a form, and instantly see a **risk prediction** along with a history of their past predictions.

---

## 🔍 What This Project Does

- Builds a **credit risk prediction model** from historical loan data.
- Exposes the model via a **Django web interface**.
- Allows **registered users** to:
  - Fill a loan application form.
  - Get an immediate **default risk probability**.
  - See whether the loan is classified as **High Risk** or **Low Risk**.
  - View lists of their **risky** and **non‑risky** loans on a dashboard.

This simulates a simple internal tool a bank or lending company might use for **pre‑screening loan applications**.

---

## ✨ Main Features

- **User Management**
  - User registration (sign‑up with validation).
  - Login / Logout using Django’s auth system.
  - Auth‑protected views (dashboard, prediction, results).

- **Loan Application & Prediction**
  - Django `ModelForm` for detailed loan application input.
  - Converts raw inputs into a feature vector.
  - Categorical encoding + numeric scaling.
  - TensorFlow/Keras **neural network** prediction.
  - Clear result:
    - Probability of default.
    - Label: **High Risk** or **Low Risk**.
    - Color‑coded status.

- **User Dashboard & History**
  - Shows recent loans for the logged‑in user.
  - Summary metrics:
    - Total loans evaluated.
    - Count of **safe** (non‑defaulter) loans.
    - Count of **risky** (defaulter) loans.
  - Separate pages listing only risky / only non‑risky loans.

- **Model Integration**
  - Uses pre‑trained files:
    - `neural_network_model.h5` (Keras model).
    - `neural_network_scaler.pkl` (scikit‑learn scaler).
  - Prediction logic fully integrated into Django views.

---
