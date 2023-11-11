import calendar
import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
import random
from tkcalendar import DateEntry

# Создание базы данных или подключение к существующей
conn = sqlite3.connect('financial_tracker.db')
cursor = conn.cursor()

# Создание таблицы для записи расходов и доходов
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        description TEXT,
        amount REAL,
        category TEXT,
        type TEXT,
        date DATE
    )
''')
conn.commit()

# Создаем глобальные переменные для вкладок
tab1 = None
tab2 = None
tab3 = None
tab4 = None
tab5 = None
tab6 = None


current_currency = "USD"

# Функция для добавления новой транзакции в базу данных
def add_transaction():

    description = description_entry.get()
    amount = amount_entry.get()
    category = category_entry.get()
    transaction_type = transaction_type_var.get()

    cursor.execute(
        "INSERT INTO transactions (description, amount, category, type, date) VALUES (?, ?, ?, ?, date('now'))",
        (description, amount, category, transaction_type))
    conn.commit()
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    show_transactions()

# Функция для отображения всех транзакций
def show_transactions():
    global current_currency  # Используйте глобальную переменную для текущей валюты
    for widget in tab1.winfo_children():
        widget.destroy()

    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()

    total_budget = calculate_total_budget()

    # Очищаем содержимое текущей вкладки
    for widget in tab1.winfo_children():
        widget.destroy()

    # Отображаем общий бюджет
    total_budget_label = tk.Label(tab1, text=f"Общий бюджет: ${total_budget:.2f}")
    total_budget_label.pack()

    if transactions:
        result_text = tk.Text(tab1, height=10, width=50)
        result_text.config(state=tk.NORMAL)
        result_text.pack()
        for transaction in transactions:
            amount = transaction[2]
            transaction_id = transaction[0]

            if isinstance(amount, (int, float)):
                if current_currency == "USD":
                    formatted_amount = f"${amount:.2f}"
                elif current_currency == "BYN":
                    # Пересчитайте в BYN согласно вашему курсу
                    formatted_amount = f"{amount * 3.4} BYN"
                elif current_currency == "RUB":
                    # Пересчитайте в RUB согласно вашему курсу
                    formatted_amount = f"{amount / 100} RUB"
                elif current_currency == "EUR":
                    # Пересчитайте в EUR согласно вашему курсу
                    formatted_amount = f"{amount} EUR"
            else:
                formatted_amount = str(amount)

            result_text.insert(tk.END,
                               f"ID: {transaction_id} - {transaction[5]} - {transaction[3]} - {transaction[1]} - {transaction[4]} - {formatted_amount}\n")
        result_text.config(state=tk.DISABLED)
    else:
        no_data_label = tk.Label(tab1, text="Нет данных о транзакциях")
        no_data_label.pack()

# Функция для добавления новой транзакции в базу данных
def add_income():
    description = income_description_entry.get()
    amount = income_amount_entry.get()
    category = income_category_entry.get()
    transaction_type = "Доход"  # Указываем тип "Доход"

    cursor.execute(
        "INSERT INTO transactions (description, amount, category, type, date) VALUES (?, ?, ?, ?, date('now'))",
        (description, amount, category, transaction_type))
    conn.commit()
    income_description_entry.delete(0, tk.END)
    income_amount_entry.delete(0, tk.END)
    income_category_entry.delete(0, tk.END)

# Функция для отображения всех доходов

def show_expenses_chart(start_date, end_date):
    for widget in tab3.winfo_children():
        widget.destroy()

    cursor.execute("SELECT category, amount, type FROM transactions WHERE date BETWEEN ? AND ?",
                   (start_date, end_date))
    transactions = cursor.fetchall()

    if transactions:
        labels = []
        amounts = []
        income = 0
        expenses = 0

        for transaction in transactions:
            category = transaction[0]
            amount = transaction[1]
            transaction_type = transaction[2]

            labels.append(category)
            amounts.append(amount)

            if transaction_type == 'Доход':
                income += amount
            elif transaction_type == 'Расход':
                expenses += amount

        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Задаем цвета

        fig, ax = plt.subplots()
        ax.pie(amounts, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
        ax.set_title('Диаграмма доходов и расходов')

        # Сохраняем диаграмму в файл
        plt.savefig('expense_pie.png')

        img = tk.PhotoImage(file='expense_pie.png')
        img_label = tk.Label(tab3, image=img)
        img_label.image = img
        img_label.pack(side='top')

        # Выводим точную информацию о доходах и расходах
        info_label = tk.Label(tab3, text=f'Доходы: ${income:.2f}\nРасходы: ${expenses:.2f}', anchor='se')
        info_label.pack(side='right', padx=10, pady=10)
    else:
        no_data_label = tk.Label(tab3, text="Нет данных о транзакциях")
        no_data_label.pack()



def calculate_total_budget():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Доход'")
    total_income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Расход'")
    total_expenses = cursor.fetchone()[0] or 0

    total_budget = total_income - total_expenses
    return total_budget


def convert_currency(amount, from_currency, to_currency):
    # Укажите коэффициенты пересчета для выбранных валют
    currency_rates = {
        ('USD', 'BYN'): 3.4,
        ('RUB', 'USD'): 0.01,
        ('EUR', 'USD'): 1.0,
        # Добавьте другие валюты и их коэффициенты пересчета
    }

    if (from_currency, to_currency) in currency_rates:
        conversion_rate = currency_rates[(from_currency, to_currency)]
    else:
        return None  # Валюты для пересчета не найдены

    converted_amount = amount * conversion_rate
    return converted_amount


# Функция для поиска транзакции по ID
def search_transaction_by_id():
    try:
        transaction_id = int(search_id_entry.get())
        cursor.execute("SELECT * FROM transactions WHERE id=?", (transaction_id,))
        transaction = cursor.fetchone()

        if transaction:
            result_text = tk.Text(tab4, height=10, width=50)
            result_text.config(state=tk.NORMAL)
            result_text.pack()
            result_text.insert(tk.END,
                               f"{transaction[5]} - {transaction[3]} - {transaction[1]} - {transaction[4]} - ${transaction[2]:.2f}\n")
            result_text.config(state=tk.DISABLED)
        else:
            no_data_label = tk.Label(tab4, text="Транзакция с указанным ID не найдена")
            no_data_label.pack()
    except ValueError:
        pass

# Функция для удаления транзакции по ID
def delete_transaction_by_id():
    try:
        transaction_id = int(delete_id_entry.get())
        cursor.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
        conn.commit()
        delete_id_entry.delete(0, tk.END)
        show_transactions()
    except ValueError:
        pass


def show_transactions_for_date(event):
    print("show_transactions_for_date called")
    selected_date = calendar_widget.get_date()

    # Соединение с базой данных
    conn = sqlite3.connect('financial_tracker.db')
    cursor = conn.cursor()

    # Запрос для получения информации о доходах и расходах за весь день
    cursor.execute("SELECT * FROM transactions WHERE date LIKE ?", (f"{selected_date}%",))
    transactions = cursor.fetchall()

    income = 0
    expenses = 0
    for transaction in transactions:
        if transaction[4] == 'Доход':
            income += transaction[2]
        elif transaction[4] == 'Расход':
            expenses += transaction[2]

    popup_text = f"Дата: {selected_date}\nДоходы: {income}\nРасходы: {expenses}"

    if transactions:
        # Отобразите информацию во всплывающей подсказке
        tooltip = tk.Toplevel(tab6)
        tooltip.wm_geometry("+%d+%d" % (root.winfo_pointerx() + 10, root.winfo_pointery() + 10))
        label = tk.Label(tooltip, text=popup_text)
        label.pack()
        tooltip.after(3000, tooltip.destroy)  # Закрыть всплывающую подсказку через 3 секунды
    else:
        popup_text = f"На {selected_date} нет данных о транзакциях"
        print(popup_text)



def change_currency(new_currency):
    global current_currency
    current_currency = new_currency
    show_transactions()  # Обновите отображение данных
    # Другие обновления для ваших вкладок, если необходимо

# Функция для переключения на вкладку с расходами
def switch_to_expenses():
    notebook.select(tab1)

# Функция для переключения на вкладку с доходами
def switch_to_income():
    notebook.select(tab2)

# Создание GUI
root = tk.Tk()
root.title("Система учета финансов")
root.geometry("850x620")


# Создаем тему оформления
style = ttk.Style()
style.configure('TFrame', background='light blue')
style.configure('TButton', background='light green')
style.configure('TLabel', background='light blue')
style.configure('TText', background='white')

# Создаем фрейм с полосами прокрутки для вкладок

canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

content = ttk.Frame(canvas)
canvas.create_window((0, 0), window=content, anchor=tk.NW)

# Создаем вкладки
notebook = ttk.Notebook(content)
notebook.pack()

tab1 = ttk.Frame(notebook)
tab1_width = 80000  # Ширина вкладки
tab1_height = 3000  # Высота вкладки
notebook.add(tab1, text="Все транзакции и общий бюджет")

tab2 = ttk.Frame(notebook)
tab2_width = 80000  # Ширина вкладки
tab2_height = 3000  # Высота вкладки
notebook.add(tab2, text="Добавить доходы и расходы")

tab3 = ttk.Frame(notebook)
tab3_width = 80000  # Ширина вкладки
tab3_height = 3000  # Высота вкладки
notebook.add(tab3, text="Диаграмма")

tab4 = ttk.Frame(notebook)
tab4_width = 80000  # Ширина вкладки
tab4_height = 3000  # Высота вкладки
notebook.add(tab4, text="Поиск и удаление транзакции по ID")

tab5 = ttk.Frame(notebook)
tab5_width = 80000  # Ширина вкладки
tab5_height = 3000  # Высота вкладки
notebook.add(tab5, text="Обмен валют")

tab6 = ttk.Frame(notebook)
notebook.add(tab6, text="Календарь")
tab6_width = 80000  # Ширина вкладки
tab6_height = 3000  # Высота вкладки
notebook.select(tab6)

# Вкладка для добавления расхода
description_label = tk.Label(tab2, text="Описание:")
description_label.pack()
description_entry = tk.Entry(tab2)
description_entry.pack()
amount_label = tk.Label(tab2, text="Сумма:")
amount_label.pack()
amount_entry = tk.Entry(tab2)
amount_entry.pack()
category_label = tk.Label(tab2, text="Категория:")
category_label.pack()
category_entry = tk.Entry(tab2)
category_entry.pack()

transaction_type_var = tk.StringVar()
transaction_type_var.set("Расход")
transaction_type_label = tk.Label(tab2, text="Тип транзакции:")
transaction_type_label.pack()
transaction_type_menu = tk.OptionMenu(tab2, transaction_type_var, "Расход", "Доход")
transaction_type_menu.pack()

add_button = tk.Button(tab2, text="Добавить расход", command=add_transaction)
add_button.pack()

# Вкладка для добавления дохода
income_description_entry = tk.Entry(tab2)
income_amount_entry = tk.Entry(tab2)
income_category_entry = tk.Entry(tab2)
add_income_button = tk.Entry(tab2)



# Вкладка для отображения диаграммы расходов
show_expenses_chart_button = tk.Button(tab3, text="Показать диаграмму расходов", command=show_expenses_chart)
show_expenses_chart_button.pack()

# Вкладка для переключения на вкладку с расходами
switch_to_expenses_button = tk.Button(tab1, text="Перейти к расходам", command=switch_to_expenses)
switch_to_expenses_button.pack()

# Вкладка для переключения на вкладку с доходами
switch_to_income_button = tk.Button(tab1, text="Перейти к доходам", command=switch_to_income)
switch_to_income_button.pack()

# Вкладка для поиска транзакции по ID
search_id_label = tk.Label(tab4, text="ID для поиска:")
search_id_label.pack()
search_id_entry = tk.Entry(tab4)
search_id_entry.pack()
search_button = tk.Button(tab4, text="Найти транзакцию по ID", command=search_transaction_by_id)
search_button.pack()

# Вкладка для удаления транзакции по ID
delete_id_label = tk.Label(tab4, text="ID для удаления:")
delete_id_label.pack()
delete_id_entry = tk.Entry(tab4)
delete_id_entry.pack()
delete_button = tk.Button(tab4, text="Удалить транзакцию по ID", command=delete_transaction_by_id)
delete_button.pack()


currency_label = tk.Label(tab5, text="Выберите валюту:")


change_currency_label = tk.Label(tab5, text="Изменить валюту:")
currency_var = tk.StringVar()
currency_var.set("USD")  # Устанавливаем USD как валюту по умолчанию

usd_button = tk.Radiobutton(tab5, text="USD", variable=currency_var, value="USD", command=lambda: change_currency("USD"))
usd_button.pack()

byn_button = tk.Radiobutton(tab5, text="BYN", variable=currency_var, value="BYN", command=lambda: change_currency("BYN"))
byn_button.pack()

rub_button = tk.Radiobutton(tab5, text="RUB", variable=currency_var, value="RUB", command=lambda: change_currency("RUB"))
rub_button.pack()

eur_button = tk.Radiobutton(tab5, text="EUR", variable=currency_var, value="EUR", command=lambda: change_currency("EUR"))
eur_button.pack()
update_currency_button = tk.Button(tab5, text="Применить валюту и пересчитать", command=show_transactions)
update_currency_button.pack()

# Создайте Calendar виджет
calendar_widget = DateEntry(tab6)
calendar_widget.pack(padx=10, pady=10)

# Привяжите функцию к событию выбора даты
calendar_widget.bind("<<DateEntrySelected>>", show_transactions_for_date)


# Запуск отображения всех транзакций при запуске программы
# Определение start_date и end_date
from datetime import date, timedelta

end_date = date.today()
start_date = end_date - timedelta(days=30)  # Например, за последний месяц

# Вызов функций
show_transactions()
show_expenses_chart(start_date, end_date)

root.mainloop()




