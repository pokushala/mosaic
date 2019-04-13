from PIL import Image
from settings import TILE_SIZE

class MosaicImage:
	def __init__(self, original_img):
		self.image = Image.new(original_img.mode, original_img.size)
		self.x_tile_count = original_img.size[0] / TILE_SIZE
		self.y_tile_count = original_img.size[1] / TILE_SIZE
		self.total_tiles  = self.x_tile_count * self.y_tile_count

	def add_tile(self, tile_data, coords):
		img = Image.new('RGB', (TILE_SIZE, TILE_SIZE))
		img.putdata(tile_data)
		self.image.paste(img, coords)

	def save(self, path):
		self.image.save(path)