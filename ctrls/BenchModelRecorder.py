#!/bin/python
# -*- coding: utf-8 -*-

import os
import csv
import numpy as np
from settings import *
from datetime import datetime
import matplotlib.pyplot as plt
from os.path import isfile, join, isdir
from scipy.stats.mstats import gmean

class BenchModelRecorder():
    '''Record the BenchMark Result For Model'''
    def __init__(self, model_infos, number):
        self.model_description = model_infos["Model Description"]
        self.number = number
        self.rois = []
        self.filename = join(BENCHMARK_MODEL_PATH, self.model_description + '.csv')
    
    def restart(self):
        f = open(self.filename, 'w')
        cw = csv.writer(f, delimiter = ',')
        cw.writerow(self._getModelHeader())
        f.close()

    def _getModelHeader(self):
        '''輸出至同一個 Model 下紀錄的 Header'''
        header = ["number"]
        for year in range(BENCHMARK_YEAR_START, BENCHMARK_YEAR_END + 1):
            header.append(year)
        header.append('total')
        return header

    def update(self, result, year_day):
        roi = float(result["Asset Series"][-1])/result["Asset Series"][-year_day]
        self.rois.append(str(round((roi-1) * 100, 3)) + '%')

    def updateFinal(self, result):
        self.total_roi = float(result["Asset Series"][-1])/result["Asset Series"][0]

    def record(self):
        f = open(self.filename, 'ab')
        cw = csv.writer(f, delimiter = ',')
        for i in range(BENCHMARK_YEAR_END - BENCHMARK_YEAR_START - len(self.rois) + 1):
            self.rois.insert(0, '0.0%')
        cw.writerow([self.number] + self.rois + [str(round((self.total_roi-1)*100, 3)) + '%'])

        self.rois = []
