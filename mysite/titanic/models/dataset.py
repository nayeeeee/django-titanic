from dataclasses import dataclass

@dataclass  #데코레이터?
class Dataset(object):

    context: str
    fname: str
    train: object   # train.csv 가 DF로 전환된 객체
    test: object    # test.csv 가 DF로 전환된 객체
    id: str         # 승객ID로 문제가 된다.
    label: str      # 승객ID에 따른 생존여부로 답이 된다.

    # 데이터를 읽고(getter = 프로퍼티) / 쓰기(setter) 기능을 추가한다.

    @property
    def context(self) -> str : return self._context

    @context.setter
    def context(self, context): self._context = context

    @property
    def fname(self) -> str: return self.fname

    @fname.setter
    def fname(self, fname): self.fname = fname

    @property
    def train(self) -> str: return self.train

    @train.setter
    def train(self, train): self.train = train

    @property
    def test(self) -> str: return self.test

    @test.setter
    def test(self, test): self.test = test

    @property
    def id(self) -> str: return self.id

    @id.setter
    def id(self, id): self.id = id

    @property
    def label(self) -> str: return self.label

    @label.setter
    def label(self, label): self.label = label

