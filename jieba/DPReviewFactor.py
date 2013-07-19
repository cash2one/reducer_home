
import jieba

class ReviewHandler:

    def __init__(self):

        self.dictfile = []
        self.model = []
        self.reviewfile = None
        self.result = {}
        self.shopDish = {}

    def LoadFile(self, dict):
        for file in dict:
            jieba.load_userdict(file)

    def LoadShopDish(self, filemane):
        self.shopDish = {}

    def LoadModel(self):
        ' '

    def excute(self,file):
        ''

    def Show(self):
        ''

