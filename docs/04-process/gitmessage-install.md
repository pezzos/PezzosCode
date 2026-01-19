# Commit Template Installation

This project provides a commit template in `.gitmessage`.

## Local Installation (recommended)

```bash
git config commit.template .gitmessage
```

## Global Installation (optional)

```bash
cp .gitmessage ~/.gitmessage
git config --global commit.template ~/.gitmessage
```

## Verification

```bash
git config --get commit.template
```