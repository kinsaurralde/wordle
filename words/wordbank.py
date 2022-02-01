class WordBank:
    def __init__(self, words) -> None:
        self.words = words
        print(f"Created wordbank with {len(self.words)} words")

    def getList(self):
        return self.words

    def filter(self, pattern, excluded_chars):
        result = []
        pattern_length = len(pattern)
        if pattern_length != 5:
            print(f"Pattern length {pattern_length} != 5")
            return result
        for word in self.words:
            include = True
            for i, char in enumerate(word):
                if char in excluded_chars or (pattern[i] is not None and char != pattern[i]):
                    include = False
                    break
            if include:
                result.append(word)
        return result

    def filter2(self, hints):
        result = []
        for word in self.words:
            include = True
            for i, char in enumerate(word):
                if char in hints['grey']:
                    include = False
                    break
                if hints['green'][i] is not None:
                    if char != hints['green'][i]:
                        include = False
                        break
            for char in hints['yellow']:
                if char not in word:
                    include = False
                    break
            if include:
                result.append(word)
        return result

