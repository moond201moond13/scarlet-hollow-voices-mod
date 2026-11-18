"""The Scarlet Hollow cast. Edit descriptions here, then re-make a voice with:
    py cast_voices.py --redo stella
(narrator and tabitha were approved by hand and are NOT made by the script.)

VOICE_DEFS: voice name -> (description, speaker id whose lines supply the sample text)
CAST:       speaker id in the game -> (voice name, default delivery style)
These descriptions were written from the character names and their lines, so check them
by ear. Anything marked CHECK is a guess.
"""

GENERIC_REF = "I never thought I would be standing here again, after all this time."

VOICE_DEFS = {
    # ---- main cast -------------------------------------------------------
    "stella": ("A young woman in her mid-twenties with a bright, warm, animated voice and an easy, casual delivery. Curious and enthusiastic, quick to laugh, with a clear, slightly breathy tone.", "stella"),
    "kaneeka": ("A woman in her mid-twenties with a low, smooth alto voice, rich and slightly husky. A mature, grounded adult delivery: dry, deadpan and unimpressed, with a sarcastic undertone and an easy, unhurried pace.", "kaneeka"),
    "oscar": ("A man in his late twenties with a warm, friendly, upbeat mid-range voice. Helpful and open, easygoing, with a hearty, slightly boyish delivery.", "oscar"),
    "avery": ("A young man in his twenties with a gentle, friendly, slightly shy mid-range voice. Warm and a little nervous, polite, with a soft, easy delivery.", "avery"),
    "sybil": ("An older woman in her sixties with a warm, refined, motherly voice. Gentle but firm, polished diction, a calm and kindly Southern lilt.", "sybil"),
    "doctor": ("A woman in her fifties with a crisp, firm, authoritative voice. Brisk and professional, dry, with a no-nonsense tone and clear diction.", "doctor"),
    "reese": ("A man in his late twenties with a relaxed, casual, slightly hoarse voice. Easygoing and wry, a bit reserved, with a lazy, understated delivery.", "reese"),
    "franklin": ("A man in his forties with a firm, flat, official voice. Measured and procedural, authoritative, with a slight Southern accent.", "franklin"),
    "duke": ("An older man in his sixties with a deep, gravelly, weathered Southern drawl. Gruff and blunt, rough around the edges, with a quiet warmth underneath.", "duke"),
    "wayne": ("A man with a calm, low, measured voice and formal, precise diction. Unhurried and composed, quietly unsettling, with an even, polished tone.", "wayne"),
    "gretchen": ("An elderly woman with a dignified, slightly raspy, theatrical voice and precise, old-fashioned diction. Proud and whimsical, with dry humor and a gentle, quavering warmth.", "gretchen"),
    "rosalina": ("A teenage girl with a clear, light, earnest voice. Sensible and a little tense, thoughtful, with a soft, slightly worried delivery.", "rosalina"),
    "irma": ("An older Southern woman in her sixties with a firm, weathered voice and a rural drawl. Motherly and stern, tired but resilient.", "irma"),
    "daniel": ("A young man in his late twenties with a warm, eager, earnest voice. Friendly and a little nervous, upbeat, with a gentle, slightly high-pitched delivery.", "daniel"),
    "derekson": ("A man in his fifties with a stern, measured, authoritative voice. Formal and firm, controlled, with a slight Southern accent.", "derekson"),
    "julius": ("A man in his thirties with an easy, teasing, hearty voice. Casual and friendly, working-class Southern, with a relaxed, joking delivery.", "julius"),
    "zachs": ("A man in his thirties with a rough, casual, drawling working-class Southern voice. Suspicious and blunt, with a lazy, gravelly tone.", "zachs"),
    "bo": ("A young man in his early twenties with a polite, soft, earnest Southern voice. Gentle and respectful, a little sad.", "bo"),
    "carmilla": ("A woman in her twenties with a breathy, haunting, dreamy voice. Poetic and intense, wistful and tender, with a faint, ethereal quality.", "carmilla"),
    "alexis": ("A teenage girl with a casual, bright, mildly sarcastic voice. Curious and chatty, with a light, youthful delivery.", "alexis"),
    "earl": ("An elderly man in his seventies with a creaky, gravelly, grumbling Southern voice. Gruff and wary, with a slow drawl.", "earl"),
    "isaacs": ("A man in his fifties with a weary, worried, low voice. Anxious and tired, with a rough, strained delivery.", "isaacs"),
    "miles": ("A young man in his early twenties with a snide, teasing, slightly nasal voice. Casual and sarcastic, restless, with a boyish, bored tone.", "miles"),
    "davis": ("A man in his thirties with an easy, flat, matter-of-fact voice. Casual and good-natured, a little tired, working-class Southern.", "davis"),
    "becka": ("A teenage girl with a brash, sharp, indignant voice. Sassy and quick to anger, bright and loud, with a bratty edge.", "becka"),
    "smith": ("A man in his fifties with a knowing, conspiratorial, gossipy Southern voice. Sly and easy, with a rough, lazy drawl.", "smith"),
    "dustin": ("A thick, rumbling, gravelly voice that speaks slowly and simply, in broken English. Gentle and earnest, like a large kindly creature.", "dustin"),
    "janey": ("A woman in her sixties with a sweet, warm, slightly quavering voice. Kindly and chatty, honeyed and gentle, with a church-lady lilt.", "janey"),
    "scraps": ("An older man with a gruff but gentle, humble voice and a slow, warm, rough drawl. Modest and sincere, with a quiet authority that others listen to.", "scraps"),
    "harrison": ("A young man in his twenties with a casual, easygoing, slightly hesitant voice. Chatty and modern, a little awkward.", "harrison"),
    "zane": ("A teenage boy with a bright, eager, boyish voice. Enthusiastic and goofy, with a youthful, slightly cracking delivery.", "zane"),
    "daisy": ("A young woman with a bright, breathless, urgent voice. Eager and earnest, quick and energetic.", "daisy"),
    "rodriguez": ("A man in his forties with a friendly, hearty, easy voice. Working-class, warm, with a casual, joking delivery.", "rodriguez"),
    "bs": ("A man in his late twenties with a relaxed, chatty, easygoing voice and a friendly grin in his tone. Casual and rambling, a little rough, with a cheerful, slightly unsettling ease, as if everything is a joke.", "bs"),
    "mayor": ("A man in his fifties with a bombastic, smarmy, hearty voice. Smooth-talking and oily, a politician's grin in his tone.", "mayor"),
    "beckamom": ("A woman in her forties with a tense, strained, indignant voice. Protective and sharp, close to shrill when upset.", "beckamom"),
    "dustinmom": ("A deep, rumbling, thick voice speaking in simple broken English. Protective and stern, with a heavy, gravelly weight.", "dustinmom"),
    "johnson": ("A middle-aged man in his forties with a sly, teasing, drawling Southern voice. Casual and knowing, a working miner, a little mischievous.", "johnson"),
    "winnie": ("A woman in her forties with a prim, cultured, cutting voice. Dry and snide, polished, with a knowing edge.", "winnie"),
    "huggby": ("An older man with a loud, barking, impatient, gravelly Southern voice. Gruff and commanding, an old sheriff.", "huggby"),
    "froufrou": ("A haughty, snooty, nasal voice with a French accent. Pompous and disdainful, polished, with a sneering, theatrical delivery.", "froufrou"),
    "tate": ("A man in his forties with an easy, cheerful, chatty Southern voice. Friendly and relaxed.", "tate"),
    "pixel": ("A bright, chirping, playful voice with a silly, cheerful, mischievous quality, like a talkative cat.", "pixel"),
    "spot": ("A rough, dry, cynical, drawling voice. Gruff and wisecracking, with a gravelly working-class edge.", "spot"),
    "tan": ("A brash, nasal, tough-talking voice with an old-fashioned, wisecracking swagger. Gruff and quick.", "tan"),
    "brown": ("A gruff, stubborn, grumbling voice, defensive and flustered, with a rough working-class tone.", "brown"),
    "security": ("A man with a flat, bored, blunt voice. Authoritative and dry.", "security"),
    "woman": ("A woman with a creaky, hushed, insinuating voice. Knowing and mysterious, with a thin, rasping quality.", "woman"),
    "witch": ("A woman with a silken, calm, cold voice. Sly and soothing, with a smooth, deliberate, faintly menacing delivery.", "witch"),
    "baker": ("A man in his thirties with a loud, animated, brash voice. Indignant and expressive, a rough working-class miner.", "baker"),
    "eldritch": ("A low, rumbling, otherworldly voice, slow and eerie, speaking in poetic riddles, calm and unsettling.", "mountainlion"),
    "enoch": ("An older man with a weary, hoarse, gruff voice. Tired and worn, with a slow, careful delivery.", "enoch"),
    "police": ("A man with a dry, firm, professional voice. Calm and official.", "police"),
    "dad": ("A man in his fifties with a warm, gentle, tired voice, fatherly and sincere.", "dad"),
    # ---- shared voices for minor characters ------------------------------
    "edwardine": ("A woman in her sixties with a soft, warm, wistful voice. Gentle and tender, a little frail, with a quiet, loving sincerity. CHECK: guessed from her letters to Tabby.", None),
    "man_working": ("A man in his forties with a rough, casual, working-class Southern voice. Plain-spoken and a bit weathered.", "coal_miner1"),
    "man_old": ("An older man in his sixties with a gruff, worn, slow Southern voice. Weathered and stern.", "goscar"),
    "woman_generic": ("A woman in her forties with a plain, friendly, slightly tired Southern voice. Direct and down to earth.", "crowd2"),
    "woman_stern": ("A woman with a sharp, cold, commanding voice. Clipped and unimpressed, with a stern edge.", "joan"),
    "woman_young": ("A young woman in her twenties with a soft, polite, clear voice. Gentle and a little reserved.", "young_woman"),
    "child": ("A small child's voice, around six years old, high and bright. Innocent, blunt and curious.", "tulip"),
    "critter": ("A small, quick, squeaky comedic animal voice, high and chirpy, with a lot of attitude.", None),
}

# speaker id in the game -> (voice name, default delivery style; "" = none)
OLDER = "The same person many years later, older and more weathered."
CAST = {
    "": ("narrator", ""),
    "n": ("narrator", "Hushed, eerie and dreamlike, slow."),
    "tabitha": ("tabitha", ""),
    "stella": ("stella", ""), "kaneeka": ("kaneeka", ""), "oscar": ("oscar", ""),
    "avery": ("avery", ""), "sybil": ("sybil", ""), "sybil_forsyth": ("sybil", ""),
    "doctor": ("doctor", ""), "reese": ("reese", ""),
    "reesem": ("reese", "Manic, euphoric and menacing, supremely confident."),
    "franklin": ("franklin", ""), "duke": ("duke", ""), "wayne": ("wayne", ""),
    "wayne_unknown": ("wayne", "Hesitant, quiet and shy."),
    "gretchen": ("gretchen", ""),
    "finalgretchen": ("gretchen", "Dreamy, eerie, tender and unsettling."),
    "rosalina": ("rosalina", ""), "irma": ("irma", ""), "daniel": ("daniel", ""),
    "derekson": ("derekson", ""), "julius": ("julius", ""), "zachs": ("zachs", ""),
    "bo": ("bo", ""), "carmilla": ("carmilla", ""), "alexis": ("alexis", ""),
    "earl": ("earl", ""), "isaacs": ("isaacs", ""), "miles": ("miles", ""),
    "davis": ("davis", ""), "becka": ("becka", ""), "smith": ("smith", ""),
    "dustin": ("dustin", ""), "dustinmom": ("dustinmom", ""), "janey": ("janey", ""),
    "scraps": ("scraps", ""), "harrison": ("harrison", ""), "zane": ("zane", ""),
    "daisy": ("daisy", ""), "rodriguez": ("rodriguez", ""), "bs": ("bs", ""),
    "mayor": ("mayor", ""), "beckamom": ("beckamom", ""), "johnson": ("johnson", ""),
    "winnie": ("winnie", ""), "huggby": ("huggby", ""), "froufrou": ("froufrou", ""),
    "cat": ("froufrou", ""), "tate": ("tate", ""), "pixel": ("pixel", ""),
    "spot": ("spot", ""), "tan": ("tan", ""), "brown": ("brown", ""),
    "security": ("security", ""), "woman": ("woman", ""), "witch": ("witch", ""),
    "baker": ("baker", ""), "enoch": ("enoch", ""), "police": ("police", ""),
    "dad": ("dad", ""),
    # ids that only appear as the real speaker of "speaker"/"unknown"/"extend" lines
    "ugoat": ("critter", ""), "edwardine": ("edwardine", ""),
    "man_working": ("man_working", ""), "woman_generic": ("woman_generic", ""),
    # u-prefixed ids look like "same person, not yet identified": use the base voice
    "ukaneeka": ("kaneeka", ""), "uduke": ("duke", ""), "ubecka": ("becka", ""),
    "udbecka": ("becka", ""), "uzane": ("zane", ""), "udzane": ("zane", ""),
    "uearl": ("earl", ""), "uderekson": ("derekson", ""), "ualexis": ("alexis", ""),
    "ubeckamom": ("beckamom", ""), "ubrown": ("brown", ""), "uspot": ("spot", ""),
    "utan": ("tan", ""), "ujaney": ("janey", ""), "uwinnie": ("winnie", ""),
    "uirma": ("irma", ""), "urosalina": ("rosalina", ""), "udrosalina": ("rosalina", ""),
    # g-prefixed ids look like grown-up versions: base voice, older delivery (CHECK)
    "gkaneeka": ("kaneeka", OLDER), "gavery": ("avery", OLDER), "gstella": ("stella", OLDER),
    "gzane": ("zane", OLDER), "galexis": ("alexis", OLDER), "grosalina": ("rosalina", OLDER),
    "goscar": ("man_old", ""),
    # mixed ids
    "staneeka": ("stella", ""), "taneeka": ("tabitha", ""), "tabithakaneeka": ("tabitha", ""),
    "allteens": ("alexis", ""),
    # shared minor voices
    "coal_miner1": ("man_working", ""), "coal_miner2": ("man_working", ""),
    "coal_miner3": ("man_working", ""), "coal_miner4": ("man_working", ""),
    "miner": ("man_working", ""), "beckadad": ("man_working", ""),
    "paramedic": ("man_working", ""), "bus_driver": ("man_working", ""),
    "chef": ("man_working", ""), "preacher": ("man_working", ""), "man": ("man_working", ""),
    "fmshaw": ("man_working", ""), "fmscarlet": ("man_working", ""),
    "charlie": ("man_working", ""), "teddy": ("man_working", ""), "uteddy": ("man_working", ""),
    "crowd1": ("man_working", "Angry, shouting."), "crowd3": ("man_working", "Angry, shouting."),
    "crowd2": ("woman_generic", "Angry, shouting."),
    "joan": ("woman_stern", ""), "young_woman": ("woman_young", ""), "bride": ("woman_young", ""),
    "bertie": ("woman", ""), "verena": ("woman", ""),
    "tulip": ("child", ""), "child": ("child", ""),
    "gp": ("child", "Plaintive, anxious and worried."),
    "mountainlion": ("eldritch", ""), "eldritch_unknown": ("eldritch", ""),
    "deer": ("eldritch", ""), "chicken": ("eldritch", ""),
    "opossum": ("critter", ""), "raccoon": ("critter", ""), "stick": ("critter", ""),
    "goat": ("critter", ""), "bird": ("critter", ""), "bat": ("critter", ""),
    "otherbat": ("critter", ""), "bugs": ("critter", ""), "momopossum": ("critter", ""),
    "bothopossums": ("critter", ""), "ggretchen": ("critter", ""), "ggretchen1": ("critter", ""),
    # online commenters and similar
    "moth": ("harrison", ""), "hidden": ("harrison", ""), "lucky": ("harrison", ""),
    "uncle": ("harrison", ""), "gary": ("harrison", ""), "sung": ("harrison", ""),
}

# Not voiced yet (need a game-side rule first): the player, "extend" continuation
# lines, and the placeholders whose real speaker changes while the game runs.
NOT_YET = {"p", "extend", "speaker", "unknown"}
