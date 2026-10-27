"""Regenerate the mini-game lexicon from the trivia question bank.

The word games (Boggle, Word Chain, Word Wheel, Word Ladder) need a dictionary
to check guesses against. Rather than ship a third-party word list, we harvest
one from our own 3,400+ questions: every alphabetic token of 3-9 letters that
turns up at least twice. That gives a few thousand real, topical English words
including the proper nouns a trivia audience expects to be allowed.

Run it from the project root whenever the question bank grows a lot:

    python -m app.utils.build_lexicon
"""
import collections
import json
import os
import re

# Everyday words a quiz-question corpus happens to be thin on, so short-word
# games do not reject obvious guesses.
SUPPLEMENT = """
able ache acid aged aide ails aims airs ajar akin ales alms aloe amid amps ands
ants apes apex arch arcs arid arms army arts ashy atom aunt aura auto avid away
awry axes axis babe bade bags bail bait bake bald bale balm band bane bang bank
bard bare barn base bash bask bass bath bats bead beak beam bean bear beat beds
beef been beer bees beet bell belt bend bent best bide bids bike bile bill bind
bins bird bite bits blab bled blew blip blob blot blow blue blur boar boat bode
body boil bold bolt bomb bond bone bony book boom boon boot bore born both bout
bowl bows brag bran bray brew brig brim brow buck buds buff bugs bulb bulk bull
bump bunk buns bunt buoy burn burp bury bush bust busy buzz cabs cage cake calf
call calm came camp cane cans cape caps card care cart case cash cask cast cats
cave cedar cell cent chap char chat chew chin chip chop chug cite city clad clam
clan clap claw clay clip clod clog clot club clue coal coat coax code coil coin
coke cold colt comb come cone cook cool coop cope cops copy cord core cork corn
cost cosy cots coup cove cowl cows cozy crab crag cram crew crib crop crow cubs
cues cuff cull cult cups curb curd cure curl curt cusp cute cuts cyst dabs dado
daft dale dame damp dams dare dark darn dart dash date dawn days daze dead deaf
deal dean dear debt deck deed deem deep deer dell dens dent deny desk dial dice
dies diet digs dill dime dims dine ding dins dint dips dire dirt disc dish disk
dive dock does dole doll dolt dome done doom door dope dose dote dots dour dove
down doze drab drag dram drat draw drew drip drop drum dual duck duct dude duel
dues duet duke dull duly dumb dump dune dung dunk dusk dust duty dyes dyke each
earl earn ears ease east easy eats ebbs echo eddy edge edgy edit eels eggs egos
elks ells elms else emit ends envy epic eras errs etch even ever ewes exam exit
eyed eyes face fact fade fads fail fain fair fake fall fame fang fans fare farm
fast fate fats fawn faze fear feat feed feel fees feet fell felt fend fern feud
figs file fill film find fine fins fire firm fish fist fits five fizz flag flak
flan flap flat flaw flax flea fled flee flew flex flip flit floe flog flop flow
flue flux foal foam foes fogs foil fold folk fond font food fool foot fora force
ford fore fork form fort foul four fowl foxy frail frame fray free fret frog
from fuel full fume fund fungi funny furl fury fuse fuss fuzz gain gait gale
gall game gang gaps gape garb gash gasp gate gaunt gave gawk gaze gear geese
gems gene gent germ gift gigs gild gill gilt gird girl gist give glad glee glen
glib glow glue glum glut gnarl gnat goad goal goat gods goes gold golf gone gong
good goof gore gory gosh gout gown grab grad graft grain gram grand grape grasp
grass grave gray graze grew grey grid grim grin grip grit grope grow grub gulf
gull gulp gums gush gust guts guys gyms hack hail hair hale half hall halo halt
hand hang hard hare hark harm harp hash hasp hate hats haul have hawk haze hazy
head heal heap hear heat heed heel heft heir held helm help hemp hens herb herd
here hero hers hewn hide high hike hill hilt hind hint hips hire hiss hits hive
hoax hobo hock hoes hogs hold hole holy home hone honk hood hoof hook hoop hoot
hope hops horn hose host hour hove howl hubs hues huff huge hugs hula hulk hull
hums hung hunk hunt hurl hurt hush husk huts hymn iced icon idea idle idly idol
inch inks inns into ions iota iron isle itch item jabs jack jade jail jams jars
jaws jays jazz jeep jeer jell jerk jest jets jibe jigs jilt jinx jobs jock jogs
join joke jolt jots jowl joys judo jugs jump junk jury just jute keel keen keep
kegs kelp kept kerb keys kick kids kiln kilt kind king kins kiss kite kits knee
knew knit knob knot know lace lack lacy lads lady laid lain lair lake lamb lame
lamp land lane laps lard lark lash lass last late lath laud lava lawn laws lays
laze lazy lead leaf leak lean leap leas left legs lend lens lent less lest lets
levy liar lice lick lids lied lien lies life lift like lilt lily limb lime limp
line link lint lion lips lisp list live load loaf loam loan lobe lobs lock lode
loft logs loin lone long look loom loon loop loot lope lord lore lose loss lost
lots loud lout love lows luck lugs lull lump lung lure lurk lush lust lute lynx
mace made maid mail maim main make male mall malt mane mans many maps mare mark
mars mash mask mass mast mate math mats maul maze mead meal mean meat meek meet
meld melt memo mend menu meow mesh mess mice mild mile milk mill mime mind mine
mint minx mire miss mist mite moan moat mock mode mold mole monk mood moon moor
moot mope more morn moss most moth move much muck muff mugs mule mull mums murk
muse mush musk must mute mutt myth nabs nags nail name nape naps nave navy near
neat neck need neon nest nets news newt next nibs nice nick nigh nine nips node
nods noel none nook noon norm nose nosy note noun nova nude nuns oaks oars oath
oats obey oboe odds odes ogle oils oily okay olds omen omit once ones only onto
onus onyx ooze opal open opts oral orbs ores ouch ours oust outs oval oven over
owed owes owls owns oxen pace pack pact pads page paid pail pain pair pale palm
pane pang pans pant papa pare park part pass past pate path pats pave pawn paws
pays peak peal pear peas peat peck peek peel peep peer pegs pelt pens pent perk
perm pert pest pets pews pick pier pies pigs pike pile pill pine ping pink pins
pint pipe pith pits pity plan play plea pled plod plop plot plow ploy plug plum
plus poem poet poke pole poll polo pond pony pool poor pope pops pore pork port
pose posh post posy pots pour pout pram prawn pray prey prim prod prom prop pros
prow pubs puck puff pugs pull pulp puma pump punk puns punt pupa pups pure purl
purr push puts putt pyre quay quell query quest queue quick quid quiet quill
quilt quip quit quiz quota race rack racy raft rage rags raid rail rain rake
ramp rams rang rank rant rape rapt rare rash rasp rate rats rave rays raze read
real ream reap rear reed reef reek reel refs reins rely rend rent rest ribs rice
rich ride rife rift rigs rile rims rind ring rink riot ripe rips rise risk rite
road roam roar robe robs rock rode rods roes roll romp rook room root rope rose
rosy rote rots rout rove rows rubs ruby rude rues ruff rugs ruin rule rump rung
runs runt ruse rush rust ruts sack safe saga sage said sail sake sale salt same
sand sane sang sank saps sari sash sate save sawn saws says scab scam scan scar
scat seal seam sear seas seat sect seed seek seem seen seep seer sees self sell
semi send sent sets sewn sews shad shag shah sham shed shin ship shoe shop shot
show shun shut shy sick side sift sigh sign silk sill silo silt sing sink sins
sips sire site sits size skew skid skim skin skip skis slab slam slap slat slay
sled slew slid slim slip slit slob sloe slog slop slot slow slug slum slur smog
smug snag snap snip snob snow snub snug soak soap soar sobs sock soda sofa soft
soil sold sole solo some song sons soon soot sore sort soul soup sour sown sows
soya spam span spar spas spat sped spin spit spot spry spun spur stab stag star
stay stem step stew stir stop stow stub stud stun such suds sued sues suit sulk
sums sung sunk suns sure surf swab swag swam swan swap swat sway swig swim swum
tabs tack tact tags tail take tale talk tall tame tang tank tape taps tarn tart
task taut taxi teak teal team tear teas teem teen tell tend tens tent term tern
test text thaw thee them then they thin this thud thug thus tick tide tidy tied
tier ties tile till tilt time tine tins tint tiny tips tire toad toes tofu toil
told toll tomb tone tons took tool toot tops tore torn tort toss tots tour tout
town tows toys tram trap tray tree trek trey trim trio trip trod trot troy true
tsar tuba tube tubs tuck tuft tugs tulip tuna tune turf turn tusk twig twin twit
twos tyke type tyre ugly undo unit unto upon urge urns used user uses vain vale
vane vans vase vast veal veer veil vein vend vent verb very vest veto vets vial
vibe vice vied vies view vile vine viol visa vise void volt vote vows wade wads
waft wage wags waif wail wait wake walk wall wand wane want ward ware warm warn
warp wars wart wary wash wasp watt wave wavy waxy ways weak weal wean wear webs
weds weed week weep weft weld well welt wend went wept were west wham wharf what
wheat wheel when whet whey which whiff while whim whine whip whirl whisk white
whom wick wide wife wigs wild will wilt wily wimp wind wine wing wink wins wipe
wire wiry wise wish wisp with wits woes woke wolf womb wont wood wool word wore
work worm worn wrap wren writ yard yarn yawn yeah year yell yelp yoga yoke yolk
your yule zeal zero zest zinc zone zoom
"""


def build(output_path: str, db_path: str = None) -> int:
    import sqlite3

    if db_path is None:
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        db_path = os.path.join(root, 'instance', 'sitebuilder.sqlite')

    counts = collections.Counter()
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute('SELECT prompt, options_json FROM quiz_questions').fetchall()
    finally:
        conn.close()

    for prompt, options in rows:
        blob = f"{prompt or ''} {options or ''}"
        for token in re.findall(r'[A-Za-z]+', blob):
            if 3 <= len(token) <= 9:
                counts[token.lower()] += 1

    words = {w for w, n in counts.items() if n >= 2}
    words.update(SUPPLEMENT.split())
    words = sorted(w for w in words if w.isalpha() and 3 <= len(w) <= 9)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as fh:
        json.dump(words, fh, separators=(',', ':'))
    return len(words)


if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    target = os.path.join(root, 'app', 'static', 'data', 'qm-lexicon.json')
    total = build(target)
    print(f'Wrote {total} words to {target}')
