from os import listdir
from os.path import exists, isfile, join
from typing import List, Optional

import cv2
from logzero import logger

from backend.src.entities import BasicResponse, ImageFrame
from backend.src.image_accessor.image_accessor import ImageAccessor


class LocalAccessor(ImageAccessor):
    def __init__(self, folder_path: str) -> None:
        self._folder_path = folder_path

    def get_image_list(self, image_name: str) -> List[str]:
        image_folder_path = join(self._folder_path, image_name)
        if not exists(image_folder_path):
            logger.warning(f"{image_folder_path} does not exist!")
            return []

        files = [
            f for f in listdir(image_folder_path) if isfile(join(image_folder_path, f))
        ]
        image_files = [f for f in files if self._is_image_file(f)]
        return image_files

    def put_image(self, image: ImageFrame) -> BasicResponse:
        raise NotImplementedError("You should implement this!")

    def get_image(self, image_name: str, image_id: str) -> Optional[ImageFrame]:
        image_path = join(self._folder_path, image_name, image_id)
        try:
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img
        except Exception:
            return None

    def inject(self, **kwargs) -> None:
        pass
