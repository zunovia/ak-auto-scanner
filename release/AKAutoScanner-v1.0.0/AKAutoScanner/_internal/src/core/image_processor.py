"""
Image processing and duplicate detection using SSIM.
"""
import cv2
import numpy as np
from pathlib import Path
from typing import Optional, List, Tuple
from skimage.metrics import structural_similarity as ssim

from ..utils.logger import logger


class ImageProcessor:
    """Handles image comparison and duplicate detection."""

    def __init__(self, similarity_threshold: float = 0.95):
        """
        Initialize image processor.

        Args:
            similarity_threshold: SSIM threshold for considering images as duplicates (0.0-1.0)
        """
        self.similarity_threshold = similarity_threshold
        logger.info(f"ImageProcessor initialized with threshold: {similarity_threshold}")

    def compare_images(self, img1_path: Path, img2_path: Path) -> Tuple[bool, float]:
        """
        Compare two images using SSIM algorithm.

        Args:
            img1_path: Path to first image
            img2_path: Path to second image

        Returns:
            Tuple of (is_duplicate, similarity_score)
        """
        try:
            # Load images in grayscale
            img1 = cv2.imread(str(img1_path), cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imread(str(img2_path), cv2.IMREAD_GRAYSCALE)

            if img1 is None or img2 is None:
                logger.error(f"Failed to load images: {img1_path} or {img2_path}")
                return False, 0.0

            # Resize to same dimensions if needed
            if img1.shape != img2.shape:
                logger.debug(f"Resizing images: {img1.shape} -> {img2.shape}")
                img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

            # Calculate SSIM
            score = ssim(img1, img2)

            is_duplicate = score >= self.similarity_threshold

            logger.debug(f"SSIM score: {score:.4f} (threshold: {self.similarity_threshold}) "
                        f"-> {'DUPLICATE' if is_duplicate else 'DIFFERENT'}")

            return is_duplicate, score

        except Exception as e:
            logger.error(f"Error comparing images: {e}")
            return False, 0.0

    def is_duplicate(self, img1_path: Path, img2_path: Path) -> bool:
        """
        Check if two images are duplicates.

        Args:
            img1_path: Path to first image
            img2_path: Path to second image

        Returns:
            True if images are duplicates, False otherwise
        """
        is_dup, _ = self.compare_images(img1_path, img2_path)
        return is_dup

    def remove_consecutive_duplicates(self, image_paths: List[Path]) -> List[Path]:
        """
        Remove consecutive duplicate images from a list.

        Args:
            image_paths: List of image paths

        Returns:
            List of unique image paths (duplicates removed)
        """
        if not image_paths:
            return []

        unique_images = [image_paths[0]]
        duplicates_removed = 0

        for i in range(1, len(image_paths)):
            is_dup = self.is_duplicate(unique_images[-1], image_paths[i])

            if not is_dup:
                unique_images.append(image_paths[i])
            else:
                duplicates_removed += 1
                logger.debug(f"Removing duplicate: {image_paths[i].name}")

        logger.info(f"Removed {duplicates_removed} duplicate images. "
                   f"Remaining: {len(unique_images)}")

        return unique_images

    def get_image_dimensions(self, image_path: Path) -> Optional[Tuple[int, int]]:
        """
        Get image dimensions.

        Args:
            image_path: Path to image

        Returns:
            Tuple of (width, height) or None if error
        """
        try:
            img = cv2.imread(str(image_path))
            if img is None:
                return None
            height, width = img.shape[:2]
            return (width, height)
        except Exception as e:
            logger.error(f"Error getting image dimensions: {e}")
            return None

    def validate_images(self, image_paths: List[Path]) -> Tuple[List[Path], List[Path]]:
        """
        Validate a list of images and separate valid from invalid.

        Args:
            image_paths: List of image paths to validate

        Returns:
            Tuple of (valid_images, invalid_images)
        """
        valid_images = []
        invalid_images = []

        for img_path in image_paths:
            if not img_path.exists():
                logger.warning(f"Image does not exist: {img_path}")
                invalid_images.append(img_path)
                continue

            try:
                img = cv2.imread(str(img_path))
                if img is None or img.size == 0:
                    logger.warning(f"Invalid image: {img_path}")
                    invalid_images.append(img_path)
                else:
                    valid_images.append(img_path)
            except Exception as e:
                logger.warning(f"Error validating image {img_path}: {e}")
                invalid_images.append(img_path)

        logger.info(f"Image validation: {len(valid_images)} valid, {len(invalid_images)} invalid")
        return valid_images, invalid_images

    def crop_margins(self, image_path: Path, output_path: Path,
                     margin_percent: float = 2.0) -> bool:
        """
        Crop margins from an image (optional feature).

        Args:
            image_path: Input image path
            output_path: Output image path
            margin_percent: Percentage of margin to crop from each side

        Returns:
            True if successful, False otherwise
        """
        try:
            img = cv2.imread(str(image_path))
            if img is None:
                return False

            height, width = img.shape[:2]

            # Calculate crop margins
            margin_x = int(width * margin_percent / 100)
            margin_y = int(height * margin_percent / 100)

            # Crop image
            cropped = img[margin_y:height-margin_y, margin_x:width-margin_x]

            # Save cropped image
            output_path.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(output_path), cropped)

            logger.debug(f"Cropped image: {image_path} -> {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error cropping image: {e}")
            return False

    def calculate_hash(self, image_path: Path) -> Optional[str]:
        """
        Calculate perceptual hash for quick comparison (alternative to SSIM).

        Args:
            image_path: Path to image

        Returns:
            Hash string or None if error
        """
        try:
            img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
            if img is None:
                return None

            # Resize to 8x8
            resized = cv2.resize(img, (8, 8), interpolation=cv2.INTER_AREA)

            # Calculate mean
            mean = resized.mean()

            # Create hash based on whether pixel is above or below mean
            hash_bits = (resized > mean).flatten()
            hash_str = ''.join(['1' if bit else '0' for bit in hash_bits])

            return hash_str

        except Exception as e:
            logger.error(f"Error calculating hash: {e}")
            return None
