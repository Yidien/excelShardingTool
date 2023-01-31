# coding:utf-8

import os
import PySide2


dir_name = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dir_name, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


from guietta import Gui, ___
from PySide2.QtWidgets import QFileDialog
import pandas as pd


def event_select_input_file(gui, *args):
    gui.input_file = QFileDialog.getOpenFileName()[0]
    if not gui.output_dir:
        gui.output_dir = os.path.dirname(gui.input_file)
    return


def event_select_output_dir(gui, *args):
    gui.output_dir = QFileDialog.getExistingDirectory()
    return


def event_work(gui, *args):
    if gui.input_file and gui.output_dir:
        gui.bt_work.setEnabled(False)
        df = pd.read_excel(gui.input_file)
        grouped = df.groupby(['入库类型1', '入库类型2', '入库等级'])
        prefix_file_name = gui.output_dir + '/' + (gui.prefix + '-' if gui.prefix else '')
        for name, group in grouped:
            file_name = prefix_file_name + '-'.join(map(lambda x: str(x), name)) + gui.postfix
            group[['敏感词', '备注']].to_csv(file_name, sep=',', index=False)
        gui.bt_work.setEnabled(True)
    return


def main():
    gui = Gui\
        (
            ['输入文件：', '__input_file__', ___, ___, (['选择文件...'], 'bt_input_file')],
            ['输出文件夹：', '__output_dir__', ___, ___, (['选择文件夹...'], 'bt_output_dir')],
            ['前缀：', '__prefix__', '后缀：', '__postfix__', (['分片'], 'bt_work')],
            title='敏感词分片工具'
        )

    gui.bt_input_file = event_select_input_file
    gui.bt_output_dir = event_select_output_dir
    gui.bt_work = event_work

    gui.postfix = '.txt'

    gui.run()
    return


if __name__ == '__main__':
    main()