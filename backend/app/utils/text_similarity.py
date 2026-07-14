"""Lightweight text similarity helpers for advisory search."""
import math
import re
from collections import Counter
from dataclasses import dataclass


TOKEN_PATTERN = re.compile(r"[^\w\s]", re.UNICODE)


def normalize_text(value: str | None) -> str:
    """Normalize text for exact comparisons."""
    if not value:
        return ""
    return " ".join(TOKEN_PATTERN.sub(" ", str(value).lower()).split())


def tokenize_text(value: str | None) -> list[str]:
    """Tokenize text for BM25 scoring."""
    normalized = normalize_text(value)
    return [token for token in normalized.split() if len(token) > 2]


@dataclass(frozen=True)
class SimilarityDocument:
    """Document used by the BM25 similarity scorer."""
    key: str
    text: str


@dataclass(frozen=True)
class SimilarityScore:
    """Score returned for a similarity document."""
    key: str
    score: float


class BM25Similarity:
    """Small BM25-style scorer for in-memory candidate sets."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: list[SimilarityDocument] = []
        self.corpus: list[list[str]] = []
        self.document_lengths: list[int] = []
        self.average_document_length = 0.0
        self.inverse_document_frequency: dict[str, float] = {}

    def fit(self, documents: list[SimilarityDocument]) -> None:
        """Build the scorer index from documents."""
        self.documents = documents
        self.corpus = [tokenize_text(document.text) for document in documents]
        self.document_lengths = [len(tokens) for tokens in self.corpus]
        if not self.corpus:
            self.average_document_length = 0.0
            self.inverse_document_frequency = {}
            return

        self.average_document_length = sum(self.document_lengths) / len(self.document_lengths)
        document_frequencies: Counter[str] = Counter()
        for tokens in self.corpus:
            document_frequencies.update(set(tokens))

        document_count = len(self.corpus)
        self.inverse_document_frequency = {
            token: math.log((document_count - frequency + 0.5) / (frequency + 0.5) + 1)
            for token, frequency in document_frequencies.items()
        }

    def score(self, query: str) -> list[SimilarityScore]:
        """Score indexed documents against a query."""
        query_tokens = tokenize_text(query)
        if not query_tokens or not self.documents or self.average_document_length <= 0:
            return [SimilarityScore(document.key, 0.0) for document in self.documents]

        results: list[SimilarityScore] = []
        for document, tokens, document_length in zip(
            self.documents,
            self.corpus,
            self.document_lengths,
            strict=True,
        ):
            term_frequencies = Counter(tokens)
            score = 0.0
            for token in query_tokens:
                idf = self.inverse_document_frequency.get(token)
                if idf is None:
                    continue
                frequency = term_frequencies[token]
                numerator = frequency * (self.k1 + 1)
                denominator = frequency + self.k1 * (
                    1 - self.b + self.b * document_length / self.average_document_length
                )
                score += idf * numerator / denominator
            results.append(SimilarityScore(document.key, score))

        return sorted(results, key=lambda result: result.score, reverse=True)
