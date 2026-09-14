# Employee Attrition Prediction

A machine learning project to predict whether an employee is likely to leave an organization based on employee and job-related features.

## Project Workflow

- Data cleaning and quality checks
- Exploratory Data Analysis (EDA)
- Feature preprocessing using `StandardScaler` and `OneHotEncoder`
- Logistic Regression, Decision Tree, Random Forest, and XGBoost comparison
- Cross-validation using Stratified K-Fold
- Evaluation using Accuracy, Precision, Recall, F1-score, and ROC-AUC

## Results

The final Logistic Regression model achieved:

| Metric | Score |
|---|---:|
| Accuracy | 75.5% |
| Precision | 35.6% |
| Recall | 66.0% |
| F1-score | 46.3% |
| Test ROC-AUC | 80.4% |
| 5-Fold CV ROC-AUC | 82.7% |

Because employee attrition is an imbalanced classification problem, recall and ROC-AUC were considered alongside accuracy.

## Project Structure

```text
employee-attrition/
├── data/
├── models/
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_baseline.ipynb
│   └── 04_model_comparison.ipynb
├── .gitignore
└── README.md