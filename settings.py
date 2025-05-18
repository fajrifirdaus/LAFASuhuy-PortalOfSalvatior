# game setup
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64
HITBOX_OFFSET = {
    'player': -26,
    'object': -50,
    'grass': -10,
    'crystal1': 0,
    'crystal2': 0,
    'crystal3': 0,
    'crystal4': 0,
    'crystal5': 0,
    'portal': 0,
    'invisible': 0}

# ui 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = (29,250,0)
UI_BG_COLOR = '#777777'
UI_BORDER_COLOR = '#ffffff'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'green'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# weapons 
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'graphics/weapons/sai/full.png'}}

# magic
magic_data = {    
	'nova': {'strength': 5,'cost': 20,'graphic':'graphics/particles/nova/nova.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'graphics/particles/heal/heal.png'}}

#enemy
monster_data = {
	'siMerah': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'audio/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'siHijau': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'audio/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}