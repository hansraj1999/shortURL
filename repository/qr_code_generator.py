"""QR Code generation utility"""
import qrcode
from io import BytesIO
import base64
import logging

logger = logging.getLogger(__name__)


def generate_qr_code(url: str) -> str:
    """
    Generate a QR code for the given URL and return it as a base64-encoded string.
    
    Args:
        url: The URL to encode in the QR code
        
    Returns:
        Base64-encoded string of the QR code image (PNG format)
    """
    try:
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,  # Controls the size of the QR Code
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
            box_size=10,  # Size of each box in pixels
            border=4,  # Border thickness in boxes
        )
        
        # Add data
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to bytes
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Encode to base64
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        logger.info(f"Generated QR code for URL: {url}")
        return img_base64
        
    except Exception as e:
        logger.error(f"Error generating QR code: {str(e)}")
        raise

