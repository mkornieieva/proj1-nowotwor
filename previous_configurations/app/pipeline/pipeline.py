import os
from fast import extract_files
from ekstrakcjaxml import convert_xml_to_txt
from korektanazwtxt import match_and_rename


def safe_extract_files(src_folder, dest_folder):
    try:
        extract_files(src_folder, dest_folder)
    except Exception as e:
        print(f"Error while moving files from {src_folder} to {dest_folder}: {e}")


def safe_convert_xml_to_txt(xml_folder, txt_folder):
    try:
        convert_xml_to_txt(xml_folder, txt_folder)
    except Exception as e:
        print(f"Error while converting XML to TXT in folder {xml_folder}: {e}")


def safe_match_and_rename(txt_folder, dicom_folder, output_folder):
    try:
        match_and_rename(txt_folder, dicom_folder, output_folder)
    except Exception as e:
        print(f"Error while matching and renaming TXT files: {e}")


def main():
    # Ścieżki folderów
    src_folder_dicom = r'*przyklad*'  # Folder źródłowy plików dicom
    dest_folder_xml = r'*przyklad*'  # Folder docelowy dla XML
    src_folder_xml = r'*przyklad*'  # Folder źródłowy plików xml
    dest_folder_dicom = r'*przyklad*'  # Folder docelowy dla DICOM
    xml_folder = r'*przyklad*'  # Folder z plikami XML
    txt_folder = r'*przyklad*'  # Folder docelowy dla TXT
    renamed_txt_folder = r'*przyklad*'  # Folder na TXT z poprawionymi nazwami

    print("Przenoszenie plików xml...")
    safe_extract_files(src_folder_xml, dest_folder_xml)

    print("Przenoszenie plików dicom...")
    safe_extract_files(src_folder_dicom, dest_folder_dicom)

    print("Konwersja plików XML na TXT...")
    safe_convert_xml_to_txt(xml_folder, txt_folder)

    print("Dopasowywanie i zmiana nazw plików TXT...")
    safe_match_and_rename(txt_folder, dest_folder_dicom, renamed_txt_folder)

    print("Proces zakończony pomyślnie!")


if __name__ == "__main__":
    main()