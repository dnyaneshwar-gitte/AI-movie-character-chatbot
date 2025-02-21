import requests
from bs4 import BeautifulSoup
from database import insert_dialogue

def scrape_movie_script(url, character):
    """Scrapes movie script and stores dialogues in MongoDB."""
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch page: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Try finding the script inside <pre> or <td class="scrtext">
    script = soup.find("pre") or soup.find("td", class_="scrtext")
    
    if not script:
        print("❌ No script found! It may be a PDF or external link.")
        return

    print("✅ Script found! Extracting dialogues...")  # Debugging output

    # Convert character name to lowercase for case-insensitive matching
    character_lower = character.lower()
    
    # Split text into lines
    lines = script.get_text().split("\n")
    
    found = False  # Track if we found any dialogues
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Convert script line to lowercase for comparison
        if line.lower() == character_lower:
            if i + 1 < len(lines):  # Ensure there's a next line
                dialogue = lines[i + 1].strip()
                if dialogue:
                    print(f"📌 Found Dialogue: {dialogue}")  # Debugging output
                    insert_dialogue(character, dialogue)
                    found = True

    if not found:
        print(f"⚠️ No dialogues found for {character}!")
