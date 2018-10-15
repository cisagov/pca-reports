#!/bin/bash
set -e

if [ "$1" = 'pca-import' ]; then
  pca-import "${@:2}"
elif [ "$1" = 'pca-report' ]; then
  pca-report "${@:2}"
elif [ "$1" = 'pca-tool' ]; then
  pca-tool "${@:2}"
elif [ "$1" = 'pca-template-preview' ]; then
  pca-template-preview "${@:2}"
else
  echo "Usage:"
  echo "  docker run [DOCKER OPTIONS] dhub.ncats.dhs.gov:5001/pca-reports pca-import [OPTIONS]"
  echo "  docker run [DOCKER OPTIONS] dhub.ncats.dhs.gov:5001/pca-reports pca-report [OPTIONS]"
  echo "  docker run [DOCKER OPTIONS] dhub.ncats.dhs.gov:5001/pca-reports pca-tool [OPTIONS]"
  echo "  docker run [DOCKER OPTIONS] dhub.ncats.dhs.gov:5001/pca-reports pca-template-preview [OPTIONS]"
fi
