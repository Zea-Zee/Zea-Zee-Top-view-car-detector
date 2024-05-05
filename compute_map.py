from collections import defaultdict
import os
import numpy as np

def calculate_iou(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    intersection_x = max(x1, x2)
    intersection_y = max(y1, y2)
    intersection_w = min(x1 + w1, x2 + w2) - intersection_x
    intersection_h = min(y1 + h1, y2 + h2) - intersection_y

    if intersection_w <= 0 or intersection_h <= 0:
        return 0

    intersection_area = intersection_w * intersection_h
    box1_area = w1 * h1
    box2_area = w2 * h2
    iou = intersection_area / (box1_area + box2_area - intersection_area)

    return iou

def calculate_ap(precision, recall):
    m_recall = np.concatenate(([0.], recall, [1.]))
    m_precision = np.concatenate(([0.], precision, [0.]))

    for i in range(len(m_precision) - 2, -1, -1):
        m_precision[i] = max(m_precision[i], m_precision[i+1])

    indices = np.where(m_recall[1:] != m_recall[:-1])[0] + 1
    ap = np.sum((m_recall[indices] - m_recall[indices-1]) * m_precision[indices])
    return ap

def evaluate_detection(ground_truth_dir, predicted_dir, iou_threshold=0.5):
    ground_truth = defaultdict(list)
    for file in os.listdir(ground_truth_dir):
        if file.endswith(".txt"):
            with open(os.path.join(ground_truth_dir, file), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip().split()
                    image_id = file[:-4]  # Удаляем расширение .txt из имени файла
                    class_id = int(line[0])
                    x, y, w, h = map(float, line[1:])
                    ground_truth[image_id].append((class_id, x, y, w, h))

    predicted = defaultdict(list)
    for file in os.listdir(predicted_dir):
        if file.endswith(".txt"):
            with open(os.path.join(predicted_dir, file), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip().split()
                    image_id = file[:-4]  # Удаляем расширение .txt из имени файла
                    class_id = int(line[0])
                    confidence = float(line[1])
                    try:
                        x, y, w, h = map(float, line[2:])
                    except ValueError:
                        print("Ошибка: неправильное количество значений в строке:", line)
                        continue  # Продолжить цикл, игнорируя эту строку

                    predicted[image_id].append((class_id, confidence, x, y, w, h))

    average_precision = []
    for image_id, ground_truth_boxes in ground_truth.items():
        if image_id not in predicted:
            continue

        predicted_boxes = predicted[image_id]
        predicted_boxes.sort(key=lambda x: x[1], reverse=True)
        true_positives = np.zeros(len(predicted_boxes))
        false_positives = np.zeros(len(predicted_boxes))
        total_true_objects = len(ground_truth_boxes)

        for i, predicted_box in enumerate(predicted_boxes):
            _, confidence, px, py, pw, ph = predicted_box
            predicted_box = (px, py, pw, ph)

            for j, ground_truth_box in enumerate(ground_truth_boxes):
                _, gx, gy, gw, gh = ground_truth_box
                ground_truth_box = (gx, gy, gw, gh)
                iou = calculate_iou(predicted_box, ground_truth_box)

                if iou >= iou_threshold:
                    true_positives[i] = 1
                    ground_truth_boxes.pop(j)
                    break

            false_positives[i] = 1 - true_positives[i]

        cumulative_true_positives = np.cumsum(true_positives)
        cumulative_false_positives = np.cumsum(false_positives)
        precision = cumulative_true_positives / (cumulative_true_positives + cumulative_false_positives)
        recall = cumulative_true_positives / total_true_objects

        ap = calculate_ap(precision, recall)
        average_precision.append(ap)

    mAP = np.mean(average_precision)
    return mAP

# Пример использования
ground_truth_dir = './dataset/test/labels'
predicted_dir = ('yolov5/runs/detect/exp5/labels' if input('Choose dataset: small / big') == 'small' else 'yolov5/runs/detect/exp7/labels')
mAP = evaluate_detection(ground_truth_dir, predicted_dir)
print("mAP:", mAP)
