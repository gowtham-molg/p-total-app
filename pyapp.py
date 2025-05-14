import tkinter as tk
from tkinter import ttk, messagebox

DEFAULT_PSTEPS = [80, 85, 90, 95, 99, 99.5, 99.9, 99.95]

def calculate_totals():
    try:
        n = float(entry_n.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for n.")
        return

    for row_id in tree.get_children():
        try:
            p_step_percent = float(tree.item(row_id, 'values')[0])
            p_step = p_step_percent / 100.0
            p_total = 100 * (p_step ** n)
            tree.set(row_id, column="ptotal", value=f"{p_total:.3f}")
        except ValueError:
            tree.set(row_id, column="ptotal", value="Invalid")
 
 #hmmmmmm
def edit_cell(event):
    region = tree.identify_region(event.x, event.y)
    if region != "cell":
        return

    column = tree.identify_column(event.x)
    row_id = tree.identify_row(event.y)
    if not row_id or column not in ("#1", "#2"):
        return

    col_index = int(column.replace("#", "")) - 1
    col_key = tree["columns"][col_index]
    x, y, width, height = tree.bbox(row_id, column)
    value = tree.set(row_id, col_key)

    edit = tk.Entry(root)
    edit.place(x=x + tree.winfo_x(), y=y + tree.winfo_y(), width=width, height=height)
    edit.insert(0, value)
    edit.focus()

    def save_and_recalculate(event=None):
        new_value = edit.get()
        try:
            val = float(new_value)
            tree.set(row_id, col_key, val)

            n = float(entry_n.get())
            if col_key == "pstep":
                # Forward calculation: ptotal = 100 * (pstep/100)^n
                p_step = val / 100.0
                p_total = 100 * (p_step ** n)
                tree.set(row_id, "ptotal", f"{p_total:.3f}")
            elif col_key == "ptotal":
                # Reverse calculation: pstep = (ptotal/100)^(1/n)
                p_total = val / 100.0
                if p_total <= 0:
                    raise ValueError
                p_step = (p_total) ** (1 / n)
                tree.set(row_id, "pstep", f"{p_step * 100:.3f}")
        except ValueError:
            tree.set(row_id, col_key, "Invalid")

        edit.destroy()

    edit.bind("<Return>", save_and_recalculate)
    edit.bind("<KP_Enter>", save_and_recalculate)
    edit.bind("<FocusOut>", lambda e: edit.destroy())

# GUI Setup
root = tk.Tk()
root.title("Cumulative P-TOTAL From P-STEP")

# Input frame
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

tk.Label(top_frame, text="Number of Steps (n):").pack(side=tk.LEFT, padx=(0, 5))
entry_n = tk.Entry(top_frame, width=10)
entry_n.pack(side=tk.LEFT)
entry_n.insert(0, "56")
entry_n.bind("<Return>", lambda e: calculate_totals())
entry_n.bind("<KP_Enter>", lambda e: calculate_totals())

tk.Button(top_frame, text="Calculate", command=calculate_totals).pack(side=tk.LEFT, padx=10)

# Table
columns = ("pstep", "ptotal")
tree = ttk.Treeview(root, columns=columns, show='headings', height=10)

tree.heading("pstep", text="P-STEP (%)")
tree.heading("ptotal", text="Cumulative P-TOTAL")

tree.column("pstep", anchor=tk.CENTER, width=100)
tree.column("ptotal", anchor=tk.CENTER, width=150)

# Default rows
for p in DEFAULT_PSTEPS:
    tree.insert('', 'end', values=(p, ""))

tree.pack(padx=10, pady=10)
tree.bind("<Double-1>", edit_cell)

# Styling
style = ttk.Style()
style.configure("Treeview", rowheight=25)
style.map("Treeview", background=[('selected', '#cce6ff')])
style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
style.configure("Treeview", bordercolor='gray', relief='solid')

root.mainloop()
