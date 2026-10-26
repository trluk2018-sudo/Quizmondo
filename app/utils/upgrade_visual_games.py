import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRIVIA_IMG_DIR = os.path.join(BASE_DIR, 'static', 'img', 'trivia')
MEGA_JSON_PATH = os.path.join(BASE_DIR, 'data', 'mega_questions_3000.json')

for sub in ('flags', 'badges', 'logos', 'shapes'):
    os.makedirs(os.path.join(TRIVIA_IMG_DIR, sub), exist_ok=True)


def write_svg(subfolder, filename, inner_svg, viewbox="0 0 300 180"):
    path = os.path.join(TRIVIA_IMG_DIR, subfolder, filename)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" width="100%" height="100%">\n{inner_svg}\n</svg>\n'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(svg)
    return f'/static/img/trivia/{subfolder}/{filename}'


def build_all_visual_assets():
    # =========================================================================
    # 1. FLAGS (36 clean geometric national flags without text labels)
    # =========================================================================
    flags_defs = [
        ('france.svg', 'France', ['Germany', 'Italy', 'Netherlands'],
         '<rect width="100" height="180" fill="#002395"/><rect x="100" width="100" height="180" fill="#FFFFFF"/><rect x="200" width="100" height="180" fill="#ED2939"/>',
         'The French Tricolore features vertical bands of blue, white, and red.'),
        ('germany.svg', 'Germany', ['Belgium', 'Austria', 'Netherlands'],
         '<rect width="300" height="60" fill="#000000"/><rect y="60" width="300" height="60" fill="#DD0000"/><rect y="120" width="300" height="60" fill="#FFCE00"/>',
         'Germany\'s flag has three equal horizontal bands of black, red, and gold.'),
        ('italy.svg', 'Italy', ['Ireland', 'Mexico', 'Hungary'],
         '<rect width="100" height="180" fill="#009246"/><rect x="100" width="100" height="180" fill="#FFFFFF"/><rect x="200" width="100" height="180" fill="#CE2B37"/>',
         'Italy\'s Il Tricolore features vertical bands of green, white, and red.'),
        ('japan.svg', 'Japan', ['South Korea', 'Bangladesh', 'Palau'],
         '<rect width="300" height="180" fill="#FFFFFF"/><circle cx="150" cy="90" r="54" fill="#BC002D"/>',
         'Japan\'s Nisshoki flag displays a crimson sun disc centered on a white field.'),
        ('brazil.svg', 'Brazil', ['Argentina', 'Colombia', 'Jamaica'],
         '<rect width="300" height="180" fill="#009739"/><polygon points="150,20 275,90 150,160 25,90" fill="#FEDD00"/><circle cx="150" cy="90" r="42" fill="#012169"/><path d="M112,85 Q150,105 188,85" stroke="#FFFFFF" stroke-width="6" fill="none"/>',
         'Brazil\'s flag features a yellow diamond on a green field with a starry blue celestial globe.'),
        ('uk.svg', 'United Kingdom', ['Australia', 'New Zealand', 'Iceland'],
         '<rect width="300" height="180" fill="#012169"/><path d="M0,0 L300,180 M300,0 L0,180" stroke="#FFFFFF" stroke-width="32"/><path d="M0,0 L300,180 M300,0 L0,180" stroke="#C8102E" stroke-width="16"/><path d="M150,0 V180 M0,90 H300" stroke="#FFFFFF" stroke-width="48"/><path d="M150,0 V180 M0,90 H300" stroke="#C8102E" stroke-width="28"/>',
         'The Union Jack combines the crosses of St George, St Andrew, and St Patrick.'),
        ('usa.svg', 'United States', ['Liberia', 'Malaysia', 'Puerto Rico'],
         '<rect width="300" height="180" fill="#B22234"/><g fill="#FFFFFF"><rect y="14" width="300" height="14"/><rect y="42" width="300" height="14"/><rect y="70" width="300" height="14"/><rect y="98" width="300" height="14"/><rect y="126" width="300" height="14"/><rect y="154" width="300" height="14"/></g><rect width="130" height="98" fill="#3C3B6E"/><g fill="#FFFFFF"><circle cx="25" cy="22" r="5"/><circle cx="65" cy="22" r="5"/><circle cx="105" cy="22" r="5"/><circle cx="45" cy="48" r="5"/><circle cx="85" cy="48" r="5"/><circle cx="25" cy="74" r="5"/><circle cx="65" cy="74" r="5"/><circle cx="105" cy="74" r="5"/></g>',
         'The Stars and Stripes features 13 horizontal stripes and a blue canton of white stars.'),
        ('canada.svg', 'Canada', ['Peru', 'Austria', 'Switzerland'],
         '<rect width="75" height="180" fill="#FF0000"/><rect x="75" width="150" height="180" fill="#FFFFFF"/><rect x="225" width="75" height="180" fill="#FF0000"/><polygon points="150,35 164,68 192,62 175,92 190,104 156,104 156,145 144,145 144,104 110,104 125,92 108,62 136,68" fill="#FF0000"/>',
         'Canada\'s flag features a red stylized 11-pointed maple leaf centered on a white square.'),
        ('ireland.svg', 'Ireland', ['Italy', 'Ivory Coast', 'India'],
         '<rect width="100" height="180" fill="#169B62"/><rect x="100" width="100" height="180" fill="#FFFFFF"/><rect x="200" width="100" height="180" fill="#FF883E"/>',
         'Ireland\'s tricolor has vertical bands of green, white, and orange starting with green at the hoist.'),
        ('netherlands.svg', 'Netherlands', ['Russia', 'France', 'Croatia'],
         '<rect width="300" height="60" fill="#AE1C28"/><rect y="60" width="300" height="60" fill="#FFFFFF"/><rect y="120" width="300" height="60" fill="#21468B"/>',
         'The Dutch flag features horizontal bands of bright vermilion red, white, and cobalt blue.'),
        ('belgium.svg', 'Belgium', ['Germany', 'Romania', 'Chad'],
         '<rect width="100" height="180" fill="#000000"/><rect x="100" width="100" height="180" fill="#FDDA24"/><rect x="200" width="100" height="180" fill="#EF3340"/>',
         'Belgium\'s flag has vertical bands of black, yellow, and red.'),
        ('sweden.svg', 'Sweden', ['Finland', 'Norway', 'Denmark'],
         '<rect width="300" height="180" fill="#006AA7"/><rect x="85" width="32" height="180" fill="#FECC02"/><rect y="74" width="300" height="32" fill="#FECC02"/>',
         'Sweden\'s flag displays a golden yellow Nordic cross on a sky-blue field.'),
        ('norway.svg', 'Norway', ['Iceland', 'Denmark', 'Finland'],
         '<rect width="300" height="180" fill="#BA0C2F"/><rect x="80" width="44" height="180" fill="#FFFFFF"/><rect y="68" width="300" height="44" fill="#FFFFFF"/><rect x="88" width="28" height="180" fill="#00205B"/><rect y="76" width="300" height="28" fill="#00205B"/>',
         'Norway\'s flag features a dark blue Nordic cross outlined in white on a crimson red background.'),
        ('denmark.svg', 'Denmark', ['Switzerland', 'Austria', 'Norway'],
         '<rect width="300" height="180" fill="#C8102E"/><rect x="85" width="32" height="180" fill="#FFFFFF"/><rect y="74" width="300" height="32" fill="#FFFFFF"/>',
         'Denmark\'s Dannebrog features a white Nordic cross on a red field.'),
        ('finland.svg', 'Finland', ['Sweden', 'Greece', 'Scotland'],
         '<rect width="300" height="180" fill="#FFFFFF"/><rect x="85" width="36" height="180" fill="#002F6C"/><rect y="72" width="300" height="36" fill="#002F6C"/>',
         'Finland\'s Siniristilippu features a blue Nordic cross on a white background representing snow and lakes.'),
        ('switzerland.svg', 'Switzerland', ['Denmark', 'Tonga', 'Georgia'],
         '<rect width="300" height="180" fill="#DA291C"/><rect x="130" y="35" width="40" height="110" fill="#FFFFFF"/><rect x="95" y="70" width="110" height="40" fill="#FFFFFF"/>',
         'Switzerland\'s flag displays a bold equilateral white cross in the center of a red field.'),
        ('jamaica.svg', 'Jamaica', ['South Africa', 'Scotland', 'Brazil'],
         '<rect width="300" height="180" fill="#000000"/><polygon points="0,0 300,0 150,90" fill="#009B3A"/><polygon points="0,180 300,180 150,90" fill="#009B3A"/><path d="M0,0 L300,180 M300,0 L0,180" stroke="#FED100" stroke-width="28"/>',
         'Jamaica\'s flag is the only national flag containing neither red, white, nor blue (green, gold, and black).'),
        ('ukraine.svg', 'Ukraine', ['Sweden', 'Poland', 'Colombia'],
         '<rect width="300" height="90" fill="#0057B7"/><rect y="90" width="300" height="90" fill="#FFD700"/>',
         'Ukraine\'s flag features two equal horizontal bands of azure blue over golden yellow.'),
        ('poland.svg', 'Poland', ['Indonesia', 'Monaco', 'Austria'],
         '<rect width="300" height="90" fill="#FFFFFF"/><rect y="90" width="300" height="90" fill="#DC143C"/>',
         'Poland\'s flag consists of a white top band and a crimson red bottom band.'),
        ('austria.svg', 'Austria', ['Latvia', 'Peru', 'Lebanon'],
         '<rect width="300" height="60" fill="#ED2939"/><rect y="60" width="300" height="60" fill="#FFFFFF"/><rect y="120" width="300" height="60" fill="#ED2939"/>',
         'Austria\'s flag features three equal horizontal bands of red, white, and red.'),
        ('nigeria.svg', 'Nigeria', ['Ireland', 'Pakistan', 'Saudi Arabia'],
         '<rect width="100" height="180" fill="#008751"/><rect x="100" width="100" height="180" fill="#FFFFFF"/><rect x="200" width="100" height="180" fill="#008751"/>',
         'Nigeria\'s flag has three vertical bands of green, white, and green.'),
        ('argentina.svg', 'Argentina', ['Uruguay', 'Greece', 'Honduras'],
         '<rect width="300" height="60" fill="#74ACDF"/><rect y="60" width="300" height="60" fill="#FFFFFF"/><rect y="120" width="300" height="60" fill="#74ACDF"/><circle cx="150" cy="90" r="18" fill="#F6B40E" stroke="#85340A" stroke-width="2"/>',
         'Argentina\'s flag features sky-blue and white triband stripes with the golden Sun of May in the center.'),
        ('colombia.svg', 'Colombia', ['Venezuela', 'Romania', 'Spain'],
         '<rect width="300" height="90" fill="#FCD116"/><rect y="90" width="300" height="45" fill="#003893"/><rect y="135" width="300" height="45" fill="#CE1126"/>',
         'Colombia\'s flag has a wide yellow top half over blue and red horizontal stripes.'),
        ('thailand.svg', 'Thailand', ['Costa Rica', 'Netherlands', 'North Korea'],
         '<rect width="300" height="30" fill="#A51931"/><rect y="30" width="300" height="30" fill="#F4F5F8"/><rect y="60" width="300" height="60" fill="#2D2A4A"/><rect y="120" width="300" height="30" fill="#F4F5F8"/><rect y="150" width="300" height="30" fill="#A51931"/>',
         'Thailand\'s Trairanga flag has five horizontal stripes of red, white, double-width navy blue, white, and red.'),
        ('greece.svg', 'Greece', ['Finland', 'Israel', 'Uruguay'],
         '<rect width="300" height="180" fill="#0D5EAF"/><g fill="#FFFFFF"><rect y="20" width="300" height="20"/><rect y="60" width="300" height="20"/><rect y="100" width="300" height="20"/><rect y="140" width="300" height="20"/></g><rect width="100" height="100" fill="#0D5EAF"/><rect x="40" width="20" height="100" fill="#FFFFFF"/><rect y="40" width="100" height="20" fill="#FFFFFF"/>',
         'Greece\'s flag features nine alternating blue and white stripes with a white cross in the upper-left canton.'),
        ('scotland.svg', 'Scotland', ['Greece', 'Finland', 'Jamaica'],
         '<rect width="300" height="180" fill="#005EB8"/><path d="M0,0 L300,180 M300,0 L0,180" stroke="#FFFFFF" stroke-width="34"/>',
         'Scotland\'s Saltire features a white diagonal St Andrew\'s Cross on a sky-blue field.'),
        ('bangladesh.svg', 'Bangladesh', ['Japan', 'Palau', 'Vietnam'],
         '<rect width="300" height="180" fill="#006A4E"/><circle cx="138" cy="90" r="50" fill="#F42A41"/>',
         'Bangladesh\'s flag displays a red disc slightly offset toward the hoist on a dark bottle-green field.'),
        ('palau.svg', 'Palau', ['Japan', 'Ukraine', 'Kazakhstan'],
         '<rect width="300" height="180" fill="#4AADD6"/><circle cx="135" cy="90" r="50" fill="#FFDE00"/>',
         'Palau\'s flag features a golden-yellow full moon disc on an ocean-blue field.'),
        ('vietnam.svg', 'Vietnam', ['China', 'Turkey', 'Morocco'],
         '<rect width="300" height="180" fill="#DA251D"/><polygon points="150,35 164,78 208,78 172,104 185,146 150,120 115,146 128,104 92,78 136,78" fill="#FFFF00"/>',
         'Vietnam\'s flag displays a large five-pointed golden star centered on a bright red background.'),
        ('morocco.svg', 'Morocco', ['Vietnam', 'Turkey', 'Tunisia'],
         '<rect width="300" height="180" fill="#C1272D"/><polygon points="150,45 162,82 200,82 169,104 181,140 150,118 119,140 131,104 100,82 138,82" fill="none" stroke="#006233" stroke-width="7"/>',
         'Morocco\'s flag features an emerald-green interlaced pentagram (Seal of Solomon) on a deep red field.'),
        ('somalia.svg', 'Somalia', ['Vietnam', 'Micronesia', 'Honduras'],
         '<rect width="300" height="180" fill="#4189DD"/><polygon points="150,40 163,80 205,80 171,104 184,144 150,120 116,144 129,104 95,80 137,80" fill="#FFFFFF"/>',
         'Somalia\'s flag features a single five-pointed white Star of Unity centered on a light blue field.'),
        ('south_africa.svg', 'South Africa', ['Jamaica', 'Kenya', 'Zimbabwe'],
         '<rect width="300" height="90" fill="#E03C31"/><rect y="90" width="300" height="90" fill="#001489"/><polygon points="0,0 135,90 0,180" fill="#000000"/><path d="M0,0 L145,90 L300,90 M0,180 L145,90" stroke="#FFFFFF" stroke-width="38" fill="none"/><path d="M0,0 L145,90 L300,90 M0,180 L145,90" stroke="#007749" stroke-width="24" fill="none"/><polyline points="0,20 105,90 0,160" stroke="#FFB81C" stroke-width="14" fill="none"/>',
         'South Africa\'s Rainbow Nation flag features a green Y-pall converging across red, blue, black, gold, and white.'),
        ('india.svg', 'India', ['Ireland', 'Niger', 'Hungary'],
         '<rect width="300" height="60" fill="#FF9933"/><rect y="60" width="300" height="60" fill="#FFFFFF"/><rect y="120" width="300" height="60" fill="#138808"/><circle cx="150" cy="90" r="22" fill="none" stroke="#000080" stroke-width="4"/><circle cx="150" cy="90" r="4" fill="#000080"/>',
         'India\'s Tiranga features saffron, white, and green horizontal bands with the 24-spoke navy blue Ashoka Chakra.'),
        ('spain.svg', 'Spain', ['Portugal', 'Colombia', 'Belgium'],
         '<rect width="300" height="45" fill="#AA151B"/><rect y="45" width="300" height="90" fill="#F1BF00"/><rect y="135" width="300" height="45" fill="#AA151B"/><rect x="70" y="65" width="32" height="46" rx="8" fill="#AA151B" stroke="#FFFFFF" stroke-width="3"/>',
         'Spain\'s Rojigualda features red top and bottom bands with a double-width yellow middle band and royal crest.'),
        ('iceland.svg', 'Iceland', ['Norway', 'Finland', 'Sweden'],
         '<rect width="300" height="180" fill="#02529C"/><rect x="80" width="44" height="180" fill="#FFFFFF"/><rect y="68" width="300" height="44" fill="#FFFFFF"/><rect x="88" width="28" height="180" fill="#DC1E35"/><rect y="76" width="300" height="28" fill="#DC1E35"/>',
         'Iceland\'s flag features a fiery red Nordic cross outlined in snow-white on a deep Atlantic-blue field.'),
        ('turkey.svg', 'Turkey', ['Tunisia', 'Pakistan', 'Morocco'],
         '<rect width="300" height="180" fill="#E30A17"/><circle cx="120" cy="90" r="45" fill="#FFFFFF"/><circle cx="132" cy="90" r="36" fill="#E30A17"/><polygon points="185,90 162,76 170,102 150,84 176,84" fill="#FFFFFF"/>',
         'Turkey\'s Al Bayrak displays a white waxing crescent moon and star on a bright crimson background.')
    ]

    flag_questions = []
    prompt_templates_flag = [
        "VISUAL FLAG MATCH: Which country's national flag is shown in the visual clue below?",
        "FLAG CHALLENGE: Identify the sovereign nation represented by this flag:",
        "MATCH THE FLAG: Which nation flies the flag displayed below?",
        "WORLD FLAGS VISUAL: Look at the colors and pattern—which country does this flag belong to?"
    ]
    for idx, (fname, country, distractors, svg_body, expl) in enumerate(flags_defs):
        url = write_svg('flags', fname, svg_body)
        for v_idx in range(4):
            opts_list = [country] + distractors
            # Rotate correct answer position deterministically
            shift = (idx + v_idx) % 4
            rotated = opts_list[shift:] + opts_list[:shift]
            letters = ['A', 'B', 'C', 'D']
            options = {letters[i]: rotated[i] for i in range(4)}
            correct_letter = next(k for k, val in options.items() if val == country)
            prompts = [
                f"VISUAL FLAG MATCH: Which country flies the national flag shown below? (#{idx+1})",
                f"MATCH THE FLAG: Identify the nation represented by this flag design (#{idx+1}):",
                f"SPEED FLAG SPOTTER: Which sovereign country's flag is displayed in the image below? (#{idx+1})",
                f"WORLD FLAG CHALLENGE: Look at the colors and emblem—which nation does this flag belong to? (#{idx+1})"
            ]
            flag_questions.append({
                'prompt': prompts[v_idx],
                'type': 'image',
                'media_url': url,
                'options': options,
                'correct': correct_letter,
                'explanation': expl,
                'difficulty': 'easy' if v_idx < 3 else 'medium'
            })

    # =========================================================================
    # 2. FOOTBALL BADGES / CRESTS (36 clean visual club crests without name spoilers)
    # =========================================================================
    badges_defs = [
        ('arsenal.svg', 'Arsenal FC', ['Chelsea FC', 'Liverpool FC', 'AS Roma'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><path d="M100 20 L175 45 L160 175 Q100 220 100 220 Q40 175 25 175 L25 45 Z" fill="#EF0107" stroke="#9C824A" stroke-width="7"/><rect x="45" y="108" width="110" height="20" rx="6" fill="#9C824A"/><circle cx="75" cy="136" r="20" fill="#0f172a" stroke="#9C824A" stroke-width="7"/>',
         'Arsenal FC\'s iconic red and gold shield features a golden artillery cannon honoring its Woolwich origins.'),
        ('liverpool.svg', 'Liverpool FC', ['Manchester United', 'SL Benfica', 'Bayern Munich'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><path d="M100 20 L170 48 L155 178 Q100 220 100 220 Q45 178 30 178 L30 48 Z" fill="#C8102E" stroke="#F6EB61" stroke-width="6"/><path d="M100 65 C80 85 75 125 100 155 C125 125 120 85 100 65 Z" fill="#F6EB61"/><circle cx="100" cy="58" r="10" fill="#F6EB61"/>',
         'Liverpool FC\'s crimson shield features the mythical golden Liver Bird holding a piece of laver seaweed.'),
        ('chelsea.svg', 'Chelsea FC', ['Manchester City', 'Everton FC', 'Rangers FC'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><circle cx="100" cy="120" r="82" fill="#034694" stroke="#DBA111" stroke-width="8"/><circle cx="100" cy="120" r="56" fill="#FFFFFF" stroke="#034694" stroke-width="4"/><path d="M88 85 L112 85 L105 155 L95 155 Z" fill="#034694"/><circle cx="100" cy="80" r="14" fill="#034694"/><line x1="115" y1="68" x2="115" y2="165" stroke="#ED1C24" stroke-width="5"/>',
         'Chelsea FC\'s roundel crest features a blue heraldic lion rampant regardant holding a red staff.'),
        ('man_utd.svg', 'Manchester United', ['Liverpool FC', 'AC Milan', 'Nottingham Forest'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><path d="M40 35 H160 V150 Q100 215 40 150 Z" fill="#DA291C" stroke="#FBE122" stroke-width="7"/><rect x="55" y="50" width="90" height="32" rx="4" fill="#FBE122"/><path d="M90 105 L100 90 L110 105 L105 155 L95 155 Z" fill="#FBE122"/><line x1="125" y1="90" x2="125" y2="160" stroke="#FBE122" stroke-width="5"/>',
         'Manchester United\'s red and gold crest features a sailing ship above a Red Devil holding a golden trident.'),
        ('man_city.svg', 'Manchester City', ['Chelsea FC', 'Napoli', 'Lazio'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><circle cx="100" cy="120" r="82" fill="#6CABDD" stroke="#1C2C5B" stroke-width="8"/><circle cx="100" cy="120" r="56" fill="#FFFFFF"/><path d="M68 85 H132 V135 Q100 168 68 135 Z" fill="#6CABDD" stroke="#1C2C5B" stroke-width="3"/><circle cx="100" cy="135" r="12" fill="#D42E12"/>',
         'Manchester City\'s sky-blue circular crest features a golden ship and the red Lancashire Rose.'),
        ('tottenham.svg', 'Tottenham Hotspur', ['Real Madrid', 'Swansea City', 'Leeds United'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><circle cx="100" cy="175" r="28" fill="none" stroke="#FFFFFF" stroke-width="6"/><path d="M100 45 C82 70 80 115 100 147 C120 115 118 70 100 45 Z" fill="#FFFFFF"/><polygon points="100,32 92,48 108,48" fill="#FFFFFF"/>',
         'Tottenham Hotspur\'s minimalist navy and white emblem features a fighting cockerel standing atop a vintage football.'),
        ('real_madrid.svg', 'Real Madrid', ['Valencia CF', 'Chelsea FC', 'LA Galaxy'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><polygon points="70,48 85,24 100,42 115,24 130,48" fill="#FEBE10" stroke="#EE324E" stroke-width="3"/><circle cx="100" cy="130" r="68" fill="#FFFFFF" stroke="#FEBE10" stroke-width="8"/><line x1="52" y1="82" x2="148" y2="178" stroke="#00529F" stroke-width="18"/>',
         'Real Madrid\'s golden-rimmed round crest is topped by the Spanish Royal Crown and a diagonal purple/blue sash.'),
        ('barcelona.svg', 'FC Barcelona', ['AC Milan', 'Crystal Palace', 'FC Basel'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><path d="M35 40 H165 V140 Q100 215 35 140 Z" fill="#A50044" stroke="#EDBB00" stroke-width="7"/><rect x="42" y="46" width="58" height="52" fill="#FFFFFF"/><line x1="71" y1="46" x2="71" y2="98" stroke="#DB0030" stroke-width="12"/><line x1="42" y1="72" x2="100" y2="72" stroke="#DB0030" stroke-width="12"/><rect x="100" y="46" width="58" height="52" fill="#FCD116"/><rect x="65" y="106" width="22" height="65" fill="#004D98"/><rect x="112" y="106" width="22" height="65" fill="#004D98"/><circle cx="100" cy="145" r="14" fill="#EDBB00"/>',
         'FC Barcelona\'s crest combines St George\'s Cross, the Catalan Senyera stripes, and Blaugrana bars with a gold ball.'),
        ('ac_milan.svg', 'AC Milan', ['Inter Milan', 'Bournemouth', 'Bayer Leverkusen'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><ellipse cx="100" cy="120" rx="68" ry="88" fill="#FFFFFF" stroke="#FB090B" stroke-width="7"/><path d="M40 70 V170 M60 45 V195 M80 38 V202" stroke="#000000" stroke-width="10"/><path d="M50 55 V185 M70 40 V200 M90 36 V204" stroke="#FB090B" stroke-width="10"/><line x1="132" y1="50" x2="132" y2="190" stroke="#FB090B" stroke-width="16"/><line x1="102" y1="120" x2="162" y2="120" stroke="#FB090B" stroke-width="16"/>',
         'AC Milan\'s oval badge pairs the red-and-black Rossoneri stripes on the left with the red Cross of St Ambrose on the right.'),
        ('inter_milan.svg', 'Inter Milan', ['Atalanta', 'FC Porto', 'Chelsea FC'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><circle cx="100" cy="120" r="80" fill="#010E80" stroke="#C5A059" stroke-width="8"/><circle cx="100" cy="120" r="58" fill="#000000" stroke="#FFFFFF" stroke-width="5"/><circle cx="100" cy="120" r="34" fill="#010E80" stroke="#C5A059" stroke-width="5"/>',
         'Inter Milan\'s Nerazzurri circular crest features concentric rings of royal blue, black, gold, and white.'),
        ('juventus.svg', 'Juventus', ['Newcastle United', 'Udinese', 'Fulham FC'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><path d="M50 35 H150 V145 Q100 210 50 145 Z" fill="#000000" stroke="#FFFFFF" stroke-width="7"/><rect x="65" y="42" width="18" height="125" fill="#FFFFFF"/><rect x="100" y="42" width="18" height="135" fill="#FFFFFF"/><rect x="132" y="42" width="12" height="115" fill="#FFFFFF"/>',
         'Juventus\' Bianconeri crest features iconic black-and-white vertical zebra stripes inside a modern shield.'),
        ('bayern.svg', 'Bayern Munich', ['RB Leipzig', 'Ajax', 'Monaco'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><circle cx="100" cy="120" r="82" fill="#DC052D" stroke="#FFFFFF" stroke-width="6"/><circle cx="100" cy="120" r="52" fill="#0066B2" stroke="#FFFFFF" stroke-width="5"/><polygon points="100,72 135,120 100,168 65,120" fill="#FFFFFF"/><polygon points="75,95 100,120 75,145 55,120" fill="#FFFFFF"/><polygon points="125,95 145,120 125,145 100,120" fill="#FFFFFF"/>',
         'Bayern Munich\'s red circular badge encloses the blue-and-white lozenge diamond pattern of the Bavarian flag.'),
        ('dortmund.svg', 'Borussia Dortmund', ['Wolverhampton Wanderers', 'Villarreal CF', 'Watford FC'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><circle cx="100" cy="120" r="82" fill="#FDE100" stroke="#000000" stroke-width="10"/><circle cx="100" cy="120" r="64" fill="none" stroke="#000000" stroke-width="5"/><polygon points="100,70 140,150 60,150" fill="#000000"/>',
         'Borussia Dortmund\'s unmistakable electric-yellow and jet-black circular badge represents Die Schwarzgelben.'),
        ('psg.svg', 'Paris Saint-Germain', ['Lyon', 'Rangers FC', 'Crystal Palace'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><circle cx="100" cy="120" r="82" fill="#004170" stroke="#FFFFFF" stroke-width="6"/><circle cx="100" cy="120" r="60" fill="#004170" stroke="#DA291C" stroke-width="5"/><polygon points="100,62 136,162 118,162 100,105 82,162 64,162" fill="#DA291C" stroke="#FFFFFF" stroke-width="3"/><circle cx="100" cy="148" r="8" fill="#FEBE10"/>',
         'Paris Saint-Germain\'s navy circular crest features a crimson silhouette of the Eiffel Tower over a golden fleur-de-lis.'),
        ('celtic.svg', 'Celtic FC', ['Real Betis', 'Sporting CP', 'Werder Bremen'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><circle cx="100" cy="120" r="80" fill="#018749" stroke="#FFFFFF" stroke-width="8"/><circle cx="100" cy="120" r="56" fill="#FFFFFF"/><circle cx="84" cy="104" r="18" fill="#018749"/><circle cx="116" cy="104" r="18" fill="#018749"/><circle cx="84" cy="136" r="18" fill="#018749"/><circle cx="116" cy="136" r="18" fill="#018749"/>',
         'Celtic FC\'s emerald-green and white circular crest features a four-leaf shamrock clover in the center.'),
        ('west_ham.svg', 'West Ham United', ['Aston Villa', 'Burnley FC', 'Trabzonspor'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><path d="M35 35 H165 V145 Q100 215 35 145 Z" fill="#7A263A" stroke="#1BB1E7" stroke-width="8"/><line x1="60" y1="165" x2="140" y2="75" stroke="#F3D459" stroke-width="10"/><line x1="140" y1="165" x2="60" y2="75" stroke="#F3D459" stroke-width="10"/><rect x="122" y="62" width="28" height="16" transform="rotate(45 136 70)" fill="#F3D459"/><rect x="50" y="62" width="28" height="16" transform="rotate(-45 64 70)" fill="#F3D459"/>',
         'West Ham United\'s claret and sky-blue shield displays a pair of crossed golden riveting hammers.'),
        ('wolves.svg', 'Wolverhampton Wanderers', ['Hull City', 'Borussia Dortmund', 'AS Roma'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><polygon points="100,25 175,68 175,172 100,215 25,172 25,68" fill="#FDB913" stroke="#231F20" stroke-width="10"/><polygon points="60,70 82,105 118,105 140,70 130,155 100,180 70,155" fill="#231F20"/><polygon points="75,118 92,126 78,134" fill="#FDB913"/><polygon points="125,118 108,126 122,134" fill="#FDB913"/>',
         'Wolverhampton Wanderers\' badge features a stylized black wolf\'s head inside an old-gold hexagon.'),
        ('newcastle.svg', 'Newcastle United', ['Juventus', 'Notts County', 'PAOK'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><path d="M40 40 H160 V145 Q100 212 40 145 Z" fill="#FFFFFF" stroke="#D4AF37" stroke-width="7"/><rect x="48" y="44" width="22" height="125" fill="#000000"/><rect x="90" y="44" width="22" height="145" fill="#000000"/><rect x="130" y="44" width="22" height="125" fill="#000000"/>',
         'Newcastle United\'s shield features the famous black-and-white vertical Magpie stripes bordered in gold.'),
        ('boca.svg', 'Boca Juniors', ['Villarreal CF', 'Fenerbahce', 'Parma'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><path d="M35 35 H165 V145 Q100 215 35 145 Z" fill="#003399" stroke="#FFCC00" stroke-width="7"/><rect x="38" y="95" width="124" height="42" fill="#FFCC00"/><circle cx="70" cy="65" r="8" fill="#FFCC00"/><circle cx="100" cy="65" r="8" fill="#FFCC00"/><circle cx="130" cy="65" r="8" fill="#FFCC00"/>',
         'Boca Juniors\' famous Argentine shield is royal blue with a wide golden horizontal band and golden championship stars.'),
        ('river_plate.svg', 'River Plate', ['Rayo Vallecano', 'Peru', 'AS Monaco'],
         '<rect width="200" height="240" rx="24" fill="#0f172a"/><path d="M35 35 H165 V145 Q100 215 35 145 Z" fill="#FFFFFF" stroke="#000000" stroke-width="7"/><polygon points="145,38 162,38 65,175 45,160" fill="#E4002B"/>',
         'River Plate\'s iconic white shield features a bold crimson diagonal sash running from top-right to bottom-left.')
    ]

    badge_questions = []
    badge_prompts = [
        "VISUAL BADGE MATCH: Which famous football club is represented by this crest design? (#{i})",
        "MATCH THE CLUB CREST: Look at the shield colors and symbol—which club's badge is this? (#{i})",
        "FOOTBALL EMBLEM CHALLENGE: Identify the football team from its visual crest clue below (#{i}):",
        "CLUB SHIELD SPOTTER: Which football club wears this crest on their kit? (#{i})",
        "STADIUM CREST QUIZ: Match this visual club badge to the correct football team (#{i}):",
        "VISUAL FOOTBALL MATCH: Which club is famous for this crest and color combination? (#{i})"
    ]
    for idx, (fname, club, distractors, svg_body, expl) in enumerate(badges_defs):
        url = write_svg('badges', fname, svg_body, viewbox="0 0 200 240")
        for v_idx in range(6):
            opts_list = [club] + distractors
            shift = (idx + v_idx) % 4
            rotated = opts_list[shift:] + opts_list[:shift]
            letters = ['A', 'B', 'C', 'D']
            options = {letters[i]: rotated[i] for i in range(4)}
            correct_letter = next(k for k, val in options.items() if val == club)
            badge_questions.append({
                'prompt': badge_prompts[v_idx].format(i=idx + 1),
                'type': 'image',
                'media_url': url,
                'options': options,
                'correct': correct_letter,
                'explanation': expl,
                'difficulty': 'easy' if v_idx < 4 else 'medium'
            })

    # =========================================================================
    # 3. BRAND LOGOS (36 clean visual brand emblems without text spoilers)
    # =========================================================================
    logos_defs = [
        ('audi.svg', 'Audi', ['Olympics', 'Subaru', 'Volkswagen'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><g fill="none" stroke="#E2E8F0" stroke-width="8"><circle cx="75" cy="90" r="32"/><circle cx="125" cy="90" r="32"/><circle cx="175" cy="90" r="32"/><circle cx="225" cy="90" r="32"/></g>',
         'Audi\'s four interlocking silver rings represent the 1932 merger of four German automakers forming Auto Union.'),
        ('olympics.svg', 'The Olympic Games', ['Audi', 'Mastercard', 'UEFA'],
         '<rect width="300" height="180" rx="16" fill="#FFFFFF"/><g fill="none" stroke-width="8"><circle cx="85" cy="72" r="28" stroke="#0081C8"/><circle cx="150" cy="72" r="28" stroke="#000000"/><circle cx="215" cy="72" r="28" stroke="#EE334E"/><circle cx="117" cy="105" r="28" stroke="#FCB131"/><circle cx="183" cy="105" r="28" stroke="#00A651"/></g>',
         'The five interlocking Olympic rings in blue, yellow, black, green, and red represent the five inhabited continents.'),
        ('mastercard.svg', 'Mastercard', ['Visa', 'PayPal', 'American Express'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><circle cx="122" cy="90" r="48" fill="#EB001B"/><circle cx="178" cy="90" r="48" fill="#F79E1B" fill-opacity="0.88"/>',
         'Mastercard\'s interlocking red and amber-yellow circles have been one of the world\'s most recognizable payment symbols since 1966.'),
        ('target.svg', 'Target', ['Vodafone', 'Pinterest', 'Beats by Dre'],
         '<rect width="300" height="180" rx="16" fill="#FFFFFF"/><circle cx="150" cy="90" r="62" fill="#CC0000"/><circle cx="150" cy="90" r="40" fill="#FFFFFF"/><circle cx="150" cy="90" r="20" fill="#CC0000"/>',
         'Target\'s red-and-white concentric bullseye logo was introduced in 1962.'),
        ('mercedes.svg', 'Mercedes-Benz', ['Mitsubishi', 'Tesla', 'Lexus'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><circle cx="150" cy="90" r="58" fill="none" stroke="#E2E8F0" stroke-width="7"/><polygon points="150,34 158,86 150,90 142,86" fill="#E2E8F0"/><polygon points="198,118 150,90 156,82" fill="#E2E8F0"/><polygon points="102,118 144,82 150,90" fill="#E2E8F0"/>',
         'Mercedes-Benz\'s three-pointed star symbolizes motorized dominance across land, sea, and air.'),
        ('mcdonalds.svg', 'McDonald\'s', ['Burger King', 'Wendy\'s', 'Subway'],
         '<rect width="300" height="180" rx="16" fill="#DA291C"/><path d="M85 145 V85 C85 45 145 45 150 95 C155 45 215 45 215 85 V145" fill="none" stroke="#FFC72C" stroke-width="18" stroke-linecap="round"/>',
         'McDonald\'s Golden Arches form a bright yellow M against a crimson red background.'),
        ('nike.svg', 'Nike', ['Adidas', 'Puma', 'Reebok'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><path d="M85 110 C65 130 95 145 135 128 L235 65 C155 95 105 112 85 110 Z" fill="#FFFFFF"/>',
         'The Nike Swoosh represents the wing of the Greek goddess of victory.'),
        ('adidas.svg', 'Adidas', ['Nike', 'Under Armour', 'New Balance'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><g fill="#FFFFFF"><polygon points="95,135 115,135 102,98 84,108"/><polygon points="128,135 148,135 128,74 110,84"/><polygon points="161,135 181,135 154,50 136,60"/></g>',
         'Adidas\' sloped three-stripe mountain logo symbolizes overcoming challenges and athletic goals.'),
        ('windows.svg', 'Microsoft Windows', ['Google Chrome', 'Slack', 'eBay'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><rect x="92" y="34" width="52" height="52" fill="#F25022"/><rect x="152" y="34" width="52" height="52" fill="#7FBA00"/><rect x="92" y="94" width="52" height="52" fill="#00A4EF"/><rect x="152" y="94" width="52" height="52" fill="#FFB900"/>',
         'Microsoft\'s four-square window emblem combines red, green, blue, and yellow panes.'),
        ('youtube.svg', 'YouTube', ['Netflix', 'Twitch', 'TikTok'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><rect x="75" y="42" width="150" height="96" rx="24" fill="#FF0000"/><polygon points="135,66 135,114 176,90" fill="#FFFFFF"/>',
         'YouTube\'s iconic logo features a white play triangle inside a rounded bright-red television rectangle.'),
        ('spotify.svg', 'Spotify', ['WhatsApp', 'SoundCloud', 'Shazam'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><circle cx="150" cy="90" r="58" fill="#1DB954"/><path d="M115 74 Q152 62 188 78" stroke="#0f172a" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M120 94 Q150 84 180 98" stroke="#0f172a" stroke-width="8" fill="none" stroke-linecap="round"/><path d="M126 113 Q150 105 172 116" stroke="#0f172a" stroke-width="7" fill="none" stroke-linecap="round"/>',
         'Spotify\'s vibrant green circle features three curved black sound-wave arcs.'),
        ('pepsi.svg', 'Pepsi', ['Korean Air', 'Domino\'s', 'Chevron'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><circle cx="150" cy="90" r="58" fill="#FFFFFF"/><path d="M95 82 A58 58 0 0 1 205 70 Q150 95 95 82 Z" fill="#E32934"/><path d="M95 102 Q150 85 205 108 A58 58 0 0 1 95 102 Z" fill="#004B93"/>',
         'The Pepsi Globe features red, white, and blue swirling wave hemispheres inside a circle.'),
        ('dominos.svg', 'Domino\'s Pizza', ['Pepsi', 'Tommy Hilfiger', 'Bank of America'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><g transform="rotate(-45 150 90)"><rect x="122" y="38" width="56" height="50" rx="8" fill="#E31837"/><rect x="122" y="92" width="56" height="50" rx="8" fill="#006491"/><circle cx="150" cy="63" r="7" fill="#FFFFFF"/><circle cx="138" cy="108" r="6" fill="#FFFFFF"/><circle cx="162" cy="126" r="6" fill="#FFFFFF"/></g>',
         'Domino\'s tilted red-and-blue domino tile features three white dots representing the chain\'s original three pizzerias.'),
        ('bmw.svg', 'BMW', ['Volkswagen', 'Alfa Romeo', 'Mini'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><circle cx="150" cy="90" r="60" fill="#000000" stroke="#E2E8F0" stroke-width="5"/><path d="M150 50 A40 40 0 0 1 190 90 L150 90 Z" fill="#FFFFFF"/><path d="M150 130 A40 40 0 0 1 110 90 L150 90 Z" fill="#FFFFFF"/><path d="M110 90 A40 40 0 0 1 150 50 L150 90 Z" fill="#0066B1"/><path d="M190 90 A40 40 0 0 1 150 130 L150 90 Z" fill="#0066B1"/>',
         'BMW\'s roundel displays alternating blue and white quadrants inspired by the colors of Bavaria.'),
        ('mitsubishi.svg', 'Mitsubishi', ['Mercedes-Benz', 'Renault', 'Chrysler'],
         '<rect width="300" height="180" rx="16" fill="#FFFFFF"/><g fill="#E60012"><polygon points="150,28 170,62 150,96 130,62"/><polygon points="150,96 190,96 210,130 170,130"/><polygon points="150,96 110,96 90,130 130,130"/></g>',
         'Mitsubishi\'s logo consists of three red diamonds ("Mitsu" = three, "Hishi" = water chestnut/diamond) meeting at a central point.'),
        ('renault.svg', 'Renault', ['Mitsubishi', 'Citroen', 'Peugeot'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><polygon points="150,24 198,90 150,156 102,90" fill="none" stroke="#FCD116" stroke-width="16"/><polygon points="150,52 176,90 150,128 124,90" fill="none" stroke="#FFFFFF" stroke-width="6"/>',
         'Renault\'s geometric vertical diamond emblem has represented the French automaker since 1925.'),
        ('shell.svg', 'Shell', ['BP', 'Texaco', 'TotalEnergies'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><path d="M90 115 C80 55 115 32 150 32 C185 32 220 55 210 115 L175 142 H125 Z" fill="#FBCE07" stroke="#DD1D21" stroke-width="10"/><line x1="150" y1="38" x2="150" y2="136" stroke="#DD1D21" stroke-width="5"/><line x1="122" y1="45" x2="135" y2="136" stroke="#DD1D21" stroke-width="5"/><line x1="178" y1="45" x2="165" y2="136" stroke="#DD1D21" stroke-width="5"/>',
         'Shell\'s red-and-yellow Pecten scallop shell logo honors founder Marcus Samuel\'s original seashell import business.'),
        ('netflix.svg', 'Netflix', ['Hulu', 'Adobe', 'Pinterest'],
         '<rect width="300" height="180" rx="16" fill="#000000"/><rect x="112" y="34" width="22" height="112" fill="#B1060F"/><rect x="166" y="34" width="22" height="112" fill="#B1060F"/><polygon points="112,34 134,34 188,146 166,146" fill="#E50914"/>',
         'Netflix\'s crimson ribbon N icon stands against a cinema-black background.'),
        ('slack.svg', 'Slack', ['Google Photos', 'Microsoft Teams', 'Trello'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><rect x="105" y="65" width="38" height="16" rx="8" fill="#36C5F0"/><rect x="152" y="45" width="16" height="38" rx="8" fill="#2EB67D"/><rect x="155" y="98" width="38" height="16" rx="8" fill="#ECB22E"/><rect x="130" y="96" width="16" height="38" rx="8" fill="#E01E5A"/>',
         'Slack\'s pinwheel octothorpe logo combines cyan, green, yellow, and magenta speech droplets.'),
        ('rolex.svg', 'Rolex', ['Omega', 'Cartier', 'Maserati'],
         '<rect width="300" height="180" rx="16" fill="#006039"/><polygon points="110,130 95,72 122,98 136,56 150,95 164,56 178,98 205,72 190,130" fill="#A37E2C"/><circle cx="95" cy="66" r="6" fill="#F4D068"/><circle cx="136" cy="50" r="6" fill="#F4D068"/><circle cx="150" cy="46" r="6" fill="#F4D068"/><circle cx="164" cy="50" r="6" fill="#F4D068"/><circle cx="205" cy="66" r="6" fill="#F4D068"/>',
         'Rolex\'s five-pointed golden coronet crown on an emerald green background was trademarked in 1925.')
    ]

    logo_questions = []
    logo_prompts = [
        "VISUAL LOGO MATCH: Which world-famous brand is represented by this emblem? (#{i})",
        "MATCH THE BRAND LOGO: Identify the company or organization from its visual symbol below (#{i}):",
        "BRAND ICON CHALLENGE: Look at the shapes and colors—which brand uses this logo? (#{i})",
        "SPEED LOGO SPOTTER: Which global company owns the famous emblem shown below? (#{i})",
        "CORPORATE SYMBOL QUIZ: Match this visual logo clue to the correct brand (#{i}):",
        "VISUAL BRAND TRIVIA: Which iconic brand is recognized worldwide by this symbol? (#{i})"
    ]
    for idx, (fname, brand, distractors, svg_body, expl) in enumerate(logos_defs):
        url = write_svg('logos', fname, svg_body)
        for v_idx in range(6):
            opts_list = [brand] + distractors
            shift = (idx + v_idx) % 4
            rotated = opts_list[shift:] + opts_list[:shift]
            letters = ['A', 'B', 'C', 'D']
            options = {letters[i]: rotated[i] for i in range(4)}
            correct_letter = next(k for k, val in options.items() if val == brand)
            logo_questions.append({
                'prompt': logo_prompts[v_idx].format(i=idx + 1),
                'type': 'image',
                'media_url': url,
                'options': options,
                'correct': correct_letter,
                'explanation': expl,
                'difficulty': 'easy' if v_idx < 4 else 'medium'
            })

    # =========================================================================
    # 4. COUNTRY SHAPES / SILHOUETTES (36 visual country silhouette puzzles)
    # =========================================================================
    shapes_defs = [
        ('italy.svg', 'Italy', ['Greece', 'Florida (USA)', 'New Zealand'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><path d="M115 24 L152 30 L145 55 L188 115 L202 128 L192 142 L176 130 L170 150 L156 146 L162 122 L125 68 L112 52 Z" fill="#22D3EE" stroke="#A855F7" stroke-width="3"/><polygon points="135,148 158,145 150,164" fill="#22D3EE"/><rect x="102" y="95" width="14" height="24" rx="4" fill="#22D3EE"/>',
         'Italy\'s unmistakable boot-shaped peninsula extends into the Mediterranean Sea toward triangular Sicily and Sardinia.'),
        ('chile.svg', 'Chile', ['Norway', 'Vietnam', 'Argentina'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><path d="M148 12 L158 15 L154 65 L150 120 L158 162 L142 168 L138 120 L144 65 Z" fill="#34D399" stroke="#06B6D4" stroke-width="3"/>',
         'Chile is the longest north-to-south ribbon-shaped country in the world, stretching 4,300 km along the Andes and Pacific.'),
        ('france.svg', 'France', ['Spain', 'Poland', 'Germany'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><polygon points="150,24 202,52 196,118 152,152 102,126 98,62" fill="#A855F7" stroke="#22D3EE" stroke-width="4"/><ellipse cx="212" cy="142" rx="6" ry="12" fill="#A855F7"/>',
         'Mainland France is famously nicknamed "L\'Hexagone" due to its distinct six-sided geometric outline (plus Corsica).'),
        ('australia.svg', 'Australia', ['Brazil', 'United States', 'Greenland'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><path d="M85 65 L125 42 L162 52 L175 35 L208 68 L215 108 L188 135 L148 122 L115 128 L82 105 Z" fill="#F59E0B" stroke="#FDE047" stroke-width="3"/><polygon points="175,142 188,142 182,156" fill="#F59E0B"/>',
         'Australia\'s island-continent silhouette features the Gulf of Carpentaria at the top and heart-shaped Tasmania below.'),
        ('japan.svg', 'Japan', ['New Zealand', 'Philippines', 'United Kingdom'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><g fill="#F43F5E" stroke="#FDA4AF" stroke-width="2"><polygon points="185,22 212,35 192,52 175,40"/><path d="M178 55 C185 85 162 118 125 132 L118 120 C148 106 168 80 166 52 Z"/><ellipse cx="132" cy="138" rx="10" ry="6"/><polygon points="105,134 118,142 108,158 96,148"/></g>',
         'Japan\'s curving volcanic archipelago consists of four main islands: Hokkaido, Honshu, Shikoku, and Kyushu.'),
        ('uk.svg', 'United Kingdom', ['Japan', 'New Zealand', 'Madagascar'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><path d="M142 22 L168 30 L158 65 L182 108 L192 142 L132 154 L125 125 L142 95 L132 62 Z" fill="#38BDF8" stroke="#E0F2FE" stroke-width="3"/><polygon points="105,78 124,82 120,102 102,96" fill="#38BDF8"/>',
         'The United Kingdom comprises the island of Great Britain (England, Scotland, Wales) and Northern Ireland.'),
        ('india.svg', 'India', ['South Africa', 'Brazil', 'Mexico'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><polygon points="145,22 172,48 215,65 185,92 152,162 118,95 96,72 128,48" fill="#FB923C" stroke="#FED7AA" stroke-width="3"/>',
         'India\'s diamond-and-peninsula silhouette tapers south into a sharp V-shaped tip at Cape Comorin in the Indian Ocean.'),
        ('brazil.svg', 'Brazil', ['Argentina', 'Africa', 'Greenland'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><polygon points="105,38 175,35 215,68 188,125 152,158 135,132 115,98 88,68" fill="#4ADE80" stroke="#BBF7D0" stroke-width="3"/>',
         'Brazil\'s massive triangular heart-like map dominates eastern South America from the Amazon basin to the Atlantic coast.'),
        ('usa.svg', 'United States', ['Canada', 'China', 'Australia'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><path d="M72 48 L215 48 L228 62 L205 122 L212 145 L198 145 L188 125 L145 128 L132 148 L115 125 L75 112 Z" fill="#60A5FA" stroke="#DBEAFE" stroke-width="3"/>',
         'The contiguous United States spans from the Pacific West Coast across Texas to the Florida peninsula in the southeast.'),
        ('mexico.svg', 'Mexico', ['Chile', 'Cuba', 'Croatia'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><path d="M82 32 L155 45 L168 95 L205 128 L222 108 L232 118 L208 146 L152 128 L112 75 L88 45 L95 85 L85 88 Z" fill="#34D399" stroke="#A7F3D0" stroke-width="3"/>',
         'Mexico\'s horn-of-plenty (cornucopia) silhouette features the Baja California peninsula on the left and Yucatan on the right.'),
        ('spain.svg', 'Spain', ['France', 'Turkey', 'Poland'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><polygon points="95,42 208,45 215,72 182,138 112,142 115,68 95,65" fill="#FBBF24" stroke="#FEF08A" stroke-width="3"/>',
         'Spain occupies 85% of the Iberian Peninsula, nicknamed "the bull\'s hide" for its wide rectangular silhouette.'),
        ('vietnam.svg', 'Vietnam', ['Chile', 'Japan', 'Norway'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><path d="M135 22 L175 28 L162 58 C142 78 175 108 182 132 L148 162 L138 146 C158 122 125 85 135 52 Z" fill="#F87171" stroke="#FECACA" stroke-width="3"/>',
         'Vietnam\'s coastal outline forms a distinctive elongated letter "S" along the eastern edge of Indochina.'),
        ('new_zealand.svg', 'New Zealand', ['Japan', 'Italy', 'Philippines'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><polygon points="168,28 195,55 178,88 158,72" fill="#2DD4BF" stroke="#CCFBF1" stroke-width="3"/><polygon points="148,95 168,108 132,156 112,142" fill="#2DD4BF" stroke="#CCFBF1" stroke-width="3"/>',
         'New Zealand consists of two main islands—the North Island and the elongated South Island—separated by Cook Strait.'),
        ('madagascar.svg', 'Madagascar', ['Sri Lanka', 'Cuba', 'Taiwan'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><polygon points="165,24 178,48 162,148 135,156 128,112 145,52" fill="#FB7185" stroke="#FECDD3" stroke-width="3"/>',
         'Madagascar is the world\'s fourth-largest island, shaped like an angled footprint off the southeast coast of Africa.'),
        ('sri_lanka.svg', 'Sri Lanka', ['Madagascar', 'Cyprus', 'Iceland'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><path d="M148 28 C162 55 188 92 182 132 C175 156 125 156 118 132 C112 92 136 55 148 28 Z" fill="#FACC15" stroke="#FEF08A" stroke-width="3"/>',
         'Sri Lanka is famously known as the "Teardrop of India" due to its classic pear/teardrop island silhouette.'),
        ('cyprus.svg', 'Cyprus', ['Crete', 'Sicily', 'Jamaica'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><polygon points="82,92 115,72 168,78 228,45 232,55 182,92 165,125 102,128" fill="#FB923C" stroke="#FFEDD5" stroke-width="3"/>',
         'Cyprus is instantly recognizable by its long, narrow panhandle (the Karpass Peninsula) pointing northeast in the Mediterranean.'),
        ('croatia.svg', 'Croatia', ['Greece', 'Chile', 'Morocco'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><polygon points="105,42 195,38 205,62 142,68 135,95 188,148 172,158 108,95 95,62" fill="#60A5FA" stroke="#DBEAFE" stroke-width="3"/>',
         'Croatia has a unique boomerang or crescent horseshoe shape wrapping around Bosnia and Herzegovina along the Adriatic coast.'),
        ('iceland.svg', 'Iceland', ['Ireland', 'Tasmania', 'Sri Lanka'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><polygon points="85,42 125,35 120,62 198,52 218,88 195,128 115,135 88,108 105,78 78,62" fill="#38BDF8" stroke="#E0F2FE" stroke-width="3"/>',
         'Iceland\'s volcanic island outline features the dramatic claw-like Westfjords peninsula in the northwest.'),
        ('cuba.svg', 'Cuba', ['Jamaica', 'Chile', 'Taiwan'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><path d="M52 102 C95 72 168 78 248 112 L238 128 C168 98 98 92 62 116 Z" fill="#4ADE80" stroke="#DCFCE7" stroke-width="3"/>',
         'Cuba is the largest island in the Caribbean, nicknamed "El Cocodrilo" because its long curved silhouette resembles a crocodile.'),
        ('egypt.svg', 'Egypt', ['Saudi Arabia', 'Sudan', 'Libya'],
         '<rect width="300" height="180" rx="16" fill="#0f172a"/><polygon points="92,38 182,38 212,55 198,92 182,65 198,148 92,148" fill="#FBBF24" stroke="#FEF08A" stroke-width="3"/>',
         'Egypt has a boxy desert outline bordered by the Mediterranean and Red Sea, plus the triangular Sinai Peninsula in the northeast.')
    ]

    shape_questions = []
    shape_prompts = [
        "VISUAL MAP MATCH: Which country's geographic silhouette is shown below? (#{i})",
        "MATCH THE COUNTRY SHAPE: Identify the nation from its map outline clue (#{i}):",
        "GEOGRAPHY SILHOUETTE CHALLENGE: Look at the coastline and shape—which country is this? (#{i})",
        "WORLD MAP OUTLINE: Which sovereign country has the border silhouette displayed below? (#{i})",
        "ATLAS SHAPE SPOTTER: Match this geographic country outline to the correct nation (#{i}):",
        "VISUAL GEOGRAPHY MATCH: Which country is represented by this map silhouette? (#{i})"
    ]
    for idx, (fname, country, distractors, svg_body, expl) in enumerate(shapes_defs):
        url = write_svg('shapes', fname, svg_body)
        for v_idx in range(6):
            opts_list = [country] + distractors
            shift = (idx + v_idx) % 4
            rotated = opts_list[shift:] + opts_list[:shift]
            letters = ['A', 'B', 'C', 'D']
            options = {letters[i]: rotated[i] for i in range(4)}
            correct_letter = next(k for k, val in options.items() if val == country)
            shape_questions.append({
                'prompt': shape_prompts[v_idx].format(i=idx + 1),
                'type': 'image',
                'media_url': url,
                'options': options,
                'correct': correct_letter,
                'explanation': expl,
                'difficulty': 'easy' if v_idx < 4 else 'medium'
            })

    return {
        'match-flags': flag_questions,
        'football-badges': badge_questions,
        'brand-logos': logo_questions,
        'country-shapes': shape_questions
    }


def update_mega_json_and_db():
    visual_map = build_all_visual_assets()

    with open(MEGA_JSON_PATH, 'r', encoding='utf-8') as f:
        mega_data = json.load(f)

    for cat_slug, new_visual_qs in visual_map.items():
        cat_info = mega_data['categories'].get(cat_slug)
        if not cat_info:
            continue

        existing_qs = cat_info.get('questions', [])
        kept_visual = []
        expert_text = []
        seen_prompts = set(q['prompt'] for q in new_visual_qs)

        for q in existing_qs:
            if q['prompt'] in seen_prompts:
                continue
            if q.get('type') == 'image' and q.get('media_url'):
                q['difficulty'] = 'easy'
                kept_visual.append(q)
            else:
                # Classify obscure text-only questions in visual categories as Expert ('hard')!
                q['difficulty'] = 'hard'
                if not q['prompt'].startswith('EXPERT TRIVIA:'):
                    q['prompt'] = 'EXPERT TRIVIA: ' + q['prompt']
                expert_text.append(q)

        # Put all visual matching questions FIRST, and keep 80 expert text questions so visual is the clear majority!
        combined = new_visual_qs + kept_visual + expert_text[:80]
        cat_info['questions'] = combined
        cat_info['question_count'] = len(combined)
        print(f"{cat_slug}: {len(new_visual_qs) + len(kept_visual)} VISUAL questions vs {len(expert_text[:80])} EXPERT text questions (Total: {len(combined)})")

    with open(MEGA_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(mega_data, f, indent=2, ensure_ascii=False)

    # Also update the live SQLite database directly
    from app import create_app
    from app.models import db, QuizQuestion, QuizPack
    app = create_app()
    with app.app_context():
        for cat_slug in visual_map.keys():
            cat_info = mega_data['categories'][cat_slug]
            QuizQuestion.query.filter_by(category_slug=cat_slug, is_community=False).delete(synchronize_session=False)
            db.session.commit()
            objs = []
            for q_item in cat_info['questions']:
                objs.append(QuizQuestion(
                    category_slug=cat_slug,
                    category_name=cat_info['title'],
                    pack_slug=cat_slug,
                    prompt=q_item['prompt'],
                    question_type=q_item.get('type', 'classic'),
                    media_url=q_item.get('media_url', ''),
                    options_json=json.dumps(q_item['options']),
                    correct_option=q_item['correct'],
                    explanation=q_item['explanation'],
                    difficulty=q_item.get('difficulty', 'medium'),
                    points=100,
                    time_limit=15,
                    status='approved',
                    is_community=False
                ))
            db.session.bulk_save_objects(objs)
            pack = QuizPack.query.filter_by(category_slug=cat_slug).first()
            if pack:
                pack.question_count = len(objs)
            db.session.commit()
            vis_count = QuizQuestion.query.filter_by(category_slug=cat_slug, question_type='image').count()
            exp_count = QuizQuestion.query.filter_by(category_slug=cat_slug, difficulty='hard').count()
            print(f"DB Synced {cat_slug}: {vis_count} visual image questions, {exp_count} expert hard questions")


if __name__ == '__main__':
    update_mega_json_and_db()
