#!/usr/bin/env bash

BUMP_RULE=${1:-patch}

cd $PROJECT_DIR

poetry version $BUMP_RULE
NEW_VERSION=$(poetry version --short)

kacl-cli release "$NEW_VERSION" --modify --auto-link
TAG_BODY=$(kacl-cli get "$NEW_VERSION")

git add CHANGELOG.md pyproject.toml
git commit -m "Tag $NEW_VERSION"

git tag -a "$NEW_VERSION" -m "$TAG_BODY"
