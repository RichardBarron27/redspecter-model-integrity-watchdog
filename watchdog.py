import json, yaml, time
from pathlib import Path
from rich import print
from openai import OpenAI

cfg = yaml.safe_load(open("config.yml"))
probes = yaml.safe_load(open("probes.yml"))["baseline"]

client = OpenAI()
outdir = Path(cfg["output"]["directory"])
outdir.mkdir(exist_ok=True)

results = []
for p in probes:
    r = client.chat.completions.create(
        model=cfg["model"]["model_name"],
        messages=[{"role": "user", "content": p["prompt"]}],
        temperature=cfg["model"]["temperature"],
        timeout=cfg["execution"]["timeout_seconds"],
    )
    content = r.choices[0].message.content
    results.append({"id": p["id"], "response": content})
    print(f"[green]{p['id']}[/green] collected")

Path("baseline.json").write_text(json.dumps(results, indent=2))
print("[bold cyan]Baseline written[/bold cyan]")
