# dotkit

The terminal output vocabulary for small python command-line tools: `ui` prints status lines (`→ ✓ ⚠ ✗ ·`, a bold title, a dim note, a `✨` summary) and `colors` decides per stream whether escape codes are wanted.
It is the python half of the `_ui` fish function in [dotfiles](https://github.com/jmanuelrosa/dotfiles), so a fish function and a python tool look the same on screen.

Stdlib only, Python 3.

## Vendored, not published

Every consumer has to run with nothing but `python3`: scripts executed from a checkout, skill scripts run by an agent harness, and zipapp releases with no dependencies.
None of them can install a package at runtime, so a published package would still have to be copied into each one.
This repository is therefore the single source, and `bin/dotkit-vendor` is the copy step.

| Consumer | Vendored into |
|---|---|
| [dotfiles](https://github.com/jmanuelrosa/dotfiles) | `lib/python/dotkit/` |
| [agent-catalog](https://github.com/jmanuelrosa/agent-catalog) | `lib/python/dotkit/` |
| [kura](https://github.com/jmanuelrosa/kura) | `kura/` |
| [hostof](https://github.com/jmanuelrosa/hostof) | `_hostof_runtime/` |

Revisit publishing if a consumer appears that can install dependencies, or if `ui` and `colors` start changing often enough that vendoring becomes the bottleneck.

## How a consumer stays in sync

A consumer opts in with a `dotkit.json` at its root naming the package directory the modules land in:

```json
{ "target": "lib/python/dotkit" }
```

Vendoring copies `ui.py` and `colors.py` there and records this repository's commit and each file's sha256 in that same file.
The consumer's own test suite hashes its copies against those values, offline, so an edit made to a copy instead of here fails that consumer's tests.

```fish
bin/dotkit-vendor ~/Developer/dotfiles ~/Developer/agent-catalog   # copy, refusing uncommitted module changes
bin/dotkit-vendor --check ~/Developer/personal/kura                # report edited or outdated copies
```

`make vendor CONSUMERS="..."` and `make check CONSUMERS="..."` wrap the same calls.
Each consumer then commits its updated copies and `dotkit.json` like any other change.

## Development

`make test` runs the suite.
The differential test proving `ui.py` and `_ui.fish` render identical bytes lives in dotfiles, beside the fish half it compares against.
