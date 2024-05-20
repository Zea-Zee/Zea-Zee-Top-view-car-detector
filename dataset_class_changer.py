import os

def process_files_in_directory():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    i = 0
    for file_name in files:
        print(i)
        i += 1
        with open(file_name, 'r') as file:
            lines = file.readlines()

        modified_lines = []
        for line in lines:
            if line.startswith('1'):
                modified_lines.append('0' + line[1:])
                print(file_name, line)
            else:
                modified_lines.append(line)

        with open(file_name, 'w') as file:
            file.writelines(modified_lines)

if __name__ == "__main__":
    process_files_in_directory()
