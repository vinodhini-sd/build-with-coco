# Train and Deploy a Churn Prediction Model

> Build, register, and serve an ML model end-to-end using Snowflake ML.

## The Prompt

```
Build a customer churn prediction model using Snowflake ML:
1. Use PROD.ANALYTICS.CUSTOMER_FEATURES as training data (columns: tenure_months,
   monthly_spend, support_tickets_90d, login_frequency, contract_type, churned)
2. Train an XGBoost classifier, tune hyperparameters, and log to the Model Registry
3. Deploy the best model as a model service endpoint
4. Run batch inference on PROD.ANALYTICS.ACTIVE_CUSTOMERS and save predictions
Show me the feature importance and model metrics (AUC, precision, recall).
```

## What This Triggers

- Machine learning skill (full ML pipeline)
- Feature engineering and train/test split
- XGBoost training with hyperparameter tuning
- Model Registry logging (experiment tracking)
- Model service deployment for inference
- Batch prediction on active customers

## Before You Run

- Snowflake ML feature store or a feature table with training data
- A labeled dataset (with the target column — e.g., `churned`)
- Compute pool or warehouse for training

## Tips

- Replace table and column names with your actual feature set
- Works for any classification task: fraud detection, lead scoring, defect prediction
- Add "also create a Streamlit app for exploring predictions" for a front-end
- Say "use LightGBM instead" to switch algorithms
