"""
CLI-modul för Nexus Repository API
"""

import argparse
import sys
from typing import Optional

from .main import run_server


def create_parser() -> argparse.ArgumentParser:
    """Skapa argument parser"""
    parser = argparse.ArgumentParser(
        prog="nexus-api",
        description="Nexus Repository Manager API Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exempel:
  nexus-api                          # Starta server på standard port 3000
  nexus-api --port 8080              # Starta på port 8080
  nexus-api --host 127.0.0.1         # Starta bara på localhost
  nexus-api --reload                 # Starta med auto-reload för utveckling
  nexus-api --log-level debug        # Starta med debug-loggning
        """
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host att binda till (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=3000,
        help="Port att lyssna på (default: 3000)"
    )
    
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Aktivera auto-reload för utveckling"
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["critical", "error", "warning", "info", "debug", "trace"],
        default="info",
        help="Loggningsnivå (default: info)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="nexus-repository-api 1.0.0"
    )
    
    return parser


def main(args: Optional[list] = None) -> int:
    """Huvudfunktion för CLI"""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    try:
        print(f"🚀 Startar Nexus Repository API på {parsed_args.host}:{parsed_args.port}")
        print(f"📚 API-dokumentation: http://{parsed_args.host}:{parsed_args.port}/docs")
        print(f"🔍 Health check: http://{parsed_args.host}:{parsed_args.port}/health")
        print("🛑 Tryck Ctrl+C för att stoppa servern")
        print()
        
        run_server(
            host=parsed_args.host,
            port=parsed_args.port,
            reload=parsed_args.reload,
            log_level=parsed_args.log_level
        )
        return 0
        
    except KeyboardInterrupt:
        print("\n👋 Servern stoppas...")
        return 0
    except Exception as e:
        print(f"❌ Fel vid start av server: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
