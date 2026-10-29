# -*- coding: utf-8 -*-
"""Reference and fact articles, maintained in code and seeded on boot.

Two kinds live here. Reference pieces are deliberately list-heavy and dense,
written so that someone stuck on a crossword clue can search the site, land on
one and find the word. Fact pieces are shorter reads that answer a question
people actually ask, and double as quiz material.

Matched on slug, like the guides above them in quiz_seed, so a redeploy updates
the wording rather than creating a second copy, and never overrides a cover
image that has been hand-picked in admin.
"""

# Categories are created on demand by the seeder, in this order.
ARTICLE_CATEGORIES = [
    ('Quiz Reference', 'quiz-reference'),
    ('Facts & Curiosities', 'facts-and-curiosities'),
    ('Quiz Craft', 'quiz-craft'),
]


def _a(slug, title, category, excerpt, image, content, meta=''):
    return {
        'slug': slug,
        'title': title,
        'category': category,
        'excerpt': excerpt,
        'featured_image': image,
        'content': content.strip(),
        'meta_description': meta or excerpt,
    }


REF = 'Quiz Reference'
FACT = 'Facts & Curiosities'
CRAFT = 'Quiz Craft'


ARTICLES = [

    # ==================================================================
    _a('capital-cities-of-europe', 'Every Capital City in Europe, Including the Ones People Get Wrong',
       REF,
       'All 44 European capitals in one table, plus the eight that catch people out in quizzes and crosswords — and why Switzerland’s answer is more awkward than it looks.',
       '/static/img/articles/europe-capitals.svg',
       """
<p>Capital cities are quiz bread and butter, and crossword setters love them because the names are short, distinctive and unambiguous. Here is the full European set, followed by the handful that reliably cost teams a point.</p>

<h3>The full list</h3>
<table>
<tr><th>Country</th><th>Capital</th></tr>
<tr><td>Albania</td><td>Tirana</td></tr>
<tr><td>Andorra</td><td>Andorra la Vella</td></tr>
<tr><td>Austria</td><td>Vienna</td></tr>
<tr><td>Belarus</td><td>Minsk</td></tr>
<tr><td>Belgium</td><td>Brussels</td></tr>
<tr><td>Bosnia and Herzegovina</td><td>Sarajevo</td></tr>
<tr><td>Bulgaria</td><td>Sofia</td></tr>
<tr><td>Croatia</td><td>Zagreb</td></tr>
<tr><td>Cyprus</td><td>Nicosia</td></tr>
<tr><td>Czechia</td><td>Prague</td></tr>
<tr><td>Denmark</td><td>Copenhagen</td></tr>
<tr><td>Estonia</td><td>Tallinn</td></tr>
<tr><td>Finland</td><td>Helsinki</td></tr>
<tr><td>France</td><td>Paris</td></tr>
<tr><td>Germany</td><td>Berlin</td></tr>
<tr><td>Greece</td><td>Athens</td></tr>
<tr><td>Hungary</td><td>Budapest</td></tr>
<tr><td>Iceland</td><td>Reykjavik</td></tr>
<tr><td>Ireland</td><td>Dublin</td></tr>
<tr><td>Italy</td><td>Rome</td></tr>
<tr><td>Kosovo</td><td>Pristina</td></tr>
<tr><td>Latvia</td><td>Riga</td></tr>
<tr><td>Liechtenstein</td><td>Vaduz</td></tr>
<tr><td>Lithuania</td><td>Vilnius</td></tr>
<tr><td>Luxembourg</td><td>Luxembourg City</td></tr>
<tr><td>Malta</td><td>Valletta</td></tr>
<tr><td>Moldova</td><td>Chisinau</td></tr>
<tr><td>Monaco</td><td>Monaco</td></tr>
<tr><td>Montenegro</td><td>Podgorica</td></tr>
<tr><td>Netherlands</td><td>Amsterdam</td></tr>
<tr><td>North Macedonia</td><td>Skopje</td></tr>
<tr><td>Norway</td><td>Oslo</td></tr>
<tr><td>Poland</td><td>Warsaw</td></tr>
<tr><td>Portugal</td><td>Lisbon</td></tr>
<tr><td>Romania</td><td>Bucharest</td></tr>
<tr><td>Russia</td><td>Moscow</td></tr>
<tr><td>San Marino</td><td>San Marino</td></tr>
<tr><td>Serbia</td><td>Belgrade</td></tr>
<tr><td>Slovakia</td><td>Bratislava</td></tr>
<tr><td>Slovenia</td><td>Ljubljana</td></tr>
<tr><td>Spain</td><td>Madrid</td></tr>
<tr><td>Sweden</td><td>Stockholm</td></tr>
<tr><td>Switzerland</td><td>Bern</td></tr>
<tr><td>Ukraine</td><td>Kyiv</td></tr>
<tr><td>United Kingdom</td><td>London</td></tr>
<tr><td>Vatican City</td><td>Vatican City</td></tr>
</table>

<h3>The eight that catch people out</h3>
<ul>
<li><strong>Switzerland — Bern.</strong> Not Zurich, which is bigger, and not Geneva, which holds the international institutions. Switzerland has never formally declared a capital at all; Bern is the "federal city" and functions as one.</li>
<li><strong>Netherlands — Amsterdam.</strong> But the government, parliament and royal offices all sit in The Hague. Amsterdam is the constitutional capital, The Hague is the working one.</li>
<li><strong>Turkey — Ankara.</strong> Istanbul is far larger and far better known, and has not been the capital since 1923.</li>
<li><strong>Portugal — Lisbon.</strong> Easy, until a setter offers Porto, which is where the wine and the second city are.</li>
<li><strong>Malta — Valletta.</strong> Two Ls and two Ts, and almost always misspelled.</li>
<li><strong>Liechtenstein — Vaduz.</strong> Five letters and a Z, which is exactly why it turns up in crosswords far more often than its size deserves.</li>
<li><strong>Kosovo — Pristina.</strong> Contested as a country, so some quiz sources list it and some do not.</li>
<li><strong>Ukraine — Kyiv.</strong> Spelled Kiev in older sources. Modern usage follows the Ukrainian transliteration.</li>
</ul>

<h3>Useful for crosswords</h3>
<p>Short capitals are setters’ favourites because they fit anywhere: <strong>Rome</strong> (4), <strong>Oslo</strong> (4), <strong>Riga</strong> (4), <strong>Bern</strong> (4), <strong>Kyiv</strong> (4), <strong>Paris</strong> (5), <strong>Minsk</strong> (5), <strong>Sofia</strong> (5), <strong>Vaduz</strong> (5), <strong>Skopje</strong> (6) and <strong>Vienna</strong> (6). If a clue points vaguely at Europe and you need four letters, start with Oslo and Rome.</p>
"""),

    # ==================================================================
    _a('greek-gods-and-their-roman-names', 'The Greek Gods and Their Roman Names',
       REF,
       'Zeus or Jupiter, Ares or Mars — the full pairing table, what each god was actually responsible for, and the four where the two traditions do not line up neatly.',
       '/static/img/articles/greek-roman-gods.svg',
       """
<p>Ask a quiz question about classical mythology and you are really asking which naming tradition the setter has in mind. The Romans adopted the Greek gods wholesale and renamed them, so almost every figure has two names. Crossword setters exploit this constantly: the clue says "god of war" and the answer could be <strong>Ares</strong> (4) or <strong>Mars</strong> (4).</p>

<h3>The main pairings</h3>
<table>
<tr><th>Greek</th><th>Roman</th><th>Responsible for</th></tr>
<tr><td>Zeus</td><td>Jupiter</td><td>King of the gods, sky and thunder</td></tr>
<tr><td>Hera</td><td>Juno</td><td>Marriage, queen of the gods</td></tr>
<tr><td>Poseidon</td><td>Neptune</td><td>The sea, earthquakes, horses</td></tr>
<tr><td>Hades</td><td>Pluto</td><td>The underworld and the dead</td></tr>
<tr><td>Athena</td><td>Minerva</td><td>Wisdom, strategy, crafts</td></tr>
<tr><td>Apollo</td><td>Apollo</td><td>Light, music, prophecy, healing</td></tr>
<tr><td>Artemis</td><td>Diana</td><td>The hunt, the moon, wild places</td></tr>
<tr><td>Ares</td><td>Mars</td><td>War</td></tr>
<tr><td>Aphrodite</td><td>Venus</td><td>Love and beauty</td></tr>
<tr><td>Hephaestus</td><td>Vulcan</td><td>Fire, forges, metalwork</td></tr>
<tr><td>Hermes</td><td>Mercury</td><td>Messages, travel, trade, thieves</td></tr>
<tr><td>Demeter</td><td>Ceres</td><td>Harvest and agriculture</td></tr>
<tr><td>Dionysus</td><td>Bacchus</td><td>Wine, theatre, revelry</td></tr>
<tr><td>Hestia</td><td>Vesta</td><td>The hearth and home</td></tr>
<tr><td>Persephone</td><td>Proserpina</td><td>Spring, and queen of the underworld</td></tr>
<tr><td>Eros</td><td>Cupid</td><td>Desire</td></tr>
<tr><td>Cronus</td><td>Saturn</td><td>Time, and the previous ruling generation</td></tr>
<tr><td>Gaia</td><td>Terra</td><td>The Earth itself</td></tr>
<tr><td>Helios</td><td>Sol</td><td>The sun</td></tr>
<tr><td>Selene</td><td>Luna</td><td>The moon</td></tr>
<tr><td>Nike</td><td>Victoria</td><td>Victory</td></tr>
<tr><td>Pan</td><td>Faunus</td><td>The wild, shepherds, panic</td></tr>
</table>

<h3>Where the two traditions do not match</h3>
<ul>
<li><strong>Apollo kept his name.</strong> The Romans imported him directly without renaming, which is why he is the one answer that works either way.</li>
<li><strong>Ares and Mars are not the same character.</strong> Ares was disliked by the Greeks — brutal, reckless, barely heroic. Mars was respected in Rome, a father of the nation and second only to Jupiter.</li>
<li><strong>Hades is not quite Pluto.</strong> Hades is the underworld’s grim ruler; Pluto carries a sense of wealth, from the riches buried in the earth.</li>
<li><strong>Artemis and Diana drifted apart.</strong> Diana absorbed Italian woodland deities and became more closely tied to the moon than Artemis originally was.</li>
</ul>

<h3>Quick crossword lengths</h3>
<p><strong>3:</strong> Pan, Sol. <strong>4:</strong> Zeus, Hera, Juno, Ares, Mars, Eros, Nike, Gaia, Luna. <strong>5:</strong> Hades, Pluto, Venus, Diana, Ceres, Vesta. <strong>6:</strong> Athena, Apollo, Hermes, Vulcan. <strong>7:</strong> Jupiter, Minerva, Mercury, Bacchus, Neptune.</p>
"""),

    # ==================================================================
    _a('chemical-symbols-that-dont-match', 'Chemical Symbols That Look Nothing Like Their Element',
       REF,
       'Why gold is Au, lead is Pb and tungsten is W. Eleven elements whose symbols come from older names, plus the full table of the ones worth memorising.',
       '/static/img/articles/chemical-symbols.svg',
       """
<p>Most chemical symbols are obvious once you see them. Oxygen is O, carbon is C, calcium is Ca. Then there is a group of eleven whose symbols appear to have nothing to do with their English names at all — and those are precisely the ones that turn up in quizzes.</p>

<p>The reason is simple: the symbols were set using Latin, and in one case German, rather than English.</p>

<h3>The eleven oddities</h3>
<table>
<tr><th>Element</th><th>Symbol</th><th>Comes from</th></tr>
<tr><td>Gold</td><td>Au</td><td><em>Aurum</em>, Latin for gold</td></tr>
<tr><td>Silver</td><td>Ag</td><td><em>Argentum</em></td></tr>
<tr><td>Iron</td><td>Fe</td><td><em>Ferrum</em></td></tr>
<tr><td>Copper</td><td>Cu</td><td><em>Cuprum</em>, from Cyprus</td></tr>
<tr><td>Lead</td><td>Pb</td><td><em>Plumbum</em> — the root of "plumber"</td></tr>
<tr><td>Tin</td><td>Sn</td><td><em>Stannum</em></td></tr>
<tr><td>Mercury</td><td>Hg</td><td><em>Hydrargyrum</em>, "water silver"</td></tr>
<tr><td>Sodium</td><td>Na</td><td><em>Natrium</em></td></tr>
<tr><td>Potassium</td><td>K</td><td><em>Kalium</em></td></tr>
<tr><td>Antimony</td><td>Sb</td><td><em>Stibium</em></td></tr>
<tr><td>Tungsten</td><td>W</td><td><em>Wolfram</em>, from German</td></tr>
</table>

<h3>The story behind three of them</h3>
<p><strong>Lead and plumbing.</strong> Roman water pipes were made of lead, so the people who fitted them were <em>plumbarii</em>. The pipes are long gone and the job name survived.</p>
<p><strong>Copper and Cyprus.</strong> The island was the Roman world’s main source of copper, and the metal was called <em>aes cyprium</em>, "metal of Cyprus", shortened to <em>cuprum</em>.</p>
<p><strong>Tungsten and wolfram.</strong> Tungsten is Swedish for "heavy stone". German miners called its ore <em>wolfram</em>, said to be because it ate through tin like a wolf. English took the Swedish name, the symbol took the German one, and the element has been answering to both ever since.</p>

<h3>Other symbols worth knowing</h3>
<p>H hydrogen, He helium, Li lithium, C carbon, N nitrogen, O oxygen, F fluorine, Ne neon, Mg magnesium, Al aluminium, Si silicon, P phosphorus, S sulfur, Cl chlorine, Ar argon, Ca calcium, Ti titanium, Cr chromium, Mn manganese, Co cobalt, Ni nickel, Zn zinc, Br bromine, Kr krypton, Ag silver, I iodine, Xe xenon, Pt platinum, U uranium.</p>

<h3>For crossword solvers</h3>
<p>Setters use chemical symbols as hidden letter fragments all the time. "Gold" in a cryptic clue very often means you should write <strong>AU</strong> or <strong>OR</strong> (the heraldic term). "Iron" means <strong>FE</strong>, "silver" means <strong>AG</strong>, "tin" means <strong>SN</strong>, and "lead" can mean <strong>PB</strong> or simply the first letter of the following word.</p>
"""),

    # ==================================================================
    _a('collective-nouns-for-animals', 'Collective Nouns for Animals, From a Murder to a Parliament',
       REF,
       'A murder of crows, a parliament of owls, a crash of rhinos. The full working list of animal collective nouns, where the strange ones came from, and which are actually used.',
       '/static/img/articles/collective-nouns.jpg',
       """
<p>Collective nouns are a quiz staple and a crossword gift, because the answers are short, vivid and unmistakable. Most of the famous ones come from a single source: <em>The Book of Saint Albans</em>, printed in 1486, which listed "terms of venery" used by hunters. A good number were jokes even then.</p>

<h3>Birds</h3>
<table>
<tr><th>Animal</th><th>Collective noun</th></tr>
<tr><td>Crows</td><td>A murder</td></tr>
<tr><td>Ravens</td><td>An unkindness</td></tr>
<tr><td>Owls</td><td>A parliament</td></tr>
<tr><td>Geese (on the ground)</td><td>A gaggle</td></tr>
<tr><td>Geese (in flight)</td><td>A skein</td></tr>
<tr><td>Larks</td><td>An exaltation</td></tr>
<tr><td>Goldfinches</td><td>A charm</td></tr>
<tr><td>Starlings</td><td>A murmuration</td></tr>
<tr><td>Peacocks</td><td>An ostentation</td></tr>
<tr><td>Magpies</td><td>A tiding</td></tr>
<tr><td>Nightingales</td><td>A watch</td></tr>
<tr><td>Flamingos</td><td>A flamboyance</td></tr>
<tr><td>Jays</td><td>A band</td></tr>
<tr><td>Herons</td><td>A siege</td></tr>
</table>

<h3>Mammals</h3>
<table>
<tr><th>Animal</th><th>Collective noun</th></tr>
<tr><td>Lions</td><td>A pride</td></tr>
<tr><td>Rhinos</td><td>A crash</td></tr>
<tr><td>Hippos</td><td>A bloat</td></tr>
<tr><td>Otters</td><td>A raft</td></tr>
<tr><td>Hyenas</td><td>A cackle</td></tr>
<tr><td>Zebras</td><td>A dazzle</td></tr>
<tr><td>Giraffes</td><td>A tower</td></tr>
<tr><td>Porcupines</td><td>A prickle</td></tr>
<tr><td>Kangaroos</td><td>A mob</td></tr>
<tr><td>Bats</td><td>A colony or cloud</td></tr>
<tr><td>Ferrets</td><td>A business</td></tr>
<tr><td>Moles</td><td>A labour</td></tr>
<tr><td>Apes</td><td>A shrewdness</td></tr>
<tr><td>Whales</td><td>A pod</td></tr>
</table>

<h3>Everything else</h3>
<p>A <strong>shiver</strong> of sharks. A <strong>smack</strong> of jellyfish. A <strong>bask</strong> of crocodiles. A <strong>knot</strong> of toads. A <strong>bed</strong> of oysters. A <strong>cloud</strong> of grasshoppers. A <strong>scourge</strong> of mosquitoes. A <strong>float</strong> of crocodiles in water. An <strong>army</strong> of frogs. A <strong>rhumba</strong> of rattlesnakes.</p>

<h3>Which of these are real?</h3>
<p>It depends what you mean by real. Terms like <em>pride</em>, <em>pod</em>, <em>flock</em>, <em>herd</em>, <em>swarm</em> and <em>gaggle</em> are in genuine everyday use. Terms like <em>shrewdness of apes</em> and <em>unkindness of ravens</em> have been copied from list to list for five centuries without ever being used by anyone describing actual animals.</p>
<p>That does not make them wrong — they are recorded in the dictionaries and they are what quizzes expect — but it is worth knowing that the 1486 book was partly a joke book for gentlemen, alongside a <em>superfluity of nuns</em> and a <em>doctrine of doctors</em>.</p>

<h3>The short ones for crosswords</h3>
<p><strong>3:</strong> pod, mob. <strong>4:</strong> herd, pack, raft, knot, bevy, cast, army. <strong>5:</strong> pride, swarm, flock, crash, bloat, troop, charm, skein. <strong>6:</strong> gaggle, colony, cackle, dazzle, prickle. <strong>7:</strong> murder, shiver.</p>
"""),

    # ==================================================================
    _a('longest-rivers-in-the-world', 'The Longest Rivers in the World, and the Argument About First Place',
       REF,
       'The top twenty rivers by length, which continent each drains, and why the Nile and the Amazon have been swapping the number one spot for decades.',
       '/static/img/articles/rivers.jpg',
       """
<p>Rivers are reliable quiz territory, with one catch: the top of the list is genuinely disputed. Measurements depend on where you decide a river begins, and reasonable people disagree.</p>

<h3>The top twenty</h3>
<table>
<tr><th>#</th><th>River</th><th>Approx. length</th><th>Continent</th></tr>
<tr><td>1</td><td>Nile</td><td>6,650 km</td><td>Africa</td></tr>
<tr><td>2</td><td>Amazon</td><td>6,400 km</td><td>South America</td></tr>
<tr><td>3</td><td>Yangtze</td><td>6,300 km</td><td>Asia</td></tr>
<tr><td>4</td><td>Mississippi–Missouri</td><td>6,275 km</td><td>North America</td></tr>
<tr><td>5</td><td>Yenisei</td><td>5,540 km</td><td>Asia</td></tr>
<tr><td>6</td><td>Yellow River (Huang He)</td><td>5,460 km</td><td>Asia</td></tr>
<tr><td>7</td><td>Ob</td><td>5,410 km</td><td>Asia</td></tr>
<tr><td>8</td><td>Río de la Plata–Paraná</td><td>4,880 km</td><td>South America</td></tr>
<tr><td>9</td><td>Congo</td><td>4,700 km</td><td>Africa</td></tr>
<tr><td>10</td><td>Amur</td><td>4,440 km</td><td>Asia</td></tr>
<tr><td>11</td><td>Lena</td><td>4,400 km</td><td>Asia</td></tr>
<tr><td>12</td><td>Mekong</td><td>4,350 km</td><td>Asia</td></tr>
<tr><td>13</td><td>Mackenzie</td><td>4,240 km</td><td>North America</td></tr>
<tr><td>14</td><td>Niger</td><td>4,200 km</td><td>Africa</td></tr>
<tr><td>15</td><td>Brahmaputra</td><td>3,850 km</td><td>Asia</td></tr>
<tr><td>16</td><td>Murray–Darling</td><td>3,670 km</td><td>Australia</td></tr>
<tr><td>17</td><td>Tocantins</td><td>3,650 km</td><td>South America</td></tr>
<tr><td>18</td><td>Volga</td><td>3,530 km</td><td>Europe</td></tr>
<tr><td>19</td><td>Indus</td><td>3,180 km</td><td>Asia</td></tr>
<tr><td>20</td><td>Danube</td><td>2,850 km</td><td>Europe</td></tr>
</table>

<h3>Why the top two keep swapping</h3>
<p>The Nile has traditionally held first place, and most quizzes still expect it. But a 2007 Brazilian expedition traced the Amazon to a different headwater high in the Peruvian Andes, which added enough length to put it ahead.</p>
<p>The disagreement comes down to three choices. Which tributary counts as the true source? Where does the river end — at the last narrow channel, or out through a wide estuary? And how do you measure a channel that braids and wanders across a floodplain? Change any one of those and the order changes.</p>
<p>What is not disputed: the <strong>Amazon</strong> carries vastly more water than any other river, roughly as much as the next seven combined.</p>

<h3>Europe’s own order</h3>
<p>The Volga is Europe’s longest at about 3,530 km, followed by the Danube at 2,850 km. The Danube is the more quizzed of the two because it passes through or touches ten countries, more than any other river in the world, and four capital cities: Vienna, Bratislava, Budapest and Belgrade.</p>

<h3>Short river names for crosswords</h3>
<p><strong>2:</strong> Ob. <strong>3:</strong> Po, Exe, Dee, Ure. <strong>4:</strong> Nile, Ouse, Aire, Tyne, Amur, Lena, Oder, Elbe. <strong>5:</strong> Rhine, Volga, Tiber, Trent, Indus, Niger, Congo, Severn (6). The Exe, Ouse and Ure are solvers’ favourites because of the vowels.</p>
"""),

    # ==================================================================
    _a('roman-numerals-explained', 'Roman Numerals, Explained Properly',
       REF,
       'The seven letters, the subtraction rule, how to read a long numeral at a glance, and the years that trip people up — including why 1999 is not MIM.',
       '/static/img/articles/roman-numerals.svg',
       """
<p>Roman numerals turn up on clock faces, film credits, monarchs, Super Bowls and, constantly, in cryptic crosswords. The system is small enough to learn in ten minutes.</p>

<h3>The seven letters</h3>
<table>
<tr><th>Letter</th><th>Value</th></tr>
<tr><td>I</td><td>1</td></tr>
<tr><td>V</td><td>5</td></tr>
<tr><td>X</td><td>10</td></tr>
<tr><td>L</td><td>50</td></tr>
<tr><td>C</td><td>100</td></tr>
<tr><td>D</td><td>500</td></tr>
<tr><td>M</td><td>1,000</td></tr>
</table>
<p>A useful way to hold the order: <em>I Value Xylophones Like Cows Dig Milk</em>.</p>

<h3>The two rules</h3>
<p><strong>Add when the letters descend.</strong> VIII is 5 + 1 + 1 + 1 = 8. LXX is 50 + 10 + 10 = 70.</p>
<p><strong>Subtract when a smaller letter comes before a larger one.</strong> IV is 4, IX is 9, XL is 40, XC is 90, CD is 400, CM is 900.</p>
<p>Only six subtractive pairs are allowed: <strong>IV, IX, XL, XC, CD, CM</strong>. You may only subtract I from V and X, X from L and C, and C from D and M. That is why 1999 is <strong>MCMXCIX</strong> and never MIM — I cannot be subtracted from M.</p>

<h3>Reading a long numeral</h3>
<p>Work left to right in chunks, thousands first. Take <strong>MCMLXXXIV</strong>:</p>
<ul>
<li>M = 1000</li>
<li>CM = 900 &rarr; 1900</li>
<li>LXXX = 80 &rarr; 1980</li>
<li>IV = 4 &rarr; <strong>1984</strong></li>
</ul>

<h3>Years people get wrong</h3>
<table>
<tr><th>Year</th><th>Numeral</th></tr>
<tr><td>1900</td><td>MCM</td></tr>
<tr><td>1944</td><td>MCMXLIV</td></tr>
<tr><td>1969</td><td>MCMLXIX</td></tr>
<tr><td>1999</td><td>MCMXCIX</td></tr>
<tr><td>2000</td><td>MM</td></tr>
<tr><td>2024</td><td>MMXXIV</td></tr>
<tr><td>2026</td><td>MMXXVI</td></tr>
</table>

<h3>The clock face oddity</h3>
<p>Traditional clock faces print four as <strong>IIII</strong>, not IV. Nobody is certain why. The most likely explanation is visual balance — IIII on the left mirrors VIII on the right — and the habit simply stuck. Big Ben is a notable exception and uses IV.</p>

<h3>Why crossword setters love them</h3>
<p>Roman numerals let a setter smuggle letters into an answer. "Fifty" means <strong>L</strong>. "Hundred" means <strong>C</strong>. "Thousand" or "a grand" means <strong>M</strong>. "Five hundred" means <strong>D</strong>. "One" at the start of a word is very often <strong>I</strong>. If a clue mentions a number and the answer does not look numeric, this is almost always what is going on.</p>
"""),

]
