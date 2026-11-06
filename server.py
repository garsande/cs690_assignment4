
"""MCP server exposing the coding agent's project tools.

Creates an MCPServer named "a4-tools" and registers the four tools
defined in agent.tools.TOOLS: list_files, read_file, edit_file,
and run_tests.

Each tool's name, description, and input schema are derived from
its Python function name, docstring, and parameters.

When executed directly, the server requires a --workspace PATH
argument identifying the project folder. It configures the workspace
and starts the MCP server using stdio transport.

Importing this module does not start the server, allowing tests
and other MCP clients to connect to the server directly.

File operations are restricted to the configured workspace
by the underlying agent tools.
"""

import argparse

from mcp.server import MCPServer

from agent import tools


# Create the MCP server.
mcp = MCPServer("a4-tools")


# Register the four agent tools.
for fn in tools.TOOLS:
    mcp.add_tool(fn)


def main() -> None:
    """Configure the workspace and start the MCP server.

    Requires --workspace PATH as a command-line argument.
    The path identifies the project directory containing files
    that the agent can inspect, edit, and test.

    Starts the server using stdio transport so MCP clients
    can discover and invoke the registered tools.
    """
    parser = argparse.ArgumentParser(
        description="MCP server for Assignment 4 coding agent tools."
    )

    parser.add_argument(
        "--workspace",
        required=True,
        help="Path to the project workspace."
    )

    args = parser.parse_args()

    tools.use_workspace(args.workspace)

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
