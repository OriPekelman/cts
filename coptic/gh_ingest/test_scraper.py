import unittest
from unittest.mock import patch, MagicMock
from django.conf import settings
from django.test import override_settings, TestCase
from gh_ingest.corpus_scraper import (
    CorpusScraper
)
from gh_ingest.scraper_exceptions import  TTDirMissing


class TestCorpusScraper(unittest.TestCase):

    @patch("os.listdir")
    @patch("os.path.isdir")
    @patch("gh_ingest.corpus_scraper.get_setting_and_error_if_none")
    def test_infer_dirs(self, mock_get_setting, mock_isdir, mock_listdir):
        # Setup mock return values
        mock_get_setting.return_value = "/tmp/mock/local/repo/path"
        mock_listdir.return_value = [
            "pseudo.timothy_ANNIS",
            "pseudo.timothy_CONLLU",
            "pseudo.timothy_PAULA",
            "pseudo.timothy_TEI",
        ]
        mock_isdir.side_effect = lambda path: not path.endswith(".zip")

        with patch.object(CorpusScraper, 'clone_repo', return_value=None), \
             patch.object(CorpusScraper, 'ensure_repo', return_value=None):
            with patch.object(CorpusScraper, 'clone_repo', return_value=None), \
                 patch.object(CorpusScraper, 'ensure_repo', return_value=None):
                scraper = CorpusScraper()
        corpus = MagicMock()

        # Call the method
        result = scraper._infer_dirs(corpus, "pseudo-timothy")

        # Check the results
        self.assertEqual(
            result,
            ("pseudo.timothy_TEI", "pseudo.timothy_ANNIS", "pseudo.timothy_PAULA"),
        )  


@override_settings(LOCAL_REPO_PATH="../../corpora")
class TestCorpusScraperWithFiles(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.local_repo_path = settings.LOCAL_REPO_PATH
        cls.scraper = CorpusScraper()

    def test_infer_dirs(self):
        corpus_dirname = "pseudo-timothy"
        corpus = MagicMock()
        result = self.scraper._infer_dirs(corpus, corpus_dirname)
        self.assertEqual(
            result,
            ("pseudo.timothy_TEI", "pseudo.timothy_ANNIS", "pseudo.timothy_PAULA"),
        )

    def test_get_texts(self):
        corpus_dirname = "pseudo-timothy"
        corpus = MagicMock()
        corpus.github_relannis = "pseudo.timothy_ANNIS"
        corpus.annis_corpus_name = "pseudo.timothy"
        texts = self.scraper._get_texts(corpus, corpus_dirname)
        self.assertTrue(len(texts) > 0)

    def test_get_texts_no_texts(self):
        corpus_dirname = "empty-corpus"
        corpus = MagicMock()
        corpus.github_relannis = "empty-corpus_ANNIS"
        corpus.annis_corpus_name = "empty-corpus"
        with self.assertRaises(TTDirMissing):
            self.scraper._get_texts(corpus, corpus_dirname)

    def test_get_texts_missing_dir(self):
        corpus_dirname = "nonexistent-corpus"
        corpus = MagicMock()
        corpus.github_paula = "nonexistent-corpus_PAULA.zip"
        corpus.annis_corpus_name = "nonexistent-corpus"
        with self.assertRaises(TTDirMissing):
            self.scraper._get_texts(corpus, corpus_dirname)

    def test_parse_corpus(self):
        corpus_dirname = "pseudo-timothy"
        transaction = self.scraper.parse_corpus(corpus_dirname)
        self.assertIsNotNone(transaction)
        self.assertTrue(len(transaction._text_pairs) > 0)


if __name__ == "__main__":
    unittest.main()
