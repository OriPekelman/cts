from django.test import TestCase
from texts.models import (
    Corpus, Text, HtmlVisualization, 
    HtmlVisualizationFormat, TextMeta
)
class ModelTests(TestCase):
    def setUp(self):
        self.corpus = Corpus.objects.create(
            title="Test Corpus",
            slug="test-corpus",
            urn_code="test",
            annis_corpus_name="test_corpus",
            github="test/repo"
        )
        
        self.text = Text.objects.create(
            title="Test Text",
            slug="test-text",
            corpus=self.corpus
        )

    def test_html_visualization_format(self):
        """Test HtmlVisualizationFormat model"""
        format = HtmlVisualizationFormat.objects.get(slug="norm")
        self.assertEqual(format.title, "Normalized Text")
        self.assertEqual(format.button_title, "normalized")

    def test_html_visualization(self):
        """Test HtmlVisualization model"""
        format = HtmlVisualizationFormat.objects.get(slug="norm")
        viz = HtmlVisualization.objects.create(
            visualization_format_slug=format.slug,
            html="<p>Test content</p>"
        )
        self.assertEqual(viz.visualization_format.slug, "norm")
        self.assertEqual(viz.html, "<p>Test content</p>")