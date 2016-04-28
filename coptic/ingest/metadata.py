import logging
from urllib import request
from bs4 import BeautifulSoup
from texts.models import TextMeta, CorpusMeta

logger = logging.getLogger(__name__)


def collect_corpus_meta(url, corpus):
	logger.info("Fetching and saving corpus metadata")
	def factory(): return CorpusMeta()
	collect(url, factory, corpus.corpus_meta)


def collect_text_meta(url, text):
	logger.info("Fetching and saving text metadata")
	def factory(): return TextMeta()
	collect(url, factory, text.text_meta)


def collect(url, factory, parent):
	for fields in get_selected_annotation_fields(url, ('name', 'value', 'pre', 'corpusname')):
		meta = factory()
		meta.name, meta.value, meta.pre, meta.corpus_name = fields
		meta.save()
		parent.add(meta)


def get_selected_annotation_fields(url, fields):
	'Fetch from the url, and return the requested fields for each annotation found, in a list of lists'
	try:
		markup = request.urlopen(url).read()
		soup = BeautifulSoup(markup)
		if '(1960)' in markup:
			logger.info(markup)
			logger.info(soup)
		fields = [[a.find(field).text for field in fields] for a in soup.find_all("annotation")]
		return fields
	except Exception as e:
		logger.error(e)
		return []
