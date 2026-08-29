#!/usr/bin/env python3
"""
Verification script for Weather Agent setup
Checks if all components are configured correctly
"""
import os
import sys
from pathlib import Path

def check_environment():
    """Check if .env file exists and is configured"""
    print("🔍 Checking environment configuration...")
    
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        env_file = Path(".env")
    
    from dotenv import load_dotenv
    if env_file.exists():
        load_dotenv(dotenv_path=env_file)
    else:
        load_dotenv()
    
    openrouter_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if openrouter_key and openrouter_key != "your_openrouter_api_key_here":
        print(f"✅ OPENROUTER_API_KEY configured ({openrouter_key[:10]}...)")
    elif google_key and google_key != "your_google_api_key_here":
        print(f"✅ GOOGLE_API_KEY configured ({google_key[:10]}...)")
    else:
        print("⚠️  OPENROUTER_API_KEY / GOOGLE_API_KEY not configured in .env")
        print("   To configure OpenRouter: echo 'OPENROUTER_API_KEY=your_key' > 04-lab/mcp-client/.env")
        print("   To configure Gemini:     echo 'GOOGLE_API_KEY=your_key' > 04-lab/mcp-client/.env")
    
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        ("google.adk", "Google ADK"),
        ("openai", "OpenAI"),
        ("litellm", "LiteLLM"),
        ("mcp", "MCP"),
        ("fastmcp", "FastMCP"),
        ("dotenv", "python-dotenv"),
        ("httpx", "httpx"),
    ]
    
    all_installed = True
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} not installed")
            all_installed = False
    
    if not all_installed:
        print("\n   Install with: uv sync")
        print("   Or: pip install google-adk google-generativeai mcp fastmcp python-dotenv httpx")
    
    return all_installed

def check_agent_structure():
    """Check if agent directory structure is correct"""
    print("\n🔍 Checking agent structure...")
    
    base_dir = Path(__file__).parent
    required_files = [
        base_dir / "weather_agent/agent.py",
        base_dir / "weather_agent/__init__.py",
    ]
    
    all_exist = True
    for path in required_files:
        if path.exists():
            print(f"✅ {path.relative_to(base_dir)}")
        else:
            print(f"❌ {path.relative_to(base_dir)} not found")
            all_exist = False
    
    return all_exist

def check_mcp_server():
    """Check if MCP server is accessible"""
    print("\n🔍 Checking MCP server connectivity...")
    
    server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8085/mcp")
    
    try:
        import httpx
        import asyncio
        
        async def test_connection():
            async with httpx.AsyncClient() as client:
                response = await client.get(server_url, timeout=5.0)
                return response.status_code
        
        status_code = asyncio.run(test_connection())
        
        if status_code in [200, 404, 405, 406]:  # FastMCP HTTP endpoint returns 200, 404, 405 or 406 on plain GET
            print(f"✅ MCP server reachable at {server_url} (HTTP {status_code})")
            return True
        else:
            print(f"⚠️  MCP server returned status {status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Cannot reach MCP server ({server_url}): {e}")
        print("   Start server with: cd 04-lab/mcp-server && python weather.py")
        return False

def check_agent_import():
    """Try to import the agent"""
    print("\n🔍 Checking agent import...")
    
    try:
        # Suppress warnings during import
        import warnings
        warnings.filterwarnings("ignore")
        
        sys.path.insert(0, str(Path(__file__).parent))
        from weather_agent import root_agent
        print(f"✅ Agent imported successfully: {root_agent.name}")
        print(f"   Model: {root_agent.model}")
        return True
    except Exception as e:
        print(f"❌ Failed to import agent: {e}")
        return False

def main():
    """Run all verification checks"""
    print("=" * 60)
    print("Weather Agent Setup Verification")
    print("=" * 60)
    print()
    
    checks = [
        check_environment(),
        check_dependencies(),
        check_agent_structure(),
        check_mcp_server(),
        check_agent_import(),
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ All checks passed!")
        print("\n🚀 Ready to start!")
        print("   1. Start server: ./start_server.sh (or: python 04-lab/mcp-server/weather.py)")
        print("   2. Start client: ./start_client.sh (or: adk web --directory 04-lab/mcp-client)")
        print("\n📍 Then open: http://localhost:8000")
        return 0
    else:
        print("❌ Some checks failed")
        print("\n⚠️  Fix the issues above and run this script again")
        return 1

if __name__ == "__main__":
    sys.exit(main())

