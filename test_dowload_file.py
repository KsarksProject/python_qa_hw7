import os
import zipfile

import PyPDF2
import pandas as pd


def create_zip_archive(zip_name, files):
    with zipfile.ZipFile(zip_name, 'w') as archive:
        for file in files:
            archive.write(file, os.path.basename(file))


def read_zip_content(zip_name):
    extracted_content = {}
    with zipfile.ZipFile(zip_name, 'r') as archive:
        for file_name in archive.namelist():
            with archive.open(file_name) as file:
                if file_name.endswith('.pdf'):
                    reader = PyPDF2.PdfReader(file)
                    text = ''.join(page.extract_text() for page in reader.pages)
                    extracted_content[file_name] = text
                elif file_name.endswith('.xlsx'):
                    excel_data = pd.read_excel(file)
                    extracted_content[file_name] = excel_data.to_dict()
                elif file_name.endswith('.csv'):
                    csv_data = pd.read_csv(file)
                    extracted_content[file_name] = csv_data.to_dict()
    return extracted_content


# Тесты
def test_create_zip_archive():
    files_to_archive = [
        'tmp/Black_Hat_Python.pdf',
        'tmp/sample2.xlsx',
        'tmp/sample4.csv'
    ]
    zip_file_name = 'tmp/test_files.zip'

    create_zip_archive(zip_file_name, files_to_archive)
    assert os.path.exists(zip_file_name), "Архив не был создан"


def test_read_zip_content():
    zip_file_name = 'tmp/test_files.zip'

    content = read_zip_content(zip_file_name)

    assert 'Black_Hat_Python.pdf' in content
    assert "Black Hat Python: программирование" in content['Black_Hat_Python.pdf']

    assert 'sample2.xlsx' in content
    assert 'Creator' in content['sample2.xlsx']
    assert 'John Doe' in content['sample2.xlsx']['Creator'].values()

    assert 'sample4.csv' in content
    assert 'Game Number' in content['sample4.csv']
    assert content['sample4.csv']['Game Number'][0] == 1
