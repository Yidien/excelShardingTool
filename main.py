# coding:utf-8

from os import environ, path
from PySide2 import __file__


dir_name = path.dirname(__file__)
plugin_path = path.join(dir_name, 'plugins', 'platforms')
environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


from guietta import Gui, ___, C
from PySide2.QtWidgets import QFileDialog, QMessageBox
from pandas import read_excel


def event_select_input_file(gui, *args):
    gui.input_file = QFileDialog.getOpenFileName()[0]
    if not gui.output_dir:
        gui.output_dir = path.dirname(gui.input_file)
    return


def event_select_output_dir(gui, *args):
    gui.output_dir = QFileDialog.getExistingDirectory()
    return


def event_work(gui, *args):
    ret_string = '输入或输出文件（夹）为空'
    gui.bt_work.setEnabled(False)
    if gui.input_file and gui.output_dir:
        if gui.cb_admin.isChecked():
            output_file_by_admin(gui.input_file, gui.output_dir, gui.prefix, gui.postfix)
        else:
            output_file(gui.input_file, gui.output_dir, gui.prefix, gui.postfix)
        ret_string = '分片成功'
    QMessageBox.information(None, '结果', ret_string)
    gui.bt_work.setEnabled(True)
    return


def output_file(input_file, output_dir, prefix, postfix):
    df = read_excel(input_file)
    grouped = df.groupby(['入库类型1', '入库类型2', '入库等级'])
    prefix_file_name = output_dir + '/' + (prefix + '-' if prefix else '')
    for name, group in grouped:
        file_name = prefix_file_name + '-'.join(map(lambda x: str(x), name)) + postfix
        group[['敏感词', '备注']].to_csv(file_name, sep=',', index=False)
    return


def output_file_by_admin(input_file, output_dir, prefix, postfix):
    df = read_excel(input_file)
    prefix_file_name = output_dir + '/' + (prefix + '-' if prefix else '')
    file_name = prefix_file_name + path.splitext(path.basename(input_file))[0] + '-输出' + postfix
    df["入库类型"] = df["入库类型1"] + '/' + df["入库类型2"]
    df["输出"] = df.apply(
        lambda line: '||'.join([str(line["敏感词"]), line["入库类型"], line["入库等级"], line["备注"]]), axis=1)
    # df["输出"] = '||'.join([df["敏感词"].astype(str), df["入库类型"], df["入库等级"], df["备注"]])
    df["输出"].to_csv(file_name, sep=',', index=False, header=None)
    return


def main():
    gui = Gui\
        (
            ['输入文件：', '__input_file__', ___, ___, ___, (['选择文件...'], 'bt_input_file')],
            ['输出文件夹：', '__output_dir__', ___, ___, ___, (['选择文件夹...'], 'bt_output_dir')],
            ['前缀：', '__prefix__', '后缀：', '__postfix__', (C('管理员录入'), 'cb_admin'), (['分片'], 'bt_work')],
            title='敏感词分片工具'
        )

    gui.bt_input_file = event_select_input_file
    gui.bt_output_dir = event_select_output_dir
    gui.bt_work = event_work

    gui.postfix = '.txt'
    gui.cb_admin.setChecked(True)

    gui.run()
    return


if __name__ == '__main__':
    main()