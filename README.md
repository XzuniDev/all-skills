# All skills (SKILL.md only)

Every skill from the repos below, one folder per repo. Each skill is `<folder>/<skill-name>/SKILL.md`.

| Folder | Skills | Source |
|---|---|---|
| [anthropic-skills](anthropic-skills) | 15 | [anthropics/skills](https://github.com/anthropics/skills) |
| [mattpocock-skills](mattpocock-skills) | 39 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| [addyosmani-agent-skills](addyosmani-agent-skills) | 25 | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) |
| [vercel-skills](vercel-skills) | 1 | [vercel-labs/skills](https://github.com/vercel-labs/skills) |
| [superpowers](superpowers) | 15 | [obra/superpowers](https://github.com/obra/superpowers) |
| [google-skills](google-skills) | 179 | [google/skills](https://github.com/google/skills) |
| [graphify](graphify) | 1 | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) |
| [karpathy-skills](karpathy-skills) | 1 | [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) |
| [taste-skill](taste-skill) | 1 | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) |
| [cybersecurity-skills](cybersecurity-skills) | 818 | [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) |
| [hallmark-anti-slop](hallmark-anti-slop) | 1 | [Nutlope/hallmark](https://github.com/Nutlope/hallmark) |
| **Total** | **1096** | |

## Install in Gemini CLI

Run the line for each folder you want, then run `/skills reload` in Gemini:

```bash
gemini skills install https://github.com/XzuniDev/all-skills.git --path anthropic-skills --consent
gemini skills install https://github.com/XzuniDev/all-skills.git --path mattpocock-skills --consent
gemini skills install https://github.com/XzuniDev/all-skills.git --path addyosmani-agent-skills --consent
gemini skills install https://github.com/XzuniDev/all-skills.git --path vercel-skills --consent
gemini skills install https://github.com/XzuniDev/all-skills.git --path superpowers --consent
gemini skills install https://github.com/XzuniDev/all-skills.git --path google-skills --consent
gemini skills install https://github.com/XzuniDev/all-skills.git --path graphify --consent
gemini skills install https://github.com/XzuniDev/all-skills.git --path karpathy-skills --consent
gemini skills install https://github.com/XzuniDev/all-skills.git --path taste-skill --consent
gemini skills install https://github.com/XzuniDev/all-skills.git --path cybersecurity-skills --consent
gemini skills install https://github.com/XzuniDev/all-skills.git --path hallmark-anti-slop --consent
```

If this repo is private, git on your computer has to be signed in to GitHub for these commands to work.

Gemini reads the description of every installed skill at the start of each session. `cybersecurity-skills` and `google-skills` are big, so install them only if you need them.

## Notes

- Only the `SKILL.md` files are here. Many skills normally come with helper files (scripts, reference docs) that are not included.
- Not included: Anthropic's `docx`, `pdf`, `pptx` and `xlsx` skills, because their license doesn't allow copies outside Anthropic's products. [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) has no SKILL.md files; it is a list of links.
- Renamed: Addy Osmani's `test-driven-development` is `addyosmani-test-driven-development`, so it doesn't overwrite Superpowers' skill. Graphify's `skill.md` is saved as `SKILL.md`.
- Each folder includes its source repo's license file, when the repo has one.

## Update

Actions tab > **Build skills** > **Run workflow** rebuilds every folder from the original repos.
