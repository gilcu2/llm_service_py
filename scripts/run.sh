#!/bin/bash

./scripts/export_requirements.sh
./scripts/build_images.sh
docker-compose up
