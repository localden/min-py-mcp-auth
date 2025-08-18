"""Configuration settings for the MCP auth server."""

import os
from typing import Optional


class Config:
    """Configuration class that loads from environment variables with sensible defaults."""
    
    # Server settings
    HOST: str = os.getenv("HOST", "localhost")
    PORT: int = int(os.getenv("PORT", "3000"))
    
    # Auth server settings
    AUTH_HOST: str = os.getenv("AUTH_HOST", "localhost")
    AUTH_PORT: int = int(os.getenv("AUTH_PORT", "8080"))
    AUTH_REALM: str = os.getenv("AUTH_REALM", "master")
    
    # OAuth client settings
    OAUTH_CLIENT_ID: str = os.getenv("OAUTH_CLIENT_ID", "mcp-server")
    OAUTH_CLIENT_SECRET: str = os.getenv("OAUTH_CLIENT_SECRET", "UO3rmozkFFkXr0QxPTkzZ0LMXDidIikB")
    
    # Server settings
    MCP_SCOPE: str = os.getenv("MCP_SCOPE", "mcp:tools")
    TRANSPORT: str = os.getenv("TRANSPORT", "streamable-http")
    
    @property
    def server_url(self) -> str:
        """Build the server URL."""
        return f"http://{self.HOST}:{self.PORT}"
    
    @property
    def auth_base_url(self) -> str:
        """Build the auth server base URL."""
        return f"http://{self.AUTH_HOST}:{self.AUTH_PORT}/realms/{self.AUTH_REALM}/"
    
    def validate(self) -> None:
        """Validate configuration."""
        if self.TRANSPORT not in ["sse", "streamable-http"]:
            raise ValueError(f"Invalid transport: {self.TRANSPORT}. Must be 'sse' or 'streamable-http'")


# Global configuration instance
config = Config()
