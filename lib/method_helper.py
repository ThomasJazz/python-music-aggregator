import os
import shutil
import ntpath
import hashlib
import csv
from datetime import datetime
from os import listdir
from os.path import isfile, join
from pathlib import Path
from PIL import Image
import os

class MethodHelper:
    def __init__(self):
        pass
    
    ########################################
    # ------------------------------------ #
    # ------- File Structure Manip ------- #
    # ------------------------------------ #
    ########################################

    def get_files_in_dir(self, src: str, recursive=False, extension='', contains='', match_case=False, full_path=True):
        src = src.replace('''\\''', '/')
        files = []
        filtered_files = []
        contains_lst = contains.split(',')

        if (recursive):
            for r, d, f in os.walk(src):
                for filename in f:
                    file_path = join(r, filename).replace('\\', '/')

                    if (match_case):
                        if any(val in file_path for val in contains_lst):
                            files.append(file_path)
                    else:
                        if any(val.lower() in file_path.lower() for val in contains_lst):
                            files.append(file_path)


        else: # TODO: Make this return full path
            files = [join(src, f) for f in listdir(src) if (isfile(join(src, f)))]

            for i in range(0, len(files)):
                file_path = files[i]

                if (contains_lst and any(val.lower() in file_path.lower() for val in contains_lst)):
                    filtered_files.append(files[i].replace('''\\''', '/'))
            
            return filtered_files
            
        if not(full_path):
            for i in range(0, len(files)):
                files[i] = os.path.basename(files[i])

        return files

    # Recursively retrieve all files and subfiles with contains value in them
    # Because it's recursive, all files in returned list will include the full path, unlike get_files_in_dir
    def get_files_in_dir_recursive(self, src: str, contains='', excludes=None, item_limit=None):
        files = []
        
        for r, d, f in os.walk(src):
            for filename in f:
                full_path = join(r, filename).replace('\\', '/')
                
                if contains.lower() in full_path.lower():
                    if (item_limit and len(files) >= item_limit):
                        break
                    files.append(full_path)


        if (excludes is None):  # If we don't need to exclude anything, we go ahead and return
            return files

        elif (excludes is not None):    # Exclude files
            filtered_files = []
            for file in files:
                if not(excludes.lower() in file.lower()):
                    filtered_files.append(file)

            return filtered_files


    def check_and_create_dir(self, src):
        if os.path.isdir(src):
            pass
        else:
            try:
                os.mkdir(src)
            except:
                print("Error creating directory")


    def get_parent_dir(self, src):
        basename = os.path.basename(src)
        return src.replace(basename, '')


    def copy_paste_file_structure(self, src, dest_dir):
        if (os.path.isdir(src)):
            if not(os.path.isdir(dest_dir)): # Create destination directory if it doesn't already exist
                os.mkdir(dest_dir)

            for r, d, f in os.walk(src):
                if (os.path.isdir(r)):
                    sub_dir = r.replace(src, '')
                    new_dir = dest_dir + sub_dir
                    try:
                        if not(os.path.isdir(new_dir)):
                            os.mkdir(new_dir)
                        if not(os.path.isdir(new_dir)):
                            raise FileNotFoundError
                    except Exception as e:
                        print(str(e))


    def get_file_structure(self, src, contains='', recursive=True, full_path=True):
        contains = contains.lower()
        sub_dirs = []
        if (recursive):
            if (os.path.isdir(src)):
                for r, d, f in os.walk(src):
                    for directory in d:
                        dir_path = join(r, directory)
                        dir_path = dir_path.replace('\\', '/')
                        if (os.path.isdir(dir_path) and contains.lower() in dir_path.lower()):
                            if not(directory.endswith('/')):
                                directory += '/'
                            if not(directory == src):
                                sub_dirs.append(dir_path)
        else:
            sub_dirs = [join(src, f) for f in listdir(src) if (os.path.isdir(join(src, f)) and contains.lower() in f.lower())]


        if not(full_path):
            sub_dirs_temp = []

            for file in sub_dirs:
                sub_dirs_temp.append(os.path.basename(file))
            
            sub_dirs = sub_dirs_temp
            
        return sub_dirs


    def delete_files_in_dir(self, dir: str):
        dir = dir.lower()

        file_lst = self.get_files_in_dir(dir)
        if (len(file_lst) > 500):
            confirm = input(f'About to delete {len(file_lst)} files. Please confirm with y/yes')

            if not(confirm == 'y' or confirm == 'yes'):
                return

        for f in file_lst:
            if (self.file_exists(f)):
                os.remove(f)

    # Archive EVERY file in the 'src' directory
    def archive_files(self, src: str, dest='', extension='', contains='', override=False):
        if (dest == ''):
            dest = src + '_Archive/'
        
        assert (os.path.isdir(dest)), "[Error] Archive folder does not exist: {0}".format(dest)

        lst_files = self.get_files_in_dir(src)
    
        # Make sure there are actually files to archive
        if (len(lst_files) > 0):
            for file in lst_files:
                if (contains in file and file.endswith(extension)):
                    src_filename = src + file
                    dest_filename = dest + file
                    try:
                        if override is True:
                            self.cut_paste_file(src_filename, dest_filename, override=override)
                        else:
                            self.cut_paste_file(src_filename, dest_filename)
                        assert(self.file_exists(dest_filename) and not self.file_exists(src_filename)), "Warning, failed to archive file: {0}".format(dest_filename)
                    except Exception as e:
                        print(e)
                        return 0
        
        return 1

    @staticmethod
    def file_exists(file_path: str):
        try:
            if (os.path.exists(file_path) == False) or (os.stat(file_path).st_size == 0):
                return False
        except:
            return False
        return True


    def cut_paste_file(self, src: str, dest: str, override=False):
        if (self.file_exists(dest) and override == False):
            raise Exception("Error, cannot override existing file")
        else:
            shutil.move(src, dest)
        
            if self.file_exists(src):
                raise Exception("Failed to cut and paste file")
        

    def copy_paste_file(self, src: str, dest: str, override=False):
        if (self.file_exists(dest) and override == False):
            raise Exception("Error, cannot override existing file")
        else:
            shutil.copy(src, dest)
            if not(self.file_exists(dest)):
                raise Exception("")


    def copy_files_to_dir(self, src: str, dest: str, extension='', contains='', include_dirs=False):
        if not(src.endswith('/')):
            src += '/'
        if not(dest.endswith('/')):
            dest += '/'

        lst_files = []
        if (include_dirs):
            lst_files = os.listdir(src)
        else:
            lst_files = [f for f in os.listdir(src) if isfile(join(src, f))]

        if (len(lst_files) > 0):
            for file in lst_files:
                if (file.endswith(extension) and contains in file):
                    src_filename = src + file
                    dest_filename = dest + file

                    self.copy_paste_file(src_filename, dest_filename)

    ########################################
    # ------------------------------------ #
    # ------------ File Info ------------- #
    # ------------------------------------ #
    ########################################
    def get_basename(self, file: str):
        return ntpath.basename(file)
    
    def get_file_hash(self, file: str):
        hash_md5 = hashlib.md5()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_dir_size(self, directory: str):
        files_in_dir = self.get_files_in_dir(directory, recursive=True)
        size_kb = sum([os.path.getsize(f) for f in files_in_dir if os.path.isfile(f)])
        return size_kb

    #######################################
    # ----------------------------------- #
    # ------------- Utility ------------- #
    # ----------------------------------- #
    #######################################

    def get_current_date(self):
        return datetime.today().strftime('%Y%m%d')

    def get_current_datetime(self):
        return datetime.today().strftime('%Y%m%d-%H%M%S')

    def get_sql_date(self):
        return datetime.today().strftime('%Y-%m-%d')
    
    def get_sql_date_time(self):
        return datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')

    ########################################
    # ------------------------------------ #
    # ------------- File I/O ------------- #
    # ------------------------------------ #
    ########################################

    def export_lst_to_file(self, file_path, output: list):
        with open(file_path, 'w') as file:
            for line in output:
                file.write(line + '\n')


    def write_delimited_file(self, file_path, data_lst, fieldterminator, rowterminator):
        #data_lst = self.stringify_2d_list(data_lst)
        with open(file_path, 'w', encoding='utf-8') as file:
            for i in range(0, len(data_lst)):
                items = data_lst[i]
                row = [(item or '') for item in items]
                data_lst[i] = row

            file.writelines(f'%s{rowterminator}' % fieldterminator.join(line) for line in data_lst)
    

    def read_csv(self, file_path: str, delimiter=","):
        with open(file_path, encoding="utf-8", newline='') as csvfile:
            csv_read_obj = csv.reader(csvfile, delimiter=delimiter)
            csv_read_lst = list(csv_read_obj)
            return csv_read_lst
    

    ##########################################
    # -------------------------------------- #
    # --------- Data Manipulation ---------- #
    # -------------------------------------- #
    ##########################################

    def convert_2dlst_to_lst_of_dict(self, lst_of_lst):
        return_lst = []
        headers_lst = lst_of_lst[0]
        for row in lst_of_lst:
            zipped_dict = dict(zip(headers_lst, row))
            return_lst.append(zipped_dict)

        return return_lst

    def clean_lst(self, dataset, exclude_terms: list):
        clean_data = []

        for item in dataset:
            if not(any(word.lower() in item.lower() for word in exclude_terms)):
                clean_data.append(item)
        
        return clean_data
