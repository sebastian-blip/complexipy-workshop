"""
Unit tests for text analyzer module
"""

import pytest
from text_analyzer.src.text_analyzer import (
    analyze_text,
    format_analysis_report,
)


@pytest.fixture
def simple_text():
    """Simple text fixture for testing"""
    return "Hello world. This is a test."


@pytest.fixture
def complex_text():
    """Complex text fixture for testing"""
    return """
        Python is a wonderful programming language. It's easy to learn and very powerful!
        Many developers love Python because of its simplicity and readability.

        You can build web applications, data analysis tools, and even machine learning models.
        The community is amazing and very helpful.
        """


class TestTextAnalyzer:
    """Test cases for text analyzer functions"""

    def test_empty_text(self):
        """Test behavior with empty text"""
        result = analyze_text("")
        assert "error" in result
        assert result["error"] == "Text cannot be empty"

    def test_none_text(self):
        """Test behavior with None text"""
        result = analyze_text(None)
        assert "error" in result

    def test_basic_statistics(self, simple_text):
        """Test basic text statistics"""
        result = analyze_text(simple_text)

        # Check structure
        assert "basic_stats" in result
        assert "word_analysis" in result
        assert "character_analysis" in result
        assert "readability" in result

        # Check basic stats
        basic_stats = result["basic_stats"]
        assert basic_stats["total_characters"] == len(simple_text)
        assert basic_stats["total_sentences"] == 2
        assert basic_stats["total_paragraphs"] == 1

    def test_word_analysis(self, simple_text):
        """Test word analysis functionality"""
        result = analyze_text(simple_text)
        word_analysis = result["word_analysis"]

        assert word_analysis["total_words"] == 6
        assert "most_common_words" in word_analysis
        assert "average_word_length" in word_analysis
        assert "longest_word" in word_analysis
        assert "shortest_word" in word_analysis
        assert "lexical_diversity" in word_analysis

        # Check that lexical diversity is between 0 and 1
        assert word_analysis["lexical_diversity"] >= 0
        assert word_analysis["lexical_diversity"] <= 1

    def test_character_analysis(self, simple_text):
        """Test character analysis functionality"""
        result = analyze_text(simple_text)
        char_analysis = result["character_analysis"]

        assert "uppercase_count" in char_analysis
        assert "lowercase_count" in char_analysis
        assert "digit_count" in char_analysis
        assert "punctuation_count" in char_analysis
        assert "whitespace_count" in char_analysis

        # Check that counts are non-negative
        for key, value in char_analysis.items():
            if key != "most_common_letters":
                assert value >= 0

    def test_readability_analysis(self, simple_text):
        """Test readability analysis"""
        result = analyze_text(simple_text)
        readability = result["readability"]

        assert "average_words_per_sentence" in readability
        assert "flesch_score" in readability
        assert "difficulty_level" in readability

        # Check that Flesch score is between 0 and 100
        assert readability["flesch_score"] >= 0
        assert readability["flesch_score"] <= 100

    def test_options_top_words_count(self, complex_text):
        """Test custom top words count option"""
        options = {"top_words_count": 3}
        result = analyze_text(complex_text, options)

        most_common = result["word_analysis"]["most_common_words"]
        assert len(most_common) == 3

    def test_options_language_detection(self, complex_text):
        """Test language detection option"""
        options = {"include_language_detection": True}
        result = analyze_text(complex_text, options)

        assert "language_detection" in result
        lang_info = result["language_detection"]
        assert "detected_language" in lang_info
        assert "confidence" in lang_info

    def test_options_sentiment_analysis(self):
        """Test sentiment analysis option"""
        positive_text = "This is wonderful! I love it. Amazing and fantastic!"
        negative_text = "This is terrible. I hate it. Bad and awful!"

        options = {"include_sentiment": True}

        # Test positive sentiment
        result = analyze_text(positive_text, options)
        assert "sentiment_analysis" in result
        assert result["sentiment_analysis"]["sentiment"] == "Positive"

        # Test negative sentiment
        result = analyze_text(negative_text, options)
        assert result["sentiment_analysis"]["sentiment"] == "Negative"

    def test_format_analysis_report(self, simple_text):
        """Test report formatting"""
        result = analyze_text(simple_text)
        report = format_analysis_report(result)

        # Check that report is a string
        assert isinstance(report, str)

        # Check that it contains expected sections
        assert "TEXT ANALYSIS REPORT" in report
        assert "BASIC STATISTICS" in report
        assert "WORD ANALYSIS" in report
        assert "CHARACTER ANALYSIS" in report
        assert "READABILITY" in report

    def test_format_error_report(self):
        """Test formatting of error results"""
        error_result = {"error": "Test error"}
        report = format_analysis_report(error_result)

        assert "Error: Test error" in report

    def test_edge_cases(self):
        """Test edge cases"""
        # Single word
        result = analyze_text("Hello")
        assert result["word_analysis"]["total_words"] == 1
        assert result["basic_stats"]["total_sentences"] == 1

        # Numbers and special characters
        result = analyze_text("Test123 with numbers! And punctuation?")
        assert result["character_analysis"]["digit_count"] > 0
        assert result["character_analysis"]["punctuation_count"] > 0

    def test_invalid_options(self, simple_text):
        """Test behavior with invalid options"""
        # Invalid top_words_count
        options = {"top_words_count": -1}
        result = analyze_text(simple_text, options)

        # Should fall back to default (5)
        most_common = result["word_analysis"]["most_common_words"]
        assert len(most_common) <= 5

        # Non-integer top_words_count
        options = {"top_words_count": "invalid"}
        result = analyze_text(simple_text, options)

        # Should fall back to default (5)
        most_common = result["word_analysis"]["most_common_words"]
        assert len(most_common) <= 5


class TestTextAnalyzerIntegration:
    """Integration tests for the text analyzer"""

    def test_full_analysis_workflow(self):
        """Test the complete analysis workflow"""
        text = """
        The quick brown fox jumps over the lazy dog.
        This sentence contains every letter of the alphabet!

        Python programming is fun and rewarding.
        """

        options = {
            "top_words_count": 5,
            "include_language_detection": True,
            "include_sentiment": True,
        }

        result = analyze_text(text, options)

        expected_sections = [
            "basic_stats",
            "word_analysis",
            "character_analysis",
            "readability",
            "language_detection",
            "sentiment_analysis",
        ]

        for section in expected_sections:
            assert section in result

        report = format_analysis_report(result)

        expected_in_report = [
            "BASIC STATISTICS",
            "WORD ANALYSIS",
            "CHARACTER ANALYSIS",
            "READABILITY",
            "LANGUAGE DETECTION",
            "SENTIMENT ANALYSIS",
        ]

        for section in expected_in_report:
            assert section in report

    def test_different_text_types(self):
        """Test with different types of text"""
        test_cases = [
            ("Short.", {"basic_stats": {"total_sentences": 1}}),
            (
                "Multiple sentences. Here's another! And a question?",
                {"basic_stats": {"total_sentences": 3}},
            ),
            (
                "Paragraph one.\n\nParagraph two.",
                {"basic_stats": {"total_paragraphs": 2}},
            ),
            ("UPPERCASE TEXT", {"character_analysis": {"uppercase_count": 13}}),
            ("lowercase text", {"character_analysis": {"lowercase_count": 13}}),
        ]

        for text, expectations in test_cases:
            result = analyze_text(text)

            for section, expected_values in expectations.items():
                for key, expected_value in expected_values.items():
                    assert result[section][key] == expected_value
