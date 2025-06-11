import os
import pydicom
import shutil

def match_and_rename(txt_folder, dicom_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    dicom_files = [f for f in os.listdir(dicom_folder) if f.endswith('.dcm')]
    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]

    for dicom_file in dicom_files:
        dicom_path = os.path.join(dicom_folder, dicom_file)
        dcm = pydicom.dcmread(dicom_path)
        sop_instance_uid = dcm.SOPInstanceUID

        for txt_file in txt_files:
            txt_uid = os.path.splitext(txt_file)[0]
            if sop_instance_uid == txt_uid:
                new_txt_filename = os.path.splitext(dicom_file)[0] + '.txt'
                new_txt_path = os.path.join(output_folder, new_txt_filename)
                shutil.move(os.path.join(txt_folder, txt_file), new_txt_path)
                print(f"Renamed {txt_file} to {new_txt_filename}")
                break


if __name__ == "__main__":
    txt_folder = r'E:\!!!!!STUDIAsem4\PROJ2\AI-detect\data\txt'  # Update with the path to your TXT folder
    dicom_folder = r'E:\!!!!!STUDIAsem4\PROJ2\AI-detect\data\dicom'  # Update with the path to your DICOM folder
    output_folder = r'E:\!!!!!STUDIAsem4\PROJ2\AI-detect\data\renamed_txt'  # Update with the path to save the renamed TXT files
    match_and_rename(txt_folder, dicom_folder, output_folder)
