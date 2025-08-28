# Pydantic AI Web Search Agent - Project Planning

## Project Overview
This project aims to build a Pydantic AI agent capable of searching the web using either Brave Search API or SearXNG, depending on environment configuration. The agent will be versatile, allowing for seamless switching between search providers while maintaining consistent functionality and response structure.

## Architecture

### Components
1. **Agent Core (web_agent.py)**
   - Main Pydantic AI agent implementation
   - Handles system prompt and tool integration
   - Manages environment-based configuration

2. **Search Tools (search_tools.py)**
   - Brave Search implementation
   - SearXNG implementation
   - Common interface for both search providers

3. **Schemas (schemas.py)**
   - Defines Pydantic models for search results and provider config

4. **Config (settings.py)**
   - Reads environment variables
   - Determines which provider to use at runtime

5. **MCP Server (server.py)**
   - FastMCP server exposing the `web_search` tool
   - Entry point for MCP-compatible clients

### Tech Stack
- **Pydantic AI**: Core agent framework
- **Python 3.10+**: Base language
- **httpx**: For async HTTP calls
- **python-dotenv**: For environment variable management
- **pytest**: For unit testing
- **FastMCP**: To expose the agent as a server

## Search Provider Integration

### Brave Search
- **API Endpoint**: https://api.search.brave.com/res/v1/web/search
- **Authentication**: API key via `X-Subscription-Token` header
- **Query Parameters**: q (query), count (results), offset, country, search_lang, freshness, safesearch
- **Key Features**: Web search, news, videos, images
- **Configuration**: `BRAVE_API_KEY` environment variable

### SearXNG
- **API Endpoint**: Self-hosted or public instance (via SEARXNG_BASE_URL)
- **Authentication**: None required (for most instances)
- **Query Parameters**: q (query), format=json, categories, engines, language
- **Key Features**: Metasearch capabilities, privacy-focused
- **Configuration**: `SEARXNG_BASE_URL` environment variable

## System Prompt Strategy
The agent will use a dynamic system prompt that:
1. Explains its capability to search the web
2. Indicates which search provider is being used
3. Provides relevant disclaimers about search results
4. Includes instructions on how to format and present search results

## Agent Functionality

### Primary Features
- Web search with query customization
- Configurable number of results
- Consistent response formatting
- Error handling and rate limit management
- Automatic provider selection based on environment

### Agent Input/Output Structure
- **Input**: Natural language queries
- **Output**: Structured search results with:
  - Title
  - URL
  - Snippet/description
  - Source attribution

## Testing Strategy
- Unit test each search tool independently
- Mock HTTP responses for predictable testing
- Verify provider selection logic for different env configurations
- Test error conditions (invalid API key, network failures, empty env)
- Integration tests with a local SearXNG instance
