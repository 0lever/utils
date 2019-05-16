# -*- coding:utf-8 -*-
import pandas as pd


class Excel(object):
    DEFAULT = 0
    RIGHT = 1
    DOWN = 2

    def __init__(self):
        pass

    @staticmethod
    def dfs2excel(dfs, filename, sheetnames=[], connect_type=DEFAULT, col_gap=1, row_gap=1):
        """
        dataframe数组写excel
        :param dfs: dataframe数组
        :param filename: excel文件名
        :param sheetnames: sheet页名称数组
        :param connect_type: excel连接方向
        :param col_gap: 列间隙
        :param row_gap: 行间隙
        :return: filename
        """
        try:
            sheetname_iter = iter(sheetnames)
            excelWrite = pd.ExcelWriter(filename)

            if connect_type == Excel.DEFAULT:
                for i in range(len(dfs)):
                    df = dfs[i]
                    sheetname = next(sheetname_iter, "Sheet{index}".format(index=i))
                    df.to_excel(excelWrite, sheet_name=sheetname, index=False)
            elif connect_type == Excel.RIGHT:
                sheetname = next(sheetname_iter, "Sheet0")
                startcol = 0
                for i in range(len(dfs)):
                    df = dfs[i]
                    df.to_excel(excelWrite, sheet_name=sheetname, startcol=startcol, index=False)
                    startcol = startcol + df.shape[1] + col_gap
            elif connect_type == Excel.DOWN:
                sheetname = next(sheetname_iter, "Sheet0")
                startrow = 0
                for i in range(len(dfs)):
                    df = dfs[i]
                    df.to_excel(excelWrite, sheet_name=sheetname, startrow=startrow, index=False)
                    # +1 是加header头
                    startrow = startrow + df.shape[0] + 1 + row_gap
            excelWrite.save()
            return filename
        except Exception as e:
            print(e)
            return None
