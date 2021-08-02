from typing import List

import boto3
from logzero import logger

from backend.src.entities import BasicResponse, ImageFrame
from backend.src.image_accessor.image_accessor import ImageAccessor


class S3Accessor(ImageAccessor):
    def __init__(
        self, s3_public_key: str, s3_secret_key: str, s3_bucket: str, s3_region: str,
    ) -> None:
        self.s3 = boto3.resource(
            "s3",
            region_name=s3_region,
            aws_access_key_id=s3_public_key,
            aws_secret_access_key=s3_secret_key,
        )
        self._bucket = self.s3.Bucket(s3_bucket)
        logger.info("S3 Accessor Initialized")

    def get_image_list(self, image_name: str) -> List[str]:
        try:
            file_names = [
                obj.key
                for obj in self._bucket.objects.filter(Prefix=f"{image_name}/")
                if self._is_image_file(obj.key)
            ]
            return file_names
        except Exception as e:
            logger.error(e)
            return []

    def put_image(self, image: ImageFrame) -> BasicResponse:
        raise NotImplementedError("You should implement this!")

    def get_image(self, image_name: str, image_id: str) -> ImageFrame:
        raise NotImplementedError("You should implement this!")

    def inject(self, **kwargs) -> None:
        pass
