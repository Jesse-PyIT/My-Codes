# Space Base Defense Game
import pygame
import random
import math
import time
import datetime    
import cProfile as profile
import os
import numpy as np
import json
from time import time, ctime, strftime, gmtime
from os import listdir
from pygame.locals import *

pygame.init()

window_info = pygame.display.Info()
screen_width = window_info.current_w
screen_height = window_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))


def show_variable(var, font, loc=(300,600)):
    
    surf = font.render(f'{var}', True, 'yellow')
    rect = surf.get_rect(center=loc)
    screen.blit(surf, rect)
    
def load_and_scale(image_path, scale_y=False):
    global screen_width
    global screen_height
    #default_screen_width = 1460
    #default_screen_height = 720
    default_aspect_ratio = 1460 / 720
    current_aspect_ratio = screen_width / screen_height
    aspect_ratio_difference = current_aspect_ratio / default_aspect_ratio
    img = pygame.image.load(image_path).convert_alpha()
    #width_ratio = img.get_width() / default_screen_width
    #height_ratio = img.get_height() / default_screen_height
    #height_to_width_ratio = img.get_height() / img.get_width()
    #fixed_width = screen_width * width_ratio
    #fixed_height = screen_height * height_ratio
    #if scale_y is True:
    #img = pygame.transform.scale(img, (fixed_width, (height_to_width_ratio * fixed_width)))
    img = pygame.transform.scale_by(img, aspect_ratio_difference)
    #elif scale_y is False:
        #img = pygame.transform.scale(img, (fixed_width, fixed_height))
    return img


def load_animation(image_folder, scale=None):
    
    images = np.array(listdir(image_folder))
    animations = []
    if scale != None:
        scale_factor = screen_width * scale
    for image in images:
        if scale != None:
            img = load_and_scale(str(image_folder + image), scale_y=True)
        else:
            img = load_and_scale(str(image_folder + image))
        animations.append(img)
            
    return np.array(animations)
    
    
def load_enemy_ships(folder, boss=False):
    
    _ships = listdir(folder)
    ships = sorted(_ships)
    fixed_ships = []
    for img in ships:
        print(folder + img)
        original_img = pygame.image.load(folder + img).convert_alpha()
        width = original_img.get_width()
        height = original_img.get_height()
        if boss is True:
            if width > height:
                resize_factor = screen_width * 0.225 / width
            elif height > width:
                resize_factor = screen_height * 0.3 / height 
        else:
            if width > height:
                resize_factor = screen_width * 0.075 / width
            elif height > width:
                resize_factor = screen_height * 0.1 / height
        new_img = pygame.transform.scale(original_img, (width * resize_factor, height * resize_factor))
        fixed_ships.append(new_img)
    return np.array(fixed_ships)
 
       
def load_saved_games(games):
    
    saved_games_list = [k for k in games.keys()]
    games_selection = dict()
    x = screen_width * 0.25
    y = screen_height * 0.33
    for b in saved_games_list:
        if len(games_selection) % 9 == 0:
            x = (screen_width * len(games_selection) // 9) + screen_width * 0.25
            y = screen_height * 0.33
        game_link = Button(upgrades_stat_bar, (x, y), b, upgrades_font)
        games_selection[str(len(games_selection) + 1)] = game_link 
            
        if len(games_selection) % 3 == 0 and game_link.rect.centery > screen_height / 2:
            x += game_link.rect.width + 10
            y = screen_height * 0.33
        else:
            y += game_link.rect.height + 50
    return games_selection
    
    
def play_music_track(track, fade_in_time=0):
    
    if pygame.mixer.get_num_channels() > 0:
        pygame.mixer.music.fadeout(2500)
    if not pygame.mixer.get_busy():
        pygame.mixer.music.unload()
        pygame.mixer.music.load(track)
        if game['Music'] is True:
            pygame.mixer.music.play(-1, fade_ms=fade_in_time)
        
def music_manager(current_track):
        pygame.mixer.music.fadeout(2500)
        if pygame.mixer.music.get_busy() is False:
            pygame.mixer.music.unload()
            pygame.mixer.music.load(current_track)
            if level['Battle'] is True:
                pygame.mixer.music.set_volume(0.75)
            else:
                pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1, fade_ms=5000)
            game['Screen Transition'] = False
    
    
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        return super(NumpyEncoder, self).default(obj)
    

FPS = 60
CLOCK = pygame.time.Clock()

pygame.display.set_caption('Galactic Defender')

# Modified font sizes for dynamic screen sizing
size_25_font = screen_width * (25 / 1460)
size_35_font = screen_width * (35 / 1460)
size_50_font = screen_width * (50 / 1460)
size_60_font = screen_width * (60 / 1460)

# Fonts
reg_font = pygame.font.SysFont('arial', int(size_25_font))
ui_font = pygame.font.Font('Fonts/Pavelt.ttf', int(size_25_font))
big_font = pygame.font.Font('Fonts/Pavelt.ttf', int(size_60_font))
upgrades_font = pygame.font.Font('Fonts/Pavelt.ttf', int(size_35_font))
title_font = pygame.font.Font('Fonts/Pavelt.ttf', int(size_50_font))

# Background Images
bg = pygame.image.load('stars_bg.png').convert_alpha()
bg = pygame.transform.scale(bg, (screen_width, screen_height))

# Music
starting_music = 'Sci-Fi1.wav'
gameplay_music = 'Music/gameplay_track.wav'
gameplay_music2 = 'Music/gameplay_track2.mp3'
boss_battle_music = 'Music/boss_battle_track.mp3'

# Sounds
ship_explosion_sound = pygame.mixer.Sound('ship_explosion.wav')
ship_explosion_sound.set_volume(0.1)
turret_shot_fired = pygame.mixer.Sound('turret_shot.wav')
turret_shot_fired.set_volume(0.05)
helper_turret_shot_sound = pygame.mixer.Sound('helper_turret_shot.wav')
helper_turret_shot_sound.set_volume(0.5)
button_clicked_sound = pygame.mixer.Sound('button_clicked.wav')
button_clicked_sound.set_volume(0.75)
base_hit_sound = pygame.mixer.Sound('base_hit_sound.wav')
base_hit_sound.set_volume(0.3)
shield_deactivated_sound = pygame.mixer.Sound('shield_status_changed.wav')
insufficient_funds_sound = pygame.mixer.Sound('not_enough_money.wav')
missile_flying_sound = pygame.mixer.Sound('missile_flying.mp3')
electrocuted_sound = pygame.mixer.Sound('electrocuted_sound.mp3')
electrocuted_sound.set_volume(0.1)
enemies_vaporized_sound = pygame.mixer.Sound('enemy_vaporized_sound.wav')
level_completed_sound = pygame.mixer.Sound('level_completed.mp3')
level_defeated_sound = pygame.mixer.Sound('level_defeated.mp3')
incoming_boss_sound = pygame.mixer.Sound('incoming_boss_alert.mp3')
scroll_button_clicked_sound = pygame.mixer.Sound('scroll_button_clicked.mp3')

# Animations
impact_animation = load_animation('Animations/Impact/')
for i in impact_animation:
    i = pygame.transform.scale(i,  (screen_width * 0.375, screen_height * 0.105))

ship_explosion = load_animation('Animations/Ship Explosion/')
for i in ship_explosion:
    i = pygame.transform.scale(i, (screen_width * 0.0325, screen_height * 0.072))

spawn_animation = load_animation('Animations/Spawn Cover/')
for i in spawn_animation:
    i = pygame.transform.scale(i, (100, 100))
    
charge_up_animation = load_animation('Animations/Charge Up/')

# Game Title
#game_title_label_image = pygame.image.load('Menu/game_title.png').convert_alpha()
game_title_label_image = load_and_scale('Menu/game_title.png')

# Level Button Images
level_buttons = load_animation('Level Buttons/', scale=0.1)

#locked_level_button_image = pygame.image.load('locked_level.png').convert_alpha()
locked_level_button_image = load_and_scale('locked_level.png')

# Levels Menu Title
#levels_menu_title = pygame.image.load('UI Text/level_overworld_title.png').convert_alpha()
levels_menu_title = load_and_scale('UI Text/level_overworld_title.png')

# UI Text
#music_text = pygame.image.load('UI Text/music.png').convert_alpha()
music_text = load_and_scale('UI Text/music.png')
#sounds_text = pygame.image.load('UI Text/sounds.png').convert_alpha()
sounds_text = load_and_scale('UI Text/sounds.png')
#toggle_on_text = pygame.image.load('UI Text/on.png').convert_alpha()
toggle_on_text = load_and_scale('UI Text/on.png')
#toggle_off_text = pygame.image.load('UI Text/off.png').convert_alpha()
toggle_off_text = load_and_scale('UI Text/off.png')

# Currency UI Labels
#space_crystals_label_image = pygame.image.load('UI Text/space_crystals.png').convert_alpha()
space_crystals_label_image = load_and_scale('UI Text/space_crystals.png')
#power_gems_label_image = pygame.image.load('UI Text/power_gems.png').convert_alpha()
power_gems_label_image = load_and_scale('UI Text/power_gems.png')

# UI Buttons
#goto_levels_button_image = pygame.image.load('UI Buttons/goto_levels.png').convert_alpha()
goto_levels_button_image = load_and_scale('UI Buttons/goto_levels.png')
#goto_menu_button_image = pygame.image.load('UI Buttons/goto_menu.png').convert_alpha()
goto_menu_button_image = load_and_scale('UI Buttons/goto_menu.png')
#goto_upgrades_button_image = pygame.image.load('UI Buttons/goto_upgrades.png').convert_alpha()
goto_upgrades_button_image = load_and_scale('UI Buttons/goto_upgrades.png')
go_back_button_image = pygame.image.load('UI Buttons/go_back.png').convert_alpha()
go_back_button_image = pygame.transform.scale(go_back_button_image, (screen_width * 0.16, screen_height * 0.1))
#resume_game_button_image = pygame.image.load('UI Buttons/resume_game.png').convert_alpha()
resume_game_button_image = load_and_scale('UI Buttons/resume_game.png')

# Main Menu Buttons 
#new_game_button_image = pygame.image.load('UI Buttons/new_game.png').convert_alpha()
new_game_button_image = load_and_scale('UI Buttons/new_game.png')
#load_game_button_image = pygame.image.load('UI Buttons/load_game.png').convert_alpha()
load_game_button_image = load_and_scale('UI Buttons/load_game.png')
#exit_game_button_image = pygame.image.load('UI Buttons/exit_game.png').convert_alpha()
exit_game_button_image = load_and_scale('UI Buttons/exit_game.png')

# Settings Menu Title
settings_menu_title_image = load_and_scale('UI Text/settings_menu_title.png')

# Settings Buttons
#music_toggle_button_image = pygame.image.load('music_toggle_button.png').convert_alpha()
music_toggle_button_image = load_and_scale('music_toggle_button.png')
#sounds_toggle_button_image = pygame.image.load('sounds_toggle_button.png').convert_alpha() 
sounds_toggle_button_image = load_and_scale('sounds_toggle_button.png')

# Upgrades Buttons
#base_upgrades_button_image = pygame.image.load('UI Buttons/base_upgrades.png').convert_alpha()
base_upgrades_button_image = load_and_scale('UI Buttons/base_upgrades.png')
#base_health_upgrades_button_image = pygame.image.load('UI Buttons/health_upgrades.png').convert_alpha()
base_health_upgrades_button_image = load_and_scale('UI Buttons/health_upgrades.png')
#shield_upgrades_button_image = pygame.image.load('UI Buttons/shield_upgrades.png').convert_alpha()
shield_upgrades_button_image = load_and_scale('UI Buttons/shield_upgrades.png')
#turrets_upgrades_button_image = pygame.image.load('UI Buttons/turret_upgrades.png').convert_alpha()
turrets_upgrades_button_image = load_and_scale('UI Buttons/turret_upgrades.png')
#main_turret_upgrades_button_image = pygame.image.load('UI Buttons/main_turret_upgrades.png').convert_alpha()
main_turret_upgrades_button_image = load_and_scale('UI Buttons/main_turret_upgrades.png')
#extra_turrets_upgrades_button_image = pygame.image.load('UI Buttons/helpers_upgrades.png').convert_alpha()
extra_turrets_upgrades_button_image = load_and_scale('UI Buttons/helpers_upgrades.png')
#extra_upgrades_button_image = pygame.image.load('UI Buttons/special_upgrades.png').convert_alpha()
extra_upgrades_button_image = load_and_scale('UI Buttons/special_upgrades.png')
#special_attacks_upgrades_button_image = pygame.image.load('UI Buttons/special_attacks_upgrades.png').convert_alpha()
special_attacks_upgrades_button_image = load_and_scale('UI Buttons/special_attacks_upgrades.png')
#special_defenses_upgrades_button_image = pygame.image.load('UI Buttons/special_defenses_upgrades.png').convert_alpha()
special_defenses_upgrades_button_image = load_and_scale('UI Buttons/special_defenses_upgrades.png')

# Special Attacks Buttons
#rapid_fire_button_image = pygame.image.load('UI Buttons/rapid_fire.png').convert_alpha()
rapid_fire_button_image = load_and_scale('UI Buttons/rapid_fire.png')
#cluster_shot_button_image = pygame.image.load('UI Buttons/cluster_shot.png').convert_alpha()
cluster_shot_button_image = load_and_scale('UI Buttons/cluster_shot.png')
#raining_comets_button_image = pygame.image.load('UI Buttons/raining_comets.png').convert_alpha()
raining_comets_button_image = load_and_scale('UI Buttons/raining_comets.png')
#vaporize_button_image = pygame.image.load('UI Buttons/vaporize.png').convert_alpha()
vaporize_button_image = load_and_scale('UI Buttons/vaporize.png')
#meteor_shower_button_image = pygame.image.load('UI Buttons/meteor_shower.png').convert_alpha()
meteor_shower_button_image = load_and_scale('UI Buttons/meteor_shower.png')

# Special Defenses Buttons
#shock_absorber_button_image = pygame.image.load('UI Buttons/shock_absorber.png').convert_alpha()
shock_absorber_button_image = load_and_scale('UI Buttons/shock_absorber.png')
#poison_antidote_button_image = pygame.image.load('UI Buttons/poison_antidote.png').convert_alpha()
poison_antidote_button_image = load_and_scale('UI Buttons/poison_antidote.png')

# Special Attack and Defenses container
#specials_container = pygame.image.load('specials_container.png').convert_alpha()
specials_container = load_and_scale('specials_container.png')

# Special Attacks and Defenses Label abbreviations
#special_attacks_label_abbreviated = pygame.image.load('UI Text/special_attacks_abbreviated_label.png').convert_alpha()
special_attacks_label_abbreviated = load_and_scale('UI Text/special_attacks_abbreviated_label.png')
#special_defenses_label_abbreviated = pygame.image.load('UI Text/special_defenses_abbreviated_label.png').convert_alpha()
special_defenses_label_abbreviated = load_and_scale('UI Text/special_defenses_abbreviated_label.png')

settings_button_image = pygame.image.load('settings_button.png').convert_alpha()
#continue_button_image = pygame.image.load('continue_button.png').convert_alpha()
continue_button_image = load_and_scale('continue_button.png')
#previous_button_image = pygame.image.load('previous.png').convert_alpha()
previous_button_image = load_and_scale('previous.png')

level_nav_button = pygame.image.load('continue_level_button.png').convert_alpha()
#level_nav_button = load_and_scale('continue_level_button.png')

#level_options_button_image = pygame.image.load('menu_button.png').convert_alpha()
level_options_button_image = load_and_scale('menu_button.png')
#pause_level_button_image = pygame.image.load('pause_level_button.png').convert_alpha()
pause_level_button_image = load_and_scale('pause_level_button.png')
game_speed_button_image = pygame.image.load('adjust_game_speed.png').convert_alpha()
game_speed_button_image = pygame.transform.scale_by(game_speed_button_image, 1)
repair_health = pygame.image.load('health_icon.png').convert_alpha()

# Close button
#close_button_image = pygame.image.load('close_button.png').convert_alpha()
close_button_image = load_and_scale('close_button.png')

# Player Space Base
base_main = pygame.image.load('Player/player_base.png').convert_alpha()
base_main = pygame.transform.scale(base_main, (screen_width * 0.4, screen_width * 0.4))
electrocuted_base = pygame.image.load('Player/electrocuted_base.png').convert_alpha()
electrocuted_base = pygame.transform.scale(electrocuted_base, (screen_width * 0.4, screen_width * 0.4))
poisoned_base = pygame.image.load('Player/poisoned_base.png').convert_alpha()
poisoned_base = pygame.transform.scale(poisoned_base, (screen_width * 0.4, screen_width * 0.4))
#shield_main = pygame.image.load('Player/base_shield.png').convert_alpha()
shield_main = load_and_scale('Player/base_shield.png')
#turret_main = pygame.image.load('Player/base_turret_main.png').convert_alpha()
turret_main = load_and_scale('Player/base_turret_main.png')
#turret_extra = pygame.image.load('Player/helper_turret.png').convert_alpha()
turret_extra = load_and_scale('Player/helper_turret.png')
#electrocuted_turret = pygame.image.load('Player/electrocuted_turret.png').convert_alpha()
electrocuted_turret = load_and_scale('Player/electrocuted_turret.png')
#vaporizing_arc_image = pygame.image.load('vaporizing_arc.png').convert_alpha()
vaporizing_arc_image = load_and_scale('vaporizing_arc.png')
#base_health_container = pygame.image.load('base_health_container.png').convert_alpha()
base_health_container = load_and_scale('base_health_container.png')

# Bullets
#player_laser = pygame.image.load('player_bullet.png').convert_alpha()
player_laser = load_and_scale('player_bullet.png')
#enemy_laser = pygame.image.load('enemy_bullet.png').convert_alpha()
enemy_laser = load_and_scale('enemy_bullet.png')
#enemy_turret_laser = pygame.image.load('enemy_turret_laser.png').convert_alpha()
enemy_turret_laser = load_and_scale('enemy_turret_laser.png')
#poison_laser = pygame.image.load('poison_laser.png').convert_alpha()
poison_laser = load_and_scale('poison_laser.png')
#destroy_shield_laser = pygame.image.load('destroyer.png').convert_alpha()
destroy_shield_laser = load_and_scale('destroyer.png')
#wave_blast_image = pygame.image.load('wave_blast.png').convert_alpha()
wave_blast_image = load_and_scale('wave_blast.png')
#solid_laser_image = pygame.image.load('solid_laser.png').convert_alpha()
solid_laser_image = load_and_scale('solid_laser.png')
#laser_flare = pygame.image.load('enemy_flare.png').convert_alpha()
laser_flare =load_and_scale('enemy_flare.png')
#cluster_laser_image = pygame.image.load('cluster_laser.png').convert_alpha()
cluster_laser_image = load_and_scale('cluster_laser.png')
#laser_cluster_image = pygame.image.load('laser_cluster.png').convert_alpha()
laser_cluster_image = load_and_scale('laser_cluster.png')
#critical_laser_image = pygame.image.load('critical_laser.png').convert_alpha()
critical_laser_image = load_and_scale('critical_laser.png')

# Electric bolts
#charge_bolt_image = pygame.image.load('charge_bolts.png').convert_alpha()
charge_bolt_image = load_and_scale('charge_bolts.png')

#black_hole_image = pygame.image.load('black_hole.png').convert_alpha()
black_hole_image = load_and_scale('black_hole.png')
#raining_comet_image = pygame.image.load('raining_comet.png').convert_alpha()
raining_comet_image = load_and_scale('raining_comet.png')

# Missiles
#side_missile_image = pygame.image.load('side_missile.png').convert_alpha()
side_missile_image = load_and_scale('side_missile.png')

# Bombs
#enemy_rubble_bomb = pygame.image.load('rubble_bomb.png').convert_alpha()
enemy_rubble_bomb = load_and_scale('rubble_bomb.png')

# Enemy Ships
enemy_ships = load_enemy_ships('Enemy Ships/')
enemy_boss_images = load_enemy_ships('Boss Ships/', boss=True)

healer_ring_no_effect_image = pygame.image.load('healer_ring_no_effect.png').convert_alpha()
healer_ring_no_effect_image = pygame.transform.scale(healer_ring_no_effect_image, (200, 200))

healer_ring_with_effect_image = pygame.image.load('healer_ring_with_effect.png').convert_alpha()
healer_ring_with_effect_image = pygame.transform.scale(healer_ring_with_effect_image, (200, 200))

#health_recovery_icon_image = pygame.image.load('health_recovery_icon.png').convert_alpha()
health_recovery_icon_image = load_and_scale('health_recovery_icon.png')

# Spawning Orbs
#turret_spawn_orb = pygame.image.load('boss2_turret_spawn_shot.png').convert_alpha()
turret_spawn_orb = load_and_scale('boss2_turret_spawn_shot.png')

# Meteors
#tan_meteor = pygame.image.load('meteor.png').convert_alpha()
tan_meteor = load_and_scale('meteor.png')

#test_boss = pygame.image.load('blueship2.png').convert_alpha()

#level_overworld_button = pygame.image.load('level_button.png').convert_alpha()
level_overworld_button = load_and_scale('level_button.png')

level_button = pygame.transform.scale_by(level_overworld_button, 2)
#power_crystal = pygame.image.load('power_crystal.png')
power_crystal = load_and_scale('power_crystal.png')
#power_gem_image = pygame.image.load('power_gem.png').convert_alpha()
power_gem_image = load_and_scale('power_gem.png')

#level_over_menu = pygame.image.load('level_over_window.png').convert_alpha()
level_over_menu = load_and_scale('level_over_window.png')

#upgrade_table = pygame.image.load('upgrade_window.png').convert_alpha()
upgrade_table = load_and_scale('upgrade_window.png')
#upgrades_stat_bar = pygame.image.load('Table.png').convert_alpha()
upgrades_stat_bar = load_and_scale('Table.png')
turret_empty_location = pygame.image.load('turret_location_indicator.png').convert_alpha()
turret_empty_location = pygame.transform.scale(turret_empty_location, (screen_width * 0.044, screen_height * 0.0986))

# Test surfaces for improved performance
#new_game_button = pygame.image.load('new_game_button.jpg').convert_alpha()


class Title:
    
    def __init__(self, image, pos):
        self.image = image
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        
    def show(self):
        screen.blit(self.image, self.rect)


class Feedback:
    
    def __init__(self, text, font, loc):
        self.text = text
        self.font = font
        self.loc = pygame.math.Vector2(loc)
        self.origin_pos = pygame.math.Vector2(loc)
        self.surf = self.font.render(self.text, True, 'cyan').convert_alpha()
        self.rect = self.surf.get_rect(center=self.loc)
        self.mask = pygame.mask.from_surface(self.surf)
        self.mask_surf = self.mask.to_surface(setcolor='blue', unsetcolor=(0, 0, 0, 0)).convert_alpha()
        self.red_surf = self.font.render(self.text, True, 'red').convert_alpha()
        self.red_mask_surf = self.mask.to_surface(setcolor='pink', unsetcolor=(0, 0, 0, 0)).convert_alpha()
        self.notify_time = 4
      
    def apply_updates(self):
        self.__init__(self.text, self.font, self.loc) 
            
    def snap_to_topright(self):
        self.rect.topright = pygame.math.Vector2(screen_width - 10, 5)
        
    def snap_to_topleft(self):
        self.rect.topleft = (10, 10)
        
    def snap_to_bottomleft(self):
        self.rect.bottomleft = (10, screen_height - 10)
        
    def notify_player(self):
        self.red_surf.set_alpha(255)
        self.red_mask_surf.set_alpha(255)
        self.notify_time = time()
        
    def show_notification(self):
        if time() - self.notify_time < 3:
            offset = 2
            screen.blit(self.red_mask_surf, (self.rect.x+offset, self.rect.y))
            screen.blit(self.red_mask_surf, (self.rect.x-offset, self.rect.y))
            screen.blit(self.red_mask_surf, (self.rect.x, self.rect.y+offset))
            screen.blit(self.red_mask_surf, (self.rect.x, self.rect.y+offset))
            screen.blit(self.red_mask_surf, (self.rect.x+offset, self.rect.y-offset))
            screen.blit(self.red_mask_surf, (self.rect.x+offset, self.rect.y+offset))
            screen.blit(self.red_mask_surf, (self.rect.x-offset, self.rect.y-offset))
            screen.blit(self.red_mask_surf, (self.rect.x-offset, self.rect.y+offset))
            screen.blit(self.red_surf, self.rect)
            self.red_surf.set_alpha(self.red_surf.get_alpha() - 5)
            self.red_mask_surf.set_alpha(self.red_mask_surf.get_alpha() - 5)
            
    def show_to_player(self):
        offset = 2
        screen.blit(self.mask_surf, (self.rect.x+offset, self.rect.y))
        screen.blit(self.mask_surf, (self.rect.x-offset, self.rect.y))
        screen.blit(self.mask_surf, (self.rect.x, self.rect.y+offset))
        screen.blit(self.mask_surf, (self.rect.x, self.rect.y+offset))
        screen.blit(self.mask_surf, (self.rect.x+offset, self.rect.y-offset))
        screen.blit(self.mask_surf, (self.rect.x+offset, self.rect.y+offset))
        screen.blit(self.mask_surf, (self.rect.x-offset, self.rect.y-offset))
        screen.blit(self.mask_surf, (self.rect.x-offset, self.rect.y+offset))
        screen.blit(self.surf, self.rect)
        
    def reset_position(self):
        self.loc.x = self.origin_pos.x
        self.loc.y = self.origin_pos.y
            
    def update_var(self, new_var, new_loc=None):
        self.surf = self.font.render(f'{new_var}', True, 'cyan').convert_alpha()
        if new_loc != None:
            self.rect = self.surf.get_rect(center=new_loc)
        else:
            self.rect = self.surf.get_rect(center=self.loc)
        self.mask = pygame.mask.from_surface(self.surf)
        self.mask_surf = self.mask.to_surface(setcolor='blue', unsetcolor=(0, 0, 0, 0)).convert_alpha()
            
    def slide_to(self, pos, speed):
        self.loc.move_towards_ip(pos, speed)
        self.rect.center = self.loc
        
    def slide_to_origin(self, speed):
        self.loc.move_towards_ip(self.origin_pos, speed)
        self.rect.center = self.loc
        
    def is_offsetx(self):
        if self.loc.x != self.origin_pos.x:
            return True
            
    def is_offsety(self):
        if self.loc.y != self.origin_pos.y:
            return True

        
class Animation(pygame.sprite.Sprite):
    
    def __init__(self, animations, delay, loc, sound=None):
        super().__init__()
        self.animations = animations
        self.image = self.animations[0]
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.delay = delay
        self.sound = sound
        self.play_sound = True
        self.current_sprite = 0
        self.animating = True
        self.continue_animating = False
        
    def update(self, base):
        
        if self.animating is True:
            self.current_sprite += self.delay
        if self.current_sprite >= len(self.animations):
            self.current_sprite = 0
            if self.continue_animating is False:
                self.animating = False
                self.kill()
        if self.sound != None:
            if self.play_sound is True:
                if game['Sounds'] is True:
                    self.sound.play()
                self.play_sound = False
            
        if self.animating is True:
            if self.continue_animating is True:
                self.rect.x -= 100 * game['Delta Time'] * level['Speed']
            self.image = self.animations[int(self.current_sprite)]
            screen.blit(self.image, self.rect)            


class UpgradeMenu:
    
    def __init__(self, header, dict, upgrade_increase_amounts, loc):
        self.image = upgrade_table
        self.loc = pygame.math.Vector2(loc)
        self.rect = self.image.get_rect(topleft=self.loc)
        self.title = header
        self.header = Feedback(self.title, upgrades_font, (self.rect.centerx, self.rect.top + 40))
        self.dict = dict
        self.dict_keys = [k for k in self.dict.keys()]
        self.increase_amounts = upgrade_increase_amounts
        self.buttons = self.create_buttons()
        self.button_labels = self.create_button_labels()
        
    def reset_upgrades(self):
        self.__init__(self.title, self.dict, self.increase_amounts, self.loc)
        
    def show_table(self):
        screen.blit(self.image, self.rect)
        
    def create_buttons(self):
        buttons = []
        y = 0.24
        for i in range(len(self.dict_keys)):
            if type(self.dict[self.dict_keys[i]]) == float:
                b = Button(level_nav_button, (self.rect.centerx, self.rect.height * y), f'{int(self.dict[self.dict_keys[i]])}', ui_font)
            elif self.dict_keys[i] == 'Add Turret':
                b = Button(level_nav_button, (self.rect.centerx, self.rect.height * y), f'{int(self.dict[self.dict_keys[i]])}', ui_font)
            else:
                b = Button(level_nav_button, (self.rect.centerx, self.rect.height * y), f'{self.dict[self.dict_keys[i]]}', ui_font)
            buttons.append(b)
            y += 0.17
        return np.array(buttons)
        
    def create_button_labels(self):
        button_labels = []
        for i in self.dict.keys():
            index = self.dict_keys.index(i)
            label = Feedback(i, ui_font, (self.buttons[index].rect.centerx, self.buttons[index].rect.top - 20))
            button_labels.append(label)
        return np.array(button_labels)
                
    def show_buttons(self):
        for button in self.buttons:
            button.show()
         
    def show_button_labels(self):
        for label in self.button_labels:
            label.show_to_player()
            
    def get_label(self, upgrade):
        i = np.where(self.buttons == upgrade)[0][0]
        return self.dict[self.dict_keys[i]]
        
    def update_cost(self, upgrade):
        i = np.where(self.buttons == upgrade)[0][0]
        self.dict[self.dict_keys[i]] *= self.increase_amounts[i]
        if self.dict[self.dict_keys[i]] >= 999999999:
            self.dict[self.dict_keys[i]] = 999999999
        self.buttons[i].label.update_var(f'{int(self.dict[self.dict_keys[i]])}')
        
    def get_cost(self, upgrade):
        i = np.where(self.buttons == upgrade)[0][0]
        return self.dict[self.dict_keys[i]]


class StatsTable(UpgradeMenu):
    
    def __init__(self, header, dict, stats_increase_amounts, stat_limits, loc):
        super().__init__(header, dict, stats_increase_amounts, loc)
        self.stats = self.get_stats()
        self.stat_limits = stat_limits
        
    def reset_stats(self):
        self.__init__(self.title, self.dict, self.increase_amounts, self.stat_limits, self.loc)
        
    def show_stats(self):
        for stat in self.stats:
            stat.show_to_player()
            
    def create_buttons(self):
        buttons = []
        y = 0.24
        for i in range(len(self.dict_keys)):
            if type(self.dict[self.dict_keys[i]]) == float:
                b = Button(level_nav_button, (self.rect.centerx, self.rect.height * y), '{:.1f}'.format(self.dict[self.dict_keys[i]]), ui_font)
            else:
                b = Button(level_nav_button, (self.rect.centerx, self.rect.height * y), f'{self.dict[self.dict_keys[i]]}', ui_font)
            buttons.append(b)
            y += 0.17
        return buttons
            
    def get_stats(self):
        stats = []
        for button in self.buttons:
            if type(button.label) == float:
                stat = '{:.1f}'.format(button.label)
            else:
                stat = button.label
            stats.append(stat)
        return stats
        
    def update_stat(self, stat_index):
        stat = self.stats[stat_index]
        if type(self.increase_amounts[stat_index]) == str:
            # used for Shield and Regeneration statuses
            self.dict[self.dict_keys[stat_index]] = self.increase_amounts[stat_index]
            self.buttons[stat_index].label.update_var(f'{self.dict[self.dict_keys[stat_index]]}')
        elif self.increase_amounts[stat_index] < 1:
            # used for decreasing cooldown times
            if self.dict_keys[stat_index] == 'Critical Hit':
                if self.dict[self.dict_keys[stat_index]] + self.increase_amounts[stat_index] >= self.stat_limits[stat_index]:
                    self.dict[self.dict_keys[stat_index]] = self.stat_limits[stat_index]
                else:
                    self.dict[self.dict_keys[stat_index]] += self.increase_amounts[stat_index]
            else:
                if self.dict[self.dict_keys[stat_index]] - self.increase_amounts[stat_index] <= self.stat_limits[stat_index]:
                    self.dict[self.dict_keys[stat_index]] = self.stat_limits[stat_index]
                else:
                    self.dict[self.dict_keys[stat_index]] -= self.increase_amounts[stat_index]
            self.buttons[stat_index].label.update_var('{:.1f}'.format(self.dict[self.dict_keys[stat_index]]))
        elif self.increase_amounts[stat_index] == 1:
            # used for adding Turrets and specials
            if self.dict[self.dict_keys[stat_index]] < self.stat_limits[stat_index]:
                self.dict[self.dict_keys[stat_index]] += self.increase_amounts[stat_index]
                self.buttons[stat_index].label.update_var(self.dict[self.dict_keys[stat_index]])
        elif self.increase_amounts[stat_index] > 100:
            # Used for base health repair limited to max health
            if self.dict[self.dict_keys[stat_index]] + self.increase_amounts[stat_index] > self.dict['Max Health']:
                self.dict[self.dict_keys[stat_index]] = int(self.dict['Max Health'])
            else:
                self.dict[self.dict_keys[stat_index]] += self.increase_amounts[stat_index]
            self.buttons[stat_index].label.update_var(f'{int(self.dict[self.dict_keys[stat_index]])}')
        else:
            # used for all other stat upgrades
            if self.dict[self.dict_keys[stat_index]] * self.increase_amounts[stat_index] > self.stat_limits[stat_index]:
                self.dict[self.dict_keys[stat_index]] = self.stat_limits[stat_index]
            else:
                self.dict[self.dict_keys[stat_index]] = int(self.dict[self.dict_keys[stat_index]] * self.increase_amounts[stat_index])
            self.buttons[stat_index].label.update_var(f'{int(self.dict[self.dict_keys[stat_index]])}')
      
    def get_stat(self, root, button):
        i = np.where(root == button)[0][0]
        return self.stats[i]


class Button:

    def __init__(self, image, loc, label, label_font):
        self.color = 'yellow'
        self.image = image
        self.loc = pygame.math.Vector2(loc)
        self.origin_pos = pygame.math.Vector2(loc)
        self.rect = self.image.get_rect(center=self.loc)
        if label != None:
            self.label = Feedback(f'{label}', label_font, self.rect.center)
        else:
            self.label = label
        self.button_mask = pygame.mask.from_surface(self.image)
        self.button_mask_surf = self.button_mask.to_surface(setcolor='cyan', unsetcolor=(0, 0, 0, 0)).convert_alpha()
        self.show_submenu = False
        self.locked = False
        self.notify = False
        self.flash_counter = 0
        self.flashes = 1
        self.scroll_amount = 0
        
    def show(self):
        screen.blit(self.image, self.rect)
        if self.scroll_amount != 0:
            self.scroll()
        if self.notify is True:
            if 0 < self.flash_counter < 10: 
                self.flash_selection()
            if self.flash_counter == 20:
                self.flash_counter = 0
                self.flashes -= 1
            self.flash_counter += 1
        if self.flashes <= 0:
            self.notify = False
            self.flashes = 1
            self.flash_counter = 0
        if self.label != None:
            self.label.show_to_player()
            
    def scroll(self):
        self.rect.centerx += self.scroll_amount
        if self.label != None:
            self.label.rect.centerx = self.rect.centerx
        self.scroll_amount = 0
                
    def is_offsetx(self):
        if self.loc.x != self.origin_pos.x:
            return True
            
    def is_offsety(self):
        if self.loc.y != self.origin_pos.y:
            return True
        
    def clicked(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.notify = True
                level['Button Clicked'] = True
                return True
                
    def snap_to_bottomleft(self):
        self.rect.bottomleft = (10, screen_height - 10)
      
    def reset_position(self):
        self.loc.x = self.origin_pos.x
        self.loc.y = self.origin_pos.y
                
    def flash_selection(self):
        offset = 5
        screen.blit(self.button_mask_surf, (self.rect.x+offset, self.rect.y))
        screen.blit(self.button_mask_surf, (self.rect.x-offset, self.rect.y))
        screen.blit(self.button_mask_surf, (self.rect.x, self.rect.y+offset))
        screen.blit(self.button_mask_surf, (self.rect.x, self.rect.y+offset))
        screen.blit(self.button_mask_surf, (self.rect.x+offset, self.rect.y-offset))
        screen.blit(self.button_mask_surf, (self.rect.x+offset, self.rect.y+offset))
        screen.blit(self.button_mask_surf, (self.rect.x-offset, self.rect.y-offset))
        screen.blit(self.button_mask_surf, (self.rect.x-offset, self.rect.y+offset))
        screen.blit(self.image, self.rect)
        
    def slide_to_origin(self, speed):
        self.loc.move_towards_ip(self.origin_pos, speed)
        self.rect.center = self.loc
        if self.label != None:
            self.label.rect.center = self.loc
        
    def slide_to(self, pos, speed):
        self.loc.move_towards_ip(pos, speed)
        self.rect.center = self.loc
        if self.label != None:
            self.label.rect.center = self.loc


class NavButton(Button):
    
    def __init__(self, image, loc, label=None, font=None):
        super().__init__(image, loc, label, font)
        


class Shader:
    
    def __init__(self):
        self.surface = pygame.Surface((screen_width, screen_height))
        self.rect = pygame.Rect(0, 0, screen_width, screen_height)
        self.color = pygame.Color(0, 0, 0, 0)
        self.surface.fill(self.color)
        self.alpha = 0
        self.surface.set_alpha(255)
        
    def fade_to_black(self):
        if self.alpha < 255:
            self.alpha += 100 * game['Delta Time']
        self.surface.set_alpha(self.alpha)
        
    def fade_from_black(self):
        if self.alpha > 0:
            self.alpha -= 100 * game['Delta Time']
        self.surface.set_alpha(self.alpha)      
            
    def show(self):
        if self.alpha > 0:
            screen.blit(self.surface, (0, 0))


class MiniMenu:
    
    def __init__(self, image, loc, header):
        self.image = image
        self.loc = pygame.math.Vector2(loc)
        self.origin_pos = pygame.math.Vector2(self.loc)
        self.rect = self.image.get_rect(center=self.loc)
        self.header = Feedback(header, upgrades_font, (self.rect.centerx, self.rect.top + 50))
        self.winning_loot = None
        self.winning_loot_label = None
        self.bonus_loot = None
        self.bonus_loot_label = None
        self.pc_loot = None
        self.power_gems_loot_label = None
        
    def show(self):
        screen.blit(self.image, self.rect)
        self.header.show_to_player()
        if self.winning_loot != None:
            self.winning_loot_label.show_to_player()
            self.winning_loot.show_to_player()
            self.power_gems_loot_label.show_to_player()        
            self.pc_loot.show_to_player()
            screen.blit(power_crystal, (self.winning_loot.rect.x - 40, self.winning_loot.rect.y))
            screen.blit(power_gem_image, (self.pc_loot.rect.x - 40, self.pc_loot.rect.y))
        if self.bonus_loot != None:
            self.bonus_loot.show_to_player()
        
    def generate_winnings(self, loot, power_gems, bonus_loot=None):
        accuracy = game['Current Level'].get_accuracy()
        self.winning_loot_label = Feedback('Rewards', upgrades_font, (self.rect.centerx, self.rect.top + self.rect.height * 0.25))
        self.winning_loot = Feedback(f'{int(loot)}', upgrades_font, (self.rect.centerx, self.winning_loot_label.rect.centery + self.winning_loot_label.rect.height + 10))
        self.power_gems_loot_label = Feedback(f'{accuracy}% Acc. Bonus', upgrades_font, (self.rect.centerx, self.winning_loot.rect.bottom + self.winning_loot.rect.height))
        self.pc_loot = Feedback(f'{int(power_gems)}', upgrades_font, (self.winning_loot.rect.centerx, self.power_gems_loot_label.rect.centery + self.power_gems_loot_label.rect.height + 10))
        
    def slide_to_middle(self, speed):
        self.loc.move_towards_ip((screen_width / 2, screen_height / 2), speed)
        self.rect.center = self.loc
        self.header.rect.center = (self.rect.centerx, self.rect.top + 50)
        if self.winning_loot != None:
            self.winning_loot_label.rect.center = (self.rect.centerx, self.rect.top + self.rect.height * 0.25)
            self.winning_loot.rect.center = (self.rect.centerx, self.winning_loot_label.rect.centery + self.winning_loot_label.rect.height + 10)
        if self.pc_loot != None:
            self.power_gems_loot_label.rect.center = (self.rect.centerx, self.winning_loot.rect.bottom + self.winning_loot.rect.height)
            self.pc_loot.rect.center = (self.winning_loot.rect.centerx, self.power_gems_loot_label.rect.centery + self.power_gems_loot_label.rect.height + 10)
        
    def slide_to_origin(self, speed):
        self.loc.move_towards_ip(self.origin_pos, speed)
        self.rect.center = self.loc
        self.header.rect.center = (self.rect.centerx, self.rect.top + 50)
        if self.winning_loot != None:
            self.winning_loot_label.rect.center = (self.rect.centerx, self.rect.top + self.rect.height * 0.25)
            self.winning_loot.rect.center = (self.rect.centerx, self.winning_loot_label.rect.centery + self.winning_loot_label.rect.height + 10)
        if self.pc_loot != None:
            self.power_gems_loot_label.rect.center = (self.rect.centerx, self.winning_loot.rect.bottom + self.winning_loot.rect.height)
            self.pc_loot.rect.center = (self.winning_loot.rect.centerx, self.power_gems_loot_label.rect.centery + self.power_gems_loot_label.rect.height + 10)

        
class Level:
 
    def __init__(self, image, num, num_of_types, enemy_types, button_pos, num_of_enemies, boss=None):
        self.image = image
        self.locked_image = locked_level_button_image
        self.rect = self.image.get_rect(center=button_pos)
        self.num = num
        self.enemy_types = enemy_types
        self.num_of_types = num_of_types 
        self.entry_button = NavButton(self.image, button_pos)
        self.locked_button = NavButton(locked_level_button_image, button_pos)
        self.spawn_delay = 4
        self.start_time = time()
        self.times_completed = 0
        self.num_of_enemies = num_of_enemies
        self.active_button = self.locked_button
        self.locked = True
        self.completed = False
        self.current_spawn_index = 0
        self.active_enemies = None
        self.scroll_amount = 0
        self.score_gain = 1.2345 * self.num
        self.player_base_starting_health = 0
        self.base_shield_starting_health = 0
        self.player_base_damage_taken = 0
        self.total_shots_taken = 0
        self.total_shots_hit = 0
        self.boss = boss
        self.notified_player_about_boss = False
        self.played_winning_sound = False
        self.played_defeated_sound = False
        self.boss_name = None
        
    def update(self):
        if self.locked is False:
             self.active_button = self.entry_button
        elif self.locked is True:
             self.active_button = self.locked_button 
        self.scroll()
        
    def is_boss_level(self):
        if self.active_enemies[-1].image in enemy_boss_images:
            return True
        
    def get_boss(self):
        try:
            image = enemy_boss_images[self.boss]
            return image
        except IndexError:
            return None
            
    def get_boss_stats(self):
        keys = [k for k in enemy_boss_types.keys()]
        stat_keys = [j for j in enemy_boss_types[keys[2]].keys()]
        stats = enemy_boss_types[keys[2]].copy()
        for i in stat_keys:
            if i == 'Health':
               stats[i] = enemy_boss_types[keys[2]][i] / 10
            elif i == 'Damage':
                stats[i] = enemy_boss_types[keys[2]][i] / 2
            elif i == 'Cooldown':
                stats[i] = enemy_boss_types[keys[2]][i] / 2
            elif type(enemy_boss_types[keys[2]][i]) == str:
                stats[i] = None
            
        return stats
        
    def show_boss_name_and_health(self):
        difference_ratio = self.active_enemies[-1].health / self.active_enemies[-1].max_health
        max_health_bar = pygame.Rect(screen_width * 0.25, 70, screen_width / 2, 20)
        current_health_bar = pygame.Rect(screen_width * 0.25, 70, max_health_bar.width * difference_ratio, 20)
        pygame.draw.rect(screen, 'red', max_health_bar, border_radius=10)
        pygame.draw.rect(screen, 'green', current_health_bar, border_radius=10)
        self.boss_name.show_to_player()
           
    def scroll(self):
        if self.scroll_amount > 0:
            self.entry_button.rect.centerx -= self.scroll_amount
            self.locked_button.rect.centerx -= self.scroll_amount
            self.entry_button.rect.centerx = self.entry_button.rect.centerx
            self.locked_button.rect.centerx = self.locked_button.rect.centerx
            self.scroll_amount = 0
        elif self.scroll_amount < 0:
            self.entry_button.rect.x -= self.scroll_amount
            self.locked_button.rect.x -= self.scroll_amount            
            self.entry_button.rect.centerx = self.entry_button.rect.centerx
            self.locked_button.rect.centerx = self.locked_button.rect.centerx
            self.scroll_amount = 0
         
    def loot_drop(self):
        return int(len(self.active_enemies) * 9.2 * self.num)
        
    def bonus_loot(self):
        return int(self.loot_drop() * 0.2)
    
    def get_accuracy(self):
        try:
            hit_factor = self.total_shots_hit / self.total_shots_taken
        except ZeroDivisionError:
            return 0
        else:
            return int((self.total_shots_hit / self.total_shots_taken) * 100)
    
    def power_gem_loot(self):
        try:
            hit_factor = self.total_shots_hit / self.total_shots_taken
            diff = 50 * hit_factor
        except ZeroDivisionError:
            if self.boss is None:
                return 0
            else:
                return int(100 * (self.num // 5))
        else:
            if self.boss is None:
                return int(diff)
            else:
                return int(diff + (100 * self.num // 5))
               
    def spawn_enemy(self):
        if self.current_spawn_index < len(self.active_enemies):
            enemy_group.add(self.active_enemies[self.current_spawn_index])
            self.current_spawn_index += 1
            
    def done_spawning(self):
        if self.current_spawn_index == len(self.active_enemies):
            return True
        
    def generate_enemies(self):
        queued_enemies = []
        names = [n for n in self.enemy_types.keys()]
        random_sort = []
        # Num of each type of enemy is equally split with total num of enemies
        for types in range(self.num_of_types):
            for each in range(self.num_of_enemies // self.num_of_types):
                rindex = self.enemy_types[names[types]]
                ry = random.randint(player_base.rect.top + 40, player_base.rect.bottom - 40)
                enemy = Enemy(enemy_ships[types], (screen_width + 100, ry), enemy_types[enemy_names[types]])
                queued_enemies.append(enemy)
        random.shuffle(queued_enemies)
        if self.boss != None:
            keys = [k for k in enemy_boss_types.keys()]
            queued_enemies.append(Enemy(enemy_boss_images[self.boss], (screen_width + enemy_boss_images[self.boss].get_width() + 100, screen_height / 2), enemy_boss_types[keys[self.boss]]))
            self.boss_name = Feedback('Boss', upgrades_font, (screen_width / 2, 50))
        return queued_enemies
        
    def configure_probabilities(self, num):
        start_weight = self.num_of_types
        chances = []
        for i in range(num):
            if len(chances) > 0:
                chances[i - 1] += 1
            chances.append(1)
        for j in range(len(chances)):
            chances[j] += start_weight - j
            if j > 5:
                n = j // 5 - 1
                chances[n] += 1.5                
            elif j == len(chances):
                chances[j] += 2
        return chances
        
    def load(self, base):
        self.completed = False
        self.played_winning_sound = False
        self.played_defeated_sound = False
        self.notified_player_about_boss = False
        self.spawn_delay = 4
        #level['Paused'] = False
        self.active_enemies = self.generate_enemies()
        self.current_spawn_index = 0
        self.player_base_starting_health = base.stats['Health']
        if base_shield in base_group:
            self.base_shield_starting_health = base_shield.health
        self.player_base_damage_taken = 0
        self.total_shots_hit = 0
        self.total_shots_taken = 0
        self.start_time = time()          
             

class Base(pygame.sprite.Sprite):
    loaded_saved_game = False
    loaded_game = None
    
    def __init__(self, image, pos, stats):
        super().__init__()
        self.image = image
        self.icon_image = pygame.transform.scale_by(image, 0.5)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask.outline()
        self.electrocuted_image = electrocuted_base
        self.poisoned_mask_surf = self.mask.to_surface(setcolor='green', unsetcolor=(0,0,0,0))
        self.poisoned_mask_surf = pygame.transform.scale_by(self.poisoned_mask_surf, 1.01)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.stats = stats
        self.lives = 5
        self.last_regen_time = time()
        self.poisoned = False
        self.poisoned_amount = 0
        self.poison_antidote_applied = False
        self.special_attack_used = False
        self.special_attack_in_use = None
        self.special_attack_start_time = time()
        self.special_defense_start_time = time()
        self.special_defense_used = False
        self.special_defense_duration = 30
        self.rapid_fire_delay = 1
        self.raining_comets_start_time = time()
        self.raining_comets_duration = 10
        self.last_comet_time = time()
        self.comet_delay = 0.5
        self.collided_enemy_bullets = {}
        self.electrified = False
        self.electrified_dot_num = self.mask_outline.index(random.choice(self.mask_outline))
        self.electrified_duration = 2
        self.electrified_delay = 0.4
        self.electrified_start_time = time()
        self.electrified_time = time()
        self.electrocution_damage = 0
        self.absorb_electric_shock = False
        self.absorb_electric_shock_time = time()
        self.health_bar_label = Feedback('Base', ui_font, (0, 0))
        
    def update(self, container):
        if self.poison_antidote_applied is True:
            self.image = base_main
            self.poisoned_amount = 0
        if self.poisoned is True:
            self.poisoned_damage()
            self.image = poisoned_base
        if self.stats['Health'] < self.stats['Max Health']:
            if level['Game Over'] is False:
                if self.stats['Health Regeneration'] == 'Active':
                    self.regenerate()
        container.show()
        self.health_bar_label.rect.center = (container.rect.centerx, container.rect.top + 20)
        self.health_bar_label.show_to_player()
        self.show_health(container)
        if self.absorb_electric_shock is True:
            self.shock_absorber()
              
        if self.electrified is True:
            screen.blit(self.electrocuted_image, self.rect)                                                                                                                          
            self.electrify_units()           
                
    def show_health(self, container):
        difference_ratio = self.stats['Health'] / self.stats['Max Health']
        max_health_bar = pygame.Rect(container.rect.left + 25, container.rect.centery - 25, container.rect.width - 50, 15)
        current_health_bar = pygame.Rect(container.rect.left + 25, container.rect.centery - 25, (container.rect.width - 50) * difference_ratio, 15)
        health_bar_outline = pygame.Rect(max_health_bar.x - 2, max_health_bar.y - 2, (container.rect.width - 50) + 4, 19)
        pygame.draw.rect(screen, 'black', health_bar_outline, 5, border_radius=5)
        pygame.draw.rect(screen, 'red', max_health_bar, border_radius=5)
        pygame.draw.rect(screen, 'green', current_health_bar, border_radius=5)
        
    def take_damage(self, amount):
        if self.stats['Health'] - amount < 0:
            self.stats['Health'] = 0
            if self.lives > 0:
                self.lives -= 1
        else:
            self.stats['Health'] -= amount
            
    def shock_absorber(self):
        screen.blit(vaporizing_arc_image, (self.rect.centerx, self.rect.top))
        #for point in self.mask_outline:
            #pygame.draw.circle(self.image, 'yellow', point, 5)
            
    def electrify_units(self):
        if time() - self.electrified_start_time < self.electrified_duration:
            self.image = self.electrocuted_image       
            if time() - self.electrified_time >= self.electrified_delay:               
                self.electrified_time = time()                
                self.image = base_main
                if game['Sounds'] is True:
                    electrocuted_sound.play()
                self.take_damage(self.electrocution_damage)            
        if time() - self.electrified_start_time >= self.electrified_duration:
            self.electrified = False
            self.image = base_main
            
    def poisoned_damage(self):
        if self.poisoned_amount > 0:
            if self.stats['Health'] - 3 <= 0:
                self.stats['Health'] = 0
                self.poisoned_amount = 0              
            else:
                self.stats['Health'] -= 3
                self.poisoned_amount -= 3
        else:
            self.poisoned = False
            self.image = base_main
            
    def regenerate(self):
        if time() - self.last_regen_time >= self.stats['Regen Cooldown (secs)']:
            if self.stats['Health'] < self.stats['Max Health']:
                if self.stats['Health'] + self.stats['Regen Amount'] >= self.stats['Max Health']:
                    self.stats['Health'] = self.stats['Max Health']
                else:
                    self.stats['Health'] += self.stats['Regen Amount']
                self.last_regen_time = time()
                
    def vaporize_enemies(self, group):
        for e in group:
            if e.image in enemy_ships:
                if e.rect.right < screen_width:
                    e.kill()
                    animations_group.add(Animation(impact_animation, 1, e.pos))
                    
    def meteor_shower(self, group):
        y = -100
        for i in range(50):
            x = random.randint(self.rect.right + 10, screen_width - 10)
            m = Meteor(tan_meteor, (x, y), 100, 200)
            group.add(m)
            y -= 50
            
    def cluster_shot(self, group):
        b = Bullet(cluster_laser_image, self.rect.center, base_turret.stats['Damage'], Turret.fire_speed)
        b.fired_by_player = True
        b.is_cluster = True
        group.add(b)
        
    def rain_comets(self, group):
        if time() - self.raining_comets_start_time < self.raining_comets_duration:
            if time() - self.last_comet_time > self.comet_delay:
                rx = random.randrange(-100, 500)
                comet = Comet(raining_comet_image, (rx, -200))
                group.add(comet)
                self.last_comet_time = time()
         
        
                        
class Shield(pygame.sprite.Sprite):
   
    def __init__(self, image, loc, stats):
        super().__init__()
        self.image = pygame.transform.scale(image, (base_main.get_width() + 50, base_main.get_height() + 50))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=loc)
        self.stats = stats
        self.health = self.stats['Max Health']
        self.last_regen_time = time()
        self.poisoned_amount = 0
        self.poisoned = False
        self.health_bar_label = Feedback('Shield', ui_font, (0, 0))
        
    def update(self, container):
        self.show()
        self.health_bar_label.rect.center = (container.rect.centerx, container.rect.centery + 15)
        self.health_bar_label.show_to_player()
        self.show_health(container)
              
    def show_health(self, container):
        difference_ratio = self.health / self.stats['Max Health']
        max_health_bar = pygame.Rect(container.rect.left + 25, container.rect.bottom - 30, container.rect.width - 50, 15)
        current_health_bar = pygame.Rect(container.rect.left + 25, container.rect.bottom - 30, (container.rect.width - 50) * difference_ratio, 15)
        health_bar_outline = pygame.Rect(max_health_bar.x - 2, max_health_bar.y - 2, (container.rect.width - 50) + 4, 19)
        pygame.draw.rect(screen, 'black', health_bar_outline, 5, border_radius=5)
        pygame.draw.rect(screen, 'blue', max_health_bar, border_radius=5)
        pygame.draw.rect(screen, 'cyan', current_health_bar, border_radius=5)
        
    def poisoned_damage(self):
        if self.poisoned_amount > 0:
            if self.health - 10 <= 0:
                self.health = 0
                self.poisoned_amount = 0
            else:
                self.health -= 10
                self.poisoned_amount -= 10
                self.image.set_alpha(255)
        else:
            self.poisoned = False
        
    def show(self):
        if self.poisoned is True:
            self.poisoned_damage()
        if self.image.get_alpha() > 0:
            img_alpha = self.image.get_alpha()
            self.image.set_alpha(img_alpha - 3)
        if self.health <= 0:
            self.stats['Status'] = 'Inactive'
            self.kill()
        if self.health < self.stats['Max Health'] and self.stats['Health Regeneration'] == 'Active':
            self.regenerate()
        
    def protect(self):
        screen.blit(self.image, self.rect)
        
    def take_damage(self, amount):
        if self.health - amount <= 0:
            self.health = 0
        else:
            self.health -= amount
        self.image.set_alpha(255)
        
    def regenerate(self):
        if time() - self.last_regen_time >= self.stats['Regen Cooldown (secs)']:
            if self.health >= self.stats['Max Health']:
                self.health = self.stats['Max Health']
            else:
                self.health += self.stats['Regen Amount']
                if self.health > self.stats['Max Health']:
                    self.health = self.stats['Max Health']
            self.last_regen_time = time()
            
            
class EnemyShield(pygame.sprite.Sprite):
   
    def __init__(self, image, pos, health):
        super().__init__()
        self.image = image
        self.pos = pygame.math.Vector2(pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)
        self.health = health
        self.max_health = health
        self.image.set_alpha(0)
        self.health_regeneration_amount = self.max_health * 0.015
        self.health_regeneration_rate = 1
        self.regenerate_delay = 30
        self.regeneration_multiplier = 0.015
        self.active = True
        self.poisoned = False
        self.connected_ship = None
        self.fire_speed = 10
        self.upgrade_health_cost = 2000
        self.upgrade_health_amount = 1.2
        
    def update(self):
        if self.active is True:
            if pygame.sprite.spritecollide(self, player_bullet_group, False):
                if pygame.sprite.spritecollide(self, player_bullet_group, False, pygame.sprite.collide_mask):
                    b = pygame.sprite.spritecollide(self, player_bullet_group, False, pygame.sprite.collide_mask)[0]
                    if b.mask.overlap(self.mask, (self.rect.x - b.rect.x, self.rect.y - b.rect.y)):                                                 #b.kill()
                        #pygame.sprite.spritecollide(self, player_bullet_group, True, pygame.sprite.collide_mask)
                        self.take_damage(b.damage)
                        b.kill()
        self.show()     
        self.rect = self.image.get_rect(center=self.connected_ship.pos)
        
    def show_health(self):
        difference_ratio = self.health / self.max_health
        max_health_bar = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.width, 15)
        current_health_bar = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.width * difference_ratio, 15)
        pygame.draw.rect(screen, 'red', max_health_bar, border_radius=5)
        pygame.draw.rect(screen, 'cyan', current_health_bar, border_radius=5)
        
    def show(self):
        if self.image.get_alpha() > 0:
            img_alpha = self.image.get_alpha()
            self.image.set_alpha(img_alpha - 3)
            if self.active is True:
                self.protect()
                if self.health < self.max_health:
                    self.show_health()
        if self.health <= 0:
            self.active = False
            self.kill() 
        
    def protect(self):
        screen.blit(self.image, self.rect)
        
    def activate(self):
        self.active = True
        self.health = self.max_health
        self.image.set_alpha(255)
        
    def take_damage(self, amount):
        self.health -= amount
        self.image.set_alpha(255)
        
        
class StatsContainer:
            
    def __init__(self, image, pos):
        self.image = image
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        
    def open_container(self):
        pass
        #slide container up from the bottom
        
    def close_container(self):
        pass
        #slide container down below and out of view
        
    def show(self):
        screen.blit(self.image, self.rect)
        
            
class Turret:
    
    helpers_engage = False
    fire_speed = 700
    
    def __init__(self, image, pos, stats):
        self.image = image
        self.idle_image = image
        self.updated_image = image
        self.manipulated_electrocuted_image = electrocuted_turret
        self.electrocuted_image = electrocuted_turret
        self.updated_rect = self.updated_image.get_rect(center=pygame.math.Vector2(pos))
        self.idle_rect = self.idle_image.get_rect(center=pygame.math.Vector2(pos))
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.stats = stats
        self.full_range = screen_width - player_base.rect.right
        self.last_shot_time = time()
        self.hostile = False
        self.is_idle = True
        self.attack = False
        self.engage = False
        self.target_set = False
        self.target = None
        self.special_in_use = False
        self.special = None
        self.special_duration = 30
        self.special_start_time = time()
        self.paralyzed = False
        self.paralyzed_start_time = time()
        self.reengage_time = random.choice([0.24, 0.4, 0.3, 0.2])
        self.reengage_attempt_time = time()
        self.paralyzed_duration = 2
        
    def update(self, group):
        if len(group) > 0:
            self.attack = True
        elif len(group) == 0:
            self.attack = False
        if self.attack is True and self.paralyzed is False:
            self.lock_on_target(group)
            if self.target.alive() is False:
                # Resetting target position
                self.target_set = False
        if self.paralyzed is True:
            self.attack = False
        
    def draw(self):
        if self.paralyzed is False:
            if self.attack is True:
                screen.blit(self.updated_image, self.updated_rect)
            elif self.attack is False:
                screen.blit(self.idle_image, self.idle_rect)
        if self.paralyzed is True:
            if time() - self.paralyzed_start_time < self.paralyzed_duration:
                if time() - self.reengage_attempt_time >= self.reengage_time:
                    self.reengage_attempt_time = time()
                    screen.blit(self.idle_image, self.idle_rect)
                else:
                    screen.blit(self.electrocuted_image, self.idle_rect)
            else:
                self.paralyzed = False
            
    def target_in_range(self):
        if 'Range %' in self.stats:
            if abs(self.target.pos.x - player_base.rect.right) <= (self.stats['Range %'] / 100) * self.full_range:
                return True      
        
    def set_idle_image(self, img, angle):
        self.idle_image = pygame.transform.rotate(self.image, angle - 90)
        self.electrocuted_image = pygame.transform.rotate(self.manipulated_electrocuted_image, angle - 90)
        self.idle_rect = self.idle_image.get_rect(center = pygame.math.Vector2(self.rect.center))
       
    def lock_on_target(self, target_group):
        # Extra turrets will use this function
        if self.target_set is False:
            if len(target_group) > 0:
                for i in target_group:
                    self.target = i
                    break
                self.target_set = True
                self.engage = True
      
        if self.engage is True:
           self.find_closest_target(target_group)
           self.aim_at(self.target)                      
      
    def find_closest_target(self, group):
        for i in group:
            if self.distance_to(i) < self.distance_to(self.target):
                self.target = i
                break
                  
    def distance_to(self, target):
        return pygame.math.Vector2(self.rect.center).distance_to((target.pos.x, target.pos.y))
    
    def aim_at(self, target):
        x_dist = target.rect.x-10 - self.rect.centerx
        y_dist = -(target.rect.centery - self.rect.centery)
        angle = math.degrees(math.atan2(y_dist, x_dist))
        self.updated_image = pygame.transform.rotate(self.image, angle - 90)
        self.updated_rect = self.updated_image.get_rect(center = pygame.math.Vector2(self.rect.center))
        self.set_idle_image(self.updated_image, angle)
        
    def follow_mouse_pos(self):
        # Main turret will use this function
        x_dist = pygame.mouse.get_pos()[0] - self.rect.centerx
        y_dist = -(pygame.mouse.get_pos()[1]- self.rect.centery)
        angle = math.degrees(math.atan2(y_dist, x_dist))
        image = pygame.transform.rotate(self.image, angle - 90)
        self.rect = image.get_rect(center = pygame.math.Vector2(self.rect.center))
        screen.blit(image, self.rect)
        
    def shoot(self, group):
        hits = [self.stats['Damage'], int(self.stats['Damage'] * self.stats['Critical Hit'])]
        hit_weights = np.array([100 - self.stats['Critical Hit Chance %'], self.stats['Critical Hit Chance %']])
        hit_chances = random.choices(hits, weights=hit_weights, k=100)
        chosen_damage = random.choice(hit_chances)
        if chosen_damage > self.stats['Damage']:  
            laser_image = critical_laser_image
        else:
            laser_image = player_laser
        b = Bullet(laser_image, self.rect.center, chosen_damage, self.fire_speed)
        b.fired_by_player = True
        b.player_shot = True
        group.add(b)
        if game['Sounds'] is True:
            turret_shot_fired.play()
        self.last_shot_time = time()
        
    def help_shoot(self, group):
        if time() - self.last_shot_time >= self.stats['Cooldown (secs)']:
            if self.target.alive() is True:
                hits = [self.stats['Damage'], int(self.stats['Damage'] * self.stats['Critical Hit'])]
                hit_weights = np.array([100 - self.stats['Critical Hit Chance %'], self.stats['Critical Hit Chance %']])
                hit_chances = random.choices(hits, weights=hit_weights)
                chosen_damage = random.choice(hit_chances)
                if chosen_damage > self.stats['Damage']:  
                    laser_image = critical_laser_image
                else:
                    laser_image = player_laser
                b = Bullet(laser_image, self.rect.center, chosen_damage, self.fire_speed)
                b.fired_by_helper = True
                b.target = self.target
                group.add(b)
                if game['Sounds'] is True:
                    helper_turret_shot_sound.play()
                self.last_shot_time = time()
                
                
class EnemyTurret(pygame.sprite.Sprite):
    
    def __init__(self, image, pos, stats):
        super().__init__()
        self.image = image
        self.idle_image = image
        self.updated_image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.updated_rect = self.updated_image.get_rect(center=pygame.math.Vector2(pos))
        self.idle_rect = self.idle_image.get_rect(center=pygame.math.Vector2(pos))
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.stats = stats
        self.max_health = self.stats['Health']
        self.full_range = screen_width - player_base.rect.right
        self.last_shot_time = time()
        self.fire_speed = 500
        self.hostile = False
        self.is_idle = True
        self.attack = False
        self.engage = False
        self.target_set = False
        self.target = player_base
        self.special_in_use = None
        self.last_flare_deploy_time = time()
        
    def update(self, dt):
        self.fire_at_player()
        self.hit_by_player()
        if self.stats['Health'] < self.max_health:
            self.show_health()
        if self.stats['Health'] <= 0:
            self.kill()
            
    def defense_flares(self):
        b = Bullet(laser_flare, self.rect.center, self.stats['Damage'] / 2, self.fire_speed / 2)
        b.is_hostile = True
        b.flare = True
        b.is_flare = True
        b.flare_id = i + 1
        b.set_flare()
        b.flared_pos = pygame.math.Vector2(screen_width * 0.45, random.randint(player_base.rect.top, player_base.rect.bottom))
        flares_group.add(b)
            
    def draw(self):
        screen.blit(self.image, self.rect)
            
    def show_health(self):
        difference_ratio = self.stats['Health'] / self.max_health
        max_health_bar = pygame.Rect(self.rect.centerx, self.rect.y, 200, 15)
        current_health_bar = pygame.Rect(self.rect.centerx, self.rect.y, 200 * difference_ratio, 15)
        pygame.draw.rect(screen, 'red', max_health_bar, border_radius=5)
        pygame.draw.rect(screen, 'green', current_health_bar, border_radius=5)
        
    def aim_at(self, target):
        x_dist = target.rect.x-10 - self.rect.centerx
        y_dist = -(target.rect.centery - self.rect.centery)
        angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.image, angle - 90)
        self.rect = self.image.get_rect(center = pygame.math.Vector2(self.rect.center))
        self.set_idle_image(self.image, angle)
        self.mask = pygame.mask.from_surface(self.image)
        
    def set_idle_image(self, img, angle):
        self.idle_image = pygame.transform.rotate(self.image, angle - 90)
        self.idle_rect = self.idle_image.get_rect(center = pygame.math.Vector2(self.rect.center))
        
    def fire_at_player(self):
        if self.target_set is False:
            self.aim_at(self.target)
            self.target_set = True
        if time() - self.last_shot_time >= self.stats['Cooldown']:
            if self.target.stats['Health'] > 0:
                b = Bullet(enemy_turret_laser, self.rect.center, self.stats['Damage'], self.fire_speed / 2)
                b.is_hostile = True
                b.locate_target(self.target.rect.center)
                b.set_velocity(target=self.target)
                enemy_bullet_group.add(b)
                self.last_shot_time = time()  
                
    def hit_by_player(self):
        if pygame.sprite.spritecollide(self, player_bullet_group, False):
            for b in pygame.sprite.spritecollide(self, player_bullet_group, True, pygame.sprite.collide_mask):
                if self.stats['Health'] - b.damage <= 0:
                    self.stats['Health'] = 0
                else:
                    self.stats['Health'] -= b.damage
                
    def electric_chain(self, point1, point2):
        pygame.draw.line(screen, 'cyan', self.rect.center, point1, 3)
        pygame.draw.line(screen, 'cyan', point1, point2, 3)  


class Enemy(pygame.sprite.Sprite):
    
    spawn_time = time()
    start_spawn = time()
    spawn = False
    
    def __init__(self, image, pos, stats):
        super().__init__()
        self.self = self
        self.image = image
        self.self = self
        self.pos = pygame.math.Vector2(pos)
        self.stats = stats
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.mask = pygame.mask.from_surface(self.image)
        self.health = stats['Health']
        self.max_health = stats['Health']
        self.damage = stats['Damage']
        self.cooldown = stats['Shot Cooldown']
        self.range = stats['Range']
        self.speed = self.stats['Speed']
        self.fire_speed = 400
        self.shield = self.create_shield()
        self.shot_duration = 0
        self.last_shot_time = time()
        self.beam_start_time = time()
        self.beam_rect = pygame.Rect(self.rect.centerx, self.rect.centery - 10, 100, 20)
        self.last_regen_time = time()
        self.tank_pos = pygame.math.Vector2(self.pos.x, self.pos.y - 50)
        self.tank_spawn_time = time()
        self.tanks_delivered = 0
        self.drone_spawns = 10
        self.num_of_drones = 0
        self.last_teleport_time = time()
        self.teleport_delay = 5
        self.special_fires = 0
        self.missile_launcher_engaged = 'Top'
        self.last_missile_shot_time = time()
        self.moving = True
        self.firing = False
        self.turret_spawn_time = time()
        self.last_flare_deploy_time = time()
        self.engage_missiles_time = time()
        self.reengage_missiles_delay = 5
        self.engage_missiles_duration = 5
        self.healing_ring_engaged = False
        self.healing_mask_surf = self.mask.to_surface(setcolor='yellow', unsetcolor=(0, 0, 0, 0)).convert_alpha()
        self.paralyze_shot_time = 2
        self.black_hole_death = False
        self.black_hole = None
        self.healer = False
        if self.has_special():
            if self.stats['Special'] == 'Radial Healing':
                self.health_recovery_ring = HealingRing(healer_ring_with_effect_image, self.pos)
                self.healer = True
            elif self.stats['Special'] == 'Magic Spawn':
                self.magic_spawn()
        
    def update(self, delta_time):
        if self.has_shield():
            if self.shield.active is True:
                self.shield.update()       
                             
        if self.health < self.max_health and self.image in enemy_ships:
            self.show_health()
            
        # Checking if enemy type is a boss
        if self.image in enemy_boss_images:           
                if self.stats['Special'] == 'Spawn Turrets':
                # Boss number 2 firing Special shot
                    if self.pos.x < screen_width + 100:
                        if self.special_fires == 0:
                            self.spawn_turret_shot()
                            self.turret_spawn_time = time()
                            self.special_fires += 1
                                                    
                elif self.stats['Special'] == 'Drones':
                # Boss number 3 spawns mini drones to attack
                    if self.in_range(player_base):
                        if self.num_of_drones < self.drone_spawns:
                            if time() - self.last_shot_time >= 0.5:
                                if player_base.stats['Health'] > 0:
                                    self.spawn_drone_shot()
                                    self.num_of_drones += 1
                                    self.last_shot_time = time()
                                    
                elif self.stats['Special'] == 'Side Missiles':               
                # Boss number 4 shoots out Missiles from both sides alternatively
                    if self.in_range(player_base):
                        if player_base.stats['Health'] > 0:
                            if 0 < time() - self.engage_missiles_time < self.engage_missiles_duration:
                                if time() - self.last_missile_shot_time >= 0.5:
                                    self.fire_side_missile(enemy_missile_group)
                                    self.last_missile_shot_time = time()
                                    
                            # Boss will re-engage missile launchers
                            if time() - self.engage_missiles_time >= self.engage_missiles_duration + self.reengage_missiles_delay:
                                self.engage_missiles_time = time()
                                
                if self.stats['Special'] == 'Laser Deflection':
                    pass
                                                                     
                if self.stats['Special'] == 'Gold Laser':
                    self.shot_duration = 1
                    # Boss number 7 shoots a solid gold laser beam doing constant damage
                    if self.in_range(player_base):
                        self.moving = False
                        if player_base.stats['Health'] > 0:
                            if time() - self.last_shot_time + self.shot_duration > self.cooldown:
                                self.last_shot_time = time()
                            if time() - self.last_shot_time <= self.shot_duration:
                                self.fire_laser_beam(laser_beam_group)
            
        if self.health <= 0:
            self.kill()
            animations_group.add(Animation(ship_explosion, 2.5, self.pos, ship_explosion_sound))
            if self.stats['Special'] == 'Hydra Spawn':
                self.hydra_spawn()
            elif self.stats['Special'] == 'Bomb Drop':
                self.drop_bomb()
                    
        if self.moving is True:
            if self.black_hole_death is True:
                self.pos.move_towards_ip(self.black_hole.pos, 5)               
                self.rect.center = self.pos
            else:
                self.pos.x -= self.speed * delta_time * level['Speed']
                self.rect.center = self.pos
            
        if self.stats['Special'] == 'Turret Paralyzer':
            if self.in_range(player_base):
                if 0 < time() - self.last_shot_time < self.paralyze_shot_time:
                    self.paralyze_turret()
                if time() - self.last_shot_time >= self.cooldown:
                    self.last_shot_time = time()
                    
        if self.stats['Special'] == 'Teleport':
            if time() - self.last_teleport_time >= self.teleport_delay:
                self.teleport()
                self.last_teleport_time = time()
            
        # Self healing ship
        if self.stats['Special'] == 'Health Regeneration':
            self.regenerate_health()
        
        if self.stats['Special'] == 'Linger Flares':
            if self.in_range(player_base):
                if time() - self.last_flare_deploy_time > 0.5:
                    if self.rect.right < screen_width:
                        self.deploy_flares(flares_group)
                        self.last_flare_deploy_time = time()
            
        if self.stats['Special'] == 'Kamikaze':
            self.pos.x -= self.speed * delta_time * level['Speed']
            self.rect.center = self.pos
            if pygame.sprite.spritecollide(self, base_group, False):
                base_hit = pygame.sprite.spritecollide(self, base_group, False, pygame.sprite.collide_mask)
                if base_hit:
                    for i in base_hit:
                        i.take_damage(self.max_health)
                        self.kill()
                        animations_group.add(Animation(ship_explosion, 2.5, self.pos, ship_explosion_sound))   
        
        # Enemy Defenses
        if self.has_defense():
            # Boss number 1 spawning Flares as Laser protection
            if self.stats['Defense'] == 'Flares':
                if self.in_range(player_base):
                    if time() - self.last_flare_deploy_time > 0.2:
                        self.deploy_flares(flares_group)
                        self.last_flare_deploy_time = time()
                                    
        # Enemy is within range to shoot
        if self.in_range(player_base):
            self.moving = False
            if self.black_hole_death is True:
                self.pos.move_towards_ip(self.black_hole.pos, 5)
                self.rect.center = self.pos
            
            if self.stats['Special'] == 'Tanker Delivery':
                if self.tanks_delivered < 5:
                    if time() - self.tank_spawn_time >= 10 and player_base.stats['Health'] > 0:
                        animations_group.add(Animation(spawn_animation, 2, self.pos))
                        enemy_group.add(Enemy(enemy_ships[23], self.pos, enemy_types['Plasma Tanker']))
                        self.tank_spawn_time = time()
                        self.tanks_delivered += 1
                    
            # Healer ship
            elif self.stats['Special'] == 'Radial Healing':
                if self.healing_ring_engaged is False:
                    self.engage_healing_ring()
                    self.healing_ring_engaged = True                                

            # Enemy firing attacks
            if time() - self.last_shot_time >= self.cooldown:
                if player_base.stats['Health'] > 0:
                        if self.stats['Special'] == 'Double Shot':
                            self.double_shot()
                        elif self.stats['Special'] == 'Triple Shot':
                            self.triple_shot()
                        elif self.stats['Special'] == 'Poison Laser':                  
                            self.poison_shot(self.damage)
                        elif self.stats['Special'] == 'Shield Destroy':
                            if base_shield.stats['Status'] == 'Active':
                                self.destroy_shield_shot()
                            else:
                                self.fire()
                        elif self.stats['Special'] == 'Wave Blast':
                            self.wave_blast(group)
                        elif self.stats['Special'] == 'Speed Shot':
                            self.fire_speed = 500
                            self.fire()
                        elif self.stats['Special'] == 'Charge Bolt':
                            self.emit_charge_bolt()
                        elif self.stats['Special'] == 'Cluster Bomb':
                            self.cluster_bombs()
                        else:
                            self.fire()                            
                    #else:
                        #self.fire(group)
                        self.last_shot_time = time()
                    
        self.recovery_collision()
        
        # destroy ship if its size is less than 5px wide and 5px tall
        if self.image.get_size()[0] <= 5 and self.image.get_size()[1] <= 5:
             self.kill()
             
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def take_damage(self, amount):
        if self.health - amount <= 0:
            self.health = 0
        else:
            self.health -= amount 
    
    def in_range(self, base):
        if abs((self.pos.x - self.image.get_width() / 2) - base.rect.right) <= self.range:
            return True
            
    def recovery_collision(self):
        if pygame.sprite.spritecollide(self, health_flares_group, False):
            collisions = pygame.sprite.spritecollide(self, health_flares_group, False, pygame.sprite.collide_mask)
            if collisions:
                for c in collisions:
                    if c.mini is False and self.healer is False:
                        self.regenerate_health()
                        
    def paralyze_turret(self):
        for h in helper_turret_group:
            if h.paralyzed is False:
                pygame.draw.line(screen, 'yellow', self.pos, h.pos, 5)
                print(self.pos.lerp(h.pos, 0.5))
            
    def drone(self, pos):      
        drone_image = pygame.transform.scale_by(self.image, 0.5)
        drone_stats = self.stats.copy()
        for i in drone_stats:
            if type(drone_stats[i]) == int or type(drone_stats[i]) == float:
                drone_stats[i] /= 2
            else:
                drone_stats[i] = None
        return Enemy(drone_image, pos, drone_stats)
        
    def engage_healing_ring(self):
        ring = HealingRing(healer_ring_with_effect_image, self.pos)
        ring.owner_ship = self.self
        healing_ring_group.add(ring)
        
    def emit_charge_bolt(self):
        cb = ChargeBolt(charge_bolt_image, self.pos, self.damage)
        enemy_bullet_group.add(cb)
          
    def fire_laser_beam(self, group):
        b = Laser(solid_laser_image, self.rect.center, self.damage)
        group.add(b)
        
    def fire_side_missile(self, group):
        if self.missile_launcher_engaged == 'Top':
            b = Missile(side_missile_image, (self.pos.x + 90, self.pos.y - 90), self.damage * 1.5,  self.fire_speed)
            self.missile_launcher_engaged = 'Bottom'
        elif self.missile_launcher_engaged == 'Bottom':
            b = Missile(side_missile_image, (self.pos.x + 90, self.pos.y + 90), self.damage * 1.5,  self.fire_speed)
            self.missile_launcher_engaged = 'Top'
        b.threshold = pygame.math.Vector2((b.pos.x - 10, b.pos.y))
        b.target = pygame.math.Vector2(player_base.rect.center)
        group.add(b)
                
    def teleport(self, base, group):
        group.add(Animation(impact_animation, 1, self.pos))
        self.pos.x += random.randint(150, 500)
        self.pos.y = random.randrange(int(player_base.rect.top + self.rect.height), int(player_base.rect.bottom - self.rect.height / 2))
        self.rect.center = self.pos
        group.add(Animation(impact_animation, 1, self.pos))
        
    def spawn_drone_shot(self):
        y = (player_base.rect.top + 50) + (50 * self.num_of_drones+1)
        orb = SpawnOrb(turret_spawn_orb, self.pos, (self.rect.x - 200, y))
        orb.spawn_item = Enemy(self.image, orb.spawn_pos, self.stats.copy())
        spawn_orb_group.add(orb)
        
    def spawn_defense_wall(self):
        orb1 = SpawnOrb(turret_spawn_orb, self.pos, (screen_width * 0.45, player_base.rect.top))
        orb2 = SpawnOrb(turret_spawn_orb, self.pos, (screen_width * 0.45, player_base.rect.bottom))
        orb1.spawn_item = DefenseWall(orb1.pos, screen_height / 2)
        orb2.spawn_item = DefenseWall(orb2.pos, screen_height / 2)
        spawn_orb_group.add(orb1, orb2)
        
    def spawn_turret_shot(self):
        orb = SpawnOrb(turret_spawn_orb, self.pos, (screen_width * 0.4, self.pos.y))
        orb.spawn_item = EnemyTurret(turret_extra, orb.pos, enemy_turret_stats.copy())
        orb.replicate = True
        orb.replicate_num = 2
        spawn_orb_group.add(orb)
                
    def magic_spawn(self):
        animations_group.add(Animation(impact_animation, 1, self.pos))
        self.pos.x = random.randrange(player_base.rect.right + self.range, screen_width)
        self.pos.y = random.randrange(int(player_base.rect.top + self.rect.height), int(player_base.rect.bottom - self.rect.height / 2))
        self.rect.center = self.pos
        animations_group.add(Animation(impact_animation, 1, self.pos))
    
    def show_health(self):
        difference_ratio = self.health / self.max_health
        max_health_bar = pygame.Rect(self.rect.x, self.rect.bottom + 5, self.rect.width, 15)
        current_health_bar = pygame.Rect(self.rect.x, self.rect.bottom + 5, self.rect.width * difference_ratio, 15)
        pygame.draw.rect(screen, 'red', max_health_bar, border_radius=5)
        pygame.draw.rect(screen, 'green', current_health_bar, border_radius=5)
        
    def has_special(self):
        if 'Special' in self.stats.keys():
            return True
            
    def has_defense(self):
        if 'Defense' in self.stats.keys():
            return True
            
    def has_shield(self):
        if 'Shield' in self.stats.keys():
            return True
        else:
            return False
            
    def regenerate_health(self):
        if self.health < self.max_health:
            if time() - self.last_regen_time > 0.05:
                self.health += self.max_health * 0.01
                self.last_regen_time = time()
                self.healing_glow()       
                
    def healing_glow(self):
        image = pygame.transform.scale_by(health_recovery_icon_image, 0.75)
        x = random.randint(self.rect.left + 10, self.rect.right - 10)
        flare = Flare(image, (x, self.rect.centery), (x, self.rect.top))
        flare.mini = True
        flare.speed = 30
        health_flares_group.add(flare)
        
    def create_shield(self):
        if self.has_shield() is True:
            _shield = pygame.transform.scale(shield_main, (self.rect.width + 50, self.rect.height + 50))
            shield = EnemyShield(_shield, self.rect.center, self.max_health)
            shield.connected_ship = self.self
            return shield
        else:
            return None
            
    def fire(self):
        b = Bullet(enemy_laser, self.rect.center, self.damage,  self.fire_speed)
        b.is_hostile = True
        enemy_bullet_group.add(b)
           
    def double_shot(self):
        b1 = Bullet(enemy_laser, (self.rect.centerx, self.rect.centery - 15), self.damage,  self.fire_speed)
        b2 = Bullet(enemy_laser, (self.rect.centerx, self.rect.centery + 15), self.damage,  self.fire_speed)
        b1.is_hostile = True
        b2.is_hostile = True
        enemy_bullet_group.add(b1, b2)
        
    def triple_shot(self):
        b1 = Bullet(enemy_laser, (self.rect.centerx, self.rect.centery - 15), self.damage,  self.fire_speed)
        b2 = Bullet(enemy_laser, self.rect.center, self.damage,  self.fire_speed)
        b3 = Bullet(enemy_laser, (self.rect.centerx, self.rect.centery + 15), self.damage,  self.fire_speed)
        b1.is_hostile = True
        b2.is_hostile = True
        b3.is_hostile = True
        enemy_bullet_group.add(b1, b2, b3)
        
    def poison_shot(self, poison_amount):
        b = Bullet(poison_laser, self.rect.center, self.damage,  self.fire_speed)
        b.is_hostile = True
        b.poisonous = True
        b.poison_amount = poison_amount
        enemy_bullet_group.add(b)
        
    def destroy_shield_shot(self):
        b = Bullet(destroy_shield_laser, self.rect.center, base_shield.stats['Max Health'],  self.fire_speed)
        b.is_hostile = True
        enemy_bullet_group.add(b)
        
    def wave_blast(self, group):
        b = Bullet(wave_blast_image, (self.rect.centerx - 25, self.rect.centery), self.damage, self.fire_speed)
        b.is_hostile = True
        b.wave_blast = True 
        group.add(b)
        
    def deploy_flares(self, group):
        for i in range(2):
            b = Bullet(laser_flare, self.rect.center, self.damage / 2, self.fire_speed / 2)
            b.is_hostile = True
            b.flare = True
            b.is_flare = True
            b.flare_id = i + 1
            b.set_flare()
            b.flared_pos = pygame.math.Vector2(self.rect.left - 10, random.randint(self.rect.top, self.rect.bottom))
            group.add(b)
        
    def hydra_spawn(self):
         if self.alive() is False:
             index = np.where(enemy_ships == self.image)[0][0]
             new_ship = enemy_ships[index - 1]
             new_stats = enemy_types[enemy_names[index - 1]]
             spawn_offset = 50
             enemy_group.add(Enemy(new_ship, (self.pos.x, self.pos.y - spawn_offset), new_stats))
             enemy_group.add(Enemy(new_ship, (self.pos.x, self.pos.y + spawn_offset), new_stats))
            
    def spawn_reinforcements(self):
         x_offset = 75
         y_offset = -75
         index = np.where(enemy_ships == self.image)[0][0]
         for i in range(3):
             x = self.rect.centerx + x_offset
             y = self.rect.centery + y_offset
             e = Enemy(enemy_ships[index - 2], (x, y), enemy_types[enemy_names[index - 2]])
             enemy_group.add(e)
             if i == 1:
                 x_offset *= 2
                 y_offset = 0
             else:
                 y_offset *= -1
                 
    def drop_bomb(self):
        b = Bomb(enemy_rubble_bomb, self.rect.center, self.damage * 2, 80)
        b.is_hostile = True
        enemy_bullet_group.add(b)
        
    def cluster_bombs(self):
        y_moves = [10, 0, -10]
        for y in y_moves:
            b = Bomb(enemy_rubble_bomb, self.rect.center, self.damage * 2, 80)
            b.is_hostile = True
            b.velocity_vector.y = y
            bomb_group.add(b)
        
        
class SpawnOrb(pygame.sprite.Sprite):
         
    def __init__(self, image, pos, spawn_pos):
         super().__init__()
         self.image = image
         self.pos = pygame.math.Vector2(pos)
         self.spawn_pos = pygame.math.Vector2(spawn_pos)
         self.rect = self.image.get_rect(center=self.pos)
         self.speed = 10
         self.spawn_item = None
         self.replicate = False
         self.replicate_num = 0
         self.num_replicated = 0
         self.spawn = False
         self.traveling = True
         self.stopped_traveling_time = time()
          
    def update(self, self_group):
        if self.traveling is False:
            if self.ready_to_spawn():
                animations_group.add(Animation(spawn_animation, 3, self.pos))
                if type(self.spawn_item) == EnemyTurret:
                    enemy_group.add(EnemyTurret(turret_extra, self.pos, enemy_turret_stats.copy()))
                elif type(self.spawn_item) == Enemy:
                    boss_image = game['Current Level'].get_boss()
                    boss_stats = game['Current Level'].get_boss_stats()
                    drone = self.spawn_drone(boss_image, boss_stats)
                    enemy_group.add(drone)
                self.kill()                      
                        
        # Orb is moving to its position to Spawn its spawn_item
        if self.traveling is True:
            self.pos.move_towards_ip(self.spawn_pos, self.speed)
            self.rect.center = self.pos
            if self.pos == self.spawn_pos:
                self.stopped_traveling_time = time()
                self.traveling = False          
        if self.replicate is True and self.traveling is False:
            y_spacer = 90      
            y = self.rect.height * 2
            x = 50
            for i  in range(self.replicate_num):
                orb = SpawnOrb(self.image, self.spawn_pos, (self.pos.x - x, self.pos.y + y + y_spacer))
                orb.spawn_item = self.spawn_item
                self_group.add(orb)
                self.num_replicated += 1
                y_spacer = -y_spacer
                y = -y
                 
                if self.num_replicated == 2:
                    y *= 1.5
                    y_spacer *= 1.5
            self.replicate = False
             
        if self.ready_to_spawn():
            self.spawn = True
             
    def spawn_drone(self, image, stats):
        drone = pygame.transform.scale_by(image, 0.25)
        return Enemy(drone, self.pos, stats)     
         
    def ready_to_spawn(self):
        if time() - self.stopped_traveling_time >= 3:
            return True
            
                      
class Bullet(pygame.sprite.Sprite):
        
    def __init__(self, image, pos, damage, speed):
        super().__init__()
        self.self = self
        self.image = image
        self.pos = pygame.math.Vector2(pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)
        self.damage = damage
        self.fire_speed = speed
        self.is_hostile = False
        self.poisonous = False
        self.poison_amount = 0
        self.fired_by_player = False
        self.fired_by_helper = False
        self.player_shot = False
        self.target = None
        self.wave_blast = False
        self.is_cluster = False
        self.cluster = False 
        self.is_flare = False
        self.flare = False
        self.laser_beam = False
        self.shot_time = time()
        self.firing_ship = None
        self.flare_x = 0
        self.flare_y = 0
        self.flare_id = 0
        self.flared_pos = pygame.math.Vector2(self.pos)
        self.hits = 5
        self.spray = False
        self.velocity_vector = pygame.math.Vector2(0, 0)
        self.creation_time = time()
        
    def update(self):    
        if self.fired_by_player is True:            
            self.locate_target(pygame.mouse.get_pos())
            self.set_velocity()    
            self.fired_by_player = False           
        if self.fired_by_helper is True and self.target != None:
            self.locate_target(self.target.pos)
            self.set_velocity()
            self.fired_by_helper = False
        if self.fired_by_helper is False:
            self.pos.x += self.velocity_vector.x * game['Delta Time'] * level['Speed']
            self.pos.y += self.velocity_vector.y * game['Delta Time'] * level['Speed']
            self.rect.center = self.pos
        if self.spray is True:
            # fired by player
            self.set_velocity()   
            self.pos.x += self.velocity_vector.x * game['Delta Time'] * level['Speed']
            self.pos.y += self.velocity_vector.y * game['Delta Time'] * level['Speed']
            self.rect.center = self.pos
            
        if self.is_cluster is True and self.rect.left >= player_base.rect.right:
            self.form_cluster(player_bullet_group)           
            
        if self.flare is True and self.is_hostile is True:
            self.flare_out()
            if time() - self.creation_time > 10:
                self.kill()             
        
        if self.is_hostile is True and self.flare is False:          
            self.pos.x -= self.fire_speed * game['Delta Time'] * level['Speed']
            self.rect.center = self.pos
            if self.wave_blast is True:
                self.force_push()           

        if self.rect.centerx < -10 or self.rect.centerx > screen_width or \
        self.rect.centery < 0 or self.rect.centery > screen_height:
            self.kill()
                   
    def locate_target(self, target_pos):
        # finds target and rotates image to point at target position
        x_dist = target_pos[0] - self.pos.x
        y_dist = -(target_pos[1]- self.pos.y)
        angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.image, angle - 90)
        self.rect = self.image.get_rect(center = self.rect.center)
        
    def set_velocity(self, target=None):
        if self.fired_by_helper is True:
            pos = pygame.math.Vector2(self.target.rect.center)
            distance = pygame.math.Vector2(self.rect.center).distance_to(pos)
            self.velocity_vector.x = self.fire_speed * (self.target.pos.x - self.pos.x) / distance
            self.velocity_vector.y = self.fire_speed * (self.target.pos.y - self.pos.y) / distance
        elif self.is_hostile is True:
            pos = pygame.math.Vector2(target.rect.center)
            distance = pygame.math.Vector2(self.rect.center).distance_to(pos)
            self.velocity_vector.x = self.fire_speed * (target.rect.centerx - self.pos.x) / distance
            self.velocity_vector.y = self.fire_speed * (target.rect.centery - self.pos.y) / distance
        elif self.cluster is True:
            self.set_flare()
            distance = pygame.math.Vector2(self.rect.center).distance_to(self.flared_pos)
            self.velocity_vector.x = self.fire_speed * (self.flared_pos.x - self.pos.x) / distance
            self.velocity_vector.y = self.fire_speed * (self.flared_pos.y - self.pos.y) / distance
            self.locate_target((self.flared_pos.x, self.flared_pos.y))
        elif self.spray is True:
            distance = pygame.math.Vector2(player_base.rect.center).distance_to(self.pos)
            self.velocity_vector.x = self.fire_speed * (self.pos.x - player_base.rect.centerx) / distance
            self.velocity_vector.y = self.fire_speed * (self.pos.y - player_base.rect.centery) / distance
            self.locate_target((player_base.rect.centerx, player_base.rect.centery))
        else:
            pos = pygame.math.Vector2(pygame.mouse.get_pos())
            distance = pygame.math.Vector2(self.rect.center).distance_to(pos)
            self.velocity_vector.x = self.fire_speed * (pygame.mouse.get_pos()[0] - self.rect.x) / distance
            self.velocity_vector.y = self.fire_speed * (pygame.mouse.get_pos()[1] - self.rect.y) / distance
            
    def force_push(self):
        if pygame.sprite.spritecollide(self, player_bullet_group, False):
            for b in pygame.sprite.spritecollide(self, player_bullet_group, False):
                if b.mask.overlap(self.mask, (self.rect.x - b.rect.x, self.rect.y - b.rect.y)):
                    b.kill()
                    self.hits -= 1
                    if self.hits == 0:
                        self.kill()
                        
    def set_flare(self):
        self.flare_x = random.randint(self.rect.right, self.rect.right + 100)
        self.flare_y = random.randint(self.rect.top, self.rect.bottom)
        self.flared_pos = pygame.math.Vector2(self.flare_x, self.flare_y)
   
    def flare_out(self):
        move_speed = self.fire_speed / 2 * game['Delta Time'] * level['Speed']
        self.pos.move_towards_ip(self.flared_pos, 10)
        self.rect.center = self.pos
        
    def form_cluster(self, group):
        for i in range(2):
            b = Bullet(laser_cluster_image, self.rect.center, self.damage, self.fire_speed / 5)
            b.cluster = True
            b.set_velocity()
            group.add(b)
            
            
class Bomb(Bullet):
    
    def __init__(self, image, pos, damage, speed):
        super().__init__(image, pos, damage, speed)
        self.mask_surf = self.mask.to_surface(setcolor='red', unsetcolor=(0, 0, 0, 0)).convert_alpha()
        self.last_flash_time = time()
        self.flash_delay = 1
        self.can_cluster = True
        
    def update(self):
        if self.is_hostile is True:
           # self.set_velocity(player_base)
            self.pos.x -= self.fire_speed * game['Delta Time'] * level['Speed']
            self.pos.y += self.velocity_vector.y * game['Delta Time'] * level['Speed']
            self.rect.center = self.pos
        if 0 < time() - self.last_flash_time < 0.1:
            self.flash()
        if time() - self.last_flash_time >= self.flash_delay:
            self.last_flash_time = time()
            self.flash_delay -= 0.05
        if self.flash_delay <= 0.1:
            animations_group.add(Animation(ship_explosion, 2.5, self.pos, ship_explosion_sound))
            self.kill()
        # Bomb hit by player bullet
        if pygame.sprite.spritecollide(self, player_bullet_group, False):
            if pygame.sprite.spritecollide(self, player_bullet_group, True, pygame.sprite.collide_mask):
                if self.can_cluster is True:
                    self.break_and_cluster()
                else:
                    animations_group.add(Animation(ship_explosion, 2.5, self.pos, ship_explosion_sound))
                    self.kill()               
                
        # Bomb hits player base
        if pygame.sprite.spritecollide(self, base_group, False):
            if pygame.sprite.spritecollide(self, base_group, False, pygame.sprite.collide_mask):
                animations_group.add(Animation(ship_explosion, 2.5, self.pos, ship_explosion_sound))
                self.kill()
                
    def break_and_cluster(self):
        points = self.mask.outline(every=10)
        print(points)
        animations_group.add(Animation(ship_explosion, 2.5, self.pos, ship_explosion_sound))
        self.kill()
        cluster_image = pygame.transform.scale_by(self.image, 0.5)
        image_size = cluster_image.get_size()
        max_x_point = 0
        max_y_point = 0
        x_offset = 0
        y_offset = 0
        for point in points:
            if point[0] > max_x_point:
                x_offset = point[0]
                max_x_point += point[0]
            else:
                x_offset = -point[0]
            if point[1] > max_y_point:
                y_offset = point[1]
                max_y_point += point[1]
            else:
                y_offset = -point[1]
                
            cluster_bomb = Bomb(cluster_image, (self.pos.x + (x_offset * 2), self.pos.y + (y_offset * 2)), self.damage * 0.75, self.fire_speed * 2)
            cluster_bomb.is_hostile = True
            cluster_bomb.can_cluster = False
            cluster_bomb.velocity_vector.y = random.choice([-20, 10, 20, -10])
            bomb_group.add(cluster_bomb)
            
    def flash(self):
        offset = 1
        screen.blit(self.mask_surf, (self.rect.x+offset, self.rect.y))
        screen.blit(self.mask_surf, (self.rect.x-offset, self.rect.y))
        screen.blit(self.mask_surf, (self.rect.x, self.rect.y+offset))
        screen.blit(self.mask_surf, (self.rect.x, self.rect.y+offset))
        screen.blit(self.mask_surf, (self.rect.x+offset, self.rect.y-offset))
        screen.blit(self.mask_surf, (self.rect.x+offset, self.rect.y+offset))
        screen.blit(self.mask_surf, (self.rect.x-offset, self.rect.y-offset))
        screen.blit(self.mask_surf, (self.rect.x-offset, self.rect.y+offset))
        screen.blit(self.image, self.rect)
            
            
class Meteor(pygame.sprite.Sprite):
    
    def __init__(self, image, pos, damage, speed):
        super().__init__()
        self.image = pygame.transform.rotate(image, random.randint(10, 250))
        self.rotated_image = image
        self.pos = pygame.math.Vector2(pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)
        self.damage = 1000
        self.fire_speed = speed
        self.angle = 0
        self.rotate_direction = random.choice([-1, 1])
        
    def update(self):
        self.pos.y += self.fire_speed * game['Delta Time'] * level['Speed']
        self.rect = self.image.get_rect(center = pygame.math.Vector2(self.pos))
        if pygame.sprite.spritecollide(self, enemy_group, False):
            for ship in pygame.sprite.spritecollide(self, enemy_group, False, pygame.sprite.collide_mask):
                ship.take_damage(self.damage)
                self.kill()
        if self.rect.y > screen_height:
            self.kill()
            
    def break_and_cluster(self, group):
        animations_group.add(Animation(ship_explosion, 2.5, self.pos, ship_explosion_sound))
        #self.kill()
        cluster_image = pygame.transform.scale_by(self.image, 0.5)
        for point in pygame.mask.from_surface(self.image).outline():
            cluster_bomb = Meteor(self.image, point, self.damage * 0.75, self.fire_speed)
            group.add(cluster_bomb)
        self.kill()
            

class Laser(pygame.sprite.Sprite):
               
    def __init__(self, image, pos, damage):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.damage = damage
        self.image = image
        self.rect = self.image.get_rect(center=self.pos)
        
    def update(self, base_group):
        self.pos.x -= 300 * game['Delta Time'] * level['Speed']
        self.rect.center = self.pos
        self.check_collision_with_base(base_group)
        if self.rect.right < player_base.rect.right - 50:
            self.kill()
        
    def check_collision_with_base(self, group):
        if pygame.sprite.spritecollide(self, group, False):
            if pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_mask):
                player_base.take_damage(self.damage)                    
                                                            
                    
class Missile(pygame.sprite.Sprite):
                    
    def __init__(self, image, pos, damage, fire_speed):
        super().__init__()
        self.image = image
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.damage = damage
        self.threshold = pygame.math.Vector2(self.pos)
        self.passed_threshold = False
        self.velocity_vector = pygame.math.Vector2(0, 0)
        self.target = pygame.math.Vector2(0, 0)
        self.travel_speed = fire_speed 
        
    def update(self):
        # if missile goes past the given threshold, the missile will increase speed and seek its target
        if self.passed_threshold is False:
            if self.threshold.x > self.pos.x:
                self.pos.x += self.travel_speed * game['Delta Time'] * level['Speed']
                if self.pos.x > self.threshold.x:
                    self.travel_speed *= 2
                    self.passed_threshold = True                   
            elif self.threshold.x < self.pos.x:
                self.pos.x -= self.travel_speed / 2 * game['Delta Time'] * level['Speed']
                if self.pos.x < self.threshold.x:
                    self.travel_speed *= 2
                    self.passed_threshold = True
                
        if self.passed_threshold is True:
            if self.threshold.x > self.pos.x:
                self.pos.x -= self.travel_speed * game['Delta Time'] * level['Speed']
            elif self.threshold.x < self.pos.x:
                self.pos.x += self.travel_speed * game['Delta Time'] * level['Speed']
        self.rect.center = self.pos
        self.collide_with_base()
        self.hit_by_player()
        
    def collide_with_base(self):
        if pygame.sprite.spritecollide(self, base_group, False):
            if pygame.sprite.spritecollide(self, base_group, False, pygame.sprite.collide_mask):
                player_base.take_damage(self.damage)
                animations_group.add(Animation(ship_explosion, 2, self.rect.center))
                self.kill()
                if game['Sounds'] is True:
                    ship_explosion_sound.play()
                
    def hit_by_player(self):
        if pygame.sprite.spritecollide(self, player_bullet_group, False):
            if pygame.sprite.spritecollide(self, player_bullet_group, True, pygame.sprite.collide_mask):
                animations_group.add(Animation(ship_explosion, 2, self.rect.center))
                self.kill()
                if game['Sounds'] is True:
                    ship_explosion_sound.play()

        
class HealingRing(pygame.sprite.Sprite):
                             
    def __init__(self, image, pos):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.rotated_image = image
        self.image_scale_factor = 0
        self.scaled_image = healer_ring_no_effect_image
        self.image = image
        self.rect = self.image.get_rect(center=self.pos)
        self.angle = 0
        self.movex = 10
        self.owner_ship = None
        self.scale_up = True
        self.healing_flare_velocity = pygame.math.Vector2((0, 0))
        self.health_flare_speed = 7      
        self.last_health_flare_time = time()
        self.flare_cooldown = 1
               
    def rotate_in_place(self):
        self.image = pygame.transform.rotate(self.rotated_image, self.angle)
        self.rect = self.image.get_rect(center=self.owner_ship.pos)
        if self.angle >= 0:
            self.angle = -360
        else:
            self.angle += 1
        if time() - self.last_health_flare_time >= self.flare_cooldown:
            self.set_health_flare()
            self.last_health_flare_time = time()
            
    def set_health_flare(self):
        flare_x = random.randint(self.rect.left, self.rect.right)
        flare_y = random.randint(self.rect.top, self.rect.bottom)
        flare_pos = pygame.math.Vector2(flare_x, flare_y)
        health_flare = Flare(health_recovery_icon_image, self.pos, flare_pos)
        health_flares_group.add(health_flare)  
            
    def activate_recovery_ring(self):
        #image will scale up to full size     
        if self.scale_up is True:
            if self.image_scale_factor < 1:
                self.image_scale_factor += 0.01
                self.image = pygame.transform.scale_by(self.scaled_image, self.image_scale_factor)
        self.rect = self.image.get_rect(center=self.owner_ship.pos)       
        if self.image_scale_factor >= 1:
            self.scale_up = False
        elif self.image_scale_factor <= 0:
            self.scale_up = True
            
    def update(self):
        if self.scale_up is False:
            self.rotate_in_place()
        elif self.scale_up is True:
            self.activate_recovery_ring()
        if self.owner_ship.alive() is False:
            self.kill()     
            
            
class Comet(pygame.sprite.Sprite):
            
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.damage = 20000
        
    def update(self):
        self.pos.x += 400 * game['Delta Time'] * level['Speed']
        self.pos.y += 400 * game['Delta Time'] * level['Speed']
        self.rect.center = self.pos
        self.collided_with_enemy()
        
    def collided_with_enemy(self):
        if pygame.sprite.spritecollide(self, enemy_group, False):
            for ship in pygame.sprite.spritecollide(self, enemy_group, False, pygame.sprite.collide_mask):
                ship.take_damage(self.damage)
                self.kill()                                 
            
                                              
class BlackHole(pygame.sprite.Sprite):
    
    def __init__(self, image, pos):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.rotated_image = image
        self.image = image
        self.rect = self.image.get_rect(center=self.pos)
        self.angle = 0
        self.speed = 50
        self.radius = 0.5
        
    def update(self):
        self.image = pygame.transform.rotate(self.rotated_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)
        if self.angle <= -360:
            self.angle = 0
        else:
            self.angle -= 1
            
    def suck_in_ship(self, ship):
        ship.pos.move_towards_ip(self.pos, 5)
        ship_size = ship.image.get_size()
        #if ship_size[0] > 10:
            #ship.image = pygame.transform.smoothscale(ship.image, (ship_size[0] - 1, ship_size[1] - 1))
        #distance = pygame.math.Vector2(self.pos).distance_to(ship.pos)
#        x_velocity = self.speed * (ship.pos.x - self.pos.x) / distance
#        y_velocity = self.speed * (ship.pos.y - self.pos.y) / distance
#        ship.pos.x -= x_velocity
#        ship.pos.y -= y_velocity
    

class Flare(pygame.sprite.Sprite):
    
    def __init__(self, image, pos, end_pos):
        super().__init__()
        self.image = image
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.flare_pos = pygame.math.Vector2(end_pos)
        self.start_time = time()
        self.duration = 2
        self.speed = 100
        self.velocity = self.set_velocity()
        self.recovery_amount = 250
        self.mini = False
        
    def update(self):
        if time() - self.start_time >= self.duration:
            self.kill()
        else:
            self.pos.x += self.velocity.x * game['Delta Time'] * level['Speed']
            self.pos.y += self.velocity.y * game['Delta Time'] * level['Speed']
                              
        self.rect = self.image.get_rect(center=self.pos)    
        screen.blit(self.image, self.rect)
            
    def set_velocity(self):
        distance = pygame.math.Vector2(self.pos).distance_to(self.flare_pos)
        x_velocity = self.speed * (self.flare_pos.x - self.pos.x) / distance
        y_velocity = self.speed * (self.flare_pos.y - self.pos.y) / distance
        return pygame.math.Vector2((x_velocity, y_velocity))
          
                            
                                
class ChargeBolt(pygame.sprite.Sprite):
           
    def __init__(self, image, pos, damage):
        super().__init__()
        self.create_time = time()
        self.image = image
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.damage = damage
        self.flip_time = 0.1
        self.last_flip_time = time()
        self.duration = 3
        self.speed = -500
        
    def update(self):
        if not pygame.sprite.spritecollideany(self, base_group, pygame.sprite.collide_mask):
            self.pos.x += self.speed * game['Delta Time'] * level['Speed']
        if time() - self.create_time < self.duration:
            if time() - self.last_flip_time >= self.flip_time:
                self.image = pygame.transform.flip(self.image, False, True)
                self.last_flip_time = time()
        else:
            self.kill()
        self.rect = self.image.get_rect(center=self.pos)
         
            
class VaporizingArc(pygame.sprite.Sprite):
            
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.pos = pygame.math.Vector2(pos)           
    

enemy_types = {'Cruiser': {'Health': 500,        #1
                           'Damage': 50,
                           'Shot Cooldown': 3,
                           'Range': 75,
                           'Speed': 80,
                           'Special': None},
                       
               'Thumper': {'Health': 750,        #2
                           'Damage': 100,
                           'Shot Cooldown': 2.5,
                           'Range': 180,
                           'Speed': 50,
                           'Special': None},
                       
                'Tanker': {'Health': 2500,       #3
                           'Damage': 500,
                           'Shot Cooldown': 5,
                           'Range': 300,
                           'Speed': 50,
                           'Special': None},
                      
               'Pounder': {'Health': 3050,       #4
                           'Damage': 600,
                           'Shot Cooldown': 4,
                           'Range': 350,
                           'Speed': 55,
                           'Special': None},
                       
           'Duo Fighter': {'Health': 3500,       #5
                           'Damage': 150,
                           'Shot Cooldown': 2,
                           'Range': 420,
                           'Speed': 75,
                           'Special': 'Double Shot'},
                           
           'Tri Fighter': {'Health': 3750,       #6
                           'Damage': 150,
                           'Shot Cooldown': 1.5,
                           'Range': 500,
                           'Speed': 75,
                           'Special': 'Triple Shot'},
                           
         'Speed Fighter': {'Health': 4000,       #7
                           'Damage': 150,
                           'Shot Cooldown': 0.5,
                           'Range': 560,
                           'Speed': 110,
                           'Special': None},
                             
          'Hash Fighter': {'Health': 5000,       #8
                           'Damage': 250,
                           'Shot Cooldown': 2,
                           'Range': 0,
                           'Speed': 70,
                           'Special': 'Kamikaze'},
                            
            'Venomplyer': {'Health': 5500,       #9
                           'Damage': 250,
                           'Shot Cooldown': 2,
                           'Range': 600,
                           'Speed': 45,
                           'Special': 'Poison Laser',
                           'Shield': True},
                          
          'Stingumplyer': {'Health': 5800,       #10
                           'Damage': 1000,
                           'Shot Cooldown': 5,
                           'Range': 500,
                           'Speed': 70,
                           'Special': 'Charge Bolt',
                           'Shield': True},
                            
          'Destrumplyer': {'Health': 7000,       #11
                           'Damage': 600,
                           'Shot Cooldown': 5,
                           'Range': 640,
                           'Speed': 25,
                           'Special': 'Hydra Spawn',
                           'Shield': True},
                            
                'Healer': {'Health': 10000,      #12
                           'Damage': 0,
                           'Shot Cooldown': 300,
                           'Range': 500,
                           'Speed': 55,
                           'Special': 'Radial Healing',
                           'Shield': True},
                          
              'Aidouker': {'Health': 14000,      #13
                           'Damage': 300,
                           'Shot Cooldown': 3,
                           'Range': 600,
                           'Speed': 75,
                           'Special': 'Health Regeneration',
                           'Shield': True},
                        
               'Denuker': {'Health': 20000, # one Shot to destroy player's Shield if activated
                           'Damage': 800,
                           'Shot Cooldown': 5,
                           'Range': 500,
                           'Speed': 20,
                           'Special': 'Shield Destroy',
                           'Shield': True},
                       
               'Flanker': {'Health': 18000,
                           'Damage': 400,
                           'Shot Cooldown': 5,
                           'Range': 410,
                           'Speed': 75,
                           'Special': 'Reinforcements',
                           'Shield': True},
                       
              'Debunker': {'Health': 50000,
                           'Damage': 100,
                           'Shot Cooldown': 0.25,
                           'Range': 450,
                           'Speed': 40,
                           'Special': 'Double Shot',
                           'Shield': True},
                        
           'Zipper': {'Health': 55000, # very fast mover
                      'Damage': 200,
                      'Shot Cooldown': 1,
                      'Range': 300,
                      'Speed': 140,
                      'Special': 'Double Shot',
                      'Shield': True},
                      
           'Trickster': {'Health': 60000,     #18
                         'Damage': 200,
                         'Shot Cooldown': 1.5,
                         'Range': 475,
                         'Speed': 70,
                         'Special': 'Bomb Drop',  # drops bomb after being killed
                         'Shield': True},
                         
           'Hopper': {'Health': 72000, # teleports 5 times to avoid being hit
                      'Damage': 220,
                      'Shot Cooldown': 2,
                      'Range': 250,
                      'Speed': 50,
                      'Special': 'Teleport',
                      'Shield': True},
                      
           'Wish Biller': {'Health': 80000,
                           'Damage': 300,
                           'Shot Cooldown': 3,
                           'Range': 700,
                           'Speed': 50,
                           'Special': 'Wave Blast',
                           'Shield': True},
                           
           'Courier': {'Health': 100000,
                       'Damage': 1000,
                       'Shot Cooldown': 3,
                       'Range': 200,
                       'Speed': 100,
                       'Special': 'Linger Flares',
                       'Shield': True},
                                                            
           'Diamond Killer': {'Health': 120000,
                              'Damage': 1200,
                              'Shot Cooldown': 2,
                              'Range': 415,
                              'Speed': 50,
                              'Special': 'Speed Shot',
                              'Shield': True},
           'Magician': {'Health': 200000,
                         'Damage': 2000,
                         'Shot Cooldown': 4,
                         'Range': 420,
                         'Speed': 70,
                         'Special': 'Shrinkage',
                         'Shield': True},
           'Acid Tanker': {'Health': 300000,
                             'Damage': 5000,
                             'Shot Cooldown': 10,
                             'Range': 310,
                             'Speed': 50,
                             'Special': 'Acid Shot',
                             'Shield': True},  
           'Tanker Bus': {'Health': 500000,
                          'Damage': 500,
                          'Shot Cooldown': 5,
                          'Range': 700,
                          'Speed': 50,
                          'Special': 'Tanker Delivery',
                          'Shield': True},
                          
           'Uni-Bomber': {'Health': 250000,
                          'Damage': 2500,
                          'Shot Cooldown': 7,
                          'Range': 430,
                          'Speed': 55,
                          'Special': 'Bomb Shot',
                          'Shield': True},
                          
           'Meteor Launcher': {'Health': 650000,
                               'Damage': 5000,
                               'Shot Cooldown': 15,
                               'Range': 400,
                               'Speed': 50,
                               'Special': 'Meteor Shot',
                               'Shield': True},
                               
           'Blubber Bomber': {'Health': 800000,
                              'Damage': 750,
                              'Shot Cooldown': 5,
                              'Range': 440,
                              'Speed': 50,
                              'Special': 'Cluster Bomb',
                              'Shield': True},
                              
           'Smart Destroyer': {'Health': 1000000,
                               'Damage': 1500,
                               'Shot Cooldown': 5,
                               'Range': 380,
                               'Speed': 80,
                               'Special': 'Turret Paralyzer',
                               'Shield': True},
                               
           'Ultimate Killer': {'Health': 50000000,
                               'Damage': 50000,
                               'Shot Cooldown': 10,
                               'Range': 700,
                               'Speed': 30,
                               'Special': 'Teleport',
                               'Shield': True}
}

enemy_boss_types = {'Soaring Fighter': {'Health': 20000,
                                        'Damage': 500,
                                        'Shot Cooldown': 3.5,
                                        'Range': 400,
                                        'Speed': 80,
                                        'Special': 'Double Shot',
                                        'Defense': 'Flares'},
                                        
                        'Priyatamous': {'Health': 50000,
                                        'Damage': 2000,
                                        'Shot Cooldown': 10,
                                        'Range': 550,
                                        'Speed': 50,
                                        'Special': 'Spawn Turrets',
                                        'Shield': True},
                                        
                        'Doomdefier': {'Health': 75000,
                                        'Damage': 500,
                                        'Shot Cooldown': 2,
                                        'Range': 700,
                                        'Speed': 50,
                                        'Special': 'Drones', # 1/10 damage amd health
                                        'Defense': 'TBA'},
                                        
                        'Versawing': {'Health': 100000,
                                        'Damage': 6000,
                                        'Shot Cooldown': 2.5,
                                        'Range': 650,
                                        'Speed': 50,
                                        'Special': 'Side Missiles', # 1/10 Damage and health
                                        'Defense': 'TBA'},
                                        
                        'Timodifier': {'Health': 125000,
                                        'Damage': 2500,
                                        'Shot Cooldown': 4,
                                        'Range': 500,
                                        'Speed': 60,
                                        'Special': 'Slow Down Bullets',
                                        'Defense': 'TBA'},
                                        
                        'Whoppur': {'Health': 150000,
                                        'Damage': 2500,
                                        'Shot Cooldown': 2.5,
                                        'Range': 400,
                                        'Speed': 50,
                                        'Special': 'TBA',
                                        'Defense': 'Shield'},
                                        
                        'Godship': {'Health': 200000,
                                        'Damage': 500,
                                        'Shot Cooldown': 2.5,
                                        'Range': 700,
                                        'Speed': 50,
                                        'Special': 'Gold Laser',
                                        'Defense': 'Laser Immunity'}, # can only be destroyed with special attacks
                                        
                        'Vulcanizer': {'Health': 300000,
                                        'Damage': 5000,
                                        'Shot Cooldown': 2.5,
                                        'Range': 400,
                                        'Speed': 50,
                                        'Special': 'Triple Charge Beam', # 3 Orbs charge up, meet in front middle and shoots out a massive charge
                                        'Defense': 'TBA'},
                                        
                        'Stingeray': {'Health': 500000,
                                        'Damage': 20000,
                                        'Shot Cooldown': 2.5,
                                        'Range': 400,
                                        'Speed': 50,
                                        'Special': 'TBA',
                                        'Defense': 'TBA'},
                                        
                        'Galactic Destroyer': {'Health': 1000000000,
                                        'Damage': 500000,
                                        'Shot Cooldown': 25,
                                        'Range': 400,
                                        'Speed': 50,
                                        'Special': 'TBA',
                                        'Defense': 'TBA'}
}

enemy_names = np.array([t for t in enemy_types.keys()])
# Data dicts for level variables 

try:
    with open('saved_games.txt', 'r') as f:   
        saved_games = json.loads(f.readline())
        loaded_games = load_saved_games(saved_games)
except FileNotFoundError:
    saved_games = dict()
    loaded_games = np.array([])
   
level = {'Playing': True,
         'Paused': False,
         'Abandoned': False,
         'Speed': 1,
         'Exiting': False,
         'Game Over': False,
         'Restart Game': False,
         'Screen': None,
         'On Menu': True,
         'Settings': False,
         'Battle': False,
         'Start Battle Time': time(),
         'Game Select': False,
         'Overworld': False,
         'Spawn Time': time(),
         'Show Options': False,
         'Upgrading': False,
         'Upgrade Submenu': False,
         'Upgrade Item': None,
         'Extra Turret Upgrades': False,
         'Submenu': None,
         'Submenu Stats': None,
         'Fade': False,
         'Continue': False,
         'Button Clicked': False}
         
game = {'Previous Time': time(),
        'Delta Time': time(),
        'Game Over Time': time(),
        'Current Level': 0,
        'Current Track': starting_music,
        'Screen Transition': False,
        'Music': True,
        'Sounds': True,
        'Load Game': False}
        

# Player Stats
player_stats = {'Space Crystals': 0,
                'Power Gems': 0,
                'XP': 0}
                
# Stats Menus

# Player's base stats
base_health_stats = {'Health': 5000,
                     'Max Health': 5000,
                     'Regen Cooldown (secs)': 5,
                     'Regen Amount': 20,
                     'Health Regeneration': 'Inactive'}
base_starting_stats = base_health_stats.copy()
base_health_stats_increase_amounts = [500, 1.2, 0.1, 1.1, 'Active']
base_health_stats_limits = np.array([999999999, 999999999, 0.5, 1000, None])
                 
# Player's base Shield stats   
shield_stats = {'Status': 'Inactive',
                'Max Health': 5000,
                'Regen Cooldown (secs)': 5,
                'Regen Amount': 20,              
                'Health Regeneration': 'Inactive'}
shield_starting_stats = shield_stats.copy()
shield_stats_increase_amounts = ['Active', 1.2, 0.1, 1.1, 'Active']
shield_stats_limits = np.array([None, 999999999, 0.5, 1000, 'Active'])
       
# Player's main turret stats
main_turret_stats = {'Damage': 100,
                     'Critical Hit': 1.5,
                     'Critical Hit Chance %': 5,
                     'Special Cooldown': 30,
                     'Extra Turrets': 0}
main_turret_starting_stats = main_turret_stats.copy()
main_turret_stats_increase_amounts = [1.1, 0.1, 1.2, 0.5, 1]
main_turret_stats_limits = np.array([999999999, 10, 50, 5, 4])
                     
# Helper turret stats                
extra_turret_stats = {'Damage': 100,
                      'Range %': 50,
                      'Cooldown (secs)': 5,
                      'Critical Hit': 1.5,
                      'Critical Hit Chance %': 5}           
extra_turret_stats_increase_amounts = [1.15, 1.1, 0.1, 2, 1]
extra_turret_stats_limits = np.array([999999, 100, 0.5, 10, 25])

# Stats for special attacks
special_attacks_stats = {'Rapid Fire': 0,
                         'Vaporizers': 0,
                         'Raining Comets': 0,
                         'Meteor Shower': 0,
                         'Cluster Shots': 0}
special_attacks_starting_stats = special_attacks_stats.copy()
special_attacks_stats_increase_amounts = [1, 1, 1, 1, 1]
special_attacks_stats_limits = np.array([1000, 1000, 1000, 1000, 1000])              
 
# Stats for special defenses                
special_defenses_stats = {'Shock Absorbers': 0,  # seconds duration
                          'Poison Antidote': 0,  # num of tiny clusters
                          'Flares': 0,  # seconds duration
                          'Deflection': 0,  # seconds duration
                          'Black Hole': 0}  # seconds duration 
special_defenses_starting_stats = special_defenses_stats.copy()            
special_defenses_stats_increase_amounts = [1, 1, 1, 1, 1]
special_defenses_stats_limits = np.array([5, 1000, 5, 5, 5]) 
     
# Upgrade Menus
base_health_upgrades = {'Repair': 1000,
                        'Max Health +': 2000,
                        'Regen Cooldown -': 10000,
                        'Regen Amount +': 15000,
                        'Health Regeneration': 50000}                
base_health_upgrades_increase_amounts = [1.05, 1.08, 1.09, 1.12, 1.0]    
                                    
shield_upgrades_options = {'Activate Shield': 20000,
                   'Shield Health +': 20000,
                   'Regen Cooldown -': 10000,
                   'Regen Amount +': 20000,
                   'Health Regeneration': 50000}              
shield_upgrade_increase_amounts = [1.2, 1.15, 1.1, 1.2, 1]
                         
main_turret_upgrades = {'Damage +': 1000,
                        'Critical Hit +': 2500,
                        'Critical Hit Chance': 3000,
                        'Special Cooldown': 5000,
                        'Add Turret': 500}                        
main_turret_upgrade_increase_amounts = [1.25, 1.5, 1.3, 1.15, 2]
                        
extra_turret_upgrades = {'Damage +': 1000,
                         'Range +': 1250,
                         'Cooldown -': 1500,
                         'Critical Hit +': 5000,
                         'Critical Hit Chance': 10000}                                                             
extra_turret_upgrades_increase_amounts = [1.2, 1.5, 1.1, 1.2, 1.25]
                         
special_attacks = {'Rapid Fire': 1000,
                   'Cluster Shot': 2000,                  
                   'Meteor Shower': 3000,
                   'Raining Comets': 5000,
                   'Vaporizer': 10000}
special_attacks_increase_amounts = [1, 1, 1, 1, 1]             
                               
special_defenses = {'Shock Absorber': 1000,
                    'Poison Antidote': 2000,
                    'Flares': 5000,
                    'Deflection': 10000,
                    'Black Hole': 20000}
special_defenses_increase_amounts = [1, 1, 1, 1, 1]

# Enemy Turret Stats
enemy_turret_stats = {'Health': 3000,
                      'Damage': 100,
                      'Range': 1000,
                      'Cooldown': 0.5,
                      'Critical Hit': 1,
                      'Critical Hit Chance': 0.001}

menu_offset = upgrade_table.get_width() + 10

# Player Objects
player_base = Base(base_main, (40, screen_height * 0.42), base_health_stats.copy())

helper_turret_locations = [(player_base.rect.centerx+20, player_base.rect.top+75),
                           (player_base.rect.centerx+163, player_base.rect.centery-98),
                           (player_base.rect.centerx+163, player_base.rect.centery+98),
                           (player_base.rect.centerx+20, player_base.rect.bottom-75)]
helper_turret_group = []

animations_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

# Player main objects
base_shield = Shield(shield_main, player_base.rect.center, shield_stats.copy())
base_turret = Turret(turret_main, (player_base.rect.centerx+5, player_base.rect.centery-5), main_turret_stats.copy()) 
extra_turret1 = Turret(turret_extra, helper_turret_locations[0], extra_turret_stats.copy())
extra_turret2 = Turret(turret_extra, helper_turret_locations[1], extra_turret_stats.copy())
extra_turret3 = Turret(turret_extra, helper_turret_locations[2], extra_turret_stats.copy())
extra_turret4 = Turret(turret_extra, helper_turret_locations[3], extra_turret_stats.copy())
extra_turrets = np.array([extra_turret1, extra_turret2, extra_turret3, extra_turret4])

# Stats Tables
stats_table_pos = (screen_width - menu_offset, 15)
base_stats_table = StatsTable('Health Stats', player_base.stats, base_health_stats_increase_amounts, base_health_stats_limits, stats_table_pos)
shield_stats_table = StatsTable('Shield Stats', base_shield.stats, shield_stats_increase_amounts, shield_stats_limits, stats_table_pos)
main_turret_stats_table = StatsTable('Main Turret', base_turret.stats, main_turret_stats_increase_amounts, main_turret_stats_limits, stats_table_pos)
extra_turret1_stats_table = StatsTable('Turret X1', extra_turret1.stats, extra_turret_stats_increase_amounts, extra_turret_stats_limits, stats_table_pos)
extra_turret2_stats_table = StatsTable('Turret X2', extra_turret2.stats, extra_turret_stats_increase_amounts, extra_turret_stats_limits, stats_table_pos)
extra_turret3_stats_table = StatsTable('Turret X3', extra_turret3.stats, extra_turret_stats_increase_amounts, extra_turret_stats_limits, stats_table_pos)
extra_turret4_stats_table = StatsTable('Turret X4', extra_turret4.stats, extra_turret_stats_increase_amounts, extra_turret_stats_limits, stats_table_pos)
special_attacks_stats_table = StatsTable('Supply', special_attacks_stats.copy(), special_attacks_stats_increase_amounts, special_attacks_stats_limits, stats_table_pos)
special_defenses_stats_table = StatsTable('Supply', special_defenses_stats.copy(), special_defenses_stats_increase_amounts, special_defenses_stats_limits, stats_table_pos)

# Upgrade Menu Tables
upgrade_menu_pos = (base_stats_table.rect.left - menu_offset, base_stats_table.rect.top)
base_upgrades = UpgradeMenu('Base Health', base_health_upgrades.copy(), base_health_upgrades_increase_amounts, upgrade_menu_pos)
base_turret_upgrades = UpgradeMenu('Main Turret', main_turret_upgrades.copy(), main_turret_upgrade_increase_amounts, upgrade_menu_pos)
extra_turret1_upgrades = UpgradeMenu('X1 Upgrades', extra_turret_upgrades.copy(), extra_turret_upgrades_increase_amounts, upgrade_menu_pos)
extra_turret2_upgrades = UpgradeMenu('X2 Upgrades', extra_turret_upgrades.copy(), extra_turret_upgrades_increase_amounts, upgrade_menu_pos)
extra_turret3_upgrades = UpgradeMenu('X3 Upgrades',  extra_turret_upgrades.copy(),  extra_turret_upgrades_increase_amounts,  upgrade_menu_pos)
extra_turret4_upgrades = UpgradeMenu('X4 Upgrades', extra_turret_upgrades.copy(), extra_turret_upgrades_increase_amounts, upgrade_menu_pos)
shield_upgrades = UpgradeMenu('Shield', shield_upgrades_options.copy(), shield_upgrade_increase_amounts, upgrade_menu_pos)
special_attacks_upgrades = UpgradeMenu('Attacks', special_attacks.copy(), special_attacks_increase_amounts, upgrade_menu_pos)
special_defenses_upgrades = UpgradeMenu('Defenses', special_defenses.copy(), special_defenses_increase_amounts, upgrade_menu_pos)
     
base_group = pygame.sprite.Group(player_base)
player_bullet_group = pygame.sprite.Group()
player_defenses_group = pygame.sprite.Group()
raining_comets_group = pygame.sprite.Group()

# Sprite groups for enemy attacks
enemy_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
bomb_group = pygame.sprite.Group()
laser_beam_group = pygame.sprite.Group()
flares_group = pygame.sprite.Group()
enemy_missile_group = pygame.sprite.Group()
healing_ring_group = pygame.sprite.Group()
charge_bolts_group = pygame.sprite.Group()
health_flares_group = pygame.sprite.Group()

# Game name title
game_title = NavButton(game_title_label_image, (screen_width / 2, screen_height * 0.35))

# Settings Title
settings_menu_title = Title(settings_menu_title_image, (screen_width / 2, settings_menu_title_image.get_height()))

# Level Overworld Header
levels_overworld_title = NavButton(levels_menu_title, (screen_width / 2, base_upgrades.rect.top + 50))

# Menu Buttons
menu_button_spacing = load_game_button_image.get_width() + 20
load_game_button = NavButton(load_game_button_image, (screen_width / 2, screen_height * 0.6))
play_button = NavButton(new_game_button_image, (load_game_button.rect.centerx - menu_button_spacing, screen_height * 0.6))
exit_button = NavButton(exit_game_button_image, (load_game_button.rect.centerx + menu_button_spacing, load_game_button.rect.centery))
settings_button = NavButton(settings_button_image, (50, screen_height - settings_button_image.get_height()))
settings_button.rect.bottomleft = (10, screen_height - 10)

# Feedback messages
not_enough_money_message = Feedback('Insufficient Funds', big_font, (screen_width / 2, screen_height / 2))
base_fully_repaired_message = Feedback('Base Completely Repaired', big_font, (screen_width / 2, screen_height / 2))
shield_not_active_message = Feedback('Shield Not Active', big_font, (screen_width / 2, screen_height / 2))
shield_already_active_message = Feedback('Shield Already Active', big_font,  (screen_width / 2, screen_height / 2))
regeneration_already_active_message = Feedback('Regeneration Already Active', big_font, (screen_width / 2, screen_height / 2))
turret_not_purchased_message = Feedback('Turret Not Yet Purchased', big_font, (screen_width / 2, screen_height / 2))
no_turrets_purchased_message = Feedback('No Turrets Purchased Yet', big_font, (screen_width / 2, screen_height * 0.33))
extra_turret_limit_reached_message = Feedback('Extra Turret Limit Reached', big_font,  (screen_width / 2, screen_height / 2))
stat_limit_reached_message = Feedback('Upgrade Limit Reached', big_font, (screen_width / 2, screen_height / 2))
not_unlocked_yet_message = Feedback('Not Unlocked Yet', big_font, (screen_width / 2, screen_height / 2))
must_reach_shield_level_message = Feedback('Must Complete Level 25', big_font, (screen_width / 2, screen_height * 0.33))
must_reach_extra_turret_upgrades_level_message = Feedback('Must Complete Level 35', big_font,  (screen_width / 2, screen_height * 0.33))
no_saved_games_message = Feedback('No saved Games', big_font, (load_game_button.rect.centerx, load_game_button.rect.bottom + 50))
must_complete_previous_level_message = Feedback('Must Complete Previous Level', big_font, (screen_width / 2, screen_height / 2))

# Level Mini Menus
level_completed_menu = MiniMenu(level_over_menu, (screen_width / 2, screen_height + level_over_menu.get_height() / 2), 'Level Completed')
level_defeated_menu = MiniMenu(level_over_menu, (screen_width / 2, screen_height + level_over_menu.get_height() / 2), 'Level Failed')

# Paused Level menu
paused_level_menu = MiniMenu(level_over_menu, (screen_width / 2, screen_height / 2), 'Game Paused')

# Paused Level menu buttons
unpause_game_button = NavButton(resume_game_button_image, (paused_level_menu.rect.centerx, paused_level_menu.rect.centery - 50))
abandon_game_button = NavButton(exit_game_button_image, (paused_level_menu.rect.centerx, paused_level_menu.rect.centery + 50))

player_money_enlarged_label = Feedback('Space Crystals', upgrades_font, (base_upgrades.rect.x / 2, screen_height * 0.33))
player_money_enlarged = Feedback(f'{int(player_stats["Space Crystals"])}', upgrades_font, (player_money_enlarged_label.rect.centerx, player_money_enlarged_label.rect.centery + 50))

player_power_crystals_label = Feedback('Power Gems', upgrades_font, (base_upgrades.rect.x / 2, screen_height * 0.66))
player_power_crystals_enlarged = Feedback(f'{player_stats["Power Gems"]}', upgrades_font, (player_power_crystals_label.rect.centerx, player_power_crystals_label.rect.centery + 50))

level_feedback = Feedback(f'Level: {game["Current Level"]}', ui_font, (0, 0))
player_money = Feedback(f'{player_stats["Space Crystals"]}', ui_font, (92, screen_height * 0.89))
player_money.rect.bottomleft = pygame.math.Vector2(10, screen_height - 5)
level_feedback.rect.topleft = pygame.math.Vector2(5, 5)
player_score = Feedback(f'Score: {player_stats["XP"]}', ui_font, (screen_width * 0.5, 10))
player_score.rect.topright = pygame.math.Vector2(screen_width - 5, 5)

screen_shader = Shader()

upgrades_menu_title = Feedback('Upgrades', title_font, (screen_width / 2, base_upgrades.rect.top + 50))

insufficient_funds_notification = Feedback('Not Enough Money', big_font, (screen_width/2, screen_height / 2))

turret_upgrades_button = NavButton(turrets_upgrades_button_image, (screen_width / 2, screen_height / 2))
base_turret_upgrades_button = NavButton(main_turret_upgrades_button_image, turret_upgrades_button.rect.center)
extra_turret_upgrades_button = NavButton(extra_turrets_upgrades_button_image, turret_upgrades_button.rect.center)

#test loc for centering buttons--> (full length - (num of buttons * button width)) / num of spaces = equal button spacing
extra_turret_button_spacing = base_upgrades.rect.left - (level_overworld_button.get_width() * 4) / 5
turret_x1_button = Button(level_overworld_button, (base_upgrades.rect.left * 0.2, screen_height - level_overworld_button.get_height()), 'X1', ui_font)
turret_x2_button = Button(level_overworld_button, (turret_x1_button.rect.centerx + level_overworld_button.get_width() + 20, screen_height - level_overworld_button.get_height()), 'X2', ui_font)
turret_x3_button = Button(level_overworld_button, (turret_x2_button.rect.centerx + level_overworld_button.get_width() + 20, screen_height - level_overworld_button.get_height()), 'X3', ui_font)
turret_x4_button = Button(level_overworld_button, (turret_x3_button.rect.centerx + level_overworld_button.get_width() + 20, screen_height - level_overworld_button.get_height()), 'X4', ui_font)

base_upgrades_button = NavButton(base_upgrades_button_image, (turret_upgrades_button.rect.centerx - turret_upgrades_button.rect.width - 20, screen_height / 2))
base_health_upgrades_button = NavButton(base_health_upgrades_button_image, base_upgrades_button.rect.center)
shield_upgrades_button = NavButton(shield_upgrades_button_image, base_upgrades_button.rect.center)

extra_upgrades_button = NavButton(extra_upgrades_button_image, (turret_upgrades_button.rect.centerx + turret_upgrades_button.rect.width + 20, screen_height / 2))
special_attacks_button = NavButton(special_attacks_upgrades_button_image, extra_upgrades_button.rect.center)
special_defenses_button = NavButton(special_defenses_upgrades_button_image, extra_upgrades_button.rect.center)

# Navigation Buttons for going betweeen different screens
continue_level_button = Button(level_nav_button, (level_completed_menu.rect.centerx, level_completed_menu.rect.bottom - level_nav_button.get_height() - 5), 'Continue', ui_font)
level_options_button = NavButton(level_options_button_image, (level_options_button_image.get_width() / 2 + 5, screen_height - level_options_button_image.get_height() / 2 - 5))
pause_level_button = NavButton(pause_level_button_image, (screen_width - (pause_level_button_image.get_width() / 2) - 5, pause_level_button_image.get_height() / 2 + 5))
game_speed_button = NavButton(game_speed_button_image, (screen_width - (game_speed_button_image.get_width() / 2) - 5, game_speed_button_image.get_height() / 2 + 5))
quit_level_button = Button(level_nav_button, (screen_width - (level_nav_button.get_width() / 2) - 5, level_nav_button.get_height() / 2 + 5), 'Back', ui_font)

goto_upgrades_button = NavButton(goto_upgrades_button_image, (screen_width / 2, screen_height - level_nav_button.get_height() / 2 - 10))
goto_menu_button = NavButton(goto_menu_button_image, (goto_menu_button_image.get_width() / 2 + 10, goto_menu_button_image.get_height() / 2 + 10))
goto_levels_button = NavButton(goto_levels_button_image, goto_menu_button.rect.center)

save_and_quit_button = Button(level_nav_button, (continue_level_button.rect.centerx - level_nav_button.get_width() - 10, continue_level_button.rect.centery), 'Quit', ui_font)
close_button = NavButton(close_button_image, (close_button_image.get_width() / 2 + 10, close_button_image.get_height() / 2 + 10))

replay_button = Button(level_nav_button, (level_defeated_menu.rect.centerx + level_nav_button.get_width() / 2 + 5, level_defeated_menu.rect.bottom - level_nav_button.get_height() - 5), 'Replay', ui_font)
quit_button = Button(level_nav_button, (replay_button.rect.centerx - level_nav_button.get_width() - 10, replay_button.rect.centery), 'Quit', ui_font)

continue_button = NavButton(continue_button_image, (screen_width - continue_button_image.get_width(), 5))
continue_button.rect.bottomright = (screen_width - 5, screen_height - 5)

go_back_button = NavButton(previous_button_image, (50, base_upgrades.rect.top + 50))
go_back_button.rect.bottomleft = ([5, screen_height - 5])

# Settings button objects
toggle_music_button = NavButton(music_toggle_button_image, (screen_width * 0.33, screen_height * 0.5))
toggle_sounds_button = NavButton(sounds_toggle_button_image, (screen_width * 0.66, screen_height * 0.5))
toggle_music_label = Title(music_text, (toggle_music_button.rect.centerx, toggle_music_button.rect.top - music_text.get_height()))
toggle_sounds_label = Title(sounds_text, (toggle_sounds_button.rect.centerx, toggle_music_label.rect.centery))
toggle_music_status_label = Title(toggle_on_text, (toggle_music_button.rect.centerx, toggle_music_button.rect.bottom + sounds_text.get_height()))
toggle_sounds_status_label = Title(toggle_on_text, (toggle_sounds_button.rect.centerx, toggle_music_status_label.rect.centery))

# Container for special attacks and defenses
player_stats_container = StatsContainer(specials_container, (screen_width / 2, screen_height - (specials_container.get_height() / 2)))
special_defenses_container = StatsContainer(specials_container, (screen_width - specials_container.get_width() / 2 - 20, screen_height - (specials_container.get_height() / 2)))
special_attacks_container = StatsContainer(specials_container, (special_defenses_container.rect.centerx - special_defenses_container.rect.width - 100, screen_height - (specials_container.get_height() / 2)))

# Special Attacks Label
special_attacks_container_label = Title(special_attacks_label_abbreviated, (special_attacks_container.rect.left - special_attacks_label_abbreviated.get_width() / 2, special_attacks_container.rect.centery))

# Special Attacks Buttons
rapid_fire_button = NavButton(rapid_fire_button_image, (special_attacks_container.rect.left + (rapid_fire_button_image.get_width() / 2 + 25), special_attacks_container.rect.centery))
meteor_shower_button = NavButton(meteor_shower_button_image, (rapid_fire_button.rect.centerx + rapid_fire_button.rect.width + 5, rapid_fire_button.rect.centery))
cluster_shot_button = NavButton(cluster_shot_button_image, (meteor_shower_button.rect.centerx + meteor_shower_button.rect.width + 5, meteor_shower_button.rect.centery))
vaporize_button = NavButton(vaporize_button_image, (cluster_shot_button.rect.centerx + cluster_shot_button.rect.width + 5, cluster_shot_button.rect.centery))
raining_comets_button = NavButton(raining_comets_button_image, (vaporize_button.rect.centerx + vaporize_button.rect.width + 5, vaporize_button.rect.centery))
spawn_orb_group = pygame.sprite.Group()

# Special Defenses Label
special_defenses_container_label = Title(special_defenses_label_abbreviated, (special_defenses_container.rect.left - special_defenses_label_abbreviated.get_width() / 2, special_defenses_container.rect.centery))

# Special Defenses Button
shock_absorber_button = NavButton(shock_absorber_button_image, (special_defenses_container.rect.left + (shock_absorber_button_image.get_width() / 2 + 25), special_defenses_container.rect.centery))
poison_antidote_button = NavButton(poison_antidote_button_image, (shock_absorber_button.rect.centerx + shock_absorber_button.rect.width + 5, shock_absorber_button.rect.centery))
#flares_button = NavButton()
#deflection_button = NavButton()
#black_hole_button = NavButton()

# Base and Shield Health bars
base_and_shield_stats_container = StatsContainer(base_health_container, (base_health_container.get_width() / 2 + 5, screen_height - (base_health_container.get_height() / 2)))

enemy_collisions = pygame.sprite.groupcollide(player_bullet_group, enemy_group, True, False, pygame.sprite.collide_mask)

#Test Enemy
#tester_enemy = Enemy(enemy_ships[9], (2500, screen_height / 2), enemy_types['Stingumplyer'])
#enemy_group.add(tester_enemy)

# Test Boss
#tester_boss = Enemy(enemy_boss_im)ages[3], (2500, screen_height / 2), enemy_boss_types['Versawing'])
#enemy_group.add(tester_boss)

# Test paralyze Shot
#test_p_shot = ParalysisShot((300, 200), (800, 200), 100)

# dictionary for dynamic game difficulty
player_progression_stats = {}

levels = []
level_x_offset = 0
button_spacing = (screen_width / 17.5) + (level_buttons[0].get_width() / 2)
button_y_spacing = screen_height * 0.2361
level_x_coord = screen_width * 0.1589 - (level_buttons[0].get_width() / 2)
level_y_coord = screen_height * 0.27

# Variables for assigning number of enemies in each level
num_of_types = 1
num_of_enemies = 30
delay = 4
ntypes = 2
boss_num = 0
probabilities = [6, 1, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 
                 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0]
                         
          
#for i in range(100):
for i in range(30):
   
   l = Level(level_buttons[i], i  + 1, ntypes, enemy_types, (level_x_coord + level_x_offset, level_y_coord), num_of_enemies)
   if i == 0:
       l.locked = False
   l.spawn_delay = delay 
   #l.locked = False
   if (i + 1) % 10 == 0:
       if boss_num < len(enemy_boss_types.keys()):
           l.boss = boss_num
           boss_num += 1
   levels.append(l)
   num_of_enemies += 1
   if len(levels) % 3 == 0:
       ntypes += 1 if ntypes < len(enemy_types) else 0
   if len(levels) % 6 == 0:
       level_x_coord = screen_width * 0.1589 - (level_buttons[0].get_width() / 2)
       level_y_coord += 170
   else:
       level_x_coord += button_spacing + l.rect.width / 2
   if len(levels) % 18 == 0:
       level_x_offset = (screen_width * len(levels) // 18)
       level_y_coord = screen_height * 0.27
   
levels_locked_status = dict()
for i in range(len(levels)):
    levels_locked_status[f'{levels[i].num}'] = levels[i].locked
status_keys = [k for k in levels_locked_status.keys()]
level_statuses = levels_locked_status.copy()

def save_game():
    save_date = datetime.datetime.now()
    save_time = ctime()
    
    currency_stats = json.dumps(player_stats)
    
    player_base_stats = json.dumps(player_base.stats)
    player_shield_stats = json.dumps(base_shield.stats)
    player_turret_stats = json.dumps(base_turret.stats, cls=NumpyEncoder)   
    extra_turret1_stats = json.dumps(extra_turret1.stats)
    extra_turret2_stats = json.dumps(extra_turret2.stats)
    extra_turret3_stats = json.dumps(extra_turret3.stats)
    extra_turret4_stats = json.dumps(extra_turret4.stats)
    
    base_upgrade_stats = json.dumps(base_upgrades.dict)
    shield_upgrades_stats = json.dumps(shield_upgrades.dict)
    base_turret_upgrades_stats = json.dumps(base_turret_upgrades.dict)
    extra_turret1_upgrades_stats = json.dumps(extra_turret1_upgrades.dict)
    extra_turret2_upgrades_stats = json.dumps(extra_turret2_upgrades.dict)
    extra_turret3_upgrades_stats = json.dumps(extra_turret3_upgrades.dict)
    extra_turret4_upgrades_stats = json.dumps(extra_turret4_upgrades.dict)
    
    base_stats_table_stats = json.dumps(base_stats_table.dict)
    shield_stats_table_stats = json.dumps(shield_stats_table.dict)
    main_turret_stats_table_stats = json.dumps(main_turret_stats_table.dict, cls=NumpyEncoder)
    extra_turret1_stats_table_stats = json.dumps(extra_turret1_stats_table.dict)
    extra_turret2_stats_table_stats = json.dumps(extra_turret2_stats_table.dict)
    extra_turret3_stats_table_stats = json.dumps(extra_turret3_stats_table.dict)
    extra_turret4_stats_table_stats = json.dumps(extra_turret4_stats_table.dict)
    
    levels_statuses = json.dumps(levels_locked_status)
    
    special_attacks_upgrades_stats = json.dumps(special_attacks_upgrades.dict)
    special_attack_stats = json.dumps(special_attacks_stats_table.dict)
    
    special_defenses_upgrades_stats = json.dumps(special_defenses_upgrades.dict)
    special_defense_stats = json.dumps(special_defenses_stats_table.dict)
    
    if player_base.loaded_saved_game is True:
        saved_file = player_base.loaded_game
    else:
        saved_file = f'Game {len(saved_games) + 1}.txt'
        player_base.loaded_game = saved_file
        player_base.loaded_saved_game = True
        with open('saved_games.txt', 'w+') as sf:
            saved_games[f'Game {len(saved_games) + 1}'] = save_date.strftime('%m/%d/%y')
            sf.write(json.dumps(saved_games))
    
    with open(saved_file, 'w') as f:
        f.write(save_time)
        f.write('\n\n\n')
        f.write(currency_stats)
        f.write('\n')
        f.write(player_base_stats)
        f.write('\n')
        f.write(player_shield_stats)
        f.write('\n')
        f.write(player_turret_stats)
        f.write('\n')
        f.write(extra_turret1_stats)
        f.write('\n')
        f.write(extra_turret2_stats)
        f.write('\n')
        f.write(extra_turret3_stats)
        f.write('\n')
        f.write(extra_turret4_stats)
        f.write('\n')
        f.write(base_upgrade_stats)
        f.write('\n')
        f.write(shield_upgrades_stats)
        f.write('\n')
        f.write(base_turret_upgrades_stats)
        f.write('\n')
        f.write(extra_turret1_upgrades_stats)
        f.write('\n')
        f.write(extra_turret2_upgrades_stats)
        f.write('\n')
        f.write(extra_turret3_upgrades_stats)
        f.write('\n')
        f.write(extra_turret4_upgrades_stats)
        f.write('\n')
        f.write(base_stats_table_stats)
        f.write('\n')
        f.write(shield_stats_table_stats)
        f.write('\n')
        f.write(main_turret_stats_table_stats)
        f.write('\n')
        f.write(extra_turret1_stats_table_stats)
        f.write('\n')
        f.write(extra_turret2_stats_table_stats)
        f.write('\n')
        f.write(extra_turret3_stats_table_stats)
        f.write('\n')
        f.write(extra_turret4_stats_table_stats)
        f.write('\n')
        f.write(levels_statuses)
        f.write('\n')
        f.write(special_attacks_upgrades_stats)
        f.write('\n')
        f.write(special_attack_stats)
        f.write('\n')
        f.write(special_defenses_upgrades_stats)
        f.write('\n')
        f.write(special_defense_stats)
        
     
def load_saved_game(file):

    with open(file, 'r') as f:
        lines = f.readlines()
        
        # Load in Player currency
        player_stats.update(json.loads(lines[3]))
        
        # Load in all stats of the Player's objects
        player_base.stats.update(json.loads(lines[4]))
        base_shield.stats.update(json.loads(lines[5]))
        base_turret.stats.update(json.loads(lines[6]))  
        extra_turret1.stats.update(json.loads(lines[7]))
        extra_turret2.stats.update(json.loads(lines[8]))
        extra_turret3.stats.update(json.loads(lines[9]))
        extra_turret4.stats.update(json.loads(lines[10]))
        
        # Load in and update the Upgrades costs
        base_upgrades.dict.update(json.loads(lines[11]))
        shield_upgrades.dict.update(json.loads(lines[12]))
        base_turret_upgrades.dict.update(json.loads(lines[13]))
        extra_turret1_upgrades.dict.update(json.loads(lines[14]))
        extra_turret2_upgrades.dict.update(json.loads(lines[15]))
        extra_turret3_upgrades.dict.update(json.loads(lines[16]))
        extra_turret4_upgrades.dict.update(json.loads(lines[17]))
        special_attacks_upgrades.dict.update(json.loads(lines[26]))
        special_defenses_upgrades.dict.update(json.loads(lines[28]))
        
        # Load in and update the player's objects' stats
        base_stats_table.dict.update(json.loads(lines[18]))
        shield_stats_table.dict.update(json.loads(lines[19]))
        main_turret_stats_table.dict.update(json.loads(lines[20]))
        extra_turret1_stats_table.dict.update(json.loads(lines[21]))
        extra_turret2_stats_table.dict.update(json.loads(lines[22]))
        extra_turret3_stats_table.dict.update(json.loads(lines[23]))
        extra_turret4_stats_table.dict.update(json.loads(lines[24]))
        special_attacks_stats_table.dict.update(json.loads(lines[27]))
        special_defenses_stats_table.dict.update(json.loads(lines[29]))
        
        levels_locked_status.update(json.loads(lines[25]))
        #levels = json.loads(lines[25])
        keys = [k for k in levels_locked_status.keys()]
        for i in range(len(levels)):
            levels[i].locked = levels_locked_status[keys[i]]          
        
        # Refresh Player currency
        player_money.update_var(f'{player_stats["Space Crystals"]}')
        player_money_enlarged.update_var(f'{player_stats["Space Crystals"]}')
        player_power_crystals_enlarged.update_var(f'{player_stats["Power Gems"]}')
        #player_score.update_var(f'Score: {player_stats["XP"]}')
        
        # Refresh the upgrades text surfaces 
        base_upgrades.reset_upgrades()
        shield_upgrades.reset_upgrades()
        base_turret_upgrades.reset_upgrades()
        extra_turret1_upgrades.reset_upgrades()
        extra_turret2_upgrades.reset_upgrades()
        extra_turret3_upgrades.reset_upgrades()
        extra_turret4_upgrades.reset_upgrades()          
        special_attacks_upgrades.reset_upgrades()
        special_defenses_upgrades.reset_upgrades()
        
        # Refresh the stats text surfaces 
        base_stats_table.reset_stats()
        main_turret_stats_table.reset_stats()
        shield_stats_table.reset_stats()
        extra_turret1_stats_table.reset_stats()
        extra_turret2_stats_table.reset_stats()
        extra_turret3_stats_table.reset_stats()
        extra_turret4_stats_table.reset_stats()
        special_attacks_stats_table.reset_stats()
        special_defenses_stats_table.reset_stats()
        
        if shield_stats_table.dict['Status'] == 'Active':
            base_group.add(base_shield)
        else:
            if base_shield in base_group:
                base_shield.kill()
        
        if base_turret.stats['Extra Turrets'] > 0:
            for i in range(base_turret.stats['Extra Turrets']):
                helper_turret_group.append(extra_turrets[i])
        else:
            helper_turret_group.clear()
        


def load_new_game():
                
    # Reset Player objects' stats and upgrades
    player_base.stats.update(base_health_stats)
    base_shield.stats.update(shield_stats)
    base_turret.stats.update(main_turret_stats)
    extra_turret1.stats.update(extra_turret_stats)
    extra_turret2.stats.update(extra_turret_stats)
    extra_turret3.stats.update(extra_turret_stats)
    extra_turret4.stats.update(extra_turret_stats)               
                
    # Reset upgrade tables
    base_upgrades.dict.update(base_health_upgrades)  
    base_upgrades.reset_upgrades()
    base_turret_upgrades.dict.update(main_turret_upgrades)
    base_turret_upgrades.reset_upgrades()
    shield_upgrades.dict.update(shield_upgrades_options)
    shield_upgrades.reset_upgrades()
    extra_turret1_upgrades.dict.update(extra_turret_upgrades)
    extra_turret1_upgrades.reset_upgrades()
    extra_turret2_upgrades.dict.update(extra_turret_upgrades)
    extra_turret2_upgrades.reset_upgrades()
    extra_turret3_upgrades.dict.update(extra_turret_upgrades)
    extra_turret3_upgrades.reset_upgrades()
    extra_turret4_upgrades.dict.update(extra_turret_upgrades)
    extra_turret4_upgrades.reset_upgrades()
    special_attacks_upgrades.dict.update(special_attacks)
    special_attacks_upgrades.reset_upgrades()
    special_defenses_upgrades.dict.update(special_defenses)
    special_defenses_upgrades.reset_upgrades()
                
    # Reset stats tables
    base_stats_table.dict.update(player_base.stats)
    base_stats_table.reset_stats()
                
    shield_stats_table.dict.update(shield_stats)
    shield_stats_table.reset_stats()
                
    main_turret_stats_table.dict.update(main_turret_stats)
    main_turret_stats_table.reset_stats()
               
    extra_turret1_stats_table.dict.update(extra_turret_stats)
    extra_turret1_stats_table.reset_stats()
                
    extra_turret2_stats_table.dict.update(extra_turret_stats)
    extra_turret2_stats_table.reset_stats()
                
    extra_turret3_stats_table.dict.update(extra_turret_stats)
    extra_turret3_stats_table.reset_stats()
                
    extra_turret4_stats_table.dict.update(extra_turret_stats)
    extra_turret4_stats_table.reset_stats()
                
    special_attacks_stats_table.dict.update(special_attacks_stats)
    special_attacks_stats_table.reset_stats()
    
    special_defenses_stats_table.dict.update(special_defenses_stats)
    special_defenses_stats_table.reset_stats()
    
    keys = [k for k in level_statuses.keys()]
    for i in range(len(levels)):
        levels[i].locked = level_statuses[keys[i]]
    
    player_stats['Space Crystals'] = 5000
    player_stats['Power Gems'] = 500
    player_money_enlarged.update_var(f'{player_stats["Space Crystals"]}')
    player_power_crystals_enlarged.update_var(f'{player_stats["Power Gems"]}')
    base_shield.stats['Status'] = 'Inactive'
    helper_turret_group.clear()
    player_bullet_group.empty()
    enemy_bullet_group.empty()
    enemy_group.empty()
    level['Game Over'] = False
    level['Restart Game'] = False
    
    try:
        with open('saved_games.txt', 'r') as sf:
            lines = sf.readlines()
            saved_games.update(json.loads(lines[0]))
        with open('saved_games.txt', 'w') as f:
            f.write(json.dumps(saved_games))
    except FileNotFoundError:
        pass
            

def apply_upgrades():
    player_base.stats = base_stats_table.dict
    base_shield.stats = base_shield.stats
    base_turret.stats = base_turret.stats
    extra_turret1.stats = extra_turret1.stats
    extra_turret2.stats = extra_turret2.stats
    extra_turret3.stats = extra_turret3.stats
    extra_turret4.stats = extra_turret4.stats


def load_game_selection_menu():
    for event in pygame.event.get():
        
        # Player Navigating back to the main menu
        if goto_menu_button.clicked(event):
            if game['Sounds'] is True:
                button_clicked_sound.play()
            level['Game Select'] = False
            level['On Menu'] = True
            level['Fade'] = True
        
        # Player selecting which saved game they want to load   
        for g in loaded_games:
            if loaded_games[g].clicked(event):
                if game['Sounds'] is True:
                    button_clicked_sound.play()
                player_base.loaded_game = loaded_games[g].label.text + '.txt'
                player_base.loaded_saved_game = True
                load_saved_game(player_base.loaded_game)               
                level['Fade'] = True
                level['Overworld'] = True
                level['Game Select'] = False
                
        if len(loaded_games) > 9:
            if loaded_games[list(loaded_games)[-1]].rect.x > screen_width:
                if continue_button.clicked(event):
                    for g in loaded_games:
                        loaded_games[g].scroll_amount = -screen_width
                    
                        
            if loaded_games[list(loaded_games)[0]].rect.x < 0:
                if go_back_button.clicked(event):
                    for g in loaded_games:
                        loaded_games[g].scroll_amount = screen_width    
     
    screen.blit(bg, (0, 0))
    
    for games in loaded_games:
        loaded_games[games].show()
        
    goto_menu_button.show()
    
    if len(list(loaded_games)) > 9:
        if loaded_games[list(loaded_games)[-1]].rect.x > screen_width:
            continue_button.show()
            
        if loaded_games[list(loaded_games)[0]].rect.x < 0:
            go_back_button.show()
     
    
def settings_menu():
    
    for event in pygame.event.get():
        if goto_menu_button.clicked(event):
            level['Fade'] = True
            level['Settings'] = False
            level['On Menu'] = True
            
        if toggle_music_button.clicked(event):
            if game['Music'] is True:
                game['Music'] = False
                if game['Sounds'] is True:
                    button_clicked_sound.play()
            elif game['Music'] is False:
                game['Music'] = True
                
        if toggle_sounds_button.clicked(event):
            if game['Sounds'] is True:
                game['Sounds'] = False
                button_clicked_sound.play()
            elif game['Sounds'] is False:
                game['Sounds'] = True
    
    screen.blit(bg, (0, 0))
    toggle_music_button.show()
    toggle_sounds_button.show()
    toggle_music_label.show()
    toggle_music_status_label.show()
    toggle_sounds_label.show()
    toggle_sounds_status_label.show()
    goto_menu_button.show()
    settings_menu_title.show()


def menu():
    global saved_games
    global loaded_games
    # Menu screen
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            level['Playing'] = False
            pygame.quit()
            
        if play_button.clicked(event):
            if game['Sounds'] is True:
                button_clicked_sound.play()
            level['Fade'] = True
            level['On Menu'] = False 
            level['Overworld'] = True
            player_base.loaded_saved_game = False
            player_base.loaded_game = f'Game {len(saved_games) + 1}.txt'
            load_new_game()
            save_game()
        elif load_game_button.clicked(event):            
            if len(saved_games) > 0:
                try:
                    with open('saved_games.txt', 'r') as f:   
                        saved_games = json.loads(f.readline())
                        loaded_games = load_saved_games(saved_games)
                except FileNotFoundError:
                    saved_games = dict()
                    loaded_games = np.array([])
                if game['Sounds'] is True:
                    button_clicked_sound.play()
                level['Fade'] = True
                level['On Menu'] = False
                level['Game Select'] = True             
            else:
                if game['Sounds'] is True:
                    insufficient_funds_sound.play()
                no_saved_games_message.notify_player()
        elif settings_button.clicked(event):
            if game['Sounds'] is True:
                button_clicked_sound.play()
            level['Fade'] = True
            level['On Menu'] = False
            level['Settings'] = True
        elif exit_button.clicked(event):
            if game['Sounds'] is True:
                button_clicked_sound.play()
            level['Playing'] = False
                
            
    screen.blit(bg, (0, 0))   
    game_title.show()
    play_button.show()
    load_game_button.show()
    exit_button.show()
    settings_button.snap_to_bottomleft()
    settings_button.show()
    no_saved_games_message.show_notification()
    
    
    
def level_overworld():
    
    for event in pygame.event.get():
        
        if goto_upgrades_button.clicked(event):
            if game['Sounds'] is True:
                button_clicked_sound.play()
            level['Upgrading'] = True
            level['Fade'] = True
            level['Overworld'] = False
            
        if goto_menu_button.clicked(event):
            if game['Sounds'] is True:
                button_clicked_sound.play()
            level['Fade'] = True
            level['Overworld'] = False
            level['On Menu'] = True
        
        for lvl in levels:
            if lvl.active_button.clicked(event):
                if lvl.locked is False:
                    if game['Sounds'] is True:
                        button_clicked_sound.play()
                    game['Current Level'] = lvl
                    level_feedback.update_var(f'Level: {game["Current Level"].num}')
                    level['Fade'] = True
                    level['Overworld'] = False
                    level['Battle'] = True
                    game['Screen Transition'] = True
                    game['Current Track'] = gameplay_music2
                elif lvl.locked is True:
                    if game['Sounds'] is True:
                        insufficient_funds_sound.play()
                    must_complete_previous_level_message.notify_player()
            if lvl.scroll_amount == 0:
                
                if continue_button.clicked(event):
                    if levels[-1].active_button.rect.x > screen_width:
                        if game['Sounds'] is True:
                            button_clicked_sound.play()
                        lvl.scroll_amount = screen_width
                
                if go_back_button.clicked(event):                 
                    if levels[0].active_button.rect.x < 0:
                        if game['Sounds'] is True:
                            button_clicked_sound.play()
                        lvl.scroll_amount = -screen_width       
    
    screen.blit(bg, (0, 0))
    
    for lvl in levels:
        lvl.active_button.show()
        lvl.update()
        
    must_complete_previous_level_message.show_notification()
        
    if levels[-1].active_button.rect.x > screen_width:
        continue_button.show()
    if levels[0].active_button.rect.x < 0:
        go_back_button.show()
        
    levels_overworld_title.show()
    goto_upgrades_button.show()
    goto_menu_button.show()
    

def upgrade_submenu():
    
    for event in pygame.event.get():
        if close_button.clicked(event):
            if game['Sounds'] is True:
                button_clicked_sound.play()
            apply_upgrades()
            save_game()
            level['Fade'] = True
            level['Upgrade Submenu'] = False
            level['Upgrading'] = True
            
        if level['Submenu'] == extra_turret1_upgrades or level['Submenu'] == extra_turret2_upgrades or \
        level['Submenu'] == extra_turret3_upgrades or level['Submenu'] == extra_turret4_upgrades:
            # Switching between each individual turret upgrade and stat menus
            if turret_x1_button.clicked(event):
                if extra_turret1 not in helper_turret_group:
                    if game['Sounds'] is True:
                        insufficient_funds_sound.play()
                else:
                    if game['Sounds'] is True:
                        button_clicked_sound.play()
                    level['Submenu'] = extra_turret1_upgrades
                    level['Submenu Stats'] = extra_turret1_stats_table
            if turret_x2_button.clicked(event):
                if extra_turret2 not in helper_turret_group:
                    if game['Sounds'] is True:
                        insufficient_funds_sound.play()
                    turret_not_purchased_message.notify_player()
                else:
                    if game['Sounds'] is True:
                        button_clicked_sound.play()
                    level['Submenu'] = extra_turret2_upgrades
                    level['Submenu Stats'] = extra_turret2_stats_table
            if turret_x3_button.clicked(event):
                if extra_turret3 not in helper_turret_group:
                    if game['Sounds'] is True:
                        insufficient_funds_sound.play()
                    turret_not_purchased_message.notify_player()
                else:
                    if game['Sounds'] is True:
                        button_clicked_sound.play()
                    level['Submenu'] = extra_turret3_upgrades
                    level['Submenu Stats'] = extra_turret3_stats_table
            if turret_x4_button.clicked(event):
                if extra_turret4 not in helper_turret_group:
                    if game['Sounds'] is True:
                        insufficient_funds_sound.play()
                    turret_not_purchased_message.notify_player()
                else:
                    if game['Sounds'] is True:
                        button_clicked_sound.play()
                    level['Submenu'] = extra_turret4_upgrades
                    level['Submenu Stats'] = extra_turret4_stats_table
            
        for button in level['Submenu'].buttons:
            if button.clicked(event):
                b = np.where(level['Submenu'].buttons == button)[0][0]                              
                
                # Checking if Player has enough money for the desired upgrade
                if player_stats['Space Crystals'] >= level['Submenu'].get_cost(button):
                    
                    # Handling base health upgrades 
                    if level['Submenu'] == base_upgrades:
                        if base_upgrades.button_labels[b].text == 'Repair':
                            # Player can't purchase upgrade if health is full
                            if int(player_base.stats['Health']) == int(player_base.stats['Max Health']):
                                if game['Sounds'] is True:
                                    insufficient_funds_sound.play()
                                base_fully_repaired_message.notify_player()
                            elif player_base.stats['Health'] < player_base.stats['Max Health']:
                                # Player can repair base health if it is less than the max health
                                if game['Sounds'] is True:
                                    button_clicked_sound.play()
                                player_stats['Space Crystals'] -= int(level['Submenu'].get_cost(button))
                                player_money.update_var(f'{int(player_stats["Space Crystals"])}')
                                player_money_enlarged.update_var(f'{int(player_stats["Space Crystals"])}')
                                level['Submenu'].update_cost(button)
                                level['Submenu Stats'].update_stat(b)
                                
                        # Increasing base health with Max health if they are equal in value
                        elif base_upgrades.button_labels[b].text == 'Max Health +':            
                                if level['Submenu Stats'].dict[level['Submenu Stats'].dict_keys[b]] == level['Submenu Stats'].stat_limits[b]:
                                    if game['Sounds'] is True:
                                        insufficient_funds_sound.play()
                                    stat_limit_reached_message.notify_player()
                                elif level['Submenu Stats'].dict[level['Submenu Stats'].dict_keys[b]] != level['Submenu Stats'].stat_limits[b]:
                                    if int(base_stats_table.dict['Health']) == int(base_stats_table.dict['Max Health']):
                                        if game['Sounds'] is True:
                                            button_clicked_sound.play()
                                        player_stats['Space Crystals'] -= int(level['Submenu'].get_cost(button))
                                        player_money.update_var(f'{int(player_stats["Space Crystals"])}')
                                        player_money_enlarged.update_var(f'{int(player_stats["Space Crystals"])}')
                                        level['Submenu'].update_cost(button)
                                        level['Submenu Stats'].update_stat(b)
                                        base_stats_table.dict['Health'] = base_stats_table.dict['Max Health']
                                        base_stats_table.stats[0].update_var(f'{int(base_stats_table.dict["Max Health"])}')
                                    else:
                                        if game['Sounds'] is True:
                                            button_clicked_sound.play()
                                        player_stats['Space Crystals'] -= int(level['Submenu'].get_cost(button))
                                        player_money.update_var(f'{int(player_stats["Space Crystals"])}')
                                        player_money_enlarged.update_var(f'{int(player_stats["Space Crystals"])}')
                                        level['Submenu'].update_cost(button)
                                        level['Submenu Stats'].update_stat(b)
                                        #update health to match Max health
                                
                        elif level['Submenu'].button_labels[b].text == 'Health Regeneration':
                            # Player can't purchase health Regeneration more than once
                            if player_base.stats['Health Regeneration'] == 'Active':
                                if game['Sounds'] is True:
                                    insufficient_funds_sound.play()
                                regeneration_already_active_message.notify_player()
                                #one time upgrade message notify
                            else:
                                # Activating base health Regeneration
                                if game['Sounds'] is True:
                                    button_clicked_sound.play()
                                player_stats['Space Crystals'] -= int(level['Submenu'].get_cost(button))
                                player_money.update_var(f'{int(player_stats["Space Crystals"])}')
                                player_money_enlarged.update_var(f'{int(player_stats["Space Crystals"])}')
                                level['Submenu'].update_cost(button)
                                level['Submenu Stats'].update_stat(b)
                        else:
                            if level['Submenu Stats'].dict[level['Submenu Stats'].dict_keys[b]] == level['Submenu Stats'].stat_limits[b]:
                                if game['Sounds'] is True:
                                    insufficient_funds_sound.play()
                                stat_limit_reached_message.notify_player()
                            elif level['Submenu Stats'].dict[level['Submenu Stats'].dict_keys[b]] != level['Submenu Stats'].stat_limits[b]:
                                if game['Sounds'] is True:
                                    button_clicked_sound.play()
                                player_stats['Space Crystals'] -= int(level['Submenu'].get_cost(button))
                                player_money.update_var(f'{int(player_stats["Space Crystals"])}')
                                player_money_enlarged.update_var(f'{int(player_stats["Space Crystals"])}')
                                level['Submenu'].update_cost(button)
                                level['Submenu Stats'].update_stat(b)
                    
                    # Handling Shield upgrades
                    elif level['Submenu'] == shield_upgrades:
                        # Purchasing Shield activation only if it is inactive
                        if level['Submenu'].button_labels[b].text == 'Activate Shield':
                            
                            if shield_stats_table.dict['Status'] == 'Active':
                                # Shield is already active
                                if game['Sounds'] is True:
                                    insufficient_funds_sound.play()
                                shield_already_active_message.notify_player()                      
                            else:
                                level['Submenu Stats'].dict[level['Submenu Stats'].dict_keys[b]] != level['Submenu Stats'].stat_limits[b]
                                if game['Sounds'] is True:
                                    button_clicked_sound.play()
                                player_stats['Space Crystals'] -= int(level['Submenu'].get_cost(button))
                                player_money.update_var(f'{int(player_stats["Space Crystals"])}')
                                player_money_enlarged.update_var(f'{int(player_stats["Space Crystals"])}')
                                level['Submenu'].update_cost(button)
                                level['Submenu Stats'].update_stat(b)
                                base_shield.health = shield_stats_table.dict['Max Health']
                                base_group.add(base_shield)
                                
                        # Player can only make upgrades to the Shield if it is active
                        elif shield_stats_table.dict['Status'] == 'Active':       
                            # Activating Shield Health Regeneration only if it is inactive
                            # One time purchase   
                            if level['Submenu'].button_labels[b].text == 'Health Regeneration':
                                
                                if shield_stats_table.dict['Health Regeneration'] == 'Active':
                                    # Shield regeneration already active
                                    if game['Sounds'] is True:
                                        insufficient_funds_sound.play()
                                    regeneration_already_active_message.notify_player()                     
                                else:
                                    if game['Sounds'] is True:
                                        button_clicked_sound.play()
                                    player_stats['Space Crystals'] -= int(level['Submenu'].get_cost(button))
                                    player_money.update_var(f'{int(player_stats["Space Crystals"])}')
                                    player_money_enlarged.update_var(f'{int(player_stats["Space Crystals"])}')
                                    level['Submenu'].update_cost(button)
                                    level['Submenu Stats'].update_stat(b)
                                    
                            elif level['Submenu'].button_labels[b].text == 'Shield Health +':
                                if level['Submenu Stats'].dict[level['Submenu Stats'].dict_keys[b]] == level['Submenu Stats'].stat_limits[b]:
                                    if game['Sounds'] is True:
                                        insufficient_funds_sound.play()
                                    stat_limit_reached_message.notify_player()
                                else:
                                    if int(base_shield.health) == int(shield_stats_table.dict['Max Health']):
                                        if game['Sounds'] is True:
                                            button_clicked_sound.play()
                                        player_stats['Space Crystals'] -= int(level['Submenu'].get_cost(button))
                                        player_money.update_var(f'{int(player_stats["Space Crystals"])}')
                                        player_money_enlarged.update_var(f'{int(player_stats["Space Crystals"])}')
                                        level['Submenu'].update_cost(button)
                                        level['Submenu Stats'].update_stat(b)
                                        base_shield.health = shield_stats_table.dict['Max Health']
                                        base_group.add(base_shield)
                                    else:
                                        if game['Sounds'] is True:
                                            button_clicked_sound.play()
                                        player_stats['Space Crystals'] -= int(level['Submenu'].get_cost(button))
                                        player_money.update_var(f'{int(player_stats["Space Crystals"])}')
                                        player_money_enlarged.update_var(f'{int(player_stats["Space Crystals"])}')
                                        level['Submenu'].update_cost(button)
                                        level['Submenu Stats'].update_stat(b)
                                    
                            else:
                                # Only update cost if the stat limit has not been reached
                                if level['Submenu Stats'].dict[level['Submenu Stats'].dict_keys[b]] == level['Submenu Stats'].stat_limits[b]:
                                    if game['Sounds'] is True:
                                        insufficient_funds_sound.play()
                                    stat_limit_reached_message.notify_player()
                                elif level['Submenu Stats'].dict[level['Submenu Stats'].dict_keys[b]] != level['Submenu Stats'].stat_limits[b]:  # Stat has NOT reached its limit
                                    if game['Sounds'] is True:
                                        button_clicked_sound.play()
                                    player_stats['Space Crystals'] -= int(level['Submenu'].get_cost(button))
                                    player_money.update_var(f'{int(player_stats["Space Crystals"])}')
                                    player_money_enlarged.update_var(f'{int(player_stats["Space Crystals"])}')
                                    level['Submenu'].update_cost(button)
                                    level['Submenu Stats'].update_stat(b)
                        
                        elif shield_stats_table.dict['Status'] == 'Inactive':
                            shield_not_active_message.notify_player()
                            if game['Sounds'] is True:
                                insufficient_funds_sound.play()
                        
                    # Handling main turret upgrades
                    elif level['Submenu'] == base_turret_upgrades:
                        if level['Submenu'].button_labels[b].text == 'Add Turret':
                                if player_stats['Power Gems'] >= level['Submenu'].get_cost(button):
                                    if level['Submenu Stats'].dict[level['Submenu Stats'].dict_keys[b]] < 4:
                                        if game['Sounds'] is True:
                                            button_clicked_sound.play()
                                        helper_turret_group.append(extra_turrets[len(helper_turret_group)])
                                        player_stats['Power Gems'] -= int(level['Submenu'].get_cost(button))
                                        #player_power_crystals.update_var(f'${int(player_stats["Space Crystals"])}')
                                        player_power_crystals_enlarged.update_var(f'{int(player_stats["Power Gems"])}')
                                        level['Submenu'].update_cost(button)
                                        level['Submenu Stats'].update_stat(b)
                                    else:
                                        if game['Sounds'] is True:
                                            insufficient_funds_sound.play()
                                        extra_turret_limit_reached_message.notify_player()
                                else:
                                    if game['Sounds'] is True:
                                        insufficient_funds_sound.play()
                                    not_enough_money_message.notify_player()
                            
                        # Handling all other main turret upgrades
                        else:
                            if level['Submenu Stats'].dict[level['Submenu Stats'].dict_keys[b]] == level['Submenu Stats'].stat_limits[b]:
                                if game['Sounds'] is True:
                                    insufficient_funds_sound.play()
                                stat_limit_reached_message.notify_player()
                            elif level['Submenu Stats'].dict[level['Submenu Stats'].dict_keys[b]] != level['Submenu Stats'].stat_limits[b]:
                                if game['Sounds'] is True:
                                    button_clicked_sound.play()
                                player_stats['Space Crystals'] -= int(level['Submenu'].get_cost(button))
                                player_money.update_var(f'{int(player_stats["Space Crystals"])}')
                                player_money_enlarged.update_var(f'{int(player_stats["Space Crystals"])}')
                                level['Submenu'].update_cost(button)
                                level['Submenu Stats'].update_stat(b)
                    
                    # Handling special attacks and special defenses upgrades            
                    elif level['Submenu'] == special_attacks_upgrades or \
                    level['Submenu'] == special_defenses_upgrades:
                        if player_stats['Power Gems'] >= level['Submenu'].get_cost(button):
                            if game['Sounds'] is True:
                                button_clicked_sound.play()
                            player_stats['Power Gems'] -= int(level['Submenu'].get_cost(button))
                            #player_power_crystals.update_var(f'${int(player_stats["Space Crystals"])}')
                            player_power_crystals_enlarged.update_var(f'{int(player_stats["Power Gems"])}')
                            level['Submenu'].update_cost(button)
                            level['Submenu Stats'].update_stat(b)
                        else:
                            if game['Sounds'] is True:
                                insufficient_funds_sound.play()
                            not_enough_money_message.notify_player()             
                                                                         
                    # Handling all other upgrades        
                    else:
                        if level['Submenu Stats'].dict[level['Submenu Stats'].dict_keys[b]] == level['Submenu Stats'].stat_limits[b]:
                            if game['Sounds'] is True:
                                insufficient_funds_sound.play()
                            stat_limit_reached_message.notify_player()
                        elif level['Submenu Stats'].dict[level['Submenu Stats'].dict_keys[b]] != level['Submenu Stats'].stat_limits[b]:
                            if game['Sounds'] is True:
                                button_clicked_sound.play()
                            player_stats['Space Crystals'] -= int(level['Submenu'].get_cost(button))
                            player_money.update_var(f'{int(player_stats["Space Crystals"])}')
                            player_money_enlarged.update_var(f'{int(player_stats["Space Crystals"])}')
                            level['Submenu'].update_cost(button)
                            level['Submenu Stats'].update_stat(b)
                    
                elif player_stats['Space Crystals'] < level['Submenu'].get_cost(button):
                    # Player does not enough enough money for desired upgrade
                    if game['Sounds'] is True:
                        insufficient_funds_sound.play()
                    not_enough_money_message.notify_player()
                
    
    screen.blit(bg, (0, 0))
    
    player_money_enlarged.show_to_player()
    screen.blit(power_crystal, (player_money_enlarged.rect.x - 40, player_money_enlarged.rect.top))
    player_money_enlarged_label.show_to_player()
    player_power_crystals_enlarged.show_to_player()
    screen.blit(power_gem_image, (player_power_crystals_enlarged.rect.x - 40, player_power_crystals_enlarged.rect.top))
    player_power_crystals_label.show_to_player()
    
    level['Submenu'].show_table()
    level['Submenu'].header.show_to_player()
    level['Submenu'].show_buttons()
    level['Submenu'].show_button_labels()
    
    level['Submenu Stats'].show_table()
    level['Submenu Stats'].header.show_to_player()
    level['Submenu Stats'].show_button_labels()
    level['Submenu Stats'].show_stats()
    
    for button in level['Submenu'].buttons:
        if level['Submenu'] == base_turret_upgrades:
            if button == base_turret_upgrades.buttons[-1]:
                screen.blit(power_gem_image, (button.rect.x - 40, button.rect.top + 15))
            else:
                screen.blit(power_crystal, (button.rect.x - 40, button.rect.top + 15))
        elif level['Submenu'] == special_attacks_upgrades or \
        level['Submenu'] == special_defenses_upgrades:
            screen.blit(power_gem_image, (button.rect.x - 40, button.rect.top + 15))
        else:
            screen.blit(power_crystal, (button.rect.x - 40, button.rect.top + 15))
    
    if level['Submenu'] == extra_turret1_upgrades or level['Submenu'] == extra_turret2_upgrades or \
    level['Submenu'] == extra_turret3_upgrades or level['Submenu'] == extra_turret4_upgrades:
        turret_x1_button.show()
        turret_x2_button.show()
        turret_x3_button.show()
        turret_x4_button.show()
    
    not_enough_money_message.show_notification()
    stat_limit_reached_message.show_notification()
    shield_already_active_message.show_notification()
    shield_not_active_message.show_notification()
    regeneration_already_active_message.show_notification()
    base_fully_repaired_message.show_notification()
    not_unlocked_yet_message.show_notification()
    extra_turret_limit_reached_message.show_notification()
    turret_not_purchased_message.show_notification()
    
    close_button.show()

def upgrade_menu():
    
    if True:
    
        for event in pygame.event.get():
            # Exiting the upgrade root menu
                if goto_levels_button.clicked(event):
                    if game['Sounds'] is True:
                        button_clicked_sound.play()
                    level['Upgrading'] = False
                    level['Overworld'] = True
                    level['Fade'] = True
                    base_upgrades_button.show_submenu = False
                    turret_upgrades_button.show_submenu = False
                    extra_upgrades_button.show_submenu = False              
                    
                    
                # Base Upgrades
                if base_health_upgrades_button.is_offsety():
                    if base_health_upgrades_button.clicked(event):
                        if game['Sounds'] is True:   
                            button_clicked_sound.play()
                        level['Fade'] = True
                        level['Upgrading'] = False
                        level['Upgrade Submenu'] = True
                        level['Upgrade Item'] = player_base
                        level['Submenu'] = base_upgrades
                        level['Submenu Stats'] = base_stats_table
                        base_stats_table.stats[0].update_var(f'{int(player_base.stats["Health"])}')
                        
                # Shield Upgrades
                if shield_upgrades_button.is_offsety():
                    if shield_upgrades_button.clicked(event):
                        if game['Sounds'] is True:
                            button_clicked_sound.play()
                        level['Fade'] = True
                        level['Upgrading'] = False
                        level['Upgrade Submenu'] = True
                        level['Submenu'] = shield_upgrades
                        level['Submenu Stats'] = shield_stats_table
                        
                # Main Turret Upgrades
                if base_turret_upgrades_button.is_offsety():
                    if base_turret_upgrades_button.clicked(event):
                        if game['Sounds'] is True:
                            button_clicked_sound.play()
                        level['Fade'] = True
                        level['Upgrading'] = False
                        level['Upgrade Submenu'] = True
                        level['Submenu'] = base_turret_upgrades
                        level['Submenu Stats'] = main_turret_stats_table
                        
                # Extra Turret Upgrades
                if extra_turret_upgrades_button.is_offsety():
                    if extra_turret_upgrades_button.rect.colliderect(base_turret_upgrades_button.rect) is False:
                        if extra_turret_upgrades_button.clicked(event):
                            # Player can access individual extra turret upgrades
                            if extra_turret1 not in helper_turret_group:
                                if game['Sounds'] is True:
                                    insufficient_funds_sound.play()
                                no_turrets_purchased_message.notify_player()
                            else:
                                if game['Sounds'] is True:
                                    button_clicked_sound.play()
                                #add in options to choose from which Turret to upgrade
                                level['Fade'] = True
                                level['Upgrading'] = False
                                level['Upgrade Submenu'] = True
                                level['Submenu'] = extra_turret1_upgrades
                                level['Submenu Stats'] = extra_turret1_stats_table
                        
                # Special Attacks Upgrades
                if special_attacks_button.is_offsety():
                    if special_attacks_button.clicked(event):
                        if game['Sounds'] is True:
                            button_clicked_sound.play()
                        level['Fade'] = True
                        level['Upgrading'] = False
                        level['Upgrade Submenu'] = True
                        level['Submenu'] = special_attacks_upgrades
                        level['Submenu Stats'] = special_attacks_stats_table
                        
                if special_defenses_button.is_offsety():
                    if special_defenses_button.clicked(event):
                        if game['Sounds'] is True:
                            button_clicked_sound.play()
                        level['Fade'] = True
                        level['Upgrading'] = False
                        level['Upgrade Submenu'] = True
                        level['Submenu'] = special_defenses_upgrades
                        level['Submenu Stats'] = special_defenses_stats_table      
                    
                if base_upgrades_button.clicked(event):
                    if game['Sounds'] is True:
                        button_clicked_sound.play()
                    turret_upgrades_button.show_submenu = False
                    extra_upgrades_button.show_submenu = False
                    base_upgrades_button.show_submenu = True if base_upgrades_button.show_submenu is False else False  
                    
                elif turret_upgrades_button.clicked(event):
                    if game['Sounds'] is True:
                        button_clicked_sound.play()
                    base_upgrades_button.show_submenu = False
                    extra_upgrades_button.show_submenu = False
                    turret_upgrades_button.show_submenu = True if turret_upgrades_button.show_submenu is False else False
                                   
                elif extra_upgrades_button.clicked(event):
                    if game['Sounds'] is True:
                        button_clicked_sound.play()
                    base_upgrades_button.show_submenu = False
                    turret_upgrades_button.show_submenu = False
                    extra_upgrades_button.show_submenu = True if extra_upgrades_button.show_submenu is False else False
                
        # Upgrades screen
        screen.blit(bg, (0, 0))
    
        # Upgrades title
        upgrades_menu_title.show_to_player()
        
        # Upgrades toggle buttons
        if shield_upgrades_button.is_offsety():
            shield_upgrades_button.show()
            
        if base_health_upgrades_button.is_offsety():
            base_health_upgrades_button.show()
            
        if extra_turret_upgrades_button.is_offsety():
            extra_turret_upgrades_button.show()
           
        if base_turret_upgrades_button.is_offsety():
            base_turret_upgrades_button.show()
            
        if special_defenses_button.is_offsety():
            special_defenses_button.show()
            
        if special_attacks_button.is_offsety():
            special_attacks_button.show()
        
        base_upgrades_button.show()
        turret_upgrades_button.show()
        extra_upgrades_button.show()
        goto_levels_button.show()
        
        must_reach_shield_level_message.show_notification()
        must_reach_extra_turret_upgrades_level_message.show_notification()
        no_turrets_purchased_message.show_notification()
        
        if base_upgrades_button.show_submenu is True:
            base_health_upgrades_button.slide_to((base_upgrades_button.rect.centerx, base_upgrades_button.rect.centery + base_upgrades_button.rect.height + 20), 12)
            shield_upgrades_button.slide_to((base_upgrades_button.rect.centerx, base_health_upgrades_button.rect.centery + base_health_upgrades_button.rect.height + 20), 12)
        else:
            base_health_upgrades_button.slide_to_origin(12)
            shield_upgrades_button.slide_to_origin(12)
            
        if turret_upgrades_button.show_submenu is True:
            base_turret_upgrades_button.slide_to((turret_upgrades_button.rect.centerx, turret_upgrades_button.rect.centery + turret_upgrades_button.rect.height + 20), 12)
            extra_turret_upgrades_button.slide_to((base_turret_upgrades_button.rect.centerx, base_turret_upgrades_button.rect.centery + base_turret_upgrades_button.rect.height + 20), 12)
        else:
            base_turret_upgrades_button.slide_to_origin(12)
            extra_turret_upgrades_button.slide_to_origin(12)
      
        if extra_upgrades_button.show_submenu is True:
            special_attacks_button.slide_to((extra_upgrades_button.rect.centerx, extra_upgrades_button.rect.centery + extra_upgrades_button.rect.height + 20), 12)
            special_defenses_button.slide_to((extra_upgrades_button.rect.centerx, special_attacks_button.rect.centery + special_attacks_button.rect.height + 20), 12)
        else:
            special_attacks_button.slide_to_origin(12)
            special_defenses_button.slide_to_origin(12)
            
    
def main_play():
    
    if level['Paused'] is False:
         
        for event in pygame.event.get():
             
            # Adjusting the current level speed
            # REMOVE BEFORE FINAL DISTRIBUTION TO TESTERS
            #if game_speed_button.clicked(event):
#                if game['Sounds'] is True:
#                    button_clicked_sound.play()
#                level['Button Clicked'] = True
#                if level['Speed'] == 1:
#                    level['Speed'] = 1.5
#                    game['Current Level'].spawn_delay = 2
#                elif level['Speed'] == 1.5:
#                    level['Speed'] = 2
#                    game['Current Level'].spawn_delay = 1
#                elif level['Speed'] == 2:
#                    level['Speed'] = 1
#                    game['Current Level'].spawn_delay = 4

            # Pausing the current level
            if pause_level_button.clicked(event):
                level['Paused'] = True
                
            # Level completed event handling
            if game['Current Level'].completed is True:
                if continue_level_button.clicked(event):
                    level['Button Clicked']
                    if game['Sounds'] is True:
                        button_clicked_sound.play()
                    level['Fade'] = True
                    level['Overworld'] = True
                    level['Battle'] = False
                    save_game()
                    game['Screen Transition'] = True
                    game['Current Track'] = starting_music
                    
            # Game over event handling
            if level['Game Over'] is True:
                # Reloading the current level
                if replay_button.clicked(event):
                    if game['Sounds'] is True:
                        button_clicked_sound.play()
                    level['Fade'] = True
                    level['Restart Game'] = True
                    game['Screen Transition'] = True
                    game['Current Track'] = gameplay_music2
                # Navigating back to level overworld
                if quit_button.clicked(event):
                    if game['Sounds'] is True:
                        button_clicked_sound.play()
                    level['Fade'] = True
                    level['Battle'] = False
                    level['Restart Game'] = True
                    level['Overworld'] = True
                    game['Screen Transition'] = True
                    game['Current Track'] = starting_music   
                    
            if player_base.stats['Health'] > 0:           
                    
                if rapid_fire_button.clicked(event):
                    level['Button Clicked'] = True
                    if player_base.special_attack_used is False:
                        player_base.special_attack_used = True
                        player_base.special_attack_start_time = time()
                        if base_turret.special_in_use is False:
                            base_turret.special_in_use = True
                            base_turret.special_start_time = time()
                            base_turret.special = 'Rapid Fire'
                            player_base.rapid_fire_delay = 0.1
                            #activate special timer countdown
                    
                if meteor_shower_button.clicked(event):
                    level['Button Clicked'] = True
                    if player_base.special_attack_used is False:
                        if special_attacks_stats_table.dict['Meteor Shower'] > 0:
                            player_base.meteor_shower(meteor_group)
                            player_base.special_attack_used = True
                            player_base.special_attack_start_time = time()
                            special_attacks_stats_table.dict['Meteor Shower'] -= 1
                            special_attacks_stats_table.reset_stats()
                                      
                if cluster_shot_button.clicked(event):
                    level['Button Clicked'] = True
                    player_base.special_attack_used = True
                    player_base.special_attack_start_time = time()
                    if special_attacks_stats_table.dict['Cluster Shots'] > 0:
                        base_turret.special = 'Cluster'
                        base_turret.special_in_use = True
                        special_attacks_stats_table.dict['Cluster Shots'] -= 1
                    
                if vaporize_button.clicked(event):
                    level['Button Clicked'] = True
                    if special_attacks_stats_table.dict['Vaporizers'] > 0:
                        player_base.vaporize_enemies(enemy_group)
                        player_base.special_attack_used = True
                        player_base.special_attack_start_time = time()
                        enemies_vaporized_sound.play()
                        special_attacks_stats_table.dict['Vaporizers'] -= 1
                    
                if raining_comets_button.clicked(event):
                    level['Button Clicked'] = True
                    if special_attacks_stats_table.dict['Raining Comets'] > 0:
                        player_base.special_attack_start_time = time()
                        player_base.raining_comets_start_time = time()
                        player_base.special_attack_in_use = 'Raining Comets'
                        player_base.special_attack_used = True
                        special_attacks_stats_table.dict['Raining Comets'] -= 1
                        
                if shock_absorber_button.clicked(event):
                    level['Button Clicked'] = True
                    if special_defenses_stats_table.dict['Shock Absorbers'] > 0:
                        player_base.special_defense_start_time = time()
                        player_base.special_defense_used = True
                        player_base.absorb_electric_shock = True
                        special_defenses_stats_table.dict['Shock Absorbers'] -= 1
                        
                if poison_antidote_button.clicked(event):
                    level['Button Clicked'] = True
                    if special_defenses_stats_table.dict['Poison Antidote'] > 0:
                        player_base.special_defense_start_time = time()
                        player_base.special_defense_used = True
                        player_base.poison_antidote_applied = True
                        special_defenses_stats_table.dict['Poison Antidote'] -= 1
                                    
            # Player firing main turret
            if level['Button Clicked'] is False:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if player_base.stats['Health'] > 0:
                        if player_base.special_attack_used is True and base_turret.special == 'Cluster':
                            player_base.special_attack_start_time = time()
                            player_base.cluster_shot(player_bullet_group)
                            base_turret.special = None                
                        else:
                            base_turret.shoot(player_bullet_group)
                            #player_base.spray_bullets_from_edge()
                            game['Current Level'].total_shots_taken += 1
                            
        # Tracking timing for special attacks being used
        if player_base.special_attack_used is True:
            if time() - player_base.special_attack_start_time > base_turret.stats['Special Cooldown']:
                player_base.special_attack_used = False
                
        # Tracking timing for special defenses being used
        if player_base.special_defense_used is True:
            if time() - player_base.special_defense_start_time > player_base.special_defense_duration:
                player_base.special_defense_used = False
                player_base.absorb_electric_shock = False
                player_base.poison_antidote_applied = False
                        
        # Player using Rapid Fire special attack
        if pygame.mouse.get_pressed()[0] is True and level['Button Clicked'] is False:
            if time() - base_turret.special_start_time <= 30:
                if time() - base_turret.last_shot_time >= player_base.rapid_fire_delay:
                    base_turret.shoot(player_bullet_group)
            else:
                if time() - base_turret.last_shot_time >= player_base.rapid_fire_delay:
                    base_turret.shoot(player_bullet_group)
               
        # Raining comets special attack until it has reached its full duration
        if player_base.special_attack_used is True:
            if player_base.special_attack_in_use == 'Raining Comets':
                player_base.rain_comets(raining_comets_group)       
               
        # Rapid Fire special attack being disabled
        if base_turret.special_in_use is True and base_turret.special == 'Rapid Fire':
            if time() - base_turret.special_start_time >= 30:
               base_turret.special_in_use = False
               base_turret.special = None
               player_base.rapid_fire_delay = 1
               
        if pygame.mouse.get_pressed()[0] is False:
            level['Button Clicked'] = False
                
        # Waiting 3 seconds before enemies start spawning          
        if time() - game['Current Level'].start_time > 3:
            if len(enemy_group) < 20 and player_base.stats['Health'] > 0:
                # Spawn enemy ships until all the enemies have been spawned
                if time() - level['Spawn Time'] >= game['Current Level'].spawn_delay:
                    game['Current Level'].spawn_enemy()
                    level['Spawn Time'] = time()           
                            
        # Enemy attacks hitting the base or shield        
        if pygame.sprite.groupcollide(enemy_bullet_group, base_group, False, False):
            player_base.collided_enemy_bullets = pygame.sprite.groupcollide(enemy_bullet_group, base_group, False, False, pygame.sprite.collide_mask)
            if player_base.collided_enemy_bullets:
                    for c in player_base.collided_enemy_bullets:
                        for d in player_base.collided_enemy_bullets[c]:
                            if c.__class__ == Bullet:
                                if c.poisonous is True:
                                    # Base or shield gets poisoned
                                    d.poisoned = True
                                    d.poisoned_amount += c.poison_amount
                                    game['Current Level'].player_base_damage_taken += c.poison_amount
                                else:
                                    d.take_damage(c.damage)
                                    game['Current Level'].player_base_damage_taken += c.damage
                                c.kill()
                                if d.__class__ == Base:
                                    animations_group.add(Animation(impact_animation, 1, c.pos, base_hit_sound))
                            elif c.__class__ == ChargeBolt:
                                if d.__class__ == Shield:
                                    # Electric Shield takes 1 percent damage of the charge bolt
                                    d.take_damage(c.damage / 100)
                                    game['Current Level'].player_base_damage_taken += c.damage / 100
                                else:
                                    # Base and turrets get electrocuted
                                    if d.absorb_electric_shock is True:
                                        c.kill()
                                    else:
                                        d.electrocution_damage = c.damage
                                        d.electrified = True
                                        d.electrified_start_time = time()
                                    game['Current Level'].player_base_damage_taken += c.damage
                                    # Every existing helper turret is rendered useless while being electrocuted
                                    # Main turret is not affected
                                    for h in helper_turret_group:
                                        h.paralyzed = True
                                        h.paralyzed_start_time = time()                        
             
        # Black hole sucking in enemy ships that collide with the black hole rect
        if len(player_defenses_group) > 0:
            defense_collisions = pygame.sprite.groupcollide(player_defenses_group, enemy_group, False, False)
            if defense_collisions:
                for defense in defense_collisions:
                    for enemy in defense_collisions[defense]:
                        enemy.black_hole_death = True
                        enemy.black_hole = defense
                if pygame.sprite.groupcollide(player_defenses_group, enemy_group, False, False, pygame.sprite.collide_circle_ratio(0.75)):
                    for enemy in defense_collisions[defense]:
                        enemy.take_damage(enemy.max_health * 0.01)
                        enemy.image = pygame.transform.scale_by(enemy.image, 0.9)
             
        # Player bullet hitting enemy ships
        if pygame.sprite.groupcollide(player_bullet_group, enemy_group, False, False):  
            enemy_collisions = pygame.sprite.groupcollide(player_bullet_group, enemy_group, False, False, pygame.sprite.collide_mask)     
            if enemy_collisions:
                for bullet in enemy_collisions:
                    
                    for ship in enemy_collisions[bullet]:
                        if ship.has_shield() and ship.shield.active is True:
                            if bullet.mask.overlap(ship.shield.mask, (ship.shield.rect.x - bullet.rect.x, ship.shield.rect.y - bullet.rect.y)):
                                ship.shield.take_damage(bullet.damage)
                        elif ship.has_shield() and ship.shield.active is False or \
                        ship.has_shield() is False:
                            ship.take_damage(bullet.damage)
                        bullet.kill()
                        if bullet.player_shot is True:
                            game['Current Level'].total_shots_hit += 1                  
                                          
        # Player bullet colliding with a flare
        if len(flares_group) > 0:
            if pygame.sprite.groupcollide(player_bullet_group, flares_group, False, False):
                if pygame.sprite.groupcollide(player_bullet_group, flares_group, True, True, pygame.sprite.collide_mask):
                    game['Current Level'].total_shots_hit += 1
                                     
        screen.blit(bg, (0, 0))
        
        enemy_missile_group.update()
        enemy_missile_group.draw(screen)
                
        laser_beam_group.update(base_group)
        laser_beam_group.draw(screen)
              
        base_group.update(base_and_shield_stats_container)
        base_group.draw(screen)       
        
        player_bullet_group.update()
        player_bullet_group.draw(screen)
        
        meteor_group.update()
        meteor_group.draw(screen)
        
        bomb_group.update()
        bomb_group.draw(screen)
        
        raining_comets_group.update()
        raining_comets_group.draw(screen)
        
        for helper in helper_turret_group:
            helper.update(enemy_group)
            helper.draw()
            if helper.attack is True and level['Game Over'] is False:
                if helper.target_in_range():
                    helper.help_shoot(player_bullet_group)    
                
        flares_group.update()
        flares_group.draw(screen)
        
        spawn_orb_group.update(spawn_orb_group)
        spawn_orb_group.draw(screen)          
                
        enemy_bullet_group.update()
        enemy_bullet_group.draw(screen)
                           
        base_turret.follow_mouse_pos()
        
        player_defenses_group.update()
        player_defenses_group.draw(screen)
                
        healing_ring_group.update()
        healing_ring_group.draw(screen)
        
        health_flares_group.update()
        health_flares_group.draw(screen)
            
        enemy_group.update(game['Delta Time'])
        enemy_group.draw(screen)    
        
        animations_group.update(player_base)
        animations_group.draw(screen)       
        
        # Level Completed Feedback Message
        if player_base.stats['Health'] > 0:
            if game['Current Level'].done_spawning() and len(enemy_group) == 0:
                if game['Current Level'].played_winning_sound is False:
                    pygame.mixer.music.pause()
                    level_completed_sound.play()
                    game['Current Level'].played_winning_sound = True
                enemy_bullet_group.empty()
                player_bullet_group.empty()
                if game['Current Level'].completed is False:
                    #if player took no damage, give bonus loot
                    if game['Current Level'].player_base_damage_taken <  1:
                        level_completed_menu.generate_winnings(game['Current Level'].loot_drop(), game['Current Level'].power_gem_loot(), game['Current Level'].bonus_loot())
                        player_stats['Space Crystals'] += game['Current Level'].loot_drop()
                        player_stats['Power Gems'] += game['Current Level'].power_gem_loot()
                        player_stats['Space Crystals'] += game['Current Level'].bonus_loot()
                    elif game['Current Level'].player_base_damage_taken > 0:
                        level_completed_menu.generate_winnings(game['Current Level'].loot_drop(), game['Current Level'].power_gem_loot())
                        player_stats['Space Crystals'] += game['Current Level'].loot_drop()
                        player_stats['Power Gems'] += game['Current Level'].power_gem_loot()
                    player_money.update_var(f'{int(player_stats["Space Crystals"])}')
                    player_power_crystals_enlarged.update_var(f'{int(player_stats["Power Gems"])}')
                    player_money_enlarged.update_var(f'{int(player_stats["Space Crystals"])}')
                    if game['Current Level'].num < len(levels):
                        levels[game['Current Level'].num].locked = False
                        levels_locked_status[status_keys[game['Current Level'].num]] = False
                game['Current Level'].completed = True
                
                        
        # Player was defeated in the current playing level
        if player_base.stats['Health'] <= 0:
            if game['Current Level'].played_defeated_sound is False:
                pygame.mixer.music.pause()
                level_defeated_sound.play()
                game['Current Level'].played_defeated_sound = True
            enemy_bullet_group.empty()
            player_bullet_group.empty()
            level['Game Over'] = True
            game['Game Over Time'] = time()
        else:
            level['Game Over'] = False
            
        # Level feedback
        #level_feedback.snap_to_topright()
#        level_feedback.show_to_player()
        
        pause_level_button.show()
        
        # Notifying player of the incoming boss if current level has a boss
        if game['Current Level'].is_boss_level():
            if game['Current Level'].done_spawning() and len(enemy_group) > 0:
                if game['Current Level'].notified_player_about_boss is False:
                    pygame.mixer.music.stop()
                    incoming_boss_sound.play()
                    game['Current Level'].notified_player_about_boss = True
                    game['Screen Transition'] = True
                    game['Current Track'] = boss_battle_music                  
                if game['Current Level'].boss is not None:
                    game['Current Level'].show_boss_name_and_health()
        
        # Only showing Special attacks if the player has some to use
        if special_attacks_stats_table.dict['Rapid Fire'] > 0 or \
        special_attacks_stats_table.dict['Meteor Shower'] > 0 or \
        special_attacks_stats_table.dict['Cluster Shots'] > 0 or \
        special_attacks_stats_table.dict['Vaporizers'] > 0 or \
        special_attacks_stats_table.dict['Raining Comets'] > 0:
            special_attacks_container_label.show()
            special_attacks_container.show()
        
        # Only showing the special defenses if the player has some to use
        if special_defenses_stats_table.dict['Shock Absorbers'] > 0 or \
        special_defenses_stats_table.dict['Poison Antidote'] > 0:
            special_defenses_container_label.show()
            special_defenses_container.show()          
        
        # Special Attacks Buttons showing if the player has them to use
        if special_attacks_stats_table.dict['Rapid Fire'] > 0:
            rapid_fire_button.show()
        if special_attacks_stats_table.dict['Meteor Shower'] > 0:
            meteor_shower_button.show()
        if special_attacks_stats_table.dict['Cluster Shots'] > 0:
            cluster_shot_button.show()
        if special_attacks_stats_table.dict['Vaporizers'] > 0:
            vaporize_button.show()
        if special_attacks_stats_table.dict['Raining Comets'] > 0:
            raining_comets_button.show()
            
        # Special Defenses Buttons showing if the player has them to use
        if special_defenses_stats_table.dict['Shock Absorbers'] > 0:
            shock_absorber_button.show()
        if special_defenses_stats_table.dict['Poison Antidote'] > 0:
            poison_antidote_button.show()
        
        # Winning rewards menu slides up from the bottom of the screen to the middle
        if game['Current Level'].completed is True and level['Battle'] is True:
            level_completed_menu.slide_to_middle(9)
            continue_level_button.slide_to((level_completed_menu.rect.centerx, level_completed_menu.rect.bottom - level_nav_button.get_height() - 5), 10)
            
        if level['Game Over'] is True and level['Restart Game'] is False:
            level_defeated_menu.slide_to_middle(9)
            replay_button.slide_to((level_defeated_menu.rect.centerx + level_nav_button.get_width() / 2 + 5, level_defeated_menu.rect.bottom - level_nav_button.get_height() - 5), 10)
            quit_button.slide_to((replay_button.rect.centerx - level_nav_button.get_width() - 10, replay_button.rect.centery), 10)
            
        if level['Battle'] is False or game['Current Level'].completed is False:
            level_completed_menu.slide_to_origin(10)
            continue_level_button.slide_to_origin(10)
           
        if player_base.stats['Health'] > 0 or level['Battle'] is False or \
        level['Restart Game'] is True:
            level_defeated_menu.slide_to_origin(10)
            replay_button.slide_to_origin(10)
            quit_button.slide_to_origin(10)
           
        if level_completed_menu.rect.top <= screen_height:
            level_completed_menu.show()
            continue_level_button.show()     
            
        if level_defeated_menu.rect.top <= screen_height:
            level_defeated_menu.show()
            replay_button.show()
            quit_button.show()       
            
        # Showing the pause level menu
    if level['Paused'] is True:
            
            for event in pygame.event.get():
                if unpause_game_button.clicked(event):
                    level['Paused'] = False
                    
                if abandon_game_button.clicked(event):
                    level['Abandoned'] = True
                    level['Button Clicked']
                    if game['Sounds'] is True:
                        button_clicked_sound.play()
                    level['Fade'] = True
                    level['Overworld'] = True
                    level['Battle'] = False
                    #level['Paused'] = False
                    game['Screen Transition'] = True
                    game['Current Track'] = starting_music
            
            if level['Abandoned'] is False:            
                paused_level_menu.show()
                unpause_game_button.show()
                abandon_game_button.show()
            
                 
    
def main():
    
    level['Screen'] = menu
    play_music_track(game['Current Track'])
    
    while level['Playing'] is True:
        
        if game['Music'] is True:
            toggle_music_status_label.image = toggle_on_text
        elif game['Music'] is False:
            toggle_music_status_label.image = toggle_off_text
            
        if game['Sounds'] is True:
            toggle_sounds_status_label.image = toggle_on_text
        elif game['Sounds'] is False:
            toggle_sounds_status_label.image = toggle_off_text
        
        game['Delta Time'] = time() - game['Previous Time']
        game['Previous Time'] = time()      
                      
        if level['Fade'] is True:
            screen_shader.fade_to_black()
        if level['Fade'] is False:
            screen_shader.fade_from_black()
            
        if screen_shader.alpha >= 254:
            level['Fade'] = False
            if level['On Menu'] is True:
                level['Screen'] = menu
            elif level['Settings'] is True:
                level['Screen'] = settings_menu    
            elif level['Game Select'] is True:
                level['Screen'] = load_game_selection_menu
            elif level['Overworld'] is True:
                if level['Abandoned'] is True:
                    player_base.stats['Health'] = game['Current Level'].player_base_starting_health
                    base_shield.stats['Health'] = game['Current Level'].base_shield_starting_health
                    level['Abandoned'] = False
                level['Screen'] = level_overworld          
            elif level['Battle'] is True:
                base_health_upgrades_button.reset_position()
                shield_upgrades_button.reset_position()
                base_turret_upgrades_button.reset_position()
                extra_turret_upgrades_button.reset_position()
                special_attacks_button.reset_position()
                special_defenses_button.reset_position()
                enemy_bullet_group.empty()
                player_bullet_group.empty()
                flares_group.empty()
                enemy_group.empty()   
                level['Paused'] = False             
                level['On Menu'] = False
                level['Screen'] = main_play  
                game['Current Level'].load(player_base)
                     
            elif level['Upgrading'] is True:
                level['Battle'] = False
                level['Screen'] = upgrade_menu
            elif level['Upgrade Submenu'] is True:
                level['Screen'] = upgrade_submenu
                
            # Game Restart
            if level['Restart Game'] is True:
                game['Current Level'].load(player_base)
                enemy_bullet_group.empty()
                player_bullet_group.empty()
                flares_group.empty()
                enemy_group.empty()
                player_base.stats['Health'] = player_base.stats['Max Health']
                level['Restart Game'] = False
                
        level['Screen']()       
        
        screen_shader.show()
        
        if game['Music'] is False:
            pygame.mixer.music.set_volume(0)
        if game['Screen Transition'] is True:
            music_manager(game['Current Track'])
            
        #if level['Battle'] is True:# and CLOCK.get_fps() > 50:
#            print('{:.2f}'.format(CLOCK.get_fps()))
            #show_variable(f'FPS = {int(CLOCK.get_fps())}', reg_font, (1380, 700))
        #show_variable(f'{screen_width}', reg_font, (100, 700))
        #screen.blit(vaporizing_arc_image, (screen_width * 0.25, 0))
        #screen.blit(test_back_button, (300, 300))
        #player_defenses_group.update()
        #player_defenses_group.draw(screen)    
        
        CLOCK.tick()
        pygame.display.update()
        
if __name__ == "__main__":
    profile.run('main()')
    #main()
    
pygame.quit()