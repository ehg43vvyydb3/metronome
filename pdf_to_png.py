import sys
import os
import fitz

def convert(pdf_path, out_dir, dpi):
    doc = fitz.open(pdf_path)
    os.makedirs(out_dir, exist_ok=True)
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=matrix)
        out_path = os.path.join(out_dir, f"page-{i}.png")
        pix.save(out_path)
        print(out_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 pdf_to_png.py <pdf_path> [out_dir] [dpi]")
        sys.exit(1)
    pdf_path = sys.argv[1]
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join("scores", base)
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 150
    convert(pdf_path, out_dir, dpi)
