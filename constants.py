# Tile image file paths
EMPTY_TILE = "images/empty_alt.png"
ONE_TILE = "images/one_alt.png"
TWO_TILE = "images/two_alt.png"
THREE_TILE = "images/three_alt.png"
FOUR_TILE = "images/four_alt.png"

# A tile must be EXACTLY ONE of the five listed types below
TYPES = {
    0: EMPTY_TILE,
    1: ONE_TILE,
    2: TWO_TILE,
    3: THREE_TILE,
    4: FOUR_TILE,
}
# Each tile .png image is 83 x 83 pixels
TILE_PIXEL_WIDTH = 83
TILE_PIXEL_HEIGHT = 83

# Margin to separate each cell
MARGIN = 3

# Vertical Border margin
VERTICAL_BORDER_MARGIN = 50

# Horizontal Border margin
HORIZONTAL_BORDER_MARGIN = 100

# Width and height of each individual tile when scaled
SCALE_FACTOR = 0.5
TILE_SCALED_WIDTH = int(TILE_PIXEL_WIDTH * SCALE_FACTOR)
TILE_SCALED_HEIGHT = int(TILE_PIXEL_HEIGHT * SCALE_FACTOR)

HIGHLIGHT_SPEED = 9
