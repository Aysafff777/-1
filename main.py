import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# --- 1. Список предопределённых цитат ---
QUOTES = [
    {"text": "Секрет успеха — постоянство цели.", "author": "Бенджамин Дизраэли", "topic": "Успех"},
    {"text": "Жизнь — это то, что происходит, пока ты строишь планы.", "author": "Джон Леннон", "topic": "Жизнь"},
    {"text": "Единственный способ делать великие дела — любить то, что ты делаешь.", "author": "Стив Джобс", "topic": "Работа"},
    {"text": "Не бойся, что не знаешь. Бойся, что не учишься.", "author": "Китайская пословица", "topic": "Обучение"},
    {"text": "Сила не в том, что ты можешь. Сила в преодолении того, чего когда-то боялся.", "author": "Риксон Грейси", "topic": "Сила духа"},
    {"text": "Величайшая слава не в том, чтобы никогда не ошибаться, а в том, чтобы уметь подняться каждый раз, когда падаешь.", "author": "Конфуций", "topic": "Ошибки"},
]

# --- 2. Управление историей ---
HISTORY_FILE = "history.json"

def load_history():
    """Загружает историю из файла JSON."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    """Сохраняет историю в файл JSON."""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# --- 3. Основная логика приложения ---
class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.root.geometry("600x500")

        self.history = load_history()

        # --- Виджеты ---
        # Текущая цитата
        self.quote_label = tk.Label(root, text="Нажмите кнопку для генерации цитаты", wraplength=450, font=('Arial', 12))
        self.quote_label.pack(pady=10)

        # Кнопка генерации
        self.generate_btn = tk.Button(root, text="Сгенерировать цитату", command=self.generate_quote)
        self.generate_btn.pack(pady=5)

        # Фильтры
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Автор:").grid(row=0, column=0, padx=5)
        self.author_entry = tk.Entry(filter_frame)
        self.author_entry.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Тема:").grid(row=0, column=2, padx=5)
        self.topic_entry = tk.Entry(filter_frame)
        self.topic_entry.grid(row=0, column=3, padx=5)

        self.filter_btn = tk.Button(filter_frame, text="Фильтровать историю", command=self.filter_history)
        self.filter_btn.grid(row=0, column=4, padx=5)

        # История (Listbox с полосой прокрутки)
        history_frame = tk.Frame(root)
        history_frame.pack(fill='both', expand=True, pady=10)

        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side='right', fill='y')

        self.history_listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set, height=12)
        self.history_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.history_listbox.yview)

        # Заполнение истории при старте
        self.update_history_display()

    def generate_quote(self):
        """Генерирует случайную цитату и добавляет её в историю."""
        quote = random.choice(QUOTES)
        
        # Проверка на дубликаты в истории (опционально, но полезно)
        if not any(q['text'] == quote['text'] and q['author'] == quote['author'] for q in self.history):
            self.history.append(quote)
            save_history(self.history) # Сохраняем сразу после добавления

        self.quote_label.config(text=f'"{quote["text"]}"\n— {quote["author"]}')
        
    def update_history_display(self, filtered_history=None):
        """Обновляет виджет Listbox с историей."""
        self.history_listbox.delete(0, tk.END) # Очищаем список

        # Используем отфильтрованную историю или полную
        history_to_show = filtered_history if filtered_history is not None else self.history

        for i, q in enumerate(history_to_show):
            entry = f'{i+1}. "{q["text"]}" — {q["author"]} ({q["topic"]})'
            self.history_listbox.insert(tk.END, entry)

    def filter_history(self):
        """Фильтрует историю по автору и теме."""
        author_filter = self.author_entry.get().strip()
        topic_filter = self.topic_entry.get().strip()
        
        filtered = []
        
        for q in self.history:
            author_match = (author_filter == "") or (author_filter.lower() in q["author"].lower())
            topic_match = (topic_filter == "") or (topic_filter.lower() in q["topic"].lower())
            
            if author_match and topic_match:
                filtered.append(q)
                
        if not filtered:
            messagebox.showinfo("Результат", "По вашему запросу ничего не найдено.")
        
        self.update_history_display(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()
    