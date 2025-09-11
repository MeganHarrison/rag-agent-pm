#!/usr/bin/env python3
"""
CLI script to download Fireflies transcripts as markdown files.
Usage: python download_fireflies_transcripts.py [--limit N] [--output-dir DIR]
"""

import argparse
import asyncio
import sys
from pathlib import Path
from fireflies_client import FirefliesClient


def main():
    parser = argparse.ArgumentParser(
        description="Download Fireflies meeting transcripts as markdown files"
    )
    parser.add_argument(
        "--limit", "-l", 
        type=int, 
        default=10,
        help="Number of transcripts to download (default: 10)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default="fireflies_transcripts",
        help="Output directory for transcripts (default: fireflies_transcripts)"
    )
    parser.add_argument(
        "--api-key", "-k",
        type=str,
        help="Fireflies API key (overrides environment variable)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.limit <= 0:
        print("Error: --limit must be greater than 0")
        sys.exit(1)
    
    # Run the download
    asyncio.run(download_transcripts(args))


async def download_transcripts(args):
    """Download transcripts with the given arguments."""
    try:
        print("=" * 60)
        print("🔥 Fireflies Transcript Downloader")
        print("=" * 60)
        print(f"📥 Downloading last {args.limit} meetings")
        print(f"📁 Output directory: {args.output_dir}")
        print("=" * 60)
        
        # Initialize client
        client = FirefliesClient(api_key=args.api_key)
        
        # Download transcripts
        await client.download_transcripts(
            output_dir=args.output_dir,
            limit=args.limit
        )
        
        print("\n✅ Download completed successfully!")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {str(e)}")
        print("\nPlease ensure you have set the FIREFLIES_API_KEY environment variable")
        print("or provide it using the --api-key parameter.")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()