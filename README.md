# HDV_pipeline
Пайплайн для поиска и описания мутаций в геноме HDV

TODO:
1. Создать docker-образ:
  + Внутри образа создать необходимые директории
  + Установить зависимости
2. Определиться какие директории должны быть привязаны у пользователя
3. Сделать универсальный пайплайн под разные вирусные гепатиты:
  + Добавить возможность добавлять и выбирать референсные последовательности
  + Оптимизировать пайплайн под работу в докере на любой ОС
  + Подумать над способом передачи параметров программе и запуском протокола обработки. Нужен ли графический интерфейс?
  + Модульная структура? Использование того или иного модуля в зависимости от задачи
***
Надо ли? Или отработать на скриптах, прежде чем переносить в докер?
* Дописать пайплайн в Jupyter notebook
* Создать начальные директории
* Положить файлы референсных последовательностей
* Написать install.sh для установки зависимостей
  + Во время установки создать в корне директории bin/ и samples/
  + В bin/ скачать и установить FastQC, Samtools, GATK, Minimap2
 
