"""MCP server exposing the Vinpearl room-booking tools."""

import json
import sys
from typing import Dict, Any, List
from tools import TOOLS_SCHEMA, dispatch_tool_call

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class MCPVinpearlServer:
    """Minimal MCP-style server for the Vinpearl booking tools."""

    def __init__(self, server_name: str = "vinpearl-booking-mcp-server"):
        self.server_name = server_name
        self.version = "2026.1.0"
        
    def list_tools(self) -> List[Dict[str, Any]]:
        """Trả về danh sách các Tools chuẩn giao thức MCP"""
        return TOOLS_SCHEMA
        
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool and wrap its JSON result in an MCP-style response.
        """
        raw_result = dispatch_tool_call(tool_name, arguments)
        try:
            content = json.loads(raw_result)
        except json.JSONDecodeError as exc:
            content = {
                "status": "EXECUTION_ERROR",
                "error": f"Tool trả về JSON không hợp lệ: {exc}",
            }
        return {
            "jsonrpc": "2.0",
            "server": self.server_name,
            "tool": tool_name,
            "result": content,
        }


# Compatibility alias for imports from the original VinUni starter project.
MCPAcademicServer = MCPVinpearlServer


if __name__ == "__main__":
    server = MCPVinpearlServer()
    print(f"MCP server: {server.server_name} ({server.version})")
    print(json.dumps(server.call_tool(
        "search_rooms",
        {
            "location": "Vinpearl Nha Trang",
            "check_in": "2026-10-01",
            "check_out": "2026-10-03",
            "adults": 2,
        },
    ), ensure_ascii=False, indent=2))
