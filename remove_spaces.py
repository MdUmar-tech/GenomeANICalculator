import os

def replace_spaces_with_underscores(directory):
    for filename in os.listdir(directory):
        if " " in filename:
            new_filename = filename.replace(" ", "_")
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            os.rename(old_path, new_path)
            print(f'Renamed: {filename} to {new_filename}')

def main():
    folder_name = input("Enter the folder name: ")
    directory_path = os.path.join(os.getcwd(), folder_name)

    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        replace_spaces_with_underscores(directory_path)
    else:
        print(f"The specified folder '{folder_name}' does not exist or is not a directory.")

if __name__ == "__main__":
    main()
