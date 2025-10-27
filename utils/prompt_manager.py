"""
Prompt Manager - Zarządzanie promptami systemowymi
"""
import json
from pathlib import Path
from typing import Dict


class PromptManager:
    """Zarządzanie promptami dla różnych kroków workflow"""

    def __init__(self, default_prompts_path: str = "config/default_prompts.json"):
        self.default_path = Path(default_prompts_path)
        self.current_prompts = self.load_default_prompts()

    def load_default_prompts(self) -> Dict:
        """Wczytaj domyślne prompty z pliku"""
        if not self.default_path.exists():
            raise FileNotFoundError(f"Brak pliku z domyślnymi promptami: {self.default_path}")

        with open(self.default_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_prompt(self, step: str) -> str:
        """Pobierz prompt dla konkretnego kroku"""
        prompt_data = self.current_prompts.get(step, {})
        return prompt_data.get("system_prompt", "")

    def get_prompt_name(self, step: str) -> str:
        """Pobierz nazwę promptu"""
        prompt_data = self.current_prompts.get(step, {})
        return prompt_data.get("name", step)

    def update_prompt(self, step: str, new_prompt: str):
        """Aktualizuj prompt dla kroku"""
        if step in self.current_prompts:
            self.current_prompts[step]["system_prompt"] = new_prompt

    def reset_to_defaults(self):
        """Resetuj wszystkie prompty do domyślnych"""
        self.current_prompts = self.load_default_prompts()

    def reset_prompt(self, step: str):
        """Resetuj pojedynczy prompt do domyślnego"""
        defaults = self.load_default_prompts()
        if step in defaults:
            self.current_prompts[step] = defaults[step]

    def save_to_file(self, filepath: str):
        """Zapisz bieżącą konfigurację promptów do pliku"""
        path = Path(filepath)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.current_prompts, f, indent=2, ensure_ascii=False)

    def load_from_file(self, filepath: str):
        """Wczytaj konfigurację promptów z pliku"""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Plik nie istnieje: {filepath}")

        with open(path, 'r', encoding='utf-8') as f:
            self.current_prompts = json.load(f)

    def get_all_prompts(self) -> Dict:
        """Pobierz wszystkie aktualnie używane prompty"""
        return self.current_prompts

    def list_available_steps(self) -> list:
        """Listuj dostępne kroki z promptami"""
        return list(self.current_prompts.keys())

    def validate_prompts(self) -> bool:
        """Waliduj czy wszystkie wymagane prompty istnieją"""
        required_steps = ["step3_extraction", "step4_structure", "step5_finalization"]
        for step in required_steps:
            if step not in self.current_prompts:
                return False
            if not self.current_prompts[step].get("system_prompt"):
                return False
        return True
