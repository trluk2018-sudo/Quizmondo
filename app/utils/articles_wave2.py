# -*- coding: utf-8 -*-
"""Thirty additional easy-to-read fact articles covering tech, news, music,
nature, food and everyday curiosities.

Follows the exact same contract as ``articles`` and ``articles_facts``:
matched on slug by ``quiz_seed._sync_articles``, using the existing site
categories so the blog stays cohesive, with a 50/50 mix of bespoke drawn
SVGs and free-licence photographs.
"""

ARTICLE_CATEGORIES_WAVE2 = [
    ('Facts & Curiosities', 'facts-and-curiosities'),
    ('Strange But True', 'strange-but-true'),
    ('Quiz Reference', 'quiz-reference'),
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


FACT = 'Facts & Curiosities'
STRANGE = 'Strange But True'
REF = 'Quiz Reference'


ARTICLES_WAVE2 = [

    # 1. TECH — Drawn SVG
    _a('how-the-internet-actually-crosses-the-ocean',
       'How the Internet Actually Crosses the Ocean',
       FACT,
       'Almost none of your messages go via satellite. Over 99% of intercontinental data travels through garden-hose-thick fibre cables lying on the seabed.',
       '/static/img/articles/subsea-cables.svg',
       """
<p>When you stream a film or load a website hosted on another continent, it is easy to picture the signal bouncing off a satellite. In reality, satellites carry less than one per cent of international internet traffic. Nearly all of it travels along the bottom of the ocean.</p>

<h3>Thinner than you expect</h3>
<p>Out in the deep ocean, far from fishing trawlers and anchors, a subsea internet cable is only about the thickness of a garden hose. Inside sit hair-thin strands of glass fibre carrying pulses of laser light, wrapped in copper, plastic and steel wire. Near the shore, where boats are a hazard, the cables are armoured and buried beneath the seabed.</p>

<h3>1.4 million kilometres of glass</h3>
<p>More than 500 active submarine cable systems now wrap the globe, stretching roughly 1.4 million kilometres — more than three times the distance to the Moon. Some of the deepest lie eight kilometres down in the Japan Trench, where the water pressure would crush a submarine.</p>

<h3>What actually breaks them</h3>
<ul>
<li><strong>Ships’ anchors and fishing nets</strong> cause roughly two-thirds of all cable faults.</li>
<li><strong>Underwater landslides and earthquakes</strong> can snap several cables at once, as happened off Taiwan in 2006.</li>
<li><strong>Sharks</strong> occasionally bite cables — Google famously wrapped parts of its Pacific lines in Kevlar-like material after footage showed sharks testing the electric field.</li>
</ul>

<h3>How a cable gets mended</h3>
<p>Specialist repair ships stay on permanent standby around the world. When a line breaks, engineers fire a light pulse down the fibre and time the reflection to pinpoint the fault to within a few hundred metres. A grappling hook hauls both ends to the deck, technicians splice the glass fibres inside a clean room, and the repaired loop is lowered back to the floor.</p>
"""),

    # 2. TECH — Drawn SVG
    _a('why-ai-models-still-get-simple-things-wrong',
       'Why AI Can Write Code in Seconds Yet Still Miscounts the Letters in Strawberry',
       FACT,
       'Large language models do not read letter by letter the way humans do. They read in chunks called tokens — which explains both their brilliance and their blind spots.',
       '/static/img/articles/ai-tokens.svg',
       """
<p>One of the oddest quirks of modern AI is how lopsided it can be. The same system that can summarise a legal contract or debug a programme in three seconds has famously stumbled when asked how many Rs are in the word <em>strawberry</em>.</p>

<h3>They do not see letters</h3>
<p>Before a language model ever sees your prompt, a small piece of software called a <strong>tokeniser</strong> chops the text into numbered chunks. Common words like <em>apple</em> or <em>London</em> become a single number. Longer or rarer words get split into two or three pieces — <em>strawberry</em>, for instance, is often sliced into <strong>str</strong>, <strong>aw</strong> and <strong>berry</strong>.</p>
<p>To the model, those pieces are just ID numbers in a giant dictionary. It knows what <em>strawberry</em> means, what it rhymes with and what jam is made from, without automatically seeing the individual letters inside the box.</p>

<h3>Why maths and reversals trip them up too</h3>
<ul>
<li><strong>Counting characters</strong> requires unpacking each token back into letters, which is an extra step unless the model pauses to spell the word out.</li>
<li><strong>Spelling backwards</strong> fails for the same reason: the model predicts the next likely token, not the reverse of a string of symbols.</li>
<li><strong>Large multiplication</strong> is hard to do in one breath, which is why newer reasoning models write out scratchpad steps or hand arithmetic to a built-in calculator.</li>
</ul>

<h3>What changed recently</h3>
<p>Modern "reasoning" models now spend a few seconds talking to themselves before answering, spelling words out letter by letter or running quick code behind the scenes. The underlying blind spot is still there — it is just wearing glasses now.</p>
"""),

    # 3. NEWS & TECH — Photo
    _a('the-worlds-smallest-and-strangest-satellites',
       'Space Junk, Shoebox Satellites and What Is Actually Orbiting Above Your Head',
       FACT,
       'More than ten thousand active satellites circle the Earth today, alongside shoebox-sized CubeSats, lost tools and flecks of paint moving faster than a rifle bullet.',
       '/static/img/articles/satellites-orbit.jpg',
       """
<p>Look up at a clear night sky away from city lights and wait five minutes. Almost certainly you will spot a steady white dot gliding smoothly across the stars. That is a satellite — and low Earth orbit has never been busier.</p>

<h3>From car-sized to shoebox-sized</h3>
<p>For decades, launching a satellite meant spending hundreds of millions on something the size of a minibus. Today, universities and small companies routinely launch <strong>CubeSats</strong>: modular cubes measuring just ten centimetres on each side. Dozens can ride piggyback on a single rocket, monitoring crops, tracking ships or testing new radio links.</p>

<h3>What else is up there</h3>
<table>
<tr><th>Object</th><th>Approximate count</th></tr>
<tr><td>Active satellites</td><td>10,000+</td></tr>
<tr><td>Defunct satellites &amp; spent rocket stages</td><td>~5,000+</td></tr>
<tr><td>Tracked debris larger than 10 cm</td><td>35,000+</td></tr>
<tr><td>Fragments between 1 cm and 10 cm</td><td>~1,000,000</td></tr>
</table>

<h3>Why a fleck of paint matters</h3>
<p>In low Earth orbit, objects travel at roughly <strong>28,000 kilometres per hour</strong> — about ten times the speed of a rifle bullet. At that velocity, a stray bolt or even a chip of dried paint carries enough kinetic energy to crack a spacecraft window or puncture a solar panel. The International Space Station has had to fire its thrusters dozens of times simply to dodge passing junk.</p>

<h3>How orbits get cleaned up</h3>
<p>New rules require low-orbit satellites to burn up in the atmosphere within five years of retirement rather than drifting for decades. Higher up, where air drag is negligible, dead satellites are nudged outwards into a "graveyard orbit" where they stay out of the way.</p>
"""),

    # 4. TECH & HISTORY — Drawn SVG
    _a('inventions-that-started-as-accidents',
       'Ten Everyday Inventions That Started as Complete Accidents',
       STRANGE,
       'From the melted chocolate bar that gave us the microwave to the failed glue behind Post-it notes — ten familiar objects nobody meant to invent.',
       '/static/img/articles/accidental-inventions.svg',
       """
<p>A surprising slice of modern life exists because an experiment went wrong, somebody forgot to wash up, or a walk in the woods got annoying.</p>

<h3>1. The microwave oven</h3>
<p>In 1945, engineer Percy Spencer was standing beside an active radar magnetron when he noticed the peanut cluster bar in his pocket had melted. He fetched popcorn kernels, then an egg (which exploded in a colleague’s face), and filed the patent shortly after.</p>

<h3>2. Penicillin</h3>
<p>Alexander Fleming returned from a 1928 holiday to find a stray mould growing in an unwashed dish of bacteria — with a clear, bacteria-free ring around it. That mould became the world’s first true antibiotic.</p>

<h3>3. Post-it notes</h3>
<p>In 1968, 3M chemist Spencer Silver tried to invent a super-strong aerospace adhesive and accidentally made a weak one that peeled off cleanly. Six years later, a colleague tired of bookmarks falling out of his choir hymnal realised what it was good for.</p>

<h3>4. Velcro</h3>
<p>Swiss engineer George de Mestral came home from a 1941 hunting trip covered in burdock burrs. Under a microscope he saw hundreds of tiny hooks catching on the loops in his trousers and his dog’s fur.</p>

<h3>5. Safety glass</h3>
<p>French chemist Édouard Bénédictus dropped a glass flask in 1903 and was startled to see it crack without shattering. It had held a plastic film called cellulose nitrate that dried into an invisible skin inside.</p>

<h3>6. Super Glue</h3>
<p>Harry Coover rejected cyanoacrylate in 1942 because it stuck to everything it touched and ruined his optical lenses. Nine years later he realised that sticking to everything instantly was a selling point.</p>

<h3>7. Pacemakers</h3>
<p>Wilson Greatbatch reached into a box for the wrong resistor while building a heart-sound recorder in 1956. The circuit began pulsing rhythmically — matching the cadence of a human heartbeat.</p>

<h3>8. Teflon</h3>
<p>In 1938, Roy Plunkett opened a cylinder of refrigerant gas and found nothing came out, even though the cylinder felt heavy. Sawing it open revealed a white, waxy, impossibly slippery powder.</p>

<h3>9. Slinky</h3>
<p>Naval engineer Richard James was working on tension springs to steady ship instruments in 1943 when one fell off a shelf and "walked" across the floor.</p>

<h3>10. X-rays</h3>
<p>Wilhelm Röntgen was testing cathode-ray tubes in a darkened room in 1895 when a chemically coated screen across the bench began to glow. He held his wife’s hand in front of it and saw the bones and her wedding ring.</p>
"""),

    # 5. TECH — Drawn SVG
    _a('why-batteries-still-die-in-the-cold',
       'Why Your Phone Battery Dies in the Cold (and How Solid-State Cells Aim to Fix It)',
       FACT,
       'Your battery is not actually empty when your phone shuts off in winter — the chemistry inside has simply slowed down. Here is what is going on inside the case.',
       '/static/img/articles/cold-batteries.svg',
       """
<p>Step outside on a freezing morning with 40% battery and watch your phone suddenly announce 1% and switch off. Walk back indoors, let it warm up for ten minutes, and half the charge miraculously returns. You did not lose the electricity — you lost the speed of the chemistry.</p>

<h3>Cold treacle inside the cell</h3>
<p>A lithium-ion battery works by shuttling charged lithium ions back and forth through a liquid electrolyte between two electrodes. Like honey in a fridge, that liquid thickens as the temperature drops. The ions struggle to move, internal resistance spikes, and the voltage dips below the minimum your phone needs to stay awake.</p>
<p>Rather than risk crashing mid-operation, the phone’s power chip plays safe and shuts the device down.</p>

<h3>Why electric cars preheat their batteries</h3>
<p>Electric vehicles use the exact same chemistry on a much larger scale, which is why winter range drops by 15% to 30%. Modern EVs actively warm their battery packs before you arrive at a fast charger — because forcing rapid current into a freezing lithium-ion cell can permanently plate metallic lithium onto the anode.</p>

<h3>What solid-state batteries promise</h3>
<ul>
<li><strong>No liquid electrolyte:</strong> Replacing the flammable liquid with a solid ceramic or polymer layer cuts fire risk dramatically.</li>
<li><strong>Higher energy density:</strong> Packing more charge into the same weight could push car ranges past 600 miles.</li>
<li><strong>Faster charging:</strong> Solid electrolytes handle higher currents with less degradation, though making them cheaply at factory scale remains the big engineering hurdle.</li>
</ul>
"""),

    # 6. TECH & SCIENCE — Drawn SVG
    _a('how-gps-needs-einstein-to-work',
       'Why Your Sat-Nav Would Be Wrong by Six Miles a Day Without Einstein',
       STRANGE,
       'Relativity sounds like pure chalkboard physics, yet the map app on your phone relies on both of Einstein’s theories every single second.',
       '/static/img/articles/gps-einstein.svg',
       """
<p>Albert Einstein’s theories of relativity are usually filed under "things that only matter near black holes". In truth, you use them every time you check when the next bus is coming or follow a sat-nav to a roundabout.</p>

<h3>GPS is really a clock system</h3>
<p>Each GPS satellite carries an atomic clock and constantly broadcasts the exact time and its position. Your phone catches signals from at least four satellites, compares how long each radio wave took to arrive, and works out where you are. Because radio waves travel at the speed of light, a timing error of just one millionth of a second puts you <strong>300 metres</strong> in the wrong place.</p>

<h3>Two opposite relativistic effects</h3>
<p>Up at 20,200 kilometres altitude, satellite clocks experience time differently from clocks on the ground for two competing reasons:</p>
<ul>
<li><strong>Special relativity (speed):</strong> The satellites race along at 14,000 km/h, which makes their clocks tick about <strong>7 microseconds slower</strong> per day than ours.</li>
<li><strong>General relativity (gravity):</strong> Earth’s gravity is weaker up there, which makes their clocks tick about <strong>45 microseconds faster</strong> per day.</li>
</ul>

<h3>The net drift</h3>
<p>Combine the two and satellite clocks run roughly <strong>38 microseconds fast</strong> every single day. Left uncorrected, that tiny fraction of a second would accumulate into a navigation error of roughly <strong>10 kilometres (over 6 miles) per day</strong>. Within a week your phone would place you in the wrong county.</p>
<p>Engineers build Einstein’s equations directly into the satellite hardware before launch, deliberately tuning their clocks slightly slow on Earth so they tick at the right pace in orbit.</p>
"""),

    # 7. TECH & HISTORY — Photo
    _a('the-first-things-ever-put-on-the-internet',
       'The First Things Ever Put on the Internet (Including a Coffee Pot)',
       STRANGE,
       'Before social media, streaming or online shopping, the early internet was built on a crashed word, a Cambridge coffee pot and a pizza order.',
       '/static/img/articles/early-internet.jpg',
       """
<p>The internet now carries the weight of global commerce, news and entertainment, so it is refreshing to look back at how wonderfully mundane its first milestones were.</p>

<h3>The first message: "LO"</h3>
<p>On 29 October 1969, UCLA student Charley Kline tried to send the word <em>LOGIN</em> over ARPANET to a computer at Stanford. He typed L, then O — and the remote system crashed. The very first message sent across the precursor to the internet was simply <strong>LO</strong>.</p>

<h3>The first webcam: a coffee pot</h3>
<p>In 1991, computer scientists at the University of Cambridge grew tired of walking down several flights of stairs to the Trojan Room only to find the coffee pot empty. They pointed a spare camera at the pot and streamed a grainy 128×128 greyscale snapshot onto their local network — and later onto the World Wide Web. Millions watched it before it was switched off in 2001, and the pot itself sold at auction for over £3,000.</p>

<h3>The first banner ad</h3>
<p>In October 1994, AT&amp;T placed a small rectangular graphic on <em>HotWired</em> asking: "Have you ever clicked your mouse right here? You will." Roughly <strong>44% of everyone who saw it clicked</strong> — a click-through rate modern advertisers can only dream about.</p>

<h3>The first online purchase</h3>
<p>Depending on how strictly you count encryption, the contenders are either a Pizza Hut pepperoni-and-mushroom pizza ordered in August 1994, or a Sting CD (<em>Ten Summoner’s Tales</em>) bought days earlier using the first encrypted credit-card transaction for $12.48 plus shipping.</p>

<h3>The first YouTube video</h3>
<p>Uploaded on 23 April 2005 by co-founder Jawed Karim, <em>Me at the zoo</em> lasts nineteen seconds and consists of Karim standing in front of elephants in San Diego noting that they have "really, really, really long trunks".</p>
"""),

    # 8. NEWS & SCIENCE — Photo
    _a('how-modern-weather-forecasts-actually-work',
       'How Weather Forecasting Went From Guesswork to Supercomputers',
       FACT,
       'A five-day forecast today is as accurate as a one-day forecast was in the 1980s. Here is how satellites, ocean buoys and AI models predict the sky.',
       '/static/img/articles/weather-supercomputer.jpg',
       """
<p>People love to complain about the weather forecast, yet meteorology is one of the quietest scientific triumphs of the last fifty years. A modern five-day forecast is roughly as reliable as a single-day forecast was in 1980.</p>

<h3>Measuring the whole planet at once</h3>
<p>Before a forecast can be calculated, agencies need a snapshot of the atmosphere right now. Every day, weather services gather hundreds of millions of readings from:</p>
<ul>
<li><strong>Weather satellites</strong> scanning cloud tops, humidity and sea temperatures from space.</li>
<li><strong>Commercial airliners</strong> automatically reporting wind speed and temperature as they climb and cruise.</li>
<li><strong>Weather balloons</strong> launched simultaneously twice a day from roughly 800 stations worldwide.</li>
<li><strong>Drifting ocean buoys</strong> measuring surface pressure in remote seas where ships rarely sail.</li>
</ul>

<h3>Chopping the sky into boxes</h3>
<p>Supercomputers divide the atmosphere into a vast three-dimensional grid of boxes and apply the laws of fluid physics to step each box forward in time — minute by minute, day by day. Because tiny measurement errors grow quickly (the famous "butterfly effect"), forecasters run the model dozens of times with slight tweaks. When 40 out of 50 runs show rain on Tuesday, you see an 80% chance of rain on your phone.</p>

<h3>The new AI wave</h3>
<p>In the last few years, machine-learning weather models trained on forty years of historical observations have begun matching — and occasionally beating — traditional physics supercomputers, while running in minutes on a single desktop chip rather than hours on a warehouse of servers.</p>
"""),

    # 9. MUSIC — Photo
    _a('why-vinyl-records-still-outsell-cds',
       'Why Vinyl Records Came Back — and How a Groove Actually Holds a Song',
       FACT,
       'A vinyl record is one continuous spiral groove up to half a kilometre long, read by a microscopic diamond. No wonder people never quite let it go.',
       '/static/img/articles/vinyl-records.jpg',
       """
<p>In an era when nearly every song ever recorded fits inside your pocket for the price of two coffees a month, vinyl records have quietly staged one of the most unlikely comebacks in modern retail — outselling CDs in both the UK and the US.</p>

<h3>Music carved in plastic</h3>
<p>Strip away the nostalgia and a vinyl record is a astonishingly simple mechanical trick. Sound is just vibrating air. When a record is mastered, those vibrations are cut as microscopic wiggles into the two V-shaped walls of a single continuous spiral groove — one wall for the left stereo channel, one for the right.</p>
<p>Drop a tiny diamond stylus into that groove and the wiggles shake the needle, which shakes a microscopic magnet inside a coil of wire, producing a tiny electrical signal that an amplifier turns back into music.</p>

<h3>Facts hidden in the groove</h3>
<ul>
<li><strong>Length:</strong> One side of a standard 12-inch LP contains a single groove roughly <strong>450 to 500 metres long</strong>.</li>
<li><strong>Speed:</strong> Standard albums spin at <strong>33⅓ revolutions per minute</strong> — chosen in 1948 so a 12-inch disc could hold roughly 22 minutes per side, enough for a classical movement.</li>
<li><strong>Outer tracks sound sharper:</strong> Because the outer rim moves past the needle faster than the inner ring near the label, engineers often place loud, bright songs at the start of a side and softer ballads at the end.</li>
</ul>

<h3>Why people keep buying them</h3>
<p>Listening to vinyl forces an album to be played in order, without skipping thirty seconds in. Add the twelve-inch artwork, liner notes and the simple pleasure of owning a physical thing nobody can remove from a streaming catalogue, and the revival makes complete sense.</p>
"""),

    # 10. MUSIC — Drawn SVG
    _a('famous-songs-written-in-under-an-hour',
       'Eight Famous Songs Written in Less Than an Hour',
       FACT,
       'Some masterpieces take years of studio agony. Others were dashed off on the back of an envelope, in a cab, or to fill three empty minutes on an album.',
       '/static/img/articles/fast-songs.svg',
       """
<p>Songwriting is notoriously unpredictable. Leonard Cohen famously spent years drafting dozens of verses for <em>Hallelujah</em>; other classics arrived almost fully formed before the tea went cold.</p>

<h3>1. Black Sabbath — Paranoid (~25 minutes)</h3>
<p>The band needed a short filler track to finish their 1970 album. Guitarist Tony Iommi came up with the riff on the spot while the rest of the band were at the pub, Geezer Butler scribbled the lyrics in minutes, and it became their signature song.</p>

<h3>2. Paul McCartney — Yesterday (in a dream)</h3>
<p>McCartney woke up in 1965 with the entire melody in his head and spent weeks asking friends if he had accidentally stolen it. Until he found the real lyrics, he sang the placeholder words <em>"Scrambled eggs, oh my baby how I love your legs"</em>.</p>

<h3>3. Guns N’ Roses — Sweet Child o’ Mine (~5 minutes)</h3>
<p>Slash was warming up with a string-skipping exercise he thought sounded like circus music. Bandmates joined in as a joke, Axl Rose heard it from upstairs and started writing lyrics, and one of rock’s most famous intros was born.</p>

<h3>4. Lady Gaga — Just Dance (~10 minutes)</h3>
<p>Written during a hangover in a Los Angeles studio in 2008, the debut single that launched her career was knocked out in roughly ten minutes.</p>

<h3>5. Beyoncé — Single Ladies (~20 minutes)</h3>
<p>Songwriter The-Dream wrote the lyrics in about twenty minutes after hearing Beyoncé had quietly married Jay-Z, trying to capture how single fans would react.</p>

<h3>6. R.E.M. — Losing My Religion (~15 minutes)</h3>
<p>Peter Buck had just bought a mandolin and was learning how to play it in front of the television. The arpeggio he stumbled onto while practising became the backbone of the band’s biggest hit.</p>

<h3>7. Adele — Skyfall (~10 minutes for the first draft)</h3>
<p>After reading the James Bond script, Adele and producer Paul Epworth drafted the opening verse and chorus in ten minutes flat.</p>

<h3>8. The Rolling Stones — (I Can’t Get No) Satisfaction (overnight)</h3>
<p>Keith Richards woke in a Florida hotel room, recorded the iconic guitar riff onto a cassette tape, and fell back asleep. When he played the tape the next morning, there were two minutes of guitar followed by forty minutes of snoring.</p>
"""),

    # 11. MUSIC & SCIENCE — Drawn SVG
    _a('why-music-gives-you-goosebumps',
       'Why Certain Chords Give You Goosebumps (and Why Some People Never Get Them)',
       FACT,
       'Scientists call musical chills "frisson". Brain scans show they happen when a song builds an expectation — and then breaks it at the exact right moment.',
       '/static/img/articles/music-goosebumps.svg',
       """
<p>Almost everyone has a song that triggers a sudden shiver down the spine — a swelling chorus, a key change, or a voice entering alone after silence. Researchers call the sensation <strong>frisson</strong>, from the French word for a chill.</p>

<h3>Your brain is a prediction machine</h3>
<p>While you listen to music, your brain is constantly guessing what note or beat comes next based on every song you have ever heard. When a composer builds tension and then resolves it in a slightly unexpected way — a sudden shift in volume, a surprise harmony, or a dramatic pause — your reward system fires a burst of <strong>dopamine</strong>.</p>
<p>Brain-imaging studies at McGill University found that dopamine actually begins rising <em>seconds before</em> the favourite part of a song arrives, because your brain anticipates the payoff.</p>

<h3>Why your hairs stand up</h3>
<p>Goosebumps are an ancient mammalian reflex designed to puff up fur in the cold or make an animal look larger when startled. A sudden emotional jolt from music briefly hijacks the exact same fight-or-flight wiring, even though you are sitting safely on the sofa.</p>

<h3>Why not everyone gets them</h3>
<p>Roughly half to two-thirds of people experience musical chills regularly; others never feel them at all. Studies suggest people who get frisson tend to have denser nerve fibres linking the auditory cortex (which processes sound) to the regions that handle emotion, and score higher on a personality trait psychologists call "openness to experience".</p>
"""),

    # 12. MUSIC — Drawn SVG
    _a('the-strangest-instruments-ever-invented',
       'Seven Real Musical Instruments You Probably Did Not Know Existed',
       STRANGE,
       'An instrument you play without touching, an organ powered by ocean waves, and Benjamin Franklin’s spinning glass bowls.',
       '/static/img/articles/strange-instruments.svg',
       """
<p>Most of us can name the standard orchestra sections without blinking. Beyond violins and trumpets, however, inventors have spent centuries turning electricity, water, fire and spinning glass into music.</p>

<h3>1. The Theremin</h3>
<p>Invented by Russian physicist Léon Theremin in 1920, it is the only well-known instrument played entirely without physical contact. Two metal antennas sense the position of the player’s hands in mid-air — one controls pitch, the other volume. You have almost certainly heard its eerie wail in 1950s sci-fi films and the Beach Boys’ <em>Good Vibrations</em>.</p>

<h3>2. The Sea Organ (Zadar, Croatia)</h3>
<p>Built into a marble staircase along the Adriatic waterfront, 35 hidden organ pipes are played continuously by the movement of waves and wind pushing air through underwater tubes. No two minutes sound quite the same.</p>

<h3>3. The Glass Armonica</h3>
<p>Invented by Benjamin Franklin in 1761 — he considered it his most satisfying invention. Nested glass bowls spin on a horizontal spindle, and the player touches the rims with wet fingers to produce an angelic, shimmering chord. Mozart and Beethoven both wrote pieces for it.</p>

<h3>4. The Nyckelharpa</h3>
<p>A traditional Swedish "keyed fiddle" dating back to the 14th century. It looks like a cross between a violin and a typewriter: the player bows the strings while pressing wooden keys that slide tangents against them, while twelve sympathetic strings ring underneath.</p>

<h3>5. The Hydrolauphone</h3>
<p>An acoustic instrument where you block jets of water with your fingers to redirect the flow into sound-producing chambers — essentially a flute made of water.</p>

<h3>6. The Pyrophone</h3>
<p>Invented in the 1870s, the pyrophone is an organ whose notes are produced by controlled gas flames burning inside glass tubes.</p>

<h3>7. The Stalacpipe Organ</h3>
<p>Installed in Luray Caverns, Virginia, in 1956, it uses rubber-tipped mallets wired to a console to tap real limestone stalactites across three and a half acres of cave, turning the cavern itself into the largest musical instrument on Earth.</p>
"""),

    # 13. MUSIC — Drawn SVG
    _a('how-the-440hz-tuning-standard-happened',
       'Why Almost Every Orchestra in the World Tunes to 440 Hz',
       FACT,
       'For centuries, the note A meant something completely different in London, Paris and Vienna. Agreeing on 440 vibrations per second took nearly a century of arguments.',
       '/static/img/articles/tuning-440hz.svg',
       """
<p>Before an orchestra plays a note, the oboe sounds a single steady A and everyone adjusts to match it. Almost everywhere on Earth, that note vibrates at exactly <strong>440 cycles per second (440 Hz)</strong>. It was not always that way.</p>

<h3>When every city had its own A</h3>
<p>In the 17th and 18th centuries there was no global standard for pitch. An A played on a church organ in Hamburg might be a whole tone higher than an A in Paris. Travelling singers hated it, because arias that sat comfortably in one city strained their voices in the next.</p>
<p>Even worse, nineteenth-century orchestras engaged in "pitch inflation": string players noticed that tuning slightly sharper made violins sound brighter and louder, so rival orchestras crept higher and higher until sopranos began threatening to quit.</p>

<h3>France steps in</h3>
<p>In 1859, the French government passed a law fixing A at <strong>435 Hz</strong> — the <em>diapason normal</em> — and cast a master tuning fork in Paris. Britain and America drifted slightly higher, partly because brass instruments warmed up faster in heated concert halls.</p>

<h3>How 440 Hz won</h3>
<p>In 1939 an international conference in London recommended <strong>440 Hz</strong>, and in 1955 the International Organization for Standardization made it official as <strong>ISO 16</strong>. Today, electronic tuners, synthesizers and digital audio workstations all default to 440 Hz — though a few European orchestras still quietly nudge up to 442 or 443 Hz for extra brilliance.</p>
"""),

    # 14. MUSIC — Photo
    _a('songs-that-were-originally-written-for-someone-else',
       'Ten Hit Songs That Were Originally Written for Someone Else',
       FACT,
       'From Umbrella and ...Baby One More Time to Since U Been Gone — huge pop anthems that passed through other hands before finding the voice that made them famous.',
       '/static/img/articles/studio-microphone.jpg',
       """
<p>Behind the scenes of pop music, hit songs are passed around like hot potatoes. A track turned down by one superstar on a Tuesday can launch someone else’s career by Friday.</p>

<ul>
<li><strong>...Baby One More Time (Britney Spears):</strong> Written by Max Martin for R&amp;B trio TLC, who passed because they were taking a break and did not like the line "hit me baby".</li>
<li><strong>Umbrella (Rihanna):</strong> Written with Britney Spears in mind; her label turned it down without her even hearing it. Mary J. Blige also passed before Rihanna recorded it.</li>
<li><strong>Since U Been Gone (Kelly Clarkson):</strong> Originally offered to Pink and then Hilary Duff, who could not hit the chorus notes.</li>
<li><strong>Toxic (Britney Spears):</strong> Offered first to Kylie Minogue, who turned it down — a decision she later joked was "the one that got away".</li>
<li><strong>I Don’t Want to Miss a Thing (Aerosmith):</strong> Diane Warren wrote it imagining Celine Dion singing it; it ended up giving Aerosmith their only US number one.</li>
<li><strong>Happy (Pharrell Williams):</strong> Originally recorded by CeeLo Green for <em>Despicable Me 2</em>, before Green’s team opted to focus on his own album instead.</li>
<li><strong>Telephone (Lady Gaga &amp; Beyoncé):</strong> Gaga originally wrote it for Britney Spears’s <em>Circus</em> album; Spears even recorded a demo before shelving it.</li>
<li><strong>Nothing Compares 2 U (Sinéad O’Connor):</strong> Written by Prince for his side-project band The Family in 1985, where it barely charted until O’Connor’s 1990 version took over the world.</li>
<li><strong>Don’t You (Forget About Me) (Simple Minds):</strong> Written for <em>The Breakfast Club</em> and turned down by Billy Idol, Bryan Ferry and The Fixx before Simple Minds reluctantly agreed.</li>
<li><strong>Shape of You (Ed Sheeran):</strong> Sheeran began writing it for Rihanna, then decided halfway through the session that some of the lyrics did not fit her and kept it himself.</li>
</ul>
"""),

    # 15. NATURE — Photo
    _a('how-trees-talk-through-the-wood-wide-web',
       'How Forests Share Food and Warnings Underground',
       FACT,
       'Beneath every woodland floor sits a vast web of microscopic fungi linking tree roots together, trading sugars for minerals and passing chemical distress signals.',
       '/static/img/articles/wood-wide-web.jpg',
       """
<p>Walk through an old woodland and the trees look like solitary rivals competing for sunlight. Look a few centimetres below the leaf litter, however, and the forest is wired together like a neighbourhood.</p>

<h3>The fungal trade network</h3>
<p>Almost all land plants form partnerships with <strong>mycorrhizal fungi</strong> — microscopic threads (hyphae) that wrap around and even enter tree roots. The deal is mutually beneficial: trees use sunlight to make carbon-rich sugars and pump up to 30% of them down into the fungi; in return, the ultra-fine fungal threads mine the soil for water, phosphorus and nitrogen that thick tree roots cannot reach on their own.</p>

<h3>One web, many trees</h3>
<p>Because a single fungal network can connect to the roots of dozens of neighbouring trees, ecologist Suzanne Simard’s isotope-tracing experiments in the 1990s showed that carbon can move from one tree to another — for example, from sunlit birch trees to shaded Douglas fir seedlings struggling on the forest floor.</p>

<h3>Chemical warnings</h3>
<p>When a tree is attacked by aphids or beetles, it releases defensive chemicals both into the air and into the underground network. Neighbouring trees connected to the same fungal threads can detect those signals and start producing bitter, insect-repelling compounds before the pests even arrive.</p>

<h3>Not quite a fairy tale</h3>
<p>Biologists are careful to point out that the "Wood Wide Web" is not pure altruism. Fungi are shrewd traders — they hoard nutrients in areas of scarcity and sometimes charge higher carbon "prices" to desperate plants. Still, a forest is far closer to a connected community than a collection of lone trunks.</p>
"""),

    # 16. NATURE — Drawn SVG
    _a('the-loudest-animals-on-earth',
       'The Loudest Animals on Earth (and Why a Tiny Shrimp Beats a Jet Engine)',
       STRANGE,
       'Blue whales and sperm whales can be heard across oceans, yet one of the loudest sounds in the entire animal kingdom comes from a shrimp five centimetres long.',
       '/static/img/articles/loudest-animals.svg',
       """
<p>Ask a quiz team to name the loudest animal on Earth and most will write down "lion" or "elephant". Both are impressive, yet neither makes the top five.</p>

<h3>The real heavyweights</h3>
<table>
<tr><th>Animal</th><th>Peak volume</th><th>Notes</th></tr>
<tr><td>Sperm whale</td><td>up to ~230 dB (underwater)</td><td>Echolocation clicks powerful enough to stun prey</td></tr>
<tr><td>Snapping (pistol) shrimp</td><td>~210 dB (underwater)</td><td>A collapsing cavitation bubble, not a vocal cord</td></tr>
<tr><td>Blue whale</td><td>~188 dB (underwater)</td><td>Low-frequency calls travel hundreds of miles</td></tr>
<tr><td>Greater bulldog bat</td><td>~140 dB (in air)</td><td>Ultrasonic — mercifully above human hearing</td></tr>
<tr><td>Howler monkey</td><td>~128–140 dB (in air)</td><td>Heard three miles away through dense rainforest</td></tr>
<tr><td>White bellbird</td><td>~125 dB (in air)</td><td>Loudest bird ever measured — louder than a chainsaw</td></tr>
<tr><td>Lion</td><td>~114 dB (in air)</td><td>Audible up to five miles across open savannah</td></tr>
</table>

<h3>How a five-centimetre shrimp breaks 200 decibels</h3>
<p>The pistol shrimp does not shout. One of its claws is oversized and hinged like a spring-loaded hammer. When it snaps shut, it fires a jet of water so fast that the pressure drops below boiling point, forming a microscopic <strong>cavitation bubble</strong>. A millisecond later the surrounding water crushes the bubble — creating a shockwave over 200 decibels, a flash of light, and a brief core temperature approaching the surface of the Sun. Nearby small fish are stunned instantly.</p>
<p>Whole colonies of snapping shrimp on reefs make so much crackling noise that submarine sonar operators during World War II used them as acoustic camouflage.</p>
"""),

    # 17. NATURE — Photo
    _a('why-autumn-leaves-change-colour',
       'Why Autumn Leaves Turn Red and Gold — It Is Not Just the Cold',
       FACT,
       'Yellow and orange pigments were hiding inside green leaves all summer. Reds, on the other hand, are freshly manufactured by the tree at the very last minute.',
       '/static/img/articles/autumn-leaves.jpg',
       """
<p>Every October, whole hillsides switch from green to copper, gold and scarlet. Most people assume frost causes it, yet the real trigger is something far more reliable than the weather: <strong>the length of the night</strong>.</p>

<h3>Daylight is the alarm clock</h3>
<p>Because temperatures bounce up and down wildly from year to year, trees cannot trust a cold snap to tell them winter is coming. Instead, they track shortening daylight hours. Once nights pass a critical length, deciduous trees begin shutting down their leaf factories and pulling valuable nutrients back into their branches and roots before dropping the leaves.</p>

<h3>Gold was there all along</h3>
<p>Throughout spring and summer, leaves are packed with <strong>chlorophyll</strong> — the green pigment that captures sunlight. Chlorophyll is so dominant that it masks two other pigments already sitting in the leaf: yellow <strong>xanthophylls</strong> and orange <strong>carotenoids</strong> (the same compound that colours carrots). As chlorophyll breaks down in autumn, the green curtain lifts and the hidden yellows and oranges simply show through.</p>

<h3>Red is made fresh</h3>
<p>Bright scarlets and crimsons come from a different family of pigments called <strong>anthocyanins</strong>, which trees actively manufacture in autumn when bright sunny days trap sugars inside the leaf and cool nights slow their exit. Scientists think these red pigments act like biological sunscreen, shielding the leaf’s fragile cells from autumn glare for just a few extra days while the tree finishes salvaging nitrogen.</p>
"""),

    # 18. NATURE — Photo
    _a('birds-that-sleep-while-flying',
       'How Some Birds Stay Aloft for Months Without Landing Once',
       STRANGE,
       'Common swifts spend ten months straight in the air, and frigatebirds sleep with half their brain switched off while gliding over the open ocean.',
       '/static/img/articles/soaring-seabird.jpg',
       """
<p>If you watch common swifts screaming over British rooftops in June, you are looking at one of the most extreme athletes on the planet. Apart from the few weeks they spend raising chicks in a nest, they barely touch solid ground at all.</p>

<h3>Ten months without landing</h3>
<p>In 2016, researchers at Lund University fitted tiny lightweight data loggers onto common swifts. The results astonished even ornithologists: several birds stayed continuously airborne for <strong>ten full months</strong> between breeding seasons, eating insects on the wing, drinking by skimming water surfaces, and sleeping high in the night sky while gliding on rising air currents.</p>

<h3>Half-brain sleep at 3,000 feet</h3>
<p>How do you sleep without stalling or crashing into the sea? Miniature brain-wave recorders mounted on great frigatebirds flying over the Pacific revealed the trick: <strong>unihemispheric slow-wave sleep</strong>. They literally switch off one half of their brain at a time while keeping the other half — and the opposite eye — awake to watch for thermals and other birds.</p>
<p>Even more remarkably, frigatebirds in flight managed on just <strong>42 minutes of sleep per day</strong>, taken in tiny ten-second bursts — compared with over twelve hours a day once they returned to land.</p>

<h3>The albatross autopilot</h3>
<p>Wandering albatrosses cross entire oceans while barely flapping their wings, using a technique called <strong>dynamic soaring</strong>: repeatedly swooping down into slower wind near the wave troughs and turning up into faster wind above, harvesting free energy from the wind gradient for thousands of miles.</p>
"""),

    # 19. NATURE — Drawn SVG
    _a('the-oldest-living-things-on-earth',
       'The Oldest Living Things on Earth Right Now',
       REF,
       'A California pine older than Stonehenge’s final stones, a shark swimming since Shakespeare’s day, and a single underground colony that may predate agriculture.',
       '/static/img/articles/oldest-living.svg',
       """
<p>Human lifespans feel long until you compare them with the quiet record-holders sharing the planet right now. Every organism below is alive today — or verified by ring counts and radiocarbon dating.</p>

<h3>Verified individual record-holders</h3>
<table>
<tr><th>Organism</th><th>Estimated age</th><th>Where</th></tr>
<tr><td>Great Basin bristlecone pine ("Methuselah")</td><td>~4,850 years</td><td>White Mountains, California</td></tr>
<tr><td>Alerce tree ("Gran Abuelo")</td><td>~3,600–5,000+ years</td><td>Alerce Costero, Chile</td></tr>
<tr><td>Ocean quahog clam ("Ming")</td><td>507 years (when found)</td><td>Icelandic seabed</td></tr>
<tr><td>Greenland shark</td><td>~270–400+ years</td><td>North Atlantic &amp; Arctic</td></tr>
<tr><td>Bowhead whale</td><td>200+ years</td><td>Arctic waters</td></tr>
<tr><td>Jonathan the Seychelles giant tortoise</td><td>190+ years (hatched ~1832)</td><td>Saint Helena</td></tr>
</table>

<h3>Clonal colonies: bending the rules</h3>
<p>If you count genetically identical stems sharing one single root system, the numbers leap into deep prehistory:</p>
<ul>
<li><strong>Pando (Utah, USA):</strong> A 106-acre forest of roughly 47,000 quaking aspen trunks that are all genetically one single male organism, connected underground. Estimates put its age between <strong>9,000 and 16,000 years</strong>.</li>
<li><strong>Posidonia oceanica (Mediterranean Sea):</strong> Vast meadows of Neptune grass off Ibiza and Formentera are single clonal organisms thought to be tens of thousands of years old.</li>
</ul>

<h3>Why Greenland sharks live so long</h3>
<p>In freezing Arctic water, everything runs in slow motion. A Greenland shark cruises at barely one mile per hour, grows less than a centimetre a year, and does not even reach breeding maturity until it is roughly <strong>150 years old</strong>.</p>
"""),

    # 20. NATURE & PHYSICS — Photo
    _a('why-cats-always-land-on-their-feet',
       'How Cats Flip Mid-Air Without Breaking the Laws of Physics',
       FACT,
       'Nineteenth-century physicists were baffled by how a falling cat twists right-side up with nothing to push against. The answer turns out to be a clever trick of geometry.',
       '/static/img/articles/cat-physics.jpg',
       """
<p>If you float in empty space with nothing to push off, basic physics says you cannot start spinning from a standstill — angular momentum has to stay conserved. Yet drop a cat upside down from a low height and, within half a second, it flips neatly onto all four paws. It puzzled physicists for decades.</p>

<h3>The two-cylinder trick</h3>
<p>In 1894, French physiologist Étienne-Jules Marey took high-speed photographs of a falling cat at 60 frames per second and solved the mystery. A cat is not a rigid brick; it has an extraordinarily flexible spine and no collarbone, which lets it behave like <strong>two separate cylinders</strong> hinged at the waist:</p>
<ol>
<li>First, the cat bends sharply at the waist and <strong>tucks its front legs in close</strong> while extending its back legs out wide.</li>
<li>Because tucked legs are much easier to spin than extended ones (just like a figure skater pulling their arms in), the front half rotates quickly while the back half twists only slightly in the opposite direction.</li>
<li>Next, the cat reverses the trick: it <strong>extends its front legs</strong> and tucks its back legs in, rotating the rear half round to match the front.</li>
</ol>
<p>Total angular momentum stays strictly zero throughout — yet the cat finishes 180 degrees turned and lands cleanly on its feet.</p>

<h3>Useful for astronauts too</h3>
<p>NASA actually studied the "cat righting reflex" in the 1960s to teach astronauts how to reorient their bodies while floating weightlessly inside a spacecraft without grabbing a handrail.</p>
"""),

    # 21. FOOD & DRINK — Photo
    _a('how-coffee-took-over-the-world',
       'How Coffee Went From an Ethiopian Forest to Two Billion Cups a Day',
       FACT,
       'Smuggled beans, banned coffeehouses, and why the plant evolved caffeine in the first place — the surprisingly dramatic history of your morning cup.',
       '/static/img/articles/coffee-history.jpg',
       """
<p>Today the world drinks more than two billion cups of coffee every day, yet for most of human history the plant grew wild in only one corner of the planet: the misty highlands of Ethiopia.</p>

<h3>Why the plant makes caffeine at all</h3>
<p>Coffee plants did not evolve caffeine to help humans through Monday mornings. Caffeine is a natural <strong>chemical weapon</strong>. In high concentrations inside leaves and seeds, it paralyses or kills insects that try to eat the plant. In tiny doses inside the flower nectar, however, it actually improves bees’ memory — making them more likely to come back and pollinate the same species again.</p>

<h3>From Yemen to London’s "Penny Universities"</h3>
<p>By the 15th century, coffee was being roasted and brewed in Sufi monasteries in Yemen to help worshippers stay awake during night prayers. Yemen guarded its monopoly fiercely, boiling or roasting every exported bean so nobody else could plant it. Legend credits a 17th-century pilgrim named Baba Budan with smuggling seven fertile beans out of Mocha strapped to his chest into India.</p>
<p>When coffeehouses reached London in the 1650s, they became known as <strong>"penny universities"</strong>: for the price of a single penny cup, anyone could sit for hours debating politics, science and shipping news. Lloyd’s of London, the London Stock Exchange and several newspapers all began inside London coffeehouses.</p>

<h3>Arabica vs Robusta</h3>
<ul>
<li><strong>Arabica</strong> (~60% of global supply): grown at higher altitudes, sweeter and more aromatic, with roughly half the caffeine of Robusta.</li>
<li><strong>Robusta</strong> (~40%): hardier, earthier, higher in caffeine, and prized for giving Italian espresso its thick golden crema.</li>
</ul>
"""),

    # 22. FOOD & SCIENCE — Drawn SVG
    _a('why-chilli-peppers-feel-hot',
       'Why Chilli Peppers Feel Hot When Nothing Is Actually Burning',
       FACT,
       'A chilli pepper is at room temperature, yet your mouth insists it is on fire. The culprit is a single molecule that hijacks your pain wiring — and birds are completely immune to it.',
       '/static/img/articles/chilli-scoville.svg',
       """
<p>Bite into a fresh habanero and your body reacts as if you just swallowed boiling water: your mouth stings, your face flushes, your eyes water and you start sweating. Yet if you stick a thermometer into the pepper, it is sitting peacefully at room temperature.</p>

<h3>A false alarm in your nerves</h3>
<p>Chillies contain a colourless oil called <strong>capsaicin</strong>. On your tongue and skin sit microscopic nerve receptors called <strong>TRPV1</strong> whose real job is to warn your brain when you touch something dangerously hot (above about 43°C). Capsaicin happens to fit into that exact receptor like a stolen key, tricking your brain into believing your mouth is literally burning.</p>

<h3>Why birds do not care</h3>
<p>Chilli plants evolved capsaicin for a brilliant reason. Mammals have grinding molar teeth that crush chilli seeds and destroy them; birds swallow seeds whole and fly miles away before dropping them intact in ready-made fertiliser. Conveniently, <strong>birds’ TRPV1 receptors are shaped differently</strong> — capsaicin does not bind to them at all. A parrot can munch a Carolina Reaper as casually as a cucumber.</p>

<h3>Why water makes it worse</h3>
<p>Capsaicin is an oil, not water-soluble. Gulping cold water just spreads the oil across more receptors. What actually works is <strong>milk or yoghurt</strong>: a milk protein called <strong>casein</strong> acts like tiny detergent sponges that wrap around capsaicin molecules and wash them off your nerves.</p>
"""),

    # 23. FOOD & HISTORY — Photo
    _a('the-strange-history-of-spices-worth-more-than-gold',
       'When Nutmeg Was Worth More Than Gold',
       STRANGE,
       'In the 17th century, a handful of nutmeg from one tiny Indonesian island group could buy a house in London — and the Dutch traded Manhattan to keep it.',
       '/static/img/articles/nutmeg-spices.jpg',
       """
<p>Open a kitchen cupboard today and a jar of ground nutmeg costs less than two pounds. Four hundred years ago, it was one of the most valuable substances on Earth, and European empires fought bloody wars to control it.</p>

<h3>One tiny archipelago</h3>
<p>Until the late 18th century, the nutmeg tree (<em>Myristica fragrans</em> — which also produces mace from the lacy red shell around the seed) grew natively in only one place on the entire planet: the <strong>Banda Islands</strong>, a speck of volcanic land in eastern Indonesia.</p>
<p>By the time a pound of nutmeg travelled from Banda through Arab and Venetian traders to London, its price had multiplied hundreds of times over. It was prized not only for flavouring food, but because doctors of the era believed a pouch of nutmeg hung around the neck could ward off the bubonic plague.</p>

<h3>The island traded for New York</h3>
<p>By the mid-1600s the Dutch East India Company controlled nearly every Banda island except one tiny English-held outcrop called <strong>Run</strong>. After years of fighting, the two nations signed the Treaty of Breda in 1667. The Dutch kept Run — securing a total global monopoly on nutmeg — and in exchange let the English keep a muddy little Dutch trading post on the other side of the world called <strong>New Amsterdam</strong>, which the English renamed New York.</p>

<h3>How the monopoly collapsed</h3>
<p>In 1770, a French horticulturist named Pierre Poivre (literally "Peter Pepper") managed to smuggle live nutmeg seedlings out of the Dutch East Indies and plant them on Mauritius. Once nutmeg grew elsewhere, the price collapsed — and Manhattan turned out to be the better deal.</p>
"""),

    # 24. FOOD & SCIENCE — Photo
    _a('why-bread-crusts-and-seared-steaks-taste-so-good',
       'The Maillard Reaction: The One Piece of Chemistry Behind Almost Every Good Meal',
       FACT,
       'Toasted bread, roasted coffee, crispy chips and seared steak all owe their flavour to the exact same chemical reaction — discovered in 1912 by a French doctor.',
       '/static/img/articles/maillard-bread.jpg',
       """
<p>Compare a boiled piece of dough with a crusty sourdough loaf, or a steamed potato with a roast one. The ingredients are identical, yet one tastes bland and the other smells irresistible from the hallway. Almost all of that magic comes from one chemical reaction.</p>

<h3>Meet Louis-Camille Maillard</h3>
<p>In 1912, French physician Louis-Camille Maillard was studying how amino acids link together when he noticed that heating proteins and sugars together turned the mixture brown and filled his lab with savoury, nutty aromas. He was not even trying to study cooking — he was researching kidney disease — yet he had just named the foundation of modern flavour.</p>

<h3>The 140°C rule</h3>
<p>The <strong>Maillard reaction</strong> starts rolling properly around <strong>140°C to 165°C</strong>. That single number explains almost every golden rule in the kitchen:</p>
<ul>
<li><strong>Why you pat meat dry before frying:</strong> Water boils at 100°C. As long as food is wet, the surface is stuck at 100°C — too cool for browning. You steam instead of sear.</li>
<li><strong>Why you do not crowd the frying pan:</strong> Too many mushrooms or pieces of chicken release steam faster than it can escape, trapping the pan below 140°C.</li>
<li><strong>Why a pinch of baking soda speeds up caramelising onions:</strong> Slightly alkaline conditions turbo-charge the Maillard reaction, browning food in half the time.</li>
</ul>

<h3>Not the same as caramelisation</h3>
<p>Caramelisation involves sugars alone heated past 160°C. The Maillard reaction needs both <strong>sugars and amino acids</strong> — and creates hundreds of completely new aroma compounds, which is why roasted coffee, malted barley, toasted marshmallows and crispy roast potatoes all share a warm, complex depth.</p>
"""),

    # 25. FOOD & DRINK — Drawn SVG
    _a('how-tea-is-all-the-same-plant',
       'Green, Black, Oolong and White: How One Plant Makes Almost Every Tea',
       REF,
       'Every true tea in the world — from delicate Japanese sencha to builder’s brew — comes from the exact same evergreen bush. The only difference is what happens after picking.',
       '/static/img/articles/tea-plant.svg',
       """
<p>Walk down a supermarket tea aisle and you might assume green tea, white tea, oolong and English Breakfast come from completely different crops. In fact, every single true tea on Earth comes from the leaves of one evergreen shrub: <strong><em>Camellia sinensis</em></strong>.</p>

<h3>It is all about oxidation</h3>
<p>Cut an apple in half and leave it on the counter: within minutes enzymes in the flesh react with oxygen and turn it brown. Tea makers use that exact same process — <strong>oxidation</strong> — to transform freshly picked leaves into completely different drinks.</p>

<table>
<tr><th>Tea type</th><th>Oxidation level</th><th>How it is made</th></tr>
<tr><td><strong>White tea</strong></td><td>Very light (~5%)</td><td>Young buds picked and simply withered and dried in the sun or warm air.</td></tr>
<tr><td><strong>Green tea</strong></td><td>None (0%)</td><td>Steamed (Japan) or pan-fired (China) straight after picking to switch off the browning enzymes and lock in the fresh green taste.</td></tr>
<tr><td><strong>Oolong</strong></td><td>Partial (15–80%)</td><td>Leaves are bruised, rolled and partly oxidised before firing — giving everything from floral light oolongs to rich, toasty dark ones.</td></tr>
<tr><td><strong>Black tea</strong></td><td>Full (100%)</td><td>Crushed or rolled so the juices meet the air completely, turning the leaf dark copper-brown with bold tannins.</td></tr>
<tr><td><strong>Pu-erh</strong></td><td>Fermented</td><td>Aged with beneficial microbes over months or decades, much like fine cheese or wine.</td></tr>
</table>

<h3>What about herbal "teas"?</h3>
<p>Chamomile, peppermint, rooibos and hibiscus do not come from <em>Camellia sinensis</em> at all. Strictly speaking they are <strong>tisanes</strong> (infusions) — which is why they are naturally caffeine-free.</p>
"""),

    # 26. FOOD & SCIENCE — Photo
    _a('why-chocolate-melts-at-body-temperature',
       'Why Chocolate Melts in Your Mouth and Not in Your Hand (Usually)',
       FACT,
       'Good chocolate snaps crisply at room temperature and turns silky the instant it hits your tongue because cocoa butter forms six different crystal shapes — and only one is right.',
       '/static/img/articles/chocolate-melt.jpg',
       """
<p>Most fats are either stubbornly solid like wax or messy and soft like butter on a warm day. Cocoa butter is one of nature’s strangest exceptions: it stays rock-hard and glossy at 22°C, yet melts almost instantaneously at <strong>34°C</strong> — just below human body temperature (37°C).</p>

<h3>The secret of Crystal Form V</h3>
<p>When melted cocoa butter cools down, its fat molecules can stack themselves into <strong>six different crystal structures</strong>, labelled Forms I through VI. Most of them are terrible for eating: Forms I to IV melt too easily, look dull and feel crumbly or greasy.</p>
<p><strong>Form V</strong> is the chocolatier’s prize. Its tightly packed crystals give chocolate its mirror shine, its sharp snap when you break a square, and that exact 34°C melting point on your tongue.</p>

<h3>What "tempering" actually does</h3>
<p>When you see a pastry chef melting chocolate, cooling it on a marble slab and gently warming it back up by a couple of degrees, they are not showing off. They are deliberately melting away the bad crystals so only Form V seeds survive, forcing the entire bar to set cleanly.</p>

<h3>What that white dust on old chocolate is</h3>
<p>Leave a bar in a warm cupboard and it develops chalky white streaks called <strong>fat bloom</strong>. It is not mould and it is completely safe to eat — the cocoa butter simply warmed up, rose to the surface, and recrystallised into a rougher form (Form VI). Melt it into hot chocolate and nobody will ever know.</p>
"""),

    # 27. EVERYDAY LIFE — Photo
    _a('why-aeroplane-windows-are-round',
       'Why Aeroplane Windows Have Rounded Corners (and the Disaster That Forced It)',
       FACT,
       'Early passenger jets had big square windows — until two tragic mid-air breakups in 1954 taught aviation engineers a hard lesson about metal fatigue.',
       '/static/img/articles/aeroplane-window.jpg',
       """
<p>Next time you sit in a window seat, look closely at the pane beside you. Every passenger jet on Earth has oval or rounded-corner windows, and there is a tiny pinhole near the bottom of the inner plastic. Neither feature is decorative.</p>

<h3>The de Havilland Comet</h3>
<p>In 1952, Britain’s <strong>de Havilland Comet</strong> became the world’s first commercial jetliner — flying twice as fast and twice as high as propeller planes, in a sleek pressurised cabin with large, handsome <strong>square windows</strong>.</p>
<p>Then, in 1954, two Comets broke apart in mid-air within three months of each other. Investigators salvaged wreckage from the Mediterranean seabed and submerged an entire Comet fuselage in a giant water tank, pressurising and depressurising it thousands of times to simulate flight after flight.</p>

<h3>Why corners kill metal</h3>
<p>Every time a jet climbs to 35,000 feet, the cabin inflates slightly like a balloon, and deflates again when it lands. Engineers discovered that <strong>sharp 90-degree corners concentrate stress</strong> — focusing two to three times as much force on the tiny metal tip of the corner until microscopic fatigue cracks form and unzip the fuselage.</p>
<p>Rounding the corners spreads that stress smoothly around the frame. Every airliner built since 1954 has used rounded windows.</p>

<h3>And the tiny pinhole?</h3>
<p>Cabin windows actually have three panes: the outer structural pane, a middle fail-safe pane, and the flimsy plastic scratch guard you touch. The tiny "bleed hole" sits in the middle pane so cabin air pressure equalises across it — ensuring the strong outer pane carries the full pressure load, while also stopping the window from fogging up.</p>
"""),

    # 28. WORLD & EVERYDAY LIFE — Photo
    _a('how-shipping-containers-shrunk-the-world',
       'The Metal Box That Quietly Changed Almost Everything You Buy',
       FACT,
       'Before 1956, loading a cargo ship took a week of dockers hoisting sacks and crates by hand. One standardised corrugated steel box cut shipping costs by over 90%.',
       '/static/img/articles/shipping-containers.jpg',
       """
<p>Ask people which twentieth-century invention reshaped the global economy most and they will usually say the microchip or the internet. Economists often point to something far less glamorous: a corrugated steel box twenty or forty feet long.</p>

<h3>Before the box</h3>
<p>Until the 1950s, freight moved as "break-bulk" cargo — loose barrels, sacks of coffee, timber bundles and cardboard boxes. Loading a single ship meant hundreds of dockworkers spending a full week wedging odd-shaped parcels into the hold by hand, then unloading them piece by piece at the other end. Ships spent more time tied up in port than sailing, and theft and damage were routine.</p>

<h3>Malcom McLean’s idea</h3>
<p>In April 1956, American trucking entrepreneur <strong>Malcom McLean</strong> loaded 58 metal trailer boxes onto a converted tanker called the <em>Ideal X</em> in Newark, New Jersey, and sailed them to Houston. Loading costs plunged from nearly $6 per ton to roughly <strong>16 cents per ton</strong>.</p>
<p>The real breakthrough was <strong>standardisation</strong>: agreeing globally on exact dimensions and corner twist-locks so the exact same box can lift straight off a mega-ship in Rotterdam, drop onto a railway flatcar, and hitch onto a lorry without anyone ever opening the doors.</p>

<h3>By the numbers</h3>
<ul>
<li>The largest modern container ships carry over <strong>24,000 twenty-foot containers (TEUs)</strong> in a single voyage.</li>
<li>Because shipping a pair of trainers from Asia to Europe now costs pennies per pair, global supply chains and year-round supermarket produce became economically possible.</li>
</ul>
"""),

    # 29. WORLD & STRANGE — Drawn SVG
    _a('why-time-zones-make-no-geographical-sense',
       'The Strangest Time Zones on Earth (Including a 45-Minute Offset)',
       STRANGE,
       'Earth has 24 hours in a day, yet there are 38 different local times in use — including a 3.5-hour border jump in Afghanistan and a country that spans five zones on one clock.',
       '/static/img/articles/weird-timezones.svg',
       """
<p>In a tidy world, the globe would be sliced into 24 neat orange segments, each one hour apart. Because borders are drawn by politics rather than astronomers, the real map of time zones is wonderfully chaotic.</p>

<h3>The strangest outliers</h3>
<ul>
<li><strong>Nepal (UTC+5:45):</strong> One of only three places on Earth using a 45-minute offset (alongside New Zealand’s Chatham Islands and the tiny town of Eucla in Australia). Nepal picked it in 1986 to match the local solar time of Mount Gaurishankar — and to stay 15 minutes distinct from India (UTC+5:30).</li>
<li><strong>China (one zone for the whole country):</strong> Geographically China stretches across five natural time zones, yet since 1949 the entire nation runs on Beijing Time (UTC+8). In far-western Xinjiang, the sun can rise at 10 a.m. in winter.</li>
<li><strong>The Afghanistan–China border:</strong> Step across the tiny 76-kilometre Wakhan Corridor border and your watch jumps by <strong>3 hours and 30 minutes</strong> in a single stride — the largest single-step time-zone jump on land.</li>
<li><strong>Kiribati (UTC+14:00):</strong> In 1995 this Pacific island nation bent the International Date Line sharply eastwards so all its islands shared the same calendar day — making Kiribati the first place on Earth to welcome each New Year, a full 26 hours ahead of Baker Island.</li>
<li><strong>France holds the record:</strong> Thanks to its overseas territories scattered across the Atlantic, Indian and Pacific oceans, France spans <strong>12 different time zones</strong> — more than Russia (11) or the United States.</li>
</ul>
"""),

    # 30. SCIENCE & EVERYDAY LIFE — Drawn SVG
    _a('why-bridges-are-built-with-gaps',
       'Why Bridges Have Metal Teeth, Skyscrapers Sway and Train Tracks Sing',
       FACT,
       'Solid steel and concrete are never truly still. On a hot summer afternoon, the Eiffel Tower grows up to 15 centimetres taller — and engineers have to design around it.',
       '/static/img/articles/bridge-gaps.svg',
       """
<p>Drive across a large motorway bridge and you feel a rhythmic <em>thump-thump</em> as your tyres cross interlocking rows of metal teeth. Those gaps are not a construction flaw — without them, the bridge would tear itself apart in July.</p>

<h3>Solid metal breathes with the weather</h3>
<p>Almost every material expands when heated and shrinks when cooled, because warmer atoms vibrate harder and nudge each other slightly further apart. Over a one-metre steel ruler, a 30°C summer swing changes the length by barely a third of a millimetre. Over a one-kilometre suspension bridge, that tiny fraction multiplies into <strong>more than 30 centimetres of movement</strong>.</p>
<p><strong>Expansion joints</strong> — those interlocking steel combs — let the roadway slide back and forth smoothly as temperatures climb and drop.</p>

<h3>Three more structures that quietly move</h3>
<ul>
<li><strong>The Eiffel Tower:</strong> Built of puddle iron, it grows up to <strong>15 centimetres taller</strong> on hot summer days — and leans slightly away from the sun as the sunlit side expands faster than the shaded side.</li>
<li><strong>Skyscrapers:</strong> Tall towers are engineered to flex in high winds rather than snap. Inside Taipei 101 hangs a 660-tonne golden steel pendulum suspended between the 87th and 92nd floors that swings gently in the opposite direction to calm the sway.</li>
<li><strong>Railway tracks:</strong> Older rails left small gaps between lengths (producing the classic <em>clickety-clack</em> sound). Modern high-speed lines use continuous welded rail stretched tightly in warm weather so it stays under tension — though extreme heatwaves can still cause tracks to buckle into S-shapes, forcing speed limits.</li>
</ul>
"""),

]

