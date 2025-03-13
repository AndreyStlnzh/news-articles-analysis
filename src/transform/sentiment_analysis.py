import nltk
import pandas as pd

from matplotlib import pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer


nltk.download('vader_lexicon')


class SentimentAnalysis:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()


    def process_sentiment_analysis(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """Определение тональности текста

        Args:
            data (pd.DataFrame): датафрейм

        Returns:
            pd.DataFrame: датафрейм с новой колонкой 'sentiment'
        """
        data["sentiment"] = data["description"].apply(self.get_text_sentiment)

        return data

    def get_text_sentiment(
        self,
        text: str
    ) -> str:
        """Функция определения тональности текста

        Args:
            text (str): исходный текст

        Returns:
            str: тональность (neg, neu, pos, compound)
        """
        
        sentiment_scores = self.sia.polarity_scores(text)
        return max(sentiment_scores, key=sentiment_scores.get)
    

    def draw_sentiment_bar(
        self,
        data: pd.DataFrame,
    ) -> None:
        """Фунция отображения графика"""
        sentiment_counts = data["sentiment"].value_counts()

        plt.bar(sentiment_counts.index, sentiment_counts.values, color=["blue", "gray", "red", "green"])
        plt.title('Распределение тональности текстов')
        plt.xlabel('Тональность')
        plt.ylabel('Частота')
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.show()
