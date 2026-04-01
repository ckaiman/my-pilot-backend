import os
import django
import asyncio
from mcp.server.models import InitializationOptions
from mcp.server import Notification, Server
from mcp.server.stdio import stdio_server
import mcp.types as types

# --- 1. Bootstrap Django ---
# This allows the script to use Django Models outside of a standard web request.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pilot_backend.settings')
django.setup()

from api.models import Mission

# --- 2. Create MCP Server ---
server = Server("pilot-mission-control")

# --- 3. Define Tools ---

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools for the mission control agent."""
    return [
        types.Tool(
            name="list_missions",
            description="List all space missions and their current status.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="get_mission_details",
            description="Get full details for a specific mission by name.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "The exact name of the mission"},
                },
                "required": ["name"],
            },
        ),
        types.Tool(
            name="update_mission_status",
            description="Update the status of a mission (e.g., 'In Progress', 'Completed').",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "The name of the mission"},
                    "status": {"type": "string", "description": "The new status string"},
                },
                "required": ["name", "status"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    if not arguments:
        arguments = {}

    # Tool: list_missions
    if name == "list_missions":
        # Note: sync_to_async or similar is usually needed for production,
        # but for this simple pilot script, direct ORM calls work.
        missions = Mission.objects.all()
        result = "\n".join([f"- {m.name}: {m.status}" for m in missions])
        return [types.TextContent(type="text", text=f"Current Missions:\n{result}" if result else "No missions found.")]

    # Tool: get_mission_details
    elif name == "get_mission_details":
        m_name = arguments.get("name")
        try:
            m = Mission.objects.get(name=m_name)
            details = f"Mission: {m.name}\nStatus: {m.status}\nDescription: {m.description}"
            return [types.TextContent(type="text", text=details)]
        except Mission.DoesNotExist:
            return [types.TextContent(type="text", text=f"Mission '{m_name}' not found.")]

    # Tool: update_mission_status
    elif name == "update_mission_status":
        m_name = arguments.get("name")
        m_status = arguments.get("status")
        try:
            m = Mission.objects.get(name=m_name)
            old_status = m.status
            m.status = m_status
            m.save()
            return [types.TextContent(type="text", text=f"Updated '{m_name}' from '{old_status}' to '{m_status}'.")]
        except Mission.DoesNotExist:
            return [types.TextContent(type="text", text=f"Mission '{m_name}' not found.")]

    raise ValueError(f"Unknown tool: {name}")

# --- 4. Main Entry Point ---
async def main():
    # Run the server using standard input/output (stdio)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="pilot-mission-control",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=Notification(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
