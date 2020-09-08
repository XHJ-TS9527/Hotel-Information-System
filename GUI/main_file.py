#导入包
import sys
sys.path.append('..')
import tkinter as tk
import main_window_package as mk
import global_manager as gm
import multiprocessing
import multiprocessing_win

def main():
    gm.initial_global_dict()
    main_win=tk.Tk()
    mk.main_window_thread(main_win)

if __name__=='__main__':
    multiprocessing.freeze_support() #打包用
    main()