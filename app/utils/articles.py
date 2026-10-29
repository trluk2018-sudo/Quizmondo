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

    # ==================================================================
    _a('why-pluto-stopped-being-a-planet', 'Why Pluto Stopped Being a Planet',
       FACT,
       'Pluto did not change. The definition did, and only because astronomers kept finding more objects like it. What actually happened in 2006, and why the answer is eight.',
       '/static/img/articles/solarsystem.jpg',
       """
<p>Ask how many planets there are and plenty of people still say nine, usually while adding that the whole thing was a bit unfair. Here is what actually happened.</p>

<h3>Pluto was always the odd one out</h3>
<p>Discovered in 1930 by Clyde Tombaugh, Pluto never quite fitted. It is small — smaller than our own Moon. Its orbit is tilted 17 degrees out of the plane the other planets share, and it is so stretched that for twenty years of its 248-year circuit it is closer to the Sun than Neptune. For most of the 20th century this was treated as a charming quirk.</p>

<h3>Then astronomers started finding more of them</h3>
<p>From the 1990s, better telescopes revealed that the outer solar system is full of icy bodies. The Kuiper Belt turned out to contain thousands of objects, and some were not far off Pluto’s size.</p>
<p>The decisive one was <strong>Eris</strong>, found in 2005. It is roughly Pluto’s size and about 27% more massive. Astronomers faced a straight choice: admit Eris as the tenth planet and brace for an eleventh, twelfth and twentieth, or decide what a planet actually is.</p>

<h3>The 2006 definition</h3>
<p>The International Astronomical Union agreed that a planet must do three things:</p>
<ol>
<li><strong>Orbit the Sun.</strong></li>
<li><strong>Be massive enough for its own gravity to pull it into a round shape.</strong></li>
<li><strong>Have "cleared the neighbourhood" around its orbit.</strong></li>
</ol>
<p>Pluto passes the first two comfortably. It fails the third. It shares its region with a vast number of other Kuiper Belt objects and has not swept them up or flung them away, as the eight planets did with their own orbital paths long ago. Pluto was reclassified as a <strong>dwarf planet</strong>.</p>

<h3>The objections, fairly stated</h3>
<p>The vote has been criticised, and not unreasonably. Only a few hundred of the IAU’s thousands of members were present. "Clearing the neighbourhood" is vague — Earth shares its orbit with plenty of near-Earth asteroids, and Jupiter has the Trojans parked in its path. Several planetary scientists, including the lead on NASA’s New Horizons mission to Pluto, still reject the definition and argue for a purely geophysical one based on shape, under which Pluto and several moons would be planets.</p>
<p>That argument is genuine and ongoing. But for quiz purposes the answer is settled: <strong>eight</strong>.</p>

<h3>The five dwarf planets</h3>
<p><strong>Ceres</strong> (in the asteroid belt), <strong>Pluto</strong>, <strong>Haumea</strong>, <strong>Makemake</strong> and <strong>Eris</strong>. Ceres is itself a reclassification story: it was called a planet for about fifty years after its discovery in 1801, until astronomers found so many other asteroids that it was demoted. Pluto is the second object to be treated this way, not the first.</p>

<h3>Worth knowing</h3>
<ul>
<li><strong>Pluto has five moons.</strong> The largest, Charon, is so big relative to Pluto that the pair orbit a point in empty space between them.</li>
<li><strong>Nobody has seen a full Pluto year.</strong> It has not completed one orbit since its discovery, and will not until 2178.</li>
<li><strong>It was named by an eleven-year-old.</strong> Venetia Burney of Oxford suggested the Roman god of the underworld, and her grandfather passed it on.</li>
</ul>
"""),

    # ==================================================================
    _a('animal-facts-that-sound-made-up', 'Twelve Animal Facts That Sound Completely Made Up',
       FACT,
       'Wombat cubes, immortal jellyfish, shrimp that punch at the speed of a bullet, and the bird that sleeps mid-flight — all true, with the reasons why.',
       '/static/img/articles/animal-facts.jpg',
       """
<p>Every one of these is genuinely true, which is why they make such good quiz questions. The explanation is usually more interesting than the fact.</p>

<h3>1. Wombats produce cube-shaped droppings</h3>
<p>Around a hundred a night, and they really are cubic. The last stretch of the wombat’s intestine has regions of differing stiffness that shape the contents as they dry. Cubes do not roll away, which matters for an animal that marks territory on logs and rocks.</p>

<h3>2. Octopuses have three hearts and blue blood</h3>
<p>Two hearts push blood through the gills, one serves the rest of the body. Their blood uses haemocyanin, which carries oxygen with copper rather than iron, making it blue and far more efficient in cold, low-oxygen water. The main heart stops when they swim, which is why they prefer crawling.</p>

<h3>3. A shrimp punches hard enough to boil water</h3>
<p>The mantis shrimp’s club accelerates at the pace of a .22 bullet. It moves so fast that the water behind it vaporises into a bubble, which collapses with a flash of light and a shockwave. The prey is hit twice: once by the club, once by the bubble.</p>

<h3>4. One jellyfish can reverse its own ageing</h3>
<p><em>Turritopsis dohrnii</em>, when injured or starving, can revert its adult cells to an earlier life stage and start again, in principle indefinitely. It is still perfectly edible by everything else in the sea, so immortality is theoretical.</p>

<h3>5. Swifts stay airborne for ten months</h3>
<p>Tracking has shown common swifts flying continuously for up to ten months, feeding, mating and sleeping on the wing. They shut down half the brain at a time while gliding, a trick dolphins also use.</p>

<h3>6. Sea otters hold hands while sleeping</h3>
<p>So they do not drift apart on the current. They also wrap themselves in kelp as an anchor, and each keeps a favourite stone in a pouch of loose skin under the foreleg for breaking shells.</p>

<h3>7. Cows have best friends</h3>
<p>Research at Northampton found that cows paired with a preferred companion had measurably lower heart rates than those penned with a random animal. Separate the pair and stress hormones rise.</p>

<h3>8. A flamingo is not born pink</h3>
<p>Chicks are grey. The colour comes from carotenoid pigments in the algae and brine shrimp they eat, processed in the liver and deposited in the feathers. A flamingo on the wrong diet fades to white.</p>

<h3>9. Tardigrades survive the vacuum of space</h3>
<p>In 2007 tardigrades were exposed to open space for ten days, and some survived and reproduced afterwards. They can enter a desiccated state called a tun, replacing their water with a sugar that turns their cells to glass.</p>

<h3>10. Elephants cannot jump</h3>
<p>Alone among mammals, they have no moment with all four feet off the ground at once. Their legs are built as weight-bearing columns, with little of the springy tendon that powers a jump, and the bones could not take the landing.</p>

<h3>11. A snail can sleep for three years</h3>
<p>Some desert and land snails seal themselves into their shell with dried mucus and enter estivation, waiting out drought. Revivals after several years are documented, including a British Museum specimen glued to a display card in 1846 that turned out to be alive four years later.</p>

<h3>12. Crows recognise faces and hold grudges</h3>
<p>A University of Washington study had researchers wear a particular mask while trapping crows. The birds scolded anyone wearing that mask for years afterwards — including crows that had never been trapped, having learned it from the others.</p>
"""),

    # ==================================================================
    _a('the-human-body-in-numbers', 'The Human Body in Numbers',
       FACT,
       'Bones, beats, blood, blinks and breaths. The figures that come up in quizzes, the ones usually quoted wrongly, and what they mean.',
       '/static/img/articles/body-numbers.svg',
       """
<p>A body is a set of surprisingly quotable numbers. These are the ones worth knowing, with the common mistakes flagged.</p>

<h3>The structure</h3>
<table>
<tr><th>Measure</th><th>Number</th></tr>
<tr><td>Bones in an adult</td><td>206</td></tr>
<tr><td>Bones at birth</td><td>About 300, many of which fuse</td></tr>
<tr><td>Bones in each hand</td><td>27</td></tr>
<tr><td>Bones in each foot</td><td>26</td></tr>
<tr><td>Skeletal muscles</td><td>About 600</td></tr>
<tr><td>Teeth, adult</td><td>32, including wisdom teeth</td></tr>
<tr><td>Teeth, child</td><td>20 milk teeth</td></tr>
<tr><td>Pairs of ribs</td><td>12</td></tr>
<tr><td>Vertebrae in the neck</td><td>7</td></tr>
</table>
<p>More than half the bones in the body are in the hands and feet — 106 of 206 between them.</p>

<h3>The running costs</h3>
<table>
<tr><th>Measure</th><th>Number</th></tr>
<tr><td>Resting heart rate</td><td>60–100 beats a minute</td></tr>
<tr><td>Heartbeats in a year</td><td>Roughly 35 million</td></tr>
<tr><td>Breaths a day</td><td>Around 20,000</td></tr>
<tr><td>Blood volume</td><td>About 5 litres</td></tr>
<tr><td>Blinks a day</td><td>Around 15,000 to 20,000</td></tr>
<tr><td>Litres of saliva a year</td><td>Roughly 500</td></tr>
<tr><td>Body temperature</td><td>About 37°C, though the average is now measured a little lower</td></tr>
<tr><td>Water as a share of body mass</td><td>About 60% in an adult</td></tr>
</table>

<h3>The very small and very long</h3>
<ul>
<li><strong>Smallest bone:</strong> the stapes, about 3 mm, in the middle ear.</li>
<li><strong>Longest bone:</strong> the femur, roughly a quarter of your height.</li>
<li><strong>Longest nerve:</strong> the sciatic, from the lower back to the foot.</li>
<li><strong>Blood vessels end to end:</strong> commonly quoted as 100,000 km, which is an estimate built on estimates. Treat it as "a very long way" rather than a fact.</li>
<li><strong>Strongest muscle:</strong> depends what you mean. The masseter, in the jaw, exerts most force for its size; the gluteus maximus is the largest; the heart does the most total work.</li>
</ul>

<h3>Figures people repeat that are wrong</h3>
<ul>
<li><strong>"You only use 10% of your brain."</strong> Entirely false. Brain imaging shows activity throughout, and there is no idle 90%.</li>
<li><strong>"The body replaces itself every seven years."</strong> Some cells turn over in days, others in decades. The lens of the eye and most neurons of the cerebral cortex stay with you for life.</li>
<li><strong>"Fingernails keep growing after death."</strong> The skin retracts as it dehydrates, which makes nails and stubble look longer. Nothing is growing.</li>
<li><strong>"Humans have five senses."</strong> A convention from Aristotle. Balance, temperature, pain and proprioception — knowing where your limbs are without looking — are all separate senses.</li>
</ul>
"""),

    # ==================================================================
    _a('how-the-days-of-the-week-got-their-names', 'How the Days of the Week Got Their Names',
       FACT,
       'Four English days are named after Norse gods, two after the sun and moon, and one after a Roman. The full derivation, and why French and Spanish look so different.',
       '/static/img/articles/days-of-week.svg',
       """
<p>English day names are a collision of two systems. The Romans named the days after the seven classical planets, which were themselves named after gods. When those names reached northern Europe, most of the Roman gods were swapped for their closest Germanic equivalent. One was not.</p>

<h3>The seven</h3>
<table>
<tr><th>Day</th><th>From</th><th>Who or what</th></tr>
<tr><td>Monday</td><td>Mōnandæg</td><td>The Moon</td></tr>
<tr><td>Tuesday</td><td>Tīwesdæg</td><td>Tīw, Norse Tyr, god of war and law</td></tr>
<tr><td>Wednesday</td><td>Wōdnesdæg</td><td>Wōden, Norse Odin</td></tr>
<tr><td>Thursday</td><td>Thunresdæg</td><td>Thunor, Norse Thor, god of thunder</td></tr>
<tr><td>Friday</td><td>Frīgedæg</td><td>Frige, linked to Frigg or Freyja</td></tr>
<tr><td>Saturday</td><td>Sæternesdæg</td><td>Saturn — the one Roman name kept</td></tr>
<tr><td>Sunday</td><td>Sunnandæg</td><td>The Sun</td></tr>
</table>

<h3>Why the swap works so neatly</h3>
<p>Line the English names up against the Roman ones and the logic appears:</p>
<table>
<tr><th>Roman</th><th>Germanic stand-in</th><th>Shared role</th></tr>
<tr><td>Mars (<em>martis</em>)</td><td>Tīw / Tyr</td><td>War</td></tr>
<tr><td>Mercury (<em>mercurii</em>)</td><td>Wōden / Odin</td><td>Travel, cunning, the dead</td></tr>
<tr><td>Jupiter (<em>iovis</em>)</td><td>Thunor / Thor</td><td>Thunder, the sky</td></tr>
<tr><td>Venus (<em>veneris</em>)</td><td>Frige</td><td>Love</td></tr>
</table>
<p>This is why French keeps the Roman originals almost intact: <em>mardi</em>, <em>mercredi</em>, <em>jeudi</em>, <em>vendredi</em>. Spanish and Italian do the same. English went through a Norse filter; the Romance languages did not.</p>

<h3>The two ends of the week</h3>
<p>French, Spanish and Italian replaced Sunday with a Christian name — <em>dimanche</em>, <em>domingo</em>, <em>domenica</em>, all from <em>dies Dominicus</em>, the Lord’s day — and Saturday with words derived from Sabbath: <em>samedi</em>, <em>sábado</em>. English kept the older pagan names at both ends.</p>

<h3>Why seven at all?</h3>
<p>The seven-day week has no astronomical basis. It comes from Babylonian astronomy, which tracked seven moving objects in the sky — the Sun, the Moon, Mercury, Venus, Mars, Jupiter and Saturn — and was reinforced by the Jewish Sabbath cycle. The Romans used an eight-day market week before adopting the seven-day one in the first century AD.</p>
<p>It has been attacked since. The French Revolutionary calendar tried ten-day weeks, and the Soviet Union experimented with five and six-day cycles in the 1930s. Both were abandoned.</p>

<h3>For quizzes</h3>
<ul>
<li><strong>Which day is named after a Roman god in English?</strong> Saturday, and only Saturday.</li>
<li><strong>Which Norse god gives us Wednesday?</strong> Odin, as Wōden.</li>
<li><strong>Which two are named after things rather than gods?</strong> Sunday and Monday.</li>
</ul>
"""),

    # ==================================================================
    _a('why-is-the-sea-salty', 'Why Is the Sea Salty?',
       FACT,
       'Rain is fresh, rivers are fresh, and they both drain into the sea. So where does the salt come from, why does it not keep rising, and why is the Dead Sea so much saltier?',
       '/static/img/articles/sea-salt.jpg',
       """
<p>The sea is about 3.5% salt by weight. Scaled up, every litre of seawater holds roughly 35 grams of dissolved solids, mostly sodium chloride. If you spread all the salt in the oceans evenly over the land, it would form a layer about 150 metres deep.</p>

<h3>Where it comes from</h3>
<p>Two sources, working on very different timescales.</p>
<p><strong>Rain, slowly dissolving the land.</strong> Rainwater is slightly acidic, because it picks up carbon dioxide from the air and forms weak carbonic acid. Over millions of years that acid eats at rock, freeing ions of sodium, chloride, calcium and magnesium. Rivers carry them to the sea. Each river is only faintly salty — far too faint to taste — but they have been doing this continuously for billions of years, and the sea is where it all collects.</p>
<p><strong>Hydrothermal vents, from below.</strong> Seawater seeps into cracks in the ocean floor, is heated by magma, strips minerals out of the hot rock and jets back out. Underwater volcanoes add more directly.</p>

<h3>Why rivers stay fresh</h3>
<p>This is the part that confuses people. The answer is that rivers are a conveyor belt, not a container. Water flows through and keeps going, carrying its dissolved minerals out to sea. The sea is the end of the line. Water leaves it only by evaporating, and evaporation takes the water and leaves the salt behind.</p>
<p>A lake with an outflowing river stays fresh for the same reason. A lake with no outlet does not.</p>

<h3>So why is it not getting saltier?</h3>
<p>Because salt leaves too. The ocean has been at roughly its present saltiness for hundreds of millions of years, in a slow balance. Salt is removed when sea spray blows inland, when shallow seas evaporate and leave salt deposits, when minerals react with fresh volcanic rock on the sea floor, and when marine organisms take up calcium and other ions to build shells that eventually become sediment.</p>

<h3>Why the Dead Sea is different</h3>
<p>The Dead Sea is about 34% salt, nearly ten times ordinary seawater. It sits in the lowest land basin on Earth, in a hot, dry climate, and it has <strong>no outlet</strong>. The Jordan brings water in; only evaporation takes it out. Everything dissolved stays, and keeps concentrating.</p>
<p>The same thing happens at the Great Salt Lake in Utah and Lake Assal in Djibouti, which is saltier still.</p>

<h3>Things worth knowing</h3>
<ul>
<li><strong>The Baltic is almost drinkable</strong> in places — under 1% salt, because so many rivers feed it and it exchanges little water with the Atlantic.</li>
<li><strong>The Red Sea is unusually salty</strong> for an open sea, at around 4%, because it is hot, has high evaporation and almost no rivers flowing into it.</li>
<li><strong>Drinking seawater dehydrates you.</strong> Your kidneys cannot produce urine as salty as the sea, so they must use your own body water to flush the excess salt out.</li>
</ul>
"""),

    # ==================================================================
    _a('where-everyday-phrases-come-from', 'Where Everyday Phrases Actually Come From',
       FACT,
       'Fifteen common sayings traced to their real origin — and the popular explanations that turn out to be invented, including almost every acronym story you have heard.',
       '/static/img/articles/phrases.jpg',
       """
<p>Phrase origins attract invented explanations more than almost any other subject. These are the ones that hold up, and a few famous ones that do not.</p>

<h3>Genuine origins</h3>
<p><strong>Rule of thumb.</strong> From using the thumb as a rough measure in brewing, carpentry and cooking. The widely repeated claim that it refers to a law permitting a man to beat his wife with a stick no thicker than his thumb has no legal basis; it comes from an 18th-century joke about a judge, repeated until it sounded official.</p>
<p><strong>Steal someone’s thunder.</strong> Precisely traceable. The playwright John Dennis invented a new way of making thunder noises for his 1704 play, which flopped. He then heard his own thunder machine being used in a production of Macbeth and said, "They steal my thunder."</p>
<p><strong>Turn a blind eye.</strong> Attributed to Nelson at Copenhagen in 1801, who raised a telescope to his blind eye to avoid seeing the signal to withdraw. The story is probably embroidered but is contemporary rather than invented later.</p>
<p><strong>Bite the bullet.</strong> From battlefield surgery before anaesthetic, giving the patient something to clamp down on.</p>
<p><strong>Mad as a hatter.</strong> Hat makers used mercury to treat felt. Chronic mercury poisoning causes tremors, slurred speech and severe anxiety, and the trade’s reputation long predates Lewis Carroll.</p>
<p><strong>Caught red-handed.</strong> A Scottish legal term from the 15th century, meaning a poacher caught with blood still on the hands.</p>
<p><strong>Pull out all the stops.</strong> From organ playing: the stops control which sets of pipes sound, and pulling them all out produces maximum volume.</p>
<p><strong>At loggerheads.</strong> A loggerhead was a long-handled iron tool with a ball on the end, used for heating tar — and apparently for hitting people with.</p>
<p><strong>Saved by the bell.</strong> Boxing, where the bell ends the round before a count is finished. Not, as commonly claimed, from bells on coffins for the accidentally buried; those devices existed but the phrase does not come from them.</p>
<p><strong>Let the cat out of the bag.</strong> Disputed, but most likely from markets where a piglet was sold in a sack and a cat substituted by dishonest traders. Opening the bag revealed the fraud. The same trick gives us "a pig in a poke".</p>

<h3>Origins that are invented</h3>
<p><strong>Almost every acronym story is false.</strong> English made very few words from acronyms before the 20th century. "Posh" does not stand for Port Out, Starboard Home. "Golf" is not Gentlemen Only, Ladies Forbidden. "Tip" is not To Insure Promptness. "News" is not North East West South. Each was reverse-engineered long after the word existed.</p>
<p><strong>Raining cats and dogs</strong> has no convincing origin. The story about animals falling through thatched roofs is a 1990s internet invention, part of a widely circulated list of fake etymologies that also produced "the whole nine yards" and "threshold" explanations.</p>
<p><strong>Sleep tight</strong> is unlikely to refer to tightening rope beds. The adverb "tight" meaning soundly is attested, and rope beds were not usually tightened nightly.</p>

<h3>How to spot a fake</h3>
<p>Be suspicious when the explanation is unusually tidy, when it involves an acronym, when it explains the phrase too literally, and when it comes with a vivid historical scene. Real etymologies are usually messier and often uncertain.</p>
"""),

    # ==================================================================
    _a('how-leap-years-actually-work', 'How Leap Years Actually Work',
       FACT,
       'Every four years, except every hundred, except every four hundred. Why 1900 was not a leap year and 2000 was, and what the extra day is correcting.',
       '/static/img/articles/leap-year.svg',
       """
<p>Most people know leap years come every four years. Fewer know about the two exceptions, which is exactly why they make good quiz questions.</p>

<h3>The problem being solved</h3>
<p>A year is not a whole number of days. The Earth takes about <strong>365.2422 days</strong> to go round the Sun. A calendar of 365 days therefore runs fast by just under a quarter of a day a year.</p>
<p>Left alone, that drifts. After a century the calendar would be 24 days out; after 750 years, midsummer would fall in what the calendar called spring. For an agricultural society, and for a church fixing Easter against the spring equinox, that is a real problem.</p>

<h3>The Julian fix, and why it overcorrected</h3>
<p>Julius Caesar’s calendar of 45 BC added one day every four years, treating the year as exactly 365.25 days. That is close, but it is 11 minutes and 14 seconds too long. Small, but it accumulates: about one day every 128 years. By the 1500s the calendar had drifted ten days from the seasons.</p>

<h3>The Gregorian rule</h3>
<p>In 1582 Pope Gregory XIII’s reform added two exceptions. A year is a leap year if:</p>
<ol>
<li>It is divisible by <strong>4</strong>, <em>unless</em></li>
<li>it is divisible by <strong>100</strong>, <em>unless</em></li>
<li>it is also divisible by <strong>400</strong>.</li>
</ol>
<table>
<tr><th>Year</th><th>Leap?</th><th>Why</th></tr>
<tr><td>2024</td><td>Yes</td><td>Divisible by 4</td></tr>
<tr><td>1900</td><td>No</td><td>Divisible by 100, not by 400</td></tr>
<tr><td>2000</td><td>Yes</td><td>Divisible by 400</td></tr>
<tr><td>2100</td><td>No</td><td>Divisible by 100, not by 400</td></tr>
</table>
<p>This drops three leap days every four centuries, giving an average year of 365.2425 days — within about 27 seconds of the truth, or one day’s error in roughly 3,200 years.</p>

<h3>The ten days that never happened</h3>
<p>Catholic countries adopted the new calendar in October 1582, skipping from the 4th straight to the 15th. Protestant and Orthodox countries held out for a long time. Britain and its colonies did not switch until <strong>1752</strong>, by which point eleven days had to be dropped: 2 September was followed by 14 September. Russia changed only after the 1917 revolution, which is why the October Revolution is commemorated in November.</p>

<h3>Worth knowing</h3>
<ul>
<li><strong>29 February birthdays</strong> affect roughly one person in 1,461.</li>
<li><strong>Leap seconds are a separate thing entirely</strong>, added irregularly to account for the slowing of Earth’s rotation, not its orbit. A decision has been taken to stop using them by 2035.</li>
<li><strong>The leap year tradition of women proposing</strong> on 29 February is a 19th-century invention with a fake Irish backstory attached.</li>
<li><strong>1712 in Sweden had a 30 February.</strong> Sweden botched a gradual transition between calendars, then reverted by adding an extra day. It is the only time that date has existed.</li>
</ul>
"""),

    # ==================================================================
    _a('why-sixty-seconds-in-a-minute', 'Why There Are Sixty Seconds in a Minute',
       FACT,
       'Everything else went metric. Time did not. The answer is Babylonian, involves counting on finger bones, and explains why a circle has 360 degrees too.',
       '/static/img/articles/sixty.svg',
       """
<p>We measure almost everything in tens. Time is the glaring exception: 60 seconds, 60 minutes, 24 hours. The reason is about 4,000 years old.</p>

<h3>The Babylonians counted in sixties</h3>
<p>Sumerian and later Babylonian mathematics used a base-60 system, called sexagesimal. It was not arbitrary. <strong>60 divides cleanly by 1, 2, 3, 4, 5, 6, 10, 12, 15, 20 and 30.</strong> For a civilisation doing arithmetic without decimal fractions, that is enormously convenient: a third of an hour is 20 minutes exactly, a quarter is 15, a fifth is 12. Try that with 100 and you get recurring fractions almost immediately.</p>

<h3>How you count to sixty on two hands</h3>
<p>There is a neat theory for where 60 came from. Each finger, excluding the thumb, has three segments — twelve on one hand. Use the thumb to tap each segment in turn and you count to 12 on one hand. Each time you reach 12, raise one finger on the other hand. Five fingers, twelve each: <strong>60</strong>.</p>
<p>This also explains the stubborn persistence of 12 in English measurement: twelve inches, twelve pence in a shilling, twelve in a dozen.</p>

<h3>How it reached the clock</h3>
<p>The Egyptians divided day and night into twelve parts each, giving 24 hours. Greek astronomers, building on Babylonian records, needed finer divisions for their calculations and divided the hour into 60 <em>partes minutae primae</em> — "first small parts" — and each of those into 60 <em>partes minutae secundae</em>, "second small parts".</p>
<p>That is where the words come from. A <strong>minute</strong> is a minute, meaning tiny, division. A <strong>second</strong> is literally the second division.</p>
<p>Clocks could not measure anything that precise for centuries afterwards. Minute hands only became common in the 1600s, after the pendulum clock made them worth having.</p>

<h3>And why a circle has 360 degrees</h3>
<p>Same source. 360 is six sixties, divides by a great many numbers, and is conveniently close to the number of days in a year — so the sun moves roughly one degree along the ecliptic each day. Minutes and seconds of arc survive in navigation and astronomy for exactly the same reason they survive in time.</p>

<h3>The attempts to change it</h3>
<p>Revolutionary France introduced decimal time in 1793: ten-hour days, 100-minute hours, 100-second minutes. It required everyone to buy a new clock and think in unfamiliar units, and was abandoned within about eighteen months. A decimal calendar of twelve 30-day months plus five spare days lasted rather longer, until Napoleon scrapped it in 1806.</p>
<p>Metric time has been proposed repeatedly since and has never caught on. Sixty has survived every attempt to replace it — not because it is better in the abstract, but because changing it would mean changing every clock, every timetable and every habit at once.</p>
"""),

    # ==================================================================
    _a('why-your-keyboard-says-qwerty', 'Why Your Keyboard Says QWERTY',
       FACT,
       'The layout was designed for a machine with physical levers that jammed. Why it survived the typewriter, whether Dvorak is really faster, and the "typewriter" row myth.',
       '/static/img/articles/qwerty.jpg',
       """
<p>The letters on your keyboard are arranged in an order that made sense for a mechanical device nobody has used in decades. Here is how it happened and why it stuck.</p>

<h3>The jamming problem</h3>
<p>Christopher Latham Sholes built his first practical typewriter in the late 1860s with keys in alphabetical order. On those machines each key swung a metal typebar up to strike the paper. If two bars next to each other were struck in quick succession, they collided and jammed, and the typist had to stop and untangle them by hand.</p>
<p>Sholes rearranged the keys over several years so that letters frequently typed one after another in English sat far apart on the typebar basket, reducing collisions. The layout sold to Remington in 1873 is recognisably QWERTY.</p>

<h3>The "it was designed to slow typists down" claim</h3>
<p>This is half right in a way that is usually told wrong. The goal was never to slow the typist; it was to stop the machine jamming, which in practice let people type <em>faster</em> without stopping to fix it. The distinction matters, and the slowing-down version is repeated far more often than the truth.</p>

<h3>The telegraph theory</h3>
<p>There is decent evidence that early Morse telegraph operators influenced the layout too. They were among the first heavy users, transcribing Morse live, and some of QWERTY’s odder choices — the placement of Z and S, for instance — fit the ambiguities of American Morse better than they fit English letter frequency.</p>

<h3>Why it survived</h3>
<p>By the 1890s, typists had been trained on QWERTY in huge numbers, and schools taught touch-typing on it. Any manufacturer selling a different layout had to persuade buyers to retrain their entire typing pool. The layout outlived the mechanism it was built for because the cost of switching was carried by people, not machines — the textbook example of what economists call path dependence.</p>

<h3>Is Dvorak actually faster?</h3>
<p>August Dvorak patented an alternative in 1936, putting vowels and common consonants on the home row. Early US Navy studies reported large gains, but Dvorak himself was involved in running them, and later independent research has found differences small enough to be within the noise. Speed appears to depend far more on practice than on layout.</p>
<p>Colemak, a more recent design that keeps most keys where QWERTY has them, is the more popular alternative today precisely because it is easier to switch to.</p>

<h3>The typewriter row</h3>
<p>All the letters of "typewriter" appear on the top row — T, Y, P, E, W, R, I, T, E, R. It is widely claimed Sholes arranged this deliberately so salesmen could type the product name quickly. There is no contemporary evidence for it, and it is more likely a coincidence that was noticed afterwards and turned into a story.</p>

<h3>Elsewhere in the world</h3>
<ul>
<li><strong>AZERTY</strong> in France and Belgium.</li>
<li><strong>QWERTZ</strong> in Germany and much of central Europe, where Z is common in German.</li>
<li><strong>QWERTY with modifications</strong> almost everywhere else, including the UK, where the only real differences from the US layout are the position of @, " and the £ sign.</li>
</ul>
"""),

    # ==================================================================
    _a('foods-not-from-where-you-think', 'Nine Foods That Are Not From Where You Think',
       FACT,
       'Chicken tikka masala, fortune cookies, French fries, Swiss fondue and more — dishes whose nationality is a marketing decision, an accident, or simply wrong.',
       '/static/img/articles/food-origins.jpg',
       """
<p>National dishes are often younger and more foreign than they look. These are the ones quizzes love.</p>

<h3>1. Chicken tikka masala — Britain</h3>
<p>Almost certainly invented in a British Indian restaurant, with Glasgow the most commonly claimed birthplace. The usual story has a chef adding a tin of tomato soup and cream to dry tikka for a customer who wanted gravy. Robin Cook called it "a true British national dish" in 2001. It is not served in India except to tourists.</p>

<h3>2. Fortune cookies — Japan, then California</h3>
<p>Not Chinese. Similar crackers containing paper fortunes were made in Kyoto in the 1800s. Japanese immigrants brought them to California, where they were served in Japanese-run tea gardens. During the Second World War, with Japanese Americans interned, Chinese American restaurants took over production, and the cookie became permanently associated with Chinese food.</p>

<h3>3. French fries — probably Belgium</h3>
<p>Belgium claims them, with a tradition of frying small fish in the Meuse valley and switching to potato strips when the river froze. The "French" is thought to come from American soldiers in the First World War who encountered them in French-speaking Belgium. The Belgians are still annoyed about it.</p>

<h3>4. Croissants — Austria</h3>
<p>The crescent-shaped <em>kipferl</em> is Viennese and far older than the French pastry. August Zang opened a Viennese bakery in Paris in 1839, French bakers imitated it, and over the following decades the laminated butter dough we now call a croissant developed in France. The shape is Austrian; the pastry is French.</p>

<h3>5. Swiss fondue — a marketing campaign</h3>
<p>Melted cheese dishes are genuinely old and Alpine. But fondue became <em>the</em> Swiss national dish because the Swiss Cheese Union promoted it heavily from the 1930s to sell surplus cheese, pushing it as patriotic, including into army rations. The same organisation popularised the idea that every meal should end with cheese.</p>

<h3>6. Vindaloo — Portugal</h3>
<p>From the Portuguese <em>carne de vinha d’alhos</em>, meat in wine and garlic, brought to Goa by Portuguese colonists. Local cooks substituted palm vinegar for wine and added chillies — which the Portuguese had themselves brought from the Americas.</p>

<h3>7. Tempura — Portugal again</h3>
<p>Portuguese missionaries in 16th-century Japan ate battered fried fish during Ember Days, periods of fasting from meat. The Latin <em>quattuor tempora</em>, four times, is the likely source of the name. Japanese cooks refined the technique into something far lighter than the original.</p>

<h3>8. German chocolate cake — not German</h3>
<p>Named after Samuel German, an Englishman who developed a type of dark baking chocolate for an American company in 1852. The recipe first appeared in a Dallas newspaper in 1957 as "German’s Chocolate Cake". The apostrophe fell off and the nationality stuck.</p>

<h3>9. Spaghetti bolognese — not really Bologna</h3>
<p>Bologna has <em>ragù alla bolognese</em>, but it is traditionally served with tagliatelle, not spaghetti, and is meatier and far less tomato-heavy than the British version. The dish as most of the world knows it developed abroad. The mayor of Bologna has publicly complained about it more than once.</p>

<h3>And one that is exactly what it says</h3>
<p><strong>Hawaiian pizza</strong> is Canadian. Invented in Ontario in 1962 by Sam Panopoulos, a Greek immigrant, and named after the brand of tinned pineapple he used.</p>
"""),

    # ==================================================================
    _a('what-flags-are-telling-you', 'What Flags Are Actually Telling You',
       FACT,
       'Crescents, crosses, stars, pan-African and pan-Arab colours. How to read a national flag you have never seen before, and the rules most of them follow.',
       '/static/img/articles/flags.svg',
       """
<p>Flags are not random. Once you know a handful of patterns you can make a decent guess at a flag’s region, and often its history, without recognising it at all.</p>

<h3>The Nordic cross</h3>
<p>An off-centre cross, shifted towards the hoist, marks a Nordic country: Denmark, Sweden, Norway, Finland and Iceland, plus the Faroe Islands and Åland. Denmark’s Dannebrog is the original and is traditionally dated to 1219, making it the oldest continuously used national flag. Every other Nordic flag is a deliberate copy of its layout.</p>

<h3>Pan-Slavic colours</h3>
<p>Red, white and blue in horizontal bands runs through Russia, Serbia, Slovakia, Slovenia, Croatia and Czechia. The scheme was adopted at a Slavic congress in Prague in 1848, borrowing from the Russian flag, which had itself borrowed from the Dutch.</p>

<h3>Pan-African colours</h3>
<p>Red, gold and green — often with black — appear across Ghana, Senegal, Mali, Guinea, Cameroon, Ethiopia and many more. Ethiopia is the source: it was the African state that resisted colonisation, and newly independent countries adopted its colours deliberately. Red for blood shed, gold for mineral wealth, green for the land.</p>

<h3>Pan-Arab colours</h3>
<p>Red, white, black and green mark Jordan, Palestine, Kuwait, Sudan, the UAE, Iraq, Syria, Egypt and Yemen. They derive from the flag of the Arab Revolt of 1916, each colour representing a historic dynasty or era: black for the Abbasids, white for the Umayyads, green for the Fatimids, red for the Hashemites.</p>

<h3>The crescent and star</h3>
<p>Common across Muslim-majority countries — Turkey, Pakistan, Tunisia, Algeria, Malaysia, Azerbaijan. It is an Ottoman inheritance rather than a religious requirement, which is why many Muslim countries do not use it. Saudi Arabia instead carries the <em>shahada</em> in script above a sword, and because the text is sacred, the flag is never flown at half-mast.</p>

<h3>The Union Jack in the corner</h3>
<p>A canton with the Union Flag marks a current or former British territory: Australia, New Zealand, Fiji, Tuvalu, and various overseas territories. Distinguishing Australia from New Zealand is a standard quiz trap — Australia has six white stars including a large seven-pointed Commonwealth Star; New Zealand has four red stars with white borders.</p>

<h3>The rules most flags follow</h3>
<ul>
<li><strong>Keep it simple</strong> enough for a child to draw from memory.</li>
<li><strong>Use meaningful symbolism</strong> rather than decoration.</li>
<li><strong>Use two or three basic colours.</strong></li>
<li><strong>No lettering or seals</strong>, which are illegible at a distance and reversed on the back.</li>
<li><strong>Be distinctive, or deliberately related</strong> to a flag you share history with.</li>
</ul>

<h3>The ones that break the rules</h3>
<ul>
<li><strong>Nepal</strong> is the only non-rectangular national flag, two stacked pennants.</li>
<li><strong>Switzerland and Vatican City</strong> are the only two squares.</li>
<li><strong>Paraguay</strong> has different designs on each side.</li>
<li><strong>Mozambique</strong> carries an AK-47, the only modern firearm on a national flag.</li>
<li><strong>Belize</strong> has fifty-odd colours and two human figures, making it the most complex of all.</li>
</ul>
"""),

    # ==================================================================
    _a('why-honey-never-goes-off', 'Why Honey Never Goes Off',
       FACT,
       'Edible honey has been found in 3,000-year-old Egyptian tombs. Three properties keep it safe almost indefinitely, and one of them explains why it must never be given to a baby.',
       '/static/img/articles/honey.jpg',
       """
<p>Honey is the only common food that does not spoil. Sealed jars recovered from Egyptian tombs, thousands of years old, have been found still edible. Three things are doing the work.</p>

<h3>1. There is almost no water in it</h3>
<p>Honey is typically 17 to 18% water, and bacteria and moulds need far more than that to live. More importantly, honey is a supersaturated sugar solution — so much sugar dissolved in so little water that it is desperate to absorb more. It is strongly <strong>hygroscopic</strong>: it pulls water out of anything it touches, including any microbe that lands in it, drying the cell out through osmosis before it can multiply.</p>

<h3>2. It is acidic</h3>
<p>Honey sits at a pH of about 3.9, roughly as acidic as orange juice, which is hostile to most spoilage organisms.</p>

<h3>3. The bees add hydrogen peroxide</h3>
<p>This is the clever part. Bees secrete an enzyme called glucose oxidase into the nectar. When honey is diluted, that enzyme breaks glucose down into gluconic acid and <strong>hydrogen peroxide</strong> — an antiseptic. Concentrated honey produces very little, but the moment it is diluted, as it would be by any moisture that got in, peroxide production starts up and kills what arrived with the water.</p>

<h3>Why bees make it so dry</h3>
<p>None of this is for our benefit. Nectar is about 70 to 80% water when collected. Bees reduce it by passing it between themselves, exposing it to air in the comb and fanning their wings to evaporate the rest. They are making a food store that will survive a winter without refrigeration. The side effect is a substance that outlasts civilisations.</p>

<h3>The conditions that break it</h3>
<p>Honey keeps indefinitely only if kept <strong>sealed and dry</strong>. Left open, it absorbs atmospheric moisture, the sugar concentration falls, and it can ferment — which is how mead is made deliberately. A wet spoon in the jar is the usual culprit.</p>

<h3>Crystallised is not spoiled</h3>
<p>Honey turning grainy and pale is normal. The glucose is simply coming out of solution, and it happens faster in cooler conditions and with some floral sources than others. Standing the jar in warm water dissolves it again. Raw honey crystallises sooner because pollen grains give the crystals something to form on.</p>

<h3>The exception: never give honey to a baby</h3>
<p>Honey can contain dormant spores of <em>Clostridium botulinum</em>. They are harmless to anyone with a developed gut, because established gut bacteria out-compete them. In an infant under twelve months the gut flora is not yet established, the spores can germinate, and the result is infant botulism, which is serious. Honey’s own defences stop the bacteria growing <em>in the jar</em>, but they do not destroy the spores.</p>

<h3>Worth knowing</h3>
<ul>
<li><strong>Honey has been used on wounds for millennia</strong>, and medical-grade honey is used in modern wound care — the peroxide and the water-drawing effect together.</li>
<li><strong>A worker bee makes about a twelfth of a teaspoon</strong> of honey in her entire life.</li>
<li><strong>Manuka honey</strong> has additional antibacterial activity from methylglyoxal, which does not depend on the peroxide mechanism.</li>
</ul>
"""),

    # ==================================================================
    _a('how-to-win-a-pub-quiz', 'How to Win a Pub Quiz',
       CRAFT,
       'Team size, who to bring, how to handle the ones nobody knows, and the two rounds that decide most quizzes. Practical tactics rather than "know more things".',
       '/static/img/articles/pub.jpg',
       """
<p>Most teams lose pub quizzes on process, not knowledge. These are the things that actually move the score.</p>

<h3>Build the team for coverage, not cleverness</h3>
<p>Four to six is the sweet spot. Below four you have gaps; above six the discussion gets slower than the quiz. One very well-read person is worth less than four people with genuinely different lives — someone who watches sport, someone who watches television, someone older than the rest of you, someone who listens to chart music.</p>
<p>The single most useful team member is usually the one who is thirty years older or younger than everyone else.</p>

<h3>Write the answer down last</h3>
<p>Appoint one person to hold the pen for the whole quiz, and let them be the one who decides when to commit. Teams lose points by writing an early confident answer and never revisiting it. Leave blanks and come back; the answer often arrives while you are arguing about question seven.</p>

<h3>Know how to argue</h3>
<p>The commonest failure in a pub quiz team is the loudest person winning. A useful habit: before settling, ask everyone to say how sure they are out of ten. Someone quietly on eight should beat someone confidently on five, and this makes that visible without anyone having to fight for it.</p>
<p>Equally, if nobody is above a four, stop. Write the most plausible answer quickly and spend the time on a question you can actually get.</p>

<h3>Guess properly</h3>
<ul>
<li><strong>Never leave a blank.</strong> There is no negative marking in a pub quiz.</li>
<li><strong>For a year, guess a round number in the right era.</strong> You often get a point for being within a range.</li>
<li><strong>For "which country", the answer is usually not the obvious one</strong> — a setter asking about the world’s largest producer of something rarely means the country you first think of.</li>
<li><strong>For a person, go for the most famous candidate that fits.</strong> Setters write for a pub, not a seminar.</li>
<li><strong>If the question names an unusual detail, it is doing work.</strong> "Which Scottish-born engineer" is narrowing it for a reason.</li>
</ul>

<h3>The rounds that decide it</h3>
<p><strong>The picture round.</strong> Usually handed out early to work on throughout the night. Teams that leave it until last get fewer of them. Give it to one person immediately and let them chip away while the others handle the spoken rounds.</p>
<p><strong>The music round.</strong> Intros are recognised almost instantly or not at all. If nobody has it in five seconds, nobody is going to have it in thirty. Move on and come back.</p>
<p><strong>The wipeout or jackpot round.</strong> Where most quizzes are genuinely won and lost. If the format lets you wager, wager on the category your weakest-covered member is strongest in, not the one the team feels best about collectively.</p>

<h3>Things that are worth more than they look</h3>
<ul>
<li><strong>Read the question sheet ahead</strong> if you have one. Half the team can work on later questions.</li>
<li><strong>Write legibly.</strong> Points are genuinely lost to handwriting at marking time.</li>
<li><strong>Hand in on time.</strong> Also genuinely lost.</li>
<li><strong>Check the spelling of names</strong> if the quizmaster has said spelling counts. Most say it does not, some mean it.</li>
</ul>

<h3>And the etiquette</h3>
<p>No phones. It is obvious from the answers, it is obvious from your face, and the quizmaster has seen it a hundred times. Winning a meat raffle by cheating is a poor way to spend an evening.</p>
"""),

    # ==================================================================
    _a('how-to-solve-a-cryptic-crossword-clue', 'How to Solve a Cryptic Crossword Clue',
       CRAFT,
       'Every cryptic clue contains a definition and a piece of wordplay. Learn the eight clue types and the standard indicator words, and the whole thing opens up.',
       '/static/img/articles/cryptic.svg',
       """
<p>Cryptic crosswords look impenetrable and are not. They follow strict rules, and once you know them you are no longer guessing.</p>

<h3>The one rule everything rests on</h3>
<p><strong>Every cryptic clue gives you the answer twice.</strong> Once as a straight definition, once as wordplay. The definition is almost always at the very start or the very end of the clue, never in the middle.</p>
<p>So the first move on any clue is to find where it splits. Read the first word or two as a definition, then the last word or two, and see which feels like it could define a word.</p>

<h3>The eight clue types</h3>

<p><strong>1. Anagram.</strong> Signalled by a word suggesting disorder: <em>confused, broken, mixed, cooked, drunk, out, badly, strangely, arranged</em>.</p>
<p><em>Example:</em> "Cheater, oddly, is an instructor" (7). The definition is "instructor" at the end. "Oddly" signals an anagram, and the fodder is CHEATER, which rearranges to <strong>TEACHER</strong>. Both halves land: TEACHER is an instructor, and its letters are those of "cheater".</p>

<p><strong>2. Hidden word.</strong> The answer sits inside the clue, spanning words. Signalled by <em>in, some, part of, held by, within</em>.</p>
<p><em>Example:</em> "Beginning found in lemon sets" (5). "Found in" signals a hidden word and "beginning" is the definition. Read straight across the letters: lem<strong>ON SET</strong>s gives <strong>ONSET</strong>.</p>

<p><strong>3. Reversal.</strong> The answer is another word backwards. Signalled by <em>back, returning, up (in a down clue), reflected, going west</em>.</p>
<p><em>Example:</em> "Evil returning live" (4) &rarr; LIVE reversed is <strong>EVIL</strong>.</p>

<p><strong>4. Charade.</strong> The answer is built from pieces joined in order, like charades.</p>
<p><em>Example:</em> "Vehicle animal provides floor covering" (6). Take the pieces in order: vehicle gives CAR, animal gives PET, and together they make <strong>CARPET</strong>, which is the floor covering.</p>

<p><strong>5. Container.</strong> One word goes inside another. Signalled by <em>in, around, holding, swallowing, eating, outside</em>.</p>

<p><strong>6. Deletion.</strong> Remove a letter. Signalled by <em>heartless</em> (lose the middle), <em>endless / unfinished</em> (lose the last), <em>beheaded</em> (lose the first).</p>

<p><strong>7. Homophone.</strong> Sounds like another word. Signalled by <em>we hear, reportedly, on the radio, said, aloud</em>.</p>

<p><strong>8. Double definition.</strong> Two meanings side by side, no wordplay at all. Usually a short clue of two or three words.</p>
<p><em>Example:</em> "Left port" (4) &rarr; <strong>LEFT</strong> and port both mean the same side of a ship.</p>

<h3>The abbreviations setters assume you know</h3>
<table>
<tr><th>Clue says</th><th>You write</th></tr>
<tr><td>Learner, student</td><td>L</td></tr>
<tr><td>Doctor</td><td>MD, DR, MO</td></tr>
<tr><td>Queen</td><td>ER, R</td></tr>
<tr><td>King</td><td>K, R</td></tr>
<tr><td>Gold</td><td>OR, AU</td></tr>
<tr><td>Silver</td><td>AG</td></tr>
<tr><td>Iron</td><td>FE</td></tr>
<tr><td>Fifty / hundred / thousand</td><td>L / C / M</td></tr>
<tr><td>Note</td><td>A–G, DO, RE, MI, TE</td></tr>
<tr><td>Sailor</td><td>AB, TAR, SALT</td></tr>
<tr><td>Point</td><td>N, S, E, W</td></tr>
<tr><td>About</td><td>RE, CA, C</td></tr>
<tr><td>Very</td><td>SO (in music, F for forte)</td></tr>
<tr><td>River</td><td>R, or EXE, PO, DEE</td></tr>
</table>

<h3>How to work a clue</h3>
<ol>
<li><strong>Count the letters</strong> and write the enumeration down.</li>
<li><strong>Find the definition</strong> at one end.</li>
<li><strong>Look for an indicator word</strong> in the rest — it tells you which of the eight types you are in.</li>
<li><strong>Solve the wordplay</strong> and check it against the definition.</li>
<li><strong>Confirm both halves work.</strong> If only one does, you have the wrong answer.</li>
</ol>
<p>That last step is the one that separates solving from guessing. A cryptic answer is right when <em>both</em> readings land. If you cannot explain why your answer works, it is probably not the answer.</p>
"""),

    # ==================================================================
    _a('how-to-write-a-quiz-round-worth-playing', 'How to Write a Quiz Round Worth Playing',
       CRAFT,
       'The difference between a good question and a hard one. Pitching difficulty, ordering a round, writing plausible wrong answers, and the mistakes that lose a room.',
       '/static/img/articles/quiz-craft.svg',
       """
<p>Writing quiz questions is harder than it looks, and the common failure is not that questions are too easy or too hard. It is that they are not enjoyable to be asked.</p>

<h3>A good question is one people enjoy getting wrong</h3>
<p>That is the whole craft in a sentence. The best questions produce a groan and a "of course" when the answer comes, not a shrug. Aim for things people half know, where the answer is retrievable with effort.</p>
<p>A question nobody can get teaches nothing and flattens the room. A question everybody gets is a formality. The sweet spot is roughly <strong>60 to 70% of the room getting it</strong>, with the rest kicking themselves.</p>

<h3>Pitch it at what people have been exposed to</h3>
<p>Not what they have studied. Most people have absorbed an enormous amount of information passively and have no idea they know it. The skill is finding the questions that unlock it.</p>
<p>"What is the capital of Burkina Faso?" tests whether somebody has memorised a list. "Which country's flag is the only one that is not rectangular?" tests whether somebody has ever looked properly at a flag. The second is a far better question and is not easier.</p>

<h3>Order the round properly</h3>
<p>Start easy. The first question sets the room's confidence for the whole round, and a team that gets question one wrong spends question two still arguing about it.</p>
<p>A reliable eight-question shape:</p>
<ol>
<li>Easy, to settle everyone.</li>
<li>Easy.</li>
<li>Medium.</li>
<li>Medium.</li>
<li>The hard one, placed where the room is warmed up but not tired.</li>
<li>Medium, to recover.</li>
<li>Something funny or surprising.</li>
<li>Medium-hard, so the round ends on a real contest.</li>
</ol>

<h3>Writing the wrong answers</h3>
<p>For multiple choice, the wrong options are where the quality lives. Three rules:</p>
<ul>
<li><strong>Every option must be plausible.</strong> If one is obviously silly you have turned a four-way question into a three-way one.</li>
<li><strong>Keep them the same kind of thing.</strong> Four countries, four years, four people. Mixing categories gives the answer away.</li>
<li><strong>Keep them the same length.</strong> Players unconsciously pick the longest, most detailed option, because question writers unconsciously write it.</li>
</ul>
<p>The strongest wrong answer is the one most people would give if you asked the question open — the common misconception. "Which planet is hottest?" is a good question precisely because Mercury is a tempting wrong answer.</p>

<h3>Write the explanation, not just the answer</h3>
<p>The ten seconds after the answer is read out is when people actually learn something, and it is the part most quizzes waste. "Venus, because a runaway greenhouse effect traps the heat, which is why it is hotter than Mercury" is worth four times "Venus".</p>

<h3>The mistakes that lose a room</h3>
<ul>
<li><strong>Ambiguity.</strong> If two answers are defensible, you will spend five minutes arguing and someone will leave annoyed. Test every question on someone who was not in the room when you wrote it.</li>
<li><strong>Questions that are really about one hobby.</strong> A round of Premier League squad numbers is a specialist exam wearing a quiz costume.</li>
<li><strong>Too many dates.</strong> One year question per round. They are memory tests, not thinking.</li>
<li><strong>Burying the question.</strong> Put the thing being asked at the end, after the context, so people know what they are listening for.</li>
<li><strong>Not checking.</strong> Facts drift. Record-holders change, countries rename, "largest" and "first" claims get overtaken. Check anything superlative before you use it.</li>
</ul>
"""),

    # ==================================================================
    _a('memory-tricks-that-work-for-trivia', 'Memory Tricks That Actually Work for Trivia',
       CRAFT,
       'The memory palace, chunking, spacing and why you forget names. Techniques with real evidence behind them, and how to use them on things quizzes ask about.',
       '/static/img/articles/chess.jpg',
       """
<p>Competitive memory athletes are not born with unusual brains. Studies scanning them have found ordinary memory hardware running better techniques. Here are the ones worth the effort.</p>

<h3>1. The memory palace</h3>
<p>The oldest technique there is, attributed to the Greek poet Simonides. Picture a place you know intimately — your home, your walk to work — and place each thing you want to remember at a specific spot along a fixed route.</p>
<p>To remember the planets in order, put the Sun on your doorstep, Mercury on the hall table, Venus on the stairs, and so on. To recall them, walk the route.</p>
<p>It works because spatial memory is extraordinarily strong and almost effortless, while abstract lists are neither. You are smuggling the list into a system built for places.</p>
<p><strong>Make the images absurd.</strong> A vivid, strange, moving image sticks far better than a sensible one. Saturn as a giant onion ring wedged in your bathroom door will outlast any amount of staring at a list.</p>

<h3>2. Chunking</h3>
<p>Working memory holds roughly four to seven items. But an item can be any size. "BBCITVCNNFBI" is twelve letters and nearly impossible; "BBC ITV CNN FBI" is four chunks and trivial.</p>
<p>This is why phone numbers are grouped, and why chess masters can reproduce a board after a glance — they are not seeing twenty pieces but five familiar formations. The same works for dates, lists and sequences: find the groups.</p>

<h3>3. Spacing, not cramming</h3>
<p>The most robustly supported finding in the whole field. Reviewing material at increasing intervals — a day, three days, a week, a month — produces far more durable memory than the same total time spent in one session.</p>
<p>Cramming works for tomorrow and is nearly useless for next month. If you want a question bank in your head for a quiz league that runs all season, ten minutes a week beats two hours the night before.</p>

<h3>4. Testing yourself, not rereading</h3>
<p>Rereading notes feels productive and mostly is not. The act of <em>retrieving</em> something strengthens the memory far more than seeing it again. Cover the answers and try to produce them. Getting it wrong and then seeing the answer is better for retention than never having struggled.</p>

<h3>Why you forget names</h3>
<p>Names are uniquely hard, and it is not your fault. A name is arbitrary — nothing about a person's face tells you they are called Graham, whereas "baker" would at least connect to something. Arbitrary labels have nothing to hook onto.</p>
<p>What helps:</p>
<ul>
<li><strong>Say it back immediately.</strong> "Nice to meet you, Graham."</li>
<li><strong>Attach it to an image.</strong> Graham → a cracker, placed on his forehead. Ridiculous, and it works.</li>
<li><strong>Use it once more within a minute</strong>, then again before you leave.</li>
</ul>

<h3>Applying it to quiz material</h3>
<ul>
<li><strong>Ordered lists</strong> — planets, monarchs, elements, Oscar winners — go in a memory palace.</li>
<li><strong>Pairs</strong> — capitals and countries, gods and their Roman names — go in a linked image. Picture a bear drinking beer in Bern.</li>
<li><strong>Numbers</strong> — convert to something concrete. 1066 is easier as an image of an arrow than as four digits.</li>
<li><strong>Anything you keep getting wrong</strong> — this is the material worth spacing. The questions you already know need no revision at all.</li>
</ul>

<h3>What does not work</h3>
<p>Listening to recordings while asleep does nothing. "Brain training" games mostly make you better at those games. And there is no evidence for learning styles — being a "visual learner" is not a real category, though visual imagery helps everybody.</p>
"""),

    # ==================================================================
    _a('a-short-history-of-the-quiz-show', 'A Short History of the Quiz Show',
       CRAFT,
       'From 1930s radio to the scandal that nearly killed the format, through Mastermind and Millionaire to the streaming era. How the quiz show became what it is.',
       '/static/img/articles/quiz-show.jpg',
       """
<p>The quiz show is nearly a century old, and its shape has been set as much by scandal and regulation as by entertainment.</p>

<h3>Radio, 1930s</h3>
<p>The format began on American radio. <em>Professor Quiz</em> in 1936 is usually credited as the first, with listeners sending in questions. <em>Information Please</em> turned the idea round: a panel of experts tried to answer questions from the audience, and listeners won money when they stumped them. The BBC’s <em>Round Britain Quiz</em> started in 1947 and is still running, making it the oldest surviving quiz programme anywhere.</p>

<h3>Television and the big money, 1950s</h3>
<p>Television raised the stakes literally. <em>The $64,000 Question</em> launched in 1955 and was a sensation — contestants in isolation booths, enormous prizes, weeks of build-up around a single person.</p>

<h3>The scandal that changed everything</h3>
<p>It was rigged. In 1958 it emerged that producers of <em>Twenty-One</em> had been feeding answers to telegenic contestants and instructing others to lose. Charles Van Doren, a Columbia academic who had become a national figure during a long winning run, eventually admitted to Congress that his entire run was scripted.</p>
<p>The fallout was severe. Big-money quizzes vanished from American television almost completely, and US law was changed to make rigging a contest a federal offence. The format only recovered by becoming modest: daytime shows with small prizes and visible fairness.</p>

<h3>Britain goes the other way</h3>
<p>British television never had the same crisis, partly because strict rules capped prize values for decades. That pushed the BBC and ITV towards difficulty and format invention rather than money.</p>
<ul>
<li><strong>University Challenge</strong> (1962), adapted from America’s <em>College Bowl</em>, and still built on speed and genuine academic range.</li>
<li><strong>Mastermind</strong> (1972), devised by Bill Wright, a former RAF gunner who had been interrogated by the Gestapo — which is where the black chair, the spotlight and the relentless questioning came from.</li>
<li><strong>Blockbusters</strong>, <strong>Fifteen to One</strong>, <strong>Countdown</strong>: formats built on structure rather than jackpots.</li>
</ul>

<h3>Millionaire changes the world, 1998</h3>
<p><em>Who Wants to Be a Millionaire?</em> was devised in Britain and became the most successfully exported television format in history, licensed to well over a hundred countries. Its innovations — the lifelines, the money ladder, the lighting dropping as the stakes rose, the long pause before "final answer" — are now standard everywhere.</p>
<p>It also produced the format’s most famous modern scandal, the 2001 coughing conviction, later re-examined and dramatised.</p>

<h3>The quizzer as character</h3>
<p>The 2000s moved the expert from contestant to opponent. <em>The Chase</em>, <em>Eggheads</em> and <em>The Weakest Link</em> made the professional quizzer a recurring personality, which solved an old problem: you can keep a brilliant player on screen indefinitely if they are not the one winning the money.</p>

<h3>And now</h3>
<p>The format has survived streaming better than most, because it is cheap to make, endlessly repeatable and works as background viewing. The genuine change is that quizzes are now mostly played rather than watched — on phones, in apps, asynchronously against friends. The pub quiz, which long predates all of this, carries on largely unchanged.</p>

<h3>Quiz show facts worth knowing</h3>
<ul>
<li><strong>The Mastermind chair</strong> is an original prop and has its own travel case.</li>
<li><strong>Jeopardy!</strong> answers in the form of a question partly as a legacy of the rigging scandal — giving contestants the answer was a way of signalling fairness.</li>
<li><strong>Countdown</strong> was the first programme broadcast on Channel 4, in November 1982.</li>
<li><strong>University Challenge</strong> was off air from 1987 to 1994, and Bamber Gascoigne presented the first run, Jeremy Paxman the second.</li>
</ul>
"""),

    # ==================================================================
    _a('tricks-crossword-setters-reuse', 'The Tricks Crossword Setters Use Again and Again',
       CRAFT,
       'Setters have a standard toolkit, and most of it repeats. The vocabulary they rely on, the misdirections they love, and the words that exist mainly to fit a grid.',
       '/static/img/articles/setter-tricks.svg',
       """
<p>Crossword setters are not trying to beat you. They are trying to beat you <em>fairly</em>, which means working within conventions you are expected to learn. Once you know the toolkit, half the fight is over.</p>

<h3>Crosswordese: words that live mostly in grids</h3>
<p>Short words with awkward vowel patterns are gold to a setter and rare in ordinary life. You will meet these constantly:</p>
<table>
<tr><th>Word</th><th>Means</th></tr>
<tr><td>ERNE</td><td>Sea eagle</td></tr>
<tr><td>ADIT</td><td>Mine entrance</td></tr>
<tr><td>ETUI</td><td>Small needle case</td></tr>
<tr><td>OAST</td><td>Hop-drying kiln</td></tr>
<tr><td>ESNE</td><td>Anglo-Saxon labourer</td></tr>
<tr><td>ANIL</td><td>Indigo plant</td></tr>
<tr><td>EWER</td><td>Water jug</td></tr>
<tr><td>ORLE</td><td>Heraldic border</td></tr>
<tr><td>ALEE</td><td>Away from the wind</td></tr>
<tr><td>EPEE</td><td>Fencing sword</td></tr>
<tr><td>OLEO</td><td>Margarine</td></tr>
<tr><td>ASEA</td><td>At sea</td></tr>
</table>

<h3>The misdirections</h3>
<p><strong>Capital letters that mean nothing.</strong> A clue starts with a capital because clues do, so "Bill" might be a duck’s beak, an invoice or a poster, not a man.</p>
<p><strong>Words with two jobs.</strong> "Flower" is very often something that flows — a river. "Number" can mean something that numbs. "Second" can be a unit of time, a supporter, or the letter after the first.</p>
<p><strong>Proper nouns hiding in plain sight.</strong> "Rose" as a past tense. "Reading" as a town. "Polish" as a nationality or a verb, depending on the capital letter you are not allowed to rely on.</p>
<p><strong>Plural traps.</strong> A clue ending in S is not necessarily a plural — it might be the last letter of a charade.</p>

<h3>Indicator words to recognise instantly</h3>
<table>
<tr><th>Device</th><th>Typical signals</th></tr>
<tr><td>Anagram</td><td>confused, broken, cooked, drunk, strange, wild, out, poorly, novel, arranged</td></tr>
<tr><td>Reversal</td><td>back, up, returning, retreating, reflected, recalled</td></tr>
<tr><td>Hidden</td><td>in, some, part of, held by, a bit of, within</td></tr>
<tr><td>Homophone</td><td>we hear, said, reportedly, on the radio, aloud, spoken</td></tr>
<tr><td>Container</td><td>in, around, holding, eating, outside, embracing</td></tr>
<tr><td>Deletion</td><td>heartless, endless, beheaded, curtailed, topless</td></tr>
<tr><td>First letters</td><td>initially, firstly, leaders, at the start, heads of</td></tr>
<tr><td>Last letters</td><td>finally, ends, tails, at last</td></tr>
</table>

<h3>The ones that catch everyone</h3>
<ul>
<li><strong>"Perhaps" or "say" or "for example"</strong> means the definition is a category, not the exact thing. "Dog, say" could clue SPANIEL or PET.</li>
<li><strong>"Nothing" is O.</strong> "Love" in a tennis sense is also O.</li>
<li><strong>"One" is I or A or AN.</strong></li>
<li><strong>"The French" is LE, LA or LES.</strong> "The German" is DER, DIE or DAS. Setters love this.</li>
<li><strong>"Boxer" might be Ali</strong>, and a great many short clues are really asking for a famous three-letter surname.</li>
<li><strong>A question mark at the end</strong> is a warning: the clue is doing something cheeky, usually a pun or a definition that is stretched.</li>
</ul>

<h3>Why the same answers recur</h3>
<p>A setter filling a grid needs words that interlock. Letters like E, A, R, S and T appear constantly because they are common in English, so answers rich in them fit more easily. That is why you meet ERNE and ETUI far more often in crosswords than in life, and why the same handful of rivers, Greek gods, musical notes and chemical symbols turn up week after week.</p>
<p>Which means learning them pays compound interest. The crosswordese above, plus the abbreviations setters assume, will unlock more clues than any amount of general knowledge.</p>
"""),

]
