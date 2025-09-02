import lightgbm as lgb
import joblib

def train_lightgbm(X_train, y_train):
    # Tuned LightGBM for better accuracy
    model = lgb.LGBMClassifier(
        boosting_type='gbdt',
        num_leaves=63,
        max_depth=-1,
        learning_rate=0.03,
        n_estimators=500,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_samples=20,  # Prevent overfitting & too-small splits
        min_split_gain=0.001,  # Avoid negative split gains
        random_state=42
    )

    # Train model
    model.fit(X_train, y_train)

    # Save model
    joblib.dump(model, "outputs/model.pkl")

    return model
