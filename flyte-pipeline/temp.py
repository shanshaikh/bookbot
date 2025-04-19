import pandas as pd
import logging
import joblib
from flytekit import task, workflow
from flytekit.types.file import FlyteFile
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

#set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

@task
def load_and_split_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    # step 1: load dataset
    logging.info("loading dataset..")
    data = load_breast_cancer()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target, name="target")
    
    # step 2: splitting data
    logging.info("Splitting the data..")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

@task
def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> FlyteFile:
    logging.info("training the model..")
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    
    filename = "trained_model.joblib"
    joblib.dump(model, filename)
    return FlyteFile(path=filename)

@task
def evaluate_model(model_file: FlyteFile, X_test: pd.DataFrame, y_test: pd.Series) -> float:
    logging.info("predict and eval")
    model = joblib.load(model_file.download())  # download to local path
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_pred, y_test)
    logging.info(f"Model accuracy: {accuracy * 100:.2f}%")
    return float(accuracy)

@task
def save_model(model_file: FlyteFile, filename: str = "trained_breast_cancer_model.joblib") -> str:
    logging.info("saving model..")
    local_path = model_file.download()
    joblib.dump(joblib.load(local_path), filename)
    return filename

@workflow
def training_workflow() -> float:
    X_train, X_test, y_train, y_test = load_and_split_data()
    model_file = train_model(X_train=X_train, y_train=y_train)
    accuracy = evaluate_model(model_file=model_file, X_test=X_test, y_test=y_test)
    save_model(model_file=model_file, filename="trained_breast_cancer_model.joblib")
    return accuracy