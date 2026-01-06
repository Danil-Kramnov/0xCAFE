#!/usr/bin/env python3
"""
0xCAFE - Code before coffee!
Daily coding challenge tracker by Daniel Kramnov
"""

import click
import yaml
import webbrowser
from rich.console import Console
from rich.table import Table
from pathlib import Path
from datetime import datetime

from platforms.leetcode import LeetCodePlatform
from utils.file_manager import FileManager
from utils.git_manager import GitManager
from utils.test_runner import TestRunner

console = Console()


def load_config():
    """Load config.yaml"""
    import os
    print(f"DEBUG: Inside load_config(), cwd={os.getcwd()}")
    print(f"DEBUG: config.yaml exists? {os.path.exists('config.yaml')}")
    with open("config.yaml", "r") as f:
        print("DEBUG: File opened, about to parse YAML")
        result = yaml.safe_load(f)
        print(f"DEBUG: YAML parsed successfully, config keys: {result.keys()}")
        return result


@click.group()
def cli():
    """0xCAFE - Start your day with code, not coffee ☕→💻"""
    pass


@cli.command()
@click.option('--difficulty', type=click.Choice(['Easy', 'Medium', 'Hard']),
              help='Only fetch specific difficulty')
def fetch(difficulty):
    """Fetch today's leetcode daily challenge"""

    import sys
    print(f"DEBUG: sys.argv = {sys.argv}")
    #console.print("\n🔍 Fetching today's challenge...\n", style="bold blue")
    print("\n🔍 Fetching today's challenge...\n")

    print("DEBUG: About to load config...")
    config = load_config()
    print("DEBUG: Config loaded successfully")
    print("DEBUG: About to create platform...")
    platform = LeetCodePlatform(config['leetcode'])
    print("DEBUG: Platform created successfully")
    print("DEBUG: About to fetch challenge...")
    challenge = platform.fetch_daily_challenge()
    print("DEBUG: Challenge fetched successfully")
    
    if not challenge:
        console.print("❌ Failed to fetch challenge", style="bold red")
        console.print("   Check your internet connection", style="dim")
        return
    
    # filter by difficulty if specified
    if difficulty and challenge['difficulty'] != difficulty:
        console.print(f"⏭️  Skipping {challenge['difficulty']} challenge", style="yellow")
        return
    
    # show info
    table = Table(title="📋 Today's Challenge")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Title", challenge['title'])
    table.add_row("Difficulty", challenge['difficulty'])
    table.add_row("Topics", ", ".join(challenge['topics'][:3]))
    table.add_row("URL", challenge['url'])
    
    console.print(table)
    
    # create files
    file_manager = FileManager(config['paths']['challenges_dir'])
    challenge_dir = file_manager.create_challenge_directory(
        challenge['platform'],
        challenge['date'],
        challenge['title_slug']
    )
    
    readme_path = file_manager.create_readme(challenge_dir, challenge)
    solution_path = file_manager.create_solution_file(challenge_dir, challenge)
    
    console.print(f"\n✅ Created files in: {challenge_dir}\n", style="bold green")
    console.print(f"📝 {readme_path}", style="dim")
    console.print(f"💻 {solution_path}\n", style="dim")
    
    # auto commit if enabled
    if config['git']['auto_commit']:
        git_manager = GitManager()
        commit_msg = f"📥 Fetched: {challenge['title']} ({challenge['difficulty']})"
        
        rel_files = [
            str(readme_path),
            str(solution_path)
        ]
        
        git_manager.commit_challenge(rel_files, commit_msg)
    
    console.print("🚀 Ready to code!\n", style="bold green")


@cli.command()
@click.argument('title_slug')
def get(title_slug):
    """
    Fetch specific problem by title slug
    
    Example: python main.py get two-sum
    """
    
    console.print(f"\n🔍 Fetching: {title_slug}...\n", style="bold blue")
    
    config = load_config()
    platform = LeetCodePlatform(config['leetcode'])
    challenge = platform.fetch_challenge_by_id(title_slug)
    
    if not challenge:
        console.print(f"❌ Problem '{title_slug}' not found", style="bold red")
        console.print("   Check the title slug (e.g., 'two-sum')", style="dim")
        return
    
    # show info
    table = Table(title=f"📋 {challenge['title']}")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("ID", challenge['id'])
    table.add_row("Difficulty", challenge['difficulty'])
    table.add_row("Topics", ", ".join(challenge['topics'][:3]))
    table.add_row("URL", challenge['url'])
    
    console.print(table)
    
    # create files
    file_manager = FileManager(config['paths']['challenges_dir'])
    challenge_dir = file_manager.create_challenge_directory(
        challenge['platform'],
        datetime.now().strftime("%Y-%m-%d"),
        challenge['title_slug']
    )
    
    readme_path = file_manager.create_readme(challenge_dir, challenge)
    solution_path = file_manager.create_solution_file(challenge_dir, challenge)
    
    console.print(f"\n✅ Created files in: {challenge_dir}\n", style="bold green")
    
    if config['git']['auto_commit']:
        git_manager = GitManager()
        commit_msg = f"📥 Fetched: {challenge['title']} ({challenge['difficulty']})"
        
        rel_files = [
            str(readme_path),
            str(solution_path)
        ]
        
        git_manager.commit_challenge(rel_files, commit_msg)
    
    console.print("🚀 Ready to code!\n", style="bold green")


@cli.command()
@click.argument('challenge_path', type=click.Path(exists=True))
def test(challenge_path):
    """
    Run local tests for a challenge
    
    Example: python main.py test challenges/leetcode/2025-01-06-two-sum/
    """
    
    challenge_dir = Path(challenge_path)
    
    if not challenge_dir.is_dir():
        console.print(f"❌ Not a directory: {challenge_path}", style="bold red")
        return
    
    console.print(f"\n🧪 Testing solution in: {challenge_dir.name}\n", style="bold blue")
    
    runner = TestRunner(challenge_dir)
    success = runner.run_tests()
    
    if success:
        console.print("🎉 All tests passed! Ready to submit.\n", style="bold green")
    else:
        console.print("💭 Keep working on it!\n", style="yellow")


@cli.command()
@click.argument('challenge_path', type=click.Path(exists=True))
def open(challenge_path):
    """
    Open challenge in browser (for submitting to leetcode)
    
    Example: python main.py open challenges/leetcode/2025-01-06-two-sum/
    """
    
    challenge_dir = Path(challenge_path)
    readme_file = challenge_dir / "README.md"
    
    if not readme_file.exists():
        console.print(f"❌ README not found", style="bold red")
        return
    
    # extract URL from readme
    content = readme_file.read_text()
    import re
    url_match = re.search(r'\*\*URL:\*\* (.+)', content)
    
    if url_match:
        url = url_match.group(1).strip()
        console.print(f"\n🌐 Opening: {url}\n", style="bold blue")
        webbrowser.open(url)
    else:
        console.print(f"❌ URL not found in README", style="bold red")


@cli.command()
@click.argument('challenge_path', type=click.Path(exists=True))
@click.option('--push', is_flag=True, help='Push to remote after commit')
def solve(challenge_path, push):
    """
    Mark challenge as solved and commit
    
    Example: python main.py solve challenges/leetcode/2025-01-06-two-sum/ --push
    """
    
    challenge_dir = Path(challenge_path)
    
    if not challenge_dir.is_dir():
        console.print(f"❌ Not a directory: {challenge_path}", style="bold red")
        return
    
    solution_file = challenge_dir / "solution.py"
    readme_file = challenge_dir / "README.md"
    
    if not solution_file.exists():
        console.print(f"❌ solution.py not found", style="bold red")
        return
    
    # update readme status
    if readme_file.exists():
        content = readme_file.read_text()
        content = content.replace(
            "Status: In Progress",
            f"Status: ✅ Solved"
        )
        content += f"\n- Completed: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        readme_file.write_text(content)
    
    # commit
    config = load_config()
    git_manager = GitManager()
    
    # extract title from directory name
    title = challenge_dir.name.split('-', 3)[-1].replace('-', ' ').title()
    commit_msg = f"✅ Solved: {title}"
    
    rel_files = [
        str(solution_file),
        str(readme_file)
    ]
    
    if git_manager.commit_challenge(rel_files, commit_msg):
        console.print(f"\n🎉 Marked as solved: {title}\n", style="bold green")
        
        if push:
            git_manager.push_to_remote()
    else:
        console.print("\n❌ Failed to commit\n", style="bold red")


@cli.command()
def status():
    """Show your stats and progress"""
    
    config = load_config()
    challenges_dir = Path(config['paths']['challenges_dir']) / "leetcode"
    
    if not challenges_dir.exists():
        console.print("\n📊 No challenges yet!", style="yellow")
        console.print("   Run 'python main.py fetch' to get started\n", style="dim")
        return
    
    total = 0
    solved = 0
    in_progress = 0
    
    # count challenges
    for challenge_dir in challenges_dir.iterdir():
        if challenge_dir.is_dir():
            total += 1
            readme = challenge_dir / "README.md"
            if readme.exists():
                content = readme.read_text()
                if "✅ Solved" in content:
                    solved += 1
                else:
                    in_progress += 1
    
    # display stats
    table = Table(title="📊 Your Stats")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", style="white")
    
    table.add_row("Total Challenges", str(total))
    table.add_row("Solved", f"[green]{solved}[/green]")
    table.add_row("In Progress", f"[yellow]{in_progress}[/yellow]")
    
    if total > 0:
        completion_rate = (solved / total) * 100
        table.add_row("Completion Rate", f"{completion_rate:.1f}%")
    
    console.print("\n")
    console.print(table)
    console.print("\n")


if __name__ == "__main__":
    cli()