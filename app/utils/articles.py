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

    # ==================================================================
    _a('every-shakespeare-play', 'Every Shakespeare Play, Grouped and Dated',
       REF,
       'All 38 plays sorted into comedies, histories, tragedies and romances, with approximate dates, the ones of disputed authorship, and the short titles setters reach for.',
       '/static/img/articles/shakespeare.jpg',
       """
<p>Shakespeare wrote somewhere around 38 plays, depending on how you count collaborations. The First Folio of 1623 sorted them into three groups — comedies, histories and tragedies — and scholars later added a fourth, the late romances.</p>

<h3>Comedies</h3>
<p>All’s Well That Ends Well · As You Like It · The Comedy of Errors · Love’s Labour’s Lost · Measure for Measure · The Merchant of Venice · The Merry Wives of Windsor · A Midsummer Night’s Dream · Much Ado About Nothing · The Taming of the Shrew · Twelfth Night · The Two Gentlemen of Verona · The Two Noble Kinsmen · Troilus and Cressida</p>

<h3>Histories</h3>
<p>King John · Richard II · Henry IV Part 1 · Henry IV Part 2 · Henry V · Henry VI Part 1 · Henry VI Part 2 · Henry VI Part 3 · Richard III · Henry VIII</p>

<h3>Tragedies</h3>
<p>Antony and Cleopatra · Coriolanus · Hamlet · Julius Caesar · King Lear · Macbeth · Othello · Romeo and Juliet · Timon of Athens · Titus Andronicus</p>

<h3>Late romances</h3>
<p>Cymbeline · Pericles · The Tempest · The Winter’s Tale</p>

<h3>Roughly when</h3>
<table>
<tr><th>Period</th><th>Plays</th></tr>
<tr><td>c.1590–1594</td><td>The Henry VI plays, Richard III, The Comedy of Errors, Titus Andronicus, The Taming of the Shrew</td></tr>
<tr><td>c.1595–1599</td><td>Romeo and Juliet, A Midsummer Night’s Dream, Richard II, The Merchant of Venice, Henry IV, Much Ado, Henry V, Julius Caesar</td></tr>
<tr><td>c.1600–1606</td><td>Hamlet, Twelfth Night, Othello, Measure for Measure, King Lear, Macbeth</td></tr>
<tr><td>c.1607–1613</td><td>Antony and Cleopatra, Coriolanus, Pericles, Cymbeline, The Winter’s Tale, The Tempest, Henry VIII</td></tr>
</table>

<h3>The disputed ones</h3>
<ul>
<li><strong>Pericles</strong> and <strong>Henry VIII</strong> are widely accepted as collaborations, the latter with John Fletcher.</li>
<li><strong>The Two Noble Kinsmen</strong> is also Shakespeare and Fletcher, and was left out of the First Folio entirely.</li>
<li><strong>Edward III</strong> is now included in some complete editions and not in others.</li>
<li><strong>Cardenio</strong> is lost. <strong>Love’s Labour’s Won</strong> is referred to in a 1598 list and may be a lost play or an alternative title for one we already have.</li>
</ul>

<h3>Facts quizzes ask for</h3>
<ul>
<li><strong>Longest play:</strong> Hamlet, around 4,000 lines. Uncut it runs over four hours.</li>
<li><strong>Shortest:</strong> The Comedy of Errors, at roughly 1,800 lines.</li>
<li><strong>Only play set largely in Scotland:</strong> Macbeth — traditionally called "the Scottish play" in a theatre, to avoid the bad luck of naming it.</li>
<li><strong>The one with a bear:</strong> The Winter’s Tale, and its famous stage direction, "Exit, pursued by a bear".</li>
</ul>

<h3>Short titles for crosswords</h3>
<p><strong>6:</strong> Hamlet. <strong>7:</strong> Macbeth, Othello, Pericles. <strong>8:</strong> King Lear, Cymbeline. Setters also love single characters: <strong>Iago</strong> (4), <strong>Puck</strong> (4), <strong>Lear</strong> (4), <strong>Ariel</strong> (5), <strong>Hamlet</strong> (6), <strong>Juliet</strong> (6), <strong>Oberon</strong> (6), <strong>Shylock</strong> (7).</p>
"""),

    # ==================================================================
    _a('nato-phonetic-alphabet', 'The NATO Phonetic Alphabet, and Why It Sounds Like That',
       REF,
       'Alfa to Zulu in full, the numbers, the two words that are deliberately misspelled, and what the alphabet replaced — including the British one with Ack and Beer.',
       '/static/img/articles/phonetic-alphabet.svg',
       """
<p>The spelling alphabet used by aviation, shipping, the military and anyone reading a postcode down a bad phone line was agreed in 1956 after years of testing. Every word was chosen to survive noise, distortion and a heavy accent at either end.</p>

<h3>The alphabet</h3>
<table>
<tr><th>Letter</th><th>Word</th><th>Letter</th><th>Word</th></tr>
<tr><td>A</td><td>Alfa</td><td>N</td><td>November</td></tr>
<tr><td>B</td><td>Bravo</td><td>O</td><td>Oscar</td></tr>
<tr><td>C</td><td>Charlie</td><td>P</td><td>Papa</td></tr>
<tr><td>D</td><td>Delta</td><td>Q</td><td>Quebec</td></tr>
<tr><td>E</td><td>Echo</td><td>R</td><td>Romeo</td></tr>
<tr><td>F</td><td>Foxtrot</td><td>S</td><td>Sierra</td></tr>
<tr><td>G</td><td>Golf</td><td>T</td><td>Tango</td></tr>
<tr><td>H</td><td>Hotel</td><td>U</td><td>Uniform</td></tr>
<tr><td>I</td><td>India</td><td>V</td><td>Victor</td></tr>
<tr><td>J</td><td>Juliett</td><td>W</td><td>Whiskey</td></tr>
<tr><td>K</td><td>Kilo</td><td>X</td><td>X-ray</td></tr>
<tr><td>L</td><td>Lima</td><td>Y</td><td>Yankee</td></tr>
<tr><td>M</td><td>Mike</td><td>Z</td><td>Zulu</td></tr>
</table>

<h3>The two deliberate misspellings</h3>
<p><strong>Alfa</strong>, not Alpha. <strong>Juliett</strong>, with two Ts. Both are spelled that way on purpose. "Ph" is not pronounced as an F in several languages, and a French speaker reading "Juliet" would be inclined to leave the T silent. The odd spellings remove the ambiguity.</p>

<h3>The numbers</h3>
<p>Zero · One · Two · Three · Four · Five · Six · Seven · Eight · Niner. <strong>Niner</strong> keeps nine from being confused with the German <em>nein</em>, and three and five are often said as "tree" and "fife" in aviation for the same sort of reason.</p>

<h3>What came before</h3>
<p>Britain used several systems. The First World War signallers used <strong>Ack, Beer, Charlie, Don, Edward</strong> — which is where "ack-ack" for anti-aircraft fire comes from, from AA. The RAF in the Second World War used <strong>Able, Baker, Charlie, Dog, Easy, Fox</strong>, and American forces used a close variant, which is why "Able Baker" turns up in war films.</p>
<p>The problem was that these alphabets were full of sounds that do not exist in every language. The 1956 set was tested on speakers of many languages under deliberately poor conditions, and only words that survived all of it were kept.</p>

<h3>Where it shows up in quizzes</h3>
<ul>
<li><strong>Only three are place names... almost.</strong> India, Lima, Quebec are cities or countries. Sierra and Victor are not.</li>
<li><strong>Whiskey</strong> is spelled the Irish and American way, with an E, not the Scottish way.</li>
<li><strong>Oscar, Victor and Mike</strong> are the three that are ordinary first names.</li>
<li><strong>Hotel, Golf, Tango, Foxtrot</strong> — the four that are things you can do or stay in.</li>
</ul>
"""),

    # ==================================================================
    _a('zodiac-signs-and-symbols', 'The Twelve Zodiac Signs, Their Dates and Their Symbols',
       REF,
       'Each sign with its dates, symbol, ruling planet and element, the Latin names setters use, and the thirteenth constellation that is not a sign.',
       '/static/img/articles/zodiac.svg',
       """
<p>Whatever you make of astrology, the zodiac is quiz and crossword furniture. The names are Latin, they are short, and each has a symbol, an element and a ruling planet attached.</p>

<h3>The twelve</h3>
<table>
<tr><th>Sign</th><th>Symbol</th><th>Dates</th><th>Element</th><th>Ruler</th></tr>
<tr><td>Aries</td><td>The Ram</td><td>21 Mar – 19 Apr</td><td>Fire</td><td>Mars</td></tr>
<tr><td>Taurus</td><td>The Bull</td><td>20 Apr – 20 May</td><td>Earth</td><td>Venus</td></tr>
<tr><td>Gemini</td><td>The Twins</td><td>21 May – 20 Jun</td><td>Air</td><td>Mercury</td></tr>
<tr><td>Cancer</td><td>The Crab</td><td>21 Jun – 22 Jul</td><td>Water</td><td>The Moon</td></tr>
<tr><td>Leo</td><td>The Lion</td><td>23 Jul – 22 Aug</td><td>Fire</td><td>The Sun</td></tr>
<tr><td>Virgo</td><td>The Maiden</td><td>23 Aug – 22 Sep</td><td>Earth</td><td>Mercury</td></tr>
<tr><td>Libra</td><td>The Scales</td><td>23 Sep – 22 Oct</td><td>Air</td><td>Venus</td></tr>
<tr><td>Scorpio</td><td>The Scorpion</td><td>23 Oct – 21 Nov</td><td>Water</td><td>Pluto / Mars</td></tr>
<tr><td>Sagittarius</td><td>The Archer</td><td>22 Nov – 21 Dec</td><td>Fire</td><td>Jupiter</td></tr>
<tr><td>Capricorn</td><td>The Goat</td><td>22 Dec – 19 Jan</td><td>Earth</td><td>Saturn</td></tr>
<tr><td>Aquarius</td><td>The Water Bearer</td><td>20 Jan – 18 Feb</td><td>Air</td><td>Uranus / Saturn</td></tr>
<tr><td>Pisces</td><td>The Fish</td><td>19 Feb – 20 Mar</td><td>Water</td><td>Neptune / Jupiter</td></tr>
</table>

<h3>Things worth knowing</h3>
<ul>
<li><strong>Only one sign has no animal or human figure.</strong> Libra, the scales. Every other sign is a creature or a person.</li>
<li><strong>Four elements, three signs each.</strong> Fire: Aries, Leo, Sagittarius. Earth: Taurus, Virgo, Capricorn. Air: Gemini, Libra, Aquarius. Water: Cancer, Scorpio, Pisces.</li>
<li><strong>Aquarius is an air sign</strong>, despite carrying water. This catches people out constantly.</li>
<li><strong>Two signs are half-and-half.</strong> Sagittarius is a centaur, Capricorn traditionally a goat with a fish’s tail.</li>
<li><strong>The dates shift slightly</strong> year to year, because the sun does not cross the boundaries at the same clock time each year.</li>
</ul>

<h3>The thirteenth constellation</h3>
<p><strong>Ophiuchus</strong>, the serpent bearer, sits on the ecliptic between Scorpio and Sagittarius, so the sun passes through it every year. It has never been one of the twelve signs, because the zodiac divides the sky into twelve equal thirty-degree slices rather than following constellation boundaries. Every few years a news story announces that star signs have "changed". They have not.</p>

<h3>For crossword solvers</h3>
<p><strong>3:</strong> Leo. <strong>5:</strong> Aries, Libra, Virgo. <strong>6:</strong> Taurus, Gemini, Cancer, Pisces. <strong>7:</strong> Scorpio. <strong>8:</strong> Aquarius. <strong>9:</strong> Capricorn. <strong>11:</strong> Sagittarius. "The Ram", "the bull", "the scales" and "the archer" in a clue are nearly always pointing at these.</p>
"""),

    # ==================================================================
    _a('seven-wonders-ancient-and-new', 'The Seven Wonders, Ancient and New',
       REF,
       'The original seven wonders of the ancient world, which survives, the modern replacement list voted on in 2007, and the natural wonders people confuse with both.',
       '/static/img/articles/pyramids.jpg',
       """
<p>There are at least three "seven wonders" lists in circulation, and quiz questions rarely say which one they mean. Here are all of them.</p>

<h3>The seven wonders of the ancient world</h3>
<table>
<tr><th>Wonder</th><th>Where</th><th>Fate</th></tr>
<tr><td>Great Pyramid of Giza</td><td>Egypt</td><td>Still standing</td></tr>
<tr><td>Hanging Gardens of Babylon</td><td>Iraq</td><td>Possibly never existed</td></tr>
<tr><td>Statue of Zeus at Olympia</td><td>Greece</td><td>Lost, probably to fire</td></tr>
<tr><td>Temple of Artemis at Ephesus</td><td>Turkey</td><td>Destroyed, rebuilt, destroyed again</td></tr>
<tr><td>Mausoleum at Halicarnassus</td><td>Turkey</td><td>Brought down by earthquakes</td></tr>
<tr><td>Colossus of Rhodes</td><td>Greece</td><td>Fell in an earthquake after 54 years</td></tr>
<tr><td>Lighthouse of Alexandria</td><td>Egypt</td><td>Toppled by earthquakes</td></tr>
</table>

<p><strong>Only the Great Pyramid survives</strong>, and it is also the oldest of the seven by a very long way — around two thousand years older than any of the others.</p>

<h3>Three things worth knowing</h3>
<ul>
<li><strong>The Hanging Gardens may be a myth.</strong> No Babylonian text mentions them, and no archaeological trace has been found. One theory is that the descriptions actually refer to gardens at Nineveh, a different city altogether.</li>
<li><strong>The Colossus did not straddle the harbour.</strong> That image comes from medieval illustrations. It stood on one side, and at around 33 metres it was roughly the height of the Statue of Liberty without her pedestal.</li>
<li><strong>"Mausoleum" is a word because of one of them.</strong> The tomb of Mausolus at Halicarnassus was so famous that his name became the general term for any grand tomb.</li>
</ul>

<h3>The new seven wonders, voted in 2007</h3>
<table>
<tr><th>Wonder</th><th>Country</th></tr>
<tr><td>Great Wall of China</td><td>China</td></tr>
<tr><td>Petra</td><td>Jordan</td></tr>
<tr><td>Christ the Redeemer</td><td>Brazil</td></tr>
<tr><td>Machu Picchu</td><td>Peru</td></tr>
<tr><td>Chichén Itzá</td><td>Mexico</td></tr>
<tr><td>Colosseum</td><td>Italy</td></tr>
<tr><td>Taj Mahal</td><td>India</td></tr>
</table>
<p>The Great Pyramid was given honorary status rather than being made to compete, after Egypt objected to the whole exercise.</p>

<h3>And the natural seven</h3>
<p>There is no single agreed list, but the most commonly cited one runs: the Grand Canyon, the Great Barrier Reef, the Harbour of Rio de Janeiro, Mount Everest, the Northern Lights, Parícutin volcano and Victoria Falls.</p>
"""),

    # ==================================================================
    _a('what-money-is-called-around-the-world', 'What Money Is Called Around the World',
       REF,
       'The currency of every country worth knowing, the ones that share a name, the shortest and strangest, and what a rand, a rial and a ringgit actually belong to.',
       '/static/img/articles/currencies.jpg',
       """
<p>Currencies are a crossword favourite because so many are short, vowel-heavy and unmistakable: <strong>euro</strong>, <strong>rand</strong>, <strong>yen</strong>, <strong>lira</strong>, <strong>peso</strong>.</p>

<h3>Europe</h3>
<table>
<tr><th>Country</th><th>Currency</th></tr>
<tr><td>Eurozone (20 countries)</td><td>Euro</td></tr>
<tr><td>United Kingdom</td><td>Pound sterling</td></tr>
<tr><td>Switzerland</td><td>Swiss franc</td></tr>
<tr><td>Norway, Denmark, Sweden, Iceland</td><td>Krone / krona</td></tr>
<tr><td>Poland</td><td>Zloty</td></tr>
<tr><td>Czechia</td><td>Koruna</td></tr>
<tr><td>Hungary</td><td>Forint</td></tr>
<tr><td>Romania</td><td>Leu</td></tr>
<tr><td>Bulgaria</td><td>Lev</td></tr>
<tr><td>Ukraine</td><td>Hryvnia</td></tr>
<tr><td>Russia</td><td>Rouble</td></tr>
<tr><td>Turkey</td><td>Lira</td></tr>
</table>

<h3>Asia and the Middle East</h3>
<table>
<tr><th>Country</th><th>Currency</th></tr>
<tr><td>Japan</td><td>Yen</td></tr>
<tr><td>China</td><td>Yuan (the renminbi)</td></tr>
<tr><td>India, Pakistan, Sri Lanka, Nepal</td><td>Rupee</td></tr>
<tr><td>South Korea, North Korea</td><td>Won</td></tr>
<tr><td>Thailand</td><td>Baht</td></tr>
<tr><td>Vietnam</td><td>Dong</td></tr>
<tr><td>Malaysia</td><td>Ringgit</td></tr>
<tr><td>Indonesia</td><td>Rupiah</td></tr>
<tr><td>Israel</td><td>Shekel</td></tr>
<tr><td>Saudi Arabia, Qatar, Oman</td><td>Riyal / rial</td></tr>
<tr><td>Iran</td><td>Rial</td></tr>
<tr><td>Iraq, Jordan, Kuwait</td><td>Dinar</td></tr>
</table>

<h3>Africa and the Americas</h3>
<table>
<tr><th>Country</th><th>Currency</th></tr>
<tr><td>South Africa</td><td>Rand</td></tr>
<tr><td>Nigeria</td><td>Naira</td></tr>
<tr><td>Ghana</td><td>Cedi</td></tr>
<tr><td>Kenya, Tanzania, Uganda</td><td>Shilling</td></tr>
<tr><td>Egypt</td><td>Egyptian pound</td></tr>
<tr><td>Morocco</td><td>Dirham</td></tr>
<tr><td>Ethiopia</td><td>Birr</td></tr>
<tr><td>Brazil</td><td>Real</td></tr>
<tr><td>Mexico, Argentina, Chile, Colombia</td><td>Peso</td></tr>
<tr><td>Peru</td><td>Sol</td></tr>
<tr><td>Venezuela</td><td>Bolívar</td></tr>
<tr><td>Costa Rica</td><td>Colón</td></tr>
</table>

<h3>The ones that catch people out</h3>
<ul>
<li><strong>China has two names for its money.</strong> The renminbi is the currency; the yuan is the unit. Like sterling and the pound.</li>
<li><strong>Not every "dollar" is American.</strong> Australia, Canada, New Zealand, Singapore, Hong Kong, Jamaica, Fiji and more all use dollars.</li>
<li><strong>Switzerland does not use the euro.</strong> Nor do Norway, Sweden, Denmark, Poland, Czechia or Hungary, all of which are in Europe and several of which are in the EU.</li>
<li><strong>Panama and Ecuador use the US dollar</strong> as their own currency, as do several others.</li>
<li><strong>The Scottish and Northern Irish notes</strong> are pounds sterling, issued by commercial banks rather than the Bank of England. They are not a separate currency.</li>
</ul>

<h3>Short ones for crosswords</h3>
<p><strong>3:</strong> yen, won, sol, lek, leu, lev. <strong>4:</strong> euro, rand, baht, dong, cedi, birr, mark, lira. <strong>5:</strong> pound, krona, krone, zloty, pesos, rupee, franc, dinar, naira, riyal.</p>
"""),

    # ==================================================================
    _a('first-twenty-elements', 'The First Twenty Elements, and How to Remember Them',
       REF,
       'Hydrogen to calcium in order, with symbols and atomic numbers, a mnemonic that actually sticks, and what each one is for.',
       '/static/img/articles/elements.svg',
       """
<p>Quiz questions about the periodic table almost always live in the first twenty. Learn these in order and you have covered most of what any general knowledge round will ask.</p>

<h3>The first twenty</h3>
<table>
<tr><th>#</th><th>Element</th><th>Symbol</th><th>Known for</th></tr>
<tr><td>1</td><td>Hydrogen</td><td>H</td><td>Lightest and most abundant element</td></tr>
<tr><td>2</td><td>Helium</td><td>He</td><td>Balloons; the only element found in the sun first</td></tr>
<tr><td>3</td><td>Lithium</td><td>Li</td><td>Batteries; lightest metal</td></tr>
<tr><td>4</td><td>Beryllium</td><td>Be</td><td>Light, stiff, used in aerospace</td></tr>
<tr><td>5</td><td>Boron</td><td>B</td><td>Borax, heat-resistant glass</td></tr>
<tr><td>6</td><td>Carbon</td><td>C</td><td>The basis of all known life</td></tr>
<tr><td>7</td><td>Nitrogen</td><td>N</td><td>78% of the air</td></tr>
<tr><td>8</td><td>Oxygen</td><td>O</td><td>21% of the air; breathing</td></tr>
<tr><td>9</td><td>Fluorine</td><td>F</td><td>Toothpaste; most reactive element</td></tr>
<tr><td>10</td><td>Neon</td><td>Ne</td><td>Signs that glow orange-red</td></tr>
<tr><td>11</td><td>Sodium</td><td>Na</td><td>Half of table salt</td></tr>
<tr><td>12</td><td>Magnesium</td><td>Mg</td><td>Burns bright white; in chlorophyll</td></tr>
<tr><td>13</td><td>Aluminium</td><td>Al</td><td>Cans, foil, aircraft</td></tr>
<tr><td>14</td><td>Silicon</td><td>Si</td><td>Sand, glass, computer chips</td></tr>
<tr><td>15</td><td>Phosphorus</td><td>P</td><td>Matches; bones and DNA</td></tr>
<tr><td>16</td><td>Sulfur</td><td>S</td><td>The rotten-egg smell</td></tr>
<tr><td>17</td><td>Chlorine</td><td>Cl</td><td>The other half of salt; pools</td></tr>
<tr><td>18</td><td>Argon</td><td>Ar</td><td>Inert filler in light bulbs</td></tr>
<tr><td>19</td><td>Potassium</td><td>K</td><td>Bananas; nerve signals</td></tr>
<tr><td>20</td><td>Calcium</td><td>Ca</td><td>Bones, teeth, chalk</td></tr>
</table>

<h3>A mnemonic that sticks</h3>
<p>Take the initials in order — H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca — and read them as a sentence:</p>
<p><em>"Harry He Likes Beer But Could Not Obtain Food. New Nations Might Also Sign Peace Security Clause. Arthur King Can."</em></p>
<p>It is nonsense, which is exactly why it works. Most people find they can reel off the first ten within a few minutes and the rest within a day.</p>

<h3>Things people get wrong</h3>
<ul>
<li><strong>Helium was found in the sun before it was found on Earth</strong>, in the spectrum of an eclipse in 1868. It is named after Helios.</li>
<li><strong>Hydrogen is not a metal</strong> in ordinary conditions, despite sitting above the alkali metals.</li>
<li><strong>Aluminium and aluminum</strong> are the same element. The international spelling has the extra I; the American one does not.</li>
<li><strong>The lightest metal is lithium</strong>, not aluminium. Lithium floats on water.</li>
<li><strong>Fluorine, not chlorine</strong>, is the most reactive of all elements.</li>
</ul>
"""),

]
