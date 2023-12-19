
import os

current_directory = os.getcwd()

CAM_WIDTH = 640
CAM_HEIGHT = 480

X_POS_SAMPLING = 620
Y_POS_SAMPLING = 10

CURRENT_DIRECTORY = os.getcwd()
COLORS_PATH = CURRENT_DIRECTORY

DEFAULT_CAM_ID = 0

ARROW_FILE = "/home/wannatry/Mellouky/M2_SIIA/tux_interactor/dev/tux_interactions/arrow_colors.csv"
BOWLING_BALL_FILE = "/home/wannatry/Mellouky/M2_SIIA/tux_interactor/dev/tux_interactions/bowling_ball_colors.csv"
SKIMMER_FILE = "/home/wannatry/Mellouky/M2_SIIA/tux_interactor/dev/tux_interactions/skimmer_colors.csv"
ANCHOR_FILE = "/home/wannatry/Mellouky/M2_SIIA/tux_interactor/dev/tux_interactions/anchor_colors.csv"
PARACHUTE_FILE = "/home/wannatry/Mellouky/M2_SIIA/tux_interactor/dev/tux_interactions/parachute_colors.csv"
PLANGER_FILE = "/home/wannatry/Mellouky/M2_SIIA/tux_interactor/dev/tux_interactions/planger_colors.csv"
BOX_FILE = "/home/wannatry/Mellouky/M2_SIIA/tux_interactor/dev/tux_interactions/box_colors.csv"
CUPCAKE_FILE = "/home/wannatry/Mellouky/M2_SIIA/tux_interactor/dev/tux_interactions/cupcake_colors.csv"
BASKETBALL_FILE = "/home/wannatry/Mellouky/M2_SIIA/tux_interactor/dev/tux_interactions/arrow_colors.csv"
BULLET_FILE = "/home/wannatry/Mellouky/M2_SIIA/tux_interactor/dev/tux_interactions/bullet_colors.csv"

DATA_FIRE = b'FIRE'

####################### 
# FINGER COUNTER 
#######################


WIDTH = 640 
HEIGHT = 480
SQUARE_WIDTH = WIDTH // 2
SQUARE_HEIGHT = HEIGHT // 2

# Define coordinates for each region
REGIONS = [
    (0, 0, SQUARE_WIDTH, SQUARE_HEIGHT),           # Top-left region
    (SQUARE_WIDTH, 0, WIDTH, SQUARE_HEIGHT),       # Top-right region
    (0, SQUARE_HEIGHT, SQUARE_WIDTH, HEIGHT),      # Bottom-left region
    (SQUARE_WIDTH, SQUARE_HEIGHT, WIDTH, HEIGHT)   # Bottom-right region
]