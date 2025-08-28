import shap
import matplotlib.pyplot as plt
import joblib
import numpy as np

def explain_model(X_train, feature_names):
    # Load trained model
    model = joblib.load("outputs/model.pkl")

    # Initialize TreeExplainer
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_train)

    # Handle different SHAP versions safely
    if isinstance(shap_values, list):
        # Binary classification → use the positive class
        shap_vals = shap_values[1]
    else:
        shap_vals = shap_values

    # Ensure we have a 2D array
    shap_vals = np.array(shap_vals)
    if shap_vals.ndim == 1:
        shap_vals = shap_vals.reshape(-1, 1)

    # SHAP summary plot
    shap.summary_plot(shap_vals, X_train, feature_names=feature_names, show=False)
    plt.tight_layout()
    plt.savefig("outputs/shap_summary.png")
    plt.close()
