import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("./results.csv")
data.columns = data.columns.str.strip()

print(data.head())
print(data.columns)

sns.set(style="whitegrid")

fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(18, 15), sharex=True)

# Построение графиков тренировочных потерь
sns.lineplot(x='epoch', y='train/box_loss', data=data, ax=axes[0, 0], label='Box    Loss')
sns.lineplot(x='epoch', y='train/obj_loss', data=data, ax=axes[0, 0], label='Object Loss')
sns.lineplot(x='epoch', y='train/cls_loss', data=data, ax=axes[0, 0], label='Class  Loss')
axes[0, 0].set_title('Training Losses')
axes[0, 0].set_ylabel('Loss')
axes[0, 0].legend()

# Построение графиков валидационных потерь
sns.lineplot(x='epoch', y='val/box_loss', data=data, ax=axes[0, 1], label='Box      Loss')
sns.lineplot(x='epoch', y='val/obj_loss', data=data, ax=axes[0, 1], label='Object   Loss')
sns.lineplot(x='epoch', y='val/cls_loss', data=data, ax=axes[0, 1], label='Class    Loss')
axes[0, 1].set_title('Validation Losses')
axes[0, 1].set_ylabel('Loss')
axes[0, 1].legend()

# Построение графиков метрик точности и полноты
sns.lineplot(x='epoch', y='metrics/precision', data=data, ax=axes[1, 0], label='Precision')
sns.lineplot(x='epoch', y='metrics/recall', data=data, ax=axes[1, 0], label='Recall')
axes[1, 0].set_title('Precision and Recall')
axes[1, 0].set_ylabel('Value')
axes[1, 0].legend()

# Построение графиков метрик mAP
sns.lineplot(x='epoch', y='metrics/mAP_0.5', data=data, ax=axes[1, 1], label='mAP 0.5')
sns.lineplot(x='epoch', y='metrics/mAP_0.5:0.95', data=data, ax=axes[1, 1], label='mAP 0.5:0.95')
axes[1, 1].set_title('mAP Metrics')
axes[1, 1].set_ylabel('mAP')
axes[1, 1].legend()

# Построение графиков изменения скоростей обучения
sns.lineplot(x='epoch', y='x/lr0', data=data, ax=axes[2, 0], label='LR0')
sns.lineplot(x='epoch', y='x/lr1', data=data, ax=axes[2, 0], label='LR1')
sns.lineplot(x='epoch', y='x/lr2', data=data, ax=axes[2, 0], label='LR2')
axes[2, 0].set_title('Learning Rates')
axes[2, 0].set_ylabel('Learning Rate')
axes[2, 0].legend()

fig.delaxes(axes[2][1])

plt.tight_layout()
plt.savefig('./results.png')
plt.show()
