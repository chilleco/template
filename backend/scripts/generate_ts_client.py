"""
Fetch /openapi.json from running backend and
generate types + fetch client via openapi-typescript / openapi-fetch.

Usage:
    poetry run python -m scripts.generate_ts_client --url http://localhost:8000/openapi.json
"""

import subprocess, argparse, tempfile, json, urllib.request, pathlib

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:8000/openapi.json")
    ap.add_argument("--out", default="../frontend_web/src/api")   # куда кладём
    args = ap.parse_args()

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    print(f"🔄 Downloading OpenAPI from {args.url} …")
    data = urllib.request.urlopen(args.url).read()
    tmp.write(data);  tmp.close()

    out_dir = pathlib.Path(__file__).resolve().parent / args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    print("🛠  Generating TypeScript types …")
    subprocess.check_call(
        ["npx", "openapi-typescript", tmp.name, "-o", out_dir / "schema.ts"]
    )
    print("🛠  Generating openapi-fetch client …")
    subprocess.check_call(
        ["npx", "openapi-typescript-fetch", "--input", tmp.name, "--output", out_dir / "client.ts"]
    )
    print("✅ Done →", out_dir)

if __name__ == "__main__":
    main()
