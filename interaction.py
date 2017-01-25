import random
import room_data
from mini_game import *

##== Cut-Scenes ==##
m_o = [["00:d"]*16+["00:r"]*16+["00:d"]*48+["00:r"]*16+["00:d"]*32+["00:r"]*16+["C:2:64:56"],[]]
s_00 = [["M:d"]*16+["M:u"]+["00:d"]*16+["00:l"]*82+["R:0:62"], ["R:7:0:62"]]
s_01 = [["M:r"]*16+["01:d"]*28+["01:r"]*16+["01:d"]*32+["01:l"]*18+["01:f:2"]+["N:15:43"], ["N:4:15:43:32:184"]]
s_02 = [["01:u"]*16+["01:r"]*8+["R:1:15"], ["R:4:1:15"]]
s_03 = [["R:1:15"], ["R:4:1:15"]]

cut_scenes = [m_o, s_00, s_01, s_02, s_03]


class TextBox:
    def __init__(self, surface):
        self.surface = surface
        self.combat = CombatBox(surface)
        self.text = []
        self.message = ["", "", "", ""]
        self.current_message = ["", "", "", ""]
        self.current_pointer = 0
        self.font = pygame.font.Font(sans_bold, 14)
        self.text_box = img_text_box
        self.message_marker = 0
        self.decision_marker = 0
        self.yes = img_yes
        self.no = img_no
        self.decision = img_decision

    def getEvents(self, text_block, cadet):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_f:
                    if self.message != ["", "", "", ""] and "DCX" not in self.message[1]:
                        for i in range(0, 4):
                            self.current_message[i] += self.message[i]
                            self.message[i] = ""
                    else:
                        return self.update_message(text_block, cadet)
                if event.key == K_RIGHT:
                    self.decision_marker += 1
                if event.key == K_LEFT:
                    self.decision_marker -= 1
                if event.key == K_UP:
                    self.decision_marker -= 2
                if event.key == K_DOWN:
                    self.decision_marker += 2

            self.decision_marker %= (max(len(text_block.choices),1))
        return "Talking"

    def draw_text(self, surface, text_block, backdrop):
        surface.blit(backdrop, (0,0))
        surface.blit(self.text_box, (10, 200))
        delta = 0
        if (not "DCX" in self.message[1]):
            if len(self.message[self.current_pointer]) > 0:
                self.current_message[self.current_pointer] += self.message[self.current_pointer][0]
                self.message[self.current_pointer] = self.message[self.current_pointer][1:]
                # Play sound blurb
            elif self.current_pointer < 3:
                self.current_pointer += 1
            for line in self.current_message:
                text_object = self.font.render(line, 1, (0,0,0))
                text_rect = text_object.get_rect()
                text_rect.topleft = (30,210+delta)
                delta += 20
                surface.blit(text_object, text_rect)
        else:
            text_object = self.font.render(self.message[0], 1, (0,0,0))
            text_rect = text_object.get_rect()
            text_rect.topleft = (30,210)
            surface.blit(text_object, text_rect)
            i = 0
            for choice in text_block.choices:
                surface.blit(choice, (15+(i%2)*140,230+(i/2)*30))
                i += 1
            surface.blit(self.decision, (50+140*(self.decision_marker%2),235+(self.decision_marker/2)*30))

        pygame.display.update()

    def update_message(self, text_block, cadet):
        self.current_message = ["", "", "", ""]
        self.current_pointer = 0
        for i in range(0,4):
            if ("DCX" in self.message[i]):
                if ("CTX" in self.message[i]):
                    story.decisions[text_block.result] = self.decision_marker
                    story.current_scene = int(self.message[i].split(" ")[2])
                    self.message_marker = 0
                    self.message = ["", "", "", ""]
                    return "Cut_Scene"
                elif ("FLO" in self.message[i]):
                    story.decisions[text_block.result] = self.decision_marker
                    self.message_marker = 0
                    self.message = ["", "", "", ""]
                    return "Talking"
                else:
                    story.decisions[text_block.result] = self.decision_marker
                    self.message_marker = 0
                    self.message = ["", "", "", ""]
                    return "Moving"

            else:
                if (self.message_marker == len(text_block.text)):
                    self.message_marker = 0
                    self.message = ["", "", "", ""]
                    return "Moving"
                else:
                    if ("CTS" in text_block.text[self.message_marker]):
                        story.decisions[text_block.result] = 0
                        story.current_scene = int(text_block.text[self.message_marker].split(" ")[-1])
                        self.message_marker = 0
                        self.message = ["", "", "", ""]
                        return "Cut_Scene"

                    elif ("ATK" in text_block.text[self.message_marker]):
                        story.decisions[text_block.result] = 0
                        story.opponent = int(text_block.text[self.message_marker].split(" ")[1])
                        self.message_marker = 0
                        self.message = ["","","",""]
                        self.fight(cadet)

                    else:
                        self.message[i] = text_block.text[self.message_marker]
                        self.message_marker += 1
        return "Talking"
    def fight(self, cadet):
        self.combat.set_up(room_data.ROOMS[story.current_room].non_player_characters[story.opponent], cadet)
        self.mode = "Fighting"
        while self.mode == "Fighting":
            self.combat.get_events(self.surface)
            self.mode = self.combat.show(self.surface, cadet)


class Choice:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

    def show(self, surface):
        surface.blit(self.image, (self.x, self.y))

# Response format:
#[ Int: Index of current action, [Text List: first response], [damage quantity, damage target (0 = health, 1 = morale)], [Text List: second response]]
#
class Attack(Choice):
    def __init__(self):
        Choice.__init__(self,act_attack, 79-act_attack.get_width()/2, 207)

    def run(self, cadet, opponent):
        damage = cadet.strength + (cadet.strength/10)*(random.randint(0,5)/5)
        res = [0,["You muster your strength and take",
                   "a swing at your opponent's face...",
                   "... Your swing connects, causing",
                   "{0} damage".format(damage)],[damage, 0]]
        res += [["Enraged, CDT {0} retaliates!".format(opponent.name),
                 "He screams obscenities as he",
                 "throws a right cross at your",
                 "face!",
                 "OPP 0 0"]]
        res += [["The hit connects!",
                 "You stagger backward,",
                 "taking {0} physical damage",
                 "",
                 "ATE"]]
        return res


class NCOR(Choice):
    def __init__(self):
        Choice.__init__(self, act_NCOR, 213-act_NCOR.get_width()/2, 207)

    def run(self, cadet, opponent):
        res = []
        if opponent.NCOR_effect == 1:
            morale_damage = cadet.eloquence + (cadet.eloquence / 10) * (random.randint(0, 5) / 5)
            res += [0, ["You write a strongly worded NCOR",
                        "on CDT {0} and send it to their".format(opponent.name),
                        "chain of command. CDT {0}".format(opponent.name),
                        "takes {0} points of morale damage.".format(morale_damage)], [morale_damage, 1]]
            res += [["CDT {0} gives you a strongly worded".format(opponent.name),
                     "piece of their mind. Nobody likes",
                     "the guy who writes NCORs all the",
                     "time...",
                     "OPP 0 1"]]
            res += [["CDT {0}'s rebuke causes".format(opponent.name),
                     "you to question yourself...",
                     "you take {0} points of morale",
                     "damage",
                     "ATE"]]
        else:
            res += [0, ["You write a strongly worded NCO",
                        "on CDT {0} and send it to their".format(opponent.name),
                        "chain of command. CDT {0}".format(opponent.name),
                        "straight-up doesn't give a fuck."], [0, 0]]
            res += [["CDT {0} viciously mocks".format(opponent.name),
                     "you for your naive attempt",
                     "to shame them into compliance.",
                     "That's embarrassing...",
                     "OPP 0 1"]]
            res += [["Your shaming backfired!",
                     "Your weak leadership caused",
                     "you to take {0} points of",
                     "morale damage",
                     "ATE"]]
        return res


class Lead(Choice):
    def __init__(self):
        Choice.__init__(self, act_lead, 79-act_lead.get_width()/2, 252)

    def run(self, cadet, opponent):
        res = [0, ["You harness the power of",
                   "your inspirational leadership",
                   "to bring CDT {0} into line".format(opponent.name),
                   "with the standard."],
               [0, 0]]

        if opponent.helped >= opponent.help_needed:
            res += [["You can haz leading",
                    "",
                    "",
                    "",
                    "END 0 {0} 1".format(opponent.result)]]

        else:
            res += [["CDT {0} is not impressed with".format(opponent.name),
                    "your feigned leadership. Maybe",
                    "if you cared, your leadership",
                    "would be more effective...",
                    "OPP 0 1"]]
            res += [["CDT {0}'s rejection of your".format(opponent.name),
                     "leadership causes you to ",
                     "question yourself. you take {0}",
                     "morale damage.",
                     "ATE"]]

        return res


class Help(Choice):
    def __init__(self):
        Choice.__init__(self, act_help, 213-act_help.get_width()/2, 252)

    def run(self, cadet, opponent):
        opponent.helped += 1
        res = [0, ["You genuinely try to help",
                   "CDT {0} understand what".format(opponent.name),
                   "they are doing wrong...",
                   ""]]
        if opponent.helped > opponent.help_needed:
            damage = (opponent.helped/opponent.help_needed)*cadet.eloquence*85/100
            res[1] += ["CDT {0} shuffles awkwardly".format(opponent.name),
                       "as you continue to berate them",
                       "CDT {0} takes {1} additional".format(opponent.name,damage),
                       "morale damage..."]
            res += [[damage,1]]
            res += [["CDT {0} appears defeated".format(opponent.name),
                    "no action is taken against",
                    "you.",
                    "",
                    "ATE"]]
        elif opponent.helped == opponent.help_needed:
            res[1] += ["CDT {0} now understands why".format(opponent.name),
                       "they are wrong. They look at",
                       "you with the appreciation that",
                       "accompanies professional development"]
            res += [[0,1]]
            res += [["CDT {0} is too busy bathing".format(opponent.name),
                    "in the warm light of your",
                    "professionalism to retaliate",
                    "you take no damage.",
                    "ATE"]]
        else:
            res[1] += ["CDT {0} glares at you warily.".format(opponent.name),
                       "Being corrected sucks...",
                       "but maybe you have a point...",
                       ""]
            res += [[0,1]]
            res += [["CDT {0} mocks you for".format(opponent.name),
                    "drinking the Kool-Aid and",
                    "thinking you're better than",
                    "everyone else...",
                    "OPP 0 1"]]
            res += [["You question yourself for",
                    "a moment...",
                    "You take {0} points of",
                    "morale damage",
                    "ATE"]]
        return res


class CombatBox:
    def __init__(self, surface):
        self.surface = surface
        self.background = combat_surface
        self.pointer = combat_decision
        self.decision = 0
        self.level = 0
        self.i = 0; self.j = 0
        self.levels = [self.i, self.j]
        self.mode = "Fighting"
        self.display_mode = "choose"
        self.response = [[],[]]
        self.choices = [Choice(choice_act,47,207),
                        Choice(choice_analyze,164,207),
                        Choice(choice_item,34,252),
                        Choice(choice_leave,169,252)]
        self.acts = [Attack(),NCOR(),Lead(),Help()] #list of players action classes
        self.text_box = combat_text
        self.text = []
        self.message = ["", "", "", ""]
        self.message_marker = 0
        self.font = pygame.font.Font(sans_bold, 14)
        self.temp_items = []
        self.mini_game = MiniGame()
        self.mini_map = 0
        self.opp_target = 0
        self.fade = fade.convert()
        self.fade_out = 0

    def set_up(self,opponent,cadet):
        cadet.face = 1
        cadet.pose = 9
        self.opponent = opponent
        self.opponent.look_at(0)
        self.mode = "Fighting"
        self.cadet = cadet
        self.items = cadet.items

    def analyze(self):
        first = [0,["You take a moment and try to","analyze the situation","",""]]
        first += [[0, 0],["You notice some thing","","","","ATE"]]
        return first

    def leave(self):
        ## Generate Randomly
        escape = 0
        if escape < self.opponent.escape_chance:
            return [0,["You try to leave", "", "", ""], [0, 0], ["You leave the opponent confused.", "", "", "", "ATE"]]
        else:
            return [0,["You try to leave...", "", "", ""], [0, 0], ["But you can't get away that easily!", "", "", "", "OPP 0 1"], ["CDT {0} mocks you for your",
                                                                                                                                    "cowardice in trying to flee",
                                                                                                                                    "you take {0} morale damage",
                                                                                                                                    "",
                                                                                                                                    "ATE"]]

    def update_message(self):
        if self.response[0] == 0:
            if self.text == []: self.text = self.response[1]
        elif self.response[0] == 2:
            if self.text == []: self.text = self.response[3]
        elif self.response[0] == 4:
            if self.text == []: self.text = self.response[4]
        for i in range(0, 4):
            if self.message_marker == len(self.text):
                self.message_marker = 0
                self.text = []
                self.message = ["","","",""]
                self.response[0] += 1
                break
            else:
                if ("ATE" in self.text[self.message_marker]):
                    self.display_mode = "choose"
                    self.message_marker = 0
                    self.text = []
                    self.message = ["","","",""]
                    self.level = 0
                    self.decision = 0
                    break
                elif ("OPP" in self.text[self.message_marker]):
                    self.mini_map = int(self.text[self.message_marker].split(" ")[1])
                    self.opp_target = int(self.text[self.message_marker].split(" ")[2])
                    self.message_marker = 0
                    self.text = []
                    self.message = ["", "", "", ""]
                    self.response[0] += 1
                    break
                elif ("END" in self.text[self.message_marker]):
                    # End format: END [end type, who lost] [story point] [result val] [follow on?]
                    res = self.text[self.message_marker].split(" ")
                    self.display_mode = "ending"
                    self.end_type = res[1]
                    story.decisions[int(res[2])] = int(res[3])
                else:
                    self.message[i] = self.text[self.message_marker]
                    self.message_marker += 1


    def get_events(self,surface):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_LEFT: self.decision -= 1
                if event.key == K_RIGHT: self.decision += 1
                if event.key == K_UP: self.decision -= 2
                if event.key == K_DOWN: self.decision += 2

                if event.key == K_f:
                    if self.display_mode == "choose":
                        if self.level == 0:
                            ## Analyze
                            if self.decision == 1:
                                self.response = self.analyze()
                                self.display_mode = "action"
                                self.update_message()
                            ## Leave
                            if self.decision == 3:
                                self.response = self.leave()
                                self.display_mode = "action"
                                self.update_message()

                            else:
                                self.levels[self.level] = self.decision
                                self.level += 1
                                self.decision = 0

                        elif self.level == 1:
                            ## Specific ACTION
                            if self.levels[0] == 0:
                                self.response = self.acts[self.decision].run(self.cadet, self.opponent)
                                self.display_mode = "action"
                                self.update_message()
                            ## Items
                            if self.levels[0] == 2:
                                self.response = self.items[self.decision].run(self.cadet, self.opponent)
                                self.display_mode = "action"
                                self.update_message()

                    elif self.display_mode == "action":
                        if self.response[0] == 0 or self.response[0] == 2 or self.response[0] == 4:
                            self.update_message()
                        #if self.response[0] == 1:
                        #    self.response[0] += 1

                if event.key == K_d:
                    if self.level > 0 : self.level -= 1
                    self.decision = 0
        if self.level == 1 and self.levels[0] == 2: self.decision %= len(self.items)
        else: self.decision %= 4
        return self.mode

    def show(self, surface,cadet):
        surface.blit(self.background, (0,0))

        surface.blit(cadet.sprites[10], (55, 110))

        surface.blit(self.opponent.show_base(), (215, 110))

        ## Status Bars
        health_blocks = ((cadet.health*64)/cadet.max_health)*63/64
        for i in range(0,health_blocks): surface.blit(health_block, (9+i*2, 9))
        morale_blocks = ((cadet.morale*64)/cadet.max_morale)*63/64
        for i in range(0,morale_blocks): surface.blit(morale_block, (9+i*2, 31))

        ## Opponent Status
        opponent_health = ((self.opponent.health*64)/(self.opponent.max_health))*63/64
        for i in range(0, opponent_health): surface.blit(health_block, (164+i*2, 9))
        opponent_morale = ((self.opponent.morale*64)/self.opponent.max_morale)*63/64
        for i in range(0,opponent_morale): surface.blit(morale_block, (164+i*2, 31))

        surface.blit(overlay, (7,7))
        surface.blit(overlay, (7,29))
        surface.blit(overlay, (162,7))
        surface.blit(overlay, (162,29))

        if self.display_mode == "choose":

            if self.level == 0:
                surface.blit(self.pointer, (14 + (self.decision % 2) * 137, 198 + (self.decision / 2) * 45))
                for choice in self.choices:
                    choice.show(surface)

            if self.level == 1:
                if self.levels[0] == 0:
                    surface.blit(self.pointer, (14 + (self.decision % 2) * 137, 198 + (self.decision / 2) * 45))
                    for action in self.acts:
                        action.show(surface)

                if self.levels[0] == 2:
                    surface.blit(img_items, (12,196))
                    surface.blit(item_decision, (15 + (self.decision % 8) * 34, 206 + (self.decision / 8) * 34))
                    for item in range(0,len(self.items)):
                        self.items[item].show(surface,15+(item%8)*34,199+(item/8)*34)

        if self.display_mode == "action":
            if self.response[0] == 0:
                surface.blit(self.text_box, (4,188))
                delta = 0
                for line in self.message:
                    text_object = self.font.render(line, 1, (255, 255, 255))
                    text_rect = text_object.get_rect()
                    text_rect.topleft = (30, 205 + delta)
                    delta += 20
                    surface.blit(text_object, text_rect)

            elif self.response[0] == 1:
                if self.response[2][1] == 0:
                    self.opponent.health -= self.response[2][0]
                else:
                    self.opponent.morale -= self.response[2][0]

                self.response[0] += 1
                self.update_message()


            elif self.response[0] == 2:
                surface.blit(self.text_box, (4, 188))
                delta = 0
                for line in self.message:
                    text_object = self.font.render(line, 1, (255, 255, 255))
                    text_rect = text_object.get_rect()
                    text_rect.topleft = (30, 205 + delta)
                    delta += 20
                    surface.blit(text_object, text_rect)

            elif self.response[0] == 3:
                if (self.mini_map != 99):
                    self.mini_game.gen_map(mini_maps[self.mini_map])
                    self.opp_damage = self.opponent.strength - self.opponent.strength * (self.mini_game.run(surface) / 30) #* (2 / 3)
                    self.response[4][2] = self.response[4][2].format(self.opp_damage)
                self.response[0] += 1
                self.update_message()
                if self.opp_target == 0:
                    self.cadet.health -= self.opp_damage
                else:
                    self.cadet.morale -= self.opp_damage

            elif self.response[0] == 4:
                surface.blit(self.text_box, (4, 188))
                delta = 0
                for line in self.message:
                    text_object = self.font.render(line, 1, (255, 255, 255))
                    text_rect = text_object.get_rect()
                    text_rect.topleft = (30, 205 + delta)
                    delta += 20
                    surface.blit(text_object, text_rect)

        if self.cadet.health <= 0:
            print "health end"

        if self.cadet.morale <= 0:
            print "morale end"

        if self.opponent.health <=0:
            print "health win"

        if self.opponent.morale <= 0:
            print "morale win"

        if self.display_mode == "ending":
            if (self.fade_out < 255):
                self.fade_out += 5
                self.fade.set_alpha(self.fade_out)
                surface.blit(self.fade, (0,0))

            else:
                return "Post-Fight"

        pygame.display.update()
        return "Fighting"



