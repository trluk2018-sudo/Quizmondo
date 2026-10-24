import urllib.request
import os

images = {
    # QuizHub / TriviaMatrix - Arcade / Gaming
    "quizhub_hero.jpg": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=1200&q=80", # Retro arcade & gaming screen
    "quizhub_arcade.jpg": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=800&q=80", # Gaming setup / controllers
    "quizhub_esports.jpg": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80", # Esports arena tournament
    "quizhub_trivia.jpg": "https://images.unsplash.com/photo-1606167668584-78701c57f13d?auto=format&fit=crop&w=800&q=80", # Quiz / game board

    # Nest / VitalGreens - Organic, Farm, Healthy Food
    "nest_hero.jpg": "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=1200&q=80", # Fresh organic vegetable harvest bowl
    "nest_harvest.jpg": "https://images.unsplash.com/photo-1610832958506-aa56368176cf?auto=format&fit=crop&w=800&q=80", # Fresh farm produce market
    "nest_juice.jpg": "https://images.unsplash.com/photo-1622597467836-f3285f2131b8?auto=format&fit=crop&w=800&q=80", # Cold-pressed organic green juice
    "nest_salad.jpg": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=80", # Vibrant wholesome salad meal

    # Gym / ApexFit - Strength, Barbell, Athletic
    "gym_hero.jpg": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=1200&q=80", # High intensity gym training
    "gym_barbell.jpg": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80", # Olympic barbell lifting
    "gym_athlete.jpg": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?auto=format&fit=crop&w=800&q=80", # Athletic conditioning
    "gym_crossfit.jpg": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80", # Dumbbells and strength equipment

    # Course / SkillForge - Coding, Masterclass, Tech
    "course_hero.jpg": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80", # Modern digital academy student learning
    "course_coding.jpg": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=800&q=80", # Software engineering code on screen
    "course_laptop.jpg": "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80", # Collaborative tech workshop
    "course_student.jpg": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=800&q=80", # Students learning with laptops

    # Hisoft / Tek Club - Corporate IT, Cloud, Server
    "hisoft_hero.jpg": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80", # Global technology network & cloud
    "hisoft_datacenter.jpg": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&q=80", # Modern enterprise server rack
    "hisoft_cloud.jpg": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&q=80", # Technology engineering team
    "hisoft_office.jpg": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80", # Corporate headquarters
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
