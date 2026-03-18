#The Semantic Entropy Logic  
#To quantify "drift" or "garbage," we sample $N$ responses.  
#If the model says the same thing in ten different ways, entropy is low (Stable).  
#If it says ten different things, entropy is high (Drifting).  

import numpy as np
from typing import List, Dict

def calculate_semantic_entropy(cluster_probs: List[float]) -> float:
    """
    Computes Shannon Entropy over semantic clusters.
    SE = -sum(P(C) * log(P(C)))
    """
    # Normalize probabilities so they sum to 1
    probs = np.array(cluster_probs)
    probs /= probs.sum()
    
    # Calculate entropy, ignoring zero-probabilities
    entropy = -np.sum([p * np.log(p) for p in probs if p > 0])
    return float(entropy)

# Example: 
# Total 10 samples. 
# Cluster 1 (the "True" path) has 9 samples. 
# Cluster 2 (a hallucinated "Drift") has 1 sample.
samples_in_clusters = [0.9, 0.1] 
print(f"Stable SE: {calculate_semantic_entropy(samples_in_clusters):.4f}") 

# If 5 samples are in Cluster A and 5 in Cluster B (Pure Drift/Conflict)
messy_samples = [0.5, 0.5]
print(f"Drifting SE: {calculate_semantic_entropy(messy_samples):.4f}")
