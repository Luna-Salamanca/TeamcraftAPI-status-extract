# teamcraft_api/__main__.py
import argparse
from teamcraft_api.core.api import TeamcraftAPI
from teamcraft_api.processing.status_handler import lookup_status_or_action
from teamcraft_api.processing.batch_processor import batch_process_status
from pathlib import Path
import logging
import json
import sys

log_path = Path("logs/teamcraft.log")
log_path.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description="Teamcraft API CLI",
        epilog="""
Examples:
  python -m teamcraft_api --status "Bloodbath"
  python -m teamcraft_api --batch ./data/status_list.txt --quiet
  python -m teamcraft_api --status "Damage Up" --output ./custom_folder
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--status", type=str, help="Single status/action name to search")
    group.add_argument("--batch", type=str, help="Path to a file containing a list of statuses")
    parser.add_argument("--quiet", action="store_true", help="Suppress console output during batch processing")
    parser.add_argument("--output", type=str, help="Custom output directory")

    args = parser.parse_args()

    try:
        if args.status:
            api = TeamcraftAPI(quiet=args.quiet, base_dir=args.output)
            result = lookup_status_or_action(api, args.status)
            if result:
                logger.info(f"Found as {result['type']}: {args.status}")
                logger.info(json.dumps(result['data'], indent=4, ensure_ascii=False))
            else:
                logger.error(f"No data found for: {args.status}")

        elif args.batch:
            path = Path(args.batch)
            if not path.exists():
                logger.error(f"File not found: {args.batch}")
                return
            api = TeamcraftAPI(quiet=args.quiet, base_dir=args.output)
            batch_process_status(api, args.batch)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
