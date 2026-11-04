"""RAG-ready dataset transformation pipeline."""


class RAGDatasetPreparer:
    @staticmethod
    def prepare_dataset(documents: list) -> list:
        """Normalize synthetic documents for deterministic vector ingestion."""
        if not isinstance(documents, list):
            raise TypeError("documents must be a list")

        rag_records = []
        seen_ids = set()
        for index, document in enumerate(documents):
            if not isinstance(document, dict):
                raise TypeError(
                    f"document at index {index} must be a dictionary"
                )

            doc_id = document.get("id")
            if not isinstance(doc_id, str) or not doc_id.strip():
                raise ValueError(
                    f"document at index {index} must have a non-empty string id"
                )
            normalized_id = doc_id.strip()
            if normalized_id in seen_ids:
                raise ValueError(
                    f"document at index {index} has duplicate id: {normalized_id}"
                )

            text = document.get("text", "")
            if not isinstance(text, str):
                raise TypeError(
                    f"document at index {index} text must be a string"
                )
            normalized_text = text.strip()
            seen_ids.add(normalized_id)
            rag_records.append(
                {
                    "doc_id": normalized_id,
                    "text": normalized_text,
                    "token_estimate": len(normalized_text.split()),
                    "is_rag_ready": len(normalized_text) > 20,
                }
            )
        return rag_records
