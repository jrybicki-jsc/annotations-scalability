#!/bin/bash
docker build . -f Dockerfile-orch -t orchestrator && cd processor && docker build . -t processor && cd ../visualizer && docker build . -t visualizer && cd ..
