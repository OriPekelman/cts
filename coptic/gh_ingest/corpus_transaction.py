from collections import defaultdict
from django.db import transaction

from texts.models import (
    HtmlVisualizationFormat,
)
from .scraper_exceptions import *

class CorpusTransaction:
    """Keeps track of every object that needs to be added to the SQL database for a given corpus,
    and atomically saves all of them."""

    def __init__(self, corpus_name, corpus):
        self.corpus_name = corpus_name
        self._corpus = corpus
        self._text_pairs = []
        self._vis_formats = []
        self._vises = []
        self._to_delete = []

    def add_objs_to_be_deleted(self, objs):
        self._to_delete = objs

    def add_text(self, text_pair):
        self._text_pairs.append(text_pair)

    def add_vis_formats(self, formats):
        self._vis_formats = formats

    def add_vis(self, text_and_vis):
        self._vises.append(text_and_vis)

    def sort_texts(self, text_next, text_prev, text_urn):
        """
        Sorts texts based on next and previous metadata. Only actually changes their order if the next and previous
        attributes form an unbroken chain within the texts, otherwise does nothing.

        :param text_next: dict: text title -> text urn
        :param text_prev: dict: text title -> text urn
        :param text_urn: dict: text title -> text urn
        """

        class Node:
            def __init__(self, title, orig_i):
                self.title = title
                self.orig_i = orig_i
                self.prev = None
                self.next = None

            def __str__(self):
                return f"<{self.title}, {self.orig_i}>"

            def __repr__(self):
                return self.__str__()

        urn_to_node = defaultdict(lambda: None)
        nodes = []
        for i, (text, _) in enumerate(self._text_pairs):
            node = Node(text.title, i)
            nodes.append(node)
            urn = text_urn[text.title] if text.title in text_urn else None
            urn_to_node[urn] = node

        def get_next_node(node):
            return urn_to_node[text_next[node.title]]

        def get_prev_node(node):
            return urn_to_node[text_prev[node.title]]

        for node in nodes:
            next_node = get_next_node(node)
            if next_node is not None:  # and get_prev_node(next_node) == node:
                node.next = next_node
                next_node.prev = node

        start_node = nodes[0]
        while start_node.prev is not None:
            start_node = start_node.prev

        scan_node = start_node
        n_links = 0
        visited = [scan_node]
        while scan_node.next is not None and scan_node.next not in visited:
            n_links += 1
            scan_node = scan_node.next
            visited.append(scan_node.next)

        # refuse to cooperate if we don't have a full chain
        if n_links != len(nodes) - 1:
            print(
                "Insufficient data to properly order corpus based on next/prev attrs."
            )
            return

        visited = []
        new_text_pairs = []
        node = start_node
        while node is not None and node not in visited:
            new_text_pairs.append(self._text_pairs[node.orig_i])
            visited.append(node)
            node = node.next

        self._text_pairs = new_text_pairs
        print(
            "Successfully inferred proper ordering of corpus based on next/prev attrs."
        )

    @transaction.atomic
    def execute(self):
        # Delete existing objects first
        if len(self._to_delete) > 0:
            print(
                f"Found an already existing upload of '{self.corpus_name}'. "
                f"It will be automatically deleted if this transaction succeeds."
            )
            for obj in self._to_delete:
                obj.delete()

        # Set visualization formats before initial save
        vis_format_instances = []
        for vis_format in self._vis_formats:
            try:
                vis_format_instance = HtmlVisualizationFormat.objects.get(
                    slug=vis_format.slug
                )
                if vis_format_instance:
                    vis_format_instances.append(vis_format_instance)
            except HtmlVisualizationFormat.DoesNotExist:
                print(f"Warning: Visualization format '{vis_format.slug}' not found")
                continue

        if vis_format_instances:
            print(f"Our instances: {vis_format_instances}")
            self._corpus.set_visualization_formats(vis_format_instances)

        self._corpus.save()

        for text, text_metas in self._text_pairs:
            for text_meta in text_metas:
                text_meta.save()

            # Temporarily remove the corpus association to bypass constraints or trigger signals
            # FIXME: this should not be needed.
            corpus = text.corpus
            text.corpus = None
            text.save()

            # Restore the corpus association
            text.corpus = corpus
            text.save()

            for text_meta in text_metas:
                text.text_meta.add(text_meta)
            text.save()

        for text, vis in self._vises:
            vis.save()
            text.html_visualizations.add(vis)
            text.save()

        return {
            "texts": len(self._text_pairs),
            "text_metas": sum(map(lambda x: len(x[1]), self._text_pairs)),
            "vises": len(self._vises),
        }