"""
=========================================================
Saad Python Project
models.py
Version : 2.0
=========================================================

Central model definitions used across the project.
"""

from dataclasses import dataclass
from typing import List

from config import RESPONDENT_MODELS


@dataclass(frozen=True)
class AIModel:
    display_name: str
    model_id: str


def get_models() -> List[AIModel]:
    """
    Returns all configured AI models.
    """
    models = []
    for model_id in RESPONDENT_MODELS:
        display = model_id.split("/")[-1]
        models.append(AIModel(display_name=display, model_id=model_id))
    return models


def get_model_ids() -> List[str]:
    """
    Returns only the LiteLLM model IDs.
    """
    return [m.model_id for m in get_models()]


def model_exists(model_id: str) -> bool:
    """
    Check whether a model is configured.
    """
    return model_id in get_model_ids()


if __name__ == "__main__":
    print("Configured Models")
    print("-" * 40)
    for model in get_models():
        print(f"{model.display_name:25} -> {model.model_id}")
