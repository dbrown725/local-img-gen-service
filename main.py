import os
import io
import json
import base64
import string
import mimetypes
from pathlib import Path

from PIL import Image

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
UPLOADS_DIRECTORY = os.getenv("UPLOADS_DIRECTORY")
DOWNLOADS_DIRECTORY = os.getenv("DOWNLOADS_DIRECTORY")
MODEL = "google/gemini-3.1-flash-image-preview"


def validate_env():
    missing = [
        var for var in ("OPENROUTER_API_KEY", "UPLOADS_DIRECTORY", "DOWNLOADS_DIRECTORY")
        if not os.getenv(var)
    ]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")


def get_user_inputs():
    json_filename = input("Enter the carousel content JSON filename (in uploads directory): ").strip()
    image_filename = input("Enter the example image filename (in uploads directory): ").strip()
    return json_filename, image_filename


def validate_file(directory: str, filename: str) -> Path:
    path = Path(directory) / filename
    if not path.exists():
        raise FileNotFoundError(f"File not found in uploads directory: {path}")
    return path


def load_json(path: Path) -> list:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    slides = data.get("presentation")
    if not isinstance(slides, list):
        raise ValueError("JSON file must contain a 'presentation' array at the root.")
    return slides


def encode_image_base64(path: Path) -> tuple[str, str]:
    """Returns (base64_string, media_type)."""
    mime_type, _ = mimetypes.guess_type(str(path))
    if not mime_type:
        mime_type = "image/jpeg"
    with open(path, "rb") as f:
        encoded = base64.standard_b64encode(f.read()).decode("utf-8")
    return encoded, mime_type


def build_prompt(slide: dict, image_filename: str) -> str:
    content_block = (
        f'      "title": "{slide.get("title", "")}",\n'
        f'      "visual": "{slide.get("visual", "")}",\n'
        f'      "text": "{slide.get("text", "")}"'
    )
    return (
        f"You are generating an image that will be used in an Instagram Carousel. "
        f"Generate a new image using the attached file {image_filename} as a style and structure guide.\n"
        f"The final image should correctly match the attached file graphics found at the bottom of the image, "
        f"those being the url, FWD icon and the right arrow icon.\n"
        f"Content description:\n{content_block}"
    )


def call_openrouter(api_key: str, prompt: str, image_files: list[Path]) -> bytes | None:
    """
    Calls OpenRouter with the prompt and a list of image file attachments.
    Returns the generated image bytes if available, otherwise None.
    """
    import requests as _requests

    image_content = []
    for img_path in image_files:
        b64, mime = encode_image_base64(img_path)
        image_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:{mime};base64,{b64}"
            }
        })

    payload = {
        "model": MODEL,
        "modalities": ["image", "text"],
        "messages": [
            {
                "role": "user",
                "content": image_content + [{"type": "text", "text": prompt}]
            }
        ],
    }

    response = _requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()

    if not data.get("choices"):
        print(f"  Warning: No choices in response. Error: {data.get('error')}")
        return None

    message = data["choices"][0]["message"]

    # Image is returned in message.images as per OpenRouter image generation API
    images = message.get("images") or []
    for img in images:
        url = img.get("image_url", {}).get("url", "")
        if url.startswith("data:"):
            _, b64_data = url.split(",", 1)
            return base64.b64decode(b64_data)

    # Fallback: log text response
    content = message.get("content")
    if content:
        print(f"  Model text response (no image returned): {str(content)[:200]}")

    return None


def slide_label(index: int) -> str:
    """Converts 0-based index to letter label: 0->A, 1->B, ..., 25->Z, 26->AA, ..."""
    label = ""
    n = index
    while True:
        label = string.ascii_uppercase[n % 26] + label
        n = n // 26 - 1
        if n < 0:
            break
    return label


def optimize_image(image_bytes: bytes, max_dimension: int = 1080, quality: int = 85) -> tuple[bytes, str]:
    """
    Resizes and compresses an image using Pillow (similar to squoosh.app).
    Caps the longest side at max_dimension pixels and saves as JPEG at the
    given quality level. Returns (optimized_bytes, 'image/jpeg').
    """
    img = Image.open(io.BytesIO(image_bytes))

    # Convert palette/RGBA modes to RGB for JPEG compatibility
    if img.mode in ("P", "RGBA", "LA"):
        img = img.convert("RGB")

    # Downscale if either dimension exceeds max_dimension
    if max(img.width, img.height) > max_dimension:
        img.thumbnail((max_dimension, max_dimension), Image.LANCZOS)

    original_kb = len(image_bytes) / 1024
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    optimized_bytes = buf.getvalue()
    optimized_kb = len(optimized_bytes) / 1024
    print(f"  Optimized: {original_kb:.1f} KB -> {optimized_kb:.1f} KB  ({img.width}x{img.height}px)")
    return optimized_bytes, "image/jpeg"


def save_image(image_bytes: bytes, downloads_dir: str, label: str, mime_type: str = "image/png"):
    image_bytes, mime_type = optimize_image(image_bytes)
    ext = ".jpg"
    output_path = Path(downloads_dir) / f"Slide_{label}{ext}"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(image_bytes)
    return output_path


def main():
    validate_env()

    json_filename, image_filename = get_user_inputs()

    json_path = validate_file(UPLOADS_DIRECTORY, json_filename)
    image_path = validate_file(UPLOADS_DIRECTORY, image_filename)

    slides = load_json(json_path)
    total = len(slides)
    print(f"\nFound {total} slide(s) in '{json_filename}'. Starting generation...\n")

    for index, slide in enumerate(slides):
        label = slide_label(index)
        image_number = slide.get("image_number", index + 1)
        print(f"[{index + 1}/{total}] Generating Slide_{label} (image_number={image_number})...")

        prompt = build_prompt(slide, image_filename)
        image_bytes = call_openrouter(OPENROUTER_API_KEY, prompt, image_files=[image_path])

        if image_bytes:
            saved_path = save_image(image_bytes, DOWNLOADS_DIRECTORY, label)
            print(f"  Saved: {saved_path}")
        else:
            print(f"  Warning: No image data returned for Slide_{label}. Skipping save.")

    print("\nDone.")


if __name__ == "__main__":
    main()
