"""Dependency-free regression tests for RAG dataset preparation."""
import copy
import unittest

from src.rag.embedding_preparer import RAGDatasetPreparer


class RAGDatasetPreparerTests(unittest.TestCase):
    def test_normalizes_documents_without_mutating_inputs(self):
        documents = [
            {
                "id": " synthetic-doc-1 ",
                "text": "  A sufficiently detailed synthetic record.  ",
            },
            {"id": "synthetic-doc-2", "text": "short text"},
        ]
        original = copy.deepcopy(documents)

        records = RAGDatasetPreparer.prepare_dataset(documents)

        self.assertEqual(records, [
            {
                "doc_id": "synthetic-doc-1",
                "text": "A sufficiently detailed synthetic record.",
                "token_estimate": 5,
                "is_rag_ready": True,
            },
            {
                "doc_id": "synthetic-doc-2",
                "text": "short text",
                "token_estimate": 2,
                "is_rag_ready": False,
            },
        ])
        self.assertEqual(documents, original)

    def test_missing_text_is_retained_as_not_ready(self):
        records = RAGDatasetPreparer.prepare_dataset([
            {"id": "synthetic-doc-1"}
        ])

        self.assertEqual(records, [{
            "doc_id": "synthetic-doc-1",
            "text": "",
            "token_estimate": 0,
            "is_rag_ready": False,
        }])

    def test_rejects_non_list_input(self):
        with self.assertRaisesRegex(TypeError, "documents must be a list"):
            RAGDatasetPreparer.prepare_dataset(())

    def test_rejects_non_mapping_documents(self):
        with self.assertRaisesRegex(TypeError, "index 1 must be a dictionary"):
            RAGDatasetPreparer.prepare_dataset([
                {"id": "synthetic-doc-1"},
                "not-a-document",
            ])

    def test_rejects_missing_blank_and_non_string_ids(self):
        for doc_id in (None, "", "   ", 123):
            with self.subTest(doc_id=doc_id):
                with self.assertRaisesRegex(ValueError, "non-empty string id"):
                    RAGDatasetPreparer.prepare_dataset([
                        {"id": doc_id, "text": "synthetic text"}
                    ])

    def test_rejects_non_string_text(self):
        for text in (None, 123, [], {}):
            with self.subTest(text=text):
                with self.assertRaisesRegex(TypeError, "text must be a string"):
                    RAGDatasetPreparer.prepare_dataset([
                        {"id": "synthetic-doc-1", "text": text}
                    ])

    def test_rejects_duplicate_ids_after_normalization(self):
        with self.assertRaisesRegex(ValueError, "index 1 has duplicate id"):
            RAGDatasetPreparer.prepare_dataset([
                {"id": "synthetic-doc-1", "text": "first"},
                {"id": " synthetic-doc-1 ", "text": "second"},
            ])


if __name__ == "__main__":
    unittest.main()
