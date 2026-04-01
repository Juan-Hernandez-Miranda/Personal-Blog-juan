"""
lo que hace este script es muy sencillo lo unico que hace es cambiar los tamaños de las imagenes para que los 
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


SOURCE_DIR = Path(__file__).resolve().parents[1] / "frontend" / "static" / "imagenes"
OUTPUT_DIR = SOURCE_DIR

DEFAULT_MAX_WIDTH = 1600
WEBP_QUALITY = 82



TARGET_WIDTHS: dict[str, int] = {
    "chris-ried-ieic5Tq8YMk-unsplash.jpg": 1920,
    "cubo-minecraft_3840x2160_xtrafondos.com.jpg": 1920,
    "towfiqu-barbhuiya-FnA5pAzqhMM-unsplash.jpg": 1200,
    "sei-bS46IAXWAO4-unsplash.jpg": 1200,
    "domenico-loia-EhTcC9sYXsw-unsplash.jpg": 1200,
    "museums-victoria-G9Yy-iitjjg-unsplash.jpg": 1200,
    "pawel-czerwinski-WEizaiwLk1k-unsplash.jpg": 1200,
    "skajasl.jpg": 300,
    "quantu computer.jpg": 1240,
    "virtual box.jpg": 1240,
    "rtrrr.jpg": 1240,
    "einteff.jpg": 1600,
    "computer.jpg": 600,
}


def get_target_width(image_name: str) -> int:
    return TARGET_WIDTHS.get(image_name, DEFAULT_MAX_WIDTH)


def resize_to_max_width(image: Image.Image, max_width: int) -> Image.Image:
    if image.width <= max_width:
        return image

    new_height = round(image.height * max_width / image.width)
    return image.resize((max_width, new_height), Image.Resampling.LANCZOS)


def convert_jpg_to_webp(source_path: Path) -> None:
    with Image.open(source_path) as original_image:
        image = ImageOps.exif_transpose(original_image)

        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")

        target_width = get_target_width(source_path.name)
        resized_image = resize_to_max_width(image, target_width)
        resized_note = "resized" if resized_image.width < image.width else "kept"

        output_path = OUTPUT_DIR / f"{source_path.stem}.webp"
        resized_image.save(
            output_path,
            format="WEBP",
            quality=WEBP_QUALITY,
            method=6,
        )

        print(
            f"{source_path.name} -> {output_path.name} | "
            f"{resized_image.width}x{resized_image.height} | {resized_note}"
        )


def main() -> None:
    if not SOURCE_DIR.exists():
        raise SystemExit(f"No existe la carpeta de imagenes: {SOURCE_DIR}")

    jpg_files = sorted(
        path for path in SOURCE_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg"}
    )

    if not jpg_files:
        print("No se encontraron archivos JPG/JPEG para convertir.")
        return

    for source_path in jpg_files:
        convert_jpg_to_webp(source_path)


if __name__ == "__main__":
    main()