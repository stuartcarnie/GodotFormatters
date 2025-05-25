from godot_formatters.godot_types import (SYNTHETIC_PROVIDERS, SUMMARY_PROVIDERS)
from typing import Optional
import re

def get_synthetic_provider_for_type(type_name: str) -> Optional[type]:
    for pattern, provider in SYNTHETIC_PROVIDERS.items():
        if re.match(pattern, type_name):
            return provider
    return None

def get_summary_provider_for_type(type_name: str) -> Optional[object]:
    for pattern, provider in SUMMARY_PROVIDERS.items():
        if re.match(pattern, type_name):
            return provider
    return None
