# MGC

Данное приложение анализирует загружаемый пользователем аудиофайл(.MP3 или .wav) и на основании его характеристик подбирает схожие по звучанию и жанру композиции из заранее подготовленного списка.
___
## WARNING
Перед работой удостоверьтесь, что у вас установлены следующие библиотеки языка python:
- tkinter
- pygame
- librosa
- sklearn
- numpy
- pandas
- pydub

Для корректной работы библиотеки pydub удостоверьтесь, что у вас установлен ffmpeg и он находится в PATH(системные переменные среды). Актуально для Windows.
___
## Описание работы программы
Для работы с приложением необходимо запустить код в файле main.py, после чего откроется рабочее окно приложения, в котором необходимо нажать на кнопку "Загрузить аудио-файл" и выбрать файл на компьютере. После загрузки будет предложено выбрать 30-секундный фрагмент, что можно сделать при помощи ползунка в новом окне. После выбора необходимого промежутка следует нажть на кнопку "Сохранить промежуток и открыть новое окно". Начнется его обработка, которая обычно занимает не больше 20-25 секунд. 
По прошествии этого времени результат обработки будет выведен в новом окне. Он включает в себя классифицированный жанр композиции, а также 3 наиболее похожих аудиофайла из датасета.
___
## Содержание репозитория
- в папке **Data** содержится датасет GZTAN, разделенный на 2 части, изначально состоящий из 10 жанров, в каждом из которых 100 аудиофайлов формата .wav:
  + **genres_85** содержит в себе 85% изначального датасета. Используется для обучения модели SVM, классифицирующей аудиофайлы по жанрам.
  + **genres_15** содержит в себе 15% изначального датасета. Используется как валидационный датасет, при помощи которого можно проверить корректность работы программы.
- **main.py** реализует простой визуальный интерейс.
- **calculate.py** приводит аудиозапись к формату .wav, обучает модель SVM, припомощи которой происходит классификация аудиозаписи и ищет похожие аудио из genres_85.
- **time.txt** содержит в себе временной промежуток аудиозаписи, выбранный пользователем.
- **similar.txt** содержит в себе метку класса и похожие аудиозаписи, полученные в calculate.py .
