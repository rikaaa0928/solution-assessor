# solution-assessor

**Description:**

solution-assessor is an MCP (Model Context Protocol) server designed to provide evaluation and suggestions for problems and corresponding solutions. It utilizes the OpenAI API to analyze the problem and solution you provide, and points out potential issues or areas that need clarification.

**Target Audience:** Developers

**Quick Start:**

1. **Prerequisites:**
   * Docker installed
   * An OpenAI API key

2. **Configure Environment Variables:**
   Before running the container, you need to set the following environment variables:
   * `OPENAI_BASE_URL`: Your OpenAI API Base URL.
   * `OPENAI_MODEL`: The name of the OpenAI model you want to use (optional, defaults to `gpt-4o-mini`).

3. **Build Docker Image:**

   ```bash
   docker buildx build --platform linux/amd64,linux/arm64 --tag rikaaa0928/solution-assessor:latest --push .
   ```

   Alternatively, you can use the provided `build.sh` script:

   ```bash
   ./build.sh
   ```

   **Note:** Building the image may require you to log in to Docker Hub and set the `DOCKER_USERNAME` and `DOCKER_PASSWORD` environment variables.

4. **Add to MCP Server:**

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

   Please replace `$OPENAI_BASE_URL`, `$OPENAI_API_KEY`, and `$OPENAI_MODEL` with your actual values.

**Usage:**

You can interact with the solution-assessor server through an MCP client and call the `solution_assessor` tool to evaluate problems and solutions.

**Tool:**

* **solution_assessor:**
  * Description: Provides evaluation and suggestions for problems and corresponding solutions.
  * Parameters:
    * `problem` (string, required): The problem to be solved.
    * `solution` (string, required): The solution designed for the problem.

  **Example Call:**

  ```json
  {
    "tool_name": "solution_assessor",
    "arguments": {
      "problem": "How to solve the problem of a Docker container failing to start?",
      "solution": "Check the Docker logs for error messages."
    }
  }
  ```

  **Evaluation Result:**

  The OpenAI API will return a text containing the evaluation result. For example:

  ```
  The solution is a good starting point, but it could be more specific. It is recommended to provide some common troubleshooting steps in addition to checking the Docker logs, such as checking for port conflicts, whether the image exists, resource limitations, etc.
  ```

**Contribution:**

Welcome to submit issues and pull requests!

**License**

This project is licensed under the MIT License. See the LICENSE file for more information.
