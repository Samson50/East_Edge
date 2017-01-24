from characters import *

##== Choice Defaults ==##
choice_0 = [choice_000, choice_001,
            choice_002, choice_003]
choice_1 = [choice_004, choice_005]

##== Character Defaults ==##
ginger1 = female_white_ginger
brown1 = female_white_brown
basic_blocker = Blocker(32, 64, 1)
blocker_001 = NPC(cadet_npc, 30, 156, 3, blocker_text)
blocker_002 = NPC(cadet_npc, 162, 156, 2, blocker_text)

##== Text Defaults==##
text_D = ["What?", "What do you still want?", "", ""]
empty_res = TextBlock(text_D, [], -1, [])

##== Sally-port Guard ==##
text_000 = ["Jake! There are some serious regs",
            "violations going down in the",
            "barracks! I know you're just a",
            "plebe, but some day, you will be a",
            ##
            "leader! You will have graduated",
            "from East Edge! The greatest",
            "academy in the entire world!",
            "",
            ##
            "So, how will you handle it?",
            "DCX FLO",
            "",
            "",
            ##
            ""]

text_010 = ["Okay, man. That's your decision.",
            "You made it, now you have to",
            "stick to it. A good leader is true",
            "to themselves and isn't afraid",
            ##
            "to make unpopular decisions. The",
            "worst thing you can do is be",
            "fake. People can smell a fake",
            "leader from miles away.",
            ##
            "CTS 001",
            "",
            "",
            ""]


cadet_000 = NPC(white_rh_npc, 258, 96, 1, TextBlock(text_000, choice_0, 0, [
    TextBlock(text_010, choice_0, -2, [empty_res]),
    TextBlock(text_010, choice_0, -2, [empty_res]),
    TextBlock(text_010, choice_0, -2, [empty_res]),
    TextBlock(text_010, choice_0, -2, [empty_res]),
]))

##== CDT Johnson (1st Fight) ==##
text_001 = ["Hey, word spreads fast here. I",
            "heard what you said to Steve. You",
            "seem like a cool guy. I'm not",
            "about to hassle someone like you.",
            ###
            "CTS 002",
            "",
            "",
            ""]

text_002 = ["Hey, things get around pretty",
            "quick here and I heard what you",
            "said to Steve outside. I get it.",
            "You want do do the \' right thing\'",
            ###
            "You're still full of Kewl-Aid from",
            "Beast. I know how you feel, wanting",
            "to make sure that everything is",
            "Done by the book.",
            ###
            "That's what this is, right?",
            "DCX FLO",
            "",
            "",
            ###
            ""]

text_003 = ["Hey, I heard you told Steve outside",
            "that you were going to give everyone",
            "boards... Obviously you were kidding.",
            "Nobody is that crazy, right?",
            ##
            "Nobody is that crazy, right?",
            "DCX FLO",
            "",
            "",
            ##
            ""]

text_301 = ["Dude... what the fuck...",
            "",
            "",
            "",
            ##
            "ATK 001",
            "",
            "",
            ""]

text_302 = ["Haha, okay cool. I'm surprised Steve",
            "thought you were serious... He usually",
            "has a pretty good sense of humor...",
            "Oh well. See ya!",
            ###
            "CTS 002",
            "",
            "",
            ""]

text_004 = ["Need to figure something out for this",
            "response... Might change it... Might ",
            "leave it... Oh well. I guess you get to",
            "go on by",
            ###
            "CTS 002",
            "",
            "",
            ""]

text_005 = ["*Sigh* Well... I'm not about to",
            "just let someone like you walk into",
            " my company area with an attitude",
            "like that.",
            ###
            "ATK 001",
            "",
            "",
            ""]

text_006 = ["Okay, cool. Just remember that",
            "you don't have to do everything",
            "by the book to be a good leader.",
            "It's about the people.",
            ##
            "CTS 002",
            "",
            "",
            ""]

# Create texts 007 - 009
text_007 = ["Wow. You are fucked up in the head.",
            "It's cadets like you that graduate and",
            "give this place a bad reputation. I'm",
            "going to warn everyone that there's an",
            ##
            "asshole on the way. Good luck dicking",
            "people over now. You might as well forget",
            "about it and go back. This will take all",
            "the fun out of it for you.",
            ##
            "CTS 002",
            "",
            "",
            ""]

text_008 = ["Wow. I guess you're right... I hadn't",
            "looked at it like that. Listen, there's",
            "a right way and a wrong way to go about",
            "this. You could write NCORs, sure, but",
            ##
            "try talking it out first. Things aren't",
            "always black and white, and sometimes",
            "the best thing to do is give someone a",
            "break. I know you'll do the right thing.",
            ##
            "CTS 002",
            "",
            "",
            ""]

text_009 = ["You incapacitated CDT Jones.",
            "",
            "",
            "",
            ##
            "CTS 004",
            "",
            "",
            ""]

cadet_001 = Combatant(black_npc, 34, 64, 1, TextBlock(text_001, choice_0, 0, [
    TextBlock(text_001, [], 1, [empty_res]),
    TextBlock(text_002, choice_1, 1, [
        TextBlock(text_005, [], 2, [
            TextBlock(text_007, [], 3, [empty_res]),
            TextBlock(text_008, [], 3, [empty_res]),
            TextBlock(text_009, [], 3, [empty_res])
        ]),
        TextBlock(text_006, [], 2, [empty_res])
    ]),
    TextBlock(text_003, choice_1, 1, [
        TextBlock(text_301, [], 2, [
            TextBlock(text_007, [], 3, [empty_res]),
            TextBlock(text_008, [], 3, [empty_res]),
            TextBlock(text_009, [], 3, [empty_res])
        ]),
        TextBlock(text_302, [], 2, [empty_res])
    ]),
    TextBlock(text_004, [], 1, [empty_res])
]))