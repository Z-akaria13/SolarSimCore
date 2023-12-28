import pygame
import numpy as np

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
BLUE = (10, 10, 150)
POWDER_BLUE = (90,125,190)
GOLD = (218,165,32)
DEBUG_GREEN = (129, 255, 61)

screen_size = pygame.display.Info().current_w, pygame.display.Info().current_h

# create a window
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
pygame.display.set_caption("3D Tilted Circle Simulation")

# clock is used to set a max fps
clock = pygame.time.Clock()



font_size = 36
font = pygame.font.Font(None, font_size)




# =============================== maths and rotation stuff ======================================
# Function to draw a tilted circle usi
# ng matrix transformation
# Transformation function
def tilt_transform(point, tilt_angle):
    tilt_angle_radians = np.radians(tilt_angle)
    rotation_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(tilt_angle_radians), -np.sin(tilt_angle_radians)],
        [0, np.sin(tilt_angle_radians), np.cos(tilt_angle_radians)]
    ])
    return rotation_matrix.dot(point)

def rotate_around_x_axis(coords, angle_degrees):
    """Rotate 3D coordinates around the x-axis by a given angle."""
    angle_radians = np.radians(angle_degrees)
    rotation_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(angle_radians), -np.sin(angle_radians)],
        [0, np.sin(angle_radians), np.cos(angle_radians)]
    ])
    return rotation_matrix.dot(coords)

def transform_and_scale(location, center, angle, width, r):
    """
    Transform the location tuple relative to the center, rotate around the x-axis,
    project to 2D, and scale based on width and yardstick value r.
    """
    # Reorient location relative to center
    reoriented_location = np.array(location) - np.array(center)

    # Apply rotation
    rotated_location = rotate_around_x_axis(reoriented_location, angle)

    # Project to 2D (ignore z-coordinate)
    projected_location = rotated_location[:2]

    # Scale using width and yardstick
    unit_length = width / (2*r)
    scaled_location = projected_location * unit_length

    return scaled_location


#========================== end maths ===============================













#=================== visual render stuff ===============================
# Drawing a tilted circle
def draw_tilted_circle(screen, color, center, radius, tilt_angle):
    circle_points = []
    for angle in np.linspace(0, 2 * np.pi, 100):
        x, y = radius * np.cos(angle), radius * np.sin(angle)
        point = tilt_transform(np.array([x, y, 0]), tilt_angle)
        circle_points.append((center[0] + point[0], center[1] + point[1]))

    pygame.draw.lines(screen, color, True, circle_points, 1)

# Drawing a tilted line
def draw_tilted_line(screen, color, start_point, end_point, center, tilt_angle):
    transformed_start = tilt_transform(np.array(start_point), tilt_angle)
    transformed_end = tilt_transform(np.array(end_point), tilt_angle)

    pygame.draw.line(screen, color, 
                     (center[0] + transformed_start[0], center[1] + transformed_start[1]),
                     (center[0] + transformed_end[0], center[1] + transformed_end[1]))


def draw_projected_point(circle_center, location, center, colour, angle = 10, width = screen_size[0] * 0.9 , r = 20):
    scaled_coords = transform_and_scale(location, center, angle, width, r)
    line_base_Coord = transform_and_scale(location, (center[0], center[1], location[2]), angle, width, r)
    try:
        if location[2] < center[2]:
            draw_dotted_line(screen, BLUE, ( circle_center[0] + line_base_Coord[0], circle_center[1] - line_base_Coord[1]),  (circle_center[0] + scaled_coords[0], circle_center[1] - scaled_coords[1]), 1, 2, 5)
        else:
            draw_dotted_line(screen, POWDER_BLUE, ( circle_center[0] + line_base_Coord[0], circle_center[1] - line_base_Coord[1]),  (circle_center[0] + scaled_coords[0], circle_center[1] - scaled_coords[1]), 1, 1, 5)
    except:
        ()
    pygame.draw.circle(screen, colour, (circle_center[0]+ scaled_coords[0], circle_center[1] - scaled_coords[1]), 3)


def draw_dotted_line(screen, color, start_pos, end_pos, width, dot_length, space_length):
    # Calculate the total distance between the start and end positions
    total_length = pygame.math.Vector2(end_pos) - pygame.math.Vector2(start_pos)
    total_length = total_length.length()
    
    # Calculate the direction vector from start to end position
    direction_vector = pygame.math.Vector2(end_pos) - pygame.math.Vector2(start_pos)
    direction_vector.normalize_ip()  # Normalize the vector

    # Initialize the start position for drawing
    current_pos = pygame.math.Vector2(start_pos)

    # Draw the dotted line
    while total_length > 0:
        # Calculate the end position of the current segment
        segment_end_pos = current_pos + direction_vector * dot_length
        pygame.draw.line(screen, color, current_pos, segment_end_pos, width)

        # Update the current position and the total length remaining
        current_pos = segment_end_pos + direction_vector * space_length
        total_length -= (dot_length + space_length)




#==================== end of render stuff ==============================



def main():
    k = 65
    stars = [ (10, 7, 12),     (10, 7, 12),
    (9, 8, 2),
    (12.5, 7.2, 8),
    (7, 11.1, 14),
    (14.310172607940475, 8.455304441106676, 9.293279154668625),
    (5.061473687333335, 1.583264533285531, 8.441916481423082),
    (17.29692547172813, 8.27219304975507, 6.562103075535848),
    (15.090349655055029, 10.544592421010504, 14.093254161152549)]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and k < 90:
            k += 1

        elif keys[pygame.K_DOWN] and k > 0:
            k -= 1

        # Clear the screen
        screen.fill(BLACK)

        # Calculate the center and radius of the circle
        circle_center = (screen_size[0] // 2, screen_size[1] // 2)
        circle_radius = int(screen_size[0]*0.5 // 2)

        # Draw the tilted circle as an ellipse using matrix transformation
     
        draw_tilted_circle(screen, DEBUG_GREEN, circle_center, circle_radius, k)
        draw_tilted_circle(screen, DEBUG_GREEN, circle_center, circle_radius*0.3333, k)
        draw_tilted_circle(screen, DEBUG_GREEN, circle_center, circle_radius*0.6666, k)
        draw_tilted_line(screen, DEBUG_GREEN, (circle_radius*np.sin(0.785398),circle_radius*np.sin(0.785398),0), (-circle_radius*np.sin(0.785398), -circle_radius*np.sin(0.785398),0), circle_center, k)
        draw_tilted_line(screen, DEBUG_GREEN, (circle_radius*np.sin(0.785398), -circle_radius*np.sin(0.785398),0), (-circle_radius*np.sin(0.785398), circle_radius*np.sin(0.785398),0), circle_center, k)
        draw_tilted_line(screen, DEBUG_GREEN, (circle_radius,0,0), (-circle_radius, 0,0), circle_center, k)
        draw_tilted_line(screen, DEBUG_GREEN, (0,circle_radius,0), (0, -circle_radius,0), circle_center, k)
        pygame.draw.circle(screen, RED, circle_center, 5)
        
        for l in range(1, len(stars)):
            draw_projected_point(circle_center, stars[l], stars[0], GOLD, k)

    # Render text
        text = f"{k}"
        text_surface = font.render(text, True, WHITE)  # True for anti-aliased text
        text_rect = text_surface.get_rect()
        text_rect.center = (screen_size[0] // 5, screen_size[1] // 2)  # Center the text

        # Blit the text
        screen.blit(text_surface, text_rect)



        # Update the screen
        pygame.display.flip()

        # Set the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()