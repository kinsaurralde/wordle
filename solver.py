import time
import threading
import multiprocessing
from words import AnswerBank, FullWordBank
from guesstree import GuessTreeNode

WORD_LENGTH = 5
MAX_GUESSES = 6
GREY_SCORE = -3
YELLOW_SCORE = -1
GREEN_SCORE = -0

START_SCORE = -1 * GREY_SCORE * WORD_LENGTH * MAX_GUESSES

class Solver:
    def __init__(self) -> None:
        self.calls = 0
        self.guesstree = GuessTreeNode()
        self.answers = AnswerBank()
        self.allwords = FullWordBank()

    # def getScore(self, word, answer):
    #     score = 0
    #     for i, char in enumerate(word):
    #         if char == answer[i]:
    #             score += GREEN_SCORE
    #         elif char in answer:
    #             score += YELLOW_SCORE
    #         else:
    #             score += GREY_SCORE
    #     # print(f"Score of {word} = {score}")
    #     return score

    # def getPattern(self, word, answer):
    #     pattern = [None] * WORD_LENGTH
    #     if len(word) != WORD_LENGTH or len(answer) != WORD_LENGTH:
    #         return pattern
    #     for i in range(WORD_LENGTH):
    #         if word[i] == answer[i]:
    #             pattern[i] = word[i]
    #     return pattern


    # def getBannedChars(self, guess, answer):
    #     result = []
    #     for char in guess:
    #         if char not in answer:
    #             result.append(char)
    #     return result

    # def getBestGuess(self, answer, current_guess_node, guess_number, guess_list):
    #     self.calls += 1

    #     current_guess = current_guess_node.getWord()
    #     current_score = self.getScore(current_guess, answer)
    #     current_pattern = self.getPattern(current_guess, answer)
    #     current_score_response = (current_guess, self.getScore(current_guess, answer))
    #     if guess_number >= MAX_GUESSES or current_guess == answer:
    #         return current_score_response
    #     scores = {}
    #     word_list = self.allwords.filter(current_pattern, self.getBannedChars(current_guess, answer))
    #     for word in word_list:
    #         if word == current_guess or word in guess_list:
    #             continue
    #         node = GuessTreeNode(word, self.getScore(word, answer))
    #         current_guess_node.addChild(node)
    #         guess, score = self.getBestGuess(answer, node, guess_number + 1, guess_list + [word])
    #         score += current_score
    #         if score not in scores:
    #             scores[score] = []
    #         scores[score].append(word)
    #     if 0 in scores:
    #         scores.pop(0)
    #     if len(scores) == 0:
    #         return current_score_response
    #     best_score = max(scores)
    #     best_guess = scores[best_score][0]
    #     return (best_guess, best_score)

    # def run(self, answer):
    #     self.calls = 0
    #     self.guesstree = GuessTreeNode('', 0)
    #     start_time = time.time()
    #     solution = self.getBestGuess(answer, self.guesstree, 0, [])
    #     end_time = time.time()
    #     print(f"Found solution: {solution} in {self.calls} calls and {int((end_time - start_time) * 1000)}ms")
    #     print(f"Solution Score: {self.guesstree.calculateBestScore()}")

    # def runAllAnswers(self):
    #     self.calls = 0
    #     self.guesstree = GuessTreeNode('', 0)
    #     solutions = {}
    #     start_time = time.time()
    #     for answer in self.answers.getList():
    #         solutions[answer] = self.getBestGuess(answer, self.guesstree, 0, [])
    #     end_time = time.time()
    #     print(f"Found solution: {solutions} in {self.calls} calls and {int((end_time - start_time) * 1000)}ms")

    def evaluateGuess(self, answer, guess, hints):
        if len(answer) != WORD_LENGTH or len(guess) != WORD_LENGTH:
            return
        for i in range(WORD_LENGTH):
            guess_char = guess[i]
            answer_char = answer[i]
            if guess_char == answer_char:
                hints['green'][i] = guess_char
                hints['yellow'].append(guess_char)
            elif guess_char in answer:
                hints['yellow'].append(guess_char)
            else:
                hints['grey'].append(guess_char)
        return

        

    def getPossibleSolutionCount(self, answer, guess, possible_answers):
        hints = {
            'green': [None] * WORD_LENGTH,
            'yellow': [],
            'grey': []
        }
        self.evaluateGuess(answer, guess, hints)
        filtered = self.filter(possible_answers, hints)
        # possible_guesses = self.filter(possible_guesses, hints)
        # guess = possible_answers[0]
        # print(f"[{guess_count}]: {len(possible_answers)}\t\t{len(possible_guesses)}")
        return len(filtered)

    def testAnswer(self, answer):
        start_time = time.time()
        possible_answers = self.answers.getList()
        possible_guesses = self.allwords.getList()
        # print(f"Start with {len(possible_answers)} possible answers and {len(possible_guesses)} possible guesses")
        guess_possible_counts = []
        for guess in possible_guesses:
            possible_count = self.getPossibleSolutionCount(answer, guess, possible_answers)
            guess_possible_counts.append(Guess(guess, possible_count))
        end_time = time.time()
        lowest_possible = min(guess_possible_counts)
        self.done_count.set(self.done_count.get() + 1)
        print(f"[{self.done_count.get()}/{self.answers_count}]: Found {lowest_possible} in {int((end_time - start_time) * 1000) / 1000} seconds")
        return lowest_possible

    def testAnswerThread(self, answer):
        lowest_possible = self.testAnswer(answer)
        word = lowest_possible.word
        # points_lock.acquire()
        if word not in self.points:
            self.points[word] = 0
        self.points[word] += 1
        # points_lock.release()

    def testAll(self):
        start_time = time.time()
        self.points = multiprocessing.Manager().dict()
        self.done_count = multiprocessing.Manager().Value('i', 0)

        answers_list = self.answers.getList()[:5]
        self.answers_count = len(answers_list)
        proccess_count = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(proccess_count)
        print(f"Starting Pool with {proccess_count} processes")
        pool.map(self.testAnswerThread, (answers_list))
        end_time = time.time()
        print(f"Completed in {int((end_time - start_time) * 1000) / 1000} seconds")
        
        best = max(self.points.items(), key=lambda x:x[1])
        print(f"{best} wins")

        return self.points
            

    def filter(self, word_list, hints):
        result = []
        for word in word_list:
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

class Guess:
    def __init__(self, word, possible_solutions) -> None:
        self.word = word
        self.possible_solutions = possible_solutions
        
    def __eq__(self, o: object) -> bool:
        return self.possible_solutions == o.possible_solutions

    def __gt__(self, o: object) -> bool:
        return self.possible_solutions > o.possible_solutions
    
    def __ge__(self, o: object) -> bool:
        return self.possible_solutions >= o.possible_solutions

    def __lt__(self, o: object) -> bool:
        return self.possible_solutions < o.possible_solutions
    
    def __le__(self, o: object) -> bool:
        return self.possible_solutions <= o.possible_solutions

    def __repr__(self) -> str:
        return f"{self.word} has {self.possible_solutions} possible solutions"
    

s = Solver()