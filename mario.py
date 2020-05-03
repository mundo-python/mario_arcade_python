import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
SCREEN_TITLE = "Mario Demo"

#Constantes para escalar los sprites
CHARACTER_SCALING = 0.17
GROUND_SCALING = 0.20
CYLINDER_SCALING = 0.20

#SPEED PLAYER
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

class MyGame(arcade.Window):

	def __init__(self):

		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

		arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

		self.coin_list = None
		self.wall_list = None
		self.player_list = None

		#Variable del sprite jugador
		self.player_sprite = None

		# Used to keep track of our scrolling
		self.view_bottom = 0
		
		self.view_left = 0

	def setup(self):
		self.player_list = arcade.SpriteList()
		self.wall_list = arcade.SpriteList()
		self.coin_list = arcade.SpriteList()

		#Player
		image_source = "mario.png"
		self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
		self.player_sprite.center_x = 64
		self.player_sprite.center_y = 93
		self.player_list.append(self.player_sprite)

		# Create the ground
		# This shows using a loop to place multiple sprites horizontally
		for x in range(0, 1250, 64):
			wall = arcade.Sprite("ground.png", GROUND_SCALING)
			wall.center_x = x
			wall.center_y = 32
			self.wall_list.append(wall)

			# This shows using a coordinate list to place sprites
		coordinate_list = [[512, 110],
							[256, 110],
							[768, 110]]

		for coordinate in coordinate_list:
			# Add a crate on the ground
			wall = arcade.Sprite("cylinder.png", CYLINDER_SCALING)
			wall.position = coordinate
			self.wall_list.append(wall)

		#Creathe the "physics engine"
		self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)
	
	def on_draw(self):
		arcade.start_render()
		self.player_list.draw()
		self.wall_list.draw()

	def on_key_press(self, key, modifiers):
		"""Called whenever a key is pressed. """

		if key == arcade.key.UP or key == arcade.key.W:
			if self.physics_engine.can_jump():
				self.player_sprite.change_y = PLAYER_JUMP_SPEED
		elif key == arcade.key.LEFT or key == arcade.key.A:
			self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
		elif key == arcade.key.RIGHT or key == arcade.key.D:
			self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

	def on_key_release(self, key, modifiers):
		"""Called when the user releases a key. """

		if key == arcade.key.LEFT or key == arcade.key.A:
			self.player_sprite.change_x = 0
		elif key == arcade.key.RIGHT or key == arcade.key.D:
			self.player_sprite.change_x = 0

	def on_update(self, delta_time):
		""" Movement and game logic """

		# Move the player with the physics engine
		self.physics_engine.update()

		# --- Manage Scrolling ---

        # Track if we need to change the viewport

		changed = False

        # Scroll left
		left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
		if self.player_sprite.left < left_boundary:
			self.view_left -= left_boundary - self.player_sprite.left
			changed = True

		# Scroll right
		right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
		if self.player_sprite.right > right_boundary:
			self.view_left += self.player_sprite.right - right_boundary
			changed = True

		# Scroll up
		top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
		if self.player_sprite.top > top_boundary:
			self.view_bottom += self.player_sprite.top - top_boundary
			changed = True

        # Scroll down
		bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
		if self.player_sprite.bottom < bottom_boundary:
			self.view_bottom -= bottom_boundary - self.player_sprite.bottom
			changed = True

		if changed:
			# Only scroll to integers. Otherwise we end up with pixels that
			# don't line up on the screen
			self.view_bottom = int(self.view_bottom)
			self.view_left = int(self.view_left)

			# Do the scrolling
			arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom,SCREEN_HEIGHT + self.view_bottom)

def main():
	window = MyGame()
	window.setup()
	arcade.run()

if __name__ == "__main__":
	main()