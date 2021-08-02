from typing import List, Optional, Tuple

from logzero import logger

from backend.src.controller.controller import Controller
from backend.src.entities import ImageFrame, StatusType


class ImageClient(Controller):
    def get_image_list(self, image_name: str) -> Tuple[StatusType, List[str]]:
        image_list = self.image_accessor.get_image_list(image_name)
        logger.info(f"Found {len(image_list)} images under {image_name}/")
        if len(image_list) == 0:
            return StatusType.NOT_FOUND, []
        return StatusType.SUCCESS, image_list

    def get_image(
        self, image_name: str, image_id: str
    ) -> Tuple[StatusType, Optional[ImageFrame]]:
        image = self.image_accessor.get_image(image_name, image_id)
        if image is None:
            return StatusType.NOT_FOUND, None
        return StatusType.SUCCESS, image
