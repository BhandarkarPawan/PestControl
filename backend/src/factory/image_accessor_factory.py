from typing import Union

from backend.src.config import ImageStoreType, ImageAccessorConfig
from backend.src.image_accessor.local_accessor import LocalAccessor
from backend.src.image_accessor.s3_accessor import S3Accessor


def create_image_accessor(
    image_config: ImageAccessorConfig,
) -> Union[LocalAccessor, S3Accessor]:

    if image_config.store_type == ImageStoreType.LOCAL:
        return LocalAccessor(folder_path=image_config.folder_path)

    else:
        return S3Accessor(
            s3_public_key=image_config.s3_public_key,
            s3_secret_key=image_config.s3_secret_key,
            s3_bucket=image_config.s3_bucket,
            s3_region=image_config.s3_region,
        )
