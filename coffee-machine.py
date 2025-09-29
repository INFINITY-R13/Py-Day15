import tkinter as tk
from tkinter import font as tkfont

# --- DATA & CONFIGURATION ---

MENU = {
    "Espresso": {
        "ingredients": {"water": 50, "coffee": 18, "milk": 0},
        "cost": 120,
    },
    "Latte": {
        "ingredients": {"water": 200, "milk": 150, "coffee": 24},
        "cost": 200,
    },
    "Cappuccino": {
        "ingredients": {"water": 250, "milk": 100, "coffee": 24},
        "cost": 240,
    }
}

class CoffeeMachineApp:
    """A GUI for the Coffee Machine with a unified high-contrast theme."""

    # --- FINAL HIGH-CONTRAST THEME ---
    COLORS = {
        "background": "#F5F5F5",
        "card_bg": "#FFFFFF",
        "text_dark": "#212121", # Dark text for all labels AND buttons
        "text_light": "#616161",
        "status_bar_text": "#FFFFFF",
        
        # Lighter backgrounds for high contrast with dark text
        "accent_light_bg": "#BBDEFB", # Light blue for 'Pay'
        "success_light_bg": "#A5D6A7", # Light green for 'Power ON'
        "error_light_bg": "#FFCDD2",   # Light red for 'Power OFF'
        "secondary_bg": "#E0E0E0",     # Grey for 'Select', 'Report', 'Back'

        # Status Bar Colors
        "status_info": "#424242",
        "status_success": "#2E7D32",
        "status_error": "#C62828",
    }

    def __init__(self, root):
        self.root = root
        self.profit = 0
        self.resources = {"water": 300, "milk": 200, "coffee": 100}
        self.is_on = True
        
        self.setup_styles()
        self.create_widgets()
        self.show_main_view()

    def setup_styles(self):
        """Configure fonts and colors for the application."""
        self.root.title("Coffee Machine")
        self.root.configure(bg=self.COLORS["background"])
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        self.font_title = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        self.font_card_title = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.font_card_body = tkfont.Font(family="Segoe UI", size=10)
        self.font_button = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.font_status = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.font_report = tkfont.Font(family="Segoe UI", size=12)

    def create_widgets(self):
        """Create the main frames and persistent widgets."""
        self.main_frame = tk.Frame(self.root, bg=self.COLORS["background"])
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        control_bar = tk.Frame(self.root, bg=self.COLORS["card_bg"], height=80, highlightbackground="#E0E0E0", highlightthickness=1)
        control_bar.pack(fill="x", side="bottom")
        control_bar.pack_propagate(False)

        self.report_button = tk.Button(control_bar, text="⚙️ Report", font=self.font_button, bg=self.COLORS["secondary_bg"], fg=self.COLORS["text_dark"], relief="flat", command=self.show_report_view)
        self.report_button.pack(side="left", padx=20, pady=15, ipady=5)

        self.power_button = tk.Button(control_bar, font=self.font_button, relief="flat", width=12, command=self.toggle_power)
        self.power_button.pack(side="right", padx=20, pady=15, ipady=5)

        self.status_label = tk.Label(self.root, text="Welcome!", font=self.font_status, height=2)
        self.status_label.pack(side="bottom", fill="x")

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def update_status(self, message, msg_type="info"):
        colors = {
            "info": self.COLORS["status_info"],
            "success": self.COLORS["status_success"],
            "error": self.COLORS["status_error"],
        }
        bg_color = colors.get(msg_type, colors["info"])
        self.status_label.config(text=message, bg=bg_color, fg=self.COLORS["status_bar_text"])

    def show_main_view(self):
        self.clear_main_frame()
        self.report_button.config(command=self.show_report_view, text="⚙️ Report")

        tk.Label(self.main_frame, text="Select your Coffee", font=self.font_title, bg=self.COLORS["background"], fg=self.COLORS["text_dark"]).pack(pady=(10, 20))

        self.drink_buttons = []
        for name, details in MENU.items():
            self.create_drink_card(name, details)
        
        self.toggle_power(initial_setup=True)

    def create_drink_card(self, name, details):
        card = tk.Frame(self.main_frame, bg=self.COLORS["card_bg"], highlightbackground="#E0E0E0", highlightthickness=1)
        card.pack(fill="x", pady=8)

        text_frame = tk.Frame(card, bg=self.COLORS["card_bg"])
        text_frame.pack(side="left", padx=15, pady=15, fill="x", expand=True)
        
        tk.Label(text_frame, text=name, font=self.font_card_title, bg=self.COLORS["card_bg"], fg=self.COLORS["text_dark"], anchor="w").pack(fill="x")
        
        ingredients_text = f"💧 {details['ingredients']['water']}ml | ☕ {details['ingredients']['coffee']}g | 🥛 {details['ingredients']['milk']}ml"
        tk.Label(text_frame, text=ingredients_text, font=self.font_card_body, bg=self.COLORS["card_bg"], fg=self.COLORS["text_light"], anchor="w").pack(fill="x", pady=2)
        
        action_frame = tk.Frame(card, bg=self.COLORS["card_bg"])
        action_frame.pack(side="right", padx=15, pady=15)

        tk.Label(action_frame, text=f"₹{details['cost']}", font=self.font_card_title, bg=self.COLORS["card_bg"], fg="#007AFF").pack(pady=(0, 10))

        buy_button = tk.Button(action_frame, text="Select", font=self.font_button, bg=self.COLORS["secondary_bg"], fg=self.COLORS["text_dark"], relief="flat", command=lambda n=name: self.handle_drink_selection(n))
        buy_button.pack(ipadx=5)
        
        self.drink_buttons.append(buy_button)

    def show_report_view(self):
        self.clear_main_frame()
        self.report_button.config(command=self.show_main_view, text="⬅️ Back")
        
        tk.Label(self.main_frame, text="Machine Report", font=self.font_title, bg=self.COLORS["background"], fg=self.COLORS["text_dark"]).pack(pady=(10, 20))

        report_frame = tk.Frame(self.main_frame, bg=self.COLORS["card_bg"], highlightbackground="#E0E0E0", highlightthickness=1)
        report_frame.pack(fill="x", pady=10)
        
        for resource, amount in self.resources.items():
            unit = "g" if resource == "coffee" else "ml"
            icon = "💧" if resource == "water" else "🥛" if resource == "milk" else "☕"
            tk.Label(report_frame, text=f"{icon} {resource.title()}: {amount}{unit}", font=self.font_report, bg=self.COLORS["card_bg"], fg=self.COLORS["text_dark"], anchor="w").pack(fill="x", padx=20, pady=8)
            
        tk.Label(report_frame, text=f"💰 Profit: ₹{self.profit}", font=self.font_report, bg=self.COLORS["card_bg"], fg=self.COLORS["text_dark"], anchor="w").pack(fill="x", padx=20, pady=8)
    
    def handle_drink_selection(self, drink_name):
        drink = MENU[drink_name]
        
        for item, required in drink["ingredients"].items():
            if self.resources[item] < required:
                self.update_status(f"Error: Not enough {item}.", "error")
                return
        
        self.show_payment_window(drink_name, drink['cost'])

    def show_payment_window(self, drink_name, cost):
        payment_win = tk.Toplevel(self.root)
        payment_win.title("Payment")
        payment_win.configure(bg=self.COLORS["background"])
        payment_win.transient(self.root); payment_win.grab_set()

        tk.Label(payment_win, text=f"Total Cost: ₹{cost}", font=self.font_card_title, bg=self.COLORS["background"], fg=self.COLORS["text_dark"]).pack(pady=15)

        entries = {}
        for text, value in {"₹10 notes": 10, "₹20 notes": 20, "₹50 notes": 50, "₹1 coins": 1, "₹2 coins": 2, "₹5 coins": 5}.items():
            frame = tk.Frame(payment_win, bg=self.COLORS["background"])
            frame.pack(pady=6, padx=20, fill="x")
            tk.Label(frame, text=text, font=self.font_report, bg=self.COLORS["background"], fg=self.COLORS["text_light"], width=10, anchor="w").pack(side="left")
            entry = tk.Entry(frame, font=self.font_report, width=15, relief="solid", bd=1); entry.pack(side="right"); entry.insert(0, "0")
            entries[value] = entry
        
        btn_frame = tk.Frame(payment_win, bg=self.COLORS["background"]); btn_frame.pack(pady=20)
        
        pay_button = tk.Button(btn_frame, text="Pay", font=self.font_button, bg=self.COLORS["accent_light_bg"], fg=self.COLORS["text_dark"], relief="flat", command=lambda: self.process_payment(drink_name, cost, entries, payment_win))
        pay_button.pack(fill="x", ipady=5, ipadx=10)

    def process_payment(self, drink_name, cost, entries, window):
        try:
            money_received = sum(int(entry.get() or 0) * value for value, entry in entries.items())
        except ValueError:
            self.update_status("Invalid input. Please use numbers.", "error"); window.destroy(); return
        
        if money_received >= cost:
            change = money_received - cost
            self.profit += cost
            for item, amount in MENU[drink_name]["ingredients"].items(): self.resources[item] -= amount
            
            self.update_status(f"Success! Enjoy your {drink_name}. ☕", "success")
            if change > 0: self.root.after(2000, lambda: self.update_status(f"Your change is ₹{change:.2f}."))
        else:
            self.update_status(f"Payment failed. You paid ₹{money_received}, but ₹{cost} was required.", "error")
        
        window.destroy()

    def toggle_power(self, initial_setup=False):
        if not initial_setup: self.is_on = not self.is_on
        
        state = "normal" if self.is_on else "disabled"
        
        for btn in getattr(self, 'drink_buttons', []): btn.config(state=state)
        
        if self.is_on:
            self.power_button.config(text="Power: ON", bg=self.COLORS["success_light_bg"], fg=self.COLORS["text_dark"])
            self.report_button.config(state="normal")
            if not initial_setup: self.update_status("Welcome! Please select a drink.")
        else:
            self.power_button.config(text="Power: OFF", bg=self.COLORS["error_light_bg"], fg=self.COLORS["text_dark"])
            self.report_button.config(state="disabled")
            if not initial_setup: self.update_status("Machine is currently off.", "error")

if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeMachineApp(root)
    root.mainloop()
    