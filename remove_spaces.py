import os

def replace_spaces_with_underscores(directory):
    for filename in os.listdir(directory):
        if " " in filename:
            new_filename = filename.replace(" ", "_")
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            os.rename(old_path, new_path)
            print(f'Renamed: {old_path} to {new_path}')

# Replace 'your_directory_path' with the path of the directory containing your files
replace_spaces_with_underscores('genomes')
