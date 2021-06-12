from builtins import staticmethod

from mysite.titanic.models.dataset import Dataset
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

class Service(object):

    dataset = Dataset()

    def new_model(self, payload) -> object:
        this = self.dataset         # this 가 dataset
        this.context = '../data/'
        this.fname = payload        # payload 는 외부에서 입력된 값 (ex. 파일명, 검색어, 등록값 ... 화면에서 입력하는값)
        return pd.read_csv(this.context + this.fname)

    # @staticmethod를 붙이지않고 def를 class와 같은 줄에 쓰면 그게 static
    # 개념은 같지만 여기에서는 구분해주기 위해서 @staticmethod를 붙여줘서 사용

    # 데이터 전처리
    @staticmethod
    def create_train(this) -> object:
        return this.train.drop('Survived', axis = 1) # axis 0 가로, 1 세로

    @staticmethod
    def create_label(this) -> object:
        return this.train['Survived']

    @staticmethod
    def drop_feature(this, *feature) -> object:   # 필요없는 데이터는 삭제하는 메소드 ( 하나 이상을 지우기 위해 * 사용)
        for i in feature:
            this.train = this.train.drop([i], axis = 1)
            this.test = this.test.drop([i], axis=1)
            # 학습, 테스트 세트는 항상 동일하게 편집한다.
            return this

    @staticmethod   # static : 공유하지않는 메소드
    def embarked_nominal(this) -> object:  #필요없는 데이터는 위에서 지운 this를 받음
        # na = 빈칸
        this.train = this.train.fillna({'Embarked', 'S'})   # S는 사우스햄튼이라는 곳에서 무질서하게 탑승한것
        this.test = this.test.fillna({'Embarked', 'S'})
        this.train['Embarked'] = this.train['Embarked'].map({'S':1, 'C':2, 'Q':3})
        this.test['Embarked'] = this.test['Embarked'].map({'S': 1, 'C': 2, 'Q': 3})
        return this     # 위의 this와 다른 this (self를 쓰지 않음)

    # Name에서 title을 추출하는 로직
    @staticmethod   # title은 이름 앞에 있는 칭호 (Mr., Major, Don...)
    def title_norminal(this) -> object:
        combine = [this.train, this.test]
        for dataset in combine:
            dataset['Title'] = dataset.Name.str.extract('([A-Za-z]+)\.', expand=False)      # ([A-Za-z]+)\. 는 정규식, 알파벳만 있는 글자 [...]이고, \는 .을 특수기호아닌 자연어로 해석하라.
        for dataset in combine:
            dataset['Title'] = dataset['Title'].replace(
                ['Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Jonkheer', 'Dona'], 'Rare')   # []안에 있는것들은 'Rare'로 통합해라
            dataset['Title'] = dataset['Title'].replace(['Countess', 'Lady', 'Sir'], 'Royal')
            dataset['Title'] = dataset['Title'].replace('Mlle', 'Mr')
            dataset['Title'] = dataset['Title'].replace('Ms', 'Miss')
            dataset['Title'] = dataset['Title'].replace('Mme', 'Rare')
            title_mapping = {'Mr': 1, 'Miss': 2, 'Mrs': 3, 'Master': 4, 'Royal': 5, 'Rare': 6}  # 숫자로 Mapping 해라 / Norminal(순서없는 숫자 표현)
            dataset['Title'] = dataset['Title'].fillna(0)
            dataset['Title'] = dataset['Title'].map(title_mapping)
        return this

    @staticmethod
    def gender_norminal(this) -> object:
        combine = [this.train, this.test]
        gender_mapping = {'male': 0, 'female': 1}
        for i in combine:
            i['Gender'] = i['Sex'].map(gender_mapping)  # i[] 컬럼명 변경
        return this

    # AGE 를 오디널해서 편집하는 구조
    @staticmethod
    def age_ordinal(this) -> object:
        train = this.train
        test = this.test
        for data in train, test:
            data['Age'] = data['Age'].fillna(-0.5)
        bins = [-1, 0, 5, 12, 18, 24, 35, 68, np.inf]
        labels = ['Unknown', 'Baby', 'Child', 'Teenager', 'Student', 'Young Adult', 'Adult', 'Senior']
        age_title_mapping = {'Unknown': 0, 'Baby': 1, 'Child': 2, 'Teenager': 3, 'Student': 4,
                             'Young Adult': 5, 'Adult': 6, 'Senior': 7}
        for data in train, test:
            data['AgeGroup'] = pd.cut(data['Age'], bins=bins, labels=labels)
            data['AgeGroup'] = data['AgeGroup'].map(age_title_mapping)
        return this

    # 요금
    @staticmethod
    def fare_ordinal(this) -> object:
        this.test['FareBand'] = pd.qcut(this.test['Fare'], 4, labels={1,2,3,4})
        this.train['FareBand'] = pd.qcut(this.train['Fare'], 4, labels={1,2,3,4}) # 최고와 최저를 통해 4등분해라

    @staticmethod
    def create_k_fold() -> object:
        return KFold(n_splits=10, shuffle=True, random_state=0) # 트레인데이터를 10등분, 반복출제 허용

    def get_accurcy(self, this):
        score = cross_val_score(RandomForestClassifier(),
                                this.train,
                                this.label,
                                cv=self.create_k_fold(),
                                n_jobs=1,
                                scoring='accuracy')   # RandomForestClassifier 는 엔진
        return round(np.mean(score)*100, 2)     # 소수점 두자리까지 출력


