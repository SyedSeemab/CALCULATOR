import tkinter as tk
import ast
import operator

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg
}

def safe_eval(expr):
    def _eval(node):
        if isinstance(node, ast.Num):  # number
            return node.n
        elif isinstance(node, ast.BinOp):  # + - * /
            return OPS[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):  # -x
            return OPS[type(node.op)](_eval(node.operand))
        else:
            raise Exception("Invalid Expression")

    tree = ast.parse(expr, mode='eval')
    return _eval(tree.body)

BUTTON_FONT = ("Helvetica", 16)
DISPLAY_FONT = ("Helvetica", 28, "bold")

BUTTONS = [
    ["C", "±", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "+"],
    ["0", ".", "="],
]

OP_MAP = {"÷": "/", "×": "*", "−": "-", "+": "+"}

BG = "#1c1c1e"
FUNC_BG = "#a5a5a5"
OP_BG = "#ff9f0a"
NUM_BG = "#333335"

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Better Calculator")
        self.root.configure(bg=BG)

        self.current = "0"
        self.expression = ""
        self.reset_next = False

        self.display_var = tk.StringVar(value="0")

        self.build_ui()

    def build_ui(self):
        display = tk.Label(
            self.root,
            textvariable=self.display_var,
            font=DISPLAY_FONT,
            bg=BG,
            fg="white",
            anchor="e",
            padx=10,
            pady=20
        )
        display.pack(fill="x")

        frame = tk.Frame(self.root, bg=BG)
        frame.pack()

        for r, row in enumerate(BUTTONS):
            c = 0
            for label in row:
                colspan = 2 if label == "0" else 1

                btn = tk.Button(
                    frame,
                    text=label,
                    font=BUTTON_FONT,
                    width=5,
                    height=2,
                    bd=0,
                    command=lambda l=label: self.on_click(l),
                    bg=self.get_color(label),
                    fg="white"
                )

                btn.grid(row=r, column=c, columnspan=colspan, padx=5, pady=5, sticky="nsew")
                c += colspan

    def get_color(self, label):
        if label in ("C", "±", "%"):
            return FUNC_BG
        elif label in OP_MAP or label == "=":
            return OP_BG
        return NUM_BG

    def on_click(self, label):
        if label.isdigit() or label == ".":
            self.input_number(label)
        elif label in OP_MAP:
            self.input_operator(label)
        elif label == "=":
            self.calculate()
        elif label == "C":
            self.clear()
        elif label == "±":
            self.toggle_sign()
        elif label == "%":
            self.percent()

    def input_number(self, num):
        if self.reset_next:
            self.current = "0"
            self.reset_next = False

        if num == "." and "." in self.current:
            return

        if self.current == "0" and num != ".":
            self.current = num
        else:
            self.current += num

        self.display_var.set(self.current)

    def input_operator(self, op):
        if self.current:
            self.expression += self.current

        if self.expression and self.expression[-1] in "+-*/":
            self.expression = self.expression[:-1]

        self.expression += OP_MAP[op]
        self.current = ""
        self.reset_next = False

    def calculate(self):
        try:
            self.expression += self.current
            result = safe_eval(self.expression)

            if isinstance(result, float) and result.is_integer():
                result = int(result)

            self.display_var.set(str(result))
            self.current = str(result)
            self.expression = ""
            self.reset_next = True

        except Exception:
            self.display_var.set("Error")
            self.clear()

    def clear(self):
        self.current = "0"
        self.expression = ""
        self.display_var.set("0")

    def toggle_sign(self):
        if self.current:
            if self.current.startswith("-"):
                self.current = self.current[1:]
            else:
                self.current = "-" + self.current
            self.display_var.set(self.current)

    def percent(self):
        if self.current:
            value = float(self.current) / 100
            self.current = str(value)
            self.display_var.set(self.current)

if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()