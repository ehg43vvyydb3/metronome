import os
import tkinter as tk
from tkinter import filedialog, messagebox

from pdf_to_png import convert

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCORES_DIR = os.path.join(SCRIPT_DIR, "scores")


def pick_and_convert():
    pdf_path = filedialog.askopenfilename(
        title="PDF 선택",
        filetypes=[("PDF 파일", "*.pdf *.PDF")],
    )
    if not pdf_path:
        return

    base = os.path.splitext(os.path.basename(pdf_path))[0]
    out_dir = os.path.join(SCORES_DIR, base)

    status_var.set(f"변환 중... ({base})")
    root.update_idletasks()

    try:
        convert(pdf_path, out_dir, 150)
    except Exception as e:
        messagebox.showerror("변환 실패", str(e))
        status_var.set("변환 실패")
        return

    status_var.set(f"완료: scores/{base}")


root = tk.Tk()
root.title("PDF → PNG 변환")
root.geometry("380x140")

tk.Button(
    root, text="PDF 선택해서 변환", command=pick_and_convert, font=("", 14), height=2
).pack(pady=16, padx=16, fill="x")

status_var = tk.StringVar(value="PDF를 선택하면 scores/곡이름/ 폴더에 PNG로 저장됩니다.")
tk.Label(root, textvariable=status_var, wraplength=340, justify="left").pack(pady=8, padx=16)

root.mainloop()
