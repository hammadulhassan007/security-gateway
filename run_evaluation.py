import csv
import json
import time
import os
import sys

# Append application path directory recursively to resolve modules smoothly
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "app"))

from detectors.rule_detector import calc_rule_risk
from detectors.semantic_detector import semantic_detector
from pii.presidio_custom import process_pii
from policy.policy_engine import evaluate_gateway_policy

def main():
    print("="*60)
    print("LAUNCHING QUANTITATIVE REPRODUCIBLE EVALUATION FRAMEWORK")
    print("="*60)

    csv_path = "data/final_eval.csv"
    if not os.path.exists(csv_path):
        print(f"[ERROR] Dataset not found at {csv_path}. Please generate it first.")
        return

    total = 0
    correct = 0
    tp, fp, tn, fn = 0, 0, 0, 0
    start_eval_time = time.time()

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt = row['prompt']
            expected_policy = row['expected_policy']
            
            # Execute Isolation pipeline
            r_score = calc_rule_risk(prompt)
            s_score = semantic_detector.calc_semantic_risk(prompt)
            pii_list, _ = process_pii(prompt)
            
            _, final_decision, _ = evaluate_gateway_policy(r_score, s_score, pii_list)

            # Map for basic Binary Confusion Matrix Calculations (Attack vs Safe)
            is_attack_expected = expected_policy == "BLOCK"
            is_attack_predicted = final_decision == "BLOCK"

            if is_attack_expected and is_attack_predicted:
                tp += 1
            elif not is_attack_expected and is_attack_predicted:
                fp += 1
            elif not is_attack_expected and not is_attack_predicted:
                tn += 1
            elif is_attack_expected and not is_attack_predicted:
                fn += 1

            if final_decision == expected_policy:
                correct += 1
            total += 1

    # Statistical Evaluation Computations
    accuracy = round((correct / total) * 100, 2) if total > 0 else 0
    precision = round(tp / (tp + fp), 4) if (tp + fp) > 0 else 0
    recall = round(tp / (tp + fn), 4) if (tp + fn) > 0 else 0
    f1_score = round(2 * (precision * recall) / (precision + recall), 4) if (precision + recall) > 0 else 0

    metrics_output = {
        "dataset_total_rows": total,
        "overall_pipeline_accuracy_percentage": accuracy,
        "confusion_matrix": {
            "true_positives": tp,
            "false_positives": fp,
            "true_negatives": tn,
            "false_negatives": fn
        },
        "metrics": {
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score
        },
        "evaluation_duration_secs": round(time.time() - start_eval_time, 2)
    }

    os.makedirs("results", exist_ok=True)
    with open("results/metrics_summary.json", "w", encoding="utf-8") as out_f:
        json.dump(metrics_output, out_f, indent=4)

    print("\n" + "="*40)
    print("📊 EVALUATION METRICS REPORT SUMMARY:")
    print("="*40)
    print(f"Total Rows Processed : {total}")
    print(f"Pipeline Accuracy    : {accuracy}%")
    print(f"Precision            : {precision}")
    print(f"Recall (Sensitivity) : {recall}")
    print(f"F1-Score             : {f1_score}")
    print("-" * 40)
    print("Confusion Matrix metrics successfully saved to 'results/metrics_summary.json'!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()