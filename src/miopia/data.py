import pandas as pd

from miopia.config import RAW


def load_raw() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return X_train, Y_train, X_test exactly as provided by the professor."""
    X_train = pd.read_csv(RAW / "X_train.csv")
    Y_train = pd.read_csv(RAW / "Y_train.csv")
    X_test = pd.read_csv(RAW / "X_test.csv")
    return X_train, Y_train, X_test
