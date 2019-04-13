from multiprocessing import cpu_count

# Change these 3 config parameters to suit your needs...
TILE_SIZE      = 50		# height/width of mosaic tiles in pixels
TILE_MATCH_RES = 5		# tile matching resolution (higher values give better fit but require more processing)
ENLARGEMENT    = 8		# the mosaic image will be this many times wider and taller than the original

TILE_BLOCK_SIZE = TILE_SIZE / max(min(TILE_MATCH_RES, TILE_SIZE), 1)
WORKER_COUNT = max(cpu_count() - 1, 1)
OUT_FILE = 'mosaic.jpeg'
EOQ_VALUE = None