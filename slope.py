import pygame as pg 
import math,pytmx,json


WIDTH,HEIGHT = 640,640
SCREEN = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption('Rampas')


class TileMap:
	def __init__(self,filename):
		tm = pytmx.load_pygame(filename,pixelaplha = True)
		self.width = tm.width * tm.tilewidth
		self.height = tm.height * tm.tileheight
		self.tmxdata = tm

	def render(self,surface):
		ti = self.tmxdata.get_tile_image_by_gid
		for layer in self.tmxdata.visible_layers:
			if isinstance(layer,pytmx.TiledTileLayer):
				for x,y,gid in layer:
					tile = ti(gid)
					if tile: surface.blit(tile,(x* self.tmxdata.tilewidth,y* self.tmxdata.tileheight))
						
	def make_map(self):

		temp_surface = pg.Surface((self.width,self.height)) #pg.SRCALPHA
		temp_surface.set_colorkey((0,0,0))	
		self.render(temp_surface)
		#temp_surface.convert_alpha()
		
		return temp_surface

class Sprite:
	def __init__(self,pos):
		self.image = pg.Surface((20,20))
		self.image.fill((255,255,255))
		self.rect = self.image.get_rect()
		self.rect.centerx = pos[0]
		self.rect.centery = pos[1] 

		self.vly = 0
		self.vlx = 0
		self.vl = 7
		self.f_g = 0.65


	def update(self):
		self.gravity()
		self.rect.centerx += self.vlx
		self.rect.centery += self.vly


	def draw(self,screen):
		screen.blit(self.image,self.rect)


	def gravity(self):
		if self.vly == 0:
			self.vly = 1
		elif self.vly < 7:
			self.vly += self.f_g


class Pasto:
	def __init__(self,pos,size):
		self.rect = pg.Rect(pos,size)

	
	def update(self,player):
		self.collided(player)


	def collided(self,player):
		if self.rect.colliderect(player.rect):
			player.rect.bottom = self.rect.top

class Rampa:
	def __init__(self,pos,angle = 45,size_x = 1):
		self.angle = int(angle)  
		self.pos_inicio = pos
		#self.image = pg.image.load('rampa.png')
		
		#if self.angle == -45:
			#self.image = pg.transform.flip(self.image,1,0)
			#self.pos_inicio = (pos[0], pos[1])


		#self.image = pg.transform.scale(self.image,(32,32))
		distancia = 45 * int(size_x)

		#la función seno y coseno funciona solo con radianes
		radianes = math.radians(self.angle)

		x_destino = self.pos_inicio[0] + distancia *math.cos(radianes)
		y_destino = self.pos_inicio[1] + distancia *math.sin(radianes)
		self.pos_destino = (x_destino,y_destino)


		self.escalera = []
		for i in range(distancia):
			desplazamiento = i 
			pos_x = self.pos_inicio[0] + desplazamiento *math.cos(radianes)
			pos_y = self.pos_inicio[1] + desplazamiento *math.sin(radianes)

			rect = pg.Rect((pos_x,pos_y),(1,1))
			self.escalera.append(rect)

		#if self.angle == -45:
		#	self.pos_inicio = (self.pos_inicio[0], self.pos_inicio[1] - 32)


	def update(self,player):
		self.collided(player)


	def draw(self,SCREEN):
		#pg.draw.line(SCREEN,(255,255,255),self.pos_inicio,self.pos_destino) 
		
		#SCREEN.blit(self.image,self.pos_inicio)
		#dibujar para debugear
		for i in self.escalera:
			pg.draw.rect(SCREEN,(255,255,255),i)


	def collided(self,player):
		for i in self.escalera:
			if i.colliderect(player.rect):
				if self.angle == 45 or self.angle == -45:
					player.rect.bottom = i.top
				elif self.angle <= -133:
					player.rect.top = i.bottom  


class Game:
	def __init__(self):
		self.maps = ['map_0.tmx']
		self.map = TileMap(self.maps[0])
		self.surface = self.map.make_map()
		self.rampas = []
		self.pastos = []

		self.load()
		self.player = Sprite((100,200))


	def load(self):
		for tile_object in self.map.tmxdata.objects:
			pos = (tile_object.x,tile_object.y)

			if tile_object.name == 'pasto':
				size = (tile_object.width,tile_object.height)
				self.pastos.append(Pasto(pos,size))

			elif tile_object.name == 'rampa':
				grado,size = tile_object.type.split(',')

				self.rampas.append(
					Rampa(
						pos,
						grado,
						size,
						)
					) 


	def update(self):

		self.player.update()


		for rampa in self.rampas:
			rampa.update(self.player)

		for pasto in self.pastos:
			pasto.update(self.player)




	def draw(self,SCREEN):
		SCREEN.fill((100,100,100))
		SCREEN.blit(self.surface,(0,0))
		
		#debugear
		for rampa in self.rampas:
			rampa.draw(SCREEN)
			
		self.player.draw(SCREEN)





def main():

	exit = 0
	game = Game()

	#-------------Rampas
	#rampa = Rampa((96,100))
	#rampa2 = Rampa((128,132))
	#rampa3 = Rampa((192,100),-45)
	#rampas = [rampa,rampa2,rampa3]
	#-------------Pasto
	#pasto = Pasto((200,200))
	#pasto2 = Pasto((0,100))

	

	#list_pasto = []
	#for i in range(3):
		#list_pasto.append(Pasto((0 + 32*i,100)))

	
	#list_tierra = []
	#img_tierra = pg.image.load('tierra.png')
	#for i in range(4):
		#tile = (img_tierra,(0 + 32*i,132))
		#list_tierra.append(tile)

	#-------------PASTO parte baja
	#-----------------------------

	#for i in range(2):
		#pos = (128 + 32*i,132)
		#list_pasto.append(Pasto(pos))




	#FPS
	clock = pg.time.Clock()

	while exit != 1:

		clock.tick(60)

		for event in pg.event.get():
			if event.type == pg.QUIT:
				exit = 1

			if event.type == pg.KEYDOWN:
				if event.key == pg.K_UP:
					game.player.vly = -7
				if event.key == pg.K_RIGHT:
					game.player.vlx = 5
				if event.key == pg.K_LEFT:
					game.player.vlx = -5

			if event.type == pg.KEYUP:
				if event.key == pg.K_RIGHT:
					game.player.vlx = 0
				if event.key == pg.K_LEFT:
					game.player.vlx = 0



		# for rampa in rampas:
		# 	rampa.update(p1)
		# 	rampa.draw(SCREEN)
		
		# for pasto in list_pasto:
		# 	pasto.update(p1)
		# 	pasto.draw(SCREEN)

		# for tierra in list_tierra:
		# 	SCREEN.blit(tierra[0],tierra[1])

		#SCREEN.blit(surface,(0,0))
		game.update()
		game.draw(SCREEN)
		pg.display.flip()


if __name__ == "__main__":
	main()
