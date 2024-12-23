import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from pygame import mixer
import threading
import time
import calculate




# Очистка папки upload перед загрузкой
def clear_upload_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)

# Функция загрузки аудиофайла
def load_audio_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
    
    if file_path:
        upload_dir = os.path.join(os.getcwd(), "upload")
        clear_upload_folder(upload_dir)
        
        file_name = os.path.basename(file_path)
        destination = os.path.join(upload_dir, file_name)
        try:
            shutil.copy(file_path, destination)
            messagebox.showinfo("Успешно", f"Файл загружен:\n{destination}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{str(e)}")
        
        open_audio_player(destination)
    else:
        messagebox.showwarning("Файл не выбран", "Вы не выбрали файл.")

# Открытие окна проигрывателя с ползунком
def open_audio_player(audio_path):
    player_window = tk.Toplevel()
    player_window.title("Аудио-проигрыватель")
    player_window.geometry("600x400")

    mixer.init()

    track_length = None
    start_time = tk.IntVar(value=0)

    def update_track_length():
        nonlocal track_length
        try:
            mixer.music.load(audio_path)
            mixer.music.play(loops=0)  
            time.sleep(0.5)  
            track_length = mixer.Sound(audio_path).get_length()
            mixer.music.stop()
            slider.config(to=int(track_length - 30))  
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось определить длину файла:\n{e}")

    def play_audio():
        mixer.music.load(audio_path)
        mixer.music.play()

    def stop_audio():
        mixer.music.stop()

    # Воспроизведение 30-секундного отрывка
    def play_audio_segment():
        start = slider.get()  
        mixer.music.load(audio_path)
        mixer.music.play(start=start)
        
        def stop_after_30_seconds():
            time.sleep(30)
            mixer.music.stop()

        threading.Thread(target=stop_after_30_seconds, daemon=True).start()

    # Сохранение промежутка и открытие нового окна
    def save_segment_and_open_new_window():
        start = slider.get()
        end = start + 30

        try:
            with open("time.txt", "w") as file:
                file.write(str(start))
                file.write('\n')
                file.write(str(end))
            messagebox.showinfo("Успешно", f"Промежуток сохранен в time.txt (Start: {start}, End: {end})")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось записать в файл:\n{e}")
        
        # Закрываем текущее окно проигрывателя
        player_window.destroy()
        calculate.calc_function()
        # Открываем новое окно
        open_new_window()






    def open_new_window():
        new_window = tk.Toplevel()
        new_window.title("Новое окно")
        new_window.geometry("800x600")
        mixer.init()  # Инициализация pygame mixer

        # Чтение данных из файла
        audio_data = {}
        with open('similar.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            genre = lines[0].strip()  # Первая строка - жанр
            for i in range(1, len(lines), 2):
                audio_name = lines[i].strip()
                audio_number = lines[i + 1].strip()
                audio_data[audio_name] = audio_number

        # Вывод жанра
        tk.Label(new_window, text=f"Жанр: {genre}", font=("Arial", 14)).pack(pady=10)

        # Создание проигрывателей и описаний для каждого аудиофайла
        for audio_name, audio_number in audio_data.items():
            # Создаём новый фрейм для каждого аудиофайла
            audio_frame = tk.Frame(new_window)
            audio_frame.pack(pady=10)

            # Вывод имени аудиозаписи
            tk.Label(audio_frame, text=audio_name, font=("Arial", 12)).pack(side=tk.LEFT)

            # Добавляем кнопку для проигрывания аудио из файла
            audio_file_path = os.path.join(audio_name)  # Путь к аудиофайлу

            def play_audio(path=audio_file_path):  # Предотвращаем замыкание
                mixer.music.stop()  # Останавливаем текущую музыку
                mixer.music.load(path)
                mixer.music.play()

            play_button = tk.Button(audio_frame, text="Играть", command=play_audio, font=("Arial", 10))
            play_button.pack(side=tk.LEFT)

            # Добавляем кнопку для остановки аудио
            stop_button = tk.Button(audio_frame, text="Остановить", command=mixer.music.stop, font=("Arial", 10))
            stop_button.pack(side=tk.LEFT)

            # Выводим число
            tk.Label(audio_frame, text=audio_number, font=("Arial", 12)).pack(side=tk.LEFT)

        # Проигрыватель для аудиофайла из папки "upload"
        upload_audio_path = calculate.find_audio("upload/")  # Замените на имя вашего файла в папке "upload"
        upload_audio_name = upload_audio_path
    
        upload_frame = tk.Frame(new_window)
        upload_frame.pack(pady=10)
    
        tk.Label(upload_frame, text="Из папки 'upload':", font=("Arial", 14)).pack(side=tk.LEFT)
    
        tk.Label(upload_frame, text=upload_audio_name, font=("Arial", 12)).pack(side=tk.LEFT)
    
        def play_upload_audio():
            mixer.music.stop()
            mixer.music.load(upload_audio_path)
            mixer.music.play()
    
        upload_play_button = tk.Button(upload_frame, text="Играть", command=play_upload_audio, font=("Arial", 10))
        upload_play_button.pack(side=tk.LEFT)
    
        # Добавляем кнопку для остановки аудио из папки "upload"
        upload_stop_button = tk.Button(upload_frame, text="Остановить", command=mixer.music.stop, font=("Arial", 10))
        upload_stop_button.pack(side=tk.LEFT)
    
        # Добавляем кнопку, чтобы закрыть новое окно
        tk.Button(new_window, text="Закрыть", command=new_window.destroy, font=("Arial", 12)).pack(pady=20)







    # Интерфейс
    play_button = tk.Button(player_window, text="▶️ Воспроизвести весь трек", command=play_audio, font=("Arial", 12))
    play_button.pack(pady=10)
    
    stop_button = tk.Button(player_window, text="⏹️ Остановить", command=stop_audio, font=("Arial", 12))
    stop_button.pack(pady=10)
    tk.Label(player_window, text="Выберите начало отрывка (в секундах):", font=("Arial", 12)).pack(pady=5)
    slider = tk.Scale(player_window, from_=0, to=100, orient=tk.HORIZONTAL, variable=start_time, font=("Arial", 12), length=400)
    slider.pack(pady=20)

    play_segment_button = tk.Button(player_window, text="▶️ Воспроизвести 30 секунд", command=play_audio_segment, font=("Arial", 12))
    play_segment_button.pack(pady=10)

    save_button = tk.Button(player_window, text="💾 Сохранить промежуток и открыть новое окно", command=save_segment_and_open_new_window, font=("Arial", 12))
    save_button.pack(pady=20)

    def on_closing():
        stop_audio()
        player_window.destroy()

    player_window.protocol("WM_DELETE_WINDOW", on_closing)

    update_track_length()
    
# Основное окно приложения
def create_app():
    root = tk.Tk()
    root.title("Загрузка аудио-файла")
    root.geometry("400x200")

    tk.Button(root, text="Загрузить аудио-файл", command=load_audio_file, font=("Arial", 14)).pack(pady=50)

    root.mainloop()

if __name__ == "__main__":
    create_app()