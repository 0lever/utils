# -*- coding:utf-8 -*-
import pandas as pd
import os


class Excel(object):
    DEFAULT = 0
    RIGHT = 1
    DOWN = 2

    def __init__(self):
        pass

    def _check_file(self, filename):
        file_dir = filename.rsplit(os.sep, 1)[0]
        if not os.path.exists(file_dir) and file_dir != filename:
            os.makedirs(file_dir)

    def dfs2excel(self, dfs, filename, sheetnames=[], connect_type=DEFAULT, gap=1):
        """
        dataframe数组写excel
        :param dfs: dataframe数组
        :param filename: excel文件名
        :param sheetnames: sheet页名称数组
        :param connect_type: excel连接方向
        :param gap: 行列间隙
        :return: filename
        """
        try:
            self._check_file(filename)

            sheetname_iter = iter(sheetnames)
            excelWrite = pd.ExcelWriter(filename)

            start = 0
            for i in range(len(dfs)):
                df = dfs[i]
                if i == 0 or connect_type == Excel.DEFAULT:
                    sheetname = next(sheetname_iter, "Sheet{index}".format(index=i))
                params = dict(excel_writer=excelWrite, sheet_name=sheetname, index=False)
                if connect_type == Excel.RIGHT:
                    params["startcol"] = start
                    start += df.shape[1] + gap
                elif connect_type == Excel.DOWN:
                    params["startrow"] = start
                    start += df.shape[0] + gap + 1
                df.to_excel(**params)
            excelWrite.save()
            return filename
        except Exception as e:
            print(e)
            return None

'''
# demo
df = pd.DataFrame({"a": [1, 2, 3]})
df1 = pd.DataFrame({"b": [2, 3, 4]})
dfs = [df, df1]

excel = Excel()
excel.dfs2excel(dfs, "aa/bb/cc/default.xlsx", ["a", "b"])
excel.dfs2excel(dfs, "aa/bb/cc/right.xlsx", ["a", "b"], Excel.RIGHT)
excel.dfs2excel(dfs, "aa/bb/cc/down.xlsx", ["a", "b"], Excel.DOWN)
'''