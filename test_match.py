import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_shop.settings')
django.setup()

from plant_recommendation.ai_service import _normalize_text, _extract_intents_and_filters, _load_resources

config, model, plants = _load_resources()

text = "cây móng rồng"
norm_input = _normalize_text(text)
print("Norm input:", repr(norm_input))

for p in plants:
    if p['slug'] == 'cay-mong-rong':
        pname = p['name'].lower()
        print("Plant name:", repr(pname))
        print("Match?", pname in norm_input)

print("\nExtract test:")
intent, filters = _extract_intents_and_filters(text)
print(f"Intent={intent}, Filters={filters}")
