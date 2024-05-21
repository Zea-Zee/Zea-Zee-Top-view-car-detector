import os
import argparse

def process_files_in_directory(start_dir):
    labels_dir = os.path.join(start_dir, 'labels')
    images_dir = os.path.join(start_dir, 'images')

    empty_files = []
    for file_name in os.listdir(labels_dir):
        file_path = os.path.join(labels_dir, file_name)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()

            if not lines:
                empty_files.append(file_name)
                continue

            modified_lines = []
            for line in lines:
                if line.startswith('1'):
                    modified_lines.append('0' + line[1:])
                    print(file_name, line)
                else:
                    modified_lines.append(line)

            with open(file_path, 'w') as file:
                file.writelines(modified_lines)

    for empty_file in empty_files:
        os.remove(os.path.join(labels_dir, empty_file))
        print(f"Deleted empty file: {empty_file} from {labels_dir}")
        base_name = os.path.splitext(empty_file)[0]

        # Поиск и удаление соответствующего файла в images
        for image_file in os.listdir(images_dir):
            if image_file.startswith(base_name):
                os.remove(os.path.join(images_dir, image_file))
                print(f"Deleted corresponding image file: {image_file} from {images_dir}")

    print(f"Total deletions: {len(empty_files)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process files in the specified start directory.")
    parser.add_argument('start_dir', type=str, help='The start directory containing labels and images folders')
    args = parser.parse_args()

    process_files_in_directory(args.start_dir)
