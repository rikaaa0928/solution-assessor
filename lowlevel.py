from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
import os
from openai import OpenAI

# Create a server instance
app = Server("solution-assessor")
client = OpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL"),
)
model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


@app.list_tools()
async def handle_list_prompts() -> list[types.Tool]:
    return [
        types.Tool(
            name="solution_assessor",
            description="提供问题和相应解决方案的评估和建议",
            inputSchema={
                "type": "object",
                "properties": {
                    "problem": {"type": "string", "description": "待解决的问题"},
                    "solution": {"type": "string", "description": "针对该问题设计的解决方案"}
                },
                "required": ["problem", "solution"]
            }
        )
    ]


@app.call_tool()
async def call_tool(
        name: str,
        arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name == "solution_assessor":
        problem = arguments["problem"]
        solution = arguments["solution"]
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system",
                     "content": "请评估以下问题和解决方案，并指出是否存在问题，或者是否需要提问者提供更多信息来澄清问题。回答请尽量简洁清晰，直奔主题"},
                    {"role": "user", "content": f"问题: {problem}\n解决方案: {solution}"},
                ],
                temperature=0
            )
            # return response.choices[0].message.content
            return [types.TextContent(type="text", text=str(response.choices[0].message.content))]
        except Exception as e:
            raise ValueError(f"调用 OpenAI API 失败: {e}，你可以认为没有问题")
    raise ValueError(f"Tool not found: {name}")


async def run():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="solution-assessor",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
