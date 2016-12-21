import pygame


## Rooms ##

sally_port_img = pygame.image.load("surfaces/sally_port.png")
barracks_a = pygame.image.load("surfaces/CADET_room_a.png")
barracks_b = pygame.image.load("surfaces/CADET_room_b.png")
hallway = pygame.image.load("surfaces/CADET_hall.png")
stairwell = pygame.image.load("surfaces/CADET_stairwell_working.png")
stairwell_ground = pygame.image.load("surfaces/CADET_stairwell_ground.png")
home_main = pygame.image.load("surfaces/HOME_main.png")
home_player = pygame.image.load("surfaces/HOME_room.png")

## Pause ##

pack_img = pygame.image.load("surfaces/paused/pack.png")
pause_img = pygame.image.load("surfaces/paused/pause.png")
quit_img = pygame.image.load("surfaces/paused/quit.png")
pause_top = pygame.image.load("surfaces/paused/pause_top.png")
pause_mid = pygame.image.load("surfaces/paused/pause_mid.png")
pause_bottom = pygame.image.load("surfaces/paused/pause_bottom.png")
pause_select = pygame.image.load("surfaces/paused/pause_select.png")

## Objects ##

door_barracks = pygame.image.load("sprites/objects/CADET_door.png")
door_stairwell = pygame.image.load("sprites/objects/CADET_door_stair1.png")
CCQ = pygame.image.load("sprites/objects/CADET_CCQ.png")
cadet_desk = pygame.image.load("sprites/objects/CADET_desk.png")
cadet_bed = pygame.image.load("sprites/objects/CADET_bed.png")
cadet_sink = pygame.image.load("sprites/objects/CADET_sink.png")
cadet_drawers = pygame.image.load("sprites/objects/CADET_drawers.png")
home_bed = pygame.image.load("sprites/objects/HOME_bed.png")
home_tree = pygame.image.load("sprites/objects/HOME_tree.png")
box = pygame.image.load("sprites/objects/box.png")

## Objects-front ##

cadet_bed_front = pygame.image.load("sprites/objects/CADET_bed_front.png")
cadet_drawers_front = pygame.image.load("sprites/objects/CADET_drawers_front.png")
cadet_wardrobe_h = pygame.image.load("sprites/objects/CADET_wardrobe.png")
cadet_wardrobe_v = pygame.image.load("sprites/objects/CADET_wardrobe_v.png")
home_bed_front = pygame.image.load("sprites/objects/HOME_bed_front.png")
home_tree_front = pygame.image.load("sprites/objects/HOME_tree_front.png")
home_table_front = pygame.image.load("sprites/objects/HOME_table.png")
home_counter_front = pygame.image.load("sprites/objects/HOME_counter.png")
home_stair_bit = pygame.image.load("sprites/objects/stair_bit.png")

## Character Packs ##

class SpritePack_NPC:
    def __init__(self, spritesList):
        self.sprites = [[],[]]
        for img in spritesList[1]:
            self.sprites[0].append(pygame.image.load(spritesList[0][0]+img))
        for img in spritesList[2]:
            self.sprites[1].append(pygame.image.load(spritesList[0][0]+"front/"+img))
    def get(self, j, i):
        return self.sprites[j][i]

class SpritePack:
    def __init__(self, spritesList):
        self.sprites = []
        for img in spritesList[1]:
            self.sprites.append(pygame.image.load(spritesList[0][0]+img))
    def __getitem__(self, i):
        return self.sprites[i]

player_pack = SpritePack([["sprites/character_packs/cadet_other/"],['b-s.png','b-l.png','b-r.png',   # back = 0
                                                      'f-s.png','f-l.png','f-r.png',    # front= 1
                                                      'l-s.png','l-l.png','l-r.png',    # left = 2
                                                      'r-s.png','r-l.png','r-r.png']])

cadet_npc = SpritePack_NPC([["sprites/character_packs/cadet_other/"],['b-s.png','b-l.png','b-r.png',   # back = 0
                                                      'f-s.png','f-l.png','f-r.png',    # front= 1
                                                      'l-s.png','l-l.png','l-r.png',    # left = 2
                                                      'r-s.png','r-l.png','r-r.png'],  # right= 3
                                                     ['b.png','f.png','l.png','r.png']])

black_npc = SpritePack_NPC([["sprites/character_packs/bald/black/"],['b-s.png','b-l.png','b-r.png',   # back = 0
                                                      'f-s.png','f-l.png','f-r.png',    # front= 1
                                                      'l-s.png','l-l.png','l-r.png',    # left = 2
                                                      'r-s.png','r-l.png','r-r.png'],  # right= 3
                                                     ['b.png','f.png','l.png','r.png']])

white_rh_npc = SpritePack_NPC([["sprites/character_packs/cadet-male-redhead/"],['b-s.png','b-l.png','b-r.png',   # back = 0
                                                      'f-s.png','f-l.png','f-r.png',    # front= 1
                                                      'l-s.png','l-l.png','l-r.png',    # left = 2
                                                      'r-s.png','r-l.png','r-r.png'],  # right= 3
                                                     ['b.png','f.png','l.png','r.png']])

female_white_ginger = SpritePack_NPC([["sprites/character_packs/ladies/red/hair-down/"],['b-s.png','b-l.png','b-r.png',   # back = 0
                                                                          'f-s.png','f-l.png','f-r.png',    # front= 1
                                                                          'l-s.png','l-l.png','l-r.png',    # left = 2
                                                                          'r-s.png','r-l.png','r-r.png'],  # right= 3
                                                                        ['b.png','f.png','l.png','r.png']])

female_white_brown = SpritePack_NPC([["sprites/character_packs/ladies/brown/bun/"],['b-s.png','b-l.png','b-r.png',   # back = 0
                                                                          'f-s.png','f-l.png','f-r.png',    # front= 1
                                                                          'l-s.png','l-l.png','l-r.png',    # left = 2
                                                                          'r-s.png','r-l.png','r-r.png'],  # right= 3
                                                                        ['b.png','f.png','l.png','r.png']])

## Interaction ##

img_text_box = pygame.image.load("sprites/decal/textBox.png")
img_yes = pygame.image.load("sprites/decal/yes.png")
img_no = pygame.image.load("sprites/decal/no.png")
img_decision = pygame.image.load("sprites/decal/decision.png")

## Combat ##

choice_act = pygame.image.load("surfaces/combat/choices/act.png")
choice_item = pygame.image.load("surfaces/combat/choices/item.png")
choice_analyze = pygame.image.load("surfaces/combat/choices/analyze.png")
choice_leave = pygame.image.load("surfaces/combat/choices/leave.png")
combat_surface = pygame.image.load("surfaces/combat/combat.png")
combat_decision = pygame.image.load("surfaces/combat/acts_decision.png")
act_attack = pygame.image.load("surfaces/combat/acts/attack.png")
act_NCOR = pygame.image.load("surfaces/combat/acts/NCOR.png")
act_help = pygame.image.load("surfaces/combat/acts/help.png")
act_lead = pygame.image.load("surfaces/combat/acts/lead.png")
combat_text = pygame.image.load("surfaces/combat/texter.png")
img_items = pygame.image.load("surfaces/combat/clicker.png")
item_decision = pygame.image.load("surfaces/combat/item_decision.png")
health_block = pygame.image.load("surfaces/combat/status/health_block.png")
morale_block = pygame.image.load("surfaces/combat/status/morale_block.png")
overlay = pygame.image.load("surfaces/combat/status/cover.png")

## Mini-Game ##

mini_sprite = SpritePack([["surfaces/combat/mini_game/mini_sprite/"],["r-0.png","r-1.png","r-2.png","r-3.png",
                                             "l-0.png","l-1.png","l-2.png","l-3.png"]])
mini_tile = pygame.image.load("surfaces/combat/mini_game/grey_brick.png")
mini_health = pygame.image.load("surfaces/combat/mini_game/health.png")
mini_enemy = pygame.image.load("surfaces/combat/mini_game/enemy.png")
mini_wall = pygame.image.load("surfaces/combat/mini_game/ranger_wall.png")
mini_shelf = pygame.image.load("surfaces/combat/mini_game/shelf.png")
mini_background = pygame.image.load("surfaces/combat/mini_game/background.png")
mini_goal = pygame.image.load("surfaces/combat/mini_game/goal.png")
mini_frame = pygame.image.load("surfaces/combat/mini_game/frame.png")
mini_plat = pygame.image.load("surfaces/combat/mini_game/platform.png")

## Menu ##

emblem = pygame.image.load("sprites/decal/emblem.png")
menu_play = pygame.image.load("sprites/decal/menu_play.png")
menu_load = pygame.image.load("sprites/decal/menu_load.png")
menu_select = pygame.image.load("sprites/decal/menu_select.png")
logo = pygame.image.load("sprites/decal/game_menu.png")
load_tile = pygame.image.load("sprites/decal/load_tile.png")
load_select = pygame.image.load("sprites/decal/load_select.png")
empty_tile = pygame.image.load("sprites/decal/load_empty.png")

## Special ##

exit_down = pygame.image.load("sprites/decal/exit_down.png")
decal_m1 = pygame.image.load("sprites/decal/M1.png")
decal_m2 = pygame.image.load("sprites/decal/M2.png")
#"surfaces/fade.png"
#"surfaces/fade_white.png"

