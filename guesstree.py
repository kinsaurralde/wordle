class GuessTree:
    def __init__(self) -> None:
        self.root = GuessTreeNode('', 0)


class GuessTreeNode:
    def __init__(self, word='', word_score=0) -> None:
        self.word = word
        self.word_score = word_score
        self.children = []

    def getWord(self):
        return self.word

    def addChild(self, child_node):
        self.children.append(child_node)

    def calculateBestScore(self):
        best_score = 0
        if len(self.children) == 0:
            return self.word_score
        for child_node in self.children:
            child_score = child_node.calculateBestScore()
            if best_score == 0 or child_score > best_score and child_score != 0:
                best_score = child_score
        return self.word_score + best_score

    def __eq__(self, o):
        return self.calculateBestScore() == o.calculateBestScore()

    def __lt__(self, o):
        return self.calculateBestScore() < o.calculateBestScore()

    def __le__(self, o):
        return self.calculateBestScore() <= o.calculateBestScore()

    def __gt__(self, o):
        return self.calculateBestScore() > o.calculateBestScore()

    def __ge__(self, o):
        return self.calculateBestScore() >= o.calculateBestScore()

    def __repr__(self) -> str:
        return f"{self.word}: {self.word_score} {self.calculateBestScore()}\t"
