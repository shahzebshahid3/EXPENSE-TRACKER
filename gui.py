from tkinter import *
from tkinter import ttk, messagebox
from reportlab.pdfgen import canvas

#  PIE CHART 

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


ASM_FILE = "finasm.asm"


MARS_PATH = r"C:\Users\Yousuf Traders\OneDrive\Desktop\Mars4_5.jar"


records = []
balance = 0
current_mode = "dark"

# ================= WINDOW =================

root = Tk()
root.title("FinASM Expense Tracker")
root.geometry("1350x760")
root.configure(bg="#1e1e1e")

# ================= THEME FUNCTION =================

def set_mode(mode):

    global current_mode

    current_mode = mode

    if mode == "light":

        bg_main = "white"
        text_main = "black"
        panel_bg = "#f0f0f0"

    else:

        bg_main = "#1e1e1e"
        text_main = "white"
        panel_bg = "#2d2d2d"

    root.configure(bg=bg_main)

    title.config(bg=bg_main, fg=text_main)

    input_panel.config(bg=bg_main)

    left_panel.config(bg=panel_bg)

    right_panel.config(bg=bg_main)

    balance_label.config(
        bg=bg_main,
        fg="green" if mode == "light" else "lightgreen"
    )

    warning_label.config(
        bg=bg_main
    )

    dashboard_panel.config(bg=bg_main)

    top_frame.config(bg=bg_main)

    middle_frame.config(bg=bg_main)

    table_frame.config(bg=bg_main)

    chart_frame.config(bg=bg_main)

    bottom_frame.config(bg=bg_main)

    category_label.config(bg=panel_bg, fg=text_main)

    amount_label.config(bg=panel_bg, fg=text_main)

    show_pie_chart()

# ================= FUNCTIONS =================

def update_balance():
    balance_label.config(text=f"Balance: Rs {balance}")

def save_data():

    with open("data.txt", "w") as file:

        for rec in records:

            line = f"{rec[0]},{rec[1]},{rec[2]}\n"

            file.write(line)

# ================= DELETE FUNCTION =================

def delete_record():

    global balance

    selected_item = tree.selection()

    if not selected_item:
        messagebox.showerror("Error", "Select Record First")
        return

    item = selected_item[0]

    values = tree.item(item, "values")

    rec_type = values[0]
    category = values[1]
    amount = int(values[2])

    # REMOVE FROM RECORDS
    for rec in records:

        if rec[0] == rec_type and rec[1] == category and rec[2] == amount:
            records.remove(rec)
            break

    # UPDATE BALANCE
    if rec_type == "Income":
        balance -= amount
    else:
        balance += amount

    tree.delete(item)

    # REMOVE WARNING IF BALANCE POSITIVE
    if balance > 0:
        warning_label.config(text="")

    update_balance()

    update_dashboard()

    refresh_dashboard_table()

    save_data()

    messagebox.showinfo("Deleted", "Record Deleted Successfully")

# ================= ADD INCOME =================

def add_income():

    global balance

    category = category_box.get()
    amount = amount_entry.get()

    if amount == "":
        messagebox.showerror("Error", "Enter Amount")
        return

    amount = int(amount)

    records.append(("Income", category, amount))

    tree.insert("", END, values=("Income", category, amount))

    balance += amount

    # CLEAR WARNING
    if balance > 0:
        warning_label.config(text="")

    update_balance()

    update_dashboard()

    refresh_dashboard_table()

    save_data()

    amount_entry.delete(0, END)

# ================= ADD EXPENSE =================

def add_expense():

    global balance

    category = category_box.get()
    amount = amount_entry.get()

    if amount == "":
        messagebox.showerror("Error", "Enter Amount")
        return

    amount = int(amount)

    # ================= NEGATIVE CHECK =================

    if balance - amount < 0:

        messagebox.showerror(
            "Over Budget",
            "You are over budget!\nExpense cannot be added."
        )

        warning_label.config(
            text="⚠ You Are Over Budget!",
            fg="red"
        )

        return

    # ================= ADD RECORD =================

    records.append(("Expense", category, amount))

    tree.insert("", END, values=("Expense", category, amount))

    balance -= amount

    # ================= ZERO BALANCE WARNING =================

    if balance == 0:

        messagebox.showwarning(
            "Warning",
            "Balance is 0.\nYou are over budget!"
        )

        warning_label.config(
            text="⚠ Balance is 0 - You Are Over Budget!",
            fg="red"
        )

    else:

        warning_label.config(text="")

    update_balance()

    update_dashboard()

    refresh_dashboard_table()

    save_data()

    amount_entry.delete(0, END)

# ================= PDF =================

def generate_pdf():

    pdf = canvas.Canvas("Expense_Report.pdf")

    pdf.setFont("Helvetica-Bold", 20)

    pdf.drawString(180, 800, "FinASM Expense Report")

    y = 740

    for rec in records:

        text = f"{rec[0]} | {rec[1]} | Rs {rec[2]}"

        pdf.drawString(80, y, text)

        y -= 25

    pdf.drawString(80, y - 30, f"Final Balance: Rs {balance}")

    pdf.save()

    messagebox.showinfo("Success", "PDF Generated Successfully")

# ================= DASHBOARD =================

def show_dashboard():

    input_panel.pack_forget()

    refresh_dashboard_table()

    dashboard_panel.pack(fill=BOTH, expand=True)

def back_to_input():

    dashboard_panel.pack_forget()

    input_panel.pack(fill=BOTH, expand=True)

def update_dashboard():

    total_income = 0
    total_expense = 0

    for rec in records:

        if rec[0] == "Income":
            total_income += rec[2]
        else:
            total_expense += rec[2]

    savings = total_income - total_expense

    income_value.config(text=f"Rs {total_income}")

    expense_value.config(text=f"Rs {total_expense}")

    savings_value.config(text=f"Rs {savings}")

    show_pie_chart()

# ================= PIE CHART =================

def show_pie_chart():

    expense_data = {}

    for rec in records:

        if rec[0] == "Expense":

            category = rec[1]
            amount = rec[2]

            if category in expense_data:
                expense_data[category] += amount
            else:
                expense_data[category] = amount

    # REMOVE OLD CHART
    for widget in chart_frame.winfo_children():
        widget.destroy()

    if len(expense_data) == 0:
        return

    labels = list(expense_data.keys())

    amounts = list(expense_data.values())

    colors = [
        "#ff6666",
        "#3399ff",
        "#ffcc4d",
        "#4dd2cc",
        "#9966ff",
        "#66ff99",
        "#ff99cc",
        "#ff5e5e"
    ]

    explode = [0.02] * len(amounts)

    fig, ax = plt.subplots(figsize=(9, 5))

    # MODE COLORS
    if current_mode == "dark":

        bg_color = "#000000"

        text_color = "white"

    else:

        bg_color = "white"

        text_color = "black"

    fig.patch.set_facecolor(bg_color)

    ax.set_facecolor(bg_color)

    # ================= SHOW ALL PERCENTAGES =================

    def format_pct(pct):
        return f"{pct:.1f}%"

    wedges, texts, autotexts = ax.pie(
        amounts,
        colors=colors,
        explode=explode,
        startangle=90,
        autopct=format_pct,
        pctdistance=0.82,
        labeldistance=1.08,
        textprops={
            'color': text_color,
            'fontsize': 11,
            'weight': 'bold'
        }
    )

    # ================= TEXT COLORS =================

    for text in texts:
        text.set_color(text_color)

    for autotext in autotexts:
        autotext.set_color(text_color)

    # ================= TITLE =================

    ax.set_title(
        "Expense Breakdown (Pie Chart)",
        fontsize=18,
        fontweight="bold",
        color=text_color,
        pad=20
    )

    # ================= LEGEND =================

    legend = ax.legend(
        wedges,
        labels,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1.0, 0.5),
        fontsize=11,
        frameon=False
    )

    legend.get_title().set_color(text_color)

    for text in legend.get_texts():
        text.set_color(text_color)

    ax.axis('equal')

    plt.subplots_adjust(
        left=0.05,
        right=0.78,
        top=0.90,
        bottom=0.05
    )

    chart = FigureCanvasTkAgg(fig, chart_frame)

    chart.draw()

    chart.get_tk_widget().pack(fill=BOTH, expand=True)

# ================= TITLE =================

title = Label(
    root,
    text="FinASM Expense Tracker",
    font=("Arial", 24, "bold"),
    bg="#1e1e1e",
    fg="white"
)

title.pack(pady=10)

# =====================================================
# INPUT PANEL
# =====================================================

input_panel = Frame(root, bg="#1e1e1e")

input_panel.pack(fill=BOTH, expand=True)

# ================= LEFT PANEL =================

left_panel = Frame(input_panel, bg="#2d2d2d", width=250)

left_panel.pack(side=LEFT, fill=Y)

# ================= RIGHT PANEL =================

right_panel = Frame(input_panel, bg="#1e1e1e")

right_panel.pack(side=RIGHT, fill=BOTH, expand=True)

# ================= TABLE =================

columns = ("Type", "Category", "Amount")

tree = ttk.Treeview(
    right_panel,
    columns=columns,
    show="headings",
    height=16
)

for col in columns:

    tree.heading(col, text=col)

    tree.column(col, width=180, anchor=CENTER)

tree.pack(pady=20)

# ================= BALANCE =================

balance_label = Label(
    right_panel,
    text="Balance: Rs 0",
    font=("Arial", 18, "bold"),
    bg="#1e1e1e",
    fg="lightgreen"
)

balance_label.pack()

# ================= WARNING LABEL =================

warning_label = Label(
    right_panel,
    text="",
    font=("Arial", 14, "bold"),
    bg="#1e1e1e",
    fg="red"
)

warning_label.pack(pady=10)

# ================= CATEGORY =================

category_label = Label(
    left_panel,
    text="Category",
    font=("Arial", 12),
    bg="#2d2d2d",
    fg="white"
)

category_label.pack(pady=10)

categories = [

    "Salary",
    "Business",
    "Rental Income",
    "Government Benefits",
    "Commissions",
    "Other Income",

    "Food",
    "Savings",
    "Transport",
    "Medical",
    "Home Insurance",
    "Personal & Family",
    "Entertainment",
    "Other Expense"
]

category_box = ttk.Combobox(
    left_panel,
    values=categories,
    width=25
)

category_box.pack(pady=5)

# ================= AMOUNT =================

amount_label = Label(
    left_panel,
    text="Amount",
    font=("Arial", 12),
    bg="#2d2d2d",
    fg="white"
)

amount_label.pack(pady=10)

amount_entry = Entry(left_panel, font=("Arial", 12))

amount_entry.pack(pady=5)

# ================= BUTTONS =================

Button(
    left_panel,
    text="Add Income",
    command=add_income,
    bg="green",
    fg="white",
    width=20,
    height=2
).pack(pady=8)

Button(
    left_panel,
    text="Add Expense",
    command=add_expense,
    bg="red",
    fg="white",
    width=20,
    height=2
).pack(pady=8)

Button(
    left_panel,
    text="Delete Selected Record",
    command=delete_record,
    bg="darkred",
    fg="white",
    width=20,
    height=2
).pack(pady=8)

Button(
    left_panel,
    text="Result Dashboard",
    command=show_dashboard,
    bg="orange",
    fg="white",
    width=20,
    height=2
).pack(pady=8)

Button(
    left_panel,
    text="Light Mode",
    command=lambda: set_mode("light"),
    bg="white",
    fg="black",
    width=20,
    height=2
).pack(pady=8)

Button(
    left_panel,
    text="Dark Mode",
    command=lambda: set_mode("dark"),
    bg="black",
    fg="white",
    width=20,
    height=2
).pack(pady=8)


# DASHBOARD PANEL


dashboard_panel = Frame(root, bg="#000000")

dashboard_panel.pack_propagate(False)

# ================= TOP BOXES =================

top_frame = Frame(dashboard_panel, bg="#000000")

top_frame.pack(pady=10)

# ================= INCOME BOX =================

income_box = Frame(top_frame, bg="#d4edda", bd=2, relief=RIDGE)

income_box.grid(row=0, column=0, padx=20)

Label(
    income_box,
    text="Total Income",
    font=("Arial", 18, "bold"),
    bg="#d4edda",
    fg="green"
).pack(padx=60, pady=10)

income_value = Label(
    income_box,
    text="Rs 0",
    font=("Arial", 24, "bold"),
    bg="#d4edda",
    fg="green"
)

income_value.pack(pady=20)

# ================= EXPENSE BOX =================

expense_box = Frame(top_frame, bg="#f8d7da", bd=2, relief=RIDGE)

expense_box.grid(row=0, column=1, padx=20)

Label(
    expense_box,
    text="Total Expense",
    font=("Arial", 18, "bold"),
    bg="#f8d7da",
    fg="red"
).pack(padx=60, pady=10)

expense_value = Label(
    expense_box,
    text="Rs 0",
    font=("Arial", 24, "bold"),
    bg="#f8d7da",
    fg="red"
)

expense_value.pack(pady=20)

# ================= SAVINGS BOX =================

savings_box = Frame(top_frame, bg="#d1ecf1", bd=2, relief=RIDGE)

savings_box.grid(row=0, column=2, padx=20)

Label(
    savings_box,
    text="Total Savings",
    font=("Arial", 18, "bold"),
    bg="#d1ecf1",
    fg="blue"
).pack(padx=60, pady=10)

savings_value = Label(
    savings_box,
    text="Rs 0",
    font=("Arial", 24, "bold"),
    bg="#d1ecf1",
    fg="blue"
)

savings_value.pack(pady=20)


# TABLE + PIE CHART

middle_frame = Frame(dashboard_panel, bg="#000000")

middle_frame.pack(fill=BOTH, expand=True, pady=10)

middle_frame.columnconfigure(0, weight=1)

middle_frame.columnconfigure(1, weight=1)

# ================= TABLE FRAME =================

table_frame = Frame(middle_frame, bg="#000000")

table_frame.grid(row=0, column=0, padx=20, sticky="n")

# ================= RECORD TABLE =================

dashboard_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=15
)

for col in columns:

    dashboard_table.heading(col, text=col)

    dashboard_table.column(col, width=170, anchor=CENTER)

dashboard_table.pack()

# ================= PIE CHART FRAME =================

chart_frame = Frame(middle_frame, bg="#000000")

chart_frame.grid(row=0, column=1, padx=20, sticky="n")

# ================= REFRESH FUNCTION =================

def refresh_dashboard_table():

    for item in dashboard_table.get_children():
        dashboard_table.delete(item)

    for rec in records:
        dashboard_table.insert("", END, values=rec)

    show_pie_chart()

# BOTTOM BUTTON FRAME

bottom_frame = Frame(dashboard_panel, bg="#000000")

bottom_frame.pack(side=TOP, pady=10)

Button(
    bottom_frame,
    text="Refresh Records",
    command=refresh_dashboard_table,
    bg="purple",
    fg="white",
    width=18,
    height=2
).grid(row=0, column=0, padx=10)

Button(
    bottom_frame,
    text="Generate PDF",
    command=generate_pdf,
    bg="blue",
    fg="white",
    width=18,
    height=2
).grid(row=0, column=1, padx=10)

Button(
    bottom_frame,
    text="Back",
    command=back_to_input,
    bg="orange",
    fg="white",
    width=18,
    height=2
).grid(row=0, column=2, padx=10)

Button(
    bottom_frame,
    text="Exit",
    command=root.quit,
    bg="gray",
    fg="white",
    width=18,
    height=2
).grid(row=0, column=3, padx=10)

# ================= RUN =================

root.mainloop()