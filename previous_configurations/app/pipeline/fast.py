import os
import shutil

# F.A.S.T. - folder and subfolder transfer

def extract_files(src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for root, _, files in os.walk(src_folder):
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_folder, file)
            shutil.move(src_file, dest_file)
            print(f"Moved: {src_file} to {dest_file}")

if __name__ == "__main__":
    src_folder = r'E:\!!!!!STUDIAsem4\lung-PET-CT-Dx'  # Update with the path to the source folder
    dest_folder = r'E:\!!!!!STUDIAsem4\PROJ2\AI-detect\data\dicom'  # Update with the path to the destination folder
    extract_files(src_folder, dest_folder)