from nltk.parse.generate import generate
from nltk import CFG
import random

pos_grammar = CFG.fromstring("""

S -> NP

NP -> Det AP

Det -> "my" | "our" | "everyone's" | "your" | "someone's" | "no one's"

AP -> Adj N

Adj -> "favorite" | "spiritual" | "dress-wearing" | "constant" | "meme-creating" | "occasional" | PropN V | "fully coys" | "January transfer window" | "perennially injured" | "spot-kick" | "sleeping" | "suffering" | "broken" | "adorably" | "intelligent" | "not stupid" | "stupid" | "tie die" | "nocturnal" | "Marxist" | "unfortunate"

PropN -> "Mauricio Pochettino" | "Jose Mourinho" | "Harry Kane" | "Tanguy Ndombele" | "Son Heung-Min" | "Joe Hart" | "Pierre-Emile Hojbjerg" | "Erik Lamela" | "Mousa Dembele" | "Troy Parrott" | "Spurs" | "Tottenham" | "Arsenal"

V -> "hating" | "loving" | "admiring" | "skeptic" | "watching" | "enthusiast"

N -> "man" | "boy" | "cheerleader" | "hater" | "guy" | "patron saint" | "saint" | "friend" | "cunt" | "analyst" | "nonce" | "bombshell" | "enthusiast" | "bloke" | "producer" | "secretary of state" | "lolly pop" | "champion" | "beauty" | "specialist" | "mistake" | "scout" | "pal" | "signing" | "superfan" | "apologist" | "director of football" | "extraordinaire"

""")

noun_grammar = CFG.fromstring("""

S -> NP PP

NP -> Det N

Det -> "a" | "the" | "some" | "one"

N -> "man" | "boy" | "guy" | "bloke" | "cunt" | "nonce" | "champion"

PP -> P VP

P -> "who" | "that"

VP -> V PropN | Adv V PropN

Adv -> "fucking" | "really" | "sometimes"

V -> "likes" | "hates" |  "loves" | "yells about" | "is skeptical about"

PropN -> "Mauricio Pochettino" | "Jose Mourinho" | "Harry Kane" | "Tanguy Ndombele" | "Son Heung-Min" | "Joe Hart" | "Pierre-Emile Hojbjerg" | "Erik Lamela" | "Mousa Dembele" | "Troy Parrott" | "Spurs" | "Tottenham" | "Arsenal" | "low blocks" | "mid blocks" | "spreadsheets" | "set pieces" | "scanning" | "Marxism" | "the internet" | "Troy Deeney" | "the Athletic" | "tie dye" | "game state" | "xG" | "appapapi appapapa" | "positivity, belief" | "Christian Eriksen" | "Dele Alli" | "Serge Aurier" | "guitars"

""")

def get_n_introductions(number) :
    r = random.randint(0,1)

    if r == 1 :
        all_pos_sentences = list(generate(pos_grammar))
        pos_number = len(all_pos_sentences)
        print(pos_number)
        pos_sentence = all_pos_sentences[random.randint(0,pos_number)]
        return "Our tactics guy, and " + ' '.join(pos_sentence) + ", Nathan A Clark. Hello, Nathan."
    else :
        all_noun_sentences = list(generate(noun_grammar))
        noun_number = len(all_noun_sentences)
        print(noun_number)
        noun_sentence = all_noun_sentences[random.randint(0,noun_number)]
        return "Our tactics guy, and " + ' '.join(noun_sentence) + ", Nathan A Clark. Hello, Nathan."
