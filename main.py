from src.preprocess import load_and_preprocess
from src.train_model import train_lightgbm
from src.evaluate import evaluate_model
from src.explain import explain_model

def main():
    print("🔄 Loading & preprocessing data...")
    X_train, X_test, y_train, y_test, scaler, feature_names = load_and_preprocess()

    print("🚀 Training LightGBM model...")
    model = train_lightgbm(X_train, y_train)

    print("📊 Evaluating model...")
    metrics = evaluate_model(model, X_test, y_test)
    print("✅ Evaluation Metrics:", metrics)

    print("🔍 Generating SHAP explainability plot...")
    explain_model(X_train, feature_names)
    print("🎉 Done! Check the outputs/ folder for results.")

if __name__ == "__main__":
    main()
