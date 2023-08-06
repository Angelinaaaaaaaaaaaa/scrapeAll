import sys

from getClean import *
from getRaw import *


def main():
    try:
        # define an input path and/or output path
        # first argv can be the path to store raw data if getRaw
        # or first argv can be the path to the json file that contains multiple links if getRaw
        # first argv is the path to raw data if getClean
        input_path = sys.argv[1]
        current = os.getcwd()
        output_path = os.path.join(current, input_path)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    except:
        # no input path provided
        output_path = os.getcwd()

    if os.path.isdir(output_path):
        if 'raw' in output_path:
            clean_output_path = output_path.replace('raw', 'clean')
        else:
            clean_output_path = output_path
    elif os.path.isfile(output_path):
        if 'raw' in output_path:
            clean_output_path = os.path.dirname(output_path).replace('raw', 'clean')
        else:
            clean_output_path = os.path.dirname(output_path)

    format = input('GetRaw or GetClean? \n').lower().replace(' ', '')
    if format == 'getraw':
        data_type = input('urls/table/image/pmos_pdf?\n').lower()
        continue_clean = input('Do you want to clean raw data after scraping? (Yes, No)\n').lower()
        getRaw(output_path, data_type)
        if continue_clean == 'yes':
            if data_type == 'urls':
                print("Please rerun the script with the newly stored json file")
            else:
                if data_type == 'pmos_pdf':
                    data_type = 'pdf'
                getClean(output_path, clean_output_path, data_type)

    if format == 'getclean':
        data_type = input('What type of data? image/pdf/table \n')
        getClean(output_path, clean_output_path, data_type)


if __name__ == '__main__':
    main()
