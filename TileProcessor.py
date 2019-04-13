import glob
from PIL import Image

from settings import TILE_BLOCK_SIZE, TILE_SIZE


class TileProcessor:
	def __init__(self, tiles_directory):
		self.tiles_directory = tiles_directory

	def __process_tile(self, tile_path):
		try:
			img = Image.open(tile_path)
			# tiles must be square, so get the largest square that fits inside the image
			w = img.size[0]
			h = img.size[1]
			min_dimension = min(w, h)
			w_crop = (w - min_dimension) / 2
			h_crop = (h - min_dimension) / 2
	
			img = img.crop((w_crop, h_crop, w - w_crop, h - h_crop))
			
			large_tile_img = img.resize((TILE_SIZE, TILE_SIZE), Image.ANTIALIAS)
			small_tile_img = img.resize((int(TILE_SIZE/TILE_BLOCK_SIZE), int(TILE_SIZE/TILE_BLOCK_SIZE)), Image.ANTIALIAS)
			
			return (large_tile_img.convert('RGB'), small_tile_img.convert('RGB'))
		except:
			return (None, None)

	def get_tiles(self):
		large_tiles = []
		small_tiles = []
		tile_names = glob.glob(self.tiles_directory + '/*.jpg')
		print("Reading files from directory", self.tiles_directory);

		for name in tile_names:
			large_tile, small_tile = self.__process_tile(name)
			if large_tile:
				large_tiles.append(large_tile)
				small_tiles.append(small_tile)
		
		print ('Processed %s tiles.' % (len(large_tiles),))

		return (large_tiles, small_tiles)