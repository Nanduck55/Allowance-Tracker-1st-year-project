import tkinter as tk
from tkinter import ttk, messagebox
import traceback
from budget_data import BudgetData
from utils import CUtils
import json
from datetime import datetime

class BudgetApp(tk.Tk):
    def __init__(this):
        super().__init__()

        this.title("Student Budget Tracker")
        this.geometry("900x950")
        this.configure(bg = "#1b1b1b")
        this.minsize(980, 700)

        try:
            this.iconbitmap("phinma_icon.ico")
        except Exception:
            pass

        # Custom Slider Color
        this.bg_r = tk.IntVar(value = 27)
        this.bg_g = tk.IntVar(value = 27)
        this.bg_b = tk.IntVar(value = 27)

        this.text_r = tk.IntVar(value = 255)
        this.text_g = tk.IntVar(value = 255)
        this.text_b = tk.IntVar(value = 255)

        this.btn_r = tk.IntVar(value = 54)
        this.btn_g = tk.IntVar(value = 54)
        this.btn_b = tk.IntVar(value = 54)

        this.border_r = tk.IntVar(value = 100)
        this.border_g = tk.IntVar(value = 100)
        this.border_b = tk.IntVar(value = 100)

        this.entryinput_r = tk.IntVar(value = 27)
        this.entryinput_g = tk.IntVar(value = 27)
        this.entryinput_b = tk.IntVar(value = 27)

        BG_MAIN = "#1b1b1b"
        BG_CARD = "#242424"
        BG_SUB = "#303030"
        HL_COLOR = "#ffffff"
        TEXT = "#ffffff"
        ENTRY_BG = "#2a2a2a"
        BTN_BG = "#363636"
        BTN_HOVER = "#4d4d4d"

        # Some Global Variables
        this.sort_reverse = False

        this.configure(bg = BG_MAIN)

        # =============================== #
        #         START STYLE             #
        # =============================== #
        this.style = ttk.Style()
        this.style.theme_use("clam")

        this.style.configure("TLabel", background = BG_CARD, foreground = TEXT, font = ("Segoe UI", 11))
        this.style.configure("TLabelframe", background = BG_CARD, foreground = HL_COLOR, borderwidth = 1, relief = "solid")
        this.style.configure("TLabelframe.Label", background = BG_CARD, foreground = HL_COLOR, font = ("Segoe UI", 11, "bold"))
        this.style.configure("TButton", background = BTN_BG, foreground = TEXT, font = ("Segoe UI", 11, "bold"), padding = 6, borderwidth = 0)
       
        this.style.map("TButton", background = [("active", BTN_HOVER)])
        this.style.configure("TEntry", fieldbackground = ENTRY_BG, background = ENTRY_BG, foreground = TEXT, padding = 6)
        this.style.configure("TCombobox", fieldbackground = ENTRY_BG, background = ENTRY_BG, foreground = TEXT, padding = 6, arrowcolor = TEXT)
        this.style.configure("Treeview", background = BG_SUB, fieldbackground = BG_SUB, foreground = TEXT, borderwidth = 0, rowheight = 28)
        this.style.configure("Treeview.Heading",background = "#3c3c3c", foreground = TEXT, font = ("Segoe UI", 11, "bold"))
        this.style.map("Treeview", background = [("selected", "#555555")])
        this.style.configure("SummaryLabel.TLabel", background = BG_CARD, foreground = "#44ff44", font = ("Segoe UI", 11, "bold"))
        this.style.configure("SummarySmall.TLabel", background = BG_CARD, foreground = TEXT, font = ("Segoe UI", 11))
        this.style.configure("TCombobox", fieldbackground = "#363636", background = "#363636", foreground ="#ffffff")
        this.style.map("TCombobox", fieldbackground = [("readonly", "#4B4242")], background = [("readonly", "#363636")], foreground = [("readonly", "#ffffff")])
        # =============================== #
        #         END STYLE               #
        # =============================== #

        try:
            this.data = BudgetData.get()
            this.create_widgets()
            this.UpdateSummary()
        except Exception as e:
            print("[CRITICAL ERROR] Failed to initialize app:", e)
            traceback.print_exc()
            messagebox.showerror("Startup Error", "An unexpected error occurred.")
            this.destroy()

        # Check if press enter
        this.bind("<Return>", lambda ev: this.AddExpense()) # necessary??

    # =============================== #
    #         START DESIGN            #
    # =============================== #
    def create_widgets(this):

        title = tk.Label(this, text = "STUDENT BUDGET TRACKER", font = ("Segoe UI Semibold", 24), bg = "#1b1b1b", fg = "#ffffff")
        title.pack(pady = 15)

        wrapper = tk.Frame(this, bg = "#1b1b1b")
        wrapper.pack(fill = "both", expand = True, padx = 10)

        # ======= Allowance Section ======= #
        frm_allowance = ttk.LabelFrame(wrapper, text = "Allowance Settings")
        frm_allowance.pack(fill = "x", padx = 5, pady = 6)

        ttk.Label(frm_allowance, text = "Allowance (PHP):").grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "w")
        this.entry_allowance = ttk.Entry(frm_allowance, width = 18)
        this.entry_allowance.grid(row = 0, column = 1, padx = 10, pady = 10)

        ttk.Button(frm_allowance, text = "Set", width = 14, command = this.SetAllowance).grid(row = 0, column = 2, padx = 10)
        ttk.Button(frm_allowance, text = "Add", width = 14, command = this.AddAllowance).grid(row = 0, column = 3, padx = 10)

        ttk.Label(frm_allowance, text = "Warning Threshold (%):").grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "w")
        this.entry_warning = ttk.Entry(frm_allowance, width = 18)
        this.entry_warning.grid(row = 1, column = 1, padx = 10, pady = 10)
        
        # Load warning threshold from data if available. if its blank then set it to 25% as default
        threshold = BudgetData.get().data.get("warning_threshold", 25)
        this.entry_warning.insert(0, str(int(threshold)))
        #this.entry_warning.insert(0, "25")  # default 25%

        ttk.Button(frm_allowance, text = "Set Warning", width = 14, command = this.SetWarning).grid(row = 1, column = 2, padx = 10)

        # ======= Expense Section ======= #
        frm_expense = ttk.LabelFrame(wrapper, text = "Add Expense")
        frm_expense.pack(fill = "x", padx = 5, pady = 6)

        ttk.Label(frm_expense, text = "Category:").grid(row = 0, column = 0, padx = 10, pady = 10)

        enum_category = ["Food", "Transport", "School", "Personal", "Others"]
        this.combo_category = ttk.Combobox(frm_expense, values = enum_category, width = 17, state = "readonly") # make the category selection to not writeable
        this.combo_category.grid(row = 0, column = 1, padx = 10, pady = 10)
        this.combo_category.set("Food")

        ttk.Label(frm_expense, text = "Amount (PHP):").grid(row = 0, column = 2, padx = 10, pady = 10)
        this.entry_amount = ttk.Entry(frm_expense, width = 15)
        this.entry_amount.grid(row = 0, column = 3, padx = 10, pady = 10)
        this.entry_amount.focus_set()

        ttk.Label(frm_expense, text = "Note:").grid(row = 0, column = 4, padx = 10, pady = 10)
        this.entry_note = ttk.Entry(frm_expense, width = 20)
        this.entry_note.grid(row = 0, column = 5, padx = 10, pady = 10)

        ttk.Button(frm_expense, text = "Add Expense", width = 13, command = this.AddExpense).grid(row = 0, column = 6, padx = 10)

        # ======= Summary Section ======= #
        frm_summary = ttk.LabelFrame(wrapper, text = "Budget Summary")
        frm_summary.pack(fill = "x", padx = 5, pady = 6)

        this.label_allowance = ttk.Label(frm_summary, text = "Allowance: PHP 0.00", style = "SummarySmall.TLabel")
        this.label_allowance.grid(row = 0, column = 0, padx = 10, pady = 10)

        this.label_spent = ttk.Label(frm_summary, text = "Total Spent: PHP 0.00", style = "SummarySmall.TLabel")
        this.label_spent.grid(row = 0, column = 1, padx = 10, pady = 10)
 
        this.label_remaining = ttk.Label(frm_summary, text = "Remaining: PHP 0.00", style = "SummaryLabel.TLabel")
        this.label_remaining.grid(row = 0, column = 2, padx = 10, pady = 10)

        # Button Pannel
        btn_panel = tk.Frame(wrapper, bg = "#1b1b1b")
        btn_panel.pack(pady = 8)
        
        # Custom Button Theme
        ttk.Button(btn_panel, text = "Theme", style = "My.TButton", command = this.OpenThemeEditor).pack(side = "left", padx = 8)

        this.style.configure("My.TButton", background ="#7c7c7c", foreground = "#ffffff")
        this.style.map("My.TButton", background = [("active", "#4d4d4d")])

        ttk.Button(btn_panel, text = "Clear History", style = "My.TButton", command = this.ClearList).pack(side = "left", padx = 8)
        ttk.Button(btn_panel, text = "History", style = "My.TButton", width = 18, command = this.ShowHistory).pack(side = "left", padx = 8)
        ttk.Button(btn_panel, text = "Category Summary", style = "My.TButton", width = 18, command = this.ViewCategorySummary).pack(side = "left", padx = 8)
        ttk.Button(btn_panel, text = "Export (CSV)", style = "My.TButton", width = 14, command = this.ExportCSV).pack(side = "left", padx = 8)
        ttk.Button(btn_panel, text = "Import (CSV)", style = "My.TButton", width = 14, command = this.ImportCSV).pack(side = "left", padx = 8)
        
        # ======= History Section ======= #
        this.frm_history = ttk.LabelFrame(wrapper, text = "Expense History")
        this.frm_history.pack(fill = "both", expand = True, padx = 5, pady = 10)
        
        # ===== Search Bar Section ===== #
        search_frame = tk.Frame(this.frm_history, bg = "#1b1b1b")
        search_frame.pack(fill = "x", padx = 10, pady = 5)
        
        tk.Label(search_frame, text = "Search:", fg = "white", bg = "#1b1b1b").pack(side = "left")
        this.entry_search = ttk.Entry(search_frame, width = 30)
        this.entry_search.pack(side = "left", padx = 10)
        
        ttk.Button(search_frame, text = "Find", command = this.SearchList).pack(side = "left", padx = 5)
        ttk.Button(search_frame, text = "Clear", command = this.ClearSearch).pack(side = "left", padx = 5)
        ttk.Button(search_frame, text = "Sort", style = "My.TButton", command = this.SortHistory).pack(side = "left", padx = 8)

         # ======= Date Section ======= #
        this.month_filter = ttk.Combobox(this.frm_history,values = ["All", "January", "February", "March","April", "May", "June", "July","August", "September", "October","November", "December"], state="readonly", width=15)

        this.month_filter.set("All")
        this.month_filter.pack(pady = 5)

        this.month_filter.bind("<<ComboboxSelected>>", lambda e: this.FilterByMonth())       

        enum_columns = ("Date/Time", "Category", "Amount", "Note")
        this.tree = ttk.Treeview(this.frm_history, columns = enum_columns, show = "headings", height = 12)

        for col in enum_columns:
            this.tree.heading(col, text = col)
            this.tree.column(col, width = 150, anchor = "center")

        this.tree.pack(fill = "both", expand = True, padx = 10, pady = 0)
        #ttk.Button(this.frm_history, text = "Sort by Highest Amount", command = this.SortHistory).pack(pady = 8)

        # Graph Parts
        this.frm_graph = tk.Frame(wrapper, bg = "#242424", padx = 10, pady = 10)
    # =============================== #
    #           END DESIGN            #
    # =============================== #

    def OpenThemeEditor(this):
        # Check if the window theme is exist and its already open.
        if hasattr(this, "theme_window") and this.theme_window is not None and this.theme_window.winfo_exists():
            this.theme_window.lift() # put it on the top of window.
            this.theme_window.focus_force()
            return

        # Create a new window
        this.theme_window = tk.Toplevel(this)
        win = this.theme_window
        win.title("Theme Editor")
        win.geometry("420x420")
        win.configure(bg="#1b1b1b")
        win.resizable(False, False)

        # Ensure the reference is cleared when the window is closed
        def on_close():
            this.theme_window = None
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_close)

        def slider_row(text, var_r, var_g, var_b, row):
            tk.Label(win, text = text, fg = "white", bg  ="#1b1b1b").grid(row = row, column = 0, pady = 10)
            
            tk.Scale(win, from_ = 0, to = 255, orient = "horizontal", variable = var_r, command = lambda e: this.ApplyFullTheme(), bg = "#1b1b1b", fg = "white", troughcolor = "#1b1b1b", activebackground = "#1b1b1b", highlightthickness = 0).grid(row = row, column = 1)
            tk.Scale(win, from_ = 0, to = 255, orient = "horizontal", variable = var_g, command = lambda e: this.ApplyFullTheme(), bg = "#1b1b1b", fg = "white", troughcolor = "#1b1b1b", activebackground = "#1b1b1b", highlightthickness = 0).grid(row = row, column = 2)
            tk.Scale(win, from_ = 0, to = 255, orient = "horizontal", variable = var_b, command = lambda e: this.ApplyFullTheme(), bg = "#1b1b1b", fg = "white", troughcolor = "#1b1b1b", activebackground = "#1b1b1b", highlightthickness = 0).grid(row = row, column = 3)

        slider_row("Background", this.bg_r, this.bg_g, this.bg_b, 0)
        slider_row("Text", this.text_r, this.text_g, this.text_b, 1)
        slider_row("Buttons", this.btn_r, this.btn_g, this.btn_b, 2)
        slider_row("Borders", this.border_r, this.border_g, this.border_b, 3)
        slider_row("EntryInput", this.entryinput_r, this.entryinput_g, this.entryinput_b, 4)


    def ApplyFullTheme(this):
        bg = f"#{this.bg_r.get():02x}{this.bg_g.get():02x}{this.bg_b.get():02x}"
        fg = f"#{this.text_r.get():02x}{this.text_g.get():02x}{this.text_b.get():02x}"
        btn = f"#{this.btn_r.get():02x}{this.btn_g.get():02x}{this.btn_b.get():02x}"
        border = f"#{this.border_r.get():02x}{this.border_g.get():02x}{this.border_b.get():02x}"
        entryinput = f"#{this.entryinput_r.get():02x}{this.entryinput_g.get():02x}{this.entryinput_b.get():02x}"

        this.configure(bg = bg)

        this.style.configure("TLabel", background = bg, foreground = fg)
        this.style.configure("TLabelframe", background = bg, foreground = fg, bordercolor = border)
        this.style.configure("TLabelframe.Label", background = bg, foreground = fg)
        this.style.configure("TButton", background = btn, foreground = fg)

        this.style.configure("TEntry", fieldbackground = entryinput, background = entryinput)
        
        # Normal State??
        this.style.configure("TCombobox", fieldbackground = entryinput, background = entryinput, foreground = fg, arrowcolor = fg)

        # Read Only State
        this.style.map("TCombobox", fieldbackground = [("readonly", entryinput)], background = [("readonly", entryinput)], foreground = [("readonly", fg)], arrowcolor = [("readonly", fg)])

        this.style.configure("My.TButton", background = btn, foreground = fg)
        this.style.map("TButton", background = [("active", border)])

        this.style.configure("Treeview", background = bg, fieldbackground = bg, foreground = fg)
        this.style.configure("Treeview.Heading", background = border, foreground = fg)

        this.style.configure("SummaryLabel.TLabel", background = bg, foreground = fg)
        this.style.configure("SummarySmall.TLabel", background = bg, foreground = fg)

        def repaint(widget):
            try:
                widget.configure(bg = bg, fg = fg)
            except:
                try:
                    widget.configure(bg = bg)
                except:
                    pass

            for child in widget.winfo_children():
                repaint(child)

        repaint(this)

    def ClearList(this):
        msg_confirm = messagebox.askyesno("Confirm", "Are you sure to continue?")
        if not msg_confirm:
            return
        
        BudgetData.get().data["expenses"] = []

        with open("budget_data.json", "w", encoding = "utf-8") as f:
            #json.clear()
            f.write("")

        for row in this.tree.get_children():
            this.tree.delete(row)

        messagebox.showinfo("Success", "Cleared History")
        this.entry_allowance.delete(0, tk.END)
        this.UpdateSummary()
        CUtils.get().DebugPrint("Cleared History successfully.")

    def ClearSearch(this):
        this.entry_search.delete(0, tk.END)
        this.UpdateSummary()

    def format_datetime(this, dt_string):  
        try:
            dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M")
            return dt.strftime("%B %d, %Y || %I:%M %p")
        except:
            return dt_string


    def SetAllowance(this):
        try:
            amount = CUtils.get().SafeFloat(this.entry_allowance.get())
            if amount <= 0:
                raise ValueError
            
            raw_value = this.entry_allowance.get().strip()

            digits_only = "".join(ch for ch in raw_value if ch.isdigit())
            if len(digits_only) >= 12:
                messagebox.showerror("Invalid Input", "Number must not exceed 12 digits.")
                return
            
            BudgetData.get().data["allowance"] = amount
            BudgetData.get().Save()
            messagebox.showinfo("Success", f"Allowance set to PHP {amount:.2f}")
            this.entry_allowance.delete(0, tk.END)
            this.UpdateWarning()
            this.UpdateSummary()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number.")

    def AddAllowance(this):
        try:
            amount = CUtils.get().SafeFloat(this.entry_allowance.get())
            if amount <= 0:
                raise ValueError
            
            raw_value = this.entry_allowance.get().strip()

            digits_only = "".join(ch for ch in raw_value if ch.isdigit())
            if len(digits_only) >= 12:
                messagebox.showerror("Invalid Input", "Number must not exceed 12 digits.")
                return
            
            BudgetData.get().data["allowance"] += amount
            BudgetData.get().Save()
            messagebox.showinfo("Success!", f"PHP {amount:.2f} added to allowance.")
            this.entry_allowance.delete(0, tk.END)
            this.UpdateWarning()
            this.UpdateSummary()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
    
    # For Numerical Dates
    # def SearchList(this):
    #     query = this.entry_search.get().lower().strip()

    #     # Clear previous rows
    #     for row in this.tree.get_children():
    #         this.tree.delete(row)

    #     expenses = BudgetData.get().data.get("expenses", [])

    #     for e in reversed(expenses):
    #         date = e["date"]
    #         category = e["category"].lower()
    #         note = e["note"].lower()
    #         amount = f"{e['amount']:.2f}"

    #         # Check if query matches any field
    #         if (query in date.lower()
    #             or query in category
    #             or query in note
    #             or query in amount):
    #             this.tree.insert("", tk.END, values = (e["date"], e["category"], f"PHP {e['amount']:.2f}", e["note"]))

    def SearchList(this):
        try:
            query = this.entry_search.get().lower().strip()

            # Clear previous rows
            for row in this.tree.get_children():
                this.tree.delete(row)

            expenses = BudgetData.get().data.get("expenses", [])

            for e in reversed(expenses):
                try:
                    # Format the date safely
                    formatted_date = this.format_datetime(e.get("date", "")).lower()
                except Exception as ex_date:
                    formatted_date = str(e.get("date", "")).lower()
                    print(f"[WARN] Failed to parse date '{e.get('date', '')}': {ex_date}")

                category = str(e.get("category", "")).lower()
                note = str(e.get("note", "")).lower()
                amount = f"{float(e.get('amount', 0)):.2f}"

                # Check if query matches any field
                if (query in formatted_date
                    or query in category
                    or query in note
                    or query in amount):
                    try:
                        this.tree.insert("", tk.END, values = (this.format_datetime(e.get("date", "")), e.get("category", ""), f"PHP {float(e.get('amount', 0)):.2f}", e.get("note", "")))
                    except Exception as ex_insert:
                        print(f"[ERROR] Failed to insert row into treeview: {ex_insert}")

        except Exception as ex:
            print(f"[ERROR] SearchList failed: {ex}")
            messagebox.showerror("Search Error", "An error occurred while searching. Please check your data.")


    def AddExpense(this):
        try:
            category = this.combo_category.get()
            amount = CUtils.get().SafeFloat(this.entry_amount.get())
            note = this.entry_note.get()

            if amount <= 0:
                raise ValueError
            
            raw_value = this.entry_amount.get().strip()
            digits_only = "".join(ch for ch in raw_value if ch.isdigit())
            if len(digits_only) >= 12:
                messagebox.showerror("Invalid Input", "Number must not exceed 12 digits.")
                return
            
            if len(note) >= 15:
                messagebox.showerror("Invalid Input", "The note must not exceed 15 characters.")
                return

            BudgetData.get().AddExpense(category, amount, note)

            # clear the fields and refocus it.
            this.entry_amount.delete(0, tk.END)
            this.entry_note.delete(0, tk.END)
            this.entry_amount.focus_set()

            this.UpdateWarning()
            this.UpdateSummary()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid expense amount.")

    def UpdateWarning(this):
        try:
            allowance = BudgetData.get().data.get("allowance", 0.0)
            spent = BudgetData.get().GetTotalSpent()
            remaining = allowance - spent

            this.label_allowance.config(text = f"Allowance: PHP {allowance:.2f}")
            this.label_spent.config(text = f"Total Spent: PHP {spent:.2f}")

            threshold = BudgetData.get().data.get("warning_threshold", 25) / 100
            
            with open("budget_data.json", "r", encoding = "utf-8") as f:
                content = f.read().strip()

            # check if the content of json is blank
            if not BudgetData.get().data["expenses"] or content == "":
                return
                        
            if remaining <= 0:
                this.label_remaining.config(text = f"Remaining: -PHP {abs(remaining):.2f} (Over Budget!)", foreground = "#ff4444")
                messagebox.showerror("Warning", "Out of Budget!")
            elif remaining / allowance <= threshold:
                this.label_remaining.config(text = f"Remaining: PHP {remaining:.2f} (Budget Warning!)", foreground = "#ff6600")
                messagebox.showerror("Warning", "Budget on Limit!")
            else:
                this.label_remaining.config(text = f"Remaining: PHP {remaining:.2f}", foreground = "#44ff44")

        except Exception as e:
            print("[ERROR] UpdateSummary:", e)
            traceback.print_exc()

    def UpdateSummary(this):
        try:
            #allowance = BudgetData.get().data.get("allowance", 0.0)
            #spent = BudgetData.get().GetTotalSpent()
            #remaining = allowance - spent

            #this.label_allowance.config(text = f"Allowance: PHP {allowance:.2f}")
            #this.label_spent.config(text = f"Total Spent: PHP {spent:.2f}")

            #threshold = BudgetData.get().data.get("warning_threshold", 25) / 100
            
            #with open("budget_data.json", "r", encoding = "utf-8") as f:
            #    content = f.read().strip()

            # check if the content of json is blank
            #if not BudgetData.get().data["expenses"] or content == "":
            #    return
                        
            # if remaining <= 0:
            #     this.label_remaining.config(text = f"Remaining: -PHP {abs(remaining):.2f} (Over Budget!)", foreground = "#ff4444")
            #     messagebox.showerror("Warning", "Out of Budget!")
            # elif remaining / allowance <= threshold:
            #     this.label_remaining.config(text = f"Remaining: PHP {remaining:.2f} (Budget Warning!)", foreground = "#ff6600")
            #     messagebox.showerror("Warning", "Budget on Limit!")
            # else:
            #     this.label_remaining.config(text = f"Remaining: PHP {remaining:.2f}", foreground = "#44ff44")

            # Refresh history
            for row in this.tree.get_children():
                this.tree.delete(row)
                
            for e in reversed(BudgetData.get().data.get("expenses", [])):
                #this.tree.insert("", tk.END, values = (e["date"], e["category"], f"PHP {e['amount']:.2f}", e["note"]))
                formatted_date = this.format_datetime(e["date"])
                this.tree.insert("", tk.END, values = (formatted_date, e["category"], f"PHP {float(e['amount']):,.2f}", e["note"]))

        except Exception as e:
            print("[ERROR] UpdateSummary:", e)
            traceback.print_exc()

    # def UpdateSummary(this):
    #    try:
    #        allowance = BudgetData.get().data.get("allowance", 0.0)
    #        spent = BudgetData.get().GetTotalSpent()

    #        remaining = allowance - spent

    #        this.label_allowance.config(text = f"Allowance: PHP {allowance:.2f}")
    #        this.label_spent.config(text = f"Total Spent: PHP {spent:.2f}")

    #        this.label_remaining.configure(style = "SummaryLabel.TLabel")
    #        if remaining < 0:
    #            this.label_remaining.config(text = f"Remaining: -PHP {abs(remaining):.2f}", foreground = "#ff4444")
    #        else:
    #            this.label_remaining.config(text = f"Remaining: PHP {remaining:.2f}", foreground = "#44ff44")

    #        # Refresh History Section
    #        for row in this.tree.get_children():
    #            this.tree.delete(row)

    #        for e in reversed(BudgetData.get().data.get("expenses", [])):
    #            this.tree.insert("", tk.END, values = (e["date"], e["category"], f"PHP {e['amount']:.2f}", e["note"]))

    #    except Exception as e:
    #        print("[ERROR] UpdateSummary:", e)
    #        traceback.print_exc()

    def ViewCategorySummary(this):
        try:
            expenses = BudgetData.get().data.get("expenses", [])
            if not expenses:
                messagebox.showinfo("No Data", "No expenses recorded yet.")
                return

            this.frm_history.pack_forget()
            this.frm_graph.pack(fill = "both", expand = True, padx = 10, pady = 5)

            for widget in this.frm_graph.winfo_children():
                widget.destroy()

            # Timeframe & Metric Sections
            top_controls = tk.Frame(this.frm_graph, bg = "#1b1b1b")
            top_controls.pack(fill = "x", padx = 10, pady = 5)

            ttk.Label(top_controls, text = "Timeframe:", background = "#1b1b1b", foreground = "white").pack(side = "left", padx = 5)
            timeframe_options = ["Current Day", "Current Week", "Current Month", "All Time"]
            timeframe_combo = ttk.Combobox(top_controls, values = timeframe_options, state = "readonly", width = 15)
            timeframe_combo.set("Current Month")
            timeframe_combo.pack(side = "left", padx = 5)

            ttk.Label(top_controls, text = "Metric:", background = "#1b1b1b", foreground = "white").pack(side = "left", padx = 5)
            metric_options = ["Spent", "Number of Expenses", "Highest Expense", "Lowest Expense", "Average Expense"]
            metric_combo = ttk.Combobox(top_controls, values = metric_options, state = "readonly", width = 18)
            metric_combo.set("Spent")
            metric_combo.pack(side = "left", padx = 5)

            # Helper functions.
            from datetime import datetime, timedelta
            def filter_expenses(expenses, timeframe):
                now = datetime.now()
                filtered = []
                for e in expenses:
                    try:
                        dt = datetime.strptime(e["date"], "%Y-%m-%d %H:%M")
                    except:
                        continue
                    if timeframe == "Current Day" and dt.date() != now.date():
                        continue
                    elif timeframe == "Current Week":
                        start_week = now - timedelta(days = now.weekday())
                        if dt.date() < start_week.date():
                            continue
                    elif timeframe == "Current Month" and dt.month != now.month:
                        continue
                    filtered.append(e)
                return filtered

            # Draw a Chart
            def draw_chart(event = None):
                # Clear previous canvas
                for w in this.frm_graph.winfo_children():
                    if isinstance(w, tk.Canvas):
                        w.destroy()

                filtered = filter_expenses(expenses, timeframe_combo.get())
                if not filtered:
                    canvas = tk.Canvas(this.frm_graph, width = 820, height = 100, bg = "#1b1b1b", bd = 0, highlightthickness = 0)
                    canvas.pack(expand = True, fill="both", padx = 10, pady = 10)
                    canvas.create_text(410, 50, text = "No data for selected timeframe", fill = "white", font = ("Segoe UI", 14, "bold"))
                    return

                # Build summary
                summary = {}
                for e in filtered:
                    cat = e["category"]
                    amt = float(e["amount"])
                    if cat not in summary:
                        summary[cat] = {"spent": 0, "count": 0, "highest": amt, "lowest": amt}

                    summary[cat]["spent"] += amt
                    summary[cat]["count"] += 1
                    summary[cat]["highest"] = max(summary[cat]["highest"], amt)
                    summary[cat]["lowest"] = min(summary[cat]["lowest"], amt)

                canvas = tk.Canvas(this.frm_graph, width = 820, height = 400, bg = "#1b1b1b", bd = 0, highlightthickness = 0)
                canvas.pack(expand = True, fill = "both", padx = 10, pady = 10)

                items = sorted(summary.items(), key = lambda x: x[1]["spent"], reverse = True)
                max_val = 0
                for _, data in items:
                    metric = metric_combo.get()
                    if metric == "Spent":
                        value = data["spent"]
                    elif metric == "Number of Expenses":
                        value = data["count"]
                    elif metric == "Highest Expense":
                        value = data["highest"]
                    elif metric == "Lowest Expense":
                        value = data["lowest"]
                    elif metric == "Average Expense":
                        value = data["spent"] / data["count"] if data["count"] > 0 else 0
                    max_val = max(max_val, value)

                margin_left = 180
                bar_area_width = 560
                top_pos = 30
                bar_height = 32
                gap = 18

                canvas.create_text(20, 12, text = "Category", fill = "white", anchor = "w", font = ("Segoe UI", 11, "bold"))
                canvas.create_text(margin_left + bar_area_width, 12, text = f"{metric_combo.get()} — %", fill = "white", anchor = "e", font = ("Segoe UI", 11, "bold"))

                enum_category_colors = {
                    "Food": "#ff9f1c",
                    "Transport": "#2ec4b6",
                    "School": "#3a86ff",
                    "Personal": "#8bd346",
                    "Others": "#9e9e9e"
                }

                y = top_pos
                total_metric = 0
                for cat, data in items:
                    metric = metric_combo.get()
                    if metric == "Spent":
                        value = data["spent"]
                    elif metric == "Number of Expenses":
                        value = data["count"]
                    elif metric == "Highest Expense":
                        value = data["highest"]
                    elif metric == "Lowest Expense":
                        value = data["lowest"]
                    elif metric == "Average Expense":
                        value = data["spent"] / data["count"] if data["count"] > 0 else 0

                    total_metric += value
                    bar_len = (value / max_val) * bar_area_width if max_val > 0 else 0
                    canvas.create_text(20, y + bar_height / 2, text = cat, fill = "white", anchor = "w", font = ("Segoe UI", 11))
                    canvas.create_rectangle(margin_left, y, margin_left + bar_area_width, y + bar_height, fill = "#2a2a2a", outline = "")
                    color = enum_category_colors.get(cat, "#ffffff")
                    canvas.create_rectangle(margin_left, y, margin_left + bar_len, y + bar_height, fill = color, outline = "")
                    value_text = f"PHP {value:.2f}" if metric == "Spent" else str(int(value))
                    pct_text = f"{(value / total_metric * 100):.1f}%" if total_metric > 0 else "0%"
                    canvas.create_text(margin_left + bar_area_width, y + bar_height / 2, text = f"{value_text} — {pct_text}", fill = "white", anchor = "e", font = ("Segoe UI", 10))
                    y += bar_height + gap

                canvas.create_text(20, y + 6, text=f"Total: {total_metric:.2f}" if metric_combo.get() == "Spent" else f"Total: {int(total_metric)}", fill = "#ffaa00", anchor = "w", font = ("Segoe UI", 11, "bold"))

            # Bind comboboxes to update chart dynamically
            timeframe_combo.bind("<<ComboboxSelected>>", draw_chart)
            metric_combo.bind("<<ComboboxSelected>>", draw_chart)

            # Initial draw
            draw_chart()

        except Exception as e:
            print("[ERROR] ViewCategorySummary:", e)
            traceback.print_exc()
       
    def FilterByMonth(this):
        try:
            choice = this.month_filter.get()

            for row in this.tree.get_children():
                this.tree.delete(row)

            expenses = BudgetData.get().data.get("expenses", [])

            for e in reversed(expenses):
                date_str = e["date"]
                month_num = int(date_str.split("-")[1])

                if choice != "All":
                    selected_index = this.month_filter["values"].index(choice)
                    if selected_index != month_num:
                        continue

                this.tree.insert("", tk.END, values = (e["date"], e["category"], f"PHP {e['amount']:.2f}", e["note"]))
        except:
            pass

    def SetWarning(this):
        try:
            threshold = float(this.entry_warning.get())
            if not 0 < threshold < 100:
                raise ValueError
            
            with open("budget_data.json", "r", encoding = "utf-8") as f:
                content = f.read().strip()

            BudgetData.get().data["warning_threshold"] = threshold
            BudgetData.get().Save()
            this.UpdateSummary()
            messagebox.showinfo("Success", f"Budget warning set at {threshold:.0f}% remaining.")

            # check if the content of json is blank
            if not BudgetData.get().data["expenses"] or content == "":
                return

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid percentage (1-99).")

    def ShowHistory(this):
        this.frm_graph.pack_forget()
        this.frm_history.pack(fill = "both", expand = True, padx = 10, pady = 5)
        this.entry_allowance.delete(0, tk.END)
        this.UpdateSummary()

    def SortHistory(this):
        try:
            expenses = BudgetData.get().data.get("expenses", [])
            if not expenses:
                messagebox.showinfo("No Data", "No expenses to sort.")
                return

            with open("budget_data.json", "r", encoding = "utf-8") as f:
                content = f.read().strip()

            # check if the content of json is blank
            if not BudgetData.get().data["expenses"] or content == "":
                return
            
            # Flipping the switch
            this.sort_reverse = not this.sort_reverse
            
            expenses.sort(key = lambda e: e["amount"], reverse = this.sort_reverse)

            BudgetData.get().Save()
            this.UpdateSummary()
            this.ShowHistory()
        except Exception as e:
            print("[ERROR] SortHistory:", e)
            traceback.print_exc()

    def ExportCSV(this):
        try:
            import csv
            from tkinter import filedialog

            expenses = BudgetData.get().data.get("expenses", [])
            if not expenses:
                messagebox.showinfo("No Data", "No expenses to export.")
                return

            file_path = filedialog.asksaveasfilename(defaultextension = ".csv", filetypes = [("CSV files", "*.csv")], title = "Save CSV")
            if not file_path:
                return

            with open(file_path, "w", newline = "", encoding = "utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["date", "category", "amount", "note"])
                for e in expenses:
                    writer.writerow([e.get("date"), e.get("category"), f"{e.get('amount'):.2f}", e.get("note")])

            messagebox.showinfo("Exported", f"Exported {len(expenses)} records to\n{file_path}")
        except Exception as e:
            print("[ERROR] ExportCSV:", e)
            traceback.print_exc()
            messagebox.showerror("Error", "Failed to export CSV.")

    def ImportCSV(this):
        try:
            import csv
            from tkinter import filedialog

            file_path = filedialog.askopenfilename(filetypes = [("CSV files", "*.csv")], title = "Import CSV")
            if not file_path:
                return

            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                expenses = list(reader)

            for row in expenses:
                BudgetData.get().AddExpense(row.get("category"), float(row.get("amount")),row.get("note"))

            messagebox.showinfo("Success", "CSV imported successfully!")
            this.UpdateSummary()

        except Exception as e:
            print("[ERROR] ImportCSV:", e)
            traceback.print_exc()
            messagebox.showerror("Error", "Failed to import CSV.")

if __name__ == "__main__":
    try:
        app = BudgetApp()
        app.mainloop()
    except Exception as e:
        print("[CRITICAL ERROR] Application crashed:", e)
        traceback.print_exc()
