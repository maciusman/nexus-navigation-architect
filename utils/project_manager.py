"""
Project Manager - Zarządzanie projektami SEO
"""
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import shutil


class ProjectManager:
    """Zarządzanie projektami w strukturze folderowej"""

    def __init__(self, base_projects_dir: str = "projekty"):
        self.base_dir = Path(base_projects_dir)
        self.base_dir.mkdir(exist_ok=True)
        self.current_project_path: Optional[Path] = None

    def create_project(self, project_name: str) -> Path:
        """Utwórz nowy projekt z folderem"""
        project_path = self.base_dir / project_name
        project_path.mkdir(exist_ok=True)

        # Utwórz plik konfiguracyjny projektu
        config = {
            "project_name": project_name,
            "created_at": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "steps_completed": {
                "step1": False,
                "step2": False,
                "step3": False,
                "step4": False,
                "step5": False
            }
        }
        self._save_project_config(project_path, config)
        self.current_project_path = project_path
        return project_path

    def load_project(self, project_path: str) -> Dict:
        """Wczytaj istniejący projekt"""
        path = Path(project_path)
        if not path.exists():
            raise FileNotFoundError(f"Projekt nie istnieje: {project_path}")

        self.current_project_path = path
        return self._load_project_config(path)

    def list_projects(self) -> list:
        """Listuj wszystkie projekty"""
        projects = []
        for project_dir in self.base_dir.iterdir():
            if project_dir.is_dir():
                config_file = project_dir / "project_settings.json"
                if config_file.exists():
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    projects.append({
                        "name": project_dir.name,
                        "path": str(project_dir),
                        "created_at": config.get("created_at"),
                        "last_modified": config.get("last_modified")
                    })
        return sorted(projects, key=lambda x: x.get("last_modified", ""), reverse=True)

    def get_file_path(self, filename: str) -> Path:
        """Pobierz ścieżkę pliku w aktualnym projekcie"""
        if not self.current_project_path:
            raise ValueError("Brak aktywnego projektu")
        return self.current_project_path / filename

    def check_file_exists(self, filename: str) -> bool:
        """Sprawdź czy plik istnieje w projekcie"""
        if not self.current_project_path:
            return False
        return (self.current_project_path / filename).exists()

    def backup_file(self, filename: str) -> Optional[Path]:
        """Utwórz backup pliku przed nadpisaniem"""
        if not self.current_project_path:
            return None

        file_path = self.current_project_path / filename
        if not file_path.exists():
            return None

        # Folder backupów
        backup_dir = self.current_project_path / "backups"
        backup_dir.mkdir(exist_ok=True)

        # Nazwa z timestampem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{file_path.stem}_{timestamp}{file_path.suffix}"

        shutil.copy2(file_path, backup_path)
        return backup_path

    def update_step_status(self, step: str, completed: bool):
        """Aktualizuj status kroku"""
        if not self.current_project_path:
            return

        config = self._load_project_config(self.current_project_path)
        config["steps_completed"][step] = completed
        config["last_modified"] = datetime.now().isoformat()
        self._save_project_config(self.current_project_path, config)

    def get_steps_status(self) -> Dict[str, bool]:
        """Pobierz status kroków"""
        if not self.current_project_path:
            return {f"step{i}": False for i in range(1, 6)}

        config = self._load_project_config(self.current_project_path)
        return config.get("steps_completed", {})

    def _save_project_config(self, path: Path, config: Dict):
        """Zapisz konfigurację projektu"""
        config_file = path / "project_settings.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def _load_project_config(self, path: Path) -> Dict:
        """Wczytaj konfigurację projektu"""
        config_file = path / "project_settings.json"
        if not config_file.exists():
            return {}

        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_prompt_config(self, prompts: Dict) -> Path:
        """Zapisz konfigurację promptów w projekcie"""
        if not self.current_project_path:
            raise ValueError("Brak aktywnego projektu")

        config_file = self.current_project_path / "prompts_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(prompts, f, indent=2, ensure_ascii=False)

        return config_file

    def load_prompt_config(self) -> Optional[Dict]:
        """Wczytaj konfigurację promptów z projektu"""
        if not self.current_project_path:
            return None

        config_file = self.current_project_path / "prompts_config.json"
        if not config_file.exists():
            return None

        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
