#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import xlwt


def build_foodlog_xls(l):
    wb = xlwt.Workbook()
    sheet= wb.add_sheet('FoodLog')
    keys= l[0].keys()
    my_list=l
    j=0
    for i in keys:
        sheet.write(0,j, i)
        j+=1
    row=1
    column=0
    j=0
    for i in my_list[0:]:
       values=i.values()
       for j in i.values():
            sheet.write(row,column, str(j))
            column+=1
       column=0 
       row+=1
    return wb