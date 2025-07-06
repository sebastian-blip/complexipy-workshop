"""
Text Analyzer - A simple module for analyzing text content
This module demonstrates moderate complexity suitable for refactoring.
"""

import re
from collections import Counter
from typing import Dict


def analyze_text(text: str, options: Dict | None = None) -> Dict:
    """
    Analyze text and return various statistics.

    Args:
        text: The text to analyze
        options: Configuration options for analysis

    Returns:
        Dictionary containing analysis results
    """
    if not text:
        return {"error": "Text cannot be empty"}

    if options is None:
        options = {}

    result = {
        "basic_stats": {},
        "word_analysis": {},
        "character_analysis": {},
        "readability": {},
    }

    result["basic_stats"]["total_characters"] = len(text)
    result["basic_stats"]["total_characters_no_spaces"] = len(
        text.replace(" ", "")
    )

    sentences = re.split(r"[.!?]+", text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    result["basic_stats"]["total_sentences"] = len(sentences)

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    result["basic_stats"]["total_paragraphs"] = len(paragraphs)

    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    result["word_analysis"]["total_words"] = len(words)

    if len(words) > 0:
        word_counts = Counter(words)

        top_count = 5
        if options and "top_words_count" in options:
            if (
                isinstance(options["top_words_count"], int)
                and options["top_words_count"] > 0
            ):
                top_count = options["top_words_count"]

        result["word_analysis"]["most_common_words"] = word_counts.most_common(
            top_count
        )

        word_lengths = [len(word) for word in words]
        result["word_analysis"]["average_word_length"] = sum(
            word_lengths
        ) / len(word_lengths)
        result["word_analysis"]["longest_word"] = max(words, key=len)
        result["word_analysis"]["shortest_word"] = min(words, key=len)

        unique_words = len(set(words))
        result["word_analysis"]["unique_words"] = unique_words
        result["word_analysis"]["lexical_diversity"] = unique_words / len(words)

    letters = [c for c in text.lower() if c.isalpha()]
    if letters:
        letter_counter = Counter(letters)
        result["character_analysis"]["most_common_letters"] = (
            letter_counter.most_common(5)
        )

    result["character_analysis"]["uppercase_count"] = sum(
        1 for c in text if c.isupper()
    )
    result["character_analysis"]["lowercase_count"] = sum(
        1 for c in text if c.islower()
    )
    result["character_analysis"]["digit_count"] = sum(
        1 for c in text if c.isdigit()
    )
    result["character_analysis"]["punctuation_count"] = sum(
        1 for c in text if c in ".,!?;:"
    )
    result["character_analysis"]["whitespace_count"] = sum(
        1 for c in text if c.isspace()
    )

    if (
        result["basic_stats"]["total_sentences"] > 0
        and result["word_analysis"]["total_words"] > 0
    ):
        avg_words_per_sentence = (
            result["word_analysis"]["total_words"]
            / result["basic_stats"]["total_sentences"]
        )
        result["readability"]["average_words_per_sentence"] = (
            avg_words_per_sentence
        )

        avg_sentence_length = avg_words_per_sentence
        avg_syllables = result["word_analysis"]["average_word_length"] * 0.7

        readability_score = (
            206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables)
        )

        if readability_score > 100:
            readability_score = 100
        elif readability_score < 0:
            readability_score = 0

        result["readability"]["flesch_score"] = round(readability_score, 2)

        if readability_score >= 90:
            result["readability"]["difficulty_level"] = "Very Easy"
        elif readability_score >= 80:
            result["readability"]["difficulty_level"] = "Easy"
        elif readability_score >= 70:
            result["readability"]["difficulty_level"] = "Fairly Easy"
        elif readability_score >= 60:
            result["readability"]["difficulty_level"] = "Standard"
        elif readability_score >= 50:
            result["readability"]["difficulty_level"] = "Fairly Difficult"
        elif readability_score >= 30:
            result["readability"]["difficulty_level"] = "Difficult"
        else:
            result["readability"]["difficulty_level"] = "Very Difficult"

    if (
        options
        and "include_language_detection" in options
        and options["include_language_detection"]
    ):
        english_words = [
            "the",
            "and",
            "to",
            "of",
            "a",
            "in",
            "is",
            "it",
            "you",
            "that",
        ]
        spanish_words = [
            "el",
            "la",
            "de",
            "que",
            "y",
            "a",
            "en",
            "un",
            "es",
            "se",
        ]

        english_count = sum(1 for word in words if word in english_words)
        spanish_count = sum(1 for word in words if word in spanish_words)

        if english_count > spanish_count:
            result["language_detection"] = {
                "detected_language": "English",
                "confidence": "Low",
            }
        elif spanish_count > english_count:
            result["language_detection"] = {
                "detected_language": "Spanish",
                "confidence": "Low",
            }
        else:
            result["language_detection"] = {
                "detected_language": "Unknown",
                "confidence": "Very Low",
            }

    if (
        options
        and "include_sentiment" in options
        and options["include_sentiment"]
    ):
        positive_words = [
            "good",
            "great",
            "excellent",
            "amazing",
            "wonderful",
            "fantastic",
            "love",
            "happy",
        ]
        negative_words = [
            "bad",
            "terrible",
            "awful",
            "hate",
            "sad",
            "angry",
            "disappointed",
            "horrible",
        ]

        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)

        if positive_count > negative_count:
            sentiment = "Positive"
        elif negative_count > positive_count:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        result["sentiment_analysis"] = {
            "sentiment": sentiment,
            "positive_words_count": positive_count,
            "negative_words_count": negative_count,
        }

    return result


def format_analysis_report(analysis_result: Dict) -> str:
    """
    Format the analysis result into a readable report.

    This function also has some complexity that can be refactored.
    """
    if "error" in analysis_result:
        return f"Error: {analysis_result['error']}"

    report = []
    report.append("=== TEXT ANALYSIS REPORT ===\n")

    if "basic_stats" in analysis_result:
        report.append("📊 BASIC STATISTICS:")
        stats = analysis_result["basic_stats"]
        report.append(
            f"  • Total Characters: {stats.get('total_characters', 0)}"
        )
        report.append(
            f"  • Characters (no spaces): {stats.get('total_characters_no_spaces', 0)}"
        )
        report.append(
            f"  • Total Words: {analysis_result.get('word_analysis', {}).get('total_words', 0)}"
        )
        report.append(f"  • Total Sentences: {stats.get('total_sentences', 0)}")
        report.append(
            f"  • Total Paragraphs: {stats.get('total_paragraphs', 0)}"
        )
        report.append("")

    if "word_analysis" in analysis_result:
        report.append("📝 WORD ANALYSIS:")
        word_stats = analysis_result["word_analysis"]

        if "average_word_length" in word_stats:
            report.append(
                f"  • Average Word Length: {word_stats['average_word_length']:.2f}"
            )

        if "longest_word" in word_stats:
            report.append(f"  • Longest Word: '{word_stats['longest_word']}'")

        if "shortest_word" in word_stats:
            report.append(f"  • Shortest Word: '{word_stats['shortest_word']}'")

        if "lexical_diversity" in word_stats:
            report.append(
                f"  • Lexical Diversity: {word_stats['lexical_diversity']:.2f}"
            )

        if "most_common_words" in word_stats:
            report.append("  • Most Common Words:")
            for word, count in word_stats["most_common_words"]:
                report.append(f"    - '{word}': {count}")

        report.append("")

    if "character_analysis" in analysis_result:
        report.append("🔤 CHARACTER ANALYSIS:")
        char_stats = analysis_result["character_analysis"]

        for key, value in char_stats.items():
            if key == "most_common_letters":
                report.append("  • Most Common Letters:")
                for letter, count in value:
                    report.append(f"    - '{letter}': {count}")
            else:
                readable_key = key.replace("_", " ").title()
                report.append(f"  • {readable_key}: {value}")

        report.append("")

    if "readability" in analysis_result:
        report.append("📖 READABILITY:")
        readability = analysis_result["readability"]

        for key, value in readability.items():
            readable_key = key.replace("_", " ").title()
            report.append(f"  • {readable_key}: {value}")

        report.append("")

    if "language_detection" in analysis_result:
        report.append("🌐 LANGUAGE DETECTION:")
        lang_info = analysis_result["language_detection"]
        report.append(
            f"  • Detected Language: {lang_info['detected_language']}"
        )
        report.append(f"  • Confidence: {lang_info['confidence']}")
        report.append("")

    if "sentiment_analysis" in analysis_result:
        report.append("😊 SENTIMENT ANALYSIS:")
        sentiment = analysis_result["sentiment_analysis"]
        report.append(f"  • Overall Sentiment: {sentiment['sentiment']}")
        report.append(
            f"  • Positive Words: {sentiment['positive_words_count']}"
        )
        report.append(
            f"  • Negative Words: {sentiment['negative_words_count']}"
        )
        report.append("")

    return "\n".join(report)


if __name__ == "__main__":
    sample_text = """
    Python is a wonderful programming language. It's easy to learn and very powerful!
    Many developers love Python because of its simplicity and readability.

    You can build web applications, data analysis tools, and even machine learning models.
    The community is amazing and very helpful.
    """

    result = analyze_text(sample_text)
    print(format_analysis_report(result))

    advanced_options = {
        "top_words_count": 3,
        "include_language_detection": True,
        "include_sentiment": True,
    }

    print("\n" + "=" * 50 + "\n")
    print("ADVANCED ANALYSIS:\n")

    advanced_result = analyze_text(sample_text, advanced_options)
    print(format_analysis_report(advanced_result))
