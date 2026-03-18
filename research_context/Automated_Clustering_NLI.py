#The "Probe": Automated Clustering with NLI  
#To make this a "Probe" that can sit in your workflow, you need a way to group those responses.  
#We use a Natural Language Inference (NLI) model to check for "Entailment" (does Statement A mean the same as Statement B?).  

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Using a standard 2026-era NLI model for the "Security Guard"
nli_model_name = "cross-encoder/nli-deberta-v3-small"
tokenizer = AutoTokenizer.from_pretrained(nli_model_name)
model = AutoModelForSequenceClassification.from_pretrained(nli_model_name)

def are_semantically_equivalent(sent1: str, sent2: str) -> bool:
    """Uses NLI to check if two thoughts are the same."""
    features = tokenizer([(sent1, sent2)], padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        scores = model(**features).logits
        # Label 1 is typically 'neutral', 2 is 'entailment'
        # We look for high entailment scores in both directions (Bi-directional)
        label_mapping = ['contradiction', 'neutral', 'entailment']
        prediction = torch.softmax(scores, dim=1).argmax().item()
    
    return label_mapping[prediction] == 'entailment'

# --- The Probe Logic ---
responses = [
    "The capital of France is Paris.",
    "Paris is the capital of France.", # Same
    "Lyon is the capital of France."   # Drift!
]

clusters = [[responses[0]]]
for res in responses[1:]:
    matched = False
    for cluster in clusters:
        if are_semantically_equivalent(res, cluster[0]):
            cluster.append(res)
            matched = True
            break
    if not matched:
        clusters.append([res])

# Calculate cluster probabilities based on counts
cluster_counts = [len(c) for c in clusters]
se_score = calculate_semantic_entropy(cluster_counts)
print(f"Final Semantic Entropy Score: {se_score:.4f}")
