# Tiefenkarte aus einem Foto (Depth Anything V2 Small, Apache-2.0). Aufruf: python tiefe.py in.jpg out.png
import sys, torch, numpy as np
from PIL import Image
from transformers import pipeline
pipe = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device="mps" if torch.backends.mps.is_available() else "cpu")
for src, dst in zip(sys.argv[1::2], sys.argv[2::2]):
    im = Image.open(src).convert("RGB")
    d = pipe(im)["predicted_depth"]
    d = torch.nn.functional.interpolate(d[None] if d.dim()==3 else d[None,None], size=im.size[::-1], mode="bicubic", align_corners=False)[0,0].numpy()
    d = (d - d.min()) / (d.max() - d.min() + 1e-6)
    Image.fromarray((d * 255).astype(np.uint8)).save(dst)
    print("ok", dst, im.size)
