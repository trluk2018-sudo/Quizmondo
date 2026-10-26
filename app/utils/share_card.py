import io
from PIL import Image, ImageDraw, ImageFont


def _get_font(size: int, bold: bool = False):
    """Attempt to load system TTF font with fallback to PIL default font."""
    font_names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "FreeSansBold.ttf" if bold else "FreeSans.ttf",
        "SegoeUI.ttf",
        "Helvetica.ttf"
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    try:
        return ImageFont.load_default(size=size)
    except Exception:
        return ImageFont.load_default()


def generate_duel_card_png(p1_name: str, p2_name: str, round_num: int, category_name: str, p1_score: int = 0, p2_score: int = 0, match_code: str = "") -> bytes:
    """Generate high-impact 1200x630 OpenGraph match preview card for WhatsApp / Social shares."""
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), color=(9, 3, 23))  # Dark cosmic purple #090317
    draw = ImageDraw.Draw(img)

    # Ambient double border
    draw.rectangle([(16, 16), (w - 16, h - 16)], outline=(124, 58, 237), width=6)   # Neon violet
    draw.rectangle([(24, 24), (w - 24, h - 24)], outline=(6, 182, 212), width=2)    # Cyan

    # Top Brand Pill
    draw.rounded_rectangle([(300, 45), (900, 105)], radius=30, fill=(28, 12, 60), outline=(147, 51, 234), width=3)
    font_brand = _get_font(26, bold=True)
    draw.text((345, 62), "⚡ QUIZMONDO ARENA • TRIVIA DUEL ⚡", fill=(6, 182, 212), font=font_brand)

    # Match Round & Category Banner
    draw.rounded_rectangle([(120, 130), (1080, 205)], radius=20, fill=(18, 10, 48), outline=(6, 182, 212), width=3)
    font_cat = _get_font(28, bold=True)
    cat_text = f"🔥 ROUND {round_num}: {category_name.upper()} • DUEL IN PLAY"
    draw.text((160, 150), cat_text[:50], fill=(250, 204, 21), font=font_cat)

    # Player 1 Battle Card (Left)
    draw.rounded_rectangle([(100, 235), (490, 485)], radius=24, fill=(15, 8, 38), outline=(6, 182, 212), width=4)
    font_sub = _get_font(20, bold=False)
    font_name = _get_font(32, bold=True)
    font_score = _get_font(30, bold=True)

    draw.text((140, 270), "CHALLENGER (PLAYER 1)", fill=(148, 163, 184), font=font_sub)
    draw.text((140, 315), str(p1_name)[:16], fill=(255, 255, 255), font=font_name)
    draw.rounded_rectangle([(140, 380), (450, 445)], radius=15, fill=(6, 78, 59), outline=(52, 211, 153), width=2)
    draw.text((165, 395), f"SCORE: {p1_score} PTS", fill=(52, 211, 153), font=font_score)

    # VS Emblem (Center)
    draw.ellipse([(545, 305), (655, 415)], fill=(124, 58, 237), outline=(236, 72, 153), width=5)
    font_vs = _get_font(36, bold=True)
    draw.text((572, 342), "VS", fill=(255, 255, 255), font=font_vs)

    # Player 2 Battle Card (Right)
    draw.rounded_rectangle([(710, 235), (1100, 485)], radius=24, fill=(15, 8, 38), outline=(236, 72, 153), width=4)
    draw.text((750, 270), "OPPONENT (PLAYER 2)", fill=(148, 163, 184), font=font_sub)
    draw.text((750, 315), str(p2_name or "Challenger")[:16], fill=(255, 255, 255), font=font_name)
    draw.rounded_rectangle([(750, 380), (1060, 445)], radius=15, fill=(136, 19, 55), outline=(244, 114, 182), width=2)
    draw.text((775, 395), f"SCORE: {p2_score} PTS", fill=(244, 114, 182), font=font_score)

    # Bottom Callout CTA
    draw.rounded_rectangle([(100, 520), (1100, 590)], radius=20, fill=(6, 182, 212), outline=(255, 255, 255), width=2)
    font_cta = _get_font(26, bold=True)
    cta_text = f"👉 TAP CARD TO ENTER THE ARENA & PLAY ROUND {round_num} NOW! 👈"
    draw.text((180, 538), cta_text, fill=(15, 23, 42), font=font_cta)

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def generate_pub_card_png(venue_name: str, pin_code: str, schedule_day: str = "", first_prize: str = "", second_prize: str = "") -> bytes:
    """Generate high-impact 1200x630 OpenGraph pub quiz invite card for WhatsApp / Social shares."""
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), color=(15, 7, 30))  # Dark ambient pub mahogany
    draw = ImageDraw.Draw(img)

    # Glowing amber / gold border
    draw.rectangle([(16, 16), (w - 16, h - 16)], outline=(245, 158, 11), width=6)  # Amber-500
    draw.rectangle([(24, 24), (w - 24, h - 24)], outline=(147, 51, 234), width=2)  # Purple-500

    # Top Brand Pill
    draw.rounded_rectangle([(300, 45), (900, 105)], radius=30, fill=(35, 15, 5), outline=(245, 158, 11), width=3)
    font_brand = _get_font(26, bold=True)
    draw.text((320, 62), "🍻 QUIZMONDO PUB QUIZ • TABLE INVITE 🍻", fill=(251, 191, 36), font=font_brand)

    # Venue Name & Schedule
    font_venue = _get_font(40, bold=True)
    draw.text((100, 140), str(venue_name)[:34], fill=(255, 255, 255), font=font_venue)

    font_sched = _get_font(22, bold=False)
    draw.text((100, 200), f"📅 Schedule: {schedule_day or 'Every Thursday at 20:00 GMT'}", fill=(203, 213, 225), font=font_sched)

    # Big Golden Room PIN Box (Left)
    draw.rounded_rectangle([(100, 250), (550, 490)], radius=25, fill=(24, 10, 45), outline=(245, 158, 11), width=4)
    draw.text((140, 280), "VENUE TABLE ROOM PIN", fill=(251, 191, 36), font=_get_font(22, bold=True))
    draw.text((140, 320), "Enter on your phone to join our table:", fill=(148, 163, 184), font=_get_font(18, bold=False))
    # Big PIN Pill
    draw.rounded_rectangle([(140, 370), (510, 460)], radius=18, fill=(245, 158, 11))
    draw.text((230, 385), str(pin_code or "7742"), fill=(15, 23, 42), font=_get_font(52, bold=True))

    # Tournament Prizes Box (Right)
    draw.rounded_rectangle([(600, 250), (1100, 490)], radius=25, fill=(24, 10, 45), outline=(147, 51, 234), width=4)
    draw.text((640, 280), "🏆 TOURNAMENT PRIZES", fill=(6, 182, 212), font=_get_font(22, bold=True))
    draw.text((640, 330), f"🥇 1st: {first_prize or '£20 Bar Tab Voucher + Trophy'}"[:30], fill=(255, 255, 255), font=_get_font(22, bold=True))
    draw.text((640, 380), f"🥈 2nd: {second_prize or 'Bottle of House Wine for Table'}"[:30], fill=(244, 114, 182), font=_get_font(22, bold=True))
    draw.text((640, 435), "⚡ 5 Themed Rounds • Big-Screen Live Scoring", fill=(148, 163, 184), font=_get_font(18, bold=False))

    # Bottom CTA Banner
    draw.rounded_rectangle([(100, 520), (1100, 590)], radius=20, fill=(245, 158, 11), outline=(255, 255, 255), width=2)
    font_cta = _get_font(26, bold=True)
    draw.text((220, 538), "👉 TAP CARD TO ENTER VENUE & JOIN OUR TABLE SQUAD! 👈", fill=(15, 23, 42), font=font_cta)

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()
