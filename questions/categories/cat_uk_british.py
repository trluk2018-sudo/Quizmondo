# -*- coding: utf-8 -*-
from .helper import make_q


def get_questions():
    q = []

    # ---------------------------------------------------------------- Monarchy & royal history
    data_monarchy = [
        ("Which king was on the throne when the Magna Carta was sealed at Runnymede in 1215?", "King John", ["Henry III", "Richard I", "Edward I"], "John sealed Magna Carta under pressure from rebel barons; it limited royal power and underpins English common law.", "easy"),
        ("Who was the last monarch of the House of Tudor?", "Elizabeth I", ["Mary I", "Henry VIII", "Edward VI"], "Elizabeth I died childless in 1603, passing the crown to James VI of Scotland and beginning the Stuart line.", "easy"),
        ("How many wives did Henry VIII have?", "Six", ["Four", "Five", "Seven"], "Catherine of Aragon, Anne Boleyn, Jane Seymour, Anne of Cleves, Catherine Howard and Catherine Parr - divorced, beheaded, died, divorced, beheaded, survived.", "easy"),
        ("Which queen reigned for just nine days in 1553?", "Lady Jane Grey", ["Mary I", "Anne Boleyn", "Matilda"], "Lady Jane Grey was proclaimed queen on 10 July 1553 and deposed by Mary I nine days later.", "medium"),
        ("Which battle in 1066 led to the Norman conquest of England?", "The Battle of Hastings", ["The Battle of Agincourt", "The Battle of Bosworth Field", "The Battle of Stamford Bridge"], "William of Normandy defeated Harold Godwinson near Hastings on 14 October 1066.", "easy"),
        ("Who was the first monarch to rule both England and Scotland?", "James I of England", ["Henry VII", "Charles I", "Edward I"], "James VI of Scotland became James I of England in 1603 in the Union of the Crowns.", "medium"),
        ("Which English king was executed in 1649 at the end of the Civil War?", "Charles I", ["Charles II", "James II", "Richard III"], "Charles I was beheaded outside the Banqueting House in Whitehall on 30 January 1649.", "medium"),
        ("Who ruled England as Lord Protector during the Commonwealth?", "Oliver Cromwell", ["Thomas Cromwell", "John Pym", "Thomas Fairfax"], "Cromwell led the republic from 1653 until his death in 1658; the monarchy was restored in 1660.", "easy"),
        ("Which monarch gave her name to a 63-year reign that ended in 1901?", "Queen Victoria", ["Queen Anne", "Elizabeth I", "Queen Mary"], "Victoria reigned from 1837 to 1901, the longest reign until Elizabeth II surpassed it in 2015.", "easy"),
        ("Which king abdicated in 1936 to marry Wallis Simpson?", "Edward VIII", ["George V", "George VI", "Edward VII"], "Edward VIII abdicated after less than a year, and his brother became George VI.", "medium"),
        ("What was the name of Elizabeth II's Platinum Jubilee year?", "2022", ["2012", "2002", "2020"], "The Platinum Jubilee in 2022 marked 70 years on the throne, a first for a British monarch.", "easy"),
        ("Which royal residence is the monarch's official London home?", "Buckingham Palace", ["Windsor Castle", "Balmoral Castle", "Sandringham House"], "Buckingham Palace has been the official London residence of British monarchs since 1837.", "easy"),
        ("Where are English and British monarchs traditionally crowned?", "Westminster Abbey", ["St Paul's Cathedral", "Canterbury Cathedral", "York Minster"], "Every coronation since 1066 has taken place at Westminster Abbey.", "easy"),
        ("Which Scottish castle is the monarch's private Highland retreat?", "Balmoral Castle", ["Edinburgh Castle", "Stirling Castle", "Glamis Castle"], "Balmoral in Aberdeenshire was bought by Prince Albert in 1852 and remains privately owned by the Royal Family.", "medium"),
        ("What is the name of the stone traditionally used in coronations, returned to Scotland in 1996?", "The Stone of Scone", ["The Stone of Iona", "The Lia Fail", "The Coronation Marble"], "Also called the Stone of Destiny, it sits in Edinburgh Castle and travels to Westminster for coronations.", "hard"),
        ("Which king united much of England and is traditionally said to have burnt the cakes?", "Alfred the Great", ["Athelstan", "Canute", "Edward the Confessor"], "Alfred of Wessex defended England against the Vikings; the cake-burning tale is a later legend.", "medium"),
        ("Which monarch was the last to be crowned in the 20th century?", "Elizabeth II", ["George VI", "George V", "Edward VIII"], "Elizabeth II was crowned on 2 June 1953, the first coronation to be televised.", "easy"),
        ("Who was known as the 'Virgin Queen'?", "Elizabeth I", ["Mary I", "Queen Anne", "Victoria"], "Elizabeth I never married, and the colony of Virginia was named in her honour.", "easy"),
        ("Which king lost the Battle of Bosworth Field in 1485?", "Richard III", ["Henry VI", "Edward IV", "Henry VII"], "Richard III's death ended the Wars of the Roses and the Plantagenet line; Henry Tudor took the crown.", "medium"),
        ("In which city was Richard III's body rediscovered in 2012?", "Leicester", ["York", "Nottingham", "Lincoln"], "His remains were found under a council car park and reburied in Leicester Cathedral in 2015.", "medium"),
        ("What is the official residence of the Prince and Princess of Wales in London?", "Kensington Palace", ["Clarence House", "St James's Palace", "Hampton Court"], "Kensington Palace has housed royals since the 17th century and is partly open to the public.", "medium"),
        ("Which queen was the mother of Elizabeth I?", "Anne Boleyn", ["Catherine of Aragon", "Jane Seymour", "Catherine Parr"], "Anne Boleyn was executed in 1536 when Elizabeth was two years old.", "medium"),
        ("What title is given to the monarch's eldest son as heir apparent?", "Prince of Wales", ["Duke of York", "Duke of Edinburgh", "Earl of Wessex"], "The title has been given to the heir apparent since Edward I invested his son in 1301.", "easy"),
        ("Which royal house ruled Britain from 1714 to 1901?", "The House of Hanover", ["The House of Stuart", "The House of Windsor", "The House of Saxe-Coburg"], "The Hanoverians began with George I and ended with Victoria.", "hard"),
        ("In which year did the Royal Family adopt the surname Windsor?", "1917", ["1901", "1936", "1947"], "George V changed the family name from Saxe-Coburg and Gotha during the First World War.", "hard"),
    ]
    for prompt, corr, dist, exp, diff in data_monarchy:
        q.append(make_q(prompt, corr, dist, exp, diff))

    # ---------------------------------------------------------------- Politics & institutions
    data_politics = [
        ("What is the official residence of the UK Prime Minister?", "10 Downing Street", ["11 Downing Street", "Chequers", "Admiralty House"], "Number 10 has been the Prime Minister's London home since Robert Walpole accepted it in 1735.", "easy"),
        ("Who was Britain's first female Prime Minister?", "Margaret Thatcher", ["Theresa May", "Barbara Castle", "Liz Truss"], "Margaret Thatcher led the country from 1979 to 1990, the longest-serving PM of the 20th century.", "easy"),
        ("Which Prime Minister led Britain through most of the Second World War?", "Winston Churchill", ["Neville Chamberlain", "Clement Attlee", "Anthony Eden"], "Churchill became Prime Minister in May 1940 and led the wartime coalition until 1945.", "easy"),
        ("What are the two Houses of the UK Parliament?", "The Commons and the Lords", ["The Commons and the Senate", "The Lords and the Assembly", "The Commons and the Convocation"], "The House of Commons is elected; the House of Lords is appointed and hereditary.", "easy"),
        ("How many members sit in the House of Commons?", "650", ["600", "550", "700"], "Each of the 650 Members of Parliament represents one constituency.", "medium"),
        ("What is the name of the bell in the Elizabeth Tower at Parliament?", "Big Ben", ["Great Tom", "The Westminster Bell", "Great Paul"], "Big Ben is the nickname of the Great Bell; the tower was renamed the Elizabeth Tower in 2012.", "easy"),
        ("Which ceremony formally opens each parliamentary session?", "The State Opening of Parliament", ["The Trooping of the Mace", "The Speaker's Procession", "The Lord Mayor's Show"], "The monarch delivers the King's or Queen's Speech setting out the government's programme.", "medium"),
        ("What is the title of the MP who chairs debates in the House of Commons?", "The Speaker", ["The Chancellor", "The Leader of the House", "The Chief Whip"], "The Speaker keeps order and is expected to set aside party allegiance.", "easy"),
        ("Which minister is responsible for the UK's finances and delivers the Budget?", "The Chancellor of the Exchequer", ["The Home Secretary", "The Foreign Secretary", "The Chief Secretary"], "The Chancellor traditionally carries the Budget in a red briefcase known as the Budget box.", "easy"),
        ("In which year did the UK formally leave the European Union?", "2020", ["2016", "2019", "2021"], "The referendum was in June 2016 and the UK left on 31 January 2020, with a transition period to year end.", "medium"),
        ("Where does the Scottish Parliament sit?", "Holyrood, Edinburgh", ["Glasgow City Chambers", "Stirling", "Perth"], "The Scottish Parliament building at Holyrood opened in 2004 and was designed by Enric Miralles.", "medium"),
        ("What is the Welsh Parliament called in Welsh?", "Senedd Cymru", ["Dail Cymru", "Cynulliad Mawr", "Ty Cymru"], "The Senedd sits in Cardiff Bay and took its current name in 2020.", "medium"),
        ("Which city is home to the Northern Ireland Assembly?", "Belfast", ["Londonderry", "Armagh", "Lisburn"], "The Assembly sits at Parliament Buildings, Stormont, in east Belfast.", "medium"),
        ("What colour are the benches in the House of Lords?", "Red", ["Green", "Blue", "Brown"], "The Lords has red benches; the Commons has green ones.", "medium"),
        ("Which document, signed in 1707, joined the kingdoms of England and Scotland?", "The Acts of Union", ["The Treaty of Edinburgh", "The Declaration of Arbroath", "The Act of Settlement"], "The Acts of Union created the Kingdom of Great Britain with a single parliament at Westminster.", "medium"),
        ("What is the maximum length of a UK Parliament before a general election must be held?", "Five years", ["Four years", "Six years", "Seven years"], "Parliament must be dissolved within five years of first meeting.", "medium"),
        ("Who was Prime Minister when the NHS was founded in 1948?", "Clement Attlee", ["Winston Churchill", "Harold Wilson", "Ramsay MacDonald"], "Attlee's Labour government created the NHS, with Aneurin Bevan as Health Minister.", "medium"),
        ("Which Prime Minister resigned after the shortest term in British history?", "Liz Truss", ["Anthony Eden", "Alec Douglas-Home", "George Canning"], "Liz Truss served 49 days in 2022, the shortest tenure of any UK Prime Minister.", "medium"),
        ("What is the name of the Prime Minister's official country residence?", "Chequers", ["Dorneywood", "Chevening", "Highgrove"], "Chequers in Buckinghamshire was given to the nation for the PM's use in 1917.", "medium"),
        ("Which royal ceremony sees a crown-wearing figure's representative check the cellars of Parliament?", "The search before the State Opening", ["The Ceremony of the Keys", "Trooping the Colour", "The Changing of the Guard"], "Yeomen of the Guard search the cellars, a tradition dating from the Gunpowder Plot of 1605.", "hard"),
        ("Who led the Gunpowder Plot's attempt to blow up Parliament in 1605?", "Robert Catesby", ["Guy Fawkes", "Thomas Percy", "Francis Tresham"], "Catesby led the conspiracy; Guy Fawkes was caught guarding the barrels and became the best-remembered plotter.", "hard"),
        ("What is the official name of the UK's national flag?", "The Union Flag", ["The Royal Standard", "The St George Cross", "The Britannia Banner"], "Often called the Union Jack, strictly a term for when it is flown at sea.", "medium"),
    ]
    for prompt, corr, dist, exp, diff in data_politics:
        q.append(make_q(prompt, corr, dist, exp, diff))

    # ---------------------------------------------------------------- UK geography
    data_geography = [
        ("What is the longest river in the United Kingdom?", "The River Severn", ["The River Thames", "The River Trent", "The River Tay"], "The Severn runs about 220 miles from mid-Wales to the Bristol Channel.", "easy"),
        ("What is the highest mountain in the British Isles?", "Ben Nevis", ["Snowdon", "Scafell Pike", "Slieve Donard"], "Ben Nevis in the Scottish Highlands rises to 1,345 metres.", "easy"),
        ("What is the highest mountain in Wales?", "Snowdon", ["Cadair Idris", "Tryfan", "Pen y Fan"], "Snowdon, or Yr Wyddfa, reaches 1,085 metres in Snowdonia.", "easy"),
        ("What is the highest mountain in England?", "Scafell Pike", ["Helvellyn", "Skiddaw", "Cross Fell"], "Scafell Pike in the Lake District stands 978 metres high.", "medium"),
        ("Which is the largest lake by surface area in Great Britain?", "Loch Lomond", ["Loch Ness", "Windermere", "Lough Neagh"], "Loch Lomond has the largest surface area in Great Britain; Lough Neagh in Northern Ireland is larger still in the UK.", "medium"),
        ("Which English county is known as the Garden of England?", "Kent", ["Surrey", "Sussex", "Devon"], "Kent earned the name for its orchards, hop gardens and fruit farms.", "easy"),
        ("What is the capital of Northern Ireland?", "Belfast", ["Londonderry", "Armagh", "Bangor"], "Belfast sits at the mouth of the River Lagan and is Northern Ireland's largest city.", "easy"),
        ("Which city is known as the Granite City?", "Aberdeen", ["Edinburgh", "Dundee", "Inverness"], "Aberdeen's buildings were largely constructed from locally quarried grey granite.", "medium"),
        ("Which strait separates Great Britain from the island of Ireland at its narrowest?", "The North Channel", ["The Irish Sea", "St George's Channel", "The Minch"], "The North Channel between Scotland and Northern Ireland narrows to about 12 miles.", "hard"),
        ("Which English city has the postcode area 'B'?", "Birmingham", ["Bristol", "Bolton", "Bradford"], "Birmingham, the UK's second-largest city, uses the B postcode area.", "medium"),
        ("What is the southernmost point of mainland Great Britain?", "Lizard Point", ["Land's End", "Start Point", "Portland Bill"], "Lizard Point in Cornwall is the mainland's most southerly spot; Land's End is the most westerly.", "medium"),
        ("Which range of hills is known as the backbone of England?", "The Pennines", ["The Cotswolds", "The Chilterns", "The Cheviots"], "The Pennines run roughly from the Peak District to the Scottish border.", "easy"),
        ("Which UK national park is the largest?", "The Cairngorms", ["The Lake District", "Snowdonia", "The Yorkshire Dales"], "The Cairngorms National Park in Scotland covers around 4,500 square kilometres.", "medium"),
        ("Which island group lies furthest north in the UK?", "Shetland", ["Orkney", "The Hebrides", "The Isles of Scilly"], "Shetland lies roughly 110 miles north of the Scottish mainland.", "medium"),
        ("What is the only English city with a cathedral but no city walls that is also an island?", "Portsmouth", ["Plymouth", "Southampton", "Hull"], "Portsmouth sits largely on Portsea Island, making it unusual among English cities.", "hard"),
        ("Which Welsh town has the longest place name in Britain?", "Llanfairpwllgwyngyll", ["Betws-y-Coed", "Machynlleth", "Aberystwyth"], "The full 58-letter name on Anglesey was coined in the 19th century to attract visitors.", "medium"),
        ("The Giant's Causeway is in which part of the UK?", "Northern Ireland", ["Scotland", "Wales", "Cornwall"], "The basalt columns on the County Antrim coast formed from cooling lava around 60 million years ago.", "easy"),
        ("Which is the largest county in England by area?", "North Yorkshire", ["Lincolnshire", "Devon", "Cumbria"], "North Yorkshire is the largest ceremonial county in England.", "medium"),
        ("Which river flows through the city of York?", "The Ouse", ["The Aire", "The Tees", "The Wharfe"], "The River Ouse runs through the heart of York and has often flooded the city.", "medium"),
        ("Which Scottish loch is famous for its supposed monster?", "Loch Ness", ["Loch Lomond", "Loch Awe", "Loch Morar"], "Loch Ness holds more fresh water than all the lakes of England and Wales combined.", "easy"),
        ("What is the largest island in the Inner Hebrides?", "Skye", ["Mull", "Islay", "Jura"], "Skye is linked to the mainland by the Skye Bridge, opened in 1995.", "medium"),
        ("Which English seaside town has the UK's oldest surviving pleasure pier?", "Southend-on-Sea", ["Brighton", "Blackpool", "Weston-super-Mare"], "Southend Pier is also the longest pleasure pier in the world at 1.33 miles.", "hard"),
        ("The Cotswolds are famous for buildings made from which material?", "Honey-coloured limestone", ["Red brick", "Granite", "Flint"], "Cotswold stone gives the villages their distinctive golden appearance.", "medium"),
        ("Which city is the most northerly in England?", "Carlisle", ["Newcastle upon Tyne", "Durham", "Berwick"], "Carlisle in Cumbria is England's most northerly city; Berwick-upon-Tweed is a town, not a city.", "hard"),
        ("How many counties are there in Northern Ireland?", "Six", ["Four", "Eight", "Nine"], "Antrim, Armagh, Down, Fermanagh, Londonderry and Tyrone.", "medium"),
    ]
    for prompt, corr, dist, exp, diff in data_geography:
        q.append(make_q(prompt, corr, dist, exp, diff))

    # ---------------------------------------------------------------- London
    data_london = [
        ("Which London landmark is a 135-metre observation wheel on the South Bank?", "The London Eye", ["The Shard", "The Monument", "The Orbit"], "Opened for the millennium, it was the world's tallest observation wheel at the time.", "easy"),
        ("What is the name of the tallest building in the UK?", "The Shard", ["One Canada Square", "The Gherkin", "22 Bishopsgate"], "The Shard at London Bridge stands 310 metres tall and opened in 2012.", "easy"),
        ("Which London bridge has two towers and a lifting roadway?", "Tower Bridge", ["London Bridge", "Westminster Bridge", "Blackfriars Bridge"], "Tower Bridge opened in 1894; its bascules still lift for tall vessels around 800 times a year.", "easy"),
        ("Which royal park is the largest in central London?", "Hyde Park", ["Regent's Park", "St James's Park", "Green Park"], "Hyde Park covers around 350 acres and contains the Serpentine lake.", "medium"),
        ("What is the oldest section of the London Underground, opened in 1863?", "The Metropolitan line", ["The Circle line", "The District line", "The Northern line"], "The Metropolitan Railway between Paddington and Farringdon was the world's first underground railway.", "medium"),
        ("Which London street is traditionally home to tailoring?", "Savile Row", ["Jermyn Street", "Bond Street", "Carnaby Street"], "Savile Row in Mayfair has been the centre of bespoke tailoring since the 19th century.", "medium"),
        ("What is the name of the famous clock tower at the Palace of Westminster?", "The Elizabeth Tower", ["The Victoria Tower", "The Albert Tower", "The Jubilee Tower"], "Renamed in 2012 for Elizabeth II's Diamond Jubilee; it houses the bell known as Big Ben.", "medium"),
        ("Which cathedral, designed by Christopher Wren, dominates the City of London skyline?", "St Paul's Cathedral", ["Westminster Abbey", "Southwark Cathedral", "Westminster Cathedral"], "Wren rebuilt St Paul's after the Great Fire of 1666; its dome was completed in 1710.", "easy"),
        ("In which year was the Great Fire of London?", "1666", ["1665", "1600", "1688"], "The fire began in a bakery on Pudding Lane and burned for four days.", "easy"),
        ("Which market in London is famous for antiques and sits in Notting Hill?", "Portobello Road Market", ["Borough Market", "Camden Market", "Spitalfields Market"], "Portobello Road hosts the world's largest antiques market on Saturdays.", "medium"),
        ("What is the name of the official residence of the Lord Mayor of London?", "Mansion House", ["Guildhall", "The Mansion", "City Hall"], "Mansion House has been the Lord Mayor's official home since the 1750s.", "hard"),
        ("Which London railway station is the terminus for Eurostar services?", "St Pancras International", ["Waterloo", "Victoria", "King's Cross"], "Eurostar moved from Waterloo to St Pancras in 2007.", "easy"),
        ("The Tower of London is guarded by soldiers known by what nickname?", "Beefeaters", ["Redcoats", "Grenadiers", "Life Guards"], "Officially Yeomen Warders, they have guarded the Tower since Tudor times.", "easy"),
        ("Which birds are famously kept at the Tower of London?", "Ravens", ["Peacocks", "Crows", "Falcons"], "Legend says the kingdom will fall if the ravens leave the Tower.", "easy"),
        ("Which square in London contains Nelson's Column?", "Trafalgar Square", ["Leicester Square", "Russell Square", "Parliament Square"], "The column commemorates Admiral Nelson's victory at Trafalgar in 1805.", "easy"),
        ("What is the name of London's financial district often called the Square Mile?", "The City of London", ["Canary Wharf", "Westminster", "Southwark"], "The City of London covers roughly one square mile and has its own Lord Mayor and police force.", "medium"),
        ("Which London museum houses the Rosetta Stone?", "The British Museum", ["The Natural History Museum", "The V&A", "The Science Museum"], "The Rosetta Stone has been in the British Museum since 1802 and unlocked Egyptian hieroglyphs.", "easy"),
        ("Which London theatre district is known as Theatreland?", "The West End", ["The East End", "Southbank", "Shoreditch"], "The West End contains around 40 major theatres around Shaftesbury Avenue and the Strand.", "easy"),
    ]
    for prompt, corr, dist, exp, diff in data_london:
        q.append(make_q(prompt, corr, dist, exp, diff))

    # ---------------------------------------------------------------- British TV & radio
    data_tv = [
        ("Which long-running BBC soap opera is set in Albert Square?", "EastEnders", ["Coronation Street", "Emmerdale", "Hollyoaks"], "EastEnders first aired in February 1985 and is set in the fictional borough of Walford.", "easy"),
        ("Which is the longest-running television soap opera in the world?", "Coronation Street", ["EastEnders", "Emmerdale", "Neighbours"], "Coronation Street began on ITV in December 1960 and is set in Weatherfield.", "easy"),
        ("Which BBC motoring show was presented by Clarkson, Hammond and May?", "Top Gear", ["Fifth Gear", "Wheeler Dealers", "Car SOS"], "The trio presented Top Gear from 2003 until 2015, when they moved to a rival streaming show.", "easy"),
        ("What is the name of the time-travelling BBC science fiction series begun in 1963?", "Doctor Who", ["Blake's 7", "Red Dwarf", "Quantum Leap"], "Doctor Who first aired the day after the Kennedy assassination and features a time machine called the TARDIS.", "easy"),
        ("Which British sitcom featured the Trotter family and a three-wheeled van?", "Only Fools and Horses", ["Open All Hours", "Porridge", "Steptoe and Son"], "Del Boy and Rodney traded from Nelson Mandela House in Peckham in their Reliant Regal.", "easy"),
        ("In 'Fawlty Towers', what nationality is the waiter Manuel?", "Spanish", ["Italian", "Portuguese", "Greek"], "Manuel is from Barcelona, as Basil Fawlty repeatedly explains to guests.", "easy"),
        ("Which quiz show features a black leather chair and the phrase 'Starter for ten'?", "University Challenge", ["Mastermind", "The Chase", "Only Connect"], "Mastermind has the black chair; University Challenge uses 'Starter for ten'. The chair belongs to Mastermind.", "hard"),
        ("Which BBC baking competition moved to Channel 4 in 2017?", "The Great British Bake Off", ["MasterChef", "Saturday Kitchen", "Great British Menu"], "Bake Off moved networks after Love Productions and the BBC failed to agree terms.", "easy"),
        ("Which British sitcom was set in a Slough paper merchants?", "The Office", ["The IT Crowd", "Peep Show", "W1A"], "Ricky Gervais and Stephen Merchant's mockumentary followed Wernham Hogg in Slough.", "medium"),
        ("What is the name of the BBC's long-running radio soap set in Ambridge?", "The Archers", ["Mrs Dale's Diary", "Brookside", "The Grove Family"], "The Archers began in 1951 and is the world's longest-running radio drama.", "medium"),
        ("Which BBC programme has broadcast the shipping forecast for decades?", "Radio 4", ["Radio 2", "Radio 5 Live", "The World Service"], "The shipping forecast is read on BBC Radio 4 and has become a national institution.", "medium"),
        ("In 'Blackadder', which actor played Edmund Blackadder?", "Rowan Atkinson", ["Hugh Laurie", "Tony Robinson", "Stephen Fry"], "Rowan Atkinson played Blackadder across four series spanning five centuries.", "easy"),
        ("Which detective series is set in Oxford and features a classic Jaguar?", "Inspector Morse", ["Midsomer Murders", "A Touch of Frost", "Vera"], "John Thaw played Morse, who drove a maroon Jaguar Mark 2.", "medium"),
        ("Which children's BBC programme is the longest-running of its kind in the world?", "Blue Peter", ["Grange Hill", "Play School", "Newsround"], "Blue Peter has aired since 1958 and awards its famous badges to young viewers.", "medium"),
        ("Which period drama about a Yorkshire estate was created by Julian Fellowes?", "Downton Abbey", ["Brideshead Revisited", "Upstairs Downstairs", "Poldark"], "Downton Abbey ran from 2010 to 2015 and was filmed largely at Highclere Castle.", "easy"),
        ("What is the name of the BBC crime drama set in Birmingham in the 1920s?", "Peaky Blinders", ["Ripper Street", "Boardwalk Empire", "Taboo"], "Peaky Blinders follows the Shelby family and takes its name from a real Birmingham gang.", "easy"),
        ("Which panel show has been hosted by Sandi Toksvig and Stephen Fry?", "QI", ["Have I Got News for You", "Mock the Week", "8 Out of 10 Cats"], "Stephen Fry hosted QI from 2003, with Sandi Toksvig taking over in 2016.", "medium"),
        ("Which Welsh town provided the setting for the sitcom 'Gavin & Stacey'?", "Barry", ["Swansea", "Newport", "Porthcawl"], "The Welsh half of the show is set in Barry Island, the English half in Billericay, Essex.", "medium"),
        ("Which BBC drama follows an anti-corruption police unit known as AC-12?", "Line of Duty", ["Bodyguard", "Happy Valley", "Broadchurch"], "Jed Mercurio's series made 'bent coppers' and the phrase 'mother of God' into catchphrases.", "medium"),
        ("What was the first programme broadcast on British colour television in 1967?", "Wimbledon tennis", ["The Queen's Speech", "Match of the Day", "Doctor Who"], "BBC Two launched colour broadcasts with coverage of Wimbledon on 1 July 1967.", "hard"),
        ("Which sitcom was set in a Peckham corner shop and starred Ronnie Barker?", "Open All Hours", ["Only Fools and Horses", "Porridge", "Are You Being Served?"], "Open All Hours was actually set in Doncaster; Barker played the stuttering shopkeeper Arkwright.", "hard"),
        ("Which long-running ITV talent show was created by Simon Cowell in 2004?", "The X Factor", ["Britain's Got Talent", "Pop Idol", "The Voice UK"], "The X Factor replaced Pop Idol and ran on ITV until 2018.", "medium"),
    ]
    for prompt, corr, dist, exp, diff in data_tv:
        q.append(make_q(prompt, corr, dist, exp, diff))

    # ---------------------------------------------------------------- British music
    data_music = [
        ("Which Liverpool band released 'Hey Jude' in 1968?", "The Beatles", ["The Rolling Stones", "The Kinks", "The Hollies"], "'Hey Jude' was the Beatles' longest single at over seven minutes and topped charts worldwide.", "easy"),
        ("Who was the lead singer of Queen?", "Freddie Mercury", ["Brian May", "Roger Taylor", "Robert Plant"], "Born Farrokh Bulsara, Mercury fronted Queen from 1970 until his death in 1991.", "easy"),
        ("Which Manchester band were led by the Gallagher brothers?", "Oasis", ["Blur", "The Stone Roses", "The Smiths"], "Noel and Liam Gallagher led Oasis to huge success with 'Definitely Maybe' and '(What's the Story) Morning Glory?'.", "easy"),
        ("Which 1960s Birmingham band is widely credited with inventing heavy metal?", "Black Sabbath", ["Led Zeppelin", "Deep Purple", "Judas Priest"], "Black Sabbath's 1970 debut is often cited as the first true heavy metal album.", "medium"),
        ("Who released the album 'Back to Black' in 2006?", "Amy Winehouse", ["Adele", "Duffy", "Lily Allen"], "'Back to Black' won five Grammy Awards and became one of the UK's best-selling albums.", "easy"),
        ("Which Welsh singer is known as 'The Voice' and sang 'Delilah'?", "Tom Jones", ["Shirley Bassey", "Harry Secombe", "Aled Jones"], "Sir Tom Jones, born in Pontypridd, has had hits across seven decades.", "easy"),
        ("Which band's album 'The Dark Side of the Moon' spent over 900 weeks on the US chart?", "Pink Floyd", ["Genesis", "Yes", "King Crimson"], "Released in 1973, it remains one of the best-selling albums of all time.", "medium"),
        ("Who wrote and performed 'Your Song' in 1970?", "Elton John", ["David Bowie", "Cat Stevens", "Rod Stewart"], "Elton John composed the music to Bernie Taupin's lyrics; it was his first major hit.", "easy"),
        ("Which David Bowie alter ego appeared on a 1972 album?", "Ziggy Stardust", ["The Thin White Duke", "Aladdin Sane", "Major Tom"], "'The Rise and Fall of Ziggy Stardust and the Spiders from Mars' made Bowie a global star.", "medium"),
        ("Which Sheffield band had a 2006 debut album that broke UK sales records?", "Arctic Monkeys", ["Pulp", "The Human League", "Def Leppard"], "'Whatever People Say I Am, That's What I'm Not' was the fastest-selling debut album in UK history at the time.", "medium"),
        ("Which British festival is held at Worthy Farm in Somerset?", "Glastonbury", ["Reading", "Leeds", "Isle of Wight"], "Michael Eavis has hosted the festival on his dairy farm at Pilton since 1970.", "easy"),
        ("Which singer released the record-breaking album '21' in 2011?", "Adele", ["Amy Winehouse", "Jessie J", "Florence Welch"], "'21' sold over 30 million copies and won six Grammy Awards.", "easy"),
        ("Which band recorded 'A Design for Life' and 'If You Tolerate This'?", "Manic Street Preachers", ["Super Furry Animals", "Stereophonics", "Catatonia"], "The Welsh band have been one of Britain's most enduring rock acts since the early 1990s.", "hard"),
        ("Which 1985 charity concert was held at Wembley Stadium and Philadelphia?", "Live Aid", ["Band Aid", "Live 8", "The Secret Policeman's Ball"], "Bob Geldof and Midge Ure organised Live Aid to raise money for the Ethiopian famine.", "medium"),
        ("What instrument is Jacqueline du Pre famous for playing?", "The cello", ["The violin", "The piano", "The harp"], "Her 1965 recording of Elgar's Cello Concerto remains a benchmark performance.", "hard"),
        ("Which British composer wrote 'The Planets' suite?", "Gustav Holst", ["Edward Elgar", "Ralph Vaughan Williams", "Benjamin Britten"], "Holst composed 'The Planets' between 1914 and 1917; 'Jupiter' supplied the tune for 'I Vow to Thee, My Country'.", "medium"),
        ("Which Elgar work provides the music for 'Land of Hope and Glory'?", "Pomp and Circumstance March No. 1", ["The Enigma Variations", "Cockaigne", "The Dream of Gerontius"], "The trio section of the first Pomp and Circumstance march became the famous anthem.", "hard"),
        ("Which Scottish band recorded 'Don't You (Forget About Me)'?", "Simple Minds", ["Big Country", "Deacon Blue", "Travis"], "The 1985 single featured on 'The Breakfast Club' soundtrack and became their biggest hit.", "medium"),
        ("Which girl group had hits with 'Wannabe' and 'Spice Up Your Life'?", "The Spice Girls", ["All Saints", "Sugababes", "Girls Aloud"], "The Spice Girls became the biggest-selling female group of all time after 'Wannabe' in 1996.", "easy"),
        ("Which annual UK chart event traditionally crowns a Christmas number one?", "The UK Singles Chart", ["The Mercury Prize", "The Brit Awards", "The Ivor Novello Awards"], "The Christmas number one has been a national talking point since the 1950s.", "medium"),
    ]
    for prompt, corr, dist, exp, diff in data_music:
        q.append(make_q(prompt, corr, dist, exp, diff))

    # ---------------------------------------------------------------- Food, drink & the pub
    data_food = [
        ("What are the two main ingredients of the dish 'bangers and mash'?", "Sausages and mashed potato", ["Beef and mashed swede", "Bacon and mushrooms", "Black pudding and mash"], "The nickname 'bangers' comes from wartime sausages bursting in the pan.", "easy"),
        ("What is traditionally served with roast beef in a British Sunday roast?", "Yorkshire pudding", ["Dumplings", "Scotch pancake", "Soda bread"], "Yorkshire pudding is a baked batter dish, first recorded in print in 1747.", "easy"),
        ("What is a 'full English breakfast' usually built around?", "Bacon, eggs and sausage", ["Porridge and cream", "Kippers and toast", "Pancakes and syrup"], "The fry-up typically adds beans, tomato, mushrooms, black pudding and fried bread.", "easy"),
        ("Which savoury pastry is associated with Cornwall and has protected status?", "The Cornish pasty", ["The Bedfordshire clanger", "The Melton Mowbray pie", "The Forfar bridie"], "A genuine Cornish pasty must be made in Cornwall and crimped on the side.", "easy"),
        ("What is haggis traditionally served with in Scotland?", "Neeps and tatties", ["Peas and chips", "Beans and toast", "Rice and gravy"], "Neeps are swede or turnip and tatties are potatoes; the dish is central to Burns Night.", "easy"),
        ("What is the main ingredient of black pudding?", "Blood", ["Liver", "Treacle", "Barley"], "Black pudding is a blood sausage, usually pig's blood with oatmeal or barley.", "medium"),
        ("Which drink is made from malted barley, hops, water and yeast?", "Beer", ["Cider", "Mead", "Perry"], "Cider is made from apples, perry from pears and mead from honey.", "easy"),
        ("What is a 'pint' in UK measure, in millilitres?", "568 ml", ["500 ml", "600 ml", "473 ml"], "An imperial pint is 568 millilitres, larger than the US pint of 473 ml.", "medium"),
        ("What is cider traditionally made from?", "Apples", ["Pears", "Grapes", "Plums"], "Pear cider is properly called perry; the West Country is Britain's cider heartland.", "easy"),
        ("Which spirit must be matured in oak casks in Scotland for at least three years to be called Scotch?", "Whisky", ["Gin", "Rum", "Brandy"], "Scotch whisky is protected by law and must be matured in Scotland for a minimum of three years.", "medium"),
        ("What is the dish 'toad in the hole'?", "Sausages baked in batter", ["A pie with a hole in the lid", "Poached eggs on toast", "Stuffed marrow"], "Sausages are baked in Yorkshire pudding batter, usually served with onion gravy.", "easy"),
        ("Which cheese takes its name from a Somerset village?", "Cheddar", ["Stilton", "Wensleydale", "Caerphilly"], "Cheddar is named after the Somerset gorge where the cheese was once matured in caves.", "easy"),
        ("Which blue cheese is known as the king of English cheeses?", "Stilton", ["Cheshire", "Red Leicester", "Double Gloucester"], "Stilton has protected status and may only be made in Derbyshire, Leicestershire and Nottinghamshire.", "medium"),
        ("What is traditionally eaten on Shrove Tuesday in Britain?", "Pancakes", ["Hot cross buns", "Simnel cake", "Mince pies"], "Pancakes used up eggs, milk and fat before the fasting of Lent.", "easy"),
        ("What is a 'cream tea' made up of?", "Scones, jam and clotted cream", ["Cake and custard", "Shortbread and cream", "Crumpets and butter"], "Devon puts cream first, Cornwall puts jam first - a debate with no end.", "easy"),
        ("Which fortified pudding is traditionally steamed and set alight at Christmas?", "Christmas pudding", ["Bakewell tart", "Spotted dick", "Eton mess"], "Also called plum pudding, it is usually doused in brandy and flamed at the table.", "medium"),
        ("Which pudding is made from meringue, cream and strawberries and named after a school?", "Eton mess", ["Bakewell pudding", "Knickerbocker glory", "Banoffee pie"], "Eton mess is traditionally served at the school's annual cricket match against Harrow.", "medium"),
        ("What does 'bitter' describe in a British pub?", "A style of pale ale", ["A stout", "A cider", "A strong lager"], "Bitter is a hop-forward British pale ale, usually served cask-conditioned.", "medium"),
        ("What is the name for a pub with no music, games or food, serving only drinks?", "A spit-and-sawdust pub", ["A free house", "A gastropub", "A tied house"], "A 'free house' is one not tied to a brewery; spit-and-sawdust describes a basic drinking pub.", "hard"),
        ("What is a 'tied house' in British pub terms?", "A pub that must buy beer from one brewery", ["A pub with no licence", "A pub with rooms", "A members-only pub"], "Tied houses contrast with free houses, which can buy from any supplier.", "hard"),
    ]
    for prompt, corr, dist, exp, diff in data_food:
        q.append(make_q(prompt, corr, dist, exp, diff))

    # ---------------------------------------------------------------- British sport
    data_sport = [
        ("Which London tennis tournament is the oldest in the world?", "Wimbledon", ["Queen's Club", "The Eastbourne International", "The Surbiton Trophy"], "The Championships have been held at the All England Club since 1877.", "easy"),
        ("What colour must players mostly wear at Wimbledon?", "White", ["Cream", "Navy", "Light grey"], "The all-white rule has governed Wimbledon clothing since the 19th century.", "easy"),
        ("Which stadium is the home of the England football team?", "Wembley Stadium", ["Old Trafford", "Twickenham", "The Emirates"], "The rebuilt Wembley opened in 2007 with its 133-metre arch.", "easy"),
        ("Which stadium is the home of English rugby union?", "Twickenham", ["Wembley", "Murrayfield", "The Millennium Stadium"], "Twickenham in south-west London has hosted England rugby since 1909.", "easy"),
        ("In which year did England win the FIFA World Cup?", "1966", ["1962", "1970", "1958"], "England beat West Germany 4-2 at Wembley, with a hat-trick from Geoff Hurst.", "easy"),
        ("Which annual horse race is run at Aintree?", "The Grand National", ["The Derby", "The Gold Cup", "The St Leger"], "The Grand National is a gruelling steeplechase over 30 fences near Liverpool.", "easy"),
        ("Where is the Epsom Derby run?", "Epsom Downs, Surrey", ["Ascot", "Newmarket", "Doncaster"], "The Derby has been run at Epsom since 1780 and is Britain's premier flat race.", "medium"),
        ("Which cricket ground is known as the home of cricket?", "Lord's", ["The Oval", "Headingley", "Edgbaston"], "Lord's in St John's Wood is home to Marylebone Cricket Club and the Ashes urn.", "easy"),
        ("What trophy do England and Australia contest in Test cricket?", "The Ashes", ["The Wisden Trophy", "The Border-Gavaskar Trophy", "The Basil D'Oliveira Trophy"], "The Ashes began in 1882 after a mock obituary for English cricket.", "easy"),
        ("Which sport is played in the Six Nations Championship?", "Rugby union", ["Rugby league", "Cricket", "Football"], "England, Scotland, Wales, Ireland, France and Italy contest it each spring.", "easy"),
        ("Which golf tournament is the oldest of the four majors?", "The Open Championship", ["The Masters", "The US Open", "The PGA Championship"], "The Open, first played at Prestwick in 1860, is the only major held outside the United States.", "medium"),
        ("Which Scottish course is known as the home of golf?", "St Andrews", ["Carnoustie", "Muirfield", "Troon"], "The Old Course at St Andrews has been played since the 15th century.", "easy"),
        ("Which city hosted the 2012 Summer Olympics?", "London", ["Manchester", "Birmingham", "Glasgow"], "London became the first city to host the modern Olympics three times.", "easy"),
        ("Which Welsh city hosts the Principality Stadium?", "Cardiff", ["Swansea", "Newport", "Wrexham"], "Formerly the Millennium Stadium, it opened in 1999 and has a retractable roof.", "medium"),
        ("How many players are on a rugby league team?", "Thirteen", ["Fifteen", "Eleven", "Twelve"], "Rugby league fields 13 players; rugby union fields 15.", "medium"),
        ("Which English football club is nicknamed the Red Devils?", "Manchester United", ["Liverpool", "Arsenal", "Nottingham Forest"], "United adopted the nickname in the 1960s under Matt Busby.", "easy"),
        ("Which football club plays at Anfield?", "Liverpool", ["Everton", "Manchester City", "Newcastle United"], "Anfield has been Liverpool's home since 1892 and is famous for the Kop.", "easy"),
        ("What is the name of the knockout football competition that is the oldest in the world?", "The FA Cup", ["The League Cup", "The Community Shield", "The Scottish Cup"], "The FA Cup was first contested in the 1871-72 season.", "medium"),
        ("Which snooker tournament is held at the Crucible Theatre?", "The World Championship", ["The Masters", "The UK Championship", "The Welsh Open"], "The World Snooker Championship has been at Sheffield's Crucible since 1977.", "medium"),
        ("Which British driver won seven Formula One world titles?", "Lewis Hamilton", ["Jenson Button", "Nigel Mansell", "Jackie Stewart"], "Hamilton equalled Michael Schumacher's record of seven championships in 2020.", "easy"),
        ("Which race takes place between Oxford and Cambridge on the Thames?", "The Boat Race", ["The Head of the River", "The Henley Regatta", "The Thames Marathon"], "The Boat Race has been rowed on the Championship Course at Putney since 1845.", "medium"),
        ("Which sport features the terms 'googly', 'silly point' and 'maiden over'?", "Cricket", ["Croquet", "Rounders", "Bowls"], "A googly is a deceptive leg-spin delivery; a maiden over concedes no runs.", "medium"),
    ]
    for prompt, corr, dist, exp, diff in data_sport:
        q.append(make_q(prompt, corr, dist, exp, diff))

    # ---------------------------------------------------------------- Literature & writers
    data_books = [
        ("Who wrote 'Pride and Prejudice'?", "Jane Austen", ["Charlotte Bronte", "George Eliot", "Elizabeth Gaskell"], "Austen's novel was published in 1813 and opens with one of literature's most quoted lines.", "easy"),
        ("Which Yorkshire sisters wrote 'Jane Eyre' and 'Wuthering Heights'?", "The Brontes", ["The Mitfords", "The Stracheys", "The Sitwells"], "Charlotte wrote 'Jane Eyre' and Emily 'Wuthering Heights', both published in 1847.", "easy"),
        ("Who created the detective Sherlock Holmes?", "Arthur Conan Doyle", ["Agatha Christie", "Wilkie Collins", "G. K. Chesterton"], "Holmes first appeared in 'A Study in Scarlet' in 1887.", "easy"),
        ("Which Victorian novelist wrote 'Oliver Twist' and 'Great Expectations'?", "Charles Dickens", ["Thomas Hardy", "Anthony Trollope", "William Thackeray"], "Dickens published most of his novels in monthly instalments.", "easy"),
        ("Who wrote the 'Harry Potter' series?", "J. K. Rowling", ["Philip Pullman", "Enid Blyton", "Diana Wynne Jones"], "The first book appeared in 1997 and the series has sold over 500 million copies.", "easy"),
        ("Which Stratford-upon-Avon playwright wrote 'Hamlet'?", "William Shakespeare", ["Christopher Marlowe", "Ben Jonson", "John Webster"], "Shakespeare wrote around 39 plays and 154 sonnets.", "easy"),
        ("How many lines does a Shakespearean sonnet have?", "Fourteen", ["Twelve", "Sixteen", "Ten"], "Three quatrains and a closing couplet, in iambic pentameter.", "medium"),
        ("Which author created the Discworld series?", "Terry Pratchett", ["Douglas Adams", "Neil Gaiman", "Michael Moorcock"], "Pratchett wrote 41 Discworld novels between 1983 and 2015.", "medium"),
        ("Who wrote 'The Hobbit' and 'The Lord of the Rings'?", "J. R. R. Tolkien", ["C. S. Lewis", "Mervyn Peake", "T. H. White"], "Tolkien was Professor of Anglo-Saxon at Oxford while writing Middle-earth.", "easy"),
        ("Which Welsh author wrote 'Charlie and the Chocolate Factory'?", "Roald Dahl", ["Dick King-Smith", "Michael Morpurgo", "Richmal Crompton"], "Dahl was born in Cardiff to Norwegian parents and wrote in a garden hut in Buckinghamshire.", "easy"),
        ("Who wrote 'Nineteen Eighty-Four'?", "George Orwell", ["Aldous Huxley", "H. G. Wells", "Anthony Burgess"], "Orwell, real name Eric Blair, published the novel in 1949.", "easy"),
        ("Which crime writer created Hercule Poirot and Miss Marple?", "Agatha Christie", ["Dorothy L. Sayers", "Ngaio Marsh", "P. D. James"], "Christie is the best-selling novelist of all time with around two billion copies sold.", "easy"),
        ("Which poet wrote 'Daffodils', beginning 'I wandered lonely as a cloud'?", "William Wordsworth", ["Samuel Taylor Coleridge", "John Keats", "Lord Byron"], "Wordsworth lived at Dove Cottage in Grasmere in the Lake District.", "medium"),
        ("Which Scottish poet wrote 'Auld Lang Syne'?", "Robert Burns", ["Walter Scott", "Robert Louis Stevenson", "Hugh MacDiarmid"], "Burns Night on 25 January celebrates the poet with haggis and recitations.", "easy"),
        ("Which novel by Mary Shelley is often called the first science fiction novel?", "Frankenstein", ["Dracula", "The Time Machine", "The Island of Doctor Moreau"], "Shelley began it in 1816 during a wet summer by Lake Geneva, aged just 18.", "medium"),
        ("Who wrote 'Brave New World'?", "Aldous Huxley", ["George Orwell", "E. M. Forster", "Evelyn Waugh"], "Published in 1932, it imagines a society built on conditioning and the drug soma.", "medium"),
        ("Which annual prize is Britain's best-known award for fiction?", "The Booker Prize", ["The Costa Award", "The Orange Prize", "The Baillie Gifford Prize"], "First awarded in 1969, it now covers fiction in English published in the UK and Ireland.", "medium"),
        ("Which poet became famous for war poems including 'Dulce et Decorum Est'?", "Wilfred Owen", ["Rupert Brooke", "Siegfried Sassoon", "Edward Thomas"], "Owen was killed in action one week before the Armistice in 1918.", "hard"),
    ]
    for prompt, corr, dist, exp, diff in data_books:
        q.append(make_q(prompt, corr, dist, exp, diff))

    # ---------------------------------------------------------------- Slang, dialect & language
    data_slang = [
        ("In British slang, what is a 'quid'?", "One pound", ["One penny", "Five pounds", "Fifty pence"], "A quid is a pound sterling; the term dates from the late 17th century.", "easy"),
        ("What does the British slang 'knackered' mean?", "Exhausted", ["Angry", "Drunk", "Confused"], "Originally from the knacker's yard, where worn-out horses were sent.", "easy"),
        ("If something is 'chuffed' in Britain, how do you feel?", "Very pleased", ["Annoyed", "Nervous", "Cold"], "Confusingly, 'chuff' once meant displeased in some dialects.", "easy"),
        ("What does 'taking the biscuit' mean?", "Being the most annoying example", ["Winning a prize", "Stealing something", "Leaving early"], "Often used as 'that really takes the biscuit' for something outrageous.", "medium"),
        ("In Cockney rhyming slang, what are your 'plates of meat'?", "Feet", ["Hands", "Teeth", "Eyes"], "Other examples include 'dog and bone' for phone and 'apples and pears' for stairs.", "medium"),
        ("In Cockney rhyming slang, what is a 'dog and bone'?", "A telephone", ["A dinner", "A policeman", "A home"], "Rhyming slang grew in the East End of London in the 19th century.", "easy"),
        ("What is a 'cuppa'?", "A cup of tea", ["A small beer", "A biscuit", "A cupboard"], "Britons drink an estimated 100 million cups of tea a day.", "easy"),
        ("What does the Scottish word 'wee' mean?", "Small", ["Wet", "Tired", "Clever"], "Used across Scotland and Northern Ireland for anything little.", "easy"),
        ("What does the Geordie word 'canny' usually mean in the North East?", "Good or pleasant", ["Careful", "Expensive", "Slow"], "In Scotland canny means shrewd; in Tyneside it is a general term of approval.", "medium"),
        ("What is a 'barm cake' in parts of northern England?", "A soft bread roll", ["A fruit loaf", "A pancake", "A sponge cake"], "The same roll is a bap, bun, batch, stottie or roll depending on the region.", "medium"),
        ("In Britain, what is the boot of a car?", "The luggage compartment", ["The bonnet", "The windscreen", "The glovebox"], "Americans call it the trunk; the bonnet is the hood.", "easy"),
        ("What do the British call the pavement that Americans call the sidewalk?", "The pavement", ["The curb", "The verge", "The footing"], "In the US, pavement usually means the road surface itself.", "easy"),
        ("What does 'Bob's your uncle' mean?", "And there you have it", ["You are in trouble", "Ask a relative", "It is expensive"], "Used to end an explanation of something simple.", "medium"),
        ("What is a 'gaff' in British slang?", "A home or flat", ["A mistake", "A party", "A pub"], "Separately, 'to blow the gaff' means to reveal a secret.", "medium"),
        ("Which word describes the Liverpool accent and its speakers?", "Scouse", ["Brummie", "Geordie", "Mackem"], "Brummie is Birmingham, Geordie is Newcastle and Mackem is Sunderland.", "medium"),
        ("What does the Welsh word 'cwtch' mean?", "A cuddle", ["A cupboard", "A hill", "A stream"], "Cwtch can mean both a hug and a small cosy space.", "hard"),
    ]
    for prompt, corr, dist, exp, diff in data_slang:
        q.append(make_q(prompt, corr, dist, exp, diff))

    # ---------------------------------------------------------------- Inventions, science & engineering
    data_science = [
        ("Which British scientist proposed the theory of evolution by natural selection?", "Charles Darwin", ["Alfred Russel Wallace", "Thomas Huxley", "Gregor Mendel"], "Darwin published 'On the Origin of Species' in 1859 after his voyage on HMS Beagle.", "easy"),
        ("Who formulated the laws of motion and universal gravitation at Cambridge?", "Isaac Newton", ["Robert Hooke", "Edmond Halley", "Michael Faraday"], "Newton's 'Principia' of 1687 is one of the most important works in science.", "easy"),
        ("Which Scottish inventor is credited with the first working television system?", "John Logie Baird", ["Alexander Graham Bell", "James Watt", "Charles Macintosh"], "Baird demonstrated a working televisor in London in 1926.", "medium"),
        ("Who discovered penicillin in 1928?", "Alexander Fleming", ["Howard Florey", "Joseph Lister", "Edward Jenner"], "Fleming noticed mould killing bacteria in a petri dish at St Mary's Hospital, London.", "easy"),
        ("Which English doctor pioneered the smallpox vaccine in 1796?", "Edward Jenner", ["Joseph Lister", "John Snow", "Alexander Fleming"], "Jenner used cowpox material, giving us the word vaccine from the Latin for cow.", "medium"),
        ("Which Scot improved the steam engine and gave his name to a unit of power?", "James Watt", ["George Stephenson", "Richard Trevithick", "Humphry Davy"], "The watt is named in his honour; his separate condenser transformed engine efficiency.", "easy"),
        ("Who invented the World Wide Web?", "Tim Berners-Lee", ["Alan Turing", "Clive Sinclair", "Charles Babbage"], "Berners-Lee wrote the first web browser and server at CERN in 1989-90.", "easy"),
        ("Which mathematician helped break the Enigma code at Bletchley Park?", "Alan Turing", ["Tommy Flowers", "Bertrand Russell", "John von Neumann"], "Turing's work on the Bombe machine is credited with shortening the Second World War.", "easy"),
        ("Which 19th-century Englishman designed a mechanical 'Analytical Engine'?", "Charles Babbage", ["Alan Turing", "Michael Faraday", "William Thomson"], "Babbage is often called the father of the computer; Ada Lovelace wrote notes on programming it.", "medium"),
        ("Who is regarded as the first computer programmer, working on Babbage's engine?", "Ada Lovelace", ["Mary Somerville", "Grace Hopper", "Dorothy Hodgkin"], "Lovelace's 1843 notes described an algorithm for computing Bernoulli numbers.", "medium"),
        ("Which engineer built the Clifton Suspension Bridge and the SS Great Britain?", "Isambard Kingdom Brunel", ["Thomas Telford", "Robert Stephenson", "Joseph Bazalgette"], "Brunel also built the Great Western Railway and Paddington station.", "medium"),
        ("Who designed London's Victorian sewer network after the Great Stink?", "Joseph Bazalgette", ["Isambard Kingdom Brunel", "John Nash", "Christopher Wren"], "Bazalgette's 1860s sewers ended cholera outbreaks and still serve the capital.", "hard"),
        ("Which British physicist discovered the electron in 1897?", "J. J. Thomson", ["Ernest Rutherford", "James Chadwick", "Paul Dirac"], "Thomson worked at the Cavendish Laboratory in Cambridge.", "medium"),
        ("Who co-discovered the structure of DNA at Cambridge in 1953?", "Francis Crick", ["Fred Hoyle", "Peter Medawar", "Archibald Garrod"], "Crick and James Watson built on X-ray work by Rosalind Franklin and Maurice Wilkins.", "medium"),
        ("Which scientist's X-ray images were crucial to solving the structure of DNA?", "Rosalind Franklin", ["Dorothy Hodgkin", "Barbara McClintock", "Marie Curie"], "Franklin's Photo 51 revealed the double helix; she died before the Nobel was awarded.", "medium"),
        ("Which British locomotive set the world steam speed record in 1938?", "Mallard", ["Flying Scotsman", "Rocket", "Evening Star"], "Mallard reached 126 mph on Stoke Bank, a record that still stands.", "medium"),
        ("Who built the locomotive 'Rocket', winner of the 1829 Rainhill Trials?", "George and Robert Stephenson", ["Isambard Kingdom Brunel", "Richard Trevithick", "Timothy Hackworth"], "Rocket set the template for steam locomotives for the next century.", "medium"),
        ("Which British astronomer discovered the planet Uranus in 1781?", "William Herschel", ["Edmond Halley", "John Flamsteed", "James Bradley"], "Herschel spotted it from his garden in Bath and first took it for a comet.", "hard"),
    ]
    for prompt, corr, dist, exp, diff in data_science:
        q.append(make_q(prompt, corr, dist, exp, diff))

    # ---------------------------------------------------------------- Traditions, customs & curiosities
    data_customs = [
        ("What is celebrated in Britain on 5 November?", "Bonfire Night", ["Remembrance Day", "May Day", "St Crispin's Day"], "Bonfire Night marks the failure of the Gunpowder Plot of 1605.", "easy"),
        ("What is traditionally worn to mark Remembrance Day?", "A poppy", ["A rose", "A thistle", "A daffodil"], "The red poppy recalls the flowers of the Flanders battlefields.", "easy"),
        ("Which day of Christmas is Boxing Day?", "26 December", ["24 December", "27 December", "1 January"], "The name may come from alms boxes opened for the poor the day after Christmas.", "easy"),
        ("What is the patron saint's day of England?", "St George's Day", ["St Andrew's Day", "St David's Day", "St Patrick's Day"], "St George's Day falls on 23 April, also Shakespeare's traditional birthday.", "easy"),
        ("On which date is St Andrew's Day, Scotland's national day?", "30 November", ["1 March", "23 April", "17 March"], "St David's Day is 1 March for Wales and St Patrick's 17 March for Ireland.", "medium"),
        ("What flower is the national emblem of Wales alongside the leek?", "The daffodil", ["The rose", "The thistle", "The shamrock"], "England has the rose, Scotland the thistle and Ireland the shamrock.", "easy"),
        ("What is the Trooping the Colour ceremony held to mark?", "The monarch's official birthday", ["The opening of Parliament", "Armistice Day", "The Commonwealth Games"], "Held each June on Horse Guards Parade, regardless of the monarch's actual birthday.", "medium"),
        ("Which annual event sees people chase a wheel of cheese down a hill in Gloucestershire?", "Cooper's Hill Cheese-Rolling", ["The Tetbury Woolsack Races", "Bog Snorkelling", "The Haxey Hood"], "Competitors tumble down a 1-in-2 slope after a 7 lb Double Gloucester.", "medium"),
        ("What is the traditional British term for a public holiday?", "A bank holiday", ["A feast day", "A rest day", "A fair day"], "The name comes from the Bank Holidays Act 1871, when banks were legally closed.", "easy"),
        ("Which sport is played on a village green with a jack and bowls?", "Lawn bowls", ["Croquet", "Petanque", "Shinty"], "Bowls has been played in Britain since at least the 13th century.", "medium"),
        ("What is Morris dancing traditionally accompanied by?", "Bells and handkerchiefs or sticks", ["Bagpipes and swords", "Drums and masks", "Fiddles and clogs only"], "English Morris dancing dates to at least the 15th century and varies by region.", "medium"),
        ("What does a British pub sign traditionally show?", "A picture as well as a name", ["Only the brewery crest", "Only the licensee's name", "Only opening hours"], "Pictorial signs date from a time when much of the population could not read.", "medium"),
        ("What time does the pub tradition of 'last orders' signal?", "The end of serving", ["Opening time", "Happy hour", "A lock-in"], "Traditionally followed by drinking-up time before the pub closes.", "easy"),
        ("Which Scottish celebration takes place at New Year?", "Hogmanay", ["Beltane", "Samhain", "Up Helly Aa"], "Hogmanay customs include first-footing, when the first visitor brings coal or whisky.", "medium"),
        ("What is the Shetland fire festival held each January called?", "Up Helly Aa", ["Hogmanay", "Beltane", "The Burryman"], "The festival ends with a replica Viking galley being set alight in Lerwick.", "hard"),
        ("In the ceremony of the keys at the Tower of London, what is locked each night?", "The Tower gates", ["The Crown Jewels vault", "The Traitors' Gate only", "The White Tower door"], "The ceremony has taken place nightly for around 700 years.", "medium"),
    ]
    for prompt, corr, dist, exp, diff in data_customs:
        q.append(make_q(prompt, corr, dist, exp, diff))

    return q


if __name__ == "__main__":
    questions = get_questions()
    print(f"uk-british generated {len(questions)} questions")
