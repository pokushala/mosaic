from multiprocessing import Process, Queue, cpu_count
from settings import EOQ_VALUE, WORKER_COUNT, OUT_FILE, TILE_SIZE, TILE_BLOCK_SIZE

from TileFitter import TileFitter
from MosaicImage import MosaicImage
from ProgressCounter import ProgressCounter


class MosaicBuilder:
	#def __init__(self):

	def fit_tiles(self, work_queue, result_queue, tiles_data):
	# this function gets run by the worker processes, one on each CPU core
		tile_fitter = TileFitter(tiles_data)

		while True:
			try:
				img_data, img_coords = work_queue.get(True)
				if img_data == EOQ_VALUE:
					break
				tile_index = tile_fitter.get_best_fit_tile(img_data)
				result_queue.put((img_coords, tile_index))
			except KeyboardInterrupt:
				pass

		# let the result handler know that this worker has finished everything
		result_queue.put((EOQ_VALUE, EOQ_VALUE))


	def build_mosaic(self, result_queue, all_tile_data_large, original_img_large):
		mosaic = MosaicImage(original_img_large)

		active_workers = WORKER_COUNT
		while True:
			try:
				img_coords, best_fit_tile_index = result_queue.get()

				if img_coords == EOQ_VALUE:
					active_workers -= 1
					if not active_workers:
						break
				else:
					tile_data = all_tile_data_large[best_fit_tile_index]
					mosaic.add_tile(tile_data, img_coords)

			except KeyboardInterrupt:
				pass

		mosaic.save(OUT_FILE)
		print ('\nFinished, output is in', OUT_FILE)

	def compose(self, original_img, tiles):
		print ('Building mosaic, press Ctrl-C to abort...')

		original_img_large, original_img_small = original_img
		tiles_large, tiles_small = tiles

		mosaic = MosaicImage(original_img_large)
		all_tile_data_large = []
		for t in tiles_large:
			all_tile_data_large.append(list(t.getdata()))

		#all_tile_data_small = [lambda tile : list(tile.getdata()) for f in tiles_small]
		all_tile_data_small = []
		for t in tiles_small:
			all_tile_data_small.append(list(t.getdata()))

		work_queue   = Queue(WORKER_COUNT)	
		result_queue = Queue()

		try:
			# start the worker processes that will build the mosaic image
			Process(target=self.build_mosaic, args=(result_queue, all_tile_data_large, original_img_large)).start()

			# start the worker processes that will perform the tile fitting
			for n in range(WORKER_COUNT):
				Process(target=self.fit_tiles, args=(work_queue, result_queue, all_tile_data_small)).start()

			progress = ProgressCounter(mosaic.x_tile_count * mosaic.y_tile_count)
			for x in range(int(mosaic.x_tile_count)):
				for y in range(int(mosaic.y_tile_count)):
					large_box = (x * TILE_SIZE, y * TILE_SIZE, (x + 1) * TILE_SIZE, (y + 1) * TILE_SIZE)
					small_box = (x * TILE_SIZE/TILE_BLOCK_SIZE, y * TILE_SIZE/TILE_BLOCK_SIZE, (x + 1) * TILE_SIZE/TILE_BLOCK_SIZE, (y + 1) * TILE_SIZE/TILE_BLOCK_SIZE)
					work_queue.put((list(original_img_small.crop(small_box).getdata()), large_box))
					progress.update()

		except KeyboardInterrupt:
			print ('\nHalting, saving partial image please wait...')

		finally:
			# put these special values onto the queue to let the workers know they can terminate
			for n in range(WORKER_COUNT):
				work_queue.put((EOQ_VALUE, EOQ_VALUE))