"""
PDF generation from image files.
"""
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from PIL import Image

from ..utils.logger import logger


class PDFGenerator:
    """Generates PDF files from images."""

    def __init__(self, quality: int = 95):
        """
        Initialize PDF generator.

        Args:
            quality: JPEG compression quality for images (1-100)
        """
        self.quality = quality
        logger.info(f"PDFGenerator initialized with quality: {quality}")

    def create_pdf(self, image_paths: List[Path], output_path: Path,
                   title: Optional[str] = None) -> Optional[Path]:
        """
        Create a PDF from a list of images.

        Args:
            image_paths: List of image file paths
            output_path: Output PDF file path
            title: Optional PDF title metadata

        Returns:
            Path to created PDF, or None if failed
        """
        if not image_paths:
            logger.error("No images provided for PDF creation")
            return None

        try:
            logger.info(f"Creating PDF with {len(image_paths)} images")

            # Load all images
            images = []
            for img_path in image_paths:
                try:
                    img = Image.open(img_path)
                    # Convert to RGB if necessary (PDF requires RGB)
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    images.append(img)
                    logger.debug(f"Loaded image: {img_path.name}")
                except Exception as e:
                    logger.warning(f"Failed to load image {img_path}: {e}")
                    continue

            if not images:
                logger.error("No valid images could be loaded")
                return None

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Create PDF
            first_image = images[0]
            remaining_images = images[1:] if len(images) > 1 else []

            # Set up PDF metadata
            pdf_metadata = {
                'Title': title or f'Kindle Scan {datetime.now().strftime("%Y-%m-%d")}',
                'Author': 'AK Auto-Scanner',
                'Subject': 'Scanned book pages',
                'Creator': 'AK Auto-Scanner',
                'Producer': 'Pillow',
                'CreationDate': datetime.now(),
            }

            # Save as PDF
            first_image.save(
                str(output_path),
                'PDF',
                resolution=100.0,
                save_all=True,
                append_images=remaining_images,
                quality=self.quality,
                optimize=False,
                **pdf_metadata
            )

            logger.info(f"PDF created successfully: {output_path}")
            logger.info(f"PDF size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")

            return output_path

        except Exception as e:
            logger.error(f"Error creating PDF: {e}")
            return None

    def create_pdf_from_directory(self, image_dir: Path, output_path: Path,
                                   pattern: str = "*.png") -> Optional[Path]:
        """
        Create a PDF from all images in a directory.

        Args:
            image_dir: Directory containing images
            output_path: Output PDF file path
            pattern: Glob pattern for image files

        Returns:
            Path to created PDF, or None if failed
        """
        if not image_dir.exists() or not image_dir.is_dir():
            logger.error(f"Invalid image directory: {image_dir}")
            return None

        # Find all matching images and sort them
        image_paths = sorted(image_dir.glob(pattern))

        if not image_paths:
            logger.error(f"No images found in {image_dir} with pattern {pattern}")
            return None

        return self.create_pdf(image_paths, output_path)

    def estimate_pdf_size(self, image_paths: List[Path]) -> float:
        """
        Estimate the size of the resulting PDF in MB.

        Args:
            image_paths: List of image file paths

        Returns:
            Estimated size in MB
        """
        if not image_paths:
            return 0.0

        try:
            # Sample first few images to estimate average size
            sample_size = min(5, len(image_paths))
            total_size = 0

            for img_path in image_paths[:sample_size]:
                if img_path.exists():
                    total_size += img_path.stat().st_size

            avg_size_per_image = total_size / sample_size
            estimated_total = avg_size_per_image * len(image_paths)

            # PDF compression factor (rough estimate)
            compression_factor = 0.8

            estimated_mb = (estimated_total * compression_factor) / 1024 / 1024
            return estimated_mb

        except Exception as e:
            logger.error(f"Error estimating PDF size: {e}")
            return 0.0

    def split_pdf(self, image_paths: List[Path], output_dir: Path,
                  pages_per_pdf: int = 100) -> List[Path]:
        """
        Create multiple PDFs if there are too many pages.

        Args:
            image_paths: List of image file paths
            output_dir: Output directory for PDFs
            pages_per_pdf: Maximum pages per PDF file

        Returns:
            List of created PDF paths
        """
        if not image_paths:
            return []

        output_dir.mkdir(parents=True, exist_ok=True)
        pdf_paths = []

        # Split images into chunks
        for i in range(0, len(image_paths), pages_per_pdf):
            chunk = image_paths[i:i + pages_per_pdf]
            chunk_num = (i // pages_per_pdf) + 1

            output_path = output_dir / f"kindle_scan_part{chunk_num}.pdf"
            pdf_path = self.create_pdf(chunk, output_path,
                                      title=f"Kindle Scan Part {chunk_num}")

            if pdf_path:
                pdf_paths.append(pdf_path)

        logger.info(f"Created {len(pdf_paths)} PDF files")
        return pdf_paths

    def add_page_numbers(self, image_paths: List[Path],
                        output_dir: Path) -> List[Path]:
        """
        Add page numbers to images before creating PDF.

        Args:
            image_paths: List of image file paths
            output_dir: Output directory for numbered images

        Returns:
            List of paths to numbered images
        """
        from PIL import ImageDraw, ImageFont

        output_dir.mkdir(parents=True, exist_ok=True)
        numbered_paths = []

        for idx, img_path in enumerate(image_paths, start=1):
            try:
                img = Image.open(img_path)
                draw = ImageDraw.Draw(img)

                # Calculate position (bottom center)
                text = str(idx)
                # Use default font since custom fonts may not be available
                font = ImageFont.load_default()

                # Get text size using textbbox
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                x = (img.width - text_width) // 2
                y = img.height - text_height - 20

                # Draw text with outline for visibility
                outline_color = "white"
                text_color = "black"

                # Draw outline
                for adj_x in [-1, 0, 1]:
                    for adj_y in [-1, 0, 1]:
                        draw.text((x + adj_x, y + adj_y), text, font=font, fill=outline_color)

                # Draw main text
                draw.text((x, y), text, font=font, fill=text_color)

                # Save numbered image
                output_path = output_dir / f"numbered_{img_path.name}"
                img.save(output_path)
                numbered_paths.append(output_path)

            except Exception as e:
                logger.warning(f"Failed to add page number to {img_path}: {e}")
                # Use original image if numbering fails
                numbered_paths.append(img_path)

        return numbered_paths
