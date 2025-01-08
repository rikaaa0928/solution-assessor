import os
from mcp.server.fastmcp import FastMCP
from openai import OpenAI
# Create an MCP server
mcp = FastMCP("solution-assessor")

client = OpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL"),
)
model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

@mcp.tool()
async def solution_assessor(problem, solution) -> str:
    """提供问题和相应解决方案的评估和建议

    Args:
        problem: 待解决的问题
        solution: 针对该问题设计的解决方案
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "请评估以下问题和解决方案，并指出是否存在问题，或者是否需要提问者提供更多信息来澄清问题。"},
                {"role": "user", "content": f"问题: {problem}\n解决方案: {solution}"},
            ],
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"调用 OpenAI API 失败: {e}，你可以认为没有问题"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
