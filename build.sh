#!/bin/bash

set -e
set -x

# 启用 buildx
docker buildx create --use --bootstrap

# 镜像名称
IMAGE_NAME="rikaaa0928/solution-assessor"

# 从 pyproject.toml 中提取版本号
VERSION=$(grep 'version = "' pyproject.toml | sed -E 's/version = "(.*)"/\1/')
TAG="v${VERSION}"
if [[ -n "${DOCKER_USERNAME}" && -n "${DOCKER_PASSWORD}" ]]; then
  docker login -u "${DOCKER_USERNAME}" -p "${DOCKER_PASSWORD}"
fi

# 构建支持多架构的镜像并打上版本号和 latest 标签
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag ${IMAGE_NAME}:${TAG} \
  --tag ${IMAGE_NAME}:latest \
  --push \
  . || {
    echo "镜像构建或推送失败！"
    exit 1
  }