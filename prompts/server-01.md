asked ChatGPT to implement server.py and provided below details along with tests/test_server.py to use for testing and verification

What it must do:
  1. Create an MCPServer named "a4-tools" and keep it in a module-level variable named mcp.
  2. Register every function in agent.tools.TOOLS as a tool, with mcp.add_tool(fn).
     That is the same as putting @mcp.tool() on the function: the function's name becomes
     the tool's name, its docstring becomes the description, and its parameters become
     the input schema.
  3. Only when run as a program (inside `if __name__ == "__main__":`), read one required
     command-line option, --workspace PATH, call tools.use_workspace(PATH), then
     mcp.run(transport="stdio").

Importing this file must not start the server: the tests import it and talk to `mcp`
directly.
"""

import argparse

from mcp.server import MCPServer

from agent import tools

# TODO(Part 5): create the server, register the tools, and write main(). About 15 lines.
mcp = None


def main() -> None:
    raise NotImplementedError("Part 5: write server.py")


if __name__ == "__main__":
    main()

