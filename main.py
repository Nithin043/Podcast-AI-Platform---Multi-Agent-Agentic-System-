"""
main.py
-------
Headless CLI runner for the full platform pipeline.

Usage:
    python main.py --url "URL" --user-id "UUID"
    python main.py --url "URL" --user-id "UUID" --skip-rag
    python main.py --start-scheduler       # Start all user schedulers
"""

import argparse
from dotenv import load_dotenv
load_dotenv()  # Load .env before any agent imports

from database.db import init_db


def main():
    init_db()

    parser = argparse.ArgumentParser(description="PodcastAI Platform CLI")
    parser.add_argument("--url",              help="YouTube video URL to process")
    parser.add_argument("--user-id",          help="User UUID to run pipeline for")
    parser.add_argument("--skip-rag",         action="store_true")
    parser.add_argument("--start-scheduler",  action="store_true",
                        help="Start channel watchers for all active users")
    args = parser.parse_args()

    if args.start_scheduler:
        from scheduler.job_scheduler import start_all_schedulers
        import time
        start_all_schedulers()
        print("[CLI] Scheduler running. Press Ctrl+C to stop.")
        try:
            while True: time.sleep(60)
        except KeyboardInterrupt:
            print("[CLI] Scheduler stopped.")
        return

    if not args.url or not args.user_id:
        parser.error("--url and --user-id are required for pipeline runs")

    from scheduler.task_runner import run_for_user
    results = run_for_user(user_id=args.user_id, video_url=args.url)

    if results:
        print(f"\n✅ Pipeline complete")
        print(f"Blog path:       {results.get('blog_path','N/A')}")
        print(f"Social path:     {results.get('social_path','N/A')}")
        print(f"Newsletter path: {results.get('newsletter_path','N/A')}")
        print(f"Publish status:  {results.get('publish_status',{})}")
    else:
        print("❌ Pipeline failed")


if __name__ == "__main__":
    main()
