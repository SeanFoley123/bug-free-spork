    def update(self):
        """ Update the player position. """
        # Check changes in position. If not on the ground, calculate gravity. Move left or right.
        self.calc_grav()
        self.rect.x += self.change_x
 
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.room.wall_list, False)
        for block in block_hit_list:
            # Check if it is deadly. If so, hurt the player
            if block.mortality == True:
                self.wound += 1
                if self.wound > self.max_wound:
                    self.kill()
            else:
                # If we are moving right, set our right side to the left side of the item we hit
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                else:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right
                self.wound = 0 # reset health if not only touching the deadly object. Currently lets you survive if touching the ground and the lava.

        # Did this update cause us to enter water or other speed-altering substance? If so, change speed by the viscosity of the substance.
        block_hit_list = pygame.sprite.spritecollide(self, self.room.sludge, False)
        for block in block_hit_list:
            self.rect.x -= self.change_x*block.visc

        ### Move up/down and repeat previous steps for the vertical movement
        self.rect.y += self.change_y
 
        block_hit_list = pygame.sprite.spritecollide(self, self.room.wall_list, False)
        for block in block_hit_list:
            if block.mortality == True:
                self.wound += 1
                if self.wound > self.max_wound:
                    self.kill()
            else:
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                else:
                    self.rect.top = block.rect.bottom

                # Stop our vertical movement if landing on something.
                self.change_y = 0
                self.wound = 0

        block_hit_list = pygame.sprite.spritecollide(self, self.room.sludge, False)
        for block in block_hit_list:
            self.rect.y -= self.change_y*block.visc

        ### Check for collisions where x/y doesn't matter: enemies, food, and objects to climb.
        enemy_hit_list = pygame.sprite.spritecollide(self, self.room.enemy_list, False)
        for enemy in enemy_hit_list:
            if enemy.mortality == True:
                self.kill()

        food_hit_list = pygame.sprite.spritecollide(self, self.room.consumeable, True)
        for food in food_hit_list:
            self.corruption += food.corr_points # If the food is immorally eaten, increase corruption

        if pygame.sprite.spritecollide(self, self.room.can_climb, False) != []:
            self.climb_okay = True
        else:
            self.climb_okay = False

        # Update the player picture if necessary
        self.how_corrupt()

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground, don't fall if we are.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def climb(self):
        """ If player hits 'c,' they climb upwards in a burst of 5 pixels. """
        self.change_y = -5