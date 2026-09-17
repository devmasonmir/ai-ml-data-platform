"""RAG-Ready Dataset Transformation Pipeline."""
from typing import List, Dict, Any

class RAGDatasetPreparer:
    @staticmethod
    def prepare_dataset(documents: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        rag_records = []
        for doc in documents:
            text = doc.get("text", "").strip()
            rag_records.append({
                "doc_id": doc.get("id"),
                "text": text,
                "token_estimate": len(text.split()),
                "is_rag_ready": len(text) > 20
            })
        return rag_records
