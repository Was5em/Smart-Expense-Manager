import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta

class ExpenseManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 مدير المصروفات الذكي")
        self.root.geometry("800x600")
        self.root.configure(bg="#8B5CF6")

        # Data
        self.expenses = []
        self.debts = []
        self.monthly_budget = 5000.0
        self.load_data()

        # UI Elements
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tabs
        self.add_expense_tab = ttk.Frame(self.notebook)
        self.add_debt_tab = ttk.Frame(self.notebook)
        self.reports_tab = ttk.Frame(self.notebook)
        self.budget_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.add_expense_tab, text="💰 إضافة مصروف")
        self.notebook.add(self.add_debt_tab, text="📝 إضافة دين")
        self.notebook.add(self.reports_tab, text="📊 التقارير")
        self.notebook.add(self.budget_tab, text="💵 الميزانية")

        self.setup_add_expense()
        self.setup_add_debt()
        self.setup_reports()
        self.setup_budget()

    def load_data(self):
        try:
            if os.path.exists('expenses.json'):
                with open('expenses.json', 'r') as f:
                    self.expenses = json.load(f)
            if os.path.exists('debts.json'):
                with open('debts.json', 'r') as f:
                    self.debts = json.load(f)
            if os.path.exists('budget.json'):
                with open('budget.json', 'r') as f:
                    self.monthly_budget = json.load(f)
        except:
            pass

    def save_data(self):
        with open('expenses.json', 'w') as f:
            json.dump(self.expenses, f)
        with open('debts.json', 'w') as f:
            json.dump(self.debts, f)
        with open('budget.json', 'w') as f:
            json.dump(self.monthly_budget, f)

    def setup_add_expense(self):
        frame = ttk.Frame(self.add_expense_tab, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="المبلغ (جنيه):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.amount_entry = ttk.Entry(frame)
        self.amount_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="الفئة:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar(value="food")
        category_combo = ttk.Combobox(frame, textvariable=self.category_var, values=["food", "transport", "bills", "entertainment", "health", "other"])
        category_combo.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="الوصف:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.desc_entry = ttk.Entry(frame)
        self.desc_entry.grid(row=2, column=1, pady=5)

        ttk.Button(frame, text="✅ إضافة المصروف", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
            category = self.category_var.get()
            desc = self.desc_entry.get()
            expense = {
                "id": len(self.expenses),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "amount": amount,
                "category": category,
                "description": desc
            }
            self.expenses.append(expense)
            self.save_data()
            messagebox.showinfo("نجح", f"تم إضافة {amount} جنيه")
            self.amount_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
        except:
            messagebox.showerror("خطأ", "أدخل مبلغ صحيح")

    def setup_add_debt(self):
        frame = ttk.Frame(self.add_debt_tab, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="المبلغ (جنيه):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.debt_amount_entry = ttk.Entry(frame)
        self.debt_amount_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="الاسم:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.debt_name_entry = ttk.Entry(frame)
        self.debt_name_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="تاريخ الاستحقاق:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.debt_date_entry = ttk.Entry(frame)
        self.debt_date_entry.grid(row=2, column=1, pady=5)

        ttk.Button(frame, text="✅ إضافة الدين", command=self.add_debt).grid(row=3, column=0, columnspan=2, pady=10)

    def add_debt(self):
        try:
            amount = float(self.debt_amount_entry.get())
            name = self.debt_name_entry.get()
            date = self.debt_date_entry.get()
            if amount <= 0 or not name or not date:
                raise ValueError
            debt = {
                "id": len(self.debts),
                "name": name,
                "amount": amount,
                "dueDate": date,
                "paid": False
            }
            self.debts.append(debt)
            self.save_data()
            messagebox.showinfo("نجح", f"تم إضافة دين: {name}")
            self.debt_amount_entry.delete(0, tk.END)
            self.debt_name_entry.delete(0, tk.END)
            self.debt_date_entry.delete(0, tk.END)
        except:
            messagebox.showerror("خطأ", "أدخل البيانات الصحيحة")

    def setup_reports(self):
        frame = ttk.Frame(self.reports_tab, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        self.reports_text = tk.Text(frame, wrap=tk.WORD, height=20)
        self.reports_text.pack(fill=tk.BOTH, expand=True)
        ttk.Button(frame, text="🔄 تحديث التقارير", command=self.update_reports).pack(pady=10)
        self.update_reports()

    def update_reports(self):
        self.reports_text.delete(1.0, tk.END)
        current_month = datetime.now().strftime("%Y-%m")
        month_expenses = [e for e in self.expenses if e["date"].startswith(current_month)]
        total = sum(e["amount"] for e in month_expenses)
        self.reports_text.insert(tk.END, f"📅 التقرير الشهري: {datetime.now().strftime('%B %Y')}\n\n")
        for e in month_expenses:
            self.reports_text.insert(tk.END, f"{e['description'] or self.get_category_name(e['category'])}: {e['amount']:.2f} ج\n")
        self.reports_text.insert(tk.END, f"\nالإجمالي: {total:.2f} جنيه\n\n")

        # Category analysis
        categories = {}
        for e in month_expenses:
            categories[e["category"]] = categories.get(e["category"], 0) + e["amount"]
        self.reports_text.insert(tk.END, "📊 تحليل الفئات:\n")
        for cat, amt in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percent = (amt / total * 100) if total else 0
            self.reports_text.insert(tk.END, f"{self.get_category_name(cat)}: {amt:.2f} ج ({percent:.1f}%)\n")

        # Upcoming debts
        today = datetime.now().date()
        upcoming = []
        for d in self.debts:
            if not d["paid"]:
                due = datetime.strptime(d["dueDate"], "%Y-%m-%d").date()
                days_left = (due - today).days
                upcoming.append((d, days_left))
        upcoming.sort(key=lambda x: x[1])
        self.reports_text.insert(tk.END, "\n⏰ الديون القادمة:\n")
        for d, days in upcoming:
            status = "متأخر" if days < 0 else "مستحق اليوم" if days == 0 else f"{days} يوم متبقي"
            self.reports_text.insert(tk.END, f"{d['name']}: {d['amount']:.2f} ج - {status}\n")

    def get_category_name(self, cat):
        names = {"food": "طعام", "transport": "مواصلات", "bills": "فواتير", "entertainment": "ترفيه", "health": "صحة", "other": "أخرى"}
        return names.get(cat, cat)

    def setup_budget(self):
        frame = ttk.Frame(self.budget_tab, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        self.budget_text = tk.Text(frame, wrap=tk.WORD, height=10)
        self.budget_text.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="الميزانية الجديدة:").pack(pady=5)
        self.new_budget_entry = ttk.Entry(frame)
        self.new_budget_entry.pack(pady=5)
        ttk.Button(frame, text="✅ تحديث الميزانية", command=self.update_budget).pack(pady=10)

        self.update_budget_display()

    def update_budget_display(self):
        self.budget_text.delete(1.0, tk.END)
        current_month = datetime.now().strftime("%Y-%m")
        spent = sum(e["amount"] for e in self.expenses if e["date"].startswith(current_month))
        remaining = self.monthly_budget - spent
        percent = (spent / self.monthly_budget * 100) if self.monthly_budget else 0
        self.budget_text.insert(tk.END, f"الميزانية: {self.monthly_budget:.2f} جنيه\n")
        self.budget_text.insert(tk.END, f"المصروف: {spent:.2f} جنيه\n")
        self.budget_text.insert(tk.END, f"المتبقي: {remaining:.2f} جنيه\n")
        self.budget_text.insert(tk.END, f"نسبة الصرف: {percent:.1f}%\n")
        status = "🚨 تجاوزت الميزانية!" if percent >= 100 else "⚠️ تبقى أقل من 10%" if percent >= 90 else "⚡ تم صرف 70%" if percent >= 70 else "✅ بخير"
        self.budget_text.insert(tk.END, f"الحالة: {status}\n")

    def update_budget(self):
        try:
            new_budget = float(self.new_budget_entry.get())
            if new_budget <= 0:
                raise ValueError
            self.monthly_budget = new_budget
            self.save_data()
            self.update_budget_display()
            messagebox.showinfo("نجح", "تم تحديث الميزانية")
            self.new_budget_entry.delete(0, tk.END)
        except:
            messagebox.showerror("خطأ", "أدخل ميزانية صحيحة")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseManagerApp(root)
    root.mainloop()
