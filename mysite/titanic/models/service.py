from mysite.titanic.models.dataset import Dataset
import pandas as pd
import numpy as np

class Service(object):

    dataset = Dataset()

    def new_model(self, payload) -> object:
        this = self.dataset         # this 가 dataset
        this.context = '../data/'
        this.fname = payload        # payload 는 외부에서 입력된 값 (ex. 파일명, 검색어, 등록값 ... 화면에서 입력하는값)
        return pd.read_csv(this.context + this.fname)