import os
import subprocess
import urllib.request
import urllib.error
import json
import time

def get_git_commits():
    result = subprocess.run(
        ["git", "log", "--oneline", "-10"],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def generate_release_notes(commits, retries=3):
    api_key = os.environ["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    prompt = f"""You are a technical writer. Based on these git commits, generate clean release notes grouped into Features, Bug Fixes, and Infrastructure changes. Keep it concise and human readable.

Commits:
{commits}

Release notes:"""

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode("utf-8")

    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode("utf-8"))
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                wait = 30 * (attempt + 1)
                print(f"Rate limited, waiting {wait} seconds before retry {attempt + 2}/{retries}...")
                time.sleep(wait)
            else:
                raise

def main():
    print("Fetching recent commits...")
    commits = get_git_commits()

    if not commits:
        print("No commits found.")
        return

    print(f"Commits found:\n{commits}\n")
    print("Generating release notes with Gemini...")

    notes = generate_release_notes(commits)

    print("\n===== RELEASE NOTES =====")
    print(notes)
    print("=========================")

    with open("CHANGELOG.md", "w") as f:
        f.write("# Changelog\n\n")
        f.write(notes)

    print("\nSaved to CHANGELOG.md")

if __name__ == "__main__":
    main()