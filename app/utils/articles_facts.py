# -*- coding: utf-8 -*-
"""Strange-but-true and cool-fact articles, seeded on boot like the first set.

Two categories. "Strange But True" is for things that sound invented and are
not — each item checkable, nothing from the usual list of internet facts that
fall apart when you look them up. "Facts & Curiosities" carries the lighter
fact pieces and shares its category with the fact articles in ``articles``.

Same contract as ``articles``: matched on slug by the seeder, so a redeploy
improves the wording instead of creating a second copy, and a cover chosen by
hand in admin is left alone.
"""

# Only the new one. "Facts & Curiosities" already exists from ``articles``,
# and the seeder matches on slug before it creates anything.
ARTICLE_CATEGORIES_FACTS = [
    ('Strange But True', 'strange-but-true'),
    ('Facts & Curiosities', 'facts-and-curiosities'),
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


STRANGE = 'Strange But True'
FACT = 'Facts & Curiosities'


ARTICLES_FACTS = [

    # ==================================================================
    _a('historical-events-that-sound-like-jokes',
       'Ten Historical Events That Sound Like Jokes But Really Happened',
       STRANGE,
       'A war against birds, a flood of beer, a pope who put a corpse on trial, and a marathon won by a man in a car. All of it documented, none of it invented.',
       '/static/img/articles/strange-history.svg',
       """
<p>Every one of these is in the record — in newspapers, inquest reports or official papers. They are the sort of thing a quizmaster saves for the last round, because half the table refuses to believe the answer.</p>

<h3>1. Australia declared war on emus and lost</h3>
<p>In 1932, around 20,000 emus moved into the wheat belt of Western Australia. Farmers asked for help and got the army: Major G. P. W. Meredith and two Lewis machine guns. The birds scattered whenever the guns opened up, ran faster than the trucks and absorbed hits that should have stopped them. The operation was called off, restarted, and called off again. The emus kept the wheat belt.</p>

<h3>2. Boston was flooded with molasses</h3>
<p>On 15 January 1919 a steel tank in the North End of Boston burst and released around 2.3 million US gallons of molasses. The wave was reported at up to 25 feet high and moved fast enough to lift buildings off their foundations. Twenty-one people died and about 150 were injured. Locals insisted for decades afterwards that you could still smell it on a hot day.</p>

<h3>3. London had a beer flood first</h3>
<p>On 17 October 1814 a vat at the Horse Shoe Brewery on Tottenham Court Road gave way, and well over a hundred thousand gallons of porter went through the slum streets of St Giles. Eight people drowned or were killed by the collapsing walls. The inquest recorded the deaths as an act of God, and the brewery was excused.</p>

<h3>4. A pope put a corpse on trial</h3>
<p>In 897 Pope Stephen VI had the body of his predecessor Formosus dug up, dressed in papal robes and propped on a throne to answer charges. A deacon was told to speak for the defence. The corpse was found guilty, stripped, mutilated and thrown in the Tiber. It is known as the Cadaver Synod, and it did Stephen no good at all — he was strangled in prison within the year.</p>

<h3>5. A war was fought over one pig</h3>
<p>In 1859, on San Juan Island between the United States and British North America, an American settler shot a pig that had got into his potatoes. The pig belonged to the Hudson's Bay Company. Both sides sent soldiers, and within weeks there were around 500 Americans with 14 cannon facing five British warships. Nobody fired. The only casualty of the Pig War was the pig.</p>

<h3>6. Napoleon was routed by rabbits</h3>
<p>In 1807, celebrating a treaty, Napoleon's chief of staff organised a rabbit hunt and bought rabbits to stock it — tame ones, as it turned out. Released, the rabbits took the hunting party for the people who normally brought their food, and charged. Accounts have Napoleon retreating to his carriage while his staff beat them off with riding crops.</p>

<h3>7. A town danced itself into hospital</h3>
<p>In July 1518 a woman recorded as Frau Troffea began dancing in a street in Strasbourg and did not stop. Within a month the city's own chronicles put the number of dancers in the hundreds. Some collapsed; the sources say several died of exhaustion. The city's response was to hire musicians, on the theory that the dancers needed to dance it out.</p>

<h3>8. A chicken lived eighteen months without its head</h3>
<p>In September 1945 a farmer in Fruita, Colorado, beheaded a cockerel for dinner and missed most of the brain stem and one ear. Mike went on to live about eighteen months, fed with an eyedropper, and toured sideshows. The story is odd but the anatomy is not: a chicken's basic functions sit low in the brain stem.</p>

<h3>9. A stork with a spear in its neck solved a mystery</h3>
<p>Until the nineteenth century nobody knew where Europe's birds went in winter — Aristotle thought they hibernated, and one English theory had them flying to the Moon. In 1822 a white stork was shot near Rostock in Germany with a 30-inch Central African spear through its neck, carried all the way home. The <em>Pfeilstorch</em>, or "arrow stork", is still in the collection at Rostock, and it is the first hard evidence of long-distance migration.</p>

<h3>10. An Olympic marathon was won by a man in a car</h3>
<p>The 1904 St Louis marathon was run in dust and heat with one water stop. Fred Lorz dropped out, got a lift, and was photographed accepting the wreath before anybody noticed. The real winner, Thomas Hicks, was kept going by his handlers on a mixture of brandy and strychnine, and had to be carried off the track. A third man was chased a mile off course by farm dogs.</p>

<p>If you want more in this vein, try <a href="/posts/animal-facts-that-sound-made-up">twelve animal facts that sound completely made up</a>.</p>
       """,
       'Ten historical events that sound invented but are fully documented, from the Emu War and the Boston molasses flood to the pope who tried a corpse.'),

    # ==================================================================
    _a('strange-places-that-really-exist',
       'Nine Places on Earth That Sound Made Up',
       STRANGE,
       'A town where almost everyone lives in one building, a fire that has burned since 1962, a river hot enough to kill, and a patch of land no country wants.',
       '/static/img/articles/strange-places.jpg',
       """
<p>All nine are on the map, and you can visit most of them. A couple you should not.</p>

<h3>Whittier, Alaska — a town in one building</h3>
<p>Nearly all of Whittier's residents live in Begich Towers, a former army barracks that also holds the shop, the church, the health clinic and the police station. The only road in runs through a single-lane tunnel shared with the railway, which switches direction by timetable and closes at night. In winter, children can get from home to school without going outside.</p>

<h3>Centralia, Pennsylvania — a town on fire</h3>
<p>A coal seam under Centralia caught alight in 1962 and has been burning ever since. Roads buckled, carbon monoxide seeped into cellars, and in 1984 the government bought the town out. A handful of residents stayed. The fire has enough coal to keep going for another couple of centuries.</p>

<h3>Darvaza, Turkmenistan — the Door to Hell</h3>
<p>A Soviet drilling rig hit a gas pocket here and the ground gave way. The crater has been alight since the 1970s — roughly 70 metres across, visible for miles at night, and hot enough that you feel it well before you reach the lip.</p>

<h3>Bir Tawil — the land nobody claims</h3>
<p>Egypt and Sudan disagree about where their border runs, and the two versions of the line mean that claiming Bir Tawil would mean giving up the much larger and more useful Hala'ib Triangle. So neither claims it. It is one of the only habitable places on land that no state wants.</p>

<h3>Socotra, Yemen — the island that went its own way</h3>
<p>Cut off for millions of years, roughly a third of Socotra's plants grow nowhere else, including the dragon's blood tree, which looks like an umbrella blown inside out and bleeds red sap. Botanists reach for the word "alien" every time, and it is hard to argue.</p>

<h3>Lake Natron, Tanzania — the lake that turns animals to stone</h3>
<p>Natron is so alkaline it can reach a pH near 10.5, and salt-laden enough that animals which die in it are coated and preserved rather than rotting. The photographs that go round online are of real calcified birds, though they were posed for the camera after being found.</p>

<h3>Shanay-timpishka, Peru — the boiling river</h3>
<p>A four-mile stretch of this Amazon tributary runs at around 86°C, hot enough to kill anything that falls in. It is not volcanic. The best explanation is water that fell as rain a long way off, worked its way deep, got hot and came back up through a fault.</p>

<h3>Hashima Island, Japan — the abandoned city block</h3>
<p>A coal island the size of a few football pitches, Hashima once held over 5,000 people and was among the most densely populated places on Earth. The mine closed in 1974 and everybody left within weeks. It is now a ruin of concrete apartment blocks, and from the sea it looks like a battleship — which is what its nickname, Gunkanjima, means.</p>

<h3>Point Nemo — the furthest you can get from land</h3>
<p>In the South Pacific there is a spot about 1,450 nautical miles from the nearest land in any direction. The closest humans are usually the crew of the International Space Station passing overhead, and space agencies use the area to drop spacecraft at the end of their lives.</p>
       """,
       'Nine real places that sound invented: a town inside one building, a 60-year coal fire, a boiling river, and land that no country will claim.'),

    # ==================================================================
    _a('experiments-that-are-still-running',
       'Seven Experiments That Have Been Running for Over Fifty Years',
       STRANGE,
       'A bell that has rung since 1840, a tar drip that has produced nine drops since 1927, and a seed study whose jars are dug up by scientists who were not born when it started.',
       '/static/img/articles/long-experiments.svg',
       """
<p>Science usually works in grant cycles of three years. These do not.</p>

<h3>The Oxford Electric Bell — since 1840</h3>
<p>A small brass bell in a laboratory at Oxford has been ringing roughly twice a second since about 1840, driven by two dry piles whose exact composition nobody knows, because opening them to find out would end the experiment. It sits under two glass domes, largely so people can get on with their work. It has rung an estimated ten billion times.</p>

<h3>Beal's seed viability experiment — since 1879</h3>
<p>William Beal buried 20 bottles of seed on the Michigan State campus, each holding 50 seeds of 23 species, to find out how long they stayed able to germinate. One bottle is dug up on a schedule and planted. The experiment has outlived Beal by more than a century, and in the 2021 dig moth mullein still came up — from seed buried before the invention of the aeroplane.</p>

<h3>The Rothamsted Park Grass Experiment — since 1856</h3>
<p>A field in Hertfordshire has been divided into strips, each given a different fertiliser treatment every year since 1856. It has quietly become the longest-running ecological experiment in the world, and because the samples were archived, researchers can measure things nobody in 1856 had heard of — including nitrogen pollution and the effect of acid rain.</p>

<h3>The pitch drop — since 1927</h3>
<p>Professor Thomas Parnell poured hot pitch into a funnel at the University of Queensland to show students that something that shatters like glass when you hit it is actually a very slow liquid. He let it settle for three years, then cut the stem in 1930. A drop falls about once a decade. Nine have fallen. No one has ever seen one land — the custodian who watched it for 52 years missed all of them, including one he lost to a camera malfunction in 2000.</p>

<h3>The Framingham Heart Study — since 1948</h3>
<p>Over 5,000 adults in Framingham, Massachusetts, agreed to be examined every couple of years for life. Their children joined in 1971, their grandchildren in 2002. Almost everything the public hears about heart disease — that smoking, blood pressure and cholesterol matter, and roughly how much — traces back to this one town.</p>

<h3>The Harvard Study of Adult Development — since 1938</h3>
<p>Two groups of young men, one from Harvard and one from poor districts of Boston, have been followed ever since, through careers, marriages, drink and illness. Its most-quoted finding is unfashionably simple: the strength of someone's relationships at 50 predicted their health at 80 better than their cholesterol did.</p>

<h3>The Keeling curve — since 1958</h3>
<p>Charles David Keeling began measuring carbon dioxide at Mauna Loa in Hawaii in 1958, and the instruments have not stopped. The resulting graph — a rising line with an annual zigzag as the northern hemisphere's plants breathe in and out — is probably the most consequential single dataset in science. It started at 315 parts per million.</p>
       """,
       'Seven scientific experiments running for 50 years or more, from the Oxford Electric Bell of 1840 to the pitch drop that has produced nine drops since 1927.'),

    # ==================================================================
    _a('things-older-than-you-think',
       'Nine Things That Are Much Older Than You Think',
       STRANGE,
       'Sharks are older than trees, Oxford was teaching before the Aztecs existed, and the fax machine was patented before the telephone. A list that quietly rearranges history.',
       '/static/img/articles/older-than-you-think.svg',
       """
<p>Most of these are true for the same reason: we file history by story rather than by date, and the stories are not in order.</p>

<h3>1. Sharks are older than trees</h3>
<p>Sharks appear in the fossil record about 450 million years ago. The first things we would call trees arrived about 385 million years ago. Sharks have been swimming for over 60 million years longer than anything has had a trunk.</p>

<h3>2. Oxford was teaching before the Aztec Empire existed</h3>
<p>There is evidence of teaching at Oxford from 1096. Tenochtitlan, the Aztec capital, was founded in 1325. By the time the Aztecs laid their first stone, Oxford had been handing out degrees for two centuries.</p>

<h3>3. Cleopatra lived closer to us than to the pyramids</h3>
<p>The Great Pyramid was finished around 2560 BC. Cleopatra died in 30 BC — about 2,530 years later. From her death to the Moon landing is roughly 2,000 years. She was closer in time to Apollo 11 than to the pyramid she could see from her own country.</p>

<h3>4. T. rex is closer to us than to Stegosaurus</h3>
<p>Stegosaurus died out around 150 million years ago. Tyrannosaurus appeared about 68 million years ago. The gap between the two famous dinosaurs is bigger than the gap between T. rex and us, which is why the two never met and every toy box lies to you.</p>

<h3>5. The fax machine came before the telephone</h3>
<p>Alexander Bain patented a working facsimile device in 1843. Alexander Graham Bell patented the telephone in 1876. A commercial fax line ran between Paris and Lyon from 1865, eleven years before anyone could ring anyone up.</p>

<h3>6. Woolly mammoths were still alive when the pyramids were built</h3>
<p>Mainland mammoths died out around 10,000 years ago, but a population survived on Wrangel Island in the Arctic Ocean until roughly 4,000 years ago. The Great Pyramid was already standing, and Egypt was already an old country.</p>

<h3>7. France was still using the guillotine when Star Wars was in cinemas</h3>
<p>Star Wars opened in May 1977. France carried out its last execution by guillotine in September of the same year, and only abolished the death penalty in 1981.</p>

<h3>8. Nintendo is older than sliced bread</h3>
<p>Nintendo was founded in 1889, making playing cards in Kyoto. Commercially sliced bread went on sale in 1928. The company behind Mario predates the loaf by nearly forty years.</p>

<h3>9. Harvard was founded before calculus</h3>
<p>Harvard was established in 1636. Newton and Leibniz developed calculus independently in the 1660s and 1670s. America's oldest university is older than the maths every one of its engineering students now has to pass.</p>
       """,
       'Nine things that are far older than people assume, from sharks predating trees to the fax machine being patented 33 years before the telephone.'),

    # ==================================================================
    _a('weirdest-weather-on-record',
       'The Weirdest Weather Ever Recorded',
       STRANGE,
       'Lightning that strikes the same lake 300 nights a year, fish that fall out of the sky on schedule, red rain, and snow in the Sahara.',
       '/static/img/articles/strange-weather.jpg',
       """
<p>Weather records are kept carefully, which is what makes the strange ones strange: they are measured, not reported third-hand.</p>

<h3>Lightning on a timetable</h3>
<p>Where the Catatumbo river meets Lake Maracaibo in Venezuela, storms form on up to around 300 nights a year and can produce hundreds of flashes an hour, for nine or ten hours at a stretch. Sailors used it to navigate. It is the most reliable lightning on the planet, and it goes off at night almost on cue.</p>

<h3>Raining fish, every year, in the same town</h3>
<p>Yoro in Honduras holds a festival called the Lluvia de Peces — the rain of fish. After a heavy early-summer storm, small fish are found on the ground away from the river. The usual explanation is a waterspout picking them up, though some researchers think they are driven up out of underground water instead. Either way the town has been celebrating it since the 1800s.</p>

<h3>Red rain</h3>
<p>Dust lifted from the Sahara rides high into the atmosphere and falls on southern Europe mixed with rain, leaving cars and windows orange-brown. It reaches Britain several times a decade. Before anyone understood it, blood rain was read as an omen, and it is in the chronicles as one.</p>

<h3>Snow in the Sahara</h3>
<p>Ain Sefra in Algeria, at the desert's northern edge, has had settling snow several times — in 1979, and again in 2016, 2018 and since. Red dunes under a white dusting is one of the odder photographs the weather produces.</p>

<h3>The hottest and coldest readings</h3>
<p>The official record high is 56.7°C at Furnace Creek in Death Valley, set in 1913, and still argued over by climatologists. The record low is −89.2°C at the Soviet Vostok station in Antarctica in 1983. The coldest permanently inhabited place is Oymyakon in Siberia, which has dropped near −68°C — cold enough that cars are left running all day.</p>

<h3>Hail the size of a football</h3>
<p>A hailstone that fell at Vivian, South Dakota, in 2010 measured 8 inches across and weighed nearly two pounds. It is the largest ever officially measured in the United States, and it left a crater in the ground.</p>

<h3>Fire whirls</h3>
<p>A big enough fire makes its own weather. When the rising column of hot air starts to spin it can form a rotating pillar of flame tens of metres high. One of the worst recorded came after the 1923 Great Kanto earthquake in Japan, where a fire whirl killed thousands of people sheltering in an open yard.</p>

<h3>The quietest killer</h3>
<p>Britain's strangest weather event was not dramatic at all. In December 1952 cold, still air trapped coal smoke over London for four days. The Great Smog was thick enough to stop buses and get into cinemas, and it is now estimated to have killed at least 4,000 people and probably far more. It produced the Clean Air Act of 1956.</p>
       """,
       'The strangest weather on record, from the Catatumbo lightning and Honduras raining fish to Saharan snow, red rain and an 8-inch hailstone.'),

    # ==================================================================
    _a('animals-that-break-the-rules',
       'Eight Animals That Break the Rules of Biology',
       STRANGE,
       'A shark that may live 400 years, a frog that freezes solid, a mammal that barely ages, and a fish that can fill a bucket with slime in seconds.',
       '/static/img/articles/rule-breaking-animals.jpg',
       """
<p>Biology has some firm expectations — that animals age, that vertebrates need a backbone, that freezing kills. These eight ignore at least one of them.</p>

<h3>1. The Greenland shark, which may reach 400</h3>
<p>Radiocarbon dating of the lenses of their eyes put one Greenland shark at somewhere around 400 years old, and the method suggests they do not reach breeding age until about 150. The oldest individuals alive now were swimming before Newton published.</p>

<h3>2. The naked mole rat, which barely ages</h3>
<p>Nearly everything's chance of dying rises steeply with age. The naked mole rat's does not seem to, which breaks a rule thought to apply to all mammals. They also get cancer vanishingly rarely, survive with almost no oxygen for long stretches, and feel no pain from acid or chilli.</p>

<h3>3. The axolotl, which regrows limbs and never grows up</h3>
<p>Axolotls regrow legs, tails, jaws, parts of the eye and even parts of the brain, without scarring. They also never leave their larval form — they keep their feathery gills and stay in the water for life, breeding as what is effectively an overgrown tadpole.</p>

<h3>4. The wood frog, which freezes solid</h3>
<p>Through an Alaskan winter a wood frog can let roughly two-thirds of its body water turn to ice. Its heart stops, its breathing stops, its brain activity stops. It floods its cells with glucose as antifreeze, and in spring it thaws and hops off.</p>

<h3>5. The hagfish, which has a skull but no backbone</h3>
<p>Hagfish have a skull and no vertebrae, which puts them awkwardly at the root of the vertebrate family tree. Threatened, they release a protein that turns litres of seawater into slime in seconds — enough to choke a shark's gills and make it let go.</p>

<h3>6. Bdelloid rotifers, which gave up sex millions of years ago</h3>
<p>These microscopic animals appear to have reproduced without males for tens of millions of years, which theory says should be a dead end. They also dry out completely and come back, and in 2021 Russian researchers revived individuals from Siberian permafrost dated to around 24,000 years old.</p>

<h3>7. The horned lizard, which squirts blood from its eyes</h3>
<p>Cornered by a coyote or a fox, some horned lizards raise the blood pressure around their eyes until vessels burst and fire a jet of blood up to a metre or so. It tastes foul to canines, which is the point.</p>

<h3>8. The platypus, which breaks four rules at once</h3>
<p>It is a mammal that lays eggs. It has no stomach to speak of. The male has a venomous spur on its hind leg, painful enough that morphine is reportedly little help. And it hunts with its eyes shut, finding prey by the faint electrical signals of their muscles. When the first specimen reached London, scientists assumed it was a hoax stitched together from other animals.</p>

<p>For more of this sort of thing, see <a href="/posts/animal-facts-that-sound-made-up">twelve animal facts that sound completely made up</a>.</p>
       """,
       'Eight animals that break biological rules: the 400-year-old Greenland shark, the barely-ageing naked mole rat, the freezing wood frog and the platypus.'),

    # ==================================================================
    _a('strangest-moments-in-sport',
       'Eight of the Strangest Things That Have Happened in Sport',
       STRANGE,
       'A swimmer who had never seen an Olympic pool, a horse that collapsed yards from winning, a race that never happened, and the longest tennis match in history.',
       '/static/img/articles/strange-sport.jpg',
       """
<p>Sport is written up as drama, and the oddest moments are the ones no script would allow.</p>

<h3>1. Eric the Eel</h3>
<p>Eric Moussambani of Equatorial Guinea qualified for the Sydney 2000 Olympics through a development place, having learned to swim eight months earlier in a 20-metre hotel pool. Both his rivals in the 100m freestyle heat false-started and were disqualified, so he swam alone. He finished in 1:52.72 — more than a minute outside the winning time — and the crowd stood up for him. He had never swum 100 metres before.</p>

<h3>2. Devon Loch</h3>
<p>In the 1956 Grand National the Queen Mother's horse Devon Loch was clear and 40 yards from the line when he half-jumped at nothing and collapsed on the flat. His jockey, Dick Francis, never satisfactorily explained it and went on to write thrillers instead. The race was won by ESB.</p>

<h3>3. The Grand National that was declared void</h3>
<p>In 1993 two false starts left the tape wrapped round several jockeys. Thirty of the 39 riders set off anyway, having not realised. Seven completed the course. The race was voided, bets were returned, and John White's winning ride counted for nothing.</p>

<h3>4. Eleven hours of tennis</h3>
<p>At Wimbledon in 2010 John Isner beat Nicolas Mahut 70–68 in the fifth set, over 11 hours and 5 minutes across three days. The scoreboard stopped working. The final set alone lasted longer than any previous complete match, and the rules were later changed so it could not happen again.</p>

<h3>5. Dorando Pietri's finish</h3>
<p>Leading the 1908 Olympic marathon in London, Pietri entered the stadium badly disorientated, turned the wrong way and fell five times in the last 400 metres. Officials helped him over the line, which got him disqualified. Queen Alexandra had a gilded cup made for him anyway.</p>

<h3>6. The gold medal won by last place</h3>
<p>In the 1,000m short-track final at the 2002 Winter Olympics, Australia's Steven Bradbury was a distant fifth of five with half a lap to go. The four skaters ahead of him collided and went down. He crossed alone for Australia's first ever Winter Olympic gold, and said afterwards he would accept it for the previous decade rather than for the race.</p>

<h3>7. Two goals in four minutes, one with a hand</h3>
<p>In the 1986 World Cup quarter-final, Diego Maradona punched Argentina's first goal past Peter Shilton and got away with it. Four minutes later he beat half the England team over 60 metres to score what was voted the goal of the century. The same player produced the most cynical and the most brilliant goal of the tournament in the same afternoon.</p>

<h3>8. Beamon's jump</h3>
<p>At the 1968 Mexico City Olympics, Bob Beamon jumped 8.90m and broke the world long jump record by 55 centimetres — an improvement so large the officials' optical measuring device would not reach, and they had to fetch a tape. The record stood for 23 years, and Beamon's best jump for the rest of his career was almost a foot shorter.</p>
       """,
       'Eight of the strangest moments in sport, from Eric the Eel and Devon Loch to the void 1993 Grand National and the 11-hour Isner-Mahut match.'),

    # ==================================================================
    _a('maths-that-feels-wrong',
       'Five Bits of Maths That Feel Wrong But Are Not',
       FACT,
       'Why 23 people in a room is enough for a shared birthday, why you should always swap doors, and why folding paper 42 times would reach the Moon.',
       '/static/img/articles/maths-paradox.svg',
       """
<p>None of these is a trick. They are all straightforwardly true, and all of them feel like a con the first time you meet them.</p>

<h3>1. Twenty-three people is enough for a shared birthday</h3>
<p>With 23 people in a room, there is a better than even chance that two of them share a birthday. With 50 it is about 97%. It feels wrong because you picture <em>your</em> birthday against 22 others. The maths is counting pairs, and 23 people make 253 pairs. In a Premier League squad, a shared birthday is the likely outcome, not the coincidence.</p>

<h3>2. You should always swap doors</h3>
<p>Three doors, a car behind one, goats behind the other two. You pick a door. The host, who knows where the car is, opens a different door to show a goat, and offers you the swap. Swapping wins two times in three.</p>
<p>The reason is that the host's choice is not random. Your first pick is right one time in three, and in the other two cases the host is forced to show you the only remaining goat, so the car is behind the door he did not open. The puzzle generated sacks of angry letters from mathematicians when it was published in 1990, and they were wrong.</p>

<h3>3. A chessboard of rice would bury the country</h3>
<p>One grain on the first square, two on the second, doubling each time. By square 64 you need 2<sup>63</sup> grains, and the total for the board is about 18.4 quintillion — some two thousand times the world's annual rice harvest. The old story has the inventor of chess asking an emperor for exactly this and the emperor agreeing before doing the sums.</p>

<h3>4. Forty-two folds reaches the Moon</h3>
<p>A sheet of paper is about a tenth of a millimetre thick. Each fold doubles it. Ten folds is roughly the height of a person; 23 folds passes a kilometre; 42 folds is around 440,000 km, past the Moon. You cannot actually do it — the record is 13 folds, set by a class of American students with a very long roll of toilet paper — but the arithmetic holds.</p>

<h3>5. An infinite hotel always has room</h3>
<p>Imagine a hotel with infinitely many rooms, all full. A guest arrives. Move the guest in room 1 to room 2, room 2 to room 3, and so on for ever: room 1 is now free. An infinite coachload arrives. Move everyone to double their room number, and every odd-numbered room is free. Hilbert's hotel is the clearest demonstration that infinity is not a very big number and does not behave like one.</p>

<p>If you want the practical version of this, our piece on <a href="/posts/memory-tricks-that-work-for-trivia">memory tricks that actually work</a> covers the same ground for quiz night.</p>
       """,
       'Five mathematical results that feel wrong and are not: the birthday problem, the Monty Hall problem, doubling rice on a chessboard, paper folding and Hilbert’s hotel.'),

    # ==================================================================
    _a('what-everyday-objects-are-for',
       'What Those Bits of Everyday Objects Are Actually For',
       FACT,
       'The hole in a pen lid, the tiny extra pocket on your jeans, the ridges on the edge of a coin, and the arrow next to your fuel gauge.',
       '/static/img/articles/everyday-objects.svg',
       """
<p>Designers rarely add anything for nothing. Here is what the odd bits are doing.</p>

<h3>The hole in a biro lid</h3>
<p>Partly to stop pressure building up and leaking ink, but mainly safety. Pen lids are a classic choking hazard for children, and the hole means that one lodged in a windpipe still lets air through. BIC has said explicitly that this is why it is there.</p>

<h3>The tiny fifth pocket on jeans</h3>
<p>It is a watch pocket. Levi's jeans from the 1870s were workwear, and a working man's watch was a pocket watch on a chain. Wristwatches took over after the First World War; the pocket stayed because the pattern did.</p>

<h3>The ridges on the edge of coins</h3>
<p>When coins were made of silver and gold, people shaved slivers off the edges and kept the metal — "clipping". Milled edges made it obvious. Isaac Newton, as Warden of the Royal Mint, pushed the recoining that stamped it out. The ridges survive on the 5p, 10p, 20p and 50p, and also help people who cannot see them tell one from another.</p>

<h3>The arrow next to the fuel pump symbol</h3>
<p>It tells you which side of the car the filler cap is on. Useful in a hire car, and worth knowing before you pull up at the wrong pump.</p>

<h3>The loop on the back of a dress shirt</h3>
<p>Called a locker loop. It comes from American navy uniform, so a sailor could hang a shirt up without a hanger, and was picked up by Ivy League students in the 1960s — who gave it a second life as a signal, since having yours torn off meant something about your relationship status.</p>

<h3>The little plastic table in a pizza box</h3>
<p>It keeps the lid off the cheese. It was patented in 1983 by Carmela Vitale and is formally a "package saver".</p>

<h3>The hole in a pasta spoon</h3>
<p>Two jobs. It lets water drain, and on many spoons it is sized to hold roughly a single portion of dry spaghetti.</p>

<h3>The blue side of an eraser</h3>
<p>Not for ink, whatever you were told at school. It is a coarser, grittier rubber meant for thick paper and heavier pencil marks — and on thin paper it mostly makes a hole.</p>

<h3>The 57 on a Heinz bottle</h3>
<p>Tap the raised 57 on the neck of a glass ketchup bottle and the sauce comes out. The number itself was invented — Henry Heinz liked the look of it and the company was already selling more than 60 products.</p>
       """,
       'What the odd details on everyday objects are for, from the hole in a pen lid and the fifth jeans pocket to the ridges on coins and the arrow by the fuel gauge.'),

    # ==================================================================
    _a('the-deep-sea-in-numbers',
       'The Deep Sea in Numbers',
       FACT,
       'How deep the deepest trench goes, what the pressure does down there, how much of the ocean we have actually mapped, and why most of the animals glow.',
       '/static/img/articles/deep-sea.jpg',
       """
<p>The ocean covers about 71% of the planet and averages 3,700 metres deep. Almost all of it is dark, cold and under enormous pressure, and we know less about it than about the surface of Mars.</p>

<h3>The numbers</h3>
<table>
<tr><th>Thing</th><th>Figure</th></tr>
<tr><td>Deepest known point (Challenger Deep, Mariana Trench)</td><td>about 10,935 m</td></tr>
<tr><td>Everest, for comparison</td><td>8,849 m</td></tr>
<tr><td>Pressure at the bottom of Challenger Deep</td><td>over 1,000 atmospheres</td></tr>
<tr><td>Depth sunlight effectively runs out</td><td>about 200 m</td></tr>
<tr><td>Depth no sunlight reaches at all</td><td>about 1,000 m</td></tr>
<tr><td>Average ocean depth</td><td>about 3,700 m</td></tr>
<tr><td>Seafloor mapped in modern detail</td><td>roughly a quarter</td></tr>
<tr><td>Deep-sea animals that produce their own light</td><td>around three quarters</td></tr>
</table>

<h3>What the pressure means</h3>
<p>At the bottom of the Mariana Trench the pressure is more than a thousand times what you feel at sea level — roughly the weight of a large car pressing on every square centimetre. Submersibles that go there have hulls of titanium or thick acrylic, and the acrylic viewports visibly compress on the way down.</p>

<h3>Why nearly everything glows</h3>
<p>Below a few hundred metres, light is not something you receive, it is something you make. An estimated three quarters of deep-sea animals are bioluminescent, using it to lure prey, confuse predators, signal to mates or produce a cloud of light and swim away from it. Most of it is blue, because blue travels furthest through seawater.</p>

<h3>The zones</h3>
<ul>
<li><strong>Sunlight zone</strong> (0–200 m) — where almost all photosynthesis happens.</li>
<li><strong>Twilight zone</strong> (200–1,000 m) — enough light to see a silhouette, not enough to grow. Home to the biggest daily animal migration on Earth, as billions of creatures rise at dusk and sink at dawn.</li>
<li><strong>Midnight zone</strong> (1,000–4,000 m) — no light at all, near freezing.</li>
<li><strong>Abyss</strong> (4,000–6,000 m) — most of the deep seafloor.</li>
<li><strong>Trenches</strong> (6,000 m+) — the hadal zone, named after Hades, and only a tiny fraction of the ocean floor.</li>
</ul>

<h3>How little we have seen</h3>
<p>Three people have been to the bottom of Challenger Deep by the old count, and a few dozen now that tourist submersibles reach it; twelve have walked on the Moon. Only around a quarter of the seafloor has been mapped at modern resolution, and new species turn up on almost every deep research cruise.</p>
       """,
       'The deep sea in numbers: the depth of Challenger Deep, the pressure down there, how much seafloor is mapped, and why most deep-sea animals glow.'),

    # ==================================================================
    _a('space-facts-that-sound-impossible',
       'Nine Facts About Space That Sound Impossible',
       FACT,
       'A planet where a day lasts longer than a year, a mountain three times the height of Everest, and a spoonful of star that weighs as much as a mountain range.',
       '/static/img/articles/space-impossible.svg',
       """
<p>Space does not do moderate. Every one of these is standard astronomy.</p>

<h3>1. A day on Venus is longer than its year</h3>
<p>Venus turns so slowly that one rotation takes about 243 Earth days, while a trip round the Sun takes about 225. It also spins backwards compared with almost everything else in the solar system, so on Venus the Sun would rise in the west.</p>

<h3>2. Saturn would float</h3>
<p>Saturn's average density is about 0.69 grams per cubic centimetre, less than water. If you had a bath big enough, it would bob. It is also the least dense planet in the solar system by a wide margin.</p>

<h3>3. A teaspoon of neutron star weighs about a billion tonnes</h3>
<p>When a massive star collapses, its core can be crushed until a mass greater than the Sun's fits inside a sphere the size of a city. The material is so dense that a sugar-cube-sized piece would outweigh Mount Everest.</p>

<h3>4. Olympus Mons is nearly three times the height of Everest</h3>
<p>Mars has the tallest volcano in the solar system at about 22 km high and roughly the width of France. Its slopes are so gentle that standing on it you would not know you were on a mountain — the summit is beyond the horizon.</p>

<h3>5. There are more trees on Earth than stars in the Milky Way</h3>
<p>The galaxy holds somewhere between 100 and 400 billion stars. Earth has an estimated three trillion trees. There are, however, far more stars in the observable universe than grains of sand on Earth.</p>

<h3>6. It rains glass, sideways, on HD 189733 b</h3>
<p>This gas giant 64 light years away has an atmosphere thought to be full of silicate particles, a temperature over 900°C and winds around 7,000 km/h. The result, as far as the models go, is molten glass blowing horizontally.</p>

<h3>7. The Moon is drifting away</h3>
<p>Laser reflectors left by the Apollo missions let us measure it precisely: the Moon recedes by about 3.8 cm a year. Hundreds of millions of years from now, total solar eclipses will no longer be possible, because the Moon will be too small in the sky to cover the Sun.</p>

<h3>8. Space smells of something</h3>
<p>Astronauts returning from spacewalks consistently report a smell on their suits and tools — seared steak, hot metal, welding fumes. The leading suspect is atomic oxygen reacting on the surfaces, plus the by-products of broken molecules out there.</p>

<h3>9. There is a hole in the universe with almost nothing in it</h3>
<p>The Boötes void is a roughly spherical region about 330 million light years across containing only a few dozen known galaxies, where it should hold thousands. As the astronomer Greg Aldering put it, if the Milky Way had been in the middle of it we would not have known there were other galaxies until the 1960s.</p>

<p>Related: <a href="/posts/why-pluto-stopped-being-a-planet">why Pluto stopped being a planet</a>.</p>
       """,
       'Nine true facts about space that sound impossible, from a Venusian day longer than its year to neutron stars, Olympus Mons and the Boötes void.'),

    # ==================================================================
    _a('your-senses-are-lying-to-you',
       'Six Ways Your Senses Are Quietly Lying to You',
       FACT,
       'There is a hole in your vision you never notice, your eyes go blind every time they move, and what you hear changes depending on what you are looking at.',
       '/static/img/articles/senses.svg',
       """
<p>Perception is not a recording. It is a running reconstruction, and the gaps get filled in without telling you.</p>

<h3>1. You have a blind spot in each eye</h3>
<p>Where the optic nerve leaves the retina there are no light receptors at all, which means a patch of each eye's view is simply missing. You never see it, because the brain paints over it using the surrounding pattern. Close one eye, hold a finger out to the side and move it slowly across your view and you can find the point where it vanishes.</p>

<h3>2. You go blind every time you move your eyes</h3>
<p>Your eyes dart between fixed points several times a second, and during each dart the visual input is a smear. The brain discards it — saccadic masking — and stitches the stable images together, stretching the last one backwards to cover the gap. You lose a surprising fraction of your waking vision this way and never notice a flicker.</p>

<h3>3. What you see changes what you hear</h3>
<p>Play the sound "ba" over a video of someone mouthing "fa" and most people hear "fa". This is the McGurk effect, and knowing about it does not switch it off. Hearing is not a separate channel; it is merged with vision before you get a say.</p>

<h3>4. You cannot tickle yourself</h3>
<p>The cerebellum predicts the sensory consequences of your own movements and damps down the result, which is how you tell your own touch from someone else's. Tickling needs the surprise. The only reliable way round it is a mirror, a delay or someone else's hand.</p>

<h3>5. The tongue map is nonsense</h3>
<p>The diagram with sweet at the front and bitter at the back comes from a mistranslated German paper from 1901 and has been in textbooks ever since. All five basic tastes are detectable across the whole tongue. There are five, incidentally — sweet, sour, salty, bitter and umami, the last only accepted in the West in the 1980s.</p>

<h3>6. Most of what you "see" is memory and guesswork</h3>
<p>Only a small central patch of your vision is sharp — about the width of your thumbnail at arm's length. Everything else is low resolution and largely colour-blind at the edges, and the detailed world you experience is assembled from the last few glances. This is why change blindness works: in the classic experiments, people fail to notice the person they are talking to being swapped for someone else.</p>
       """,
       'Six ways human senses mislead us: the retinal blind spot, saccadic masking, the McGurk effect, self-tickling, the tongue map myth and change blindness.'),

    # ==================================================================
    _a('how-long-things-really-take',
       'How Long Things Really Take',
       FACT,
       'Sunlight takes eight minutes to reach you but thousands of years to escape the Sun, and a plastic bottle outlasts everyone who has ever drunk from it.',
       '/static/img/articles/how-long.svg',
       """
<p>Some of these are much shorter than people guess, and some are much longer.</p>

<h3>Light and distance</h3>
<table>
<tr><th>Journey</th><th>Time</th></tr>
<tr><td>Sun to Earth, as light</td><td>8 minutes 20 seconds</td></tr>
<tr><td>Sun's core to its surface, as energy</td><td>tens of thousands of years</td></tr>
<tr><td>Earth to the Moon, as light</td><td>1.3 seconds</td></tr>
<tr><td>Earth to Mars, as a radio signal</td><td>3 to 22 minutes</td></tr>
<tr><td>Nearest star (Proxima Centauri), as light</td><td>4.2 years</td></tr>
<tr><td>Voyager 1 to the nearest star, at its current speed</td><td>about 70,000 years</td></tr>
</table>
<p>The second row is the surprising one. A photon leaving the Sun's core is absorbed and re-emitted so many times that the energy takes an age to work its way out — and then crosses 93 million miles of empty space in eight minutes.</p>

<h3>Around the solar system</h3>
<ul>
<li>A day on Jupiter: about 10 hours. It is the largest planet and the fastest spinning.</li>
<li>A year on Neptune: about 165 Earth years. It has completed one orbit since its discovery in 1846.</li>
<li>A day on Mercury: about 59 Earth days.</li>
</ul>

<h3>Things on Earth</h3>
<ul>
<li>A red blood cell makes a full circuit of your body in about 60 seconds.</li>
<li>Hair grows roughly 1.25 cm a month, so a shoulder-length head of hair is two or three years old at the ends.</li>
<li>A human fingernail takes about six months to grow out from base to tip; a toenail takes 12 to 18.</li>
<li>Your skeleton replaces itself gradually; the adult skeleton turns over roughly every ten years.</li>
<li>A banana skin composts in a few weeks. A plastic bottle is estimated at around 450 years, and a glass bottle has no realistic figure at all.</li>
<li>A sneeze leaves at around 100 mph; a cough at about 50.</li>
</ul>

<h3>Long odds on long times</h3>
<ul>
<li>Coal that fuelled the Industrial Revolution formed around 300 million years ago, which is why the period is called the Carboniferous.</li>
<li>The helium in a party balloon was made in stars, apart from the primordial fraction that has been around since minutes after the Big Bang.</li>
<li>The gold in a wedding ring was almost certainly forged in a neutron star collision, and is older than the solar system.</li>
</ul>
       """,
       'How long things really take, from eight minutes of sunlight to the tens of thousands of years energy spends escaping the Sun and 450 years for a plastic bottle.'),

    # ==================================================================
    _a('food-facts-worth-knowing',
       'Twelve Food Facts Worth Knowing',
       FACT,
       'Carrots were purple, bananas are mildly radioactive, almonds are not nuts, and the most expensive spice in the world is picked by hand one thread at a time.',
       '/static/img/articles/food-facts.jpg',
       """
<p>Food is the richest seam in quizzing, because everyone has an opinion and almost nobody has checked.</p>

<h3>1. Carrots were not originally orange</h3>
<p>Early cultivated carrots were purple, white or yellow. The orange carrot was developed in the Netherlands, and while the story that it was bred as a tribute to William of Orange is probably a later embellishment, the Dutch origin is not.</p>

<h3>2. Bananas are slightly radioactive</h3>
<p>Bananas are rich in potassium, and a small fraction of all natural potassium is the radioactive isotope potassium-40. The dose is trivial — physicists use the "banana equivalent dose" as a joke unit — but it is real, and a lorryload of bananas can trip a radiation sensor at a port.</p>

<h3>3. Almonds, cashews and walnuts are not nuts</h3>
<p>Botanically, a nut is a hard dry fruit that does not split open — a hazelnut or an acorn. Almonds and cashews are seeds of drupes, like plums. Peanuts are legumes, closer to peas. Walnuts and pecans are drupes too.</p>

<h3>4. A tomato is a fruit, and legally a vegetable</h3>
<p>Botanically a berry. In 1893 the US Supreme Court ruled in <em>Nix v. Hedden</em> that for the purposes of import tariffs the tomato counted as a vegetable, because that is how people eat it. Both answers are correct, depending on who is asking.</p>

<h3>5. Honey never spoils</h3>
<p>Sealed honey keeps indefinitely — low water, high acidity and a trace of hydrogen peroxide leave nothing for microbes to live on. Pots found in Egyptian tombs were still honey. We have <a href="/posts/why-honey-never-goes-off">a whole piece on why</a>.</p>

<h3>6. Saffron is the most expensive spice by weight</h3>
<p>Each thread is one of three stigmas inside a crocus flower, picked by hand on the morning it opens. It takes something like 150,000 flowers to produce a kilogram, which is why it is priced like a precious metal.</p>

<h3>7. Pineapples take two years</h3>
<p>A pineapple plant takes around two to three years to produce its first fruit, and the fruit is a cluster of dozens of individual flowers fused together. The pattern of diamonds on the skin is the map of them.</p>

<h3>8. Chocolate was a drink for most of its history</h3>
<p>Cacao was drunk, usually bitter and spiced, for some 3,000 years before anyone made a bar. Solid eating chocolate dates from the 1840s, once a press existed that could separate cocoa butter from the solids.</p>

<h3>9. Worcestershire sauce contains fermented anchovies</h3>
<p>Which makes it one of the many things vegetarians discover late. The recipe descends from a Roman-style fermented fish sauce, and the anchovies are left to break down for months.</p>

<h3>10. Nutmeg is dangerous in quantity</h3>
<p>Nutmeg contains myristicin, and a couple of whole nutmegs is enough to cause genuine poisoning — nausea, racing heart, hallucinations lasting a day or more. In baking quantities it is entirely safe.</p>

<h3>11. Vanilla is the second most expensive spice</h3>
<p>Vanilla comes from an orchid whose flowers open for less than a day and, outside Mexico, have no natural pollinator. Every pod in commercial production is pollinated by hand, a technique worked out in 1841 by a twelve-year-old enslaved boy on Réunion, Edmond Albius.</p>

<h3>12. Peppers are hot by accident of chemistry</h3>
<p>Capsaicin binds to the receptor that detects actual heat, so the brain is told the mouth is burning. Birds lack that sensitivity, which is the point: the plant wants birds to spread its seeds and mammals to leave it alone. Milk helps because capsaicin dissolves in fat, and water does not.</p>

<p>More in this line: <a href="/posts/foods-not-from-where-you-think">nine foods that are not from where you think</a>.</p>
       """,
       'Twelve food facts worth knowing, from purple carrots and mildly radioactive bananas to why almonds are not nuts and saffron costs what it does.'),

]
