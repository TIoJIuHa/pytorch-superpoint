import os
from pathlib import Path
import shutil
import subprocess
import yaml
 

current_dir = Path.cwd()
weights_dir = "logs/superpoint_drone_flight/checkpoints"

weights = sorted(os.listdir(current_dir.joinpath(weights_dir)), key=lambda name: int(name.split("_")[1]))

for weight in weights:
    # Изменение пути до модели в конфигурационном файле
    with open(current_dir.joinpath("configs/magicpoint_repeatability_heatmap.yaml"), "r") as file:
        data = yaml.safe_load(file)
    data["model"]["pretrained"] = f"{current_dir}/{weight}"

    with open(current_dir.joinpath("configs/magicpoint_repeatability_heatmap.yaml"), "w") as file:
        yaml.dump(data, file)

    # Удаление старых предсказаний
    shutil.rmtree(current_dir.joinpath("logs/superpoint_hpatches_test"))

    with open(current_dir.joinpath("result.txt"), "a") as file:
        file.write("-----\n")
        file.write(weight)
        file.write("\n-----\n")

    # Запуск скрипта для получения аннотаций
    subprocess.call(['python', 'export.py', 'export_descriptor',  'configs/magicpoint_repeatability_heatmap.yaml', 'superpoint_hpatches_test'])
    # Запуск скрипа оценки
    subprocess.call(['python', 'evaluation.py', 'logs/superpoint_hpatches_test/predictions', '--repeatibility', '--homography'])
