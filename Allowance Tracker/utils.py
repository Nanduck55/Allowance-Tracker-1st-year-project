import traceback
from singleton import Singleton

class CUtils(Singleton):
    def SafeFloat(this, value, default=0.0):
        try:
            return float(value)
        except ValueError:
            print(f"[DEBUG] Invalid float conversion: {value}")
            return default
        except Exception as e:
            print("[ERROR] Unexpected error converting to float:", e)
            traceback.print_exc()
            return default

    def DebugPrint(this, msg):
        print(f"[DEBUG] {msg}")
