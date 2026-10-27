import urllib.request
import os

images = {
    # QuizHub / TriviaMatrix - Arcade / Gaming
    "quizhub_hero.jpg": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=1200&q=80", # Retro arcade & gaming screen
    "quizhub_arcade.jpg": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=800&q=80", # Gaming setup / controllers
    "quizhub_esports.jpg": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80", # Esports arena tournament
    "quizhub_trivia.jpg": "https://images.unsplash.com/photo-1606167668584-78701c57f13d?auto=format&fit=crop&w=800&q=80", # Quiz / game board
}

target_dir = os.path.join(os.path.dirname(__file__), "app", "static", "img")
os.makedirs(target_dir, exist_ok=True)

for fname, url in images.items():
    dest = os.path.join(target_dir, fname)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            with open(dest, "wb") as f:
                f.write(data)
            print(f"Downloaded {fname} ({len(data)} bytes)")
    except Exception as e:
        print(f"Failed {fname}: {e}")
