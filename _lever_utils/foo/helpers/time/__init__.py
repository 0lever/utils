# -*- coding:utf-8 -*-
from datetime import datetime, timedelta


def get_time(num=0, sf="%Y%m%d",unit="days"):
    '''
    得到时间字符串
    :param num: 和unit配合使用计算时间
    :param sf: %Y%m%d%H%M%S
    :param unit: days = None, seconds = None, microseconds = None, milliseconds = None, minutes = None, hours = None, weeks = None
    :return: %Y%m%d%H%M%S 格式化时间
    '''

    arr = None
    exec "arr={'%s':%s}" % (unit, int(num))
    return str((datetime.today() + timedelta(**arr)).strftime(sf))


def get_certain_time(log_day, log_day_sf="%Y%m%d", num=0, sf="%Y%m%d", unit="days"):
    '''
    得到指定时间字符串
    :param log_day: 时间
    :param log_day_sf: 时间format
    :param num: 和unit配合使用计算时间
    :param sf: %Y%m%d%H%M%S
    :param unit: days = None, seconds = None, microseconds = None, milliseconds = None, minutes = None, hours = None, weeks = None
    :return: %Y%m%d%H%M%S 格式化时间
    '''
    arr = None
    exec "arr={'%s':%s}" % (unit, int(num))
    return str((datetime.strptime(log_day, log_day_sf) + timedelta(**arr)).strftime(sf))


def format_time(log_date, sf="%Y%m%d", new_sf="%Y-%m-%d"):
    '''
    格式化时间
    :param log_date: 字符串日期
    :param sf: %Y%m%d%H%M%S
    :param new_sf: %Y%m%d%H%M%S
    :return: 字符串日期
    '''
    return datetime.strptime(log_date, sf).strftime(new_sf)