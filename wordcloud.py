import matplotlib.pyplot as plt
import random
from collections import Counter, defaultdict


class Word:
    """
    Represents the properties of each word on the graph.
    """

    def __init__(self):
        self.x_loc = None
        self.y_loc = None
        self.count_ = 0
        self.size = 0

    def get_location(self):
        """
        Get the location of the word.
        """
        if self.x_loc and self.y_loc:
            return (self.x_loc, self.y_loc)
        return None


class WordCloud:
    """
    Manages the words on the word cloud and plots it.
    """

    def __init__(self):
        self.words = defaultdict(Word)
        self.word_cloud = plt.figure()
        plt.ion()

    def update_words(self, words):
        c = Counter(words.split())
        for word, count_ in c.items():
            word = word.lower()
            self.words[word].count_ += 1
            self.words[word].size += count_ * 10

    def draw_cloud(self):
        for text, properties in self.words.items():
            if not properties.get_location():
                # randomize the location of the word
                properties.x_loc = random.uniform(0.0, 1.0)
                properties.y_loc = random.uniform(0.0, 1.0)
            else:
                self.word_cloud.text(
                    properties.x_loc, properties.y_loc, text, size=properties.size
                )

        self.word_cloud.show()
        plt.pause(0.1)

    def __str__(self):
        res = ""
        for text, properties in self.words.items():
            res += f"{text}: {properties.count_}\n"

        return res
