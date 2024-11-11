import pygame
import Setting
from tank_logic import TankLogic
import math
from bullet import Bullet
from bullet_Lazer import Laser
from Minibullet import Minigun
from Static_object import normal_tanks,shot_frames,minigun_shot_frames
from explosion import Animation
import Sound
from missile import Missile
class TankControl:
    def __init__(self, tank, window_width, window_height,bullets,lasers,missiles,control_setting):
        self.tank = tank #chuyen tham so cua xe tang vao bao gom kich co vi tri goc quay
        self.window_width = window_width #tham so man hinh game
        self.window_height = window_height
        self.bullets=bullets
        self.lasers=lasers
        self.missiles=missiles
        self.last_shoot=0
        self.control_setting=control_setting
    def handle_input(self,explosion_bull):#doc event hay doc input cua pygame
        keys = pygame.key.get_pressed()
        if keys[self.control_setting['up']] :
            TankLogic.move_tank(self.tank, self.tank.tank_speed + float(self.tank.speed_add), self.window_width, self.window_height) #goi den ham di chuyen nha ae
        if keys[self.control_setting['down']]:
            TankLogic.move_tank(self.tank, -self.tank.tank_speed - float(self.tank.speed_add), self.window_width, self.window_height)
        if keys[self.control_setting['right']]:
            TankLogic.rotate_tank(self.tank, -Setting.angle)
        if keys[self.control_setting['left']]:
            TankLogic.rotate_tank(self.tank, +Setting.angle)
        if keys[self.control_setting['shoot']]:
            current_time = pygame.time.get_ticks()
            if self.tank.gun_mode == 1:
                if   (current_time-self.last_shoot) >1000  and len(self.bullets) <100  :
                    bullet = Bullet(self.tank,
                        self.tank.tank_rect.centerx + 29 * math.cos(math.radians(self.tank.tank_angle)),
                        self.tank.tank_rect.centery - 29 * math.sin(math.radians(self.tank.tank_angle)),
                        self.tank.tank_angle)
                    self.bullets.append(bullet)
                    self.last_shoot=current_time
                    Sound.bullet_sound.play()
                    animation=Animation(self.tank.tank_rect.centerx + 55 * math.cos(math.radians(self.tank.tank_angle)),
                         self.tank.tank_rect.centery - 55 * math.sin(math.radians(self.tank.tank_angle)),shot_frames,self.tank.tank_angle,128,128,1000)
                    explosion_bull.append(animation)
            elif self.tank.gun_mode == 2:
                laser=Laser(self.tank,self.tank.tank_rect.centerx + 29 * math.cos(math.radians(self.tank.tank_angle)),
                            self.tank.tank_rect.centery - 29 * math.sin(math.radians(self.tank.tank_angle)),
                            self.tank.tank_angle)
                self.lasers.append(laser)
                self.tank.tank_laser.active =True #Khi bam shot tuc la tia laser da duoc active
                self.tank.gun_mode =1 #lap tuc chuyen gun_mode ve mac dinh
                #image_path = Setting.asset + Setting.tanks_img[self.tank.id]
                self.tank.update_tank_image(normal_tanks[self.tank.id])
                Sound.laser_sound.play()
                self.last_shoot = current_time

            elif self.tank.gun_mode == 3:
                if (current_time - self.last_shoot) > 200:
                    minibull_1=Minigun(self.tank,
                        self.tank.tank_rect.centerx + 29 * math.cos(math.radians(self.tank.tank_angle+15)),
                        self.tank.tank_rect.centery - 29 * math.sin(math.radians(self.tank.tank_angle+15)),
                        self.tank.tank_angle)
                    minibull_2=Minigun(self.tank,
                        self.tank.tank_rect.centerx + 29 * math.cos(math.radians(self.tank.tank_angle)),
                        self.tank.tank_rect.centery - 29 * math.sin(math.radians(self.tank.tank_angle)),
                        self.tank.tank_angle)
                    minibull_3=Minigun(self.tank,
                        self.tank.tank_rect.centerx + 29 * math.cos(math.radians(self.tank.tank_angle-15)),
                        self.tank.tank_rect.centery - 29 * math.sin(math.radians(self.tank.tank_angle-15)),
                        self.tank.tank_angle)
                    self.last_shoot=current_time
                    self.bullets.append(minibull_1)
                    self.bullets.append(minibull_2)
                    self.bullets.append(minibull_3)
                    animation = Animation(
                        self.tank.tank_rect.centerx + 35 * math.cos(math.radians(self.tank.tank_angle)),
                        self.tank.tank_rect.centery - 35 * math.sin(math.radians(self.tank.tank_angle)),
                        minigun_shot_frames, self.tank.tank_angle,64,64,156)
                    explosion_bull.append(animation)
                    Sound.machine_gun_sound.play()
                    self.tank.minigun_bull_count +=3
            elif self.tank.gun_mode == 4:
                missile=Missile(self.tank,
                        self.tank.tank_rect.centerx + 24 * math.cos(math.radians(self.tank.tank_angle+16)),
                        self.tank.tank_rect.centery - 24 * math.sin(math.radians(self.tank.tank_angle+16)),
                        self.tank.tank_angle)
                self.missiles.append(missile)
                self.tank.gun_mode=1
                #image_path = Setting.asset + Setting.tanks_img[self.tank.id]
                self.tank.update_tank_image(normal_tanks[self.tank.id])
                self.last_shoot=pygame.time.get_ticks()
                Sound.missile_shot_sound.play()