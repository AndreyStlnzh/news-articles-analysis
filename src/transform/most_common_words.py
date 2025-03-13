import pandas as pd

from typing import Tuple
from collections import Counter
from matplotlib import pyplot as plt


class MostCommonWords:
    def __init__(self):
        pass


    def find_most_common_words(
        self,
        data: pd.DataFrame,
        n: int=10
    ) -> Tuple[list, list]:
        """Функция нахождения самых частых слов

        Args:
            data (pd.DataFrame): датафрейм
            n (int, optional): количество самых частых слов. Defaults to 10.

        Returns:
            Tuple[list, list]: список слов и список их частот
        """
        all_words = [word for sent in data["content"] for word in sent.split()]

        word_count = Counter(all_words)
        most_common = word_count.most_common(n)
        words, count = zip(*most_common)

        return words, count
    
    def draw_bar(
        self,
        words: list, 
        count: list
    ) -> None:
        """Фунция отображения графика

        Args:
            words (list): список слов
            count (list): частотность каждого слова
        """
        plt.bar(words, count)
        plt.title('Топ-10 самых частых слов')
        plt.xlabel('Слово')
        plt.ylabel('Частота')
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.show()