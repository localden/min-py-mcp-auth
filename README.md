# Minimal Python MCP Auth Server

A minimal Model Context Protocol (MCP) server with OAuth 2.0 authentication support, based on the streamable HTTP transport. This implementation follows RFC 9728 for Protected Resource Metadata and uses OAuth 2.0 Token Introspection (RFC 7662) for token validation.

## Features

- **OAuth 2.0 Authentication**: Secure token-based authentication
- **Streamable HTTP Transport**: Modern HTTP-based MCP transport
- **Token Introspection**: Validates tokens via external Authorization Server
- **RFC 9728 Compliance**: Proper AS/RS separation
- **Multiple Tools**: Demonstrates various authenticated MCP tools

## Architecture

This server acts as a **Resource Server (RS)** that:
- Provides RFC 9728 Protected Resource Metadata
- Validates access tokens via Authorization Server introspection
- Serves MCP tools that require authentication
- Always enforces audience ("aud") validation against the resource server URL

## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd min-py-mcp-auth
```

2. Install dependencies using uv (recommended) or pip:

```bash
# Using uv
uv pip install -e .

# Or using pip
pip install -e .
```

3. Create your configuration file:

```bash
# Copy the example configuration
cp .env.example .env

# Edit the .env file with your settings
```

## Configuration

The server is configured entirely through environment variables, which can be set in a `.env` file or directly in your environment.

### Configuration File (.env)

Create a `.env` file in the project root with your configuration:

```env
# MCP Server Configuration
HOST=localhost
PORT=3000

# Auth Server Configuration (Keycloak-style)
AUTH_HOST=localhost
AUTH_PORT=8080
AUTH_REALM=master

# OAuth Client Configuration
OAUTH_CLIENT_ID=mcp-server
OAUTH_CLIENT_SECRET=your-secret-here

# Server Settings
MCP_SCOPE=mcp
TRANSPORT=streamable-http
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `localhost` | Server host address |
| `PORT` | `3000` | Server port |
| `AUTH_HOST` | Same as `HOST` | Authorization server host |
| `AUTH_PORT` | `8080` | Authorization server port |
| `AUTH_REALM` | `master` | OAuth realm (Keycloak-style) |
| `OAUTH_CLIENT_ID` | `mcp-server` | OAuth client identifier |
| `OAUTH_CLIENT_SECRET` | (empty) | OAuth client secret |
| `MCP_SCOPE` | `mcp` | Required OAuth scope |
| `TRANSPORT` | `streamable-http` | Transport type (`sse` or `streamable-http`) |

## Usage

### Prerequisites

You need a running OAuth 2.0 Authorization Server that supports token introspection. For testing, you can use the example from the MCP Python SDK:

```bash
# Clone the MCP Python SDK for the auth server example
git clone https://github.com/modelcontextprotocol/python-sdk.git
cd python-sdk/examples/servers/simple-auth

# Start the Authorization Server
uv run mcp-simple-auth-as --port=9000
```

### Running the MCP Resource Server

Once you have configured your `.env` file, simply run:

```bash
# Start the server (reads configuration from .env file)
mcp-auth-server
```

The server will:
- Load configuration from `.env` file in the current directory
- Fall back to environment variables if .env file is not found
- Use default values for any unspecified settings

### Example Configurations

**Development with local Keycloak:**
```env
HOST=localhost
PORT=3000
AUTH_HOST=localhost
AUTH_PORT=8080
AUTH_REALM=mcp-dev
OAUTH_CLIENT_ID=mcp-client
TRANSPORT=streamable-http
```

**Production deployment:**
```env
HOST=0.0.0.0
PORT=8080
AUTH_HOST=keycloak.mycompany.com
AUTH_PORT=443
AUTH_REALM=production
OAUTH_CLIENT_ID=mcp-production
OAUTH_CLIENT_SECRET=super-secret-key
TRANSPORT=streamable-http
```

### Available Tools

The server provides the following authenticated tools:

1. **`add_numbers`**: Adds two numbers together and returns the result with metadata
2. **`multiply_numbers`**: Multiplies two numbers together and returns the result with metadata

Both tools require OAuth authentication and demonstrate basic arithmetic operations in a secure context.

### Testing the Server

1. **Test Resource Discovery** (RFC 9728):

```bash
curl http://localhost:3000/.well-known/oauth-protected-resource
```

2. **Test with MCP Client**: Use any MCP client that supports OAuth authentication and streamable HTTP transport.

## Authentication Flow

1. Client discovers the Authorization Server via RFC 9728 metadata
2. Client obtains access token from Authorization Server
3. Client includes token in MCP requests
4. Server validates token via introspection endpoint
5. Server serves MCP tools to authenticated clients

## Development

### Project Structure

```text
src/
└── min_py_mcp_auth/
    ├── __init__.py
    ├── server.py           # Main MCP server implementation
    └── token_verifier.py   # OAuth token validation logic
```

### Adding New Tools

To add new authenticated tools, modify `server.py` in the `create_server()` function:

```python
@app.tool()
async def your_new_tool(param: float) -> dict[str, Any]:
    """Your tool description."""
    # Tool implementation
    result = param * 2  # Example calculation
    return {
        "operation": "your_operation",
        "input": param,
        "result": result,
        "timestamp": datetime.datetime.now().isoformat()
    }
```

### Security Considerations

- Always use HTTPS in production
- Validate Authorization Server URLs to prevent SSRF
- Implement proper rate limiting
- Use connection pooling for token introspection
- Consider token caching with appropriate TTL

## License

MIT License - see LICENSE file for details.

## Related Projects

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
