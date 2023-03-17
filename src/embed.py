import pandas as pd
from typing import Optional
from rich.progress import track
import faiss

from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize, word_tokenize

from utils import read_scraper_output

import logging

logger = logging.getLogger("chatty")


class EmbeddingGenerator:
    def __init__(
        self, model_path: str, max_length: int = 90, max_entries: Optional[int] = None
    ):
        """
        Initialize the embedding generator.
        """
        self.model = SentenceTransformer(model_path)
        logger.debug(
            "Sentence transformer has max input length 0f %s", self.model.max_seq_length
        )
        self.input_data = pd.DataFrame()
        self.max_length = max_length
        self.max_entries = max_entries

    def calc_embedding(self, input_text: str) -> list:
        """
        Calculate embedding for input text using the given model.
        """
        logger.debug("Calculating embedding for input text: %s", input_text)
        return self.model.encode(input_text)

    def load_input(self, input_path: str):
        """
        Load input data from the given path.
        """
        logger.debug("Loading input data from %s", input_path)
        for n, data in enumerate(read_scraper_output(input_path)):
            if n >= self.max_entries:
                break
            content_length = len(word_tokenize(data["content"]))
            if content_length > self.max_length:
                logger.debug(
                    "Content length of %s is too long, splitting into sentences",
                    content_length,
                )
                sentences = sent_tokenize(data["content"])
                content_chunk = ""
                chunk_length = 0
                for sentence in sentences:
                    sentence_length = len(word_tokenize(sentence))
                    if sentence_length > self.max_length:
                        logger.debug(
                            "Sentence length of %s is too long, skipping",
                            sentence_length,
                        )
                        continue
                    if sentence_length + chunk_length > self.max_length:
                        data_chunk = data.copy()
                        data_chunk["content"] = content_chunk
                        data_chunk["nbr_tokens"] = chunk_length
                        logger.debug("Appending chunk %s", content_chunk)
                        self.input_data.append(data_chunk, ignore_index=True)
                        content_chunk = ""
                        chunk_length = 0

                    content_chunk += sentence
                    chunk_length += sentence_length

                data_chunk = data.copy()
                data_chunk["content"] = content_chunk
                logger.debug("Appending chunk %s", content_chunk)
                self.input_data.append(data_chunk, ignore_index=True)
            else:
                self.input_data.append(data, ignore_index=True)

    def generate_embeddings(self, input_path: str, output_path: str):
        """
        Generate embeddings for the given input data.
        """
        logger.debug("Generating embeddings for input data")
        self.input_data["embedding"] = self.input_data["content"].apply(
            self.calc_embedding
        )

    def save_embeddings(self, output_path: str):
        """
        Save embeddings to the given output path.
        """
        logger.debug("Saving embeddings to %s", output_path)
        self.input_data.to_csv(output_path, index=False)

    def create_faiss_index(self, output_path: str):
        """
        Create a FAISS index for the given embeddings.
        """
        logger.debug("Creating FAISS index")
        embeddings = self.input_data["embedding"].to_list()
        index = faiss.IndexFlatIP(768)
        index.add(embeddings)
        faiss.write_index(index, output_path)
