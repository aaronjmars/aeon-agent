#!/bin/bash
TOKEN=$(gh auth token)
git -C /home/runner/work/aeon-agent/aeon-agent/docs-sync-work remote set-url origin "https://x-access-token:${TOKEN}@github.com/aaronjmars/aeon-website.git"
git -C /home/runner/work/aeon-agent/aeon-agent/docs-sync-work push -u origin aeon/changelog-2026-06-22
