"""
Custom Tkinter Widgets - Modern Dark Theme Components
"""
import tkinter as tk
from tkinter import ttk


class ModernScrollbar(tk.Canvas):
    """Custom scrollbar with modern dark theme"""

    def __init__(self, parent, orient='vertical', **kwargs):
        super().__init__(parent,
                        bg='#1a1a1a',
                        highlightthickness=0,
                        width=12 if orient == 'vertical' else kwargs.get('height', 12),
                        height=12 if orient == 'horizontal' else kwargs.get('height', 200),
                        **kwargs)

        self.orient = orient
        self.command = None

        # Colors
        self.bg_color = '#1a1a1a'
        self.thumb_color = '#4a4a4a'
        self.thumb_hover_color = '#5a5a5a'
        self.thumb_active_color = '#f97316'

        # State
        self.thumb_rect = None
        self.is_hovering = False
        self.is_dragging = False
        self.drag_start_y = 0
        self.drag_start_x = 0

        # Bindings
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_press)
        self.bind('<B1-Motion>', self._on_drag)
        self.bind('<ButtonRelease-1>', self._on_release)

    def set(self, first, last):
        """Update scrollbar position (called by scrolled widget)"""
        self.delete('all')

        first = float(first)
        last = float(last)

        if self.orient == 'vertical':
            height = self.winfo_height()
            thumb_height = max(30, int(height * (last - first)))
            thumb_y = int(height * first)

            self.thumb_rect = self.create_rectangle(
                2, thumb_y, 10, thumb_y + thumb_height,
                fill=self._get_thumb_color(),
                outline='',
                tags='thumb'
            )
        else:
            width = self.winfo_width()
            thumb_width = max(30, int(width * (last - first)))
            thumb_x = int(width * first)

            self.thumb_rect = self.create_rectangle(
                thumb_x, 2, thumb_x + thumb_width, 10,
                fill=self._get_thumb_color(),
                outline='',
                tags='thumb'
            )

    def _get_thumb_color(self):
        """Get current thumb color based on state"""
        if self.is_dragging:
            return self.thumb_active_color
        elif self.is_hovering:
            return self.thumb_hover_color
        else:
            return self.thumb_color

    def _on_enter(self, event):
        self.is_hovering = True
        self._update_thumb_color()

    def _on_leave(self, event):
        if not self.is_dragging:
            self.is_hovering = False
            self._update_thumb_color()

    def _on_press(self, event):
        self.is_dragging = True
        self.drag_start_y = event.y
        self.drag_start_x = event.x
        self._update_thumb_color()

    def _on_drag(self, event):
        if not self.is_dragging or not self.command:
            return

        if self.orient == 'vertical':
            height = self.winfo_height()
            delta = (event.y - self.drag_start_y) / height
            self.command('moveto', delta)
            self.drag_start_y = event.y
        else:
            width = self.winfo_width()
            delta = (event.x - self.drag_start_x) / width
            self.command('moveto', delta)
            self.drag_start_x = event.x

    def _on_release(self, event):
        self.is_dragging = False
        self._update_thumb_color()

    def _update_thumb_color(self):
        """Update thumb color"""
        if self.thumb_rect:
            self.itemconfig('thumb', fill=self._get_thumb_color())


class ScrollableFrame(ttk.Frame):
    """Frame with modern scrollbar and mouse wheel support"""

    def __init__(self, parent, style='Dark.TFrame', **kwargs):
        super().__init__(parent, style=style, **kwargs)

        # Canvas
        self.canvas = tk.Canvas(self, bg='#1a1a1a', highlightthickness=0)

        # Modern scrollbar
        self.scrollbar = ModernScrollbar(self, orient='vertical')
        self.scrollbar.command = self.canvas.yview

        # Scrollable frame
        self.scrollable_frame = ttk.Frame(self.canvas, style=style)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling - bind to canvas and frame
        self._bind_mouse_wheel(self.canvas)
        self._bind_mouse_wheel(self.scrollable_frame)

        # Bind canvas resize to update scrollable frame width
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        # Setup periodic check for new widgets (to bind mouse wheel)
        self._setup_recursive_binding()

    def _on_canvas_configure(self, event):
        """Update scrollable frame width when canvas is resized"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def _setup_recursive_binding(self):
        """Setup recursive binding for all current and future widgets"""
        def check_and_bind():
            self._bind_mouse_wheel_recursive(self.scrollable_frame)
            # Re-check after 100ms to catch dynamically added widgets
            self.after(100, check_and_bind)

        check_and_bind()

    def _bind_mouse_wheel_recursive(self, widget):
        """Recursively bind mouse wheel to widget and all descendants"""
        # Bind to widget if not already bound
        if not hasattr(widget, '_mouse_wheel_bound'):
            widget.bind("<MouseWheel>", self._on_mouse_wheel, add='+')
            widget.bind("<Button-4>", self._on_mouse_wheel, add='+')
            widget.bind("<Button-5>", self._on_mouse_wheel, add='+')
            widget._mouse_wheel_bound = True

        # Recursively bind to all children
        for child in widget.winfo_children():
            self._bind_mouse_wheel_recursive(child)

    def _bind_mouse_wheel(self, widget):
        """Bind mouse wheel to widget (legacy method - now uses recursive)"""
        widget.bind("<MouseWheel>", self._on_mouse_wheel, add='+')
        widget.bind("<Button-4>", self._on_mouse_wheel, add='+')
        widget.bind("<Button-5>", self._on_mouse_wheel, add='+')

    def _on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling"""
        if event.num == 4:  # Linux scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            self.canvas.yview_scroll(1, "units")
        else:  # Windows/Mac
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def create_modern_checkbox_style():
    """Create modern checkbox style with clear visual feedback"""
    style = ttk.Style()

    # Modern checkbox with orange accent
    style.configure('Modern.TCheckbutton',
                   background='#1a1a1a',
                   foreground='#e0e0e0',
                   font=('Inter', 10))

    # Note: ttk.Checkbutton indicators are theme-dependent and harder to customize
    # We'll use layout modification for better visual feedback

    style.map('Modern.TCheckbutton',
             background=[('active', '#242424')],
             foreground=[('selected', '#f97316'), ('active', '#f97316')])

    return style
