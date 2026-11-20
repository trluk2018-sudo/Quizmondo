"""Article comprehension bonus questions for Mondo Critters' Education bar.

Mapped by article slug so after a player genuinely reads an article (scrolled +
>=15 seconds dwell time), Mondo Critters asks a quick bonus question directly
about what they just read!
"""

ARTICLE_BONUS_QUESTIONS = {
    'how-the-internet-actually-crosses-the-ocean': {
        'prompt': 'Roughly what percentage of intercontinental internet traffic travels via undersea cables rather than satellites?',
        'options': {'A': 'About 25%', 'B': 'About 50%', 'C': 'Over 99%', 'D': 'About 75%'},
        'correct': 'C',
        'explanation': 'Over 99% of intercontinental internet data travels through submarine fibre-optic cables on the seabed.',
    },
    'why-ai-models-still-get-simple-things-wrong': {
        'prompt': 'Why do language models sometimes struggle to count individual letters in words like "strawberry"?',
        'options': {'A': 'They read text in chunks called tokens rather than single letters', 'B': 'They cannot process the letter R', 'C': 'They only read vowels', 'D': 'They translate words into French first'},
        'correct': 'A',
        'explanation': 'A tokeniser slices words into numbered chunks (like str + aw + berry) before the model ever sees them.',
    },
    'the-worlds-smallest-and-strangest-satellites': {
        'prompt': 'How wide is each side of a standard modular CubeSat launched into low Earth orbit?',
        'options': {'A': '1 metre', 'B': '10 centimetres', 'C': '50 centimetres', 'D': '2 millimetres'},
        'correct': 'B',
        'explanation': 'A 1U CubeSat measures just 10 centimetres on each side.',
    },
    'inventions-that-started-as-accidents': {
        'prompt': 'What melted inside engineer Percy Spencer\'s pocket in 1945, leading to the microwave oven?',
        'options': {'A': 'A wax candle', 'B': 'A peanut cluster chocolate bar', 'C': 'A stick of butter', 'D': 'A plastic comb'},
        'correct': 'B',
        'explanation': 'Spencer noticed the peanut cluster bar in his pocket had melted while standing near an active radar magnetron.',
    },
    'why-batteries-still-die-in-the-cold': {
        'prompt': 'Why does a phone battery appear to drop suddenly in freezing winter weather?',
        'options': {'A': 'The cold thickens the liquid electrolyte and slows lithium ions down', 'B': 'Electricity freezes inside the copper wires', 'C': 'The screen draws 10x more power in cold air', 'D': 'The battery permanently loses half its capacity'},
        'correct': 'A',
        'explanation': 'Cold temperatures thicken the electrolyte like honey in a fridge, spiking resistance until the phone warms up again.',
    },
    'how-gps-needs-einstein-to-work': {
        'prompt': 'Without Einstein\'s relativity corrections, roughly how far off would GPS navigation drift every single day?',
        'options': {'A': 'About 10 centimetres', 'B': 'About 10 metres', 'C': 'About 10 kilometres (over 6 miles)', 'D': 'About 1,000 kilometres'},
        'correct': 'C',
        'explanation': 'Satellite clocks run ~38 microseconds fast per day, which would cause roughly 10 km of daily navigation drift.',
    },
    'the-first-things-ever-put-on-the-internet': {
        'prompt': 'What mundane office object was the subject of the world\'s very first webcam at Cambridge University in 1991?',
        'options': {'A': 'A photocopier', 'B': 'A coffee pot', 'C': 'A goldfish bowl', 'D': 'A car park gate'},
        'correct': 'B',
        'explanation': 'Researchers pointed a camera at the Trojan Room coffee pot so they wouldn\'t walk downstairs to find it empty.',
    },
    'how-modern-weather-forecasts-actually-work': {
        'prompt': 'Why do weather forecasters run their supercomputer models dozens of times with tiny tweaks?',
        'options': {'A': 'To average out computer hardware bugs', 'B': 'Because tiny measurement errors grow rapidly (the butterfly effect)', 'C': 'To test different cities one by one', 'D': 'Because satellites only update once a week'},
        'correct': 'B',
        'explanation': 'Ensemble forecasting measures probability — if 40 of 50 runs show rain, you get an 80% chance of rain.',
    },
    'why-vinyl-records-still-outsell-cds': {
        'prompt': 'Roughly how long is the single continuous spiral groove on one side of a 12-inch vinyl LP?',
        'options': {'A': 'About 10 metres', 'B': 'About 50 metres', 'C': 'About 450 to 500 metres', 'D': 'About 5 kilometres'},
        'correct': 'C',
        'explanation': 'One side of a standard 12-inch album packs nearly half a kilometre of microscopic spiral groove.',
    },
    'famous-songs-written-in-under-an-hour': {
        'prompt': 'What placeholder lyrics did Paul McCartney sing for "Yesterday" before writing the real words?',
        'options': {'A': 'Toasted cheese', 'B': 'Scrambled eggs', 'C': 'Sausage rolls', 'D': 'Morning tea'},
        'correct': 'B',
        'explanation': 'He sang "Scrambled eggs, oh my baby how I love your legs" while searching for the final lyrics.',
    },
    'why-music-gives-you-goosebumps': {
        'prompt': 'What French term do scientists use for musical chills or goosebumps?',
        'options': {'A': 'Frisson', 'B': 'Solfège', 'C': 'Cadence', 'D': 'Tremolo'},
        'correct': 'A',
        'explanation': 'Frisson occurs when a song builds an expectation and resolves it with a surprising emotional shift, triggering dopamine.',
    },
    'the-strangest-instruments-ever-invented': {
        'prompt': 'Which 1920 electronic instrument is played entirely in mid-air without physical contact?',
        'options': {'A': 'Nyckelharpa', 'B': 'Theremin', 'C': 'Pyrophone', 'D': 'Glass Armonica'},
        'correct': 'B',
        'explanation': 'Léon Theremin\'s instrument uses two antennas to sense hand proximity for pitch and volume.',
    },
    'how-the-440hz-tuning-standard-happened': {
        'prompt': 'What frequency (in hertz) is the international ISO 16 standard for concert A?',
        'options': {'A': '400 Hz', 'B': '432 Hz', 'C': '440 Hz', 'D': '512 Hz'},
        'correct': 'C',
        'explanation': 'ISO 16 fixed concert A at 440 cycles per second in 1955.',
    },
    'songs-that-were-originally-written-for-someone-else': {
        'prompt': 'Which artist originally wrote "Nothing Compares 2 U" before Sinéad O\'Connor\'s 1990 version became a global hit?',
        'options': {'A': 'Prince', 'B': 'David Bowie', 'C': 'Elton John', 'D': 'George Michael'},
        'correct': 'A',
        'explanation': 'Prince wrote it for his side project The Family in 1985.',
    },
    'how-trees-talk-through-the-wood-wide-web': {
        'prompt': 'What underground organisms link tree roots together to trade sugars for soil minerals?',
        'options': {'A': 'Earthworms', 'B': 'Mycorrhizal fungi', 'C': 'Leafcutter ants', 'D': 'Moss spores'},
        'correct': 'B',
        'explanation': 'Mycorrhizal fungal threads wrap around tree roots, trading soil water and minerals for tree sugars.',
    },
    'the-loudest-animals-on-earth': {
        'prompt': 'How does the five-centimetre pistol shrimp create a 200+ decibel underwater shockwave?',
        'options': {'A': 'By rubbing its legs together', 'B': 'By snapping its claw to collapse a cavitation bubble', 'C': 'By whistling through its gills', 'D': 'By clapping its tail on coral'},
        'correct': 'B',
        'explanation': 'Its high-speed claw snap creates a low-pressure cavitation bubble whose collapse produces a huge shockwave and flash of light.',
    },
    'why-autumn-leaves-change-colour': {
        'prompt': 'What is the primary seasonal alarm clock that triggers deciduous trees to change leaf colour in autumn?',
        'options': {'A': 'The first frost', 'B': 'Shortening daylight / longer nights', 'C': 'Heavy autumn rain', 'D': 'Falling air pressure'},
        'correct': 'B',
        'explanation': 'Trees track the lengthening nights rather than unpredictable temperatures.',
    },
    'birds-that-sleep-while-flying': {
        'prompt': 'How do great frigatebirds sleep while gliding over the open ocean?',
        'options': {'A': 'They land on floating driftwood', 'B': 'They switch off one half of their brain at a time', 'C': 'They never sleep at all', 'D': 'They lock their wings and dive'},
        'correct': 'B',
        'explanation': 'Unihemispheric slow-wave sleep lets them rest half their brain while the other eye stays alert.',
    },
    'the-oldest-living-things-on-earth': {
        'prompt': 'Roughly how old is the famous Great Basin bristlecone pine named "Methuselah" in California?',
        'options': {'A': 'About 800 years', 'B': 'About 1,500 years', 'C': 'About 4,850 years', 'D': 'About 12,000 years'},
        'correct': 'C',
        'explanation': 'Methuselah is around 4,850 years old — older than the final stones of Stonehenge.',
    },
    'why-cats-always-land-on-their-feet': {
        'prompt': 'Which agency studied the "cat righting reflex" in the 1960s to help astronauts turn in zero gravity?',
        'options': {'A': 'NASA', 'B': 'CERN', 'C': 'NOAA', 'D': 'Interpol'},
        'correct': 'A',
        'explanation': 'NASA studied how cats twist front and back halves independently without pushing off anything.',
    },
    'how-coffee-took-over-the-world': {
        'prompt': 'Why did coffee plants originally evolve caffeine in their leaves and seeds?',
        'options': {'A': 'To attract humans', 'B': 'As a natural chemical defence against insects', 'C': 'To survive snowstorms', 'D': 'To help roots absorb iron'},
        'correct': 'B',
        'explanation': 'In high doses caffeine paralyses insects trying to eat the plant, while tiny nectar doses help bees remember the flowers.',
    },
    'why-chilli-peppers-feel-hot': {
        'prompt': 'Why does milk cool a chilli burn much better than cold water?',
        'options': {'A': 'Milk is colder than water', 'B': 'Milk protein (casein) binds to oily capsaicin and washes it off nerves', 'C': 'Milk freezes the tongue', 'D': 'Water reacts chemically with chilli to make acid'},
        'correct': 'B',
        'explanation': 'Capsaicin is an oil — water just spreads it around, whereas casein in milk lifts it away from TRPV1 receptors.',
    },
    'the-strange-history-of-spices-worth-more-than-gold': {
        'prompt': 'In the 1667 Treaty of Breda, which Dutch colony did the English keep in exchange for the nutmeg island of Run?',
        'options': {'A': 'Cape Town', 'B': 'New Amsterdam (New York)', 'C': 'Batavia', 'D': 'Ceylon'},
        'correct': 'B',
        'explanation': 'The Dutch secured a global nutmeg monopoly by trading New Amsterdam — which became New York.',
    },
    'why-bread-crusts-and-seared-steaks-taste-so-good': {
        'prompt': 'Around what temperature does the flavour-creating Maillard reaction really get going?',
        'options': {'A': '60°C', 'B': '100°C', 'C': '140°C to 165°C', 'D': '300°C'},
        'correct': 'C',
        'explanation': 'Because water boils at 100°C, wet food stays too cool for the Maillard browning reaction to take off.',
    },
    'how-tea-is-all-the-same-plant': {
        'prompt': 'What process turns leaves from the exact same Camellia sinensis plant into white, green, oolong, or black tea?',
        'options': {'A': 'Freezing them at different depths', 'B': 'Different levels of oxidation after picking', 'C': 'Adding food colouring', 'D': 'Growing them in salt water'},
        'correct': 'B',
        'explanation': 'Controlling how much enzymes react with air (oxidation) creates every true tea style.',
    },
    'why-chocolate-melts-at-body-temperature': {
        'prompt': 'Which cocoa butter crystal structure gives tempered chocolate its snap, shine, and 34°C melt-in-the-mouth feel?',
        'options': {'A': 'Form I', 'B': 'Form III', 'C': 'Form V', 'D': 'Form IX'},
        'correct': 'C',
        'explanation': 'Tempering melts away unstable crystals so only Form V seeds set across the bar.',
    },
    'why-aeroplane-windows-are-round': {
        'prompt': 'Why did aviation engineers switch from square to rounded cabin windows after 1954?',
        'options': {'A': 'Round glass was cheaper to ship', 'B': 'Sharp 90-degree corners concentrated cabin-pressure metal fatigue', 'C': 'Passengers preferred oval views', 'D': 'Square windows fogged up faster'},
        'correct': 'B',
        'explanation': 'Sharp corners focus two to three times as much pressurisation stress, causing fatigue cracks.',
    },
    'how-shipping-containers-shrunk-the-world': {
        'prompt': 'What was the real economic breakthrough of Malcom McLean\'s 1956 shipping container?',
        'options': {'A': 'Making boxes out of aluminium', 'B': 'Global standardisation across ships, trains and lorries', 'C': 'Refrigerating every box', 'D': 'Painting them bright colours'},
        'correct': 'B',
        'explanation': 'Standard dimensions and twist-locks let one sealed box transfer seamlessly from ship to rail to truck.',
    },
    'why-time-zones-make-no-geographical-sense': {
        'prompt': 'Which country spans the most time zones in the world (12) when overseas territories are included?',
        'options': {'A': 'Russia', 'B': 'United States', 'C': 'France', 'D': 'China'},
        'correct': 'C',
        'explanation': 'France spans 12 time zones thanks to its overseas territories across the Atlantic, Indian and Pacific oceans.',
    },
    'why-bridges-are-built-with-gaps': {
        'prompt': 'Roughly how much taller can the Eiffel Tower grow on a hot summer afternoon due to thermal expansion?',
        'options': {'A': 'Up to 1 millimetre', 'B': 'Up to 15 centimetres', 'C': 'Up to 2 metres', 'D': 'It actually shrinks in heat'},
        'correct': 'B',
        'explanation': 'Its puddle-iron frame expands up to 15 cm in summer heat and leans slightly away from the sun.',
    },
    'capital-cities-of-europe': {
        'prompt': 'Which city functions as Switzerland\'s de facto capital ("federal city")?',
        'options': {'A': 'Zurich', 'B': 'Geneva', 'C': 'Bern', 'D': 'Basel'},
        'correct': 'C',
        'explanation': 'Bern is the federal city of Switzerland, not Zurich or Geneva.',
    },
    'why-honey-never-goes-off': {
        'prompt': 'What is one key reason natural honey can stay edible for thousands of years?',
        'options': {'A': 'It is stored below freezing', 'B': 'Extremely low moisture and natural acidity prevent bacteria growth', 'C': 'Bees add salt to it', 'D': 'It contains alcohol'},
        'correct': 'B',
        'explanation': 'Honey\'s low water activity, acidity, and trace hydrogen peroxide keep microbes from multiplying.',
    },
}
