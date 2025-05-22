import re
import matplotlib.pyplot as plt


file_path = "result.txt"

with open(file_path, "r") as f:
    content = f.read()

# Разделение по файла с результатами по блокам
bs = re.split(r"-{5,}", content)
bs = [block.strip() for block in bs if block.strip()]
print(bs)
blocks = []
for i in range(len(bs)-1):
    blocks.append(bs[i] + bs[i+1])


# Списки для хранения данных
weights = []
repeatabilitys = []
localization_errors = []
nn_mean_aps = []
matching_scores = []

for block in blocks:
    filename_match = re.search(r"^(superPointNet_\d+_checkpoint\.pth\.tar)", block)
    if filename_match:
        filename = filename_match.group(1)
        # Получаем эпоху из имени файла
        weight_match = re.search(r"_(\d+)_checkpoint", filename)
        if weight_match:
            weight_value = int(weight_match.group(1))
            weights.append(weight_value)
        else:
            continue

        # Извлечение данных из блока
        repeatability_match = re.search(r"repeatability:\s*([0-9.]+)", block)
        localization_error_match = re.search(r"localization error:\s*([0-9.]+)", block)
        nn_mean_AP_match = re.search(r"nn mean AP:\s*([0-9.]+)", block)
        matching_score_match = re.search(r"matching score:\s*([0-9.]+)", block)

        if repeatability_match and localization_error_match and nn_mean_AP_match and matching_score_match:
            repeatabilitys.append(float(repeatability_match.group(1)))
            localization_errors.append(float(localization_error_match.group(1)))
            nn_mean_aps.append(float(nn_mean_AP_match.group(1)))
            matching_scores.append(float(matching_score_match.group(1)))
        else:
            repeatabilitys.append(None)
            localization_errors.append(None)
            nn_mean_aps.append(None)
            matching_scores.append(None)

# Сортировка по весам для корректного отображения графиков
sorted_indices = sorted(range(len(weights)), key=lambda i: weights[i])
weights_sorted = [weights[i] for i in sorted_indices]
repeatabilitys_sorted = [repeatabilitys[i] for i in sorted_indices]
localization_errors_sorted = [localization_errors[i] for i in sorted_indices]
nn_mean_aps_sorted = [nn_mean_aps[i] for i in sorted_indices]
matching_scores_sorted = [matching_scores[i] for i in sorted_indices]

plt.figure(figsize=(12, 8))

# График Repeatability
plt.subplot(2, 2, 1)
plt.plot(weights_sorted, repeatabilitys_sorted, marker="o")
plt.xlabel("Количество эпох обучения")
plt.ylabel("Repeatability")
plt.title("Repeatability")
plt.grid(True)

# График Localization Error
plt.subplot(2, 2, 2)
plt.plot(weights_sorted, localization_errors_sorted, marker="o", color="orange")
plt.xlabel("Количество эпох обучения")
plt.ylabel("Localization Error")
plt.title("Localization Error")
plt.grid(True)

# График NN Mean AP
plt.subplot(2, 2, 3)
plt.plot(weights_sorted, nn_mean_aps_sorted, marker="o", color="green")
plt.xlabel("Количество эпох обучения")
plt.ylabel("NN Mean AP")
plt.title("NN Mean AP")
plt.grid(True)

# График Matching Score
plt.subplot(2, 2, 4)
plt.plot(weights_sorted, matching_scores_sorted, marker="o", color="red")
plt.xlabel("Количество эпох обучения")
plt.ylabel("Matching Score")
plt.title("Matching Score")
plt.grid(True)

plt.tight_layout()
plt.show()