import logging
from typing import Dict, Optional
from google.cloud import firestore
from crawler_kit.utils.google_cloud.credentials_from_env import (
    credentials_from_env,
)
from crawler_kit.modules.general.enums.topic import Topic
from crawler_kit.utils.google_cloud.set_object import set_object

logger = logging.getLogger(__name__)


class StorageError(Exception):
    pass


class PchomeStorageService:
    def __init__(self):
        self.db = firestore.Client(credentials=credentials_from_env())
        topic = Topic.Pchome
        self.source = topic.value
        self.type = "product"
        self.platform = "web"

    def _build_firestore_path(self) -> str:
        return f"sources/{self.source}/types/{self.type}/platforms/{self.platform}/raw"

    def save_crawled_data(
        self,
        trace_id: str,
        url: str,
        content: str,
        parsed_data: Optional[Dict] = None,
        screenshot: Optional[bytes] = None,
    ) -> str:
        screenshot_url = None
        if screenshot:
            screenshot_key = f"sources/{self.source}/types/{self.type}/platforms/{self.platform}/screenshots/{trace_id}.jpg"
            screenshot_url = set_object(screenshot_key, screenshot)
        doc_data = {
            "trace_id": trace_id,
            "url": url,
            "content": content,
            "screenshot": screenshot_url,
            "parsed_data": parsed_data,
            "crawled_at": firestore.SERVER_TIMESTAMP,
            "content_len": len(content),
        }
        try:
            collection = self.db.collection(self._build_firestore_path())
            doc_ref = collection.document()
            doc_ref.set(doc_data)

            logger.info(f"Successfully saved data for URL: {url}")
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error saving to Firestore: {e}")
            raise StorageError(f"Error saving to Firestore: {e}")

    def check_url_exists(self, url: str) -> Optional[str]:
        try:
            collection = self.db.collection(self._build_firestore_path())
            docs = collection.where("url", "==", url).limit(1).get()

            if docs:
                doc_id = docs[0].id
                logger.info(f"URL already exists in Firestore: {url}, doc_id: {doc_id}")
                return doc_id

            return None

        except Exception as e:
            logger.error(f"Error checking URL existence: {e}")
            raise StorageError(f"Error checking URL existence: {e}")
