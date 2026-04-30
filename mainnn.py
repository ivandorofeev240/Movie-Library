import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

#Название файла для сохранения данных
JSON_FILE = 'movies.json'

# Загрузка данных из файла
def load_movies():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Файл данных поврежден. Начинаем с пустого списка.")
            return []
    return []

# Сохранение данных в файл
def save_movies():
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

# Очистка полей ввода
def clear_inputs():
    entry_title.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_rating.delete(0, tk.END)

# Обновление таблицы
def update_table(filtered_list=None):
    for item in tree.get_children():
        tree.delete(item)
    display_list = filtered_list if filtered_list is not None else movies
    for m in display_list:
        tree.insert('', 'end', values=(m['name'], m['genre'], m['year'], m['rating']))

# Добавление нового фильма
def add_movie():
    name = entry_title.get().strip()
    genre = entry_genre.get().strip()
    year_str = entry_year.get().strip()
    rating_str = entry_rating.get().strip()

    # Проверки
    if not name or not genre or not year_str or not rating_str:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
        return

    if not year_str.isdigit():
        messagebox.showerror("Ошибка", "Год должен быть числом.")
        return

    try:
        rating_value = float(rating_str)
        if not (0 <= rating_value <= 10):
            messagebox.showerror("Ошибка", "Рейтинг должен быть в диапазоне 0-10.")
            return
    except ValueError:
        messagebox.showerror("Ошибка", "Рейтинг должен быть числом.")
        return

    movie = {
        "name": name,
        "genre": genre,
        "year": int(year_str),
        "rating": rating_value
    }
    movies.append(movie)
    update_table()
    save_movies()
    clear_inputs()

# Фильтрация по жанру и году
def filter_movies():
    genre_filter = entry_filter_genre.get().strip().lower()
    year_filter = entry_filter_year.get().strip()

    filtered = movies
    if genre_filter:
        filtered = [m for m in filtered if genre_filter in m['genre'].lower()]
    if year_filter:
        if not year_filter.isdigit():
            messagebox.showerror("Ошибка", "Фильтр по году должен быть числом.")
            return
        filtered = [m for m in filtered if m['year'] == int(year_filter)]
    update_table(filtered)

# Создаем основное окно
root = tk.Tk()
root.title("Movie Library")
root.geometry("700x600")
root.resizable(False, False)

# Загружаем данные из файла
movies = load_movies()

# Ввод данных о фильме
tk.Label(root, text="Название").grid(row=0, column=0, padx=5, pady=5, sticky='w')
entry_title = tk.Entry(root, width=30)
entry_title.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Жанр").grid(row=1, column=0, padx=5, pady=5, sticky='w')
entry_genre = tk.Entry(root, width=30)
entry_genre.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Год выпуска").grid(row=2, column=0, padx=5, pady=5, sticky='w')
entry_year = tk.Entry(root, width=30)
entry_year.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Рейтинг").grid(row=3, column=0, padx=5, pady=5, sticky='w')
entry_rating = tk.Entry(root, width=30)
entry_rating.grid(row=3, column=1, padx=5, pady=5)

# Кнопка добавить фильм
btn_add = tk.Button(root, text="Добавить фильм", command=add_movie)
btn_add.grid(row=4, column=0, columnspan=2, pady=10)

# Таблица для отображения фильмов
columns = ('Название', 'Жанр', 'Год', 'Рейтинг')
tree = ttk.Treeview(root, columns=columns, show='headings', height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor='center')
tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Фильтрация
tk.Label(root, text="Фильтр по жанру").grid(row=6, column=0, padx=5, pady=5, sticky='w')
entry_filter_genre = tk.Entry(root, width=20)
entry_filter_genre.grid(row=6, column=1, padx=5, pady=5, sticky='w')

tk.Label(root, text="Фильтр по году").grid(row=7, column=0, padx=5, pady=5, sticky='w')
entry_filter_year = tk.Entry(root, width=20)
entry_filter_year.grid(row=7, column=1, padx=5, pady=5, sticky='w')

btn_filter = tk.Button(root, text="Фильтровать", command=filter_movies)
btn_filter.grid(row=8, column=0, padx=5, pady=10, sticky='w')

btn_reset = tk.Button(root, text="Сбросить фильтр", command=lambda: update_table())
btn_reset.grid(row=8, column=1, padx=5, pady=10, sticky='w')

# Изначально отображаем все фильмы
update_table()

# Запуск главного цикла
root.mainloop()
