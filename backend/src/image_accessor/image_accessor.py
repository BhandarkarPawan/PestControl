from abc import ABC, abstractmethod
from typing import List, Optional

from backend.src.entities import BasicResponse, ImageFrame


class ImageAccessor(ABC):
    @abstractmethod
    def get_image_list(self, image_name: str) -> List[str]:
        raise NotImplementedError("You should implement this!")

    @abstractmethod
    def get_image(self, image_name: str, image_id: str) -> Optional[ImageFrame]:
        raise NotImplementedError("You should implement this!")

    @abstractmethod
    def put_image(self, image: ImageFrame) -> BasicResponse:
        raise NotImplementedError("You should implement this!")

    @abstractmethod
    def inject(self, **kwargs) -> None:
        raise NotImplementedError("You should implement this!")

    def _is_image_file(self, file_name: str) -> bool:
        file_name_split = file_name.split(".")
        if len(file_name_split) == 0:
            return False
        ext = file_name_split[-1]
        return ext in ["png", "jpg", "jpeg"]
