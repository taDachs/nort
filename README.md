# Nort (WIP)

## What do I actually want?
- generate entries automatically
- grepable
- automatically copy undone tasks from yesterday into today

## installation
- `pip3 install nort`

## Commands
- `nort new test -t tag1,tag2,tag3` generates note called test with tags tag1, tag2 and tag3
- `nort view [name]` opens note in viewer, specified in settings
- `nort list` lists all notes
- `nort list --tags tag1` lists notes that have tag1

## Options
Options can be configured in the `~/.nort.yaml` file (or `~/.config/nort/nort.yaml`)
- `viewer`: which viewer gets used by `nort view`
- `editor`: which editor gets used by `nort new` and `nort edit`
- `nort_path`: where to save the notes

## How to store meta info
- books can be own folders, or just tags
  - like notable: `Notebooks/peter/` corresponds to a notebook called peter
- `---` signifies start and end of metadata
- inside `---` yaml is used

```markdown
---
tags: [Notebooks/Work/protocols/2021/April]
title: Work on 16.04.2021
---
```

## TODO
- [x] implement nort new
- [ ] implement nort list
