"""
OCR Service - Local Tesseract OCR fallback for scanned PDFs
Provides enterprise-grade OCR capabilities without cloud APIs
"""
import re
import io
import signal
import threading
from typing import Optional, Tuple, Dict, Any
from contextlib import contextmanager

# OCR dependencies - optional imports with fallback
try:
    from pdf2image import convert_from_path
    from PIL import Image, ImageEnhance, ImageFilter
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


class TimeoutError(Exception):
    """Custom timeout exception for OCR operations"""
    pass


class OCRService:
    """
    Local OCR Service for scanned PDF processing
    
    Features:
    - Automatic detection of when OCR is needed
    - Image preprocessing for better accuracy
    - Text cleanup and deduplication
    - Confidence scoring
    - Hard timeout protection (15 seconds)
    - Max 5 pages to prevent overload
    """
    
    # OCR Quality thresholds
    MIN_TEXT_LENGTH = 800
    MIN_WORD_COUNT = 150
    MAX_OCR_PAGES = 5
    OCR_TIMEOUT_SECONDS = 15
    OCR_DPI = 300
    
    # Email and phone patterns for quality detection
    EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    PHONE_PATTERN = r'(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}|\+\d{1,3}[-.\s]?\d{6,14}'
    
    def __init__(self):
        self.ocr_available = OCR_AVAILABLE
    
    def is_available(self) -> bool:
        """Check if OCR dependencies are available"""
        return self.ocr_available
    
    def needs_ocr(
        self, 
        text: str, 
        email: Optional[str] = None, 
        phone: Optional[str] = None
    ) -> bool:
        """
        Smart OCR decision logic
        
        OCR is triggered if ANY of the following is true:
        - Text length < 800 characters
        - Word count < 150
        - No email found
        - No phone found
        
        Args:
            text: Extracted text from PyMuPDF/pypdf
            email: Detected email (if any)
            phone: Detected phone (if any)
            
        Returns:
            True if OCR should be attempted
        """
        # Check text length
        if len(text.strip()) < self.MIN_TEXT_LENGTH:
            return True
        
        # Check word count
        word_count = len(text.split())
        if word_count < self.MIN_WORD_COUNT:
            return True
        
        # Check for email
        if not email and not re.search(self.EMAIL_PATTERN, text):
            return True
        
        # Check for phone
        if not phone and not re.search(self.PHONE_PATTERN, text):
            return True
        
        return False
    
    def extract_text_with_ocr(
        self, 
        pdf_path: str,
        max_pages: Optional[int] = None
    ) -> Tuple[Optional[str], str, str]:
        """
        Extract text from PDF using Tesseract OCR
        
        Args:
            pdf_path: Path to the PDF file
            max_pages: Maximum pages to OCR (default: MAX_OCR_PAGES)
            
        Returns:
            Tuple of (extracted_text, parsing_method, ocr_confidence)
            - extracted_text: OCR text or None if failed
            - parsing_method: "ocr" | "ocr_unavailable"
            - ocr_confidence: "low" | "medium" | "high"
        """
        if not self.ocr_available:
            return None, "ocr_unavailable", "low"
        
        max_pages = max_pages or self.MAX_OCR_PAGES
        
        try:
            # Run OCR with timeout protection
            result = self._run_ocr_with_timeout(pdf_path, max_pages)
            
            if result is None:
                return None, "ocr_unavailable", "low"
            
            extracted_text, page_count = result
            
            # Clean the OCR output
            cleaned_text = self._clean_ocr_text(extracted_text)
            
            # Calculate confidence
            confidence = self._calculate_ocr_confidence(cleaned_text)
            
            return cleaned_text, "ocr", confidence
            
        except TimeoutError:
            return None, "ocr_unavailable", "low"
        except Exception as e:
            # Log error but don't crash
            print(f"OCR Error: {str(e)}")
            return None, "ocr_unavailable", "low"
    
    def _run_ocr_with_timeout(
        self, 
        pdf_path: str, 
        max_pages: int
    ) -> Optional[Tuple[str, int]]:
        """
        Run OCR with a hard timeout to prevent hanging
        
        Args:
            pdf_path: Path to PDF
            max_pages: Maximum pages to process
            
        Returns:
            Tuple of (text, page_count) or None if timeout/error
        """
        result = {"text": None, "pages": 0, "error": None}
        
        def ocr_worker():
            try:
                # Convert PDF pages to images
                images = convert_from_path(
                    pdf_path,
                    dpi=self.OCR_DPI,
                    first_page=1,
                    last_page=max_pages
                )
                
                if len(images) > max_pages:
                    # PDF has too many pages
                    result["error"] = "too_many_pages"
                    return
                
                all_text = []
                
                for i, image in enumerate(images[:max_pages]):
                    # Preprocess image for better OCR
                    processed_image = self._preprocess_image(image)
                    
                    # Run Tesseract OCR
                    page_text = pytesseract.image_to_string(
                        processed_image,
                        lang='eng',
                        config='--oem 3 --psm 6'
                    )
                    
                    all_text.append(page_text)
                    
                    # Don't store images - privacy
                    del processed_image
                    del image
                
                result["text"] = '\n\n'.join(all_text)
                result["pages"] = len(images)
                
            except Exception as e:
                result["error"] = str(e)
        
        # Run OCR in a thread with timeout
        thread = threading.Thread(target=ocr_worker)
        thread.daemon = True
        thread.start()
        thread.join(timeout=self.OCR_TIMEOUT_SECONDS)
        
        if thread.is_alive():
            # Timeout occurred
            raise TimeoutError("OCR processing exceeded timeout")
        
        if result["error"]:
            if result["error"] == "too_many_pages":
                return None
            raise Exception(result["error"])
        
        if result["text"] is None:
            return None
        
        return result["text"], result["pages"]
    
    def _preprocess_image(self, image: 'Image.Image') -> 'Image.Image':
        """
        Preprocess image for better OCR accuracy
        
        Steps:
        1. Convert to grayscale
        2. Increase contrast
        3. Apply slight sharpening
        4. Resize if needed for clarity
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed PIL Image
        """
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Increase contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        
        # Apply slight sharpening
        image = image.filter(ImageFilter.SHARPEN)
        
        # Resize if image is too small (improves OCR)
        width, height = image.size
        if width < 1500:
            scale = 1500 / width
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = image.resize((new_width, new_height), Image.LANCZOS)
        
        return image
    
    def _clean_ocr_text(self, text: str) -> str:
        """
        Clean OCR output text
        
        Removes:
        - Duplicate lines
        - Page numbers
        - Common headers/footers
        - Excessive whitespace
        
        Args:
            text: Raw OCR text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        lines = text.split('\n')
        cleaned_lines = []
        seen_lines = set()
        
        # Common patterns to remove
        page_number_pattern = re.compile(r'^\s*(?:Page\s*)?\d+\s*(?:of\s*\d+)?\s*$', re.IGNORECASE)
        header_footer_patterns = [
            re.compile(r'^\s*confidential\s*$', re.IGNORECASE),
            re.compile(r'^\s*resume\s*$', re.IGNORECASE),
            re.compile(r'^\s*curriculum\s*vitae\s*$', re.IGNORECASE),
            re.compile(r'^\s*cv\s*$', re.IGNORECASE),
        ]
        
        for line in lines:
            # Skip empty lines (but keep structure)
            stripped = line.strip()
            
            if not stripped:
                # Keep a single blank line for structure
                if cleaned_lines and cleaned_lines[-1] != '':
                    cleaned_lines.append('')
                continue
            
            # Skip page numbers
            if page_number_pattern.match(stripped):
                continue
            
            # Skip common headers/footers
            skip = False
            for pattern in header_footer_patterns:
                if pattern.match(stripped):
                    skip = True
                    break
            if skip:
                continue
            
            # Skip exact duplicate lines (OCR artifacts)
            line_key = stripped.lower()
            if line_key in seen_lines and len(stripped) < 50:
                continue
            seen_lines.add(line_key)
            
            cleaned_lines.append(line)
        
        # Join and clean up whitespace
        result = '\n'.join(cleaned_lines)
        
        # Remove excessive blank lines
        result = re.sub(r'\n{3,}', '\n\n', result)
        
        # Clean up spaces
        result = re.sub(r'[ \t]+', ' ', result)
        
        return result.strip()
    
    def _calculate_ocr_confidence(self, text: str) -> str:
        """
        Calculate OCR confidence level based on extracted content
        
        Criteria:
        - Word count
        - Email detected
        - Phone detected
        - Skills/keywords detected
        
        Args:
            text: Cleaned OCR text
            
        Returns:
            "low" | "medium" | "high"
        """
        if not text:
            return "low"
        
        score = 0
        
        # Word count scoring
        word_count = len(text.split())
        if word_count >= 300:
            score += 3
        elif word_count >= 150:
            score += 2
        elif word_count >= 50:
            score += 1
        
        # Email detected
        if re.search(self.EMAIL_PATTERN, text):
            score += 2
        
        # Phone detected
        if re.search(self.PHONE_PATTERN, text):
            score += 1
        
        # Skills/keywords detected
        skill_keywords = [
            'experience', 'education', 'skills', 'python', 'java',
            'javascript', 'developer', 'engineer', 'manager', 'analyst',
            'project', 'team', 'company', 'university', 'bachelor',
            'master', 'degree', 'certified', 'professional'
        ]
        text_lower = text.lower()
        skill_matches = sum(1 for kw in skill_keywords if kw in text_lower)
        
        if skill_matches >= 8:
            score += 3
        elif skill_matches >= 5:
            score += 2
        elif skill_matches >= 2:
            score += 1
        
        # Determine confidence level
        if score >= 7:
            return "high"
        elif score >= 4:
            return "medium"
        else:
            return "low"
    
    def get_pdf_page_count(self, pdf_path: str) -> int:
        """
        Get the number of pages in a PDF
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Page count or 0 if error
        """
        try:
            from pypdf import PdfReader
            reader = PdfReader(pdf_path)
            return len(reader.pages)
        except Exception:
            return 0
    
    def should_skip_ocr(self, pdf_path: str) -> bool:
        """
        Check if OCR should be skipped due to page count
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            True if OCR should be skipped
        """
        page_count = self.get_pdf_page_count(pdf_path)
        return page_count > self.MAX_OCR_PAGES


# Global instance for easy access
ocr_service = OCRService()
