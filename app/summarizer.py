import nltk
from newspaper import Article

from app.models.tortoise import TextSummary


async def generate_summary(id: int, url: str):
    article = Article(url)
    article.download()
    article.parse()

    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")
    finally:
        article.nlp()

    summary = article.summary

    await TextSummary.filter(id=id).update(summary=summary)
