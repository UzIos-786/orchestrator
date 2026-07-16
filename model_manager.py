"""
=========================================================
Saad Python Project
model_manager.py
Version : 2.1
=========================================================

Model registry and helper functions.
"""

from typing import Dict, List

from config import AVAILABLE_MODELS, RESPONDENT_MODELS


class ModelManager:
    def __init__(self):
        if len(AVAILABLE_MODELS) != len(RESPONDENT_MODELS):
            raise ValueError(
                f"AVAILABLE_MODELS ({len(AVAILABLE_MODELS)}) and RESPONDENT_MODELS ({len(RESPONDENT_MODELS)}) must have the same length."
            )

        self._models: List[Dict[str, str]] = [
            {
                "display_name": display,
                "model_id": model_id,
            }
            for display, model_id in zip(AVAILABLE_MODELS, RESPONDENT_MODELS)
        ]

    def all_models(self) -> List[Dict[str, str]]:
        return self._models.copy()

    def model_ids(self) -> List[str]:
        return [m["model_id"] for m in self._models]

    def display_names(self) -> List[str]:
        return [m["display_name"] for m in self._models]

    def get_model_id(self, display_name: str) -> str | None:
        for model in self._models:
            if model["display_name"] == display_name:
                return model["model_id"]
        return None

    def get_display_name(self, model_id: str) -> str | None:
        for model in self._models:
            if model["model_id"] == model_id:
                return model["display_name"]
        return None


if __name__ == "__main__":
    manager = ModelManager()

    print("Configured Models")
    print("-" * 60)

    for model in manager.all_models():
        print(f'{model["display_name"]:12} -> {model["model_id"]}')