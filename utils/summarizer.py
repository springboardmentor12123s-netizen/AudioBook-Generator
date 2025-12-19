import nltk                                             # Natural Language Toolkit for text processing
from sumy.parsers.plaintext import PlaintextParser      # Parser for plain text
from sumy.nlp.tokenizers import Tokenizer               # Tokenizer for splitting text into sentences
from sumy.summarizers.lex_rank import LexRankSummarizer # LexRank summarization algorithm

# Auto-download NLTK tokenizers if missing
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

def summarize_text(text, sentence_count=3):             
    """
    Summarize long text using LexRank algorithm.
    Returns a short clean summary.
    """
    if not text or len(text.strip()) == 0:
        return ""

    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, sentence_count)

        return " ".join([str(sentence) for sentence in summary])

    except Exception as e:
        print(f"Summarization error: {e}")
        return text    # fallback → return original text

