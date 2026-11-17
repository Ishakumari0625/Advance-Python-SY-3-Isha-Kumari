
import pandas as pd
import numpy as np

# Create a Series of ten random numbers
np.random.seed(10)
s = pd.Series(np.random.randint(1, 101, 10))
print("Original Series:")
print(s)

# Indexing
print("Element at index 3:", s[3])

# Filtering
print("Numbers greater than 50:")
print(s[s > 50])

# Statistical operations
print("Mean:", s.mean())
print("Median:", s.median())
print("Minimum:", s.min())
print("Maximum:", s.max())
