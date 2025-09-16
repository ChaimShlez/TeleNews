from typing import Any
from pymongo import MongoClient
from pymongo.errors import BulkWriteError


class MongoDBService:
    def __init__(self, connection_string: str, db_name: str):
        """Initializes the MongoDB client"""
        self._client = MongoClient(connection_string)
        self._db = self._client[db_name]

    # CRUD operations
    def insert_one(self, collection: str, document: dict[str, Any], **kwargs) -> bool:
        """
        Insert a single document into a collection

        Args:
            collection: The name of the collection to insert the document into
            document: The document to insert
            kwargs: Additional keyword arguments to pass to the insert_one method

        Returns:
            True if acknowledged that the document was inserted, False otherwise
        """
        response = self._db[collection].insert_one(document, **kwargs)
        return response.acknowledged

    def find(
            self,
            collection: str,
            query: dict = None,
            fields: list[str] = None,
            exclude_id: bool = False,
            sort: list[tuple[str, int]] = None,
            limit: int = None,
            skip: int = None
    ) -> list[dict[str, Any]] | bool:
        """
        Find documents in the collection

        Args:
            collection: The name of the collection to find the documents in
            query: The query to find the documents by
            fields: The fields to return in the documents
            exclude_id: Whether to exclude the _id field from the documents
            sort: The sort order of the documents
            limit: The maximum number of documents to return
            skip: The number of documents to skip

        Returns:
            A list of documents that match the query
        """
        query = query or {}
        projection = self._parse_projection(fields, exclude_id)

        cursor = self._db[collection].find(query, projection)

        if sort:
            cursor = cursor.sort(sort)
        if limit:
            cursor = cursor.limit(limit)
        if skip:
            cursor = cursor.skip(skip)

        return cursor.to_list()

    @staticmethod
    def _parse_projection(fields: list[str], exclude_id: bool) -> dict[str, int] | None:
        projection = {field: 1 for field in fields} if fields else None
        if projection and exclude_id:
            projection['_id'] = 0
        return projection