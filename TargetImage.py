from PIL import Image

from settings import ENLARGEMENT, TILE_BLOCK_SIZE, TILE_SIZE

class TargetImage:
	def __init__(self, image_path):
		self.image_path = image_path

	def get_data(self):
		print ('Processing main image...')
		img = Image.open(self.image_path)
		w = img.size[0] * ENLARGEMENT
		h = img.size[1]	* ENLARGEMENT
		large_img = img.resize((w, h), Image.ANTIALIAS)
		w_diff = (w % TILE_SIZE)/2
		h_diff = (h % TILE_SIZE)/2
		
		# if necesary, crop the image slightly so we use a whole number of tiles horizontally and vertically
		if w_diff or h_diff:
			large_img = large_img.crop((w_diff, h_diff, w - w_diff, h - h_diff))

		small_img = large_img.resize((int(w/TILE_BLOCK_SIZE), int(h/TILE_BLOCK_SIZE)), Image.ANTIALIAS)

		image_data = (large_img.convert('RGB'), small_img.convert('RGB'))

		print ('Main image processed.')

		return image_data
