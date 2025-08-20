from io import BytesIO
from PIL import Image


def png_to_jpg(png_data: bytes) -> bytes:
    """Convert PNG bytes to JPEG bytes. That's it."""
    try:
        with BytesIO(png_data) as input_buffer:
            image = Image.open(input_buffer)

            # Handle transparency properly
            if image.mode in ("RGBA", "LA", "P"):
                # Create white background for transparency
                background = Image.new("RGB", image.size, (255, 255, 255))
                if image.mode == "P":
                    image = image.convert("RGBA")
                background.paste(
                    image,
                    mask=image.split()[-1] if image.mode in ("RGBA", "LA") else None,
                )
                image = background
            elif image.mode != "RGB":
                image = image.convert("RGB")

            output_buffer = BytesIO()
            image.save(output_buffer, format="JPEG", quality=95)
            return output_buffer.getvalue()

    except Exception as e:
        raise ValueError(f"Failed to convert PNG to JPEG: {e}")


if __name__ == "__main__":
    with open("data/PNG_transparency_demonstration_1.png", "rb") as f:
        png_data = f.read()
    jpg_data = png_to_jpg(png_data)
    with open("data/output.jpg", "wb") as f:
        f.write(jpg_data)
