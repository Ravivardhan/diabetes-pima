import lightgbm as lgb
import joblib

def train_lightgbm(X_train, y_train):
    # Tuned LightGBM for better accuracy
    model = lgb.LGBMClassifier(
        boosting_type='gbdt',
        num_leaves=50,
        max_depth=-1,
        learning_rate=0.03,
        n_estimators=800,
        subsample=0.9,
        colsample_bytree=0.9,
        min_child_samples=30,
        min_split_gain=0.001,
        reg_alpha=0.1,
        reg_lambda=0.1,
        random_state=42
    )

    # Train model
    model.fit(X_train, y_train)

    # Save model
    joblib.dump(model, "outputs/model.pkl")

    return model
