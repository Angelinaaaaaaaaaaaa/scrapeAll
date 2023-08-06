import warnings

from src.getClean.clean_table import *
from src.getClean.image_to_table import *
from src.getClean.pdf_to_image import *

# Settings the warnings to be ignored
warnings.filterwarnings('ignore')


def getClean(input_path, output_path, data_type):
    """
    Should pass in the path to the folder of target raw/temp data
    eg. data/Guangdong/raw/prov_month
    """

    if data_type == 'image':
        # convert one image
        if os.path.isfile(input_path):
            read_image_to_xls(input_path, os.path.split(input_path)[-1], output_path)
        elif os.path.isdir(input_path):
            is_mul_dir = input('Are there multiple folders (Yes/No)? (press enter to accept the default value: No):\n').lower()
            if is_mul_dir == 'yes':
                for folder in os.listdir(input_path):
                    if os.path.isdir(os.path.join(input_path, folder)):
                        image_folder = os.path.join(input_path, folder)
                        head, tail = os.path.split(image_folder)
                        temp_path = image_folder  # same folder as image
                        # extract and split tables from images
                        convert_all_images(image_folder, temp_path)
                        all_tables = get_tables_from_excels(temp_path)
                        tables = split_tables(all_tables)
                        store_clean(tables, output_path, table_name=folder)
            else:
                head, tail = os.path.split(input_path)
                temp_path = input_path
                # extract and split tables from images
                convert_all_images(input_path, temp_path)
                all_tables = get_tables_from_excels(temp_path)
                tables = split_tables(all_tables)
                store_clean(tables, output_path, table_name=tail)

    if data_type == 'pdf':
        # if input path is one pdf:
        if os.path.isfile(input_path):
            head, tail = os.path.split(input_path)
            file_name = tail.split('.')[0]
            temp_path = os.path.join(os.path.dirname(input_path), 'temp_' + file_name + '/')
            if output_path == os.path.dirname(input_path):
                output_path = os.path.join(output_path, 'clean_' + file_name)
            # store pdf as image in temp folder
            save_image_from_pdf(input_path, temp_path)
            # extract and split tables from images
            convert_all_images(temp_path, temp_path)
            all_tables = get_tables_from_excels(temp_path)
            tables = split_tables(all_tables)
            store_clean(tables, output_path, file_name)


        # if input path is a folder
        elif os.path.isdir(input_path):
            for item in os.listdir(input_path):
                if not item.endswith('.pdf'):
                    continue
                # get file name, file path, and temporary path to store file images.
                file_name = item.split('.')[0]
                file_path = os.path.join(input_path, item)
                temp_path = os.path.join(input_path, f'temp/{file_name}/')
                # store pdf as images in temp folder
                save_image_from_pdf(file_path, temp_path, image_name=file_name)
                # extract and split tables from images
                convert_all_images(temp_path, temp_path)
                all_tables = get_tables_from_excels(temp_path)
                tables = split_tables(all_tables)
                # save tables in output folder
                new_output_path = os.path.join(output_path, file_name)
                store_clean(tables, new_output_path)

    if data_type == 'table':
        all_tables = get_tables_from_excels(input_path)
        tables = split_tables(all_tables)
        print(len(tables))
        store_clean(tables, output_path)
