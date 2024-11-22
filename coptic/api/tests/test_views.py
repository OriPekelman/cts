from django.test import TestCase, Client
from django.urls import reverse
from texts.models import Corpus, Text, HtmlVisualization, HtmlVisualizationFormat
import json

class APIViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test corpus
        self.corpus = Corpus.objects.create(
            title="Test Corpus",
            slug="test-corpus",
            urn_code="test",
            annis_corpus_name="test_corpus",
            github="test/repo"
        )
        
        # Create test text
        self.text = Text.objects.create(
            title="Test Text",
            slug="test-text",
            corpus=self.corpus
        )
        
        # Create test visualization
        self.viz_format = HtmlVisualizationFormat.objects.get(slug="norm")
        self.visualization = HtmlVisualization.objects.create(
            visualization_format_slug=self.viz_format.slug,
            html="<p>Test content</p>"
        )
        self.text.html_visualizations.add(self.visualization)

    def test_corpus_list(self):
        """Test the corpus list endpoint"""
        response = self.client.get(reverse('api:corpus-list'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('corpora', data)
        self.assertEqual(len(data['corpora']), 1)
        self.assertEqual(data['corpora'][0]['slug'], 'test-corpus')

    def test_text_list(self):
        """Test the text list endpoint"""
        response = self.client.get(reverse('api:text-list', kwargs={'corpus_slug': 'test-corpus'}))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('texts', data)
        self.assertEqual(len(data['texts']), 1)
        self.assertEqual(data['texts'][0]['slug'], 'test-text')

    def test_text_detail(self):
        """Test the text detail endpoint"""
        response = self.client.get(
            reverse('api:text-detail', 
                   kwargs={'corpus_slug': 'test-corpus', 'text_slug': 'test-text'})
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Test Text')
        self.assertEqual(data['slug'], 'test-text')

    def test_visualization(self):
        """Test the visualization endpoint"""
        response = self.client.get(
            reverse('api:visualization', 
                   kwargs={
                       'corpus_slug': 'test-corpus',
                       'text_slug': 'test-text',
                       'format_slug': 'norm'
                   })
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '<p>Test content</p>')