# solution-assessor

**描述：**

solution-assessor 是一个 MCP (Model Context Protocol) 服务器，旨在提供问题和相应解决方案的评估和建议。它利用 OpenAI 的 API 来分析您提供的问题和解决方案，并指出潜在的问题或需要澄清的地方。

**目标受众：** 开发者

**快速开始：**

1. **前提条件：**
   * 安装 Docker
   * 拥有 OpenAI API 密钥

2. **配置环境变量：**
   在运行容器之前，需要设置以下环境变量：
   * `OPENAI_BASE_URL`: 您的 OpenAI API Base URL。
   * `OPENAI_MODEL`: 您想要使用的 OpenAI 模型名称 (可选，默认为 `gemini-2.0-flash-exp`)。

3. **构建 Docker 镜像：**

   ```bash
   docker buildx build --platform linux/amd64,linux/arm64 --tag rikaaa0928/solution-assessor:latest --push .
   ```

   或者，您可以使用提供的 `build.sh` 脚本：

   ```bash
   ./build.sh
   ```

   **注意：** 构建镜像可能需要您登录 Docker Hub 并设置 `DOCKER_USERNAME` 和 `DOCKER_PASSWORD` 环境变量。

4. **在MCP Server中田间：**

   "solution-assessor": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "OPENAI_API_KEY=$OPENAI_API_KEY",
        "-e",
        "OPENAI_BASE_URL=$OPENAI_BASE_URL",
        "-e",
        "OPENAI_MODEL=$OPENAI_MODEL",
        "rikaaa0928/solution-assessor"
      ]
    }

   请将 `$OPENAI_BASE_URL`, `$OPENAI_API_KEY` 和 `$OPENAI_MODEL` 替换为您的实际值。

**使用方法：**

您可以通过 MCP 客户端与 solution-assessor 服务器进行交互，并调用 `solution_assessor` 工具来评估问题和解决方案。

**工具：**

* **solution_assessor:**
  * 描述： 提供问题和相应解决方案的评估和建议
  * 参数：
    * `problem` (string, 必需): 待解决的问题
    * `solution` (string, 必需): 针对该问题设计的解决方案

  **调用示例：**

  ```json
  {
    "tool_name": "solution_assessor",
    "arguments": {
      "problem": "如何解决 Docker 容器无法启动的问题？",
      "solution": "检查 Docker 日志以获取错误信息。"
    }
  }
  ```

  **评估结果：**

  OpenAI API 将返回一个包含评估结果的文本。例如：

  ```
  该解决方案是一个很好的起点，但可以更具体一些。建议在检查 Docker 日志的基础上，进一步提供一些常见的排错步骤，例如检查端口冲突、镜像是否存在、资源限制等。
  ```

**贡献：**

欢迎提交 issue 和 pull request!

**License**

本项目使用 MIT 许可证。有关更多信息，请参阅 LICENSE 文件。
