import tkinter as tk

BUTTON_FONT = ("Helvetica", 16)
DISPLAY_FONT = ("Helvetica", 28, "bold")

BUTTONS = [
    ["C", "±", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "+"],
    ["0", ".", "="],
]

OPERATOR_MAP = {"÷": "/", "×": "*", "−": "-", "+": "+"}

BG         = "#1c1c1e"
DISPLAY_BG = "#1c1c1e"
FUNC_BG    = "#a5a5a5"
FUNC_FG    = "#000000"
OP_BG      = "#ff9f0a"
OP_FG      = "#ffffff"
NUM_BG     = "#333335"
NUM_FG     = "#ffffff"
ZERO_BG    = "#333335"


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.expression = ""
        self.display_var = tk.StringVar(value="0")
        self.just_evaluated = False

        self._build_ui()

    def _build_ui(self):
        display_frame = tk.Frame(self.root, bg=DISPLAY_BG)
        display_frame.pack(fill="x", padx=12, pady=(20, 8))
        self.expr_label = tk.Label(
            display_frame,
            text="",
            font=("Helvetica", 13),
            bg=DISPLAY_BG,
            fg="#888888",
            anchor="e",
        )
        self.expr_label.pack(fill="x")

        tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=DISPLAY_FONT,
            bg=DISPLAY_BG,
            fg="#ffffff",
            anchor="e",
        ).pack(fill="x")

        grid_frame = tk.Frame(self.root, bg=BG)
        grid_frame.pack(padx=12, pady=(0, 12))

        for r, row in enumerate(BUTTONS):
            for c, label in enumerate(row):
                colspan = 2 if label == "0" else 1
                btn = tk.Button(
                    grid_frame,
                    text=label,
                    font=BUTTON_FONT,
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    **self._btn_style(label),
                    command=lambda l=label: self._on_press(l),
                )
                btn.grid(
                    row=r, column=c,
                    columnspan=colspan,
                    padx=5, pady=5,
                    ipadx=18 if label != "0" else 46,
                    ipady=14,
                    sticky="ew",
                )

    def _btn_style(self, label):
        if label in ("C", "±", "%"):
            return {"bg": FUNC_BG, "fg": FUNC_FG, "activebackground": "#c8c8c8", "activeforeground": FUNC_FG}
        if label in ("÷", "×", "−", "+", "="):
            return {"bg": OP_BG,   "fg": OP_FG,   "activebackground": "#ffb340", "activeforeground": OP_FG}
        return {"bg": NUM_BG, "fg": NUM_FG, "activebackground": "#4a4a4c", "activeforeground": NUM_FG}

    def _on_press(self, label):
        if label == "C":
            self._clear()
        elif label == "±":
            self._toggle_sign()
        elif label == "%":
            self._percent()
        elif label == "=":
            self._evaluate()
        elif label in OPERATOR_MAP:
            self._append_operator(label)
        else:
            self._append_digit(label)

    def _clear(self):
        self.expression = ""
        self.display_var.set("0")
        self.expr_label.config(text="")
        self.just_evaluated = False

    def _append_digit(self, digit):
        if self.just_evaluated:
            self.expression = ""
            self.just_evaluated = False

        parts = self.expression.replace("(", "").split(any_op := self._last_op_split())
        current = parts[-1] if parts else ""
        if digit == "." and "." in current:
            return

        self.expression += digit
        display = self.expression.split(any_op)[-1] if any_op else self.expression
        self.display_var.set(self.expression.split(any_op)[-1] or "0")

    def _last_op_split(self):
        for ch in reversed(self.expression):
            if ch in "+-*/":
                return ch
        return ""

    def _append_operator(self, op):
        self.just_evaluated = False
        sym = OPERATOR_MAP[op]

        if self.expression and self.expression[-1] in "+-*/":
            self.expression = self.expression[:-1]

        if not self.expression:
            self.expression = "0"

        self.expression += sym
        self.expr_label.config(text=self.expression)
        self.display_var.set(op)

    def _evaluate(self):
        if not self.expression:
            return
        try:
            result = eval(self.expression)  
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.expr_label.config(text=self.expression + " =")
            self.display_var.set(str(result))
            self.expression = str(result)
            self.just_evaluated = True
        except ZeroDivisionError:
            self.display_var.set("Error")
            self.expression = ""
            self.just_evaluated = False
        except Exception:
            self.display_var.set("Error")
            self.expression = ""
            self.just_evaluated = False

    def _toggle_sign(self):
        current = self.display_var.get()
        try:
            val = float(current)
            val = -val
            result = int(val) if val.is_integer() else val
            self.display_var.set(str(result))
            # Reflect in expression
            if self.expression:
                last_op = self._last_op_split()
                if last_op:
                    idx = self.expression.rfind(last_op)
                    self.expression = self.expression[:idx + 1] + str(result)
                else:
                    self.expression = str(result)
        except ValueError:
            pass

    def _percent(self):
        current = self.display_var.get()
        try:
            val = float(current) / 100
            result = int(val) if float(val).is_integer() else val
            self.display_var.set(str(result))
            last_op = self._last_op_split()
            if last_op:
                idx = self.expression.rfind(last_op)
                self.expression = self.expression[:idx + 1] + str(result)
            else:
                self.expression = str(result)
        except ValueError:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()