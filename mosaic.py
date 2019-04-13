import sys

from TileProcessor import TileProcessor
from TargetImage import TargetImage
from MosaicBuilder import MosaicBuilder


def mosaic(img_path, tiles_path):
	tiles_data = TileProcessor(tiles_path).get_tiles()
	image_data = TargetImage(img_path).get_data()
	builder = MosaicBuilder()
	builder.compose(image_data, tiles_data)

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print ('Usage: %s <image> <tiles directory>\r' % (sys.argv[0],))
	else:
		mosaic(sys.argv[1], sys.argv[2])

