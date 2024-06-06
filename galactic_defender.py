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
screen_width = 1460 #window_info.current_w
screen_height = 720 #window_info.current_h
screen_middle = pygame.math.Vector2(screen_width / 2, screen_height / 2)
screen = pygame.display.set_mode((screen_width, screen_height))


def show_variable(var, font, loc=(300,600)):    
    surf = font.render(f'{var}', True, 'yellow')
    rect = surf.get_rect(center=loc)
    screen.blit(surf, rect)

        
def load_and_scale(image_path, scale_y=False):
    global screen_width
    global screen_height
    default_aspect_ratio = 1460 / 720
    current_aspect_ratio = screen_width / screen_height
    aspect_ratio_difference = current_aspect_ratio / default_aspect_ratio
    img = pygame.image.load(image_path).convert_alpha()
    img = pygame.transform.scale_by(img, aspect_ratio_difference)
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
    
    ships = listdir(folder)
    fixed_ships = dict()
    for img in ships:
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
        fixed_ships[img] = new_img

    return fixed_ships
 
       
def load_saved_games(games):
    
    saved_games_list = [k for k in games.keys()]
    games_selection = list()
    x = screen_width * 0.25
    y = screen_height * 0.33
    for b in saved_games_list:
        if len(games_selection) % 9 == 0:
            x = (screen_width * len(games_selection) // 9) + screen_width * 0.25
            y = screen_height * 0.33
        game_link_index = saved_games_list.index(b)
        with open(b + '.txt', 'r') as f:
            lines = f.readlines()
            stats = json.loads(lines[3])
            rank = stats['Rank']
        game_link = Button(upgrades_stat_bar, (x, y), rank, ui_font, connected_game=saved_games_list[game_link_index])
        #games_selection[b] = game_link 
        games_selection.append(game_link)
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

class ClassEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__
            

FPS = 60
CLOCK = pygame.time.Clock()

pygame.display.set_caption('Galactic Defender')

# Modified font sizes for dynamic screen sizing
size_15_font = screen_width * (15 / 1460)
size_18_font = screen_width * (18 / 1460)
size_20_font = screen_width * (20 / 1460)
size_25_font = screen_width * (25 / 1460)
size_30_font = screen_width * (30 / 1460)
size_35_font = screen_width * (35 / 1460)
size_45_font = screen_width * (45 / 1460)
size_50_font = screen_width * (50 / 1460)
size_60_font = screen_width * (60 / 1460)

# Fonts
ui_15_font = pygame.font.SysFont('Fonts/Pavelt.ttf', int(size_15_font))
ui_18_font = pygame.font.SysFont('Fonts/Pavelt.ttf', int(size_18_font))
debug_font = pygame.font.SysFont('arial', int(size_25_font))
ui_20_font = pygame.font.Font('Fonts/Pavelt.ttf', int(size_20_font))
ui_font = pygame.font.Font('Fonts/Pavelt.ttf', int(size_25_font))
ui_30_font = pygame.font.Font('Fonts/Pavelt.ttf', int(size_30_font))
upgrades_font = pygame.font.Font('Fonts/Pavelt.ttf', int(size_35_font))
ui_45_font = pygame.font.Font('Fonts/Pavelt.ttf', int(size_45_font))
title_font = pygame.font.Font('Fonts/Pavelt.ttf', int(size_50_font))
big_font = pygame.font.Font('Fonts/Pavelt.ttf', int(size_60_font))

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
game_title_label_image = load_and_scale('Menu/game_title.png')

# Levels Menu Title
levels_menu_title = load_and_scale('UI Text/level_overworld_title.png')

# UI Text
music_text = load_and_scale('UI Text/music.png')
sounds_text = load_and_scale('UI Text/sounds.png')
toggle_on_text = load_and_scale('UI Text/on.png')
toggle_off_text = load_and_scale('UI Text/off.png')

# Currency UI Labels
space_crystals_label_image = load_and_scale('UI Text/space_crystals.png')
power_gems_label_image = load_and_scale('UI Text/power_gems.png')

# UI Buttons
goto_levels_button_image = load_and_scale('UI Buttons/goto_levels.png')
goto_menu_button_image = load_and_scale('UI Buttons/goto_menu.png')
goto_upgrades_button_image = load_and_scale('UI Buttons/goto_upgrades.png')
go_back_button_image = pygame.image.load('UI Buttons/go_back.png').convert_alpha()
go_back_to_upgrades_button_image = pygame.transform.scale_by(goto_upgrades_button_image, 0.6)
go_back_button_image = pygame.transform.scale(go_back_button_image, (screen_width * 0.16, screen_height * 0.1))
resume_game_button_image = load_and_scale('UI Buttons/resume_game.png')
play_button_image = load_and_scale('UI Buttons/play_game.png')
delete_button_image = load_and_scale('UI Buttons/delete_game.png')
locked_level_button_image = load_and_scale('locked_level.png')

# Main Menu Buttons 
new_game_button_image = load_and_scale('UI Buttons/new_game.png')
load_game_button_image = load_and_scale('UI Buttons/load_game.png')
exit_game_button_image = load_and_scale('UI Buttons/exit_game.png')

# Settings Menu Title
settings_menu_title_image = load_and_scale('UI Text/settings_menu_title.png')

# Settings Buttons
music_toggle_button_image = load_and_scale('music_toggle_button.png')
sounds_toggle_button_image = load_and_scale('sounds_toggle_button.png')

# Upgrades Buttons
base_upgrades_button_image = load_and_scale('UI Buttons/base_upgrades.png')
base_health_upgrades_button_image = load_and_scale('UI Buttons/health_upgrades.png')
shield_upgrades_button_image = load_and_scale('UI Buttons/shield_upgrades.png')
turrets_upgrades_button_image = load_and_scale('UI Buttons/turret_upgrades.png')
main_turret_upgrades_button_image = load_and_scale('UI Buttons/main_turret_upgrades.png')
extra_turrets_upgrades_button_image = load_and_scale('UI Buttons/helpers_upgrades.png')
extra_upgrades_button_image = load_and_scale('UI Buttons/special_upgrades.png')
special_attacks_upgrades_button_image = load_and_scale('UI Buttons/special_attacks_upgrades.png')
special_defenses_upgrades_button_image = load_and_scale('UI Buttons/special_defenses_upgrades.png')

# Special Attacks Buttons
rapid_fire_button_image = load_and_scale('UI Buttons/rapid_fire.png')
cluster_shot_button_image = load_and_scale('UI Buttons/cluster_shot.png')
raining_comets_button_image = load_and_scale('UI Buttons/raining_comets.png')
vaporize_button_image = load_and_scale('UI Buttons/vaporize.png')
meteor_shower_button_image = load_and_scale('UI Buttons/meteor_shower.png')

# Special Defenses Buttons
shock_absorber_button_image = load_and_scale('UI Buttons/shock_absorber.png')
poison_antidote_button_image = load_and_scale('UI Buttons/poison_antidote.png')
flares_defense_button_image = load_and_scale('UI Buttons/flares_defense.png')
laser_deflection_button_image = load_and_scale('UI Buttons/laser_deflection.png')
magnetic_mine_button_image = load_and_scale('UI Buttons/magnetic_mine.png')

# Special Attack and Defenses container
specials_container = load_and_scale('specials_container.png')

# Special Attacks and Defenses Label abbreviations
special_attacks_label_abbreviated = load_and_scale('UI Text/special_attacks_abbreviated_label.png')
special_defenses_label_abbreviated = load_and_scale('UI Text/special_defenses_abbreviated_label.png')

settings_button_image = load_and_scale('settings_button.png')
continue_button_image = load_and_scale('continue_button.png')
previous_button_image = load_and_scale('previous.png')

level_nav_button = pygame.image.load('continue_level_button.png').convert_alpha()
#level_nav_button = load_and_scale('continue_level_button.png')

level_options_button_image = load_and_scale('menu_button.png')
pause_level_button_image = load_and_scale('pause_level_button.png')
game_speed_button_image = load_and_scale('adjust_game_speed.png')

# Close button
close_button_image = load_and_scale('close_button.png')

# Player Space Base
base_main = pygame.image.load('Player/player_base.png').convert_alpha()
base_main = pygame.transform.scale(base_main, (screen_width * 0.4, screen_width * 0.4))
electrocuted_base = pygame.image.load('Player/electrocuted_base.png').convert_alpha()
electrocuted_base = pygame.transform.scale(electrocuted_base, (screen_width * 0.4, screen_width * 0.4))
poisoned_base = pygame.image.load('Player/poisoned_base.png').convert_alpha()
poisoned_base = pygame.transform.scale(poisoned_base, (screen_width * 0.4, screen_width * 0.4))
rubberized_base = pygame.image.load('Player/deflection_base.png').convert_alpha()
rubberized_base = pygame.transform.scale(rubberized_base, (screen_width * 0.4, screen_width * 0.4))
shield_main = load_and_scale('Player/base_shield.png')
turret_main = load_and_scale('Player/base_turret_main.png')
turret_extra = load_and_scale('Player/helper_turret.png')
electrocuted_turret = load_and_scale('Player/electrocuted_turret.png')
frozen_turret_image = load_and_scale('Player/frozen_turret.png')
vaporizing_arc_image = load_and_scale('vaporizing_arc.png')
base_health_container = load_and_scale('base_health_container.png')

# Bullets
player_laser = load_and_scale('player_bullet.png')
enemy_laser = load_and_scale('enemy_bullet.png')
enemy_turret_laser = load_and_scale('enemy_turret_laser.png')
poison_laser = load_and_scale('poison_laser.png')
normal_poison_laser = load_and_scale('poison_laser_normal.png')
destroy_shield_laser = load_and_scale('destroyer.png')
wave_blast_image = load_and_scale('wave_blast.png')
solid_laser_image = load_and_scale('solid_laser.png')
laser_flare =load_and_scale('enemy_flare.png')
cluster_laser_image = load_and_scale('cluster_laser.png')
laser_cluster_image = load_and_scale('laser_cluster.png')
critical_laser_image = load_and_scale('critical_laser.png')

# Electric bolts
charge_bolt_image = load_and_scale('charge_bolts.png')

raining_comet_image = load_and_scale('raining_comet.png')
magnetic_mine_image = load_and_scale('magnetic_mine.png')

# Missiles
side_missile_image = load_and_scale('side_missile.png')

# Bombs
enemy_rubble_bomb = load_and_scale('rubble_bomb.png')

# Enemy Ships
enemy_ships = load_enemy_ships('Enemy Ships/')
enemy_boss_images = load_enemy_ships('Boss Ships/', boss=True)

healer_ring_no_effect_image = pygame.image.load('healer_ring_no_effect.png').convert_alpha()
healer_ring_no_effect_image = pygame.transform.scale(healer_ring_no_effect_image, (200, 200))

healer_ring_with_effect_image = pygame.image.load('healer_ring_with_effect.png').convert_alpha()
healer_ring_with_effect_image = pygame.transform.scale(healer_ring_with_effect_image, (200, 200))

health_recovery_icon_image = load_and_scale('health_recovery_icon.png')

# Spawning Orbs
turret_spawn_orb = load_and_scale('boss2_turret_spawn_shot.png')

# Meteors
tan_meteor = load_and_scale('meteor.png')

level_overworld_button = load_and_scale('level_button.png')
level_button = pygame.transform.scale_by(level_overworld_button, 2)

# Player currency and loot images
power_crystal = load_and_scale('power_crystal.png')
power_gem_image = load_and_scale('power_gem.png')

# Player Power Stone images
red_power_stone_image = load_and_scale('Power Stones/red.png')
orange_power_stone_image = load_and_scale('Power Stones/orange.png')
yellow_power_stone_image = load_and_scale('Power Stones/yellow.png')
green_power_stone_image = load_and_scale('Power Stones/green.png')
blue_power_stone_image = load_and_scale('Power Stones/blue.png')

#level_over_menu = pygame.image.load('level_over_window.png').convert_alpha()
level_over_menu = load_and_scale('level_over_window.png')

upgrade_table = load_and_scale('upgrade_window.png')
upgrades_stat_bar = load_and_scale('Table.png')
turret_empty_location = pygame.image.load('turret_location_indicator.png').convert_alpha()
turret_empty_location = pygame.transform.scale(turret_empty_location, (screen_width * 0.044, screen_height * 0.0986))

class Title:
    
    def __init__(self, image, pos):
        self.image = image
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        
    def show(self):
        screen.blit(self.image, self.rect)

    def show_to_player(self):
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
        self.rect = self.image.get_rect(center=self.loc)
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
        if self.dict[self.dict_keys[i]] >= 999999:
            self.dict[self.dict_keys[i]] = 999999
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

    def __init__(self, image, loc, label, label_font, connected_game=None):
        self.color = 'yellow'
        self.image = image
        self.loc = pygame.math.Vector2(loc)
        self.origin_pos = pygame.math.Vector2(loc)
        self.rect = self.image.get_rect(center=self.loc)
        if label != None:
            self.label = Feedback(f'{label}', label_font, self.rect.center)
        else:
            self.label = label
        self.connected_game = connected_game
        self.button_mask = pygame.mask.from_surface(self.image)
        self.button_mask_surf = self.button_mask.to_surface(setcolor='cyan', unsetcolor=(0, 0, 0, 0)).convert_alpha()
        self.show_submenu = False
        self.locked = False
        self.notify = False
        self.flash_counter = 0
        self.flashes = 1
        self.scroll_amount = 0
        self.remaining_uses = Feedback('0', ui_20_font, (self.rect.left + (self.rect.width * 0.74), self.rect.top + (self.rect.height * 0.2)))
                
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
                        
    def show_to_player(self):
        self.show()
            
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
        
    def show_selected_dot(self):
        pygame.draw.circle(screen, 'green', (self.rect.left + (self.rect.width * 0.2), self.rect.top + (self.rect.height * 0.2)), 5)
        
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
        self.power_gems_loot = None
        self.power_gems_loot_label = None
        self.lives_left_label = None
        self.lives_left_num = None
        
    def show(self):
        screen.blit(self.image, self.rect)
        self.header.show_to_player()
        if self.winning_loot != None:
            self.winning_loot_label.show_to_player()
            self.winning_loot.show_to_player()
            self.power_gems_loot_label.show_to_player()        
            self.power_gems_loot.show_to_player()
            screen.blit(power_crystal, (self.winning_loot.rect.x - 40, self.winning_loot.rect.y))
            screen.blit(power_gem_image, (self.power_gems_loot.rect.x - 40, self.power_gems_loot.rect.y))
        if self.bonus_loot != None:
            self.bonus_loot.show_to_player()
        
    def show_lost_info(self):
        if self.lives_left_label != None:
            self.lives_left_label.show_to_player()
            self.lives_left_num.show_to_player()
            self.lives_left_label.rect.center = (self.rect.centerx, self.rect.top + (self.rect.height * 0.3))
            self.lives_left_num.rect.center = (self.lives_left_label.rect.right + size_30_font, self.lives_left_label.rect.centery)
            
    def generate_winnings(self, loot, power_gems, bonus_loot=None):
        accuracy = game['Current Level'].get_accuracy()
        self.winning_loot_label = Feedback('Rewards', upgrades_font, (self.rect.centerx, self.rect.top + self.rect.height * 0.25))
        self.winning_loot = Feedback(f'{int(loot)}', ui_30_font, (self.rect.centerx, self.winning_loot_label.rect.centery + self.winning_loot_label.rect.height + 10))
        self.power_gems_loot_label = Feedback(f'{accuracy}% Acc. Bonus', upgrades_font, (self.rect.centerx, self.winning_loot.rect.bottom + self.winning_loot.rect.height))
        self.power_gems_loot = Feedback(f'{int(power_gems)}', ui_30_font, (self.winning_loot.rect.centerx, self.power_gems_loot_label.rect.centery + self.power_gems_loot_label.rect.height + 10))
        if bonus_loot != None:
            self.bonus_loot = bonus_loot 
            self.bonus_loot.rect.center = self.rect.centerx, self.rect.top + (self.rect.height * 0.7)
        else:
            self.bonus_loot = None
    
    def generate_lost_info(self, lives_left, available_power_stones=None):
        self.lives_left_label = Feedback('Lives Left:', ui_font, (self.rect.centerx, self.rect.top + (self.rect.height * 0.3)))
        self.lives_left_num = Feedback(f'{lives_left}', ui_font, (self.lives_left_label.rect.right + size_30_font, self.lives_left_label.rect.centery))
        
    def slide_to_middle(self, speed):
        self.loc.move_towards_ip((screen_width / 2, screen_height / 2), speed)
        self.rect.center = self.loc
        self.header.rect.center = (self.rect.centerx, self.rect.top + 50)
        if self.winning_loot != None:
            self.winning_loot_label.rect.center = (self.rect.centerx, self.rect.top + self.rect.height * 0.25)
            self.winning_loot.rect.center = (self.rect.centerx, self.winning_loot_label.rect.centery + self.winning_loot_label.rect.height + 10)
        if self.power_gems_loot != None:
            self.power_gems_loot_label.rect.center = (self.rect.centerx, self.winning_loot.rect.bottom + self.winning_loot.rect.height)
            self.power_gems_loot.rect.center = (self.winning_loot.rect.centerx, self.power_gems_loot_label.rect.centery + self.power_gems_loot_label.rect.height + 10)
        if self.bonus_loot != None:
            self.bonus_loot.rect.center = self.rect.centerx, self.rect.top + (self.rect.height * 0.7)
            
        
    def slide_to_origin(self, speed):
        self.loc.move_towards_ip(self.origin_pos, speed)
        self.rect.center = self.loc
        self.header.rect.center = (self.rect.centerx, self.rect.top + 50)
        if self.winning_loot != None:
            self.winning_loot_label.rect.center = (self.rect.centerx, self.rect.top + self.rect.height * 0.25)
            self.winning_loot.rect.center = (self.rect.centerx, self.winning_loot_label.rect.centery + self.winning_loot_label.rect.height + 10)
        if self.power_gems_loot != None:
            self.power_gems_loot_label.rect.center = (self.rect.centerx, self.winning_loot.rect.bottom + self.winning_loot.rect.height)
            self.power_gems_loot.rect.center = (self.winning_loot.rect.centerx, self.power_gems_loot_label.rect.centery + self.power_gems_loot_label.rect.height + 10)
        if self.bonus_loot != None:
            self.bonus_loot.rect.center = self.rect.centerx, self.rect.top + (self.rect.height * 0.7)


class PreviewWindow:
    
    def __init__(self, image, pos):
        self.image = image
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.preview_info = dict()
        self.collected_power_stones = []
        self.previewing_saved_game = False
        
    def get_saved_game_info(self, game, connected_game, stats):
        # will get the player's currency and add them to the dictionary        
        # getting the last saved date and time
        self.preview_info['Header'] = Feedback(f'{stats["Rank"]}', ui_20_font, (self.rect.centerx, self.rect.top + (self.rect.height * 0.055)))
        self.preview_info['Last Saved Label'] = Feedback('Last Saved', ui_font, (self.rect.centerx, self.rect.top + (self.rect.height * 0.15)))
        self.preview_info['Last Saved Time'] = Feedback(f'{saved_games[connected_game]}', ui_font, (self.rect.centerx, self.preview_info['Last Saved Label'].rect.centery + (size_25_font * 1.5)))
        self.preview_info['Player Rank Label'] = Feedback('Rank', ui_font, (self.rect.centerx, self.rect.top + (self.rect.height * 0.28)))
        self.preview_info['Player Rank'] = Feedback(f'{stats["Rank"]}', ui_font, (self.rect.centerx, self.preview_info['Player Rank Label'].rect.centery + (size_25_font * 1.5)))
        self.preview_info['Player Space Crystals'] = Feedback(f'{stats["Space Crystals"]}', ui_30_font, (self.rect.centerx, self.rect.top + (self.rect.height * 0.52)))
        self.preview_info['Space Crystal Icon'] = Title(power_crystal, (self.preview_info['Player Space Crystals'].rect.left - power_crystal.get_width(), self.preview_info['Player Space Crystals'].rect.centery))
        self.preview_info['Player Power Gems'] = Feedback(f'{stats["Power Gems"]}', ui_30_font, (self.rect.centerx, self.preview_info['Player Space Crystals'].rect.centery + (size_25_font * 2)))
        self.preview_info['Power Gem Icon'] = Title(power_gem_image, (self.preview_info['Player Power Gems'].rect.left - power_gem_image.get_width(), self.preview_info['Player Power Gems'].rect.centery))
        self.preview_info['Lives Left Label'] = Feedback(f'Lives: {stats["Lives"]}', ui_font, (self.rect.centerx, self.preview_info['Player Power Gems'].rect.centery + (size_25_font * 2)))
        
    def get_power_stone_collection(self, stones):
        self.collected_power_stones.clear()
        x = (self.rect.left + self.rect.width * 0.16)
        y = (self.rect.top + (self.rect.height * 0.425))
        spacing = self.rect.width * 0.16
        for stone in stones:
            if stones[stone] > 0:
                if stone == 'Strength':
                    stone_image = red_power_stone_image
                    
                elif stone == 'Recovery':
                    stone_image = orange_power_stone_image
                    
                elif stone == 'Speed':
                    stone_image = yellow_power_stone_image
                    
                elif stone == 'Depletion':
                    stone_image = green_power_stone_image
                    
                elif stone == 'Freeze':
                    stone_image = blue_power_stone_image
                    
                if len(self.collected_power_stones) > 0:
                    s = Title(stone_image, (x + (spacing * len(self.collected_power_stones)), y))
                else:
                    s = Title(stone_image, (x, y))
                self.collected_power_stones.append(s)
        
    def get_power_stone_loot(self, level, stones):
        if level.num == 20:
            if stones['Strength'] == 0:
                self.preview_info['Loot Stone Chance'] = Feedback('75% Chance', ui_30_font, (self.rect.centerx, self.rect.top + (self.rect.height * 0.4)))
                self.preview_info['Loot Stone'] = PowerStone('Strength', red_power_stone_image, (self.preview_info['Loot Stone Chance'].rect.left - (red_power_stone_image.get_width() / 2), self.preview_info['Loot Stone Chance'].rect.centery), 1, 75)
                
        elif level.num == 30:
            if stones['Recovery'] == 0:
                self.preview_info['Loot Stone Chance'] = Feedback('50% Chance', ui_30_font, (self.rect.centerx, self.rect.top + (self.rect.height * 0.4)))
                self.preview_info['Loot Stone'] = PowerStone('Recovery', orange_power_stone_image, (self.preview_info['Loot Stone Chance'].rect.left - (orange_power_stone_image.get_width() / 2), self.preview_info['Loot Stone Chance'].rect.centery), 2, 50)
                
        elif level.num == 40:
            if stones['Speed'] == 0:
                self.preview_info['Loot Stone Chance'] = Feedback('25% Chance', ui_30_font, (self.rect.centerx, self.rect.top + (self.rect.height * 0.4)))
                self.preview_info['Loot Stone'] = PowerStone('Speed', yellow_power_stone_image, (self.preview_info['Loot Stone Chance'].rect.left - (yellow_power_stone_image.get_width() / 2), self.preview_info['Loot Stone Chance'].rect.centery), 5, 25)
                
        elif level.num == 60:
            if stones['Depletion'] == 0:
                self.preview_info['Loot Stone Chance'] = Feedback('10% Chance', ui_30_font, (self.rect.centerx, self.rect.top + (self.rect.height * 0.4)))
                self.preview_info['Loot Stone'] = PowerStone('Depletion', green_power_stone_image, (self.preview_info['Loot Stone Chance'].rect.left - (green_power_stone_image.get_width() / 2), self.preview_info['Loot Stone Chance'].rect.centery), 10, 10)
                
        elif level.num == 70:
            if stones['Freeze'] == 0:
                self.preview_info['Loot Stone Chance'] = Feedback('5% Chance', ui_30_font, (self.rect.centerx, self.rect.top + (self.rect.height * 0.4)))
                self.preview_info['Loot Stone'] = PowerStone('Freeze', blue_power_stone_image, (self.preview_info['Loot Stone Chance'].rect.left - (blue_power_stone_image.get_width() / 2), self.preview_info['Loot Stone Chance'].rect.centery), 15, 5)

        else:
            try:
                self.preview_info.pop('Loot Stone Chance')
                self.preview_info.pop('Loot Stone')
            except KeyError:
                pass

    def get_level_preview_info(self, stats, level):
        # will get the player's currency and and them to the dictionary        
        # getting the last saved date and time
        self.preview_info['Header'] = Feedback(f'Level {level.num}', upgrades_font, (self.rect.centerx, self.rect.top + (self.rect.height * 0.1)))
        self.preview_info['Number of Enemies'] = Feedback(f'Number of Enemies: {len(level.active_enemies)}', ui_30_font, (self.rect.centerx, self.rect.top + (self.rect.height * 0.28)))
        self.preview_info['Loot Rewarded Label'] = Feedback('Rewards', ui_30_font, (self.rect.centerx, self.rect.top + (self.rect.height * 0.5)))
        self.preview_info['Space Crystals Awarded'] = Feedback(f'{level.loot_drop()}', ui_30_font, (self.rect.centerx, self.preview_info['Loot Rewarded Label'].rect.bottom + (size_20_font * 1.5)))
        self.preview_info['Space Crystal Icon'] = Title(power_crystal, (self.preview_info['Space Crystals Awarded'].rect.left - power_crystal.get_width(), self.preview_info['Space Crystals Awarded'].rect.centery))
        self.preview_info['Power Gems Awarded'] = Feedback(f'{level.power_gem_loot()} - {level.power_gem_loot() + 100}', ui_30_font, (self.rect.centerx, self.preview_info['Space Crystals Awarded'].rect.centery + (size_25_font * 2)))       
        self.preview_info['Power Gem Icon'] = Title(power_gem_image, (self.preview_info['Power Gems Awarded'].rect.left - power_gem_image.get_width(), self.preview_info['Power Gems Awarded'].rect.centery))

    def set_confirm_delete_game_info(self):
        self.preview_info['Header'] = Feedback('Delete Game?', upgrades_font, (self.rect.centerx, self.rect.top + (self.rect.height * 0.1)))
        self.preview_info['Confirm Yes'] = Button(upgrades_stat_bar, (self.rect.centerx, self.rect.top + (self.rect.height * 0.6)), 'Yes', upgrades_font)
        self.preview_info['Confirm No'] = Button(upgrades_stat_bar, (self.rect.centerx, self.preview_info['Confirm Yes'].rect.centery + (self.preview_info['Confirm Yes'].rect.height * 1.2)), 'No', upgrades_font)

    def show_preview_info(self):
        screen.blit(self.image, self.rect)
        for info in self.preview_info:
            self.preview_info[info].show_to_player()
        if self.previewing_saved_game is True:
            for s in self.collected_power_stones:
                s.show_to_player()
        
                        
class Level:
 
    def __init__(self, image, num, num_of_types, enemy_types, button_pos, num_of_enemies, boss=None):
        self.image = image
        self.locked_image = locked_level_button_image
        self.rect = self.image.get_rect(center=button_pos)
        self.num = num
        self.enemy_types = enemy_types
        self.num_of_types = num_of_types 
        self.entry_button = Button(self.image, button_pos, num, ui_45_font)
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
        self.enemies_left_label = Feedback('Enemies Left:', ui_20_font, (screen_width / 2, size_15_font))
        self.enemies_left_num = Feedback('0', ui_20_font, (self.enemies_left_label.rect.right + size_20_font, self.enemies_left_label.rect.centery))
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
        if self.active_enemies[-1].is_boss is True:
            return True
        
    def get_boss(self):
        try:
            boss_name = list(k for k in enemy_boss_images.keys())[self.boss]
            image = enemy_boss_images[boss_name]
            return image
        except KeyError:
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
            self.entry_button.label.rect.center = self.entry_button.rect.center
            self.locked_button.rect.centerx = self.locked_button.rect.centerx
            self.scroll_amount = 0
        elif self.scroll_amount < 0:
            self.entry_button.rect.x -= self.scroll_amount
            self.locked_button.rect.x -= self.scroll_amount            
            self.entry_button.rect.centerx = self.entry_button.rect.centerx
            self.entry_button.label.rect.center = self.entry_button.rect.center
            self.locked_button.rect.centerx = self.locked_button.rect.centerx
            self.scroll_amount = 0
         
    def loot_drop(self):
        return int(self.num_of_enemies * 12.4 * self.num)       
     
    def enemies_left(self):
        return int(len(self.active_enemies) - self.current_spawn_index)
    
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
                
    def power_stone_loot(self, collected_stones, stone):
        loot_chances = []
        if collected_stones[stone.power] == 0:
            for i in range(stone.loot_chance):
                loot_chances.append(True)
            for j in range(100 - stone.loot_chance):
                loot_chances.append(False)
            random.shuffle(loot_chances)
            loot = random.choice(loot_chances)
            if loot is True:
                return stone
            else:
                return None 
               
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
                #rindex = self.enemy_types[names[types]]
                ry = random.randint(player_base.rect.top + 40, player_base.rect.bottom - 40)
                enemy = Enemy(enemy_ships[f'{names[types]}.png'], (screen_width + 100, ry), enemy_types[names[types]])
                queued_enemies.append(enemy)
        # Adding in the leftover amount of enemies
        # after getting an even amount of each type in num_of_types
        for each_leftover in range(self.num_of_enemies % self.num_of_types):
            random_filler = random.choice(queued_enemies)
            filler_enemy = Enemy(random_filler.image, random_filler.pos, random_filler.stats)
            queued_enemies.append(filler_enemy)
        random.shuffle(queued_enemies)
        if self.boss != None:
            keys = [k for k in enemy_boss_types.keys()]
            boss_image = enemy_boss_images[f'{keys[self.boss]}.png']
            e = Enemy(boss_image, (screen_width + boss_image.get_width() + 100, screen_height / 2), enemy_boss_types[keys[self.boss]])
            e.is_boss = True
            queued_enemies.append(e)
            self.boss_name = Feedback('Boss', upgrades_font, (screen_width / 2, 50))
        return queued_enemies
        
    def explode_reveal_power_stone(self, stone):
        x = -5
        y = -1
        # 10 power stones explode in an upward arch
        for i in range(10):
            s = PowerStone(stone.power, stone.image, stone.pos, stone.lives_granted, stone.loot_chance)
            project_pos = pygame.math.Vector2(stone.pos.x + x, stone.pos.y + y)
            s.projectile_velocity = s.set_projectile_velocity(project_pos)
            s.explode = True
            if i > 4:
                y += 1
            else:
                y -= 1
            x += 1 if x != 0 else 2
            power_stones_group.add(s)
            
        # 10 power stones explode in a downward arch
        x = -5
        y = -1
        for i in range(10):
            s = PowerStone(stone.power, stone.image, stone.pos, stone.lives_granted, stone.loot_chance)
            project_pos = pygame.math.Vector2((stone.pos.x + x, stone.pos.y + y))
            s.projectile_velocity = s.set_projectile_velocity(project_pos)
            s.explode = True
            if i > 4:
                y -= 1
            else:
                y += 1
            x += 1 if x != 0 else 2
            power_stones_group.add(s)
        
        
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
        
    def set_spawn_delay(self):
        if len(helper_turret_group) == 1:
            self.spawn_delay = 3.5
        elif len(helper_turret_group) == 2:
            self.spawn_delay = 3
        elif len(helper_turret_group) == 3:
            self.spawn_delay = 2.5
        elif len(helper_turret_group) == 4:
            self.spawn_delay = 2
        else:
            self.spawn_delay = 4
    
    def load(self, base):
        self.completed = False
        self.played_winning_sound = False
        self.played_defeated_sound = False
        self.notified_player_about_boss = False
        self.set_spawn_delay()
        #level['Paused'] = False
        self.active_enemies = self.generate_enemies()
        self.current_spawn_index = 0
        self.player_base_starting_health = base.stats['Health']
        self.enemies_left_num.update_var(f'{len(self.active_enemies) - self.current_spawn_index}')
        if base_shield.stats['Status'] == 'Active':
            if base_shield.health > 0:
                self.base_shield_starting_health = base_shield.health
                base_shield.health = base_shield.stats['Max Health']
            elif base_shield.health <= 0:
                base_shield.health = base_shield.stats['Max Health']
                self.base_shield_starting_health = base_shield.health
                base_group.add(base_shield)
        player_base.poisoned_amount = 0
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
        self.pos = pygame.math.Vector2(pos)
        self.icon_image = pygame.transform.scale_by(image, 0.5)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask.outline()
        self.electrocuted_image = electrocuted_base
        self.poisoned_mask_surf = self.mask.to_surface(setcolor='green', unsetcolor=(0,0,0,0))
        self.poisoned_mask_surf = pygame.transform.scale_by(self.poisoned_mask_surf, 1.01)
        self.rect = self.image.get_rect(center=self.pos)
        self.stats = stats
        self.lives = 5
        self.last_regen_time = time()
        self.poisoned = False
        self.poisoned_amount = 0
        self.poison_antidote_applied = False
        self.special_attack_used = False
        self.special_attack_in_use = 'None'
        self.special_attack_start_time = time()
        self.special_defense_start_time = time()
        self.special_defense_used = False
        self.special_defense_in_use = 'None'
        self.special_defense_duration = 30
        self.rapid_fire_delay = 1
        self.last_meteor_spawn_time = time()
        self.raining_comets_start_time = time()
        self.raining_comets_duration = 10
        self.last_comet_time = time()
        self.last_flare_deployed_time = time()
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
        self.selected_for_upgrade = False
        self.selected_mask = pygame.mask.from_surface(self.image)
        self.selected_mask_surf = self.selected_mask.to_surface(setcolor='yellow', unsetcolor=(0, 0, 0, 0)).convert_alpha()
            
    def update(self, container):
        if self.poison_antidote_applied is True:
            self.image = base_main
            self.poisoned_amount = 0
        if self.poisoned_amount > 0:
            self.poisoned_damage()
            self.image = poisoned_base
        if self.special_defense_in_use == 'Deflection':
            self.image = rubberized_base
        else:
            self.image = base_main 
        if self.stats['Health'] < self.stats['Max Health']:
            if level['Game Over'] is False:
                if self.stats['Health Regeneration'] == 'Active':
                    if self.electrified is False and self.poisoned_amount <= 0:
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
                
    def show(self):
        if self.selected_for_upgrade is True:
            self.show_selected_highlight()
        screen.blit(self.image, self.rect)
    
    def clicked(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
    
    def show_selected_highlight(self):
        offset = 1
        screen.blit(self.selected_mask_surf, (self.rect.x+offset, self.rect.y))
        screen.blit(self.selected_mask_surf, (self.rect.x-offset, self.rect.y))
        screen.blit(self.selected_mask_surf, (self.rect.x, self.rect.y+offset))
        screen.blit(self.selected_mask_surf, (self.rect.x, self.rect.y+offset))
        screen.blit(self.selected_mask_surf, (self.rect.x+offset, self.rect.y-offset))
        screen.blit(self.selected_mask_surf, (self.rect.x+offset, self.rect.y+offset))
        screen.blit(self.selected_mask_surf, (self.rect.x-offset, self.rect.y-offset))
        screen.blit(self.selected_mask_surf, (self.rect.x-offset, self.rect.y+offset))
    
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
            if self.stats['Health'] - 1 <= 0:
                self.stats['Health'] = 0
                self.poisoned_amount = 0              
            else:
                self.stats['Health'] -= 1
                self.poisoned_amount -= 1
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
            if type(e) == Enemy and e.is_boss is False:
                if e.rect.right < screen_width:
                    e.kill()
                    animations_group.add(Animation(impact_animation, 1, e.pos))
                    
    def meteor_shower(self):
        if time() - self.last_meteor_spawn_time >= 0.1:
            x = random.randint(self.rect.right + 10, screen_width - 10)
            player_bullet_group.add(Meteor(tan_meteor, (x, -100)))
            self.last_meteor_spawn_time = time()
            
    def cluster_shot(self, group):
        b = Bullet(cluster_laser_image, self.rect.center, base_turret.stats['Damage'], Turret.fire_speed)
        b.fired_by_player = True
        b.is_cluster = True
        group.add(b)
        
    def rain_comets(self):
        if time() - self.raining_comets_start_time < self.raining_comets_duration:
            if time() - self.last_comet_time > self.comet_delay:
                rx = random.randrange(100, int(screen_width * 0.9))
                comet = Comet(raining_comet_image, (rx, -200))
                player_bullet_group.add(comet)
                self.last_comet_time = time()
                
    def deploy_defense_flares(self):
        ry = random.randrange(self.rect.top, self.rect.bottom)
        defense_flare = Flare(laser_flare, self.pos, (self.rect.right, ry))
        defense_flare.fixed = True
        player_defenses_group.add(defense_flare)
        self.last_flare_deployed_time = time()
        
    def deflect_lasers(self, laser):
        laser.is_hostile = False
        laser.deflected = True
        laser.deflected_from_pos = pygame.math.Vector2(self.pos)
        
    def handle_special_attack_timer(self, cooldown, duration):
        if self.special_attack_used is True:
            if self.special_attack_in_use != 'None':
                if time() - self.special_attack_start_time >= duration:
                    self.special_attack_start_time = time()
                    self.special_attack_in_use = 'None'
                    self.rapid_fire_delay = 1
                    rapid_fire_button.remaining_uses.update_var(f'{special_attacks_stats_table.dict["Rapid Fire"]}')
                    cluster_shot_button.remaining_uses.update_var(f'{special_attacks_stats_table.dict["Cluster Shots"]}')
                    meteor_shower_button.remaining_uses.update_var(f'{special_attacks_stats_table.dict["Meteor Shower"]}')
                    raining_comets_button.remaining_uses.update_var(f'{special_attacks_stats_table.dict["Raining Comets"]}')
                    vaporize_button.remaining_uses.update_var(f'{special_attacks_stats_table.dict["Vaporizers"]}')
            elif self.special_attack_in_use == 'None':
                if time() - self.special_attack_start_time >= cooldown:
                    self.special_attack_used = False
                
    def handle_special_defense_timer(self, cooldown, duration):
        if self.special_defense_used is True:
            if self.special_defense_in_use != 'None':
                if time() - self.special_defense_start_time > duration:
                    self.special_defense_start_time = time()
                    self.special_defense_in_use = 'None'
                    self.poison_antidote_applied = False
                    self.absorb_electric_shock = False
                    shock_absorber_button.remaining_uses.update_var(f'{special_defenses_stats_table.dict["Shock Absorbers"]}')
                    poison_antidote_button.remaining_uses.update_var(f'{special_defenses_stats_table.dict["Poison Antidote"]}')
                    flares_defense_button.remaining_uses.update_var(f'{special_defenses_stats_table.dict["Flares"]}')
                    deflection_defense_button.remaining_uses.update_var(f'{special_defenses_stats_table.dict["Deflection"]}')
                    magnetic_mine_button.remaining_uses.update_var(f'{special_defenses_stats_table.dict["Magnetic Mine"]}')
            elif self.special_defense_in_use == 'None':
                if time() - self.special_defense_start_time >= cooldown:
                    self.special_defense_used = False
         
        
                        
class Shield(pygame.sprite.Sprite):
   
    def __init__(self, image, loc, stats):
        super().__init__()
        self.image = pygame.transform.scale(image, (base_main.get_width() + 50, base_main.get_height() + 50))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=loc)
        self.stats = stats
        self.health = self.stats['Max Health']
        self.last_regen_time = time()
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
        
    def show(self):
        if self.image.get_alpha() > 0:
            img_alpha = self.image.get_alpha()
            self.image.set_alpha(img_alpha - 3)
        if self.health <= 0:
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
        if self.active is True and self.connected_ship.alive():
            if pygame.sprite.spritecollide(self, player_bullet_group, False):
                if pygame.sprite.spritecollide(self, player_bullet_group, False, pygame.sprite.collide_mask):
                    for b in pygame.sprite.spritecollide(self, player_bullet_group, True, pygame.sprite.collide_mask):
                        #if b.mask.overlap(self.mask, (self.rect.x - b.rect.x, self.rect.y - b.rect.y)):                                                 #b.kill()
                            #pygame.sprite.spritecollide(self, player_bullet_group, True, pygame.sprite.collide_mask)
                            self.take_damage(b.damage)
                            #b.kill()
        if self.connected_ship.alive() is False:
            self.kill()
        self.show()     
        self.rect.center = self.connected_ship.pos
        
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
                screen.blit(self.image, self.rect)
                if self.health < self.max_health:
                    self.show_health()
        
    def activate(self):
        self.active = True
        self.health = self.max_health
        self.image.set_alpha(255)
        
    def take_damage(self, amount):
        if self.health - amount <= 0:
            self.health = 0
            self.active = False
            self.kill()
        else:
            self.health -= amount
        self.image.set_alpha(255)
        
        
class StatsContainer:
            
    def __init__(self, image, pos):
        self.image = image
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.outline_timer_rect = pygame.Rect(self.rect.left + (self.rect.width * 0.1), self.rect.top - 20, self.rect.width * 0.8, 10)
        self.baseline_timer_rect = pygame.Rect(self.outline_timer_rect.left + 2, self.outline_timer_rect.top + 2, self.outline_timer_rect.width - 4, 6)
        self.solid_timer_rect = pygame.Rect(self.baseline_timer_rect.left, self.baseline_timer_rect.top, self.baseline_timer_rect.width, 6)
                
    def show_timer(self, state, start_time, duration, cooldown):
        if state != 'None':
            try:
                width_diff = (duration - (time() - start_time)) / duration
            except ZeroDivisionError:
                width_diff = 1
                pass
            if (time() - start_time) < duration:
#                self.solid_timer_rect.width = 0
#            else:
                self.solid_timer_rect.width = self.baseline_timer_rect.width * width_diff
        elif state == 'None':
            try:
                width_diff = (time() - start_time) / cooldown
            except ZeroDivisionError:
                width_diff = 1
                pass
            if time() - start_time < cooldown:
                self.solid_timer_rect.width = self.baseline_timer_rect.width * width_diff
            else:
                self.solid_timer_rect.width = self.baseline_timer_rect.width
                       
        pygame.draw.rect(screen, 'green', self.solid_timer_rect, border_radius=10)
        pygame.draw.rect(screen, 'blue', self.outline_timer_rect, 2, border_radius=10)
        
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
        self.upgrading_image = image
        self.manipulated_electrocuted_image = electrocuted_turret        
        self.electrocuted_image = electrocuted_turret
        self.frozen_image = frozen_turret_image
        self.mask = pygame.mask.from_surface(self.upgrading_image)
        self.mask_surf = self.mask.to_surface(setcolor='yellow', unsetcolor=(0, 0, 0, 0)).convert_alpha()
        self.updated_rect = self.updated_image.get_rect(center=pygame.math.Vector2(pos))
        self.upgrading_rect = self.upgrading_image.get_rect(center=pygame.math.Vector2(pos))
        self.idle_rect = self.idle_image.get_rect(center=pygame.math.Vector2(pos))
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.stats = stats
        self.full_range = screen_width - player_base.rect.right
        self.last_shot_time = time()
        self.selected_for_upgrade = False
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
        self.frozen = False
        self.frozen_start_time = time()
        self.frozen_time_duration = 10
        
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
        if self.paralyzed is True or self.frozen is True:
            self.attack = False
            
    def draw_for_upgrades(self):
        if self.selected_for_upgrade is True:
            self.show_selected_highlight()
        screen.blit(self.upgrading_image, self.upgrading_rect)
        
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
        elif self.frozen is True:
            self.attack = False
            if 0 < time() - self.frozen_start_time < self.frozen_time_duration:
                screen.blit(self.frozen_turret, self.idle_rect)
            if time() - self.frozen_start_time >= self.frozen_time_duration:
                self.frozen = False
                
    def show_selected_highlight(self):
        offset = 3
        screen.blit(self.mask_surf, (self.upgrading_rect.x+offset, self.upgrading_rect.y))
        screen.blit(self.mask_surf, (self.upgrading_rect.x-offset, self.upgrading_rect.y))
        screen.blit(self.mask_surf, (self.upgrading_rect.x, self.upgrading_rect.y+offset))
        screen.blit(self.mask_surf, (self.upgrading_rect.x, self.upgrading_rect.y+offset))
        screen.blit(self.mask_surf, (self.upgrading_rect.x+offset, self.upgrading_rect.y-offset))
        screen.blit(self.mask_surf, (self.upgrading_rect.x+offset, self.upgrading_rect.y+offset))
        screen.blit(self.mask_surf, (self.upgrading_rect.x-offset, self.upgrading_rect.y-offset))
        screen.blit(self.mask_surf, (self.upgrading_rect.x-offset, self.upgrading_rect.y+offset))
        
    def clicked(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
    
    def target_in_range(self):
        if 'Range %' in self.stats:
            if abs(self.target.pos.x - player_base.rect.right) <= (self.stats['Range %'] / 100) * self.full_range:
                return True      
        
    def set_idle_image(self, img, angle):
        self.idle_image = pygame.transform.rotate(self.image, angle - 90)
        self.electrocuted_image = pygame.transform.rotate(self.manipulated_electrocuted_image, angle - 90)
        self.frozen_turret = pygame.transform.rotate(frozen_turret_image, angle - 90)
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
        if time() - self.last_shot_time >= self.stats['Cooldown (secs)'] / level['Speed']:
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
        self.teleporter = False
        self.last_teleport_time = time()
        self.last_flare_deploy_time = time()
        
    def update(self, dt):
        self.fire_at_player()
        self.hit_by_player()
        if self.teleporter is True:
            if time() - self.last_teleport_time >= 2:
                self.teleport()
        if self.stats['Health'] < self.max_health:
            self.show_health()
        if self.stats['Health'] <= 0:
            self.kill()
            
    def teleport(self):
        animations_group.add(Animation(impact_animation, 1, self.pos))
        if self.pos.y < self.target.pos.y:
            self.pos.y += screen_width * 0.25
        elif self.pos.y > self.target.pos.y:
            self.pos.y -= screen_width * 0.25
        self.aim_at(self.target)
        self.rect.center = self.pos
        animations_group.add(Animation(impact_animation, 1, self.pos))
            
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
                b.set_velocity(self.target.pos)
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
        self.shield_group = pygame.sprite.GroupSingle()
        self.shield = self.create_shield()
        self.shot_duration = 0
        self.last_shot_time = time()
        self.last_stinger_shot_time = time()
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
        self.is_boss = False
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
                             
        if self.health < self.max_health and self.is_boss is False:
            self.show_health()
            
        # Checking if enemy type is a boss
        if self.is_boss is True:           
                if self.stats['Special'] == 'Spawn Turrets':
                # Boss number 2 firing Special shot
                    if self.pos.x < screen_width + 100:
                        if self.special_fires == 0:
                            self.spawn_turret_shot()
                            self.turret_spawn_time = time()
                            self.special_fires += 1
                                                    
                elif self.stats['Special'] == 'Drones':
                # Boss number 3 spawns mini drones to attack
                    if self.rect.left < screen_width:
                        if self.num_of_drones < self.drone_spawns:
                            if time() - self.last_shot_time >= 0.25:
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
                                    self.fire_side_missile()
                                    self.last_missile_shot_time = time()
                                    
                            # Boss will re-engage missile launchers
                            if time() - self.engage_missiles_time >= self.engage_missiles_duration + self.reengage_missiles_delay:
                                self.engage_missiles_time = time()
                                
                if self.stats['Special'] == 'Laser Deflection':
                    #self.deflect_lasers()
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
                                self.fire_laser_beam()
                             
                # Boss number 9 shoots out electric bolts every 5 seconds
                # Boss will shoot out Missiles in between shooting out bolts
                if self.stats['Special'] == 'Stinger':
                    if self.in_range(player_base):
                        if player_base.stats['Health'] > 0:
                            if time() - self.turret_spawn_time >= 20:
                                self.spawn_firing_orbs()
                                self.turret_spawn_time = time()
                            if time() - self.last_missile_shot_time >= 1:
                                self.fire_side_missiles()
                                self.last_missile_shot_time = time()
                            if time() - self.last_stinger_shot_time >= self.cooldown * 2:
                                self.shoot_stinger_bolts()
                                self.last_stinger_shot_time = time()
            
        if self.health <= 0:
            self.kill()
            animations_group.add(Animation(ship_explosion, 2.5, self.pos, ship_explosion_sound))
            if self.stats['Special'] == 'Hydra Spawn':
                self.hydra_spawn()
            elif self.stats['Special'] == 'Bomb Drop':
                self.drop_bomb()
                                 
        if self.moving is True:            
            if self.black_hole_death is True and self.black_hole.alive():
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
                if pygame.sprite.spritecollide(self, player_bullet_group, False):
                    self.fire()
                    self.teleport()
                    self.last_teleport_time = time()
            
        # Self healing ship
        if self.stats['Special'] == 'Health Regeneration':
            self.regenerate_health()
        
        if self.stats['Special'] == 'Linger Flares':
            if self.in_range(player_base):
                if time() - self.last_flare_deploy_time > 0.1:
                    self.deploy_flares()
                            
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
                        self.deploy_flares()
                                                       
        # Enemy is within range to shoot
        if not self.in_range(player_base):
            self.moving = True        
        elif self.in_range(player_base):
            self.moving = False
            if self.black_hole_death is True and self.black_hole.alive():
                self.pos.move_towards_ip(self.black_hole.pos, 5)
                self.rect.center = self.pos
            
            if self.stats['Special'] == 'Tanker Delivery':
                if self.tanks_delivered < 5:
                    if time() - self.tank_spawn_time >= 10 and player_base.stats['Health'] > 0:
                        animations_group.add(Animation(spawn_animation, 2, self.pos))
                        enemy_group.add(Enemy(enemy_ships['Acid Tanker.png'], self.pos, enemy_types['Acid Tanker']))
                        self.tank_spawn_time = time()
                        self.tanks_delivered += 1
                    
            # Healer ship
            elif self.stats['Special'] == 'Radial Healing':
                if self.healing_ring_engaged is False:
                    self.engage_healing_ring()
                    self.healing_ring_engaged = True                                

            # Enemy firing attacks
            if time() - self.last_shot_time >= self.cooldown / level['Speed']:
                if player_base.stats['Health'] > 0:
                    if self.stats['Special'] == 'Double Shot':
                        self.double_shot()
                    elif self.stats['Special'] == 'Triple Shot':
                        self.triple_shot()
                    elif self.stats['Special'] == 'Poison Laser':                  
                        self.poison_shot(self.damage)
                    elif self.stats['Special'] == 'Shield Destroy':
                        if base_shield.health > 0:
                            self.destroy_shield_shot()
                        else:
                            self.fire()
                    elif self.stats['Special'] == 'Wave Blast':
                        self.wave_blast()
                    elif self.stats['Special'] == 'Speed Shot':
                        self.fire_speed = 500
                        self.fire()
                    elif self.stats['Special'] == 'Missile Shot':
                        self.fire_missile()
                    elif self.stats['Special'] == 'Charge Bolt':
                        self.emit_charge_bolt()
                    elif self.stats['Special'] == 'Cluster Bomb':
                        self.cluster_bombs()
                    else:
                        self.fire()                            
                    self.last_shot_time = time()
                
        self.recovery_collision()
          
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def take_damage(self, amount):
        if self.health - amount <= 0:
            self.health = 0
        else:
            self.health -= amount 
    
    def in_range(self, base):
        if abs((self.pos.x - self.image.get_width() / 2) - player_base.rect.right) <= self.range:
            return True
            
    def recovery_collision(self):
        if pygame.sprite.spritecollide(self, health_flares_group, False):
            collisions = pygame.sprite.spritecollide(self, health_flares_group, False, pygame.sprite.collide_mask)
            if collisions:
                for c in collisions:
                    if c.mini is False and self.healer is False:
                        self.regenerate_health()
                        
    def paralyze_turret(self):
        froze_turret = False
        for h in helper_turret_group:
            if froze_turret is True:
                break
            elif froze_turret is False:
                if h.frozen is False:
                    pygame.draw.line(screen, 'cyan', self.pos, h.pos, 5)
                    h.frozen = True
                    h.frozen_start_time = time()
                    froze_turret = True
                    break
                         
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
        
    #def deflect_lasers(self):
#        if pygame.sprite.spritecollide(self, player)
        
    def emit_charge_bolt(self):
        cb = ChargeBolt(charge_bolt_image, self.pos, self.damage)
        enemy_bullet_group.add(cb)
        
    def shoot_stinger_bolts(self):
        top_bolt = ChargeBolt(charge_bolt_image, (self.pos.x, self.rect.top + (self.rect.height * 0.3)), self.damage)
        bottom_bolt = ChargeBolt(charge_bolt_image, (self.pos.x, self.rect.top + (self.rect.height * 0.7)), self.damage)
        enemy_bullet_group.add(top_bolt, bottom_bolt)
          
    def fire_laser_beam(self):
        b = Laser(solid_laser_image, self.rect.center, self.damage)
        enemy_bullet_group.add(b)
        
    def fire_missile(self):
        b = Missile(side_missile_image, self.pos, self.damage * 1.5,  self.fire_speed)
        b.threshold = pygame.math.Vector2((b.pos.x - 10, b.pos.y))
        b.target = pygame.math.Vector2(player_base.rect.center)
        enemy_bullet_group.add(b)
        
    def fire_side_missiles(self):
        if self.missile_launcher_engaged == 'Top':
            b = Missile(side_missile_image, (self.pos.x, self.pos.y - 90), self.damage * 1.5,  self.fire_speed)
            self.missile_launcher_engaged = 'Bottom'
        elif self.missile_launcher_engaged == 'Bottom':
            b = Missile(side_missile_image, (self.pos.x, self.pos.y + 90), self.damage * 1.5,  self.fire_speed)
            self.missile_launcher_engaged = 'Top'
        b.threshold = pygame.math.Vector2((b.pos.x - 10, b.pos.y))
        b.target = pygame.math.Vector2(player_base.rect.center)
        enemy_bullet_group.add(b)
        
    def fire_side_missile(self):
        if self.missile_launcher_engaged == 'Top':
            b = Missile(side_missile_image, (self.pos.x + 90, self.pos.y - 90), self.damage * 1.5,  self.fire_speed)
            self.missile_launcher_engaged = 'Bottom'
        elif self.missile_launcher_engaged == 'Bottom':
            b = Missile(side_missile_image, (self.pos.x + 90, self.pos.y + 90), self.damage * 1.5,  self.fire_speed)
            self.missile_launcher_engaged = 'Top'
        b.threshold = pygame.math.Vector2((b.pos.x - 10, b.pos.y))
        b.target = pygame.math.Vector2(player_base.rect.center)
        enemy_bullet_group.add(b)
                
    def teleport(self):
        animations_group.add(Animation(impact_animation, 1, self.pos))
        self.pos.x += random.randint(150, 200)
        self.pos.y = random.randrange(int(player_base.rect.top + (self.rect.height / 2)), int(player_base.rect.bottom - self.rect.height / 2))
        self.rect.center = self.pos
        animations_group.add(Animation(impact_animation, 1, self.pos))
        
    def spawn_drone_shot(self):
        y = (player_base.rect.top + 50) + (50 * self.num_of_drones+1)
        orb = SpawnOrb(turret_spawn_orb, self.pos, (screen_width / 2, y))
        orb.spawn_item = Enemy(self.image, orb.spawn_pos, self.stats.copy())
        spawn_orb_group.add(orb)
        
    def spawn_firing_orbs(self):
        orb1 = SpawnOrb(turret_spawn_orb, self.pos, (screen_width * 0.4, self.rect.top))
        orb2 = SpawnOrb(turret_spawn_orb, self.pos, (screen_width * 0.4, self.rect.bottom))
        orb1.spawn_item = Bullet(enemy_turret_laser, orb1.pos, (self.damage * 0.75), self.fire_speed)
        orb2.spawn_item = Bullet(enemy_turret_laser, orb2.pos, (self.damage * 0.75), self.fire_speed)
        spawn_orb_group.add(orb1, orb2)
        
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
            enemy_shields_group.add(shield)
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
        b = Bullet(destroy_shield_laser, self.rect.center, base_shield.health, self.fire_speed)
        b.is_hostile = True
        enemy_bullet_group.add(b)
        
    def wave_blast(self):
        b = Bullet(wave_blast_image, (self.rect.centerx - 25, self.rect.centery), self.damage, self.fire_speed)
        b.is_hostile = True
        b.wave_blast = True 
        enemy_bullet_group.add(b)
        
    def deploy_flares(self):
        flared_pos = pygame.math.Vector2(self.rect.left - 10, random.randint(self.rect.top, self.rect.bottom))
        b = Flare(laser_flare, self.pos, flared_pos)
        b.fixed = True
        b.is_hostile = True
        enemy_flares_group.add(b)
        self.last_flare_deploy_time = time()
        
    def hydra_spawn(self):
         if self.alive() is False:
             new_ship = enemy_ships['Stingumplyer.png']
             new_stats = enemy_types['Stingumplyer']
             spawn_offset = 50
             enemy_group.add(Enemy(new_ship, (self.pos.x, self.pos.y - (spawn_offset / 2)), new_stats))
             enemy_group.add(Enemy(new_ship, (self.pos.x, self.pos.y + (spawn_offset / 2)), new_stats))
                       
    def drop_bomb(self):
        b = Bomb(enemy_rubble_bomb, self.rect.center, self.damage * 2, 80)
        b.is_hostile = True
        b.set_velocity(self.pos)
        enemy_bullet_group.add(b)
        
    def cluster_bombs(self):
        y_moves = [0.1, 0, -0.1]
        for y in y_moves:
            b = Bomb(enemy_rubble_bomb, self.rect.center, self.damage * 2, 80)
            b.is_hostile = True
            b.set_velocity(pygame.math.Vector2(self.pos.x, self.pos.y + y))
            enemy_bullet_group.add(b)
        
        
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
         self.last_shot_time = time()
         self.creation_time = time()
          
    def update(self, self_group):
        if self.traveling is False:
            if self.ready_to_spawn():
                
                if type(self.spawn_item) == EnemyTurret:
                    animations_group.add(Animation(spawn_animation, 3, self.pos))
                    enemy_group.add(EnemyTurret(turret_extra, self.pos, enemy_turret_stats.copy()))
                    self.kill()
                elif type(self.spawn_item) == Enemy:
                    animations_group.add(Animation(spawn_animation, 3, self.pos))
                    boss_image = game['Current Level'].get_boss()
                    boss_stats = game['Current Level'].get_boss_stats()
                    drone = self.spawn_drone(boss_image, boss_stats)
                    enemy_group.add(drone)
                    self.kill()
                elif type(self.spawn_item) == Bullet:
                    if time() - self.last_shot_time >= 0.5:
                        self.fire_lasers()
                        self.last_shot_time = time()
                    if time() - self.stopped_traveling_time >= 10:
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
             
    def fire_lasers(self):
        b = Bullet(enemy_turret_laser, self.rect.center, 2000, 550)
        #b.is_hostile = True
        b.shot_from_orb = True
        b.set_velocity(player_base.pos)
        b.locate_target(player_base.pos)
        enemy_bullet_group.add(b)
    
    def spawn_drone(self, image, stats):
        drone = pygame.transform.scale_by(image, 0.25)
        return Enemy(drone, self.pos, stats)     
         
    def ready_to_spawn(self):
        if time() - self.stopped_traveling_time >= 1:
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
        self.deflect = False
        self.deflected = False
        self.deflected_from_pos = None
        self.flare_x = 0
        self.flare_y = 0
        self.flare_id = 0
        self.flared_pos = pygame.math.Vector2(self.pos)
        self.hits = 5
        self.spray = False
        self.velocity_vector = None
        self.creation_time = time()
        self.shot_from_orb = False
        
    def update(self):    
        if self.fired_by_player is True:
            if self.velocity_vector == None:      
                self.locate_target(pygame.mouse.get_pos())
                self.set_velocity(pygame.mouse.get_pos())    
            self.pos.x += self.velocity_vector.x * game['Delta Time'] * level['Speed']
            self.pos.y += self.velocity_vector.y * game['Delta Time'] * level['Speed']
        if self.fired_by_helper is True:
            if self.velocity_vector == None:
                self.locate_target(self.target.pos)
                self.set_velocity(self.target.pos)
            self.pos.x += self.velocity_vector.x * game['Delta Time'] * level['Speed']
            self.pos.y += self.velocity_vector.y * game['Delta Time'] * level['Speed']
                    
        if self.is_cluster is True and self.pos.distance_to(player_base.pos) >= player_base.rect.width / 2:
            self.form_cluster(player_bullet_group)           
            
        if self.is_hostile is True:
            #if self.deflected is True:
#                if self.deflected_from_pos == None:
#                    self.ricochet()
#                self.pos.x += self.velocity_vector.x * game['Delta Time']
#                self.pos.y += self.velocity_vector.y * game['Delta Time']
            #if self.deflected is False:
            self.pos.x -= self.fire_speed * game['Delta Time'] * level['Speed']
            
            if self.wave_blast is True:
                self.force_push()   
                
        if self.shot_from_orb is True:
            self.pos.x += self.velocity_vector.x * game['Delta Time'] * level['Speed']
            self.pos.y += self.velocity_vector.y * game['Delta Time'] * level['Speed']
                
        if self.deflected is True:
            if self.deflect is False:
                self.ricochet()
                self.deflect = True
            self.pos.x -= self.velocity_vector.x * game['Delta Time'] * level['Speed']
            self.pos.y -= self.velocity_vector.y * game['Delta Time'] * level['Speed']

        if self.rect.centerx < -10 or self.rect.centerx > screen_width or \
        self.rect.centery < 0 or self.rect.centery > screen_height:
            self.kill()
            
        # update position of image rect to match pos
        self.rect.center = self.pos
                   
    def locate_target(self, target_pos):
        # finds target and rotates image to point at target position
        x_dist = target_pos[0] - self.pos.x
        y_dist = -(target_pos[1]- self.pos.y)
        angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.image, angle - 90)
        self.rect = self.image.get_rect(center = self.rect.center)
        
    def set_velocity(self, target_pos):
        if self.fired_by_helper is True:
            pos = pygame.math.Vector2(target_pos)
            distance = pygame.math.Vector2(self.rect.center).distance_to(pos)
            vx = self.fire_speed * (target_pos.x - self.pos.x) / distance
            vy = self.fire_speed * (target_pos.y - self.pos.y) / distance
            self.velocity_vector = pygame.math.Vector2(vx, vy)
        elif self.is_hostile is True:
            pos = pygame.math.Vector2(target_pos)
            distance = pygame.math.Vector2(self.rect.center).distance_to(pos)
            vx = self.fire_speed * (target_pos.x - self.pos.x) / distance
            vy = self.fire_speed * (target_pos.y - self.pos.y) / distance
            self.velocity_vector = pygame.math.Vector2(vx, vy)
        elif self.cluster is True:
            self.set_flare()
            distance = pygame.math.Vector2(self.rect.center).distance_to(self.flared_pos)
            vx = self.fire_speed * (self.flared_pos.x - self.pos.x) / distance
            vy = self.fire_speed * (self.flared_pos.y - self.pos.y) / distance
            self.velocity_vector = pygame.math.Vector2(vx, vy)
            self.locate_target((self.flared_pos.x, self.flared_pos.y))
        else:
            pos = pygame.math.Vector2(target_pos)
            distance = pygame.math.Vector2(self.rect.center).distance_to(pos)
            vx = self.fire_speed * (pos.x - self.pos.x) / distance
            vy = self.fire_speed * (pos.y - self.pos.y) / distance
            self.velocity_vector = pygame.math.Vector2(vx, vy)
            
    def force_push(self):
        if pygame.sprite.spritecollide(self, player_bullet_group, False):
            for b in pygame.sprite.spritecollide(self, player_bullet_group, False, pygame.sprite.collide_mask):
                if self.mask.overlap(b.mask, (b.rect.x - self.rect.x, b.rect.y - self.rect.y)):
                    b.kill()
                    self.hits -= 1
                    if self.hits == 0:
                        self.kill()
                        
    def ricochet(self):
        x_dist = self.deflected_from_pos.x - self.pos.x
        y_dist = -(self.deflected_from_pos.y - self.pos.y)
        angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center = self.rect.center)
        #self.fire_speed *= 0.7
        self.set_velocity(player_base.rect.center)
                        
    def set_flare(self):
        self.flare_x = random.randint(self.rect.right, self.rect.right + 100)
        self.flare_y = random.randint(self.rect.top, self.rect.bottom)
        self.flared_pos = pygame.math.Vector2(self.flare_x, self.flare_y)
   
    def flare_out(self):
        move_speed = self.fire_speed / 2 * game['Delta Time'] * level['Speed']
        self.pos.move_towards_ip(self.flared_pos, 10)
        self.rect.center = self.pos
        
    def form_cluster(self, group):
        for i in range(6):
            b = Bullet(laser_cluster_image, self.rect.center, self.damage, self.fire_speed / 5)
            b.cluster = True
            b.fired_by_player = True
            if i % 2 == 0:
                b.set_velocity((self.pos.x + 1, self.pos.y + 1))
            else:
                b.set_velocity((self.pos.x + 1, self.pos.y - 1))
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
            for b in pygame.sprite.spritecollide(self, base_group, False, pygame.sprite.collide_mask):
                b.take_damage(self.damage)
                animations_group.add(Animation(ship_explosion, 2.5, self.pos, ship_explosion_sound))
                self.kill()
                
    def break_and_cluster(self):
        points = self.mask.outline(every=10)
        animations_group.add(Animation(ship_explosion, 2.5, self.pos, ship_explosion_sound))
        self.kill()
        cluster_image = pygame.transform.scale_by(self.image, 0.5)
        image_size = cluster_image.get_size()
        max_x_point = 0
        max_y_point = 0
        x_offset = 0
        y_offset = 0
        for point in range(5):
            cluster_bomb = Bomb(cluster_image, (self.pos.x, self.pos.y), self.damage * 0.75, self.fire_speed * 2)
            cluster_bomb.is_hostile = True
            cluster_bomb.can_cluster = False
            ry = random.choice([-0.2, 0.1, 0.2, -0.1])
            cluster_bomb.set_velocity(pygame.math.Vector2(self.pos.x - 1, (self.pos.y + ry)))  
            enemy_bullet_group.add(cluster_bomb)
            
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
    
    def __init__(self, image, pos):
        super().__init__()
        self.image = pygame.transform.rotate(image, random.randint(10, 250))
        self.rotated_image = image
        self.pos = pygame.math.Vector2(pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)
        self.damage = 1000
        self.speed = 300
        
    def update(self):
        self.pos.y += self.speed * game['Delta Time']
        self.rect.center = self.pos
        if self.rect.y > screen_height:
            self.kill()
                        

class Laser(pygame.sprite.Sprite):
               
    def __init__(self, image, pos, damage):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.damage = damage
        self.image = image
        self.rect = self.image.get_rect(center=self.pos)
        
    def update(self):
        self.pos.x -= 300 * game['Delta Time'] * level['Speed']
        self.rect.center = self.pos
        #self.check_collision_with_base(base_group)
        
    def check_collision_with_base(self, group):
        if pygame.sprite.spritecollide(self, group, False):
            for i in pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_mask):
                i.take_damage(self.damage)
                self.kill()                
                                                            
                    
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
            for player_object in pygame.sprite.spritecollide(self, base_group, False, pygame.sprite.collide_mask):
                player_object.take_damage(self.damage)
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
              
                                              
class MagneticMine(pygame.sprite.Sprite):
    
    def __init__(self, image, pos):
        super().__init__()
        self.self = self
        self.pos = pygame.math.Vector2(pos)
        self.rotated_image = image
        self.image = image
        self.creation_time = time()
        self.rect = self.image.get_rect(center=self.pos)
        self.duration = 20
        self.angle = 0
        self.speed = 50
        
    def update(self):
        self.image = pygame.transform.rotate(self.rotated_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)
        if self.angle <= -360:
            self.angle = 0
        else:
            self.angle -= 1
        self.engage_magnetic_pull()
        if time() - self.creation_time > self.duration:
            self.kill()
            
    def engage_magnetic_pull(self):
        affected_enemies = pygame.sprite.spritecollide(self, enemy_group, False, pygame.sprite.collide_circle_ratio(3))      
        collided_enemies = pygame.sprite.spritecollide(self, enemy_group, True, pygame.sprite.collide_mask)
        for enemy in affected_enemies:           
            enemy.black_hole_death = True
            enemy.black_hole = self.self
        for enemy in collided_enemies:
            animations_group.add(Animation(ship_explosion, 2.5, enemy.pos))
   

class Flare(pygame.sprite.Sprite):
    
    def __init__(self, image, pos, end_pos):
        super().__init__()
        self.image = image
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.flare_pos = pygame.math.Vector2(end_pos)
        self.start_time = time()
        self.duration = 20
        self.speed = 100
        self.velocity = self.set_velocity()
        self.recovery_amount = 250
        self.is_hostile = False 
        self.mini = False
        self.fixed = False
        
    def update(self):            
        if self.fixed is False:
            self.pos.x += self.velocity.x * game['Delta Time'] * level['Speed']
            self.pos.y += self.velocity.y * game['Delta Time'] * level['Speed']
            if time() - self.start_time >= self.duration / 2:
                self.kill()
            
        elif self.fixed is True:
            self.pos.move_towards_ip(self.flare_pos, 10)
            if self.is_hostile is False:
                self.check_collisions(enemy_bullet_group)
            elif self.is_hostile is True:
                self.check_collisions(player_bullet_group)
            if time() - self.start_time >= self.duration:
                self.kill()          
        self.rect.center = self.pos
                
    def set_velocity(self):
        distance = pygame.math.Vector2(self.pos).distance_to(self.flare_pos)
        x_velocity = self.speed * (self.flare_pos.x - self.pos.x) / distance
        y_velocity = self.speed * (self.flare_pos.y - self.pos.y) / distance
        return pygame.math.Vector2((x_velocity, y_velocity))
        
    def check_collisions(self, group):
        if pygame.sprite.spritecollide(self, group, False):
            if pygame.sprite.spritecollide(self, group, True, pygame.sprite.collide_mask):
                self.kill()
                                     
                                
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
        self.rect.center = self.pos
         
            
class PowerStone(pygame.sprite.Sprite):
            
    def __init__(self, power, image, pos, lives_granted, loot_chance):
        super().__init__()
        self.power = power
        self.image = image
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.lives_granted = lives_granted
        self.loot_chance = loot_chance
        self.projectile_velocity = pygame.math.Vector2(0, 0)
        self.project_to_pos = pygame.math.Vector2(0, 0)
        self.projectile_speed = 350
        self.explode = False
        self.static = False
                              
    def update(self):
        if self.explode is True:
            self.explode_outward()
            if self.pos.x < 0 or self.pos.x > screen_width or \
            self.pos.y < 0 or self.pos.y > screen_height:
                self.kill()
                
    def show_to_player(self):
        screen.blit(self.image, self.rect)
                
    def explode_outward(self):
        self.pos.x += self.projectile_velocity.x * game['Delta Time']
        self.pos.y += self.projectile_velocity.y * game['Delta Time']
        self.rect.center = self.pos 
    
    
    def set_projectile_velocity(self, pos):
        distance = pygame.math.Vector2(self.pos).distance_to(pos)
        x_velocity = self.projectile_speed * (pos[0] - self.pos.x) / distance
        y_velocity = self.projectile_speed * (pos[1] - self.pos.y) / distance
        return pygame.math.Vector2((x_velocity, y_velocity))        

                

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
                           'Range': 700,
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
                           'Speed': 25,
                           'Special': 'Shield Destroy',
                           'Shield': True},
                       
               'Flanker': {'Health': 40000,
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
                          
           'Uni-Bomber': {'Health': 550000,
                          'Damage': 2500,
                          'Shot Cooldown': 7,
                          'Range': 430,
                          'Speed': 55,
                          'Special': 'Bomb Shot',
                          'Shield': True},
                          
           'Missile Launcher': {'Health': 650000,
                               'Damage': 5000,
                               'Shot Cooldown': 15,
                               'Range': 400,
                               'Speed': 50,
                               'Special': 'Missile Shot',
                               'Shield': True},
                               
           'Blubber Bomber': {'Health': 800000,
                              'Damage': 7500,
                              'Shot Cooldown': 5,
                              'Range': 440,
                              'Speed': 50,
                              'Special': 'Cluster Bomb',
                              'Shield': True},
                              
           'Smart Destroyer': {'Health': 1000000,
                               'Damage': 15000,
                               'Shot Cooldown': 5,
                               'Range': 380,
                               'Speed': 80,
                               'Special': 'Turret Paralyzer',
                               'Shield': True},
                               
           'Ultimate Killer': {'Health': 5000000,
                               'Damage': 50000,
                               'Shot Cooldown': 5,
                               'Range': 650,
                               'Speed': 60,
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
                                        'Damage': 5000,
                                        'Shot Cooldown': 2,
                                        'Range': 700,
                                        'Speed': 50,
                                        'Special': 'Drones', # 1/10 damage amd health
                                        'Shield': True},
                                        
                        'Versawing': {'Health': 100000,
                                        'Damage': 7000,
                                        'Shot Cooldown': 2.5,
                                        'Range': 650,
                                        'Speed': 50,
                                        'Special': 'Side Missiles', # 1/10 Damage and health
                                        'Shield': True},
                                        
                        'Timodifier': {'Health': 150000,  # Boss will have 4 Turrets queued for launch
                                        'Damage': 12000,  # each turret will sit as a spawn_orb
                                        'Shot Cooldown': 4,  # in the 4 spots on the ship
                                        'Range': 500,     # each turret will launch after boss is in range and spawn every 5 secs
                                        'Speed': 60,      # each turret will teleport up and down every 2 secs
                                        'Special': 'Speed Turrets', # each turret will rotate towards
                                        'Shield': True},  # and fire at base every time it teleports
                                        
                        'Whoppur': {'Health': 300000,
                                        'Damage': 2500,
                                        'Shot Cooldown': 2.5,
                                        'Range': 400,
                                        'Speed': 50,
                                        'Special': 'TBA',
                                        'Shield': True},
                                        
                        'Godship': {'Health': 500000,
                                        'Damage': 5000,
                                        'Shot Cooldown': 3,
                                        'Range': 700,
                                        'Speed': 50,
                                        'Special': 'Gold Laser',
                                        'Shield': True,
                                        'Defense': 'Laser Immunity'}, # can only be destroyed with special attacks
                                        
                        'Vulcanizer': {'Health': 1000000,
                                        'Damage': 20000,
                                        'Shot Cooldown': 2.5,
                                        'Range': 400,
                                        'Speed': 50,
                                        'Special': 'Triple Charge Beam', # 3 Orbs charge up, meet in front middle and shoots out a massive charge
                                        'Shield': True},
                                        
                        'Stingeray': {'Health': 2000000,
                                        'Damage': 20000,
                                        'Shot Cooldown': 2.5,
                                        'Range': 400,
                                        'Speed': 50,
                                        'Special': 'Stinger',
                                        'Shield': True},
                                        
                        'Galactic Destroyer': {'Health': 1000000000,
                                        'Damage': 500000,
                                        'Shot Cooldown': 25,
                                        'Range': 400,
                                        'Speed': 50,
                                        'Special': 'TBA',
                                        'Shield': True}
}

enemy_names = np.array([t for t in enemy_types.keys()])
# Data dicts for level variables 
       
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
        'Load Game': False,
        'Loaded Game': None,
        'Preview Saved Game': False,
        'Confirm Delete Game': False,
        'Preview Level': False,
        'Upgrading Base': False,
        'Upgrading Shield': False,
        'Purchasing Special Attacks': False,
        'Purchasing Special Defenses': False,
        'Redeeming Power Stones': False}
        

# Player Stats
player_stats = {'Space Crystals': 0,
                'Power Gems': 0,
                'Lives': 10,
                'Rank': 'Cadet',
                'XP': 0}
                
player_ranks = {'Cadet': 500,
                'Trooper': 2000,
                'Technician':5000,
                'Specialist': 15000,
                'Commander': 20000}
                
player_collected_power_stones = {'Strength': 0,
                                 'Recovery': 0,
                                 'Speed': 0,
                                 'Depletion': 0,
                                 'Freeze': 0}

try:
    with open('saved_games.txt', 'r') as f:   
        saved_games = json.loads(f.readline())
        loaded_games = load_saved_games(saved_games)
except FileNotFoundError:
    saved_games = dict()
    loaded_games = np.array([])                
                                                
# Stats Menus

# Player's base stats
base_health_stats = {'Health': 5000,
                     'Max Health': 5000,
                     'Regen Cooldown (secs)': 5,
                     'Regen Amount': 20,
                     'Health Regeneration': 'Inactive'}
base_starting_stats = base_health_stats.copy()
base_health_stats_increase_amounts = [500, 1.2, 0.1, 1.1, 'Active']
base_health_stats_limits = np.array([999999999, 999999999, 0.5, 1000000, None])
                 
# Player's base Shield stats   
shield_stats = {'Status': 'Inactive',
                'Max Health': 5000,
                'Regen Cooldown (secs)': 5,
                'Regen Amount': 20,              
                'Health Regeneration': 'Inactive'}
shield_starting_stats = shield_stats.copy()
shield_stats_increase_amounts = ['Active', 1.2, 0.1, 1.1, 'Active']
shield_stats_limits = np.array([None, 999999999, 0.5, 1000000, 'Active'])
       
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
extra_turret_stats_increase_amounts = [1.15, 1.1, 0.1, 0.1, 1]
extra_turret_stats_limits = np.array([999999, 100, 0.5, 10, 25])

# Stats for special attacks
special_attacks_stats = {'Rapid Fire': 0,
                         'Cluster Shots': 0,
                         'Meteor Shower': 0,
                         'Raining Comets': 0,
                         'Vaporizers': 0}
special_attacks_stats_increase_amounts = [1, 1, 1, 1, 1]
special_attacks_stats_limits = np.array([1000, 1000, 1000, 1000, 1000])              
 
# Stats for special defenses                
special_defenses_stats = {'Shock Absorbers': 0,
                          'Poison Antidote': 0,
                          'Flares': 0,
                          'Deflection': 0,
                          'Magnetic Mine': 0}
special_defenses_stats_increase_amounts = [1, 1, 1, 1, 1]
special_defenses_stats_limits = np.array([1000, 1000, 1000, 1000, 1000]) 
     
# Upgrade Menus
base_health_upgrades = {'Repair': 1000,
                        'Max Health +': 2000,
                        'Regen Cooldown -': 10000,
                        'Regen Amount +': 15000,
                        'Health Regeneration': 50000}                
base_health_upgrades_increase_amounts = [1.05, 1.08, 1.09, 1.07, 1.0]    
                                    
shield_upgrades_options = {'Activate Shield': 50000,
                           'Shield Health +': 5000,
                           'Regen Cooldown -': 10000,
                           'Regen Amount +': 15000,
                           'Health Regeneration': 50000}              
shield_upgrade_increase_amounts = [1, 1.15, 1.1, 1.09, 1]
                         
main_turret_upgrades = {'Damage +': 1000,
                        'Critical Hit +': 2500,
                        'Critical Hit Chance': 3000,
                        'Special Cooldown': 5000,
                        'Add Turret': 500}                        
main_turret_upgrade_increase_amounts = [1.2, 1.09, 1.3, 1.1, 2]
                        
extra_turret_upgrades = {'Damage +': 1000,
                         'Range +': 1250,
                         'Cooldown -': 1500,
                         'Critical Hit +': 5000,
                         'Critical Hit Chance': 10000}                                                             
extra_turret_upgrades_increase_amounts = [1.2, 1.5, 1.1, 1.07, 1.25]
                         
special_attacks = {'Rapid Fire': 1000,
                   'Cluster Shot': 2000,                  
                   'Meteor Shower': 3000,
                   'Raining Comets': 5000,
                   'Vaporizer': 10000}
special_attacks_increase_amounts = [1, 1, 1, 1, 1]             

special_attacks_durations = {'Rapid Fire': 30,
                             'Cluster Shots': 0,
                             'Meteor Shower': 20,
                             'Raining Comets': 10,
                             'Vaporizers': 0,
                             'None': 0}
                                                                                             
special_defenses = {'Shock Absorber': 1000,
                    'Poison Antidote': 2000,
                    'Flares': 5000,
                    'Deflection': 10000,
                    'Magnetic Mine': 20000}
special_defenses_increase_amounts = [1, 1, 1, 1, 1]

special_defenses_durations = {'Shock Absorbers': 30,
                              'Poison Antidote': 30,
                              'Flares': 30,
                              'Deflection': 30,
                              'Magnetic Mine': 20,
                              'None': 0}

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
stats_table_pos = (screen_width - (menu_offset / 2), screen_height / 2)
base_stats_table = StatsTable('Health Stats', player_base.stats, base_health_stats_increase_amounts, base_health_stats_limits, stats_table_pos)
shield_stats_table = StatsTable('Shield Stats', base_shield.stats, shield_stats_increase_amounts, shield_stats_limits, stats_table_pos)
base_turret_stats_table = StatsTable('Main Turret', base_turret.stats, main_turret_stats_increase_amounts, main_turret_stats_limits, stats_table_pos)
extra_turret1_stats_table = StatsTable('Turret X1', extra_turret1.stats, extra_turret_stats_increase_amounts, extra_turret_stats_limits, stats_table_pos)
extra_turret2_stats_table = StatsTable('Turret X2', extra_turret2.stats, extra_turret_stats_increase_amounts, extra_turret_stats_limits, stats_table_pos)
extra_turret3_stats_table = StatsTable('Turret X3', extra_turret3.stats, extra_turret_stats_increase_amounts, extra_turret_stats_limits, stats_table_pos)
extra_turret4_stats_table = StatsTable('Turret X4', extra_turret4.stats, extra_turret_stats_increase_amounts, extra_turret_stats_limits, stats_table_pos)
special_attacks_stats_table = StatsTable('Supply', special_attacks_stats.copy(), special_attacks_stats_increase_amounts, special_attacks_stats_limits, stats_table_pos)
special_defenses_stats_table = StatsTable('Supply', special_defenses_stats.copy(), special_defenses_stats_increase_amounts, special_defenses_stats_limits, stats_table_pos)

# Upgrade Menu Tables
upgrade_menu_pos = (base_stats_table.rect.centerx - menu_offset, screen_height / 2)
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
power_stones_group = pygame.sprite.Group()

# Sprite groups for enemy attacks
enemy_group = pygame.sprite.Group()
enemy_shields_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
enemy_flares_group = pygame.sprite.Group()
healing_ring_group = pygame.sprite.Group()
health_flares_group = pygame.sprite.Group()
spawn_orb_group = pygame.sprite.Group()

# Game name title
game_title = NavButton(game_title_label_image, (screen_width / 2, screen_height * 0.35))

# Settings Title
settings_menu_title = Title(settings_menu_title_image, (screen_width / 2, settings_menu_title_image.get_height()))

# Saved Games Header
saved_games_title = Feedback('Saved Games', title_font, (screen_width / 2, size_50_font))

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
no_saved_games_message = Feedback('No Saved Games', big_font, (load_game_button.rect.centerx, load_game_button.rect.bottom + 50))
must_complete_previous_level_message = Feedback('Must Complete Previous Level', big_font, (screen_width / 2, screen_height / 2))

# Level Mini Menus
level_completed_menu = MiniMenu(level_over_menu, screen_middle, 'Level Complete')
level_defeated_menu = MiniMenu(level_over_menu, screen_middle, 'Level Failed')

# Paused Level menu
paused_level_menu = MiniMenu(level_over_menu, (screen_width / 2, screen_height / 2), 'Game Paused')

# Paused Level menu buttons
unpause_game_button = NavButton(resume_game_button_image, (paused_level_menu.rect.centerx, paused_level_menu.rect.centery - 50))
abandon_game_button = NavButton(exit_game_button_image, (paused_level_menu.rect.centerx, paused_level_menu.rect.centery + 50))

player_money_shrunken = Feedback(f'{int(player_stats["Space Crystals"])}', ui_30_font, (base_upgrades.rect.x / 2, screen_height * 0.87))
player_power_crystals_shrunken = Feedback(f'{player_stats["Power Gems"]}', ui_30_font, (player_money_shrunken.rect.centerx, player_money_shrunken.rect.bottom + size_30_font))

player_money_enlarged = Feedback(f'{int(player_stats["Space Crystals"])}', upgrades_font, (base_upgrades.rect.x / 2, screen_height * 0.45))
player_power_crystals_enlarged = Feedback(f'{player_stats["Power Gems"]}', upgrades_font, (player_money_enlarged.rect.centerx, player_money_enlarged.rect.centery + player_money_enlarged.rect.height + 20))

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

# Buttons for navigating between the different upgrades screens
base_upgrades_button = NavButton(base_upgrades_button_image, (screen_width * 0.33, screen_height / 2))
shield_upgrades_button = NavButton(shield_upgrades_button_image, (base_upgrades_button.rect.centerx, base_upgrades_button.rect.centery + base_upgrades_button.rect.height + 30))
special_attacks_button = NavButton(special_attacks_upgrades_button_image, (screen_width * 0.66, base_upgrades_button.rect.centery))
special_defenses_button = NavButton(special_defenses_upgrades_button_image, (special_attacks_button.rect.centerx, special_attacks_button.rect.centery + special_attacks_button.rect.height + 30))

# Navigation Buttons for going betweeen different screens
continue_level_button = Button(level_nav_button, (level_completed_menu.rect.centerx, level_completed_menu.rect.bottom - level_nav_button.get_height() - 5), 'Continue', ui_20_font)
level_options_button = NavButton(level_options_button_image, (level_options_button_image.get_width() / 2 + 5, screen_height - level_options_button_image.get_height() / 2 - 5))
pause_level_button = NavButton(pause_level_button_image, (screen_width - (pause_level_button_image.get_width() / 2) - 5, pause_level_button_image.get_height() / 2 + 5))
game_speed_button = NavButton(game_speed_button_image, (pause_level_button.rect.centerx - (pause_level_button_image.get_width()) - 5, pause_level_button_image.get_height() / 2 + 5))
quit_level_button = Button(level_nav_button, (screen_width - (level_nav_button.get_width() / 2) - 5, level_nav_button.get_height() / 2 + 5), 'Back', ui_font)

goto_upgrades_button = NavButton(goto_upgrades_button_image, (screen_width / 2, screen_height - level_nav_button.get_height() / 2 - 10))
goto_menu_button = NavButton(goto_menu_button_image, (goto_menu_button_image.get_width() / 2 + 10, goto_menu_button_image.get_height() / 2 + 10))
goto_levels_button = NavButton(goto_levels_button_image, goto_menu_button.rect.center)
go_back_to_upgrades_button = NavButton(go_back_to_upgrades_button_image, (screen_width * 0.25, go_back_to_upgrades_button_image.get_height() / 2 + 10))

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
cluster_shot_button = NavButton(cluster_shot_button_image, (rapid_fire_button.rect.centerx + rapid_fire_button.rect.width + 5, rapid_fire_button.rect.centery))
meteor_shower_button = NavButton(meteor_shower_button_image, (cluster_shot_button.rect.centerx + cluster_shot_button.rect.width + 5, cluster_shot_button.rect.centery))
raining_comets_button = NavButton(raining_comets_button_image, (meteor_shower_button.rect.centerx + meteor_shower_button.rect.width + 5, meteor_shower_button.rect.centery))
vaporize_button = NavButton(vaporize_button_image, (raining_comets_button.rect.centerx + raining_comets_button.rect.width + 5, raining_comets_button.rect.centery))

# Special Defenses Label
special_defenses_container_label = Title(special_defenses_label_abbreviated, (special_defenses_container.rect.left - special_defenses_label_abbreviated.get_width() / 2, special_defenses_container.rect.centery))

# Special Defenses Button
shock_absorber_button = NavButton(shock_absorber_button_image, (special_defenses_container.rect.left + (shock_absorber_button_image.get_width() / 2 + 25), special_defenses_container.rect.centery))
poison_antidote_button = NavButton(poison_antidote_button_image, (shock_absorber_button.rect.centerx + shock_absorber_button.rect.width + 5, shock_absorber_button.rect.centery))
flares_defense_button = NavButton(flares_defense_button_image, (poison_antidote_button.rect.centerx + poison_antidote_button.rect.width + 5, poison_antidote_button.rect.centery))
deflection_defense_button = NavButton(laser_deflection_button_image, (flares_defense_button.rect.centerx + flares_defense_button.rect.width + 5, flares_defense_button.rect.centery))
magnetic_mine_button = NavButton(magnetic_mine_button_image, (deflection_defense_button.rect.centerx + deflection_defense_button.rect.width + 5, deflection_defense_button.rect.centery))

red_strength_power_stone = PowerStone('Strength', red_power_stone_image, screen_middle, 1, 75)
orange_recovery_power_stone = PowerStone('Recovery', orange_power_stone_image, screen_middle, 2, 50)
yellow_speed_power_stone = PowerStone('Speed', yellow_power_stone_image, screen_middle, 5, 25)
green_depletion_power_stone = PowerStone('Depletion', green_power_stone_image, screen_middle, 10, 10)
blue_freeze_power_stone = PowerStone('Freeze', blue_power_stone_image, screen_middle, 15, 5)

# Base and Shield Health bars
base_and_shield_stats_container = StatsContainer(base_health_container, (base_health_container.get_width() / 2 + 5, screen_height - (base_health_container.get_height() / 2)))

# Preview window for previewing info for a saved game
saved_game_preview_window = PreviewWindow(upgrade_table, (screen_width / 2, screen_height / 2))
saved_game_preview_window.previewing_saved_game = True
close_saved_game_preview_window_button = NavButton(close_button_image, (saved_game_preview_window.rect.left + (saved_game_preview_window.rect.width * 0.9), saved_game_preview_window.rect.top + (saved_game_preview_window.rect.height * 0.055)))
play_saved_game_button = NavButton(play_button_image, (saved_game_preview_window.rect.centerx, saved_game_preview_window.rect.top + (saved_game_preview_window.rect.height * 0.77)))
delete_saved_game_button = NavButton(delete_button_image, (saved_game_preview_window.rect.centerx, play_saved_game_button.rect.centery + (play_saved_game_button.rect.height + 10)))
confirm_delete_saved_game_window = PreviewWindow(level_over_menu, saved_game_preview_window.pos)

# Preview window for previewing info for a level
level_preview_window = PreviewWindow(level_over_menu, (screen_width / 2, screen_height / 2))
close_level_preview_window = NavButton(close_button_image, (level_preview_window.rect.left + (level_preview_window.rect.width * 0.9), level_preview_window.rect.top + (level_preview_window.rect.height * 0.1)))
play_level_button = NavButton(play_button_image, (level_preview_window.rect.centerx, (level_preview_window.rect.top + (level_preview_window.rect.height * 0.87))))

enemy_collisions = pygame.sprite.groupcollide(player_bullet_group, enemy_group, True, False, pygame.sprite.collide_mask)

levels = []
level_x_offset = 0
button_spacing = (screen_width / 17.5) + (level_button.get_width() / 2)
button_y_spacing = screen_height * 0.2361
level_x_coord = screen_width * 0.1589 - (level_button.get_width() / 2)
level_y_coord = screen_height * 0.27

# Variables for setting up the levels
num_of_types = 1
num_of_enemies = 20
delay = 4
boss_num = 0
          
for i in range(100):
#for i in range(30):
   
   l = Level(level_button, i + 1, num_of_types, enemy_types, (level_x_coord + level_x_offset, level_y_coord), num_of_enemies)
   if i == 0:
       l.locked = False
   l.spawn_delay = delay 
   l.locked = False
   if (i + 1) % 10 == 0:
       if boss_num < len(enemy_boss_types.keys()):
           l.boss = boss_num
           boss_num += 1
   levels.append(l)
   num_of_enemies += 1
   if len(levels) % 3 == 0:
       num_of_types += 1 if num_of_types < len(enemy_types) else 0
   if len(levels) % 6 == 0:
       level_x_coord = screen_width * 0.1589 - (level_button.get_width() / 2)
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

def get_selected_game(games_loaded, game):
    for button in games_loaded:
        if button.connected_game == game:
            return button

def delete_saved_game(game, game_button):
    global saved_games
    global loaded_games
    _saved_games = saved_games.copy()
    _loaded_games = loaded_games.copy()
    _saved_games.pop(game)
    _loaded_games.remove(game_button)
    saved_games = _saved_games.copy()
    loaded_games = _loaded_games.copy()
    with open('saved_games.txt', 'w') as f:
        f.write(json.dumps(saved_games))
    os.remove(game + '.txt')

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
    main_turret_stats_table_stats = json.dumps(base_turret_stats_table.dict, cls=NumpyEncoder)
    extra_turret1_stats_table_stats = json.dumps(extra_turret1_stats_table.dict)
    extra_turret2_stats_table_stats = json.dumps(extra_turret2_stats_table.dict)
    extra_turret3_stats_table_stats = json.dumps(extra_turret3_stats_table.dict)
    extra_turret4_stats_table_stats = json.dumps(extra_turret4_stats_table.dict)
    
    levels_statuses = json.dumps(levels_locked_status)
    
    special_attacks_upgrades_stats = json.dumps(special_attacks_upgrades.dict)
    special_attack_stats = json.dumps(special_attacks_stats_table.dict)
    
    special_defenses_upgrades_stats = json.dumps(special_defenses_upgrades.dict)
    special_defense_stats = json.dumps(special_defenses_stats_table.dict)
    
    collected_stones = json.dumps(player_collected_power_stones)
    
    if player_base.loaded_saved_game is True:
        saved_file = player_base.loaded_game
    else:
        saved_file = save_date.strftime('%m%d%y %H%M%S')
        player_base.loaded_game = saved_file
        player_base.loaded_saved_game = True
    with open('saved_games.txt', 'w+') as sf:
        if save_date.hour >= 12:
            saved_games[f'{saved_file}'] = save_date.strftime('%m-%d-%y %I:%M PM')
        else:
            saved_games[f'{saved_file}'] = save_date.strftime('%m-%d-%y %I:%M AM')
        sf.write(json.dumps(saved_games))
    
    with open(f'{saved_file}.txt', 'w') as f:
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
        f.write('\n')
        f.write(collected_stones)
        
     
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
        base_turret_stats_table.dict.update(json.loads(lines[20]))
        extra_turret1_stats_table.dict.update(json.loads(lines[21]))
        extra_turret2_stats_table.dict.update(json.loads(lines[22]))
        extra_turret3_stats_table.dict.update(json.loads(lines[23]))
        extra_turret4_stats_table.dict.update(json.loads(lines[24]))
        special_attacks_stats_table.dict.update(json.loads(lines[27]))
        special_defenses_stats_table.dict.update(json.loads(lines[29]))
        
        player_collected_power_stones.update(json.loads(lines[30]))
        
        levels_locked_status.update(json.loads(lines[25]))
        keys = [k for k in levels_locked_status.keys()]
        for i in range(len(levels)):
            levels[i].locked = levels_locked_status[keys[i]]          
        
        # Refresh Player currency
        player_money.update_var(f'{player_stats["Space Crystals"]}')
        player_money_enlarged.update_var(f'{player_stats["Space Crystals"]}')
        player_money_shrunken.update_var(f'{player_stats["Space Crystals"]}')
        player_power_crystals_enlarged.update_var(f'{player_stats["Power Gems"]}')
        player_power_crystals_shrunken.update_var(f'{player_stats["Power Gems"]}')
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
        base_turret_stats_table.reset_stats()
        shield_stats_table.reset_stats()
        extra_turret1_stats_table.reset_stats()
        extra_turret2_stats_table.reset_stats()
        extra_turret3_stats_table.reset_stats()
        extra_turret4_stats_table.reset_stats()
        special_attacks_stats_table.reset_stats()
        special_defenses_stats_table.reset_stats()
        
        # Updating UI Text to show player how many special attacks and defenses they have
        rapid_fire_button.remaining_uses.update_var(f'{special_attacks_stats_table.dict["Rapid Fire"]}')
        cluster_shot_button.remaining_uses.update_var(f'{special_attacks_stats_table.dict["Cluster Shots"]}')
        meteor_shower_button.remaining_uses.update_var(f'{special_attacks_stats_table.dict["Meteor Shower"]}')
        raining_comets_button.remaining_uses.update_var(f'{special_attacks_stats_table.dict["Raining Comets"]}')
        vaporize_button.remaining_uses.update_var(f'{special_attacks_stats_table.dict["Vaporizers"]}')
            
        shock_absorber_button.remaining_uses.update_var(f'{special_defenses_stats_table.dict["Shock Absorbers"]}')
        poison_antidote_button.remaining_uses.update_var(f'{special_defenses_stats_table.dict["Poison Antidote"]}')
        flares_defense_button.remaining_uses.update_var(f'{special_defenses_stats_table.dict["Flares"]}')
        deflection_defense_button.remaining_uses.update_var(f'{special_defenses_stats_table.dict["Deflection"]}')
        magnetic_mine_button.remaining_uses.update_var(f'{special_defenses_stats_table.dict["Magnetic Mine"]}')
        
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
                
    base_turret_stats_table.dict.update(main_turret_stats)
    base_turret_stats_table.reset_stats()
               
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
    
    player_stats['Space Crystals'] = 50000000000
    player_stats['Power Gems'] = 500000000
    player_stats['Rank'] = 'Cadet'
    player_stats['XP'] = 0
    player_money_enlarged.update_var(f'{player_stats["Space Crystals"]}')
    player_power_crystals_enlarged.update_var(f'{player_stats["Power Gems"]}')
    player_money_shrunken.update_var(f'{player_stats["Space Crystals"]}')
    player_power_crystals_shrunken.update_var(f'{player_stats["Power Gems"]}')
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
            

def load_game_selection_menu():
    for event in pygame.event.get():
        
        # Player Navigating back to the main menu
        if goto_menu_button.clicked(event):
            if game['Sounds'] is True:
                button_clicked_sound.play()
            game['Preview Saved Game'] = False
            game['Confirm Delete Game'] = False
            level['Game Select'] = False
            level['On Menu'] = True
            level['Fade'] = True
            
        if game['Confirm Delete Game'] is True:
            # Player is forced into deciding between deleting their game or not
            if confirm_delete_saved_game_window.preview_info['Confirm Yes'].clicked(event):
                if game['Sounds'] is True:
                    button_clicked_sound.play()
                # Player clicks "Yes" confirming they want to delete the selected game 
                game_button_to_delete = get_selected_game(loaded_games, player_base.loaded_game)
                delete_saved_game(game_button_to_delete.connected_game, game_button_to_delete)
                game['Confirm Delete Game'] = False
                game['Preview Saved Game'] = False
                if len(loaded_games) == 0:
                    # Navigating back to main menu if player has deleted all saved games
                    level['Game Select'] = False
                    level['On Menu'] = True
                    level['Fade'] = True
            elif confirm_delete_saved_game_window.preview_info['Confirm No'].clicked(event):
                if game['Sounds'] is True:
                    button_clicked_sound.play()
                # Delete Game window disappears
                # Player still sees their saved game info
                game['Confirm Delete Game'] = False
            
        else:          
            # Player selecting which saved game they want to load
            if game['Preview Saved Game'] is False:
                for g in loaded_games:
                    if g.clicked(event):
                        if game['Sounds'] is True:
                            button_clicked_sound.play()
                        player_base.loaded_game = g.connected_game 
                        player_base.loaded_saved_game = True
                        load_saved_game(player_base.loaded_game + '.txt')               
                        game['Preview Saved Game'] = True
                        saved_game_preview_window.get_saved_game_info(g.label.text, g.connected_game, player_stats)
                        saved_game_preview_window.get_power_stone_collection(player_collected_power_stones)
                        
            elif game['Preview Saved Game'] is True:
                if close_saved_game_preview_window_button.clicked(event):
                    if game['Sounds'] is True:
                            button_clicked_sound.play()
                    game['Preview Saved Game'] = False
                    
                if play_saved_game_button.clicked(event):
                    if game['Sounds'] is True:
                            button_clicked_sound.play()
                    level['Fade'] = True
                    level['Overworld'] = True
                    level['Game Select'] = False
                    
                if delete_saved_game_button.clicked(event):
                    if game['Sounds'] is True:
                            button_clicked_sound.play()
                    confirm_delete_saved_game_window.set_confirm_delete_game_info()
                    game['Confirm Delete Game'] = True
                    #game['Preview Saved Game'] = False
                        
            if len(loaded_games) > 9:
                if loaded_games[-1].rect.x > screen_width:
                    if continue_button.clicked(event):
                        for g in loaded_games:
                            g.scroll_amount = -screen_width
                        
                            
                if loaded_games[0].rect.x < 0:
                    if go_back_button.clicked(event):
                        for g in loaded_games:
                            g.scroll_amount = screen_width    
     
    screen.blit(bg, (0, 0))
    
    for games in loaded_games:
        games.show()
        
    goto_menu_button.show()
    saved_games_title.show_to_player()
        
    if game['Preview Saved Game'] is True:
        saved_game_preview_window.show_preview_info()
        close_saved_game_preview_window_button.show()
        play_saved_game_button.show()
        delete_saved_game_button.show()
        
        if game['Confirm Delete Game'] is True:
            confirm_delete_saved_game_window.show_preview_info()           
    
    if len(loaded_games) > 9:
        if loaded_games[-1].rect.x > screen_width:
            continue_button.show()
            
        if loaded_games[0].rect.x < 0:
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
            #player_base.loaded_game = f'Game {len(saved_games) + 1}'
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
        
        if game['Preview Level'] is False:
            for lvl in levels:
                if lvl.active_button.clicked(event):
                    if lvl.locked is False:
                        if game['Sounds'] is True:
                            button_clicked_sound.play()
                        game['Current Level'] = lvl
                        game['Preview Level'] = True
                        game['Current Level'].load(player_base)
                        level_preview_window.get_level_preview_info(player_stats, lvl)
                        level_preview_window.get_power_stone_loot(lvl, player_collected_power_stones)

                    elif lvl.locked is True:
                        if game['Sounds'] is True:
                            insufficient_funds_sound.play()
                        must_complete_previous_level_message.notify_player()
        
        elif game['Preview Level'] is True:
            if close_level_preview_window.clicked(event):
                if game['Sounds'] is True:
                    button_clicked_sound.play()
                game['Preview Level'] = False
            
            if play_level_button.clicked(event):
                if game['Sounds'] is True:
                    button_clicked_sound.play()
                level_feedback.update_var(f'Level: {game["Current Level"].num}')
                level['Fade'] = True
                level['Overworld'] = False
                level['Battle'] = True
                game['Screen Transition'] = True
                game['Current Track'] = gameplay_music2
        
        if continue_button.clicked(event):
            if levels[-1].active_button.rect.x > screen_width:
                if game['Sounds'] is True:
                    button_clicked_sound.play()
                for lvl in levels:
                    lvl.scroll_amount = screen_width
                
        if go_back_button.clicked(event):                 
            if levels[0].active_button.rect.x < 0:
                if game['Sounds'] is True:
                    button_clicked_sound.play()
                for lvl in levels:
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
    
    if game['Preview Level'] is True:
        level_preview_window.show_preview_info()
        close_level_preview_window.show()
        play_level_button.show()
        

def upgrade_submenu():
    
    for event in pygame.event.get():
            
        if go_back_to_upgrades_button.clicked(event):
            if game['Sounds'] is True:
                button_clicked_sound.play()
            save_game()
            level['Fade'] = True
            level['Upgrade Submenu'] = False
            level['Upgrading'] = True
            player_base.selected_for_upgrade = False
            base_turret.selected_for_upgrade = False
            extra_turret1.selected_for_upgrade = False
            extra_turret2.selected_for_upgrade = False
            extra_turret3.selected_for_upgrade = False
            extra_turret4.selected_for_upgrade = False
            rapid_fire_button.remaining_uses.update_var(f'{special_attacks_stats_table.dict["Rapid Fire"]}')
            cluster_shot_button.remaining_uses.update_var(f'{special_attacks_stats_table.dict["Cluster Shots"]}')
            meteor_shower_button.remaining_uses.update_var(f'{special_attacks_stats_table.dict["Meteor Shower"]}')
            raining_comets_button.remaining_uses.update_var(f'{special_attacks_stats_table.dict["Raining Comets"]}')
            vaporize_button.remaining_uses.update_var(f'{special_attacks_stats_table.dict["Vaporizers"]}')
            
            shock_absorber_button.remaining_uses.update_var(f'{special_defenses_stats_table.dict["Shock Absorbers"]}')
            poison_antidote_button.remaining_uses.update_var(f'{special_defenses_stats_table.dict["Poison Antidote"]}')
            flares_defense_button.remaining_uses.update_var(f'{special_defenses_stats_table.dict["Flares"]}')
            deflection_defense_button.remaining_uses.update_var(f'{special_defenses_stats_table.dict["Deflection"]}')
            magnetic_mine_button.remaining_uses.update_var(f'{special_defenses_stats_table.dict["Magnetic Mine"]}')
                                    
        if game['Upgrading Base'] == True:
            # Switching between turrets and base upgrades
            if player_base.clicked(event):
                player_base.selected_for_upgrade = True
                base_turret.selected_for_upgrade = False
                extra_turret1.selected_for_upgrade = False
                extra_turret2.selected_for_upgrade = False
                extra_turret3.selected_for_upgrade = False
                extra_turret4.selected_for_upgrade = False
                if game['Sounds'] is True:
                    button_clicked_sound.play()
                level['Submenu'] = base_upgrades
                level['Submenu Stats'] = base_stats_table
            
            if base_turret.clicked(event):
                player_base.selected_for_upgrade = False
                base_turret.selected_for_upgrade = True
                extra_turret1.selected_for_upgrade = False
                extra_turret2.selected_for_upgrade = False
                extra_turret3.selected_for_upgrade = False
                extra_turret4.selected_for_upgrade = False
                if game['Sounds'] is True:
                    button_clicked_sound.play()
                level['Submenu'] = base_turret_upgrades
                level['Submenu Stats'] = base_turret_stats_table
               
            if extra_turret1.clicked(event):
                if extra_turret1 not in helper_turret_group:
                    if game['Sounds'] is True:
                        insufficient_funds_sound.play()
                else:
                    player_base.selected_for_upgrade = False
                    base_turret.selected_for_upgrade = False
                    extra_turret1.selected_for_upgrade = True
                    extra_turret2.selected_for_upgrade = False
                    extra_turret3.selected_for_upgrade = False
                    extra_turret4.selected_for_upgrade = False
                    if game['Sounds'] is True:
                        button_clicked_sound.play()
                    level['Submenu'] = extra_turret1_upgrades
                    level['Submenu Stats'] = extra_turret1_stats_table
            #if turret_x2_button.clicked(event):
            if extra_turret2.clicked(event):
                if extra_turret2 not in helper_turret_group:
                    if game['Sounds'] is True:
                        insufficient_funds_sound.play()
                    turret_not_purchased_message.notify_player()
                else:
                    player_base.selected_for_upgrade = False
                    base_turret.selected_for_upgrade = False
                    extra_turret1.selected_for_upgrade = False
                    extra_turret2.selected_for_upgrade = True
                    extra_turret3.selected_for_upgrade = False
                    extra_turret4.selected_for_upgrade = False
                    if game['Sounds'] is True:
                        button_clicked_sound.play()
                    level['Submenu'] = extra_turret2_upgrades
                    level['Submenu Stats'] = extra_turret2_stats_table
            #if turret_x3_button.clicked(event):
            if extra_turret3.clicked(event):
                if extra_turret3 not in helper_turret_group:
                    if game['Sounds'] is True:
                        insufficient_funds_sound.play()
                    turret_not_purchased_message.notify_player()
                else:
                    player_base.selected_for_upgrade = False
                    base_turret.selected_for_upgrade = False
                    extra_turret1.selected_for_upgrade = False
                    extra_turret2.selected_for_upgrade = False
                    extra_turret3.selected_for_upgrade = True
                    extra_turret4.selected_for_upgrade = False
                    if game['Sounds'] is True:
                        button_clicked_sound.play()
                    level['Submenu'] = extra_turret3_upgrades
                    level['Submenu Stats'] = extra_turret3_stats_table
            #if turret_x4_button.clicked(event):
            if extra_turret4.clicked(event):
                if extra_turret4 not in helper_turret_group:
                    if game['Sounds'] is True:
                        insufficient_funds_sound.play()
                    turret_not_purchased_message.notify_player()
                else:
                    player_base.selected_for_upgrade = False
                    base_turret.selected_for_upgrade = False
                    extra_turret1.selected_for_upgrade = False
                    extra_turret2.selected_for_upgrade = False
                    extra_turret3.selected_for_upgrade = False
                    extra_turret4.selected_for_upgrade = True
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
                                player_money_shrunken.update_var(f'{int(player_stats["Space Crystals"])}')
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
                                        player_money_shrunken.update_var(f'{int(player_stats["Space Crystals"])}')
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
                                        player_money_shrunken.update_var(f'{int(player_stats["Space Crystals"])}')
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
                                player_money_shrunken.update_var(f'{int(player_stats["Space Crystals"])}')
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
                                player_money_shrunken.update_var(f'{int(player_stats["Space Crystals"])}')
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
                                player_money_shrunken.update_var(f'{int(player_stats["Space Crystals"])}')
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
                                    player_money_shrunken.update_var(f'{int(player_stats["Space Crystals"])}')
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
                                        player_money_shrunken.update_var(f'{int(player_stats["Space Crystals"])}')
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
                                        player_money_shrunken.update_var(f'{int(player_stats["Space Crystals"])}')
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
                                    player_money_shrunken.update_var(f'{int(player_stats["Space Crystals"])}')
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
                                        player_power_crystals_shrunken.update_var(f'{int(player_stats["Power Gems"])}')
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
                                player_money_shrunken.update_var(f'{int(player_stats["Space Crystals"])}')
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
                            player_power_crystals_shrunken.update_var(f'{int(player_stats["Power Gems"])}')
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
                            player_money_shrunken.update_var(f'{int(player_stats["Space Crystals"])}')
                            level['Submenu'].update_cost(button)
                            level['Submenu Stats'].update_stat(b)
                    
                elif player_stats['Space Crystals'] < level['Submenu'].get_cost(button):
                    # Player does not enough enough money for desired upgrade
                    if game['Sounds'] is True:
                        insufficient_funds_sound.play()
                    not_enough_money_message.notify_player()
                
    
    screen.blit(bg, (0, 0))
    
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
    
    if game['Upgrading Base'] is True:
        player_base.show()
        base_turret.draw_for_upgrades()
        for helper in helper_turret_group:
            helper.draw_for_upgrades()
    
        player_money_shrunken.show_to_player()
        screen.blit(power_crystal, (player_money_shrunken.rect.x - 40, player_money_shrunken.rect.top))
        player_power_crystals_shrunken.show_to_player()
        screen.blit(power_gem_image, (player_power_crystals_shrunken.rect.x - 40, player_power_crystals_shrunken.rect.top))    
    else:
        player_money_enlarged.show_to_player()
        screen.blit(power_crystal, (player_money_enlarged.rect.x - 40, player_money_enlarged.rect.top))
        player_power_crystals_enlarged.show_to_player()
        screen.blit(power_gem_image, (player_power_crystals_enlarged.rect.x - 40, player_power_crystals_enlarged.rect.top))    
                
    go_back_to_upgrades_button.show()
    
    not_enough_money_message.show_notification()
    stat_limit_reached_message.show_notification()
    shield_already_active_message.show_notification()
    shield_not_active_message.show_notification()
    regeneration_already_active_message.show_notification()
    base_fully_repaired_message.show_notification()
    not_unlocked_yet_message.show_notification()
    extra_turret_limit_reached_message.show_notification()
    turret_not_purchased_message.show_notification()
    

def upgrade_menu():
    
    for event in pygame.event.get():
        # Exiting the upgrade root menu
        if goto_levels_button.clicked(event):
            if game['Sounds'] is True:
                button_clicked_sound.play()
            level['Upgrading'] = False
            level['Overworld'] = True
            level['Fade'] = True
            
        # Base and Turrets Upgrades
        if base_upgrades_button.clicked(event):
            if game['Sounds'] is True:   
                button_clicked_sound.play()
            player_base.selected_for_upgrade = True
            game['Upgrading Shield'] = False
            game['Upgrading Base'] = True
            game['Purchasing Special Attacks'] = False
            game['Purchasing Special Defenses'] = False
            level['Fade'] = True
            level['Upgrading'] = False
            level['Upgrade Submenu'] = True
            level['Upgrade Item'] = player_base
            level['Submenu'] = base_upgrades
            level['Submenu Stats'] = base_stats_table
            base_stats_table.stats[0].update_var(f'{int(player_base.stats["Health"])}')
                
        # Shield Upgrades
        if shield_upgrades_button.clicked(event):
            game['Upgrading Shield'] = True
            game['Upgrading Base'] = False
            game['Purchasing Special Attacks'] = False
            game['Purchasing Special Defenses'] = False
            if game['Sounds'] is True:
                button_clicked_sound.play()
            level['Fade'] = True
            level['Upgrading'] = False
            level['Upgrade Submenu'] = True
            level['Submenu'] = shield_upgrades
            level['Submenu Stats'] = shield_stats_table
                
        # Special Attacks Upgrades
        if special_attacks_button.clicked(event):
            game['Upgrading Shield'] = False
            game['Upgrading Base'] = False
            game['Purchasing Special Attacks'] = True
            game['Purchasing Special Defenses'] = False
            if game['Sounds'] is True:
                button_clicked_sound.play()
            level['Fade'] = True
            level['Upgrading'] = False
            level['Upgrade Submenu'] = True
            level['Submenu'] = special_attacks_upgrades
            level['Submenu Stats'] = special_attacks_stats_table
                
        if special_defenses_button.clicked(event):
            game['Upgrading Shield'] = False
            game['Upgrading Base'] = False
            game['Purchasing Special Attacks'] = False
            game['Purchasing Special Defenses'] = True
            if game['Sounds'] is True:
                button_clicked_sound.play()
            level['Fade'] = True
            level['Upgrading'] = False
            level['Upgrade Submenu'] = True
            level['Submenu'] = special_defenses_upgrades
            level['Submenu Stats'] = special_defenses_stats_table      
            
            
    # Upgrades Main screen
    screen.blit(bg, (0, 0))

    # Upgrades title
    upgrades_menu_title.show_to_player()
    
    # Upgrades buttons
    shield_upgrades_button.show()
    base_upgrades_button.show()    
    special_defenses_button.show()
    special_attacks_button.show()
    
    # NavButton to go back to the levels overworld screen
    goto_levels_button.show()
                  
    
def main_play():
    
    if True:
         
        for event in pygame.event.get():
             
            # Adjusting the current level speed
            # REMOVE BEFORE FINAL DISTRIBUTION TO TESTERS
            if game_speed_button.clicked(event):
                if game['Sounds'] is True:
                    button_clicked_sound.play()
                level['Button Clicked'] = True
                if level['Speed'] == 1:
                    level['Speed'] = 2
                    #game['Current Level'].spawn_delay = 2
                elif level['Speed'] == 2:
                    level['Speed'] = 4
                    #game['Current Level'].spawn_delay = 1
                elif level['Speed'] == 4:
                    level['Speed'] = 1
                    #game['Current Level'].spawn_delay = 4            
             
            # Pausing the current level
            if pause_level_button.clicked(event):
                level['Paused'] = True
                
            if level['Paused'] is True:
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
                    
                if player_base.special_attack_used is False:
                    if time() - player_base.special_attack_start_time >= base_turret.stats['Special Cooldown']:
                        # Player using a special attack
                        if rapid_fire_button.clicked(event):
                            if base_turret.special_in_use is False:
                                player_base.special_attack_used = True
                                player_base.special_attack_start_time = time()
                                player_base.special_attack_in_use = 'Rapid Fire'
                                player_base.rapid_fire_delay = 0.1
                                #activate special timer countdown
                            
                        if cluster_shot_button.clicked(event):
                            if special_attacks_stats_table.dict['Cluster Shots'] > 0:
                                player_base.special_attack_in_use = 'Cluster Shots'
                                #player_base.special_attack_used = True
                                special_attacks_stats_table.dict['Cluster Shots'] -= 1
                            
                        if meteor_shower_button.clicked(event):
                            if player_base.special_attack_used is False:
                                if special_attacks_stats_table.dict['Meteor Shower'] > 0:
                                    player_base.meteor_shower()
                                    player_base.special_attack_used = True
                                    player_base.special_attack_start_time = time()
                                    player_base.special_attack_in_use = 'Meteor Shower'
                                    special_attacks_stats_table.dict['Meteor Shower'] -= 1
                                    special_attacks_stats_table.reset_stats()
                            
                        if raining_comets_button.clicked(event):
                            if special_attacks_stats_table.dict['Raining Comets'] > 0:
                                player_base.special_attack_start_time = time()
                                player_base.raining_comets_start_time = time()
                                player_base.special_attack_in_use = 'Raining Comets'
                                player_base.special_attack_used = True
                                special_attacks_stats_table.dict['Raining Comets'] -= 1
                            
                        if vaporize_button.clicked(event):
                            if special_attacks_stats_table.dict['Vaporizers'] > 0:
                                player_base.vaporize_enemies(enemy_group)
                                enemy_bullet_group.empty()
                                player_base.special_attack_used = True
                                player_base.special_attack_start_time = time()
                                if game['Sounds'] is True:
                                    enemies_vaporized_sound.play()
                                special_attacks_stats_table.dict['Vaporizers'] -= 1
    
                if player_base.special_defense_used is False:
                    if time() - player_base.special_defense_start_time >= base_turret.stats['Special Cooldown']:
                        # Player can use a special defense
                        if shock_absorber_button.clicked(event):
                            if special_defenses_stats_table.dict['Shock Absorbers'] > 0:
                                player_base.special_defense_start_time = time()
                                player_base.special_defense_used = True
                                player_base.absorb_electric_shock = True
                                player_base.special_defense_in_use = 'Shock Absorbers'
                                special_defenses_stats_table.dict['Shock Absorbers'] -= 1
                                
                        if poison_antidote_button.clicked(event):
                            if special_defenses_stats_table.dict['Poison Antidote'] > 0:
                                player_base.special_defense_start_time = time()
                                player_base.special_defense_used = True
                                player_base.poison_antidote_applied = True
                                player_base.special_defense_in_use = 'Poison Antidote'
                                special_defenses_stats_table.dict['Poison Antidote'] -= 1
                                
                        if flares_defense_button.clicked(event):
                            if special_defenses_stats_table.dict['Flares'] > 0:
                                player_base.special_defense_start_time = time()
                                player_base.special_defense_used = True
                                player_base.special_defense_in_use = 'Flares'
                                special_defenses_stats_table.dict['Flares'] -= 1
                                
                        if deflection_defense_button.clicked(event):
                            if special_defenses_stats_table.dict['Deflection'] > 0:
                                player_base.special_defense_start_time = time()
                                player_base.special_defense_used = True
                                player_base.special_defense_in_use = 'Deflection'
                                special_defenses_stats_table.dict['Deflection'] -= 1
                            
                                
                        if magnetic_mine_button.clicked(event):
                            if special_defenses_stats_table.dict['Magnetic Mine'] > 0:
                                player_base.special_defense_start_time = time()
                                player_base.special_defense_used = True
                                player_base.special_defense_in_use = 'Magnetic Mine'
                                player_defenses_group.add(MagneticMine(magnetic_mine_image, (screen_width * 0.7, screen_height / 2)))
                                special_defenses_stats_table.dict['Magnetic Mine'] -= 1
                                        
            # Player firing main turret
            if level['Button Clicked'] is False:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if player_base.stats['Health'] > 0:
                        if player_base.special_attack_in_use == 'Cluster Shots':
                            player_base.special_attack_start_time = time()
                            player_base.cluster_shot(player_bullet_group)
                            player_base.special_attack_used = True
                        else:
                            base_turret.shoot(player_bullet_group)
                            game['Current Level'].total_shots_taken += 1
           
        # Player holding down the mouse button for repetitive shooting
        if pygame.mouse.get_pressed()[0] is True and level['Button Clicked'] is False:
            if time() - base_turret.last_shot_time >= player_base.rapid_fire_delay:
                base_turret.shoot(player_bullet_group)

        player_base.handle_special_attack_timer(base_turret.stats['Special Cooldown'], special_attacks_durations[player_base.special_attack_in_use])
        player_base.handle_special_defense_timer(base_turret.stats['Special Cooldown'], special_defenses_durations[player_base.special_defense_in_use])
                              
        if player_base.special_attack_used is True:
            if player_base.special_attack_in_use == 'Raining Comets':
                player_base.rain_comets()
            elif player_base.special_attack_in_use == 'Meteor Shower':
                player_base.meteor_shower()       
               
        # Player using Flares Special Defense
        if player_base.special_defense_used is True:
            if player_base.special_defense_in_use == 'Flares':
                player_base.deploy_defense_flares()
               
        if pygame.mouse.get_pressed()[0] is False:
            level['Button Clicked'] = False
                
        # Waiting 4 seconds before enemies start spawning          
        if time() - game['Current Level'].start_time > 4:
            if len(enemy_group) < 20 and player_base.stats['Health'] > 0:
                # Spawn enemy ships until all the enemies have been spawned
                if time() - level['Spawn Time'] >= game['Current Level'].spawn_delay / level['Speed']:
                    if level['Paused'] is False:
                        game['Current Level'].spawn_enemy()
                        game['Current Level'].enemies_left_num.update_var(game['Current Level'].enemies_left())
                        level['Spawn Time'] = time()           
                            
        # Enemy attacks hitting the base or shield        
        if pygame.sprite.groupcollide(enemy_bullet_group, base_group, False, False):
            player_base.collided_enemy_bullets = pygame.sprite.groupcollide(enemy_bullet_group, base_group, False, False, pygame.sprite.collide_mask)
            if player_base.collided_enemy_bullets:
                    for enemy_bullet in player_base.collided_enemy_bullets:
                        for d in player_base.collided_enemy_bullets[enemy_bullet]:
                            if type(enemy_bullet) == Bullet:
                                if player_base.special_defense_in_use == 'Deflection':
                                    if type(d) == Base and base_shield not in base_group:
                                        player_base.deflect_lasers(enemy_bullet)
                                    else:
                                        d.take_damage(enemy_bullet.damage)
                                        enemy_bullet.kill()
                                else:
                                    # Enemy bullet hits base without the Shield                        
                                    if type(d) == Base and base_shield not in base_group:
                                        if enemy_bullet.poisonous is True:
                                            # Base or shield gets poisoned
                                            d.take_damage(enemy_bullet.damage)
                                            d.poisoned_amount += enemy_bullet.poison_amount
                                            game['Current Level'].player_base_damage_taken += enemy_bullet.poison_amount
                                            animations_group.add(Animation(impact_animation, 1, enemy_bullet.pos, base_hit_sound))
                                        else:
                                            d.take_damage(enemy_bullet.damage)
                                            game['Current Level'].player_base_damage_taken += enemy_bullet.damage
                                            animations_group.add(Animation(impact_animation, 1, enemy_bullet.pos, base_hit_sound))
                                    # Enemy bullet hits the base or shield with the Shield active
                                    # only the Shield will take damage
                                    else:
                                        d.take_damage(enemy_bullet.damage)
                                        game['Current Level'].player_base_damage_taken += enemy_bullet.damage
                                    enemy_bullet.kill()
                                        
                            elif type(enemy_bullet)  == ChargeBolt:
                                if type(d) == Shield:
                                    # Electric Shield takes 1 percent damage of the charge bolt
                                    d.take_damage(enemy_bullet.damage / 100)
                                    game['Current Level'].player_base_damage_taken += enemy_bullet.damage / 100
                                elif type(d) == Base and base_shield not in base_group:
                                    # Base and turrets get electrocuted
                                    if d.absorb_electric_shock is True:
                                        enemy_bullet.kill()
                                    else:
                                        d.electrocution_damage = enemy_bullet.damage
                                        d.electrified = True
                                        d.electrified_start_time = time()
                                    game['Current Level'].player_base_damage_taken += enemy_bullet.damage
                                    # Every existing helper turret is rendered useless while being electrocuted
                                    # Main turret is not affected
                                    for h in helper_turret_group:
                                        h.paralyzed = True
                                        h.paralyzed_start_time = time()
                                 
                            elif type(enemy_bullet) == Laser:
                                enemy_bullet.check_collision_with_base(base_group)                          
        
        # Player bullet hitting enemy ships
        if pygame.sprite.groupcollide(player_bullet_group, enemy_group, False, False):  
            enemy_collisions = pygame.sprite.groupcollide(player_bullet_group, enemy_group, False, False, pygame.sprite.collide_mask)     
            if enemy_collisions:
                for bullet in enemy_collisions:
                    
                    for ship in enemy_collisions[bullet]:
                        if ship.has_shield() and ship.shield.active is True:
                            #if bullet.mask.overlap(ship.shield.mask, (ship.shield.rect.x - bullet.rect.x, ship.shield.rect.y - bullet.rect.y)):
                            ship.shield.take_damage(bullet.damage)
                        elif ship.has_shield() and ship.shield.active is False or \
                        ship.has_shield() is False:
                            ship.take_damage(bullet.damage)
                        bullet.kill()
                        if type(bullet) == Bullet and bullet.player_shot is True:
                            game['Current Level'].total_shots_hit += 1                  
                                                                                                         
        # Player bullet colliding with a flare
        if pygame.sprite.groupcollide(player_bullet_group, enemy_flares_group, False, False):
            if pygame.sprite.groupcollide(player_bullet_group, enemy_flares_group, True, True, pygame.sprite.collide_mask):
                game['Current Level'].total_shots_hit += 1
                                     
        screen.blit(bg, (0, 0))

        if level['Paused'] is False:
            base_group.update(base_and_shield_stats_container)
            player_bullet_group.update()
            meteor_group.update()
            enemy_flares_group.update()
            spawn_orb_group.update(spawn_orb_group)
            enemy_bullet_group.update()
            player_defenses_group.update()
            healing_ring_group.update()
            health_flares_group.update()
            enemy_group.update(game['Delta Time'])
            enemy_shields_group.update()
            animations_group.update(player_base)
                                                                        
        base_group.draw(screen)       
        player_bullet_group.draw(screen)
               
        base_turret.follow_mouse_pos()
        
        
        for helper in helper_turret_group:
            if level['Paused'] is False:
                helper.update(enemy_group)
            helper.draw()
            if helper.attack is True and level['Game Over'] is False:
                if helper.target_in_range():
                    helper.help_shoot(player_bullet_group)    
                
        enemy_flares_group.draw(screen)
        spawn_orb_group.draw(screen)
        enemy_bullet_group.draw(screen)
        player_defenses_group.draw(screen)
        healing_ring_group.draw(screen)
        health_flares_group.draw(screen)
        enemy_group.draw(screen)
        enemy_shields_group.draw(screen) 
        animations_group.draw(screen)       
    
       # if int(game['Current Level'].enemies_left_num.text) > 0:
        if game['Current Level'].current_spawn_index < len(game['Current Level'].active_enemies):
           # return True
            game['Current Level'].enemies_left_label.show_to_player()
            game['Current Level'].enemies_left_num.show_to_player()
                
        # Level Completed Feedback Message
        if player_base.stats['Health'] > 0:
            if game['Current Level'].done_spawning() and len(enemy_group) == 0:
                if game['Current Level'].played_winning_sound is False:
                    pygame.mixer.stop()
                    pygame.mixer.music.stop()
                    level_completed_sound.play()
                    game['Current Level'].played_winning_sound = True
                enemy_bullet_group.empty()
                player_bullet_group.empty()
                player_base.poisoned_amount = 0
                player_base.electrified = False
                
                if game['Current Level'].completed is False:
                    # add in power stone chances at levels red-20, orange-30, yellow-40, green-60, blue-70 
                    level_completed_menu.header.update_var(f'Level {game["Current Level"].num} Complete')
                    if game['Current Level'].num == 20:
                        stone_loot = game['Current Level'].power_stone_loot(player_collected_power_stones, red_strength_power_stone)
                        if stone_loot != None:
                            game['Current Level'].explode_reveal_power_stone(red_strength_power_stone)
                            level_completed_menu.generate_winnings(game['Current Level'].loot_drop(), game['Current Level'].power_gem_loot(), stone_loot)
                        else:
                            level_completed_menu.generate_winnings(game['Current Level'].loot_drop(), game['Current Level'].power_gem_loot())
                            
                    elif game['Current Level'].num == 30:
                        stone_loot = game['Current Level'].power_stone_loot(player_collected_power_stones, orange_recovery_power_stone)
                        if stone_loot != None:
                            game['Current Level'].explode_reveal_power_stone(orange_recovery_power_stone)
                            level_completed_menu.generate_winnings(game['Current Level'].loot_drop(), game['Current Level'].power_gem_loot(), stone_loot)
                        else:
                            level_completed_menu.generate_winnings(game['Current Level'].loot_drop(), game['Current Level'].power_gem_loot())
                            
                    elif game['Current Level'].num == 40:
                        stone_loot = game['Current Level'].power_stone_loot(player_collected_power_stones, yellow_speed_power_stone)
                        if stone_loot != None:
                            game['Current Level'].explode_reveal_power_stone(yellow_speed_power_stone)
                            level_completed_menu.generate_winnings(game['Current Level'].loot_drop(), game['Current Level'].power_gem_loot(), stone_loot)
                        else:
                            level_completed_menu.generate_winnings(game['Current Level'].loot_drop(), game['Current Level'].power_gem_loot())
                            
                    elif game['Current Level'].num == 60:
                        stone_loot = game['Current Level'].power_stone_loot(player_collected_power_stones, green_depletion_power_stone)
                        if stone_loot != None:
                            game['Current Level'].explode_reveal_power_stone(green_depletion_power_stone)
                            level_completed_menu.generate_winnings(game['Current Level'].loot_drop(), game['Current Level'].power_gem_loot(), stone_loot)
                        else:
                            level_completed_menu.generate_winnings(game['Current Level'].loot_drop(), game['Current Level'].power_gem_loot())
                            
                    elif game['Current Level'].num == 70:
                        stone_loot = game['Current Level'].power_stone_loot(player_collected_power_stones, blue_freeze_power_stone)
                        if stone_loot != None:
                            game['Current Level'].explode_reveal_power_stone(blue_freeze_power_stone)
                            level_completed_menu.generate_winnings(game['Current Level'].loot_drop(), game['Current Level'].power_gem_loot(), stone_loot)
                        else:
                            level_completed_menu.generate_winnings(game['Current Level'].loot_drop(), game['Current Level'].power_gem_loot())
                            
                    else:
                        level_completed_menu.generate_winnings(game['Current Level'].loot_drop(), game['Current Level'].power_gem_loot())
                        
                    player_stats['Space Crystals'] += game['Current Level'].loot_drop()
                    player_stats['Power Gems'] += game['Current Level'].power_gem_loot()
                    player_money_enlarged.update_var(f'{int(player_stats["Space Crystals"])}')
                    player_money_shrunken.update_var(f'{int(player_stats["Space Crystals"])}')
                    player_power_crystals_enlarged.update_var(f'{int(player_stats["Power Gems"])}')
                    player_power_crystals_shrunken.update_var(f'{int(player_stats["Power Gems"])}')
                    if game['Current Level'].num < len(levels):
                        # Unlocking the next level
                        levels[game['Current Level'].num].locked = False
                        levels_locked_status[status_keys[game['Current Level'].num]] = False
                game['Current Level'].completed = True
                
                        
        # Player was defeated in the current playing level
        if player_base.stats['Health'] <= 0:
            if game['Current Level'].played_defeated_sound is False:
                pygame.mixer.stop()
                pygame.mixer.music.stop()
                level_defeated_sound.play()
                if player_stats['Lives'] > 0:
                    player_stats['Lives'] -= 1
                level_defeated_menu.generate_lost_info(player_stats['Lives'])
                game['Current Level'].played_defeated_sound = True
            enemy_bullet_group.empty()
            player_bullet_group.empty()
            level['Game Over'] = True
            game['Game Over Time'] = time()
            #add in lost info generation --> run one time
        else:
            level['Game Over'] = False
            
        # Level feedback
        #level_feedback.snap_to_topright()
#        level_feedback.show_to_player()
        
        game_speed_button.show()
        pause_level_button.show()
        
        # Notifying player of the incoming boss if current level has a boss
        if game['Current Level'].is_boss_level():
            if game['Current Level'].done_spawning() and len(enemy_group) > 0:
                if game['Current Level'].notified_player_about_boss is False:
                    pygame.mixer.stop()                 
                    incoming_boss_sound.play()
                    game['Current Level'].notified_player_about_boss = True
                    game['Screen Transition'] = True
                    game['Current Track'] = boss_battle_music                  
                game['Current Level'].show_boss_name_and_health()
        
        # Only showing Special attacks if the player has some to use
        if special_attacks_stats_table.dict['Rapid Fire'] > 0 or \
        special_attacks_stats_table.dict['Meteor Shower'] > 0 or \
        special_attacks_stats_table.dict['Cluster Shots'] > 0 or \
        special_attacks_stats_table.dict['Vaporizers'] > 0 or \
        special_attacks_stats_table.dict['Raining Comets'] > 0:
            special_attacks_container_label.show()
            special_attacks_container.show()
            special_attacks_container.show_timer(player_base.special_attack_in_use, player_base.special_attack_start_time, special_attacks_durations[player_base.special_attack_in_use], base_turret.stats['Special Cooldown'])
        
        # Only showing the special defenses if the player has some to use
        if special_defenses_stats_table.dict['Shock Absorbers'] > 0 or \
        special_defenses_stats_table.dict['Poison Antidote'] > 0 or \
        special_defenses_stats_table.dict['Flares'] > 0 or \
        special_defenses_stats_table.dict['Deflection'] > 0 or \
        special_defenses_stats_table.dict['Magnetic Mine'] > 0:
            special_defenses_container_label.show()
            special_defenses_container.show()
            special_defenses_container.show_timer(player_base.special_defense_in_use, player_base.special_defense_start_time, special_defenses_durations[player_base.special_defense_in_use], base_turret.stats['Special Cooldown'])       
        
        # Special Attacks Buttons showing if the player has them to use
        if special_attacks_stats_table.dict['Rapid Fire'] > 0:
            rapid_fire_button.show()
            if player_base.special_attack_in_use == 'Rapid Fire':
                rapid_fire_button.show_selected_dot()
            if special_attacks_stats_table.dict['Rapid Fire'] > 1:
                rapid_fire_button.remaining_uses.show_to_player()
                
        if special_attacks_stats_table.dict['Cluster Shots'] > 0:
            cluster_shot_button.show()
            if player_base.special_attack_in_use == 'Cluster Shots':
                cluster_shot_button.show_selected_dot()
            if special_attacks_stats_table.dict['Cluster Shots'] > 1:
                cluster_shot_button.remaining_uses.show_to_player()
                
        if special_attacks_stats_table.dict['Meteor Shower'] > 0:
            meteor_shower_button.show()
            if player_base.special_attack_in_use == 'Meteor Shower':
                meteor_shower_button.show_selected_dot()
            if special_attacks_stats_table.dict['Meteor Shower'] > 1:
                meteor_shower_button.remaining_uses.show_to_player()
                
        if special_attacks_stats_table.dict['Raining Comets'] > 0:
            raining_comets_button.show()
            if player_base.special_attack_in_use == 'Raining Comets':
                raining_comets_button.show_selected_dot()
            if special_attacks_stats_table.dict['Raining Comets'] > 1:
                raining_comets_button.remaining_uses.show_to_player()
                
        if special_attacks_stats_table.dict['Vaporizers'] > 0:
            vaporize_button.show()
            if player_base.special_attack_in_use == 'Vaporizers':
                vaporize_button.show_selected_dot()
            if special_attacks_stats_table.dict['Vaporizers'] > 1:
                vaporize_button.remaining_uses.show_to_player()
            
        # Special Defenses Buttons showing if the player has them to use
        if special_defenses_stats_table.dict['Shock Absorbers'] > 0:
            shock_absorber_button.show()
            if player_base.special_defense_in_use == 'Shock Absorbers':
                shock_absorber_button.show_selected_dot()
            if special_defenses_stats_table.dict['Shock Absorbers'] > 1:
                shock_absorber_button.remaining_uses.show_to_player()
                
        if special_defenses_stats_table.dict['Poison Antidote'] > 0:
            poison_antidote_button.show()
            if player_base.special_defense_in_use == 'Poison Antidote':
                poison_antidote_button.show_selected_dot()
            if special_defenses_stats_table.dict['Poison Antidote'] > 1:
                poison_antidote_button.remaining_uses.show_to_player()
                
        if special_defenses_stats_table.dict['Flares'] > 0:
            flares_defense_button.show()
            if player_base.special_defense_in_use == 'Flares':
                flares_defense_button.show_selected_dot()
            if special_defenses_stats_table.dict['Flares'] > 1:
                flares_defense_button.remaining_uses.show_to_player()
                
        if special_defenses_stats_table.dict['Deflection'] > 0:
            deflection_defense_button.show()
            if player_base.special_defense_in_use == 'Deflection':
                deflection_defense_button.show_selected_dot()
            if special_defenses_stats_table.dict['Deflection'] > 1:
                deflection_defense_button.remaining_uses.show_to_player()
                
        if special_defenses_stats_table.dict['Magnetic Mine'] > 0:
            magnetic_mine_button.show()
            if player_base.special_defense_in_use == 'Magnetic Mine':
                magnetic_mine_button.show_selected_dot()
            if special_defenses_stats_table.dict['Magnetic Mine'] > 1:
                magnetic_mine_button.remaining_uses.show_to_player()
        
        # Winning rewards menu slides up from the bottom of the screen to the middle
        if game['Current Level'].completed is True and level['Battle'] is True:
            level_completed_menu.show()
            continue_level_button.show()
            
        if level['Game Over'] is True and level['Restart Game'] is False:
            level_defeated_menu.show()
            level_defeated_menu.show_lost_info()
            replay_button.show()
            quit_button.show()
            
        if level['Paused'] is False:    
            power_stones_group.update()
        power_stones_group.draw(screen)  
            
        # Showing the pause level menu
        if level['Paused'] is True:
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
                game['Preview Saved Game'] = False
                if level['Abandoned'] is True:
                    player_base.stats['Health'] = game['Current Level'].player_base_starting_health
                    base_shield.stats['Health'] = game['Current Level'].base_shield_starting_health
                    level['Abandoned'] = False
                level['Screen'] = level_overworld
            elif level['Battle'] is True:
                player_base.special_attack_start_time = time()
                player_base.special_defense_start_time = time()
                player_base.special_attack_in_use = 'None'
                player_base.special_defense_in_use = 'None'
                enemy_bullet_group.empty()
                player_bullet_group.empty()
                enemy_flares_group.empty()
                health_flares_group.empty()
                enemy_group.empty()
                game['Preview Level'] = False
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
                enemy_flares_group.empty()
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
            #show_variable('{:.2f}'.format(CLOCK.get_fps()), debug_font, (200, 660))
        #show_variable(f'Attack active = {player_base.special_attack_used}', debug_font, (200, 600))
        #show_variable(f'Attack in use = {player_base.special_attack_in_use}', debug_font, (200, 630))
        #show_variable(f'{len(enemy_flares_group)}', debug_font, (200, 630))
        
        CLOCK.tick()
        pygame.display.update()
        
if __name__ == "__main__":
    #profile.run('main()')
    main()
    
pygame.quit()