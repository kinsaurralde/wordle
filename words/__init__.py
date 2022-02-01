from .wordbank import WordBank
from .wordlists import answers, allwords



class AnswerBank(WordBank):
    def __init__(self) -> None:
        super().__init__(answers)

class FullWordBank(WordBank):
    def __init__(self) -> None:
        super().__init__(allwords + answers)
        # super().__init__(['bright', 'punch', 'crawl', 'light'])
        # super().__init__(['lbraw', 'brain', 'noise', 'zebra', 'brawl'])
