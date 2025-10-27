"""
Nexus Navigation Architect - SEO Category Builder 3.0
Profesjonalna aplikacja do budowy struktury kategorii e-commerce
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, simpledialog, PhotoImage
import json
import re
import threading
from pathlib import Path
from PIL import Image, ImageTk
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

# Import custom utilities
from utils import (
    ProjectManager,
    PromptManager,
    OpenRouterClient,
    JinaClient,
    SitemapParser
)
from utils.custom_widgets import ScrollableFrame, create_modern_checkbox_style


class DarkInputDialog(tk.Toplevel):
    """Custom input dialog z ciemnym motywem"""

    def __init__(self, parent, title, prompt):
        super().__init__(parent)
        self.result = None

        # Window setup
        self.title(title)
        self.geometry("400x150")
        self.configure(bg='#1a1a1a')
        self.resizable(False, False)

        # Center window
        self.transient(parent)
        self.grab_set()

        # Content frame
        content = tk.Frame(self, bg='#1a1a1a', padx=20, pady=20)
        content.pack(fill="both", expand=True)

        # Prompt label
        prompt_label = tk.Label(content, text=prompt,
                               bg='#1a1a1a', fg='#e0e0e0',
                               font=('Inter', 10))
        prompt_label.pack(anchor="w", pady=(0, 10))

        # Entry
        self.entry = tk.Entry(content, bg='#2a2a2a', fg='#e0e0e0',
                             insertbackground='#f97316',
                             font=('Inter', 10),
                             relief=tk.FLAT,
                             highlightthickness=1,
                             highlightbackground='#3a3a3a',
                             highlightcolor='#f97316')
        self.entry.pack(fill="x", pady=(0, 15))
        self.entry.focus_set()
        self.entry.bind('<Return>', lambda e: self.ok_clicked())
        self.entry.bind('<Escape>', lambda e: self.cancel_clicked())

        # Buttons frame
        btn_frame = tk.Frame(content, bg='#1a1a1a')
        btn_frame.pack(fill="x")

        # OK button
        ok_btn = tk.Button(btn_frame, text="OK",
                          command=self.ok_clicked,
                          bg='#f97316', fg='#ffffff',
                          font=('Inter', 9, 'bold'),
                          relief=tk.FLAT,
                          padx=20, pady=5,
                          cursor='hand2')
        ok_btn.pack(side="right", padx=(5, 0))

        # Cancel button
        cancel_btn = tk.Button(btn_frame, text="Anuluj",
                              command=self.cancel_clicked,
                              bg='#2a2a2a', fg='#e0e0e0',
                              font=('Inter', 9),
                              relief=tk.FLAT,
                              padx=20, pady=5,
                              cursor='hand2')
        cancel_btn.pack(side="right")

    def ok_clicked(self):
        """Potwierdzenie"""
        self.result = self.entry.get()
        self.destroy()

    def cancel_clicked(self):
        """Anulowanie"""
        self.result = None
        self.destroy()


class NexusNavigationApp:
    """Główna aplikacja Nexus Navigation Architect"""

    def __init__(self, root):
        self.root = root
        self.root.title("Nexus Navigation Architect")
        self.root.geometry("1400x900")

        # Set window icon
        try:
            icon_path = Path("assety/logo.ico")
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except Exception as e:
            print(f"Could not set icon: {e}")

        # Managers
        self.project_manager = ProjectManager()
        self.prompt_manager = PromptManager()
        self.openrouter_client = None
        self.jina_client = None

        # Variables - API Keys
        self.openrouter_api_key = tk.StringVar()
        self.jina_api_key = tk.StringVar()

        # Variables - Global Settings
        self.current_project_path = tk.StringVar(value="")
        self.sitemap_url = tk.StringVar()
        self.url_filter_pattern = tk.StringVar(value=".html")

        # Variables - Step Settings
        self.num_threads_jina = tk.IntVar(value=10)
        self.max_retries_jina = tk.IntVar(value=3)
        self.num_threads_extract = tk.IntVar(value=1)
        self.max_retries_extract = tk.IntVar(value=4)
        self.batch_size = tk.IntVar(value=100)
        self.num_threads_batch = tk.IntVar(value=10)
        self.max_retries_batch = tk.IntVar(value=3)
        self.max_retries_final = tk.IntVar(value=3)

        # Variables - Model Selection
        self.model_step3 = tk.StringVar()
        self.model_step4 = tk.StringVar()
        self.model_step5 = tk.StringVar()

        # Variables - Step Selection
        self.run_step1 = tk.BooleanVar(value=False)
        self.run_step2 = tk.BooleanVar(value=False)
        self.run_step3 = tk.BooleanVar(value=False)
        self.run_step4 = tk.BooleanVar(value=False)
        self.run_step5 = tk.BooleanVar(value=False)

        # Variables - Workflow Mode
        self.supervised_mode = tk.BooleanVar(value=False)

        # Processing state
        self.processing = False
        self.waiting_for_confirmation = False
        self.current_step = 0
        self.last_completed_step = 0  # Tracking postępu dla resume
        self.available_models = []
        self.models_loaded = False

        # Setup Dark Theme
        self.setup_dark_theme()

        # Setup UI
        self.setup_ui()

        # Check existing files
        self.refresh_project_status()

    def setup_dark_theme(self):
        """Konfiguracja ciemnego motywu wzorowanego na Theme Dark Template"""
        style = ttk.Style()
        style.theme_use('default')

        # Kolory z Theme Dark Template
        bg_dark = '#0f0f0f'
        bg_panel = '#1a1a1a'
        bg_input = '#2a2a2a'
        fg_primary = '#e0e0e0'
        fg_secondary = '#9ca3af'
        accent_orange = '#f97316'
        border_color = '#2a2a2a'

        # Konfiguracja root window
        self.root.configure(bg=bg_dark)

        # Globalne opcje dla popup menu (Combobox dropdown)
        self.root.option_add('*TCombobox*Listbox.background', bg_input)
        self.root.option_add('*TCombobox*Listbox.foreground', fg_primary)
        self.root.option_add('*TCombobox*Listbox.selectBackground', accent_orange)
        self.root.option_add('*TCombobox*Listbox.selectForeground', '#ffffff')

        # Configure ttk styles
        style.configure('Dark.TFrame', background=bg_panel)
        style.configure('Dark.TLabel', background=bg_panel, foreground=fg_primary)
        style.configure('Dark.TLabelframe', background=bg_panel, foreground=accent_orange, bordercolor=border_color)
        style.configure('Dark.TLabelframe.Label', background=bg_panel, foreground=accent_orange, font=('Inter', 10, 'bold'))

        style.configure('Dark.TButton',
                        background=bg_input,
                        foreground=fg_primary,
                        bordercolor=border_color,
                        focuscolor=accent_orange,
                        lightcolor=bg_input,
                        darkcolor=bg_input,
                        padding=[15, 8],
                        relief='flat')

        style.map('Dark.TButton',
                  background=[('active', accent_orange), ('pressed', accent_orange), ('hover', '#323232')],
                  foreground=[('active', '#ffffff'), ('hover', '#ffffff')],
                  bordercolor=[('focus', accent_orange)])

        style.configure('Accent.TButton',
                        background=accent_orange,
                        foreground='#ffffff',
                        font=('Inter', 10, 'bold'),
                        padding=[15, 8],
                        relief='flat')

        style.map('Accent.TButton',
                  background=[('active', '#ff8533'), ('pressed', '#d16613'), ('hover', '#ff8533')],
                  foreground=[('active', '#ffffff')])

        style.configure('Dark.TEntry',
                        fieldbackground=bg_input,
                        background=bg_input,
                        foreground=fg_primary,
                        bordercolor=border_color,
                        insertcolor=fg_primary)

        style.configure('Dark.TCheckbutton',
                        background=bg_panel,
                        foreground=fg_primary,
                        font=('Inter', 10))

        # Highlighted state for checkboxes
        style.map('Dark.TCheckbutton',
                 background=[('active', '#242424')],
                 foreground=[('selected', accent_orange), ('active', accent_orange)])

        # Create modern checkbox style
        create_modern_checkbox_style()

        style.configure('Dark.TCombobox',
                        fieldbackground=bg_input,
                        background=bg_input,
                        foreground=fg_primary,
                        arrowcolor=accent_orange,
                        selectbackground=accent_orange,
                        selectforeground='#ffffff')

        # Map states dla Combobox
        style.map('Dark.TCombobox',
                 fieldbackground=[('readonly', bg_input), ('disabled', '#1f1f1f')],
                 background=[('readonly', bg_input), ('disabled', '#1f1f1f')],
                 foreground=[('readonly', fg_primary), ('disabled', fg_secondary)],
                 selectbackground=[('readonly', accent_orange)])

        style.configure('Dark.TSpinbox',
                        fieldbackground=bg_input,
                        background=bg_input,
                        foreground=fg_primary,
                        bordercolor=border_color,
                        arrowcolor=accent_orange,
                        insertcolor=fg_primary,
                        selectbackground=accent_orange,
                        selectforeground='#ffffff')

        # Map states dla Spinbox
        style.map('Dark.TSpinbox',
                 fieldbackground=[('readonly', bg_input), ('disabled', '#1f1f1f')],
                 background=[('readonly', bg_input), ('disabled', '#1f1f1f')],
                 foreground=[('readonly', fg_primary), ('disabled', fg_secondary)])

        style.configure('Dark.TNotebook', background=bg_panel, bordercolor=border_color)
        style.configure('Dark.TNotebook.Tab',
                        background=bg_input,
                        foreground=fg_secondary,
                        padding=[20, 10])
        style.map('Dark.TNotebook.Tab',
                  background=[('selected', bg_panel)],
                  foreground=[('selected', accent_orange)])

        # Progressbar
        style.configure('Dark.Horizontal.TProgressbar',
                        background=accent_orange,
                        troughcolor=bg_input,
                        bordercolor=border_color,
                        lightcolor=accent_orange,
                        darkcolor=accent_orange)

    def setup_ui(self):
        """Główna konfiguracja interfejsu użytkownika"""
        # Main container
        main_container = ttk.Frame(self.root, style='Dark.TFrame')
        main_container.pack(fill="both", expand=True)

        # Header with logo and title
        self.setup_header(main_container)

        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_container, style='Dark.TNotebook')
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1: Settings
        self.tab_settings = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.tab_settings, text="⚙️  Ustawienia")
        self.setup_tab_settings()

        # Tab 2: Workflow
        self.tab_workflow = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.tab_workflow, text="🔄  Workflow")
        self.setup_tab_workflow()

        # Tab 3: Prompt Editor
        self.tab_prompts = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.tab_prompts, text="📝  Edytor Promptów")
        self.setup_tab_prompts()

    def setup_header(self, parent):
        """Nagłówek z logo i nazwą aplikacji"""
        header_frame = ttk.Frame(parent, style='Dark.TFrame')
        header_frame.pack(fill="x", padx=20, pady=10)

        # Logo
        try:
            logo_img = Image.open("assety/logo_small.png")
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(header_frame, image=logo_photo, bg='#1a1a1a')
            logo_label.image = logo_photo  # Keep reference
            logo_label.pack(side="left", padx=(0, 15))
        except Exception as e:
            print(f"Could not load logo: {e}")

        # Title
        title_frame = ttk.Frame(header_frame, style='Dark.TFrame')
        title_frame.pack(side="left", fill="x", expand=True)

        title_label = tk.Label(title_frame,
                               text="Nexus Navigation Architect",
                               font=('Inter', 18, 'bold'),
                               fg='#a855f7',
                               bg='#1a1a1a')
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(title_frame,
                                  text="SEO Category Builder 3.0 · Professional E-commerce Navigation Structure Generator",
                                  font=('Inter', 9),
                                  fg='#9ca3af',
                                  bg='#1a1a1a')
        subtitle_label.pack(anchor="w")

    def setup_tab_settings(self):
        """Tab 1: Ustawienia globalne"""
        # Modern scrollable frame
        scrollable_container = ScrollableFrame(self.tab_settings)
        scrollable_container.pack(fill="both", expand=True)

        # Content
        content = ttk.Frame(scrollable_container.scrollable_frame, style='Dark.TFrame')
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # API Keys Section
        api_frame = ttk.LabelFrame(content, text="Klucze API", padding="15", style='Dark.TLabelframe')
        api_frame.pack(fill="x", pady=(0, 15))

        # OpenRouter API
        ttk.Label(api_frame, text="OpenRouter API Key:", style='Dark.TLabel').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        openrouter_entry = ttk.Entry(api_frame, textvariable=self.openrouter_api_key, width=60, show="*", style='Dark.TEntry')
        openrouter_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        load_models_btn = ttk.Button(api_frame, text="Załaduj modele", command=self.load_models, style='Dark.TButton')
        load_models_btn.grid(row=0, column=2, padx=5)

        ttk.Label(api_frame, text="https://openrouter.ai/keys", style='Dark.TLabel', foreground='#60a5fa').grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=0)

        # Jina API
        ttk.Label(api_frame, text="Jina AI API Key:", style='Dark.TLabel').grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        jina_entry = ttk.Entry(api_frame, textvariable=self.jina_api_key, width=60, show="*", style='Dark.TEntry')
        jina_entry.grid(row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        ttk.Label(api_frame, text="https://jina.ai/reader - potrzebne dla kroku 2", style='Dark.TLabel', foreground='#60a5fa').grid(
            row=3, column=1, sticky=tk.W, padx=5, pady=0)

        api_frame.columnconfigure(1, weight=1)

        # Project Management Section
        project_frame = ttk.LabelFrame(content, text="Zarządzanie Projektem", padding="15", style='Dark.TLabelframe')
        project_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(project_frame, text="Folder projektu:", style='Dark.TLabel').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        project_path_entry = ttk.Entry(project_frame, textvariable=self.current_project_path, width=50, style='Dark.TEntry')
        project_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        browse_btn = ttk.Button(project_frame, text="Wybierz", command=self.browse_project_folder, style='Dark.TButton')
        browse_btn.grid(row=0, column=2, padx=5)

        new_project_btn = ttk.Button(project_frame, text="Nowy projekt", command=self.create_new_project, style='Dark.TButton')
        new_project_btn.grid(row=0, column=3, padx=5)

        project_frame.columnconfigure(1, weight=1)

    def setup_tab_workflow(self):
        """Tab 2: Workflow (kroki 1-5)"""
        # Modern scrollable frame
        scrollable_container = ScrollableFrame(self.tab_workflow)
        scrollable_container.pack(fill="both", expand=True)

        # Content
        content = ttk.Frame(scrollable_container.scrollable_frame, style='Dark.TFrame')
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Info label
        info_label = tk.Label(content,
                              text="Wybierz kroki do wykonania i skonfiguruj ustawienia dla każdego kroku",
                              font=('Inter', 10),
                              fg='#9ca3af',
                              bg='#1a1a1a')
        info_label.pack(anchor="w", pady=(0, 15))

        # Steps Section
        self.setup_all_steps(content)

        # Progress Section
        progress_frame = ttk.LabelFrame(content, text="Postęp Przetwarzania", padding="15", style='Dark.TLabelframe')
        progress_frame.pack(fill="x", pady=(15, 0))

        # Workflow mode selection
        mode_frame = ttk.Frame(progress_frame, style='Dark.TFrame')
        mode_frame.pack(fill="x", pady=(0, 10))

        supervised_check = ttk.Checkbutton(mode_frame,
                                          text="Tryb nadzorowany (Human-in-the-loop)",
                                          variable=self.supervised_mode,
                                          style='Dark.TCheckbutton')
        supervised_check.pack(side="left")

        mode_info = tk.Label(mode_frame,
                           text="ℹ️ W trybie nadzorowanym workflow zatrzymuje się po każdym kroku i czeka na potwierdzenie",
                           font=('Inter', 8), fg='#6b7280', bg='#1a1a1a')
        mode_info.pack(side="left", padx=15)

        self.progress_var = tk.StringVar(value="Gotowy do rozpoczęcia")
        progress_label = tk.Label(progress_frame, textvariable=self.progress_var,
                                  font=('Inter', 9), fg='#e0e0e0', bg='#1a1a1a')
        progress_label.pack(anchor="w", pady=(0, 10))

        self.progress_bar = ttk.Progressbar(progress_frame, length=600, mode='determinate', style='Dark.Horizontal.TProgressbar')
        self.progress_bar.pack(fill="x", pady=(0, 10))

        # Buttons
        btn_frame = ttk.Frame(progress_frame, style='Dark.TFrame')
        btn_frame.pack(fill="x")

        self.start_button = ttk.Button(btn_frame, text="▶ Start Workflow", command=self.start_workflow, style='Accent.TButton', state=tk.DISABLED)
        self.start_button.pack(side="left", padx=5)

        self.continue_button = ttk.Button(btn_frame, text="▶ Kontynuuj", command=self.continue_workflow, style='Accent.TButton', state=tk.DISABLED)
        self.continue_button.pack(side="left", padx=5)

        self.stop_button = ttk.Button(btn_frame, text="⏸ Stop", command=self.stop_workflow, style='Dark.TButton', state=tk.DISABLED)
        self.stop_button.pack(side="left", padx=5)

        refresh_btn = ttk.Button(btn_frame, text="🔄 Odśwież Status", command=self.refresh_project_status, style='Dark.TButton')
        refresh_btn.pack(side="left", padx=5)

        # Logs Section
        log_frame = ttk.LabelFrame(content, text="Logi Przetwarzania", padding="15", style='Dark.TLabelframe')
        log_frame.pack(fill="both", expand=True, pady=(15, 0))

        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=90,
                                                   bg='#0f0f0f', fg='#e0e0e0',
                                                   insertbackground='#f97316',
                                                   font=('Consolas', 9))
        self.log_text.pack(fill="both", expand=True)

    def setup_all_steps(self, parent):
        """Setup wszystkich kroków workflow"""
        # Krok 1
        self.setup_step1(parent)
        # Krok 2
        self.setup_step2(parent)
        # Krok 3
        self.setup_step3(parent)
        # Krok 4
        self.setup_step4(parent)
        # Krok 5
        self.setup_step5(parent)

    # Kontynuacja w kolejnym komentarzu - ten plik jest za duży, więc podzielę implementację
    # Najpierw utworzę bazową strukturę, a potem dodam pozostałe metody

    def setup_step1(self, parent):
        """Krok 1: Pobranie listy produktów z sitemap lub pliku"""
        step_frame = ttk.LabelFrame(parent, text="Krok 1: Pobranie listy produktów", padding="10", style='Dark.TLabelframe')
        step_frame.pack(fill="x", pady=(0, 10))

        # Checkbox + Status
        check_status_frame = ttk.Frame(step_frame, style='Dark.TFrame')
        check_status_frame.pack(fill="x", pady=(0, 10))

        self.step1_check = ttk.Checkbutton(check_status_frame, text="Uruchom krok 1", variable=self.run_step1, style='Dark.TCheckbutton')
        self.step1_check.pack(side="left")

        self.step1_status = tk.Label(check_status_frame, text="", font=('Inter', 9), bg='#1a1a1a')
        self.step1_status.pack(side="left", padx=15)

        # Settings
        settings_frame = ttk.Frame(step_frame, style='Dark.TFrame')
        settings_frame.pack(fill="x")

        # Option 1: Sitemap
        ttk.Label(settings_frame, text="Opcja A - Z sitemap:", style='Dark.TLabel', font=('Inter', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=(5, 2), columnspan=3)

        ttk.Label(settings_frame, text="URL Sitemap:", style='Dark.TLabel').grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        sitemap_entry = ttk.Entry(settings_frame, textvariable=self.sitemap_url, width=60, style='Dark.TEntry')
        sitemap_entry.grid(row=1, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))

        ttk.Label(settings_frame, text="Filtr URL:", style='Dark.TLabel').grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        filter_entry = ttk.Entry(settings_frame, textvariable=self.url_filter_pattern, width=30, style='Dark.TEntry')
        filter_entry.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        ttk.Label(settings_frame, text="(np. '.html', '/product/')", style='Dark.TLabel', foreground='#6b7280').grid(row=2, column=2, sticky=tk.W, padx=5)

        # Separator
        separator = ttk.Separator(settings_frame, orient='horizontal')
        separator.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # Option 2: File upload
        ttk.Label(settings_frame, text="Opcja B - Z pliku TXT:", style='Dark.TLabel', font=('Inter', 9, 'bold')).grid(row=4, column=0, sticky=tk.W, padx=5, pady=(5, 2), columnspan=3)

        self.upload_file_path = tk.StringVar()
        ttk.Label(settings_frame, text="Plik z URL-ami:", style='Dark.TLabel').grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        file_label = tk.Label(settings_frame, textvariable=self.upload_file_path,
                             bg='#2a2a2a', fg='#e0e0e0', anchor='w',
                             font=('Inter', 9), relief=tk.FLAT, padx=5, pady=3)
        file_label.grid(row=5, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))

        browse_file_btn = ttk.Button(settings_frame, text="Wybierz plik", command=self.browse_urls_file, style='Dark.TButton')
        browse_file_btn.grid(row=5, column=2, padx=5, pady=2)

        ttk.Label(settings_frame, text="ℹ️ Plik TXT z URL-ami (jeden URL na linię)", style='Dark.TLabel', foreground='#6b7280').grid(row=6, column=1, sticky=tk.W, padx=5, pady=(0, 5), columnspan=2)

        settings_frame.columnconfigure(1, weight=1)

    def setup_step2(self, parent):
        """Krok 2: Pobranie opisów produktów"""
        step_frame = ttk.LabelFrame(parent, text="Krok 2: Pobranie opisów produktów (Jina Reader)", padding="10", style='Dark.TLabelframe')
        step_frame.pack(fill="x", pady=(0, 10))

        # Checkbox + Status
        check_status_frame = ttk.Frame(step_frame, style='Dark.TFrame')
        check_status_frame.pack(fill="x", pady=(0, 10))

        self.step2_check = ttk.Checkbutton(check_status_frame, text="Uruchom krok 2", variable=self.run_step2, style='Dark.TCheckbutton')
        self.step2_check.pack(side="left")

        self.step2_status = tk.Label(check_status_frame, text="", font=('Inter', 9), bg='#1a1a1a')
        self.step2_status.pack(side="left", padx=15)

        # Settings
        settings_frame = ttk.Frame(step_frame, style='Dark.TFrame')
        settings_frame.pack(fill="x")

        ttk.Label(settings_frame, text="Wątki Jina:", style='Dark.TLabel').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(settings_frame, from_=1, to=20, textvariable=self.num_threads_jina, width=10, style='Dark.TSpinbox').grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(settings_frame, text="Powtórzenia:", style='Dark.TLabel').grid(row=0, column=2, sticky=tk.W, padx=(20,5), pady=5)
        ttk.Spinbox(settings_frame, from_=1, to=5, textvariable=self.max_retries_jina, width=10, style='Dark.TSpinbox').grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

    def setup_step3(self, parent):
        """Krok 3: Ekstrakcja parametrów"""
        step_frame = ttk.LabelFrame(parent, text="Krok 3: Ekstrakcja parametrów produktów (AI)", padding="10", style='Dark.TLabelframe')
        step_frame.pack(fill="x", pady=(0, 10))

        # Checkbox + Status
        check_status_frame = ttk.Frame(step_frame, style='Dark.TFrame')
        check_status_frame.pack(fill="x", pady=(0, 10))

        self.step3_check = ttk.Checkbutton(check_status_frame, text="Uruchom krok 3", variable=self.run_step3, style='Dark.TCheckbutton')
        self.step3_check.pack(side="left")

        self.step3_status = tk.Label(check_status_frame, text="", font=('Inter', 9), bg='#1a1a1a')
        self.step3_status.pack(side="left", padx=15)

        # Settings
        settings_frame = ttk.Frame(step_frame, style='Dark.TFrame')
        settings_frame.pack(fill="x")

        ttk.Label(settings_frame, text="Model AI:", style='Dark.TLabel').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.model3_combo = ttk.Combobox(settings_frame, textvariable=self.model_step3, width=50, state="readonly")
        self.model3_combo.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        # Wyłącz scroll aby uniknąć przypadkowej zmiany
        self.model3_combo.unbind_class("TCombobox", "<MouseWheel>")
        self.model3_combo.unbind_class("TCombobox", "<Button-4>")
        self.model3_combo.unbind_class("TCombobox", "<Button-5>")

        ttk.Label(settings_frame, text="💡 Zalecane: szybkie/tanie", style='Dark.TLabel', foreground='#6b7280').grid(row=0, column=2, sticky=tk.W, padx=5)

        ttk.Label(settings_frame, text="Wątki:", style='Dark.TLabel').grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(settings_frame, from_=1, to=30, textvariable=self.num_threads_extract, width=10, style='Dark.TSpinbox').grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(settings_frame, text="Powtórzenia:", style='Dark.TLabel').grid(row=1, column=2, sticky=tk.W, padx=(20,5), pady=5)
        ttk.Spinbox(settings_frame, from_=1, to=5, textvariable=self.max_retries_extract, width=10, style='Dark.TSpinbox').grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

        settings_frame.columnconfigure(1, weight=1)

    def setup_step4(self, parent):
        """Krok 4: Budowa struktury kategorii"""
        step_frame = ttk.LabelFrame(parent, text="Krok 4: Budowa struktury kategorii (AI)", padding="10", style='Dark.TLabelframe')
        step_frame.pack(fill="x", pady=(0, 10))

        # Checkbox + Status
        check_status_frame = ttk.Frame(step_frame, style='Dark.TFrame')
        check_status_frame.pack(fill="x", pady=(0, 10))

        self.step4_check = ttk.Checkbutton(check_status_frame, text="Uruchom krok 4", variable=self.run_step4, style='Dark.TCheckbutton')
        self.step4_check.pack(side="left")

        self.step4_status = tk.Label(check_status_frame, text="", font=('Inter', 9), bg='#1a1a1a')
        self.step4_status.pack(side="left", padx=15)

        # Settings
        settings_frame = ttk.Frame(step_frame, style='Dark.TFrame')
        settings_frame.pack(fill="x")

        ttk.Label(settings_frame, text="Model AI:", style='Dark.TLabel').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.model4_combo = ttk.Combobox(settings_frame, textvariable=self.model_step4, width=50, state="readonly")
        self.model4_combo.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        # Wyłącz scroll aby uniknąć przypadkowej zmiany
        self.model4_combo.unbind_class("TCombobox", "<MouseWheel>")
        self.model4_combo.unbind_class("TCombobox", "<Button-4>")
        self.model4_combo.unbind_class("TCombobox", "<Button-5>")

        ttk.Label(settings_frame, text="💡 Zalecane: szybkie", style='Dark.TLabel', foreground='#6b7280').grid(row=0, column=2, sticky=tk.W, padx=5)

        ttk.Label(settings_frame, text="Rozmiar paczki:", style='Dark.TLabel').grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(settings_frame, from_=10, to=100, textvariable=self.batch_size, width=10, increment=5, style='Dark.TSpinbox').grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(settings_frame, text="Wątki batch:", style='Dark.TLabel').grid(row=1, column=2, sticky=tk.W, padx=(20,5), pady=5)
        ttk.Spinbox(settings_frame, from_=1, to=10, textvariable=self.num_threads_batch, width=10, style='Dark.TSpinbox').grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

        settings_frame.columnconfigure(1, weight=1)

    def setup_step5(self, parent):
        """Krok 5: Finalizacja"""
        step_frame = ttk.LabelFrame(parent, text="Krok 5: Finalizacja i optymalizacja (AI)", padding="10", style='Dark.TLabelframe')
        step_frame.pack(fill="x", pady=(0, 10))

        # Checkbox + Status
        check_status_frame = ttk.Frame(step_frame, style='Dark.TFrame')
        check_status_frame.pack(fill="x", pady=(0, 10))

        self.step5_check = ttk.Checkbutton(check_status_frame, text="Uruchom krok 5", variable=self.run_step5, style='Dark.TCheckbutton')
        self.step5_check.pack(side="left")

        self.step5_status = tk.Label(check_status_frame, text="", font=('Inter', 9), bg='#1a1a1a')
        self.step5_status.pack(side="left", padx=15)

        # Settings
        settings_frame = ttk.Frame(step_frame, style='Dark.TFrame')
        settings_frame.pack(fill="x")

        ttk.Label(settings_frame, text="Model AI:", style='Dark.TLabel').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.model5_combo = ttk.Combobox(settings_frame, textvariable=self.model_step5, width=50, state="readonly")
        self.model5_combo.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        # Wyłącz scroll aby uniknąć przypadkowej zmiany
        self.model5_combo.unbind_class("TCombobox", "<MouseWheel>")
        self.model5_combo.unbind_class("TCombobox", "<Button-4>")
        self.model5_combo.unbind_class("TCombobox", "<Button-5>")

        ttk.Label(settings_frame, text="💡 Zalecane: reasoning (o1, QwQ, DeepSeek)", style='Dark.TLabel', foreground='#6b7280').grid(row=0, column=2, sticky=tk.W, padx=5)

        ttk.Label(settings_frame, text="Powtórzenia:", style='Dark.TLabel').grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Spinbox(settings_frame, from_=1, to=5, textvariable=self.max_retries_final, width=10, style='Dark.TSpinbox').grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        settings_frame.columnconfigure(1, weight=1)

    def setup_tab_prompts(self):
        """Tab 3: Edytor promptów"""
        # Main frame
        content = ttk.Frame(self.tab_prompts, style='Dark.TFrame')
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Info
        info_label = tk.Label(content,
                              text="Edytuj prompty systemowe dla kroków 3-5. Możesz zapisać/wczytać konfigurację lub zresetować do domyślnych.",
                              font=('Inter', 10),
                              fg='#9ca3af',
                              bg='#1a1a1a')
        info_label.pack(anchor="w", pady=(0, 15))

        # Buttons
        btn_frame = ttk.Frame(content, style='Dark.TFrame')
        btn_frame.pack(fill="x", pady=(0, 15))

        ttk.Button(btn_frame, text="💾 Zapisz konfigurację", command=self.save_prompt_config, style='Dark.TButton').pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📂 Wczytaj konfigurację", command=self.load_prompt_config, style='Dark.TButton').pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔄 Resetuj do domyślnych", command=self.reset_prompts, style='Dark.TButton').pack(side="left", padx=5)

        # Notebook dla promptów
        prompts_notebook = ttk.Notebook(content, style='Dark.TNotebook')
        prompts_notebook.pack(fill="both", expand=True)

        # Prompty dla kroków 3, 4, 5
        self.prompt_editors = {}
        for step_key, step_name in [
            ("step3_extraction", "Krok 3: Ekstrakcja"),
            ("step4_structure", "Krok 4: Struktura"),
            ("step5_finalization", "Krok 5: Finalizacja")
        ]:
            tab = ttk.Frame(prompts_notebook, style='Dark.TFrame')
            prompts_notebook.add(tab, text=step_name)

            # Text editor
            text_widget = scrolledtext.ScrolledText(tab, height=25, width=100,
                                                     bg='#0f0f0f', fg='#e0e0e0',
                                                     insertbackground='#f97316',
                                                     font=('Consolas', 9),
                                                     wrap=tk.WORD)
            text_widget.pack(fill="both", expand=True, padx=10, pady=10)

            # Load current prompt
            prompt_text = self.prompt_manager.get_prompt(step_key)
            text_widget.insert("1.0", prompt_text)

            self.prompt_editors[step_key] = text_widget

    # ============ HELPER METHODS ============

    def log(self, message):
        """Dodaj wpis do logów"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def update_progress(self, message, value=None):
        """Aktualizuj pasek postępu"""
        self.progress_var.set(message)
        if value is not None:
            self.progress_bar['value'] = value
        self.root.update_idletasks()

    # ============ PROJECT MANAGEMENT ============

    def browse_project_folder(self):
        """Wybierz folder projektu"""
        folder = filedialog.askdirectory(title="Wybierz folder projektu")
        if folder:
            try:
                self.project_manager.load_project(folder)
                self.current_project_path.set(folder)
                self.log(f"✓ Wczytano projekt: {folder}")
                self.refresh_project_status()
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się wczytać projektu: {e}")

    def create_new_project(self):
        """Utwórz nowy projekt"""
        dialog = DarkInputDialog(self.root, "Nowy projekt", "Podaj nazwę projektu:")
        self.root.wait_window(dialog)
        project_name = dialog.result
        if project_name:
            try:
                project_path = self.project_manager.create_project(project_name)
                self.current_project_path.set(str(project_path))
                self.log(f"✓ Utworzono nowy projekt: {project_name}")
                self.refresh_project_status()
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się utworzyć projektu: {e}")

    def refresh_project_status(self):
        """Odśwież status wszystkich kroków"""
        if not self.project_manager.current_project_path:
            return

        # Check step files
        step1_done = self.project_manager.check_file_exists("products.txt")
        step2_done = self.project_manager.check_file_exists("content_website.json")
        step3_done = self.project_manager.check_file_exists("product_extraction.json")
        step4_done = self.project_manager.check_file_exists("categories_structure.json")
        step5_done = self.project_manager.check_file_exists("categories_final.json")

        # Update status labels
        self.update_step_status(self.step1_status, self.run_step1, step1_done)
        self.update_step_status(self.step2_status, self.run_step2, step2_done)
        self.update_step_status(self.step3_status, self.run_step3, step3_done)
        self.update_step_status(self.step4_status, self.run_step4, step4_done)
        self.update_step_status(self.step5_status, self.run_step5, step5_done)

    def update_step_status(self, label_widget, var_bool, is_done):
        """Aktualizuj status pojedynczego kroku"""
        if is_done:
            label_widget.config(text="✅ Wykonane", fg="#10b981")
            var_bool.set(False)
        else:
            label_widget.config(text="⏸️ Do wykonania", fg="#f59e0b")
            var_bool.set(True)

    def browse_urls_file(self):
        """Wybierz plik TXT z URL-ami"""
        filename = filedialog.askopenfilename(
            title="Wybierz plik z URL-ami",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.upload_file_path.set(filename)
            self.log(f"Wybrano plik: {filename}")

    # ============ MODEL LOADING ============

    def load_models(self):
        """Załaduj listę modeli z OpenRouter"""
        if not self.openrouter_api_key.get():
            messagebox.showerror("Błąd", "Podaj klucz API OpenRouter")
            return

        self.update_progress("Ładowanie modeli z OpenRouter...")

        thread = threading.Thread(target=self._load_models_thread)
        thread.daemon = True
        thread.start()

    def _load_models_thread(self):
        """Thread do ładowania modeli"""
        try:
            self.openrouter_client = OpenRouterClient(self.openrouter_api_key.get())
            models = self.openrouter_client.list_models()
            models.sort(key=lambda x: x.get('name', ''))

            model_options = [f"{m.get('name', 'Unknown')} ({m.get('id', '')})" for m in models]

            # Update comboboxes
            self.model3_combo['values'] = model_options
            self.model4_combo['values'] = model_options
            self.model5_combo['values'] = model_options

            # Set defaults
            self._set_suggested_models(models)

            self.models_loaded = True
            self.start_button.config(state=tk.NORMAL)
            self.update_progress(f"✓ Załadowano {len(models)} modeli", 0)
            self.log(f"✓ Załadowano {len(models)} modeli z OpenRouter")

        except Exception as e:
            self.log(f"❌ Błąd ładowania modeli: {e}")
            messagebox.showerror("Błąd", f"Nie udało się załadować modeli: {e}")

    def _set_suggested_models(self, models):
        """Ustaw sugerowane modele"""
        model_ids = [m.get('id', '') for m in models]
        model_names = [f"{m.get('name', 'Unknown')} ({m.get('id', '')})" for m in models]

        # Step 3: Fast/cheap
        fast_models = ['google/gemini-flash-1.5', 'anthropic/claude-3-haiku', 'openai/gpt-4o-mini', 'google/gemini-2.0-flash-exp']
        for model_id in fast_models:
            if model_id in model_ids:
                idx = model_ids.index(model_id)
                self.model_step3.set(model_names[idx])
                self.model_step4.set(model_names[idx])
                break

        # Step 5: Reasoning
        reasoning_models = ['openai/o1-mini', 'qwen/qwq-32b-preview', 'deepseek/deepseek-chat', 'anthropic/claude-3.7-sonnet']
        for model_id in reasoning_models:
            if model_id in model_ids:
                idx = model_ids.index(model_id)
                self.model_step5.set(model_names[idx])
                break

    def get_model_id_from_selection(self, selection):
        """Wyciągnij ID modelu z selecta"""
        if not selection:
            return None
        match = re.search(r'\((.*?)\)$', selection)
        return match.group(1) if match else None

    # ============ PROMPT MANAGEMENT ============

    def save_prompt_config(self):
        """Zapisz konfigurację promptów"""
        # Update prompts from editors
        for step_key, editor in self.prompt_editors.items():
            prompt_text = editor.get("1.0", tk.END).strip()
            self.prompt_manager.update_prompt(step_key, prompt_text)

        # Save to file
        if self.project_manager.current_project_path:
            try:
                filepath = self.project_manager.save_prompt_config(self.prompt_manager.get_all_prompts())
                self.log(f"✓ Zapisano konfigurację promptów: {filepath}")
                messagebox.showinfo("Sukces", "Konfiguracja promptów zapisana")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się zapisać: {e}")
        else:
            messagebox.showwarning("Ostrzeżenie", "Najpierw wybierz projekt")

    def load_prompt_config(self):
        """Wczytaj konfigurację promptów"""
        if not self.project_manager.current_project_path:
            messagebox.showwarning("Ostrzeżenie", "Najpierw wybierz projekt")
            return

        try:
            prompts = self.project_manager.load_prompt_config()
            if prompts:
                self.prompt_manager.current_prompts = prompts
                # Update editors
                for step_key, editor in self.prompt_editors.items():
                    editor.delete("1.0", tk.END)
                    prompt_text = self.prompt_manager.get_prompt(step_key)
                    editor.insert("1.0", prompt_text)
                self.log("✓ Wczytano konfigurację promptów z projektu")
                messagebox.showinfo("Sukces", "Konfiguracja promptów wczytana")
            else:
                messagebox.showinfo("Info", "Brak zapisanej konfiguracji promptów w projekcie")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wczytać: {e}")

    def reset_prompts(self):
        """Resetuj prompty do domyślnych"""
        if messagebox.askyesno("Potwierdzenie", "Czy na pewno zresetować wszystkie prompty do domyślnych?"):
            self.prompt_manager.reset_to_defaults()
            # Update editors
            for step_key, editor in self.prompt_editors.items():
                editor.delete("1.0", tk.END)
                prompt_text = self.prompt_manager.get_prompt(step_key)
                editor.insert("1.0", prompt_text)
            self.log("✓ Zresetowano prompty do domyślnych")
            messagebox.showinfo("Sukces", "Prompty zresetowane do domyślnych")

    # ============ WORKFLOW EXECUTION ============

    def start_workflow(self):
        """Rozpocznij workflow"""
        # Validation
        if not self.project_manager.current_project_path:
            messagebox.showerror("Błąd", "Najpierw wybierz projekt")
            return

        if not any([self.run_step1.get(), self.run_step2.get(), self.run_step3.get(), self.run_step4.get(), self.run_step5.get()]):
            messagebox.showerror("Błąd", "Wybierz przynajmniej jeden krok")
            return

        # Check API keys
        if (self.run_step2.get() and not self.jina_api_key.get()):
            messagebox.showerror("Błąd", "Podaj klucz Jina AI dla kroku 2")
            return

        if (any([self.run_step3.get(), self.run_step4.get(), self.run_step5.get()]) and not self.openrouter_api_key.get()):
            messagebox.showerror("Błąd", "Podaj klucz OpenRouter dla kroków 3-5")
            return

        # Check model selection
        if self.run_step3.get() and not self.model_step3.get():
            messagebox.showerror("Błąd", "Wybierz model dla kroku 3")
            return
        if self.run_step4.get() and not self.model_step4.get():
            messagebox.showerror("Błąd", "Wybierz model dla kroku 4")
            return
        if self.run_step5.get() and not self.model_step5.get():
            messagebox.showerror("Błąd", "Wybierz model dla kroku 5")
            return

        # Check dependencies (tylko jeśli poprzedni krok NIE jest zaznaczony w tym workflow)
        if self.run_step2.get() and not self.run_step1.get() and not self.project_manager.check_file_exists("products.txt"):
            messagebox.showerror("Błąd", "Krok 2 wymaga wykonania kroku 1 (brak products.txt)")
            return
        if self.run_step3.get() and not self.run_step2.get() and not self.project_manager.check_file_exists("content_website.json"):
            messagebox.showerror("Błąd", "Krok 3 wymaga wykonania kroku 2 (brak content_website.json)")
            return
        if self.run_step4.get() and not self.run_step3.get() and not self.project_manager.check_file_exists("product_extraction.json"):
            messagebox.showerror("Błąd", "Krok 4 wymaga wykonania kroku 3 (brak product_extraction.json)")
            return
        if self.run_step5.get() and not self.run_step4.get() and not self.project_manager.check_file_exists("categories_structure.json"):
            messagebox.showerror("Błąd", "Krok 5 wymaga wykonania kroku 4 (brak categories_structure.json)")
            return

        # Start processing
        self.processing = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_bar['mode'] = 'determinate'
        self.progress_bar['value'] = 0

        # Run in thread
        thread = threading.Thread(target=self.run_workflow_thread)
        thread.daemon = True
        thread.start()

    def stop_workflow(self):
        """Zatrzymaj workflow"""
        self.processing = False
        self.waiting_for_confirmation = False
        self.log("⏸ Zatrzymano. Naciśnij 'Kontynuuj' aby wznowić lub 'Start' aby zacząć od nowa.")
        self.continue_button.config(state=tk.NORMAL)

    def continue_workflow(self):
        """Kontynuuj workflow - tryb nadzorowany LUB resume po STOP"""
        if self.waiting_for_confirmation:
            # Tryb nadzorowany - kontynuuj w tym samym wątku
            self.waiting_for_confirmation = False
            self.continue_button.config(state=tk.DISABLED)
            self.log("▶ Kontynuacja workflow...")
        elif not self.processing:
            # Resume po STOP - uruchom nowy wątek od ostatniego wykonanego kroku
            self.processing = True
            self.start_button.config(state=tk.DISABLED)
            self.continue_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.log("▶ Wznowienie workflow...")

            # Run in thread
            thread = threading.Thread(target=self.run_workflow_thread, args=(True,))
            thread.daemon = True
            thread.start()

    def _wait_for_confirmation(self, step_name):
        """Czekaj na potwierdzenie użytkownika w trybie nadzorowanym"""
        self.waiting_for_confirmation = True
        self.log(f"⏸ {step_name} zakończony. Sprawdź wyniki i naciśnij 'Kontynuuj' aby przejść dalej.")
        self.continue_button.config(state=tk.NORMAL)

        # Czekaj aż użytkownik naciśnie Kontynuuj lub Stop
        while self.waiting_for_confirmation and self.processing:
            import time
            time.sleep(0.1)

    def run_workflow_thread(self, resume=False):
        """Thread wykonujący workflow"""
        try:
            total_steps = sum([
                self.run_step1.get(),
                self.run_step2.get(),
                self.run_step3.get(),
                self.run_step4.get(),
                self.run_step5.get()
            ])

            # W trybie resume, zacznij od ostatniego wykonanego kroku
            if resume:
                completed_steps = self.last_completed_step
                self.log(f"Wznowienie od kroku {completed_steps + 1}...")
            else:
                completed_steps = 0
                self.last_completed_step = 0

            # Krok 1
            if self.processing and self.run_step1.get() and (not resume or completed_steps < 1):
                self.log("=== Krok 1: Pobranie listy produktów z sitemap ===")
                self.execute_step1()
                completed_steps = max(completed_steps, 1)
                self.last_completed_step = 1
                self.update_progress(f"Krok 1 zakończony ({completed_steps}/{total_steps})", (completed_steps/total_steps)*100)
                if self.supervised_mode.get() and self.processing:
                    self._wait_for_confirmation("Krok 1")

            # Krok 2
            if self.processing and self.run_step2.get() and (not resume or completed_steps < 2):
                self.log("=== Krok 2: Pobranie opisów produktów ===")
                self.execute_step2()
                completed_steps = max(completed_steps, 2)
                self.last_completed_step = 2
                self.update_progress(f"Krok 2 zakończony ({completed_steps}/{total_steps})", (completed_steps/total_steps)*100)
                if self.supervised_mode.get() and self.processing:
                    self._wait_for_confirmation("Krok 2")

            # Krok 3
            if self.processing and self.run_step3.get() and (not resume or completed_steps < 3):
                self.log("=== Krok 3: Ekstrakcja parametrów produktów ===")
                model_id = self.get_model_id_from_selection(self.model_step3.get())
                self.log(f"Model: {model_id}")
                self.execute_step3(model_id)
                completed_steps = max(completed_steps, 3)
                self.last_completed_step = 3
                self.update_progress(f"Krok 3 zakończony ({completed_steps}/{total_steps})", (completed_steps/total_steps)*100)
                if self.supervised_mode.get() and self.processing:
                    self._wait_for_confirmation("Krok 3")

            # Krok 4
            if self.processing and self.run_step4.get() and (not resume or completed_steps < 4):
                self.log("=== Krok 4: Budowa struktury kategorii ===")
                model_id = self.get_model_id_from_selection(self.model_step4.get())
                self.log(f"Model: {model_id}")
                self.execute_step4(model_id)
                completed_steps = max(completed_steps, 4)
                self.last_completed_step = 4
                self.update_progress(f"Krok 4 zakończony ({completed_steps}/{total_steps})", (completed_steps/total_steps)*100)
                if self.supervised_mode.get() and self.processing:
                    self._wait_for_confirmation("Krok 4")

            # Krok 5
            if self.processing and self.run_step5.get() and (not resume or completed_steps < 5):
                self.log("=== Krok 5: Finalizacja kategorii ===")
                model_id = self.get_model_id_from_selection(self.model_step5.get())
                self.log(f"Model: {model_id}")
                self.execute_step5(model_id)
                completed_steps = max(completed_steps, 5)
                self.last_completed_step = 5
                self.update_progress(f"Krok 5 zakończony ({completed_steps}/{total_steps})", (completed_steps/total_steps)*100)
                if self.supervised_mode.get() and self.processing:
                    self._wait_for_confirmation("Krok 5")

            if self.processing:
                self.update_progress("✅ Workflow zakończony pomyślnie!", 100)
                self.log("=== WORKFLOW ZAKOŃCZONY POMYŚLNIE ===")
                self.refresh_project_status()
                messagebox.showinfo("Sukces", "Workflow zakończony pomyślnie!")

        except Exception as e:
            self.log(f"❌ BŁĄD: {e}")
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")
        finally:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.processing = False

    # ============ STEP EXECUTION METHODS ============
    # Te metody będą implementowane w następnej części
    # Zostaną dodane metody: execute_step1 - execute_step5
    # oraz metody pomocnicze z oryginalnego app.py

    def execute_step1(self):
        """Wykonaj krok 1 - parsowanie sitemap lub upload pliku"""
        output_path = self.project_manager.get_file_path("products.txt")

        # Check which option to use
        sitemap_url = self.sitemap_url.get()
        upload_file = self.upload_file_path.get()

        if upload_file:
            # Option B: Load from file
            self.log("Opcja B: Wczytywanie URL-i z pliku...")

            try:
                with open(upload_file, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip()]

                # Copy to project folder
                import shutil
                shutil.copy(upload_file, str(output_path))

                self.log(f"✓ Wczytano {len(urls)} URL-i z pliku")
                self.log(f"✓ Skopiowano do: {output_path}")
                self.project_manager.update_step_status("step1", True)

            except Exception as e:
                raise ValueError(f"Błąd wczytywania pliku: {e}")

        elif sitemap_url:
            # Option A: Parse sitemap
            self.log("Opcja A: Parsowanie sitemap...")

            parser = SitemapParser()

            def progress_callback(msg):
                self.log(msg)

            urls = parser.parse_sitemap(
                sitemap_url,
                self.url_filter_pattern.get() if self.url_filter_pattern.get() else None,
                progress_callback
            )

            # Save to file
            parser.save_to_file(str(output_path))

            self.log(f"✓ Znaleziono {len(urls)} URL-i produktów")
            self.log(f"✓ Zapisano do: {output_path}")
            self.project_manager.update_step_status("step1", True)

        else:
            raise ValueError("Podaj URL sitemap (Opcja A) lub wybierz plik TXT (Opcja B)")

    def execute_step2(self):
        """Wykonaj krok 2 - pobieranie treści z Jina"""
        # Load URLs
        input_path = self.project_manager.get_file_path("products.txt")
        with open(input_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]

        # Initialize Jina client
        if not self.jina_client:
            self.jina_client = JinaClient(self.jina_api_key.get())

        # Fetch content
        def progress_callback(processed, total):
            self.log(f"Przetworzono {processed}/{total} URL-i")
            progress = (processed / total) * 100
            self.update_progress(f"Pobieranie treści: {processed}/{total}", progress)

        results = self.jina_client.fetch_urls_parallel(
            urls,
            num_threads=self.num_threads_jina.get(),
            max_retries=self.max_retries_jina.get(),
            progress_callback=progress_callback,
            stop_flag_callback=lambda: self.processing
        )

        # Save to file
        output_path = self.project_manager.get_file_path("content_website.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        self.log(f"✓ Pobrano treść dla {len(results)} URL-i")
        self.log(f"✓ Zapisano do: {output_path}")
        self.project_manager.update_step_status("step2", True)

    def execute_step3(self, model_id):
        """Wykonaj krok 3 - ekstrakcja parametrów"""
        # Backup if exists
        output_file = "product_extraction.json"
        backup_path = self.project_manager.backup_file(output_file)
        if backup_path:
            self.log(f"📦 Backup: {backup_path}")

        # Load data
        input_path = self.project_manager.get_file_path("content_website.json")
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Get prompt
        system_prompt = self.prompt_manager.get_prompt("step3_extraction")

        # Process
        def process_item(item):
            if not self.processing:
                return None

            url = item['url']
            content = item['content']
            cleaned_content = self.clean_content(content)

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"The content of the product page is:\n{cleaned_content}"}
            ]

            for attempt in range(self.max_retries_extract.get() + 1):
                try:
                    response = self.openrouter_client.chat_completion(model_id, messages)
                    raw_output = self.openrouter_client.get_response_text(response)
                    cleaned_output = self.clean_field(raw_output)
                    json_data = json.loads(cleaned_output)
                    return {"url": url, "extraction": json_data}
                except json.JSONDecodeError as e:
                    if attempt < self.max_retries_extract.get():
                        self.log(f"Powtarzanie {url} (próba {attempt + 1})")
                    else:
                        self.log(f"Nie udało się: {url}")
                        return {"url": url, "extraction": {}}
                except Exception as e:
                    if attempt < self.max_retries_extract.get():
                        self.log(f"Błąd {url}: {e}")
                    else:
                        return {"url": url, "extraction": {}}
            return {"url": url, "extraction": {}}

        results = []
        total = len(data)
        processed = 0

        with ThreadPoolExecutor(max_workers=self.num_threads_extract.get()) as executor:
            futures = []

            # Submit tasks
            for item in data:
                if not self.processing:
                    break
                future = executor.submit(process_item, item)
                futures.append(future)

            # Collect results
            for future in as_completed(futures):
                if not self.processing:
                    # Cancel remaining futures
                    for f in futures:
                        f.cancel()
                    break
                result = future.result()
                if result:
                    results.append(result)
                    processed += 1
                    if processed % 10 == 0 or processed == total:
                        self.log(f"Przetworzono {processed}/{total}")
                        self.update_progress(f"Ekstrakcja: {processed}/{total}", (processed/total)*100)

        # Save
        output_path = self.project_manager.get_file_path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        self.log(f"✓ Zapisano ekstrakcję dla {len(results)} produktów")
        self.project_manager.update_step_status("step3", True)

    def execute_step4(self, model_id):
        """Wykonaj krok 4 - budowa struktury"""
        # Backup
        output_file = "categories_structure.json"
        backup_path = self.project_manager.backup_file(output_file)
        if backup_path:
            self.log(f"📦 Backup: {backup_path}")

        # Load data
        input_path = self.project_manager.get_file_path("product_extraction.json")
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Get prompt
        system_prompt = self.prompt_manager.get_prompt("step4_structure")

        # Batch processing function
        def get_navigation_json(batch):
            if not self.processing:
                return {}

            filtered_extractions = [item['extraction'] for item in batch
                                   if 'extraction' in item and
                                   item['extraction'].get('product_category', {}).get('main_category') is not None]
            if not filtered_extractions:
                return {}

            batch_data = json.dumps(filtered_extractions, ensure_ascii=False)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here is the product data:\n{batch_data}"}
            ]

            for attempt in range(self.max_retries_batch.get() + 1):
                try:
                    response = self.openrouter_client.chat_completion(model_id, messages)
                    raw_output = self.openrouter_client.get_response_text(response)
                    cleaned_output = self.clean_field(raw_output)
                    json_data = json.loads(cleaned_output)
                    return json_data
                except Exception as e:
                    if attempt < self.max_retries_batch.get():
                        self.log(f"Powtarzanie batch (próba {attempt + 1})")
                    else:
                        self.log(f"Błąd batch: {e}")
                        return {}
            return {}

        # Create batches
        batch_size = self.batch_size.get()
        batches = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

        partial_navs = []
        processed = 0
        total = len(batches)

        with ThreadPoolExecutor(max_workers=self.num_threads_batch.get()) as executor:
            futures = []

            # Submit tasks
            for batch in batches:
                if not self.processing:
                    break
                future = executor.submit(get_navigation_json, batch)
                futures.append(future)

            # Collect results
            for future in as_completed(futures):
                if not self.processing:
                    # Cancel remaining futures
                    for f in futures:
                        f.cancel()
                    break
                partial = future.result()
                if partial:
                    partial_navs.append(partial)
                processed += 1
                self.log(f"Przetworzono batch {processed}/{total}")
                self.update_progress(f"Budowa struktury: {processed}/{total}", (processed/total)*100)

        # Merge results
        merged = defaultdict(set)
        for nav in partial_navs:
            for main in nav.get('main_navigation', []):
                main_name = main['name']
                for sub in main.get('subcategories', []):
                    sub_name = sub['name']
                    merged[main_name].add(sub_name)

        main_navigation = []
        for main_name in sorted(merged.keys()):
            subcategories = [{"name": sub_name} for sub_name in sorted(merged[main_name])]
            main_navigation.append({
                "name": main_name,
                "subcategories": subcategories
            })

        # Save
        output_path = self.project_manager.get_file_path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"main_navigation": main_navigation}, f, indent=2, ensure_ascii=False)

        self.log(f"✓ Zapisano strukturę kategorii")
        self.project_manager.update_step_status("step4", True)

    def execute_step5(self, model_id):
        """Wykonaj krok 5 - finalizacja"""
        # Backup
        output_file = "categories_final.json"
        backup_path = self.project_manager.backup_file(output_file)
        if backup_path:
            self.log(f"📦 Backup: {backup_path}")

        # Load data
        input_path = self.project_manager.get_file_path("categories_structure.json")
        with open(input_path, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        # Get prompt
        system_prompt = self.prompt_manager.get_prompt("step5_finalization")

        data_str = json.dumps(loaded_data, ensure_ascii=False)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the input list:\n{data_str}"}
        ]

        for attempt in range(self.max_retries_final.get() + 1):
            if not self.processing:
                break
            try:
                self.log(f"Optymalizacja (próba {attempt + 1})...")
                response = self.openrouter_client.chat_completion(model_id, messages, max_tokens=16000)
                raw_output = self.openrouter_client.get_response_text(response)

                self.log(f"Otrzymano odpowiedź ({len(raw_output)} znaków)")

                cleaned_output = self.clean_field(raw_output)

                # Extract JSON
                json_match = re.search(r'\{[\s\S]*\}', cleaned_output)
                if json_match:
                    cleaned_output = json_match.group(0)

                optimized_json = json.loads(cleaned_output)

                # Save
                output_path = self.project_manager.get_file_path(output_file)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(optimized_json, f, indent=2, ensure_ascii=False)

                self.log("✓ Zapisano finalną strukturę kategorii")

                # Display structure
                categories = optimized_json.get('categories', [])
                self.log("\n=== Finalna Struktura Kategorii ===")
                self.display_structure(categories)

                self.project_manager.update_step_status("step5", True)
                return

            except json.JSONDecodeError as e:
                if attempt < self.max_retries_final.get():
                    self.log(f"Powtarzanie finalizacji (próba {attempt + 1})")
                    messages[1]['content'] = f"Output ONLY valid JSON. No text.\n\n{data_str}"
                else:
                    self.log(f"❌ Nie udało się sfinalizować: {e}")
            except Exception as e:
                if attempt < self.max_retries_final.get():
                    self.log(f"Powtarzanie (próba {attempt + 1}): {e}")
                else:
                    self.log(f"❌ Błąd finalizacji: {e}")

    # ============ UTILITY METHODS ============

    def clean_content(self, text):
        """Czyszczenie treści markdown"""
        text = re.sub(r'^#+\s', '', text, flags=re.MULTILINE)
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'__([^_]+)__', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)
        text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'\1', text)
        text = re.sub(r'https?://[^\s]+', '', text)
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        text = re.sub(r'^\s*[-*]\s', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s', '', text, flags=re.MULTILINE)
        text = re.sub(r'\n\s*\n', '\n', text)
        return text.strip()

    def clean_field(self, content):
        """Czyszczenie odpowiedzi AI z markdown code blocks"""
        if not content or not isinstance(content, str):
            return content
        content = re.sub(r'^```(\w+)?\s*\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'\n```$', '', content, flags=re.MULTILINE)
        return content.strip()

    def display_structure(self, cats, level=0):
        """Wyświetl strukturę kategorii w logach"""
        for cat in cats:
            self.log("  " * level + f"- {cat['name']}")
            subcats = cat.get('subcategories', [])
            if subcats:
                self.display_structure(subcats, level + 1)


if __name__ == "__main__":
    root = tk.Tk()
    app = NexusNavigationApp(root)
    root.mainloop()
