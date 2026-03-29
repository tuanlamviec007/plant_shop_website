"""
Debug script v2: Check why 'cay kim tien' doesn't match in the ACTUAL ai_service.
"""
import os
import unicodedata
import re

# EXACT _normalize_text from ai_service.py 
def _normalize_text(text):
    if not text:
        return ""
    text = text.lower()
    # Remove punctuation but keep accented characters. 
    # Just simple regex for word chars and spaces
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

# Test various user inputs
tests = [
    "giá cả cây kim tiền",
    "giá cây kim tiền",
    "cây kim tiền",
    "cây sung",
    "giá cả cây sung",
]

plant_name = "cây kim tiền"
plant_name_norm = _normalize_text(plant_name)
print(f"plant_name_norm: {repr(plant_name_norm)}")

for ui in tests:
    norm = _normalize_text(ui)
    print(f"\nUser input: {repr(ui)}")
    print(f"  norm: {repr(norm)}")
    print(f"  Match: {plant_name_norm in norm}")

# Test 'giá cả' - maybe 'cả' gets split?
test_str = "giá cả cây kim tiền"
print(f"\n--- Testing 'giá cả cây kim tiền' character by character ---")
for ch in test_str:
    print(f"  {repr(ch)}: bytes={ch.encode('utf-8')}")
