#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Obfuscate src.py into main.py using zlib + base64 + exec."""
import zlib
import base64
from pathlib import Path


def main() -> None:
    src_path = Path("src.py")
    out_path = Path("main.py")

    if not src_path.exists():
        raise SystemExit(f"Error: {src_path} not found")

    src = src_path.read_text(encoding="utf-8")
    compressed = zlib.compress(src.encode("utf-8"), level=9)
    encoded = base64.b64encode(compressed).decode("ascii")

    # Split into ~76-char lines (similar to app.py style)
    lines = [encoded[i : i + 76] for i in range(0, len(encoded), 76)]
    b64_body = "\n".join(lines)

    main_content = (
        "#!/usr/bin/env python3\n"
        "# -*- coding: utf-8 -*-\n"
        "import zlib,base64\n"
        f'_="""{b64_body}"""\n'
        "exec(zlib.decompress(base64.b64decode(_)).decode())\n"
    )

    out_path.write_text(main_content, encoding="utf-8")
    print(f"Obfuscated {src_path} -> {out_path} successfully")
    print(f"{out_path} size: {out_path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
