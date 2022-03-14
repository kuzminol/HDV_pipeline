#! /usr/bin/env python3

import os
import subprocess
import itertools

from prompt_toolkit.shortcuts import checkboxlist_dialog
from prompt_toolkit.shortcuts import input_dialog

# Получаем список всех fastq-файлов в директории с сырыми данными образцов
samples_directory = "samples"
files = sorted(os.listdir(samples_directory))

# Создаем списки для сортировки образцов по количеству fastq-файлов
one_fastq = []
several_fastq = []

# Сортируем образцы, создаём кортежи (название образца, :, *fastq.gz)
for i in range(len(files)):
    if "R1" in files[i] or "R2" in files[i]:
        several_fastq.append((files[i].split("_L")[0], ': ', samples_directory + '/' + files[i].split("_L")[0] + '_merged.fastq.gz'))
    else:
        one_fastq.append((files[i].split(".fastq")[0], ': ', samples_directory + '/' + files[i].split(".fastq")[0] + '.fastq.gz'))

# Удаляем повторные названия образцов
several_fastq = list(set(several_fastq))

# Объединяем списки с образцами, получаем общий список всех образцов
samples_one_fastq = [p[0] for p in one_fastq]
samples_several_fastq = [p[0] for p in several_fastq]
samples_fastq = sorted([*several_fastq, *one_fastq])
samples_fastq_names = sorted([*samples_one_fastq, *samples_several_fastq])
samples = list(zip(samples_fastq_names, samples_fastq_names))


samples_to_run = checkboxlist_dialog(
    title="Сборка генома",
    text="Выберите образ(-ец, -цы)",
    values=samples
).run()

availiable_threads = os.cpu_count()

threads = input_dialog(
    title='Многопоточность',
    text=f'Всего доступно {availiable_threads} поток(-а, -ов). Сколько потоков использовать в работе протокола?').run()

# В случае, если закинули просто fasq - заархивировать их в .gz
subprocess.call(f'pigz -p {threads} {samples_directory}/*.fastq', shell = True)

# Сливаем только те образцы с несколькими fastq, которые были выбраны для анализа 
for i in range(len(samples_to_run)):
    for x in samples_several_fastq: 
        if x == samples_to_run[i]:
            subprocess.call(f'zcat {samples_directory}/{samples_to_run[i]}*.gz | pigz -p {threads} > {samples_directory}/{samples_to_run[i]}_merged.fastq.gz', shell = True)

config_samples = []
for i in range(len(samples_to_run)):
    for x in samples_fastq: 
        if x[0] == samples_to_run[i]:
            config_samples.append(''.join((x[0], x[1], x[2])))
                        
config = f'''reference: 'refs/reference.fa'
threads: {threads}
samples:\n    ''' + '\n    '.join(config_samples)

config_file = 'config_assembly.yaml'
with open(config_file, 'w') as w:
    w.write(config)
