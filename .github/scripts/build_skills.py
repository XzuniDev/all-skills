#!/usr/bin/env python3
"""Rebuild every skill folder (SKILL.md only) from the original GitHub repos.

Runs from .github/workflows/build-skills.yml (Actions > Build skills > Run workflow).
Each top-level folder holds one source repo's skills as <skill-name>/SKILL.md.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[2]
REPO = os.environ.get("GITHUB_REPOSITORY", "XzuniDev/all-skills")

# (output folder, source repo, folder inside the source repo, skill folders to leave out)
SOURCES = [
    ("anthropic-skills", "anthropics/skills", "skills", {"docx", "pdf", "pptx", "xlsx"}),
    ("mattpocock-skills", "mattpocock/skills", "skills", set()),
    ("addyosmani-agent-skills", "addyosmani/agent-skills", "skills", set()),
    ("vercel-skills", "vercel-labs/skills", "skills", set()),
    ("superpowers", "obra/superpowers", "skills", set()),
    ("google-skills", "google/skills", "skills", set()),
    ("graphify", "Graphify-Labs/graphify", "graphify", set()),
    ("karpathy-skills", "multica-ai/andrej-karpathy-skills", "skills", set()),
    ("taste-skill", "Leonxlnx/taste-skill", "skills", set()),
    ("cybersecurity-skills", "mukul975/Anthropic-Cybersecurity-Skills", "skills", set()),
    ("hallmark-anti-slop", "Nutlope/hallmark", "skills", set()),
]
# Same name as Superpowers' skill, so it gets a prefix instead of one overwriting the other.
RENAME = {("addyosmani-agent-skills", "test-driven-development"): "addyosmani-test-driven-development"}

FRONTMATTER = re.compile(r"^(---\r?\n)([\s\S]*?)(\r?\n---)")


def skill_name(text):
    """Read the skill name the way Gemini CLI does (YAML first, then a simple fallback)."""
    m = FRONTMATTER.match(text)
    if not m:
        return None
    if yaml:
        try:
            data = yaml.safe_load(m.group(2))
            if isinstance(data, dict) and isinstance(data.get("name"), str) and isinstance(data.get("description"), str):
                return data["name"]
        except Exception:
            pass
    name = re.search(r"(?im)^[ \t]*name[ \t]*:(.*)$", m.group(2))
    desc = re.search(r"(?im)^[ \t]*description[ \t]*:", m.group(2))
    return name.group(1).strip().strip("\"'") if name and desc else None


def set_name(text, new):
    m = FRONTMATTER.match(text)
    fm = re.sub(r"(?m)^([ \t]*name[ \t]*:).*$", lambda x: x.group(1) + " " + new, m.group(2), count=1)
    return m.group(1) + fm + m.group(3) + text[m.end():]


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout.strip()


def fetch(repo, base, dest):
    """Shallow, sparse clone that downloads only SKILL.md and license files."""
    git("clone", "-q", "--depth", "1", "--filter=blob:none", "--no-checkout", f"https://github.com/{repo}.git", str(dest))
    git("-C", str(dest), "sparse-checkout", "set", "--no-cone",
        f"/{base}/**/SKILL.md", f"/{base}/**/skill.md", f"/{base}/*/LICENSE*", "/LICENSE*", "/LICENCE*", "/License*", "/license*")
    git("-C", str(dest), "checkout", "-q", git("-C", str(dest), "symbolic-ref", "--short", "HEAD"))


def is_license(p):
    return p.is_file() and p.name.lower().startswith(("license", "licence"))


def write_readme(rows):
    url = f"https://github.com/{REPO}.git"
    lines = [
        "# All skills (SKILL.md only)",
        "",
        "Every skill from the repos below, one folder per repo. Each skill is `<folder>/<skill-name>/SKILL.md`.",
        "",
        "| Folder | Skills | Source |",
        "|---|---|---|",
    ]
    lines += [f"| [{f}]({f}) | {c} | [{r}](https://github.com/{r}) |" for f, r, c in rows]
    lines += [
        f"| **Total** | **{sum(c for _, _, c in rows)}** | |",
        "",
        "## Install in Gemini CLI",
        "",
        "Run the line for each folder you want, then run `/skills reload` in Gemini:",
        "",
        "```bash",
    ]
    lines += [f"gemini skills install {url} --path {f} --consent" for f, _, _ in rows]
    lines += [
        "```",
        "",
        "If this repo is private, git on your computer has to be signed in to GitHub for these commands to work.",
        "",
        "Gemini reads the description of every installed skill at the start of each session. "
        "`cybersecurity-skills` and `google-skills` are big, so install them only if you need them.",
        "",
        "## Notes",
        "",
        "- Only the `SKILL.md` files are here. Many skills normally come with helper files (scripts, reference docs) that are not included.",
        "- Not included: Anthropic's `docx`, `pdf`, `pptx` and `xlsx` skills, because their license doesn't allow copies outside Anthropic's products. "
        "[VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) has no SKILL.md files; it is a list of links.",
        "- Renamed: Addy Osmani's `test-driven-development` is `addyosmani-test-driven-development`, so it doesn't overwrite Superpowers' skill. "
        "Graphify's `skill.md` is saved as `SKILL.md`.",
        "- Each folder includes its source repo's license file, when the repo has one.",
        "",
        "## Update",
        "",
        "Actions tab > **Build skills** > **Run workflow** rebuilds every folder from the original repos.",
        "",
    ]
    (ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    tmp = Path(tempfile.mkdtemp())
    seen, rows = {}, []
    for folder, repo, base, skip in SOURCES:
        src = tmp / folder
        fetch(repo, base, src)
        out = ROOT / folder
        shutil.rmtree(out, ignore_errors=True)
        out.mkdir(parents=True)
        kept = []
        for dirpath, dirnames, filenames in os.walk(src / base):
            dirnames.sort()
            sdir = Path(dirpath)
            for fn in sorted(filenames):
                if fn.lower() != "skill.md" or sdir.name in skip:
                    continue
                path = sdir / fn
                with open(path, encoding="utf-8", errors="replace", newline="") as f:
                    text = f.read()
                name = skill_name(text)
                if not name:
                    print(f"  skipped, no name/description: {repo}/{path.relative_to(src)}")
                    continue
                name = re.sub(r'[:\\/<>*?"|]', "-", name.strip())
                new = RENAME.get((folder, name)) or (f"{folder}-{name}" if name in seen else None)
                final = new or name
                if final in seen:
                    sys.exit(f"Duplicate skill name '{final}' in {seen[final]} and {repo}")
                seen[final] = repo
                dst = out / final / "SKILL.md"
                dst.parent.mkdir(parents=True)
                if new:
                    with open(dst, "w", encoding="utf-8", newline="") as f:
                        f.write(set_name(text, new))
                else:
                    shutil.copyfile(path, dst)
                kept.append(sdir)
        licenses = [p for p in sorted(src.iterdir()) if is_license(p)]
        if not licenses:
            licenses = [p for d in kept for p in sorted(d.iterdir()) if is_license(p)][:1]
        for p in licenses:
            shutil.copyfile(p, out / p.name)
        rows.append((folder, repo, len(kept)))
        print(f"{folder}: {len(kept)} skills from {repo}")
    write_readme(rows)
    print(f"TOTAL: {sum(c for _, _, c in rows)} skills")


if __name__ == "__main__":
    main()
