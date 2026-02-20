import arcade
import math
import random

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Space Shooter"

PLAYER_SCALE = 0.2
PLAYER_SPEED = 5
PLAYER_TURN_SPEED = 3
PLAYER_SHOOT_COOLDOWN = 0.1

BULLET_SPEED = 10
BULLET_SCALE = 0.6

ENEMY_SPAWN_RATE = 1
ENEMY_MIN_SPEED = 1
ENEMY_MAX_SPEED = 3
ENEMY_SCALE = 0.2

ENEMY_TYPES = ["normal", "shooter"]
ENEMY_SHOOT_COOLDOWN = 2.0
ENEMY_BULLET_SPEED = 5
ENEMY_BULLET_COLOR = arcade.color.RED


class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.power_type = power_type
        self.radius = 15
        self.speed_y = -1

        if power_type == "rapid_fire":
            self.color = arcade.color.CYAN
        elif power_type == "shield":
            self.color = arcade.color.BLUE
        else:
            self.color = arcade.color.GREEN
        
    def update(self):
        self.y += self.speed_y
    
    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)
        if self.power_type == "rapid_fire":
            arcade.draw_text("⚡", self.x - 4, self.y - 4, arcade.color.WHITE, 10)
        if self.power_type == "shield":
            arcade.draw_text("🛡️", self.x - 4, self.y - 4, arcade.color.WHITE, 10)
        else:
            arcade.draw_text("❤️", self.x - 4, self.y - 4, arcade.color.WHITE, 10)


class EnemyBullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = ENEMY_BULLET_SPEED
        self.radius = 6
        self.color = ENEMY_BULLET_COLOR

    def update(self):
        # Move bullet according to the angle
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
    
    def draw(self):
        arcade.draw_circle_filled(
            self.x, self.y, self.radius, self.color
        )
    
    def is_off_screen(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT)


class Enemy:
    def __init__(self):
        side = random.choice(["top", "right", "bottom", "left"])
        if side == "top":
            self.x = random.uniform(0, SCREEN_WIDTH)
            self.y = SCREEN_HEIGHT + 20
        elif side == "right":
            self.x = SCREEN_WIDTH + 20
            self.y = random.uniform(0, SCREEN_HEIGHT)
        elif side == "bottom":
            self.x = random.uniform(0, SCREEN_WIDTH)
            self.y = -20
        else:
            self.x = -20
            self.y = random.uniform(0, SCREEN_HEIGHT)
        
        self.enemy_type = random.choices(ENEMY_TYPES, weights=[4, 1])[0]
        self.speed = random.uniform(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
        self.angle = 0
        self.radius = 150 * ENEMY_SCALE
        self.max_health = 3
        self.health = self.max_health
        self.shoot_cooldown = 0

    def take_damage(self):
        self.health -= 1
        return self.health <= 0
    
    def update(self, player_x, player_y, delta_time):
        dx = player_x - self.x
        dy = player_y - self.y
        self.angle = math.degrees(math.atan2(dy, dx))

        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

        if self.enemy_type == "shooter":
            self.shoot_cooldown -= delta_time
    
    def shoot(self):
        if self.enemy_type == "shooter" and self.shoot_cooldown <= 0:
            bullet_x = self.x + \
                math.cos(math.radians(self.angle)) * self.radius
            bullet_y = self.y + \
                math.sin(math.radians(self.angle)) * self.radius
            self.shoot_cooldown = ENEMY_SHOOT_COOLDOWN
            return EnemyBullet(bullet_x, bullet_y, self.angle)
        return None
    
    def draw(self):
        if self.enemy_type == "shooter":
            color = arcade.color.RED
        else:
            color = arcade.color.BLUE

        arcade.draw_triangle_filled(
            self.x + math.cos(math.radians(self.angle)) * self.radius * 2,
            self.y + math.sin(math.radians(self.angle)) * self.radius * 2,
            self.x + math.cos(math.radians(self.angle + 140)) * self.radius,
            self.y + math.sin(math.radians(self.angle + 140)) * self.radius,
            self.x + math.cos(math.radians(self.angle - 140)) * self.radius,
            self.y + math.sin(math.radians(self.angle - 140)) * self.radius,
            color
        )

    def draw_health_bar(self):
        if self.health < self.max_health:
            bar_width = 50
            bar_height = 6
            health_percentage = self.health / self.max_health
            health_width = health_percentage * bar_width

            bar_x = self.x - bar_width / 2
            bar_y = self.y + self.radius + 10

            arcade.draw_lbwh_rectangle_filled(
                bar_x, bar_y, bar_width, bar_height, arcade.color.RED
            )
            arcade.draw_lbwh_rectangle_filled(
                bar_x, bar_y, health_width, bar_height, arcade.color.GREEN
            )
            arcade.draw_lbwh_rectangle_outline(
                bar_x, bar_y, bar_width, bar_height, arcade.color.WHITE
            )

    def is_off_screen(self):
        return (self.x < -50 or self.x > SCREEN_WIDTH + 50 or self.y < -50 or self.y > SCREEN_HEIGHT+50)


class BossBullet:
    def __init__(self, x, y, angle, is_big=False):
        self.x = x
        self.y = y
        self.angle = angle
        self.is_big = is_big
        self.speed = 7
        self.damage = 999 if is_big else 30

        if is_big:
            self.radius = 12
            self.color = arcade.color.YELLOW
        else:
            self.radius = 6
            self.color = arcade.color.ORANGE_RED
    
    def update(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
    
    def draw(self):
        arcade.draw_circle_filled(
            self.x, self.y, self.radius, self.color
        )
    
    def is_off_screen(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT)


class Boss:
    def __init__(self):
        self.x = SCREEN_WIDTH //2 + random.uniform(-200, 200)
        self.y = SCREEN_HEIGHT + 100

        self.speed = 2
        self.angle = 0
        self.radius = 150 * ENEMY_SCALE * 3
        self.max_health = 100
        self.health = self.max_health

        self.normal_shoot_cooldown = 0
        self.big_shoot_cooldown = 0
        self.attack_cooldown = 0
        self.damage_flash_timer = 0
        self.flashing = False

        self.entering = True
        self.target_y = SCREEN_HEIGHT - 150

        self.color = arcade.color.ORANGE
    
    def take_damage(self):
        self.health -= 1
        self.damage_flash_timer = 0.3
        self.flashing = True
        return self.health <= 0
    
    def update(self, player_x, player_y, delta_time):
        if self.entering:
            self.y -= self.speed

            if self.y <= self.target_y:
                self.y = self.target_y
                self.entering = False

        else:
            dx = player_x - self.x
            dy = player_y - self.y
            self.angle = math.degrees(math.atan2(dy, dx))

            self.x += math.cos(math.radians(self.angle)) * self.speed
            self.y += math.sin(math.radians(self.angle)) * self.speed

        self.normal_shoot_cooldown -= delta_time
        self.big_shoot_cooldown -= delta_time
        self.attack_cooldown -= delta_time

        if self.flashing:
            self.damage_flash_timer -= delta_time
            if self.damage_flash_timer <= 0:
                self.flashing = False
        
    def choose_attack(self):
        attacks = ["normal", "big"]
        weights = [7, 3]

        return random.choices(attacks, weights=weights)[0]

    def shoot_normal(self):
        if self.normal_shoot_cooldown <= 0:
            bullet_x = self.x + \
                math.cos(math.radians(self.angle)) * self.radius
            bullet_y = self.y + \
                math.sin(math.radians(self.angle)) * self.radius

            self.normal_shoot_cooldown = 1.5
            return BossBullet(bullet_x, bullet_y, self.angle, is_big=False)
        return None
    
    def shoot_big(self):
        if self.big_shoot_cooldown <= 0:
            bullet_x = self.x + \
                math.cos(math.radians(self.angle)) * self.radius
            bullet_y = self.y + \
                math.sin(math.radians(self.angle)) * self.radius

            self.big_shoot_cooldown = 8.0
            return BossBullet(bullet_x, bullet_y, self.angle, is_big=True)
        return None
    
    def attack(self):
        if self.attack_cooldown > 0:
            return []
        
        self.attack_cooldown = 2.5
        attack_type = self.choose_attack()

        if attack_type == "normal":
            return [self.shoot_normal()]
        elif attack_type == "big":
            return [self.shoot_big()]

        return []

    
    def draw(self):
        draw_color = arcade.color.WHITE if self.flashing else self.color

        points = [
            (self.x + math.cos(math.radians(self.angle)) * self.radius * 1.5,
             self.y + math.sin(math.radians(self.angle)) * self.radius * 1.5),
            (self.x + math.cos(math.radians(self.angle + 90)) * self.radius,
             self.y + math.sin(math.radians(self.angle + 90)) * self.radius),
            (self.x + math.cos(math.radians(self.angle + 180)) * self.radius * 1.5,
             self.y + math.sin(math.radians(self.angle + 180)) * self.radius * 1.5),
            (self.x + math.cos(math.radians(self.angle + 270)) * self.radius,
             self.y + math.sin(math.radians(self.angle + 270)) * self.radius),
        ]
        arcade.draw_polygon_filled(points, draw_color)

    def draw_health_bar(self):
        bar_width = 200
        bar_height = 15
        health_percentage = self.health / self.max_health
        health_width = health_percentage * bar_width

        bar_x = self.x - bar_width / 2
        bar_y = self.y + self.radius + 10

        arcade.draw_lbwh_rectangle_filled(
            bar_x, bar_y, bar_width, bar_height, arcade.color.RED
        )

        if health_percentage > 0.7:
            health_color = arcade.color.GREEN
        elif health_percentage > 0.4:
            health_color = arcade.color.YELLOW
        else:
            health_color = arcade.color.ORANGE
        
        arcade.draw_lbwh_rectangle_filled(
            bar_x, bar_y, health_width, bar_height, health_color
        )
        arcade.draw_lbwh_rectangle_outline(
            bar_x, bar_y, bar_width, bar_height, arcade.color.WHITE
        )

        arcade.draw_text(
            f"BOSS HP: {self.health}/{self.max_health}",
            bar_x-80,
            bar_y + 25,
            arcade.color.WHITE,
            12
        )

    def is_off_screen(self):
        return (self.x < -100 or self.x > SCREEN_WIDTH+100 or self.y < -100 or self.y > SCREEN_HEIGHT+100)



class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = BULLET_SPEED
        self.radius = BULLET_SCALE * 4
        
    def update(self):
        # Move bullet according to the angle
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
    
    def draw(self):
        arcade.draw_circle_filled(
            self.x, self.y, self.radius, arcade.color.YELLOW
        )
    
    def is_off_screen(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT)


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
        arcade.set_background_color(arcade.color.BLACK)

        self.player_x = SCREEN_WIDTH//2
        self.player_y = SCREEN_HEIGHT//2
        self.player_angle = 0
        self.player_radius = 150 * PLAYER_SCALE

        self.bullets = []
        self.shoot_cooldown = 0

        self.enemies = []
        self.enemy_spawn_timer = ENEMY_SPAWN_RATE

        self.health = 100
        self.score = 0
        self.highscore = self.load_highscore()
        self.game_over = False

        self.enemy_bullets = []

        self.boss = None
        self.next_boss_score = 500
        self.boss_bullets = []

        self.powerups = []
        self.rapid_fire_timer = 0.0
        self.shield_timer = 0.0

        self.keys_pressed = set()
    
    def on_draw(self):
        self.clear()

        # Drawing Player
        arcade.draw_triangle_filled(
            self.player_x + math.cos(math.radians(self.player_angle)) * self.player_radius * 1.5,
            self.player_y + math.sin(math.radians(self.player_angle)) * self.player_radius * 1.5,
            self.player_x + math.cos(math.radians(self.player_angle + 150)) * self.player_radius,
            self.player_y + math.sin(math.radians(self.player_angle + 150)) * self.player_radius,
            self.player_x + math.cos(math.radians(self.player_angle - 150)) * self.player_radius,
            self.player_y + math.sin(math.radians(self.player_angle - 150)) * self.player_radius,
            arcade.color.WHITE
        )

        for bullet in self.bullets:
            bullet.draw()
        
        for enemy in self.enemies:
            enemy.draw()
            enemy.draw_health_bar()
        
        for bullet in self.enemy_bullets:
            bullet.draw()
        
        for bullet in self.boss_bullets:
            bullet.draw()

        for powerup in self.powerups:
            powerup.draw()

        if self.boss:
            self.boss.draw()
            self.boss.draw_health_bar()
        
        if self.game_over:
            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.RED,
                40,
                anchor_x="center"
            )

            arcade.draw_text(
                "Press R to Restart",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 - 20,
                arcade.color.WHITE,
                18,
                anchor_x="center"
            )
        
        arcade.draw_text(
            f"Score: {self.score}",
            10,
            SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            f"Health: {self.health}",
            10,
            SCREEN_HEIGHT - 60,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            f"Highscore: {self.highscore}",
            10,
            SCREEN_HEIGHT - 90,
            arcade.color.YELLOW,
            16
        )

        if self.shield_timer > 0:
            arcade.draw_circle_outline(
                self.player_x,
                self.player_y,
                self.player_radius + 10,
                arcade.color.CYAN,
                3
            )
        
        y_offset = SCREEN_HEIGHT - 120

        if self.rapid_fire_timer > 0:
            arcade.draw_text(
                f"Rapid Fire: {self.rapid_fire_timer:.1f}s",
                10,
                y_offset,
                arcade.color.CYAN,
                14
            )
            y_offset -= 25

        if self.shield_timer > 0:
            arcade.draw_text(
                f"Shield: {self.shield_timer:.1f}s",
                10,
                y_offset,
                arcade.color.BLUE,
                14
            )


    
    def on_update(self, delta_time):
        if self.game_over:
            return

        self.enemy_spawn_timer -= delta_time

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= delta_time

        if arcade.key.SPACE in self.keys_pressed:
            self.shoot()

        if self.enemy_spawn_timer <= 0 and self.boss is None:
            self.enemies.append(Enemy())
            self.enemy_spawn_timer = ENEMY_SPAWN_RATE

        if arcade.key.W in self.keys_pressed:
            self.player_y += PLAYER_SPEED
        if arcade.key.S in self.keys_pressed:
            self.player_y -= PLAYER_SPEED
        if arcade.key.A in self.keys_pressed:
            self.player_x -= PLAYER_SPEED
        if arcade.key.D in self.keys_pressed:
            self.player_x += PLAYER_SPEED
        
        self.player_x = max(self.player_radius, min(SCREEN_WIDTH - self.player_radius, self.player_x))
        self.player_y = max(self.player_radius, min(SCREEN_HEIGHT - self.player_radius, self.player_y))

        if self.boss is None and self.score >= self.next_boss_score:
            self.boss = Boss()
            self.next_boss_score += 500


        if self.boss:
            self.boss.update(self.player_x, self.player_y, delta_time)

            if not self.boss.entering:
                bullets = self.boss.attack()

                for bullet in bullets:
                    if bullet:
                        self.boss_bullets.append(bullet)

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
        
        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.y < 0:
                self.powerups.remove(powerup)

        # Enemy collision with Bulllet
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                dx = bullet.x - enemy.x
                dy = bullet.y - enemy.y
                if dx*dx + dy*dy < (bullet.radius + enemy.radius)**2:
                    enemy.take_damage() # Fix this optimizatin in every collision check
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.score += 20 if enemy.enemy_type == "shooter" else 10 
                        if random.random() < 0.2:   # for a 20% drop chance
                            power_type = random.choices(["rapid_fire", "shield", "health"], weights=[5, 3, 2])[0]
                            self.powerups.append(
                                PowerUp(enemy.x, enemy.y, power_type)
                            )
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break

        # Player bullets vs Enemy bullets
        for bullet in self.bullets[:]:
            for e_bullet in self.enemy_bullets[:]:

                distance = math.sqrt((bullet.x - e_bullet.x) ** 2 +(bullet.y - e_bullet.y) ** 2)

                if distance < bullet.radius + e_bullet.radius:

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

                    if e_bullet in self.enemy_bullets:
                        self.enemy_bullets.remove(e_bullet)

                    break
        
        # Enemy bullet collision with player
        for bullet in self.enemy_bullets[:]:
            bullet.update()

            distance = math.sqrt((bullet.x - self.player_x) ** 2 +(bullet.y - self.player_y) ** 2)
            if distance < bullet.radius + self.player_radius:
                if self.shield_timer <= 0:
                    self.health -= 5
                self.enemy_bullets.remove(bullet)

                if self.health <= 0:
                    self.game_over = True

                    if self.score > self.highscore:
                        self.highscore = self.score
                        self.save_highscore()
                continue

            if bullet.is_off_screen():
                self.enemy_bullets.remove(bullet)
        
        # Enemy collision with Player
        for enemy in self.enemies[:]:
            enemy.update(self.player_x, self.player_y, delta_time)

            enemy_bullet = enemy.shoot()
            if enemy_bullet:
                self.enemy_bullets.append(enemy_bullet)

            distance = math.sqrt((enemy.x - self.player_x)**2 + (enemy.y - self.player_y)**2)
            if distance < enemy.radius + self.player_radius:
                if self.shield_timer <= 0:
                    self.health -= 10
                self.enemies.remove(enemy)
                if self.health <= 0:
                    self.game_over = True

                    if self.score > self.highscore:
                        self.highscore = self.score
                        self.save_highscore()

            elif enemy.is_off_screen():
                self.enemies.remove(enemy)
        
        # Boss Bullet vs Player
        for bullet in self.boss_bullets[:]:
            bullet.update()

            distance = math.sqrt((bullet.x - self.player_x) ** 2 + (bullet.y - self.player_y) ** 2)

            if distance < bullet.radius + self.player_radius:
                self.health -= bullet.damage
                self.boss_bullets.remove(bullet)

                if self.health <= 0:
                    self.game_over = True

            elif bullet.is_off_screen():
                self.boss_bullets.remove(bullet)
        
        # Player bullet vs Boss
        boss = self.boss

        if boss:
            for bullet in self.bullets[:]:
                distance = math.sqrt((bullet.x - self.boss.x) ** 2 + (bullet.y - self.boss.y) ** 2)

                if distance < bullet.radius + self.boss.radius:
                    self.boss.take_damage()
                    self.bullets.remove(bullet)

                    if self.boss.health <= 0:
                        self.score += 200
                        self.boss = None
                        break
        
        # Power-ups vs Player Collision
        for powerup in self.powerups[:]:
            dx = self.player_x - powerup.x
            dy = self.player_y - powerup.y

            if dx*dx + dy*dy < (self.player_radius + powerup.radius) ** 2:

                if powerup.power_type == "rapid_fire":
                    self.rapid_fire_timer = 10.0

                elif powerup.power_type == "shield":
                    self.shield_timer = 15.0

                elif powerup.power_type == "health":
                    self.health = self.health + 50

                self.powerups.remove(powerup)
        
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer -= delta_time
        if self.shield_timer > 0:
            self.shield_timer -= delta_time

    # FIX: implement the powerup class properly
        
    def shoot(self):
        if self.shoot_cooldown > 0:
            return

        bullet_x = self.player_x + \
            math.cos(math.radians(self.player_angle)) * self.player_radius
        bullet_y = self.player_y + \
            math.sin(math.radians(self.player_angle)) * self.player_radius
        self.bullets.append(Bullet(bullet_x, bullet_y, self.player_angle))
        # self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        
        # self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN /3 if self.rapid_fire_timer > 0 else PLAYER_SHOOT_COOLDOWN
        if self.rapid_fire_timer > 0:
            self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN / 3
        else:
            self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        
        # print("cooldown set to:", PLAYER_SHOOT_COOLDOWN)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

        if self.game_over and key == arcade.key.R:
            self.restart_game()
    
    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
    
    def on_mouse_motion(self, x, y, dx, dy):
        dx = x - self.player_x
        dy = y - self.player_y
        self.player_angle = math.degrees(math.atan2(dy, dx))
    
    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except:
            return 0
    
    def save_highscore(self):
        with open("highscore.txt", "w") as file:
            file.write(str(self.highscore))
    
    def restart_game(self):
        self.player_x = SCREEN_WIDTH//2
        self.player_y = SCREEN_HEIGHT//2
        self.player_angle = 0
        self.bullets.clear()
        self.enemies.clear()
        self.enemy_bullets.clear()
        self.score = 0
        self.health = 100
        self.boss = None
        self.boss_bullets.clear()
        self.next_boss_score = 500
        self.boss = None
        self.powerups.clear()
        self.game_over = False
    

def main():
    window = GameWindow()
    arcade.run()

if __name__ == "__main__":
    main()
