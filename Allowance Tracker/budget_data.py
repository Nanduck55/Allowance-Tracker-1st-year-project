import json, os, traceback
from datetime import datetime
from collections import defaultdict
from singleton import Singleton
from utils import CUtils

DATA_FILE = "budget_data.json"

class BudgetData(Singleton):
    def __init__(this):
        if hasattr(this, "initialized"):
            return
        this.initialized = True

        this.data = {
            "allowance": 0.0,
            "expenses": [],
            "currency": "PHP",
            "alert_limit": 10
        }
        
        this.Load()

    def Load(this):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    this.data = json.load(f)
                CUtils.get().DebugPrint("Data loaded successfully.")
            else:
                CUtils.get().DebugPrint("No existing data file found. Creating new...")
                this.Save()
        except json.JSONDecodeError:
            print("[ERROR] JSON file corrupted. Re-creating...")
            this.data = {"allowance": 0.0, "expenses": [], "currency": "PHP", "alert_limit": 10}
            this.Save()
        except Exception as e:
            print("[ERROR] Failed to load data:", e)
            traceback.print_exc()

    def Save(this):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(this.data, f, indent=2)
            CUtils.get().DebugPrint("Data saved successfully.")
        except Exception as e:
            print("[ERROR] Failed to save data:", e)
            traceback.print_exc()

    def AddExpense(this, category, amount, note=""):
        try:
            expense = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "category": category,
                "amount": float(amount),
                "note": note
            }
            this.data["expenses"].append(expense)
            this.Save()
        except ValueError:
            print("[ERROR] Invalid amount entered.")
            raise
        except Exception as e:
            print("[ERROR] Unexpected error while adding expense:", e)
            traceback.print_exc()

    def GetTotalSpent(this):
        try:
            return sum(e["amount"] for e in this.data["expenses"])
        except Exception as e:
            print("[ERROR] Failed to calculate total spent:", e)
            traceback.print_exc()
            return 0.0

    def GetRemaining(this):
        try:
            return this.data["allowance"] - this.GetTotalSpent()
        except Exception as e:
            print("[ERROR] Failed to compute remaining balance:", e)
            traceback.print_exc()
            return 0.0

    def GetSummaryByCategory(this):
        try:
            summary = defaultdict(float)
            
            for e in this.data["expenses"]:
                summary[e["category"]] += e["amount"]
                
            return summary
        except Exception as e:
            print("[ERROR] Failed to summarize categories:", e)
            traceback.print_exc()
            return {}
