"""
Debug script: Check why 'cay kim tien' doesn't match in entity extraction.
The core question: does p['name'].lower() match inside norm_input?
"""
import os
import unicodedata
import re

# Simulate _normalize_text
def _normalize_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

# Simulate selected_plants.json data
plants = [
    {"name": "cây kim tiền", "slug": "cay-kim-tien"},
    {"name": "cây lưỡi hổ", "slug": "cay-luoi-ho"},
    {"name": "cây kim ngân", "slug": "cay-kim-ngan"},
    {"name": "cây sung", "slug": "cay-sung"},
]

user_input = "giá cả cây kim tiền"
norm_input = _normalize_text(user_input)
print(f"norm_input: {repr(norm_input)}")

for p in plants:
    p_name_lower = p['name'].lower()
    print(f"\nChecking: {repr(p_name_lower)}")
    print(f"  plant name bytes: {p_name_lower.encode('utf-8')}")
    print(f"  norm_input bytes containing substr: {p_name_lower.encode('utf-8') in norm_input.encode('utf-8')}")
    print(f"  match: {p_name_lower in norm_input}")

    # Check unicode normalization
    p_name_nfc = unicodedata.normalize('NFC', p_name_lower)
    p_name_nfd = unicodedata.normalize('NFD', p_name_lower)
    norm_nfc = unicodedata.normalize('NFC', norm_input)
    norm_nfd = unicodedata.normalize('NFD', norm_input)
    print(f"  NFC match: {p_name_nfc in norm_nfc}")
    print(f"  NFD match: {p_name_nfd in norm_nfd}")
