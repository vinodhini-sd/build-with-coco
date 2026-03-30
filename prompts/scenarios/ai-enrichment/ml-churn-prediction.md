# Train and Deploy a Churn Prediction Model

> Build, register, and serve an ML model end-to-end using Snowflake ML.

## The Prompt

```
Build an end-to-end churn prediction model using Snowflake ML. Ask me for my feature
table and which column is the target label, then train an XGBoost classifier, tune
hyperparameters, and log the best model to the Model Registry. Run batch inference on
my active customers and show me feature importance and model metrics.
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
