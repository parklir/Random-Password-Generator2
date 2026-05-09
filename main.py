import json
import random
import string
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "password_history.json"


# Загрузка истории
def load_history():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Сохранение истории
def save_history():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")


# Генерация пароля
def generate_password():
    length = int(length_var.get())

    chars = ""
    if var_lower.get():
        chars += string.ascii_lowercase
    if var_upper.get():
        chars += string.ascii_uppercase
    if var_digits.get():
        chars += string.digits
    if var_symbols.get():
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if not chars:
        messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов")
        return

    password = "".join(random.choice(chars) for _ in range(length))
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)

    # Добавление в историю
    history.append({"password": password, "length": length})
    if len(history) > 50:
        history.pop(0)
    save_history()
    update_table()


# Обновление таблицы истории
def update_table():
    for row in table.get_children():
        table.delete(row)
    for record in history:
        table.insert("", tk.END, values=(record["password"], record["length"]))


# Копирование пароля в буфер обмена
def copy_to_clipboard():
    password = entry_password.get()
    if password:
        window.clipboard_clear()
        window.clipboard_append(password)
        messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")
    else:
        messagebox.showwarning("Ошибка", "Нет пароля для копирования")


# Очистка истории
def clear_history():
    if messagebox.askyesno("Подтверждение", "Очистить всю историю паролей?"):
        history.clear()
        save_history()
        update_table()


# Загрузка данных
history = load_history()

window = tk.Tk()
window.title("Random Password Generator")

# === Настройки ===
settings_frame = tk.LabelFrame(window, text="Настройки пароля", padx=10, pady=10)
settings_frame.pack(padx=10, pady=5, fill="x")

# Длина пароля
tk.Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, sticky="w")
length_var = tk.IntVar(value=12)
length_scale = tk.Scale(settings_frame, from_=4, to=32, orient="horizontal", variable=length_var)
length_scale.grid(row=0, column=1, padx=10)

# Чекбоксы
var_lower = tk.BooleanVar(value=True)
var_upper = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)

tk.Checkbutton(settings_frame, text="Строчные буквы (a-z)", variable=var_lower).grid(row=1, column=0, sticky="w")
tk.Checkbutton(settings_frame, text="Заглавные буквы (A-Z)", variable=var_upper).grid(row=2, column=0, sticky="w")
tk.Checkbutton(settings_frame, text="Цифры (0-9)", variable=var_digits).grid(row=3, column=0, sticky="w")
tk.Checkbutton(settings_frame, text="Спецсимволы (!@#$%^&*)", variable=var_symbols).grid(row=4, column=0, sticky="w")

# Кнопка генерации
tk.Button(settings_frame, text="Сгенерировать пароль", command=generate_password, bg="green", fg="white").grid(row=5,
                                                                                                               column=0,
                                                                                                               columnspan=2,
                                                                                                               pady=10)

# === Поле вывода пароля ===
password_frame = tk.LabelFrame(window, text="Ваш пароль", padx=10, pady=10)
password_frame.pack(padx=10, pady=5, fill="x")

entry_password = tk.Entry(password_frame, font=("Consolas", 14), width=40)
entry_password.pack(side=tk.LEFT, padx=5)

tk.Button(password_frame, text="Копировать", command=copy_to_clipboard, bg="blue", fg="white").pack(side=tk.LEFT,
                                                                                                    padx=5)

# === История паролей ===
history_frame = tk.LabelFrame(window, text="История паролей (последние 50)", padx=10, pady=10)
history_frame.pack(padx=10, pady=5, fill="both", expand=True)

columns = ("password", "length")
table = ttk.Treeview(history_frame, columns=columns, show="headings", height=10)
table.heading("password", text="Пароль")
table.heading("length", text="Длина")
table.column("password", width=300)
table.column("length", width=80)
table.pack(fill="both", expand=True)

tk.Button(history_frame, text="Очистить историю", command=clear_history, bg="red", fg="white").pack(pady=5)

update_table()
window.mainloop()