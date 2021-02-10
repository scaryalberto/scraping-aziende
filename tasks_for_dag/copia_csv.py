from shutil import copyfile
import os

def copy_file():
    src="/home/alberto/PycharmProjects/kinder/missing_address_difference_for_me.csv"
    dst=os.getcwd()+"/file di appoggio.csv"
    copyfile(src, dst)

copy_file()