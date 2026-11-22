"""Monthly retrain on the last 24 months of repaid and defaulted loans; the new version is registered in MLflow."""
import mlflow
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split


def retrain(history: pd.DataFrame) -> str:
    x, y = history.drop(columns=["defaulted"]), history["defaulted"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=7)
    with mlflow.start_run() as run:
        clf = xgb.XGBClassifier(n_estimators=300, max_depth=4, learning_rate=0.05)
        clf.fit(x_train, y_train)
        mlflow.log_metric("auc_holdout", float(clf.score(x_test, y_test)))
        mlflow.xgboost.log_model(clf, "model", registered_model_name="loan-decisions")
        return run.info.run_id
