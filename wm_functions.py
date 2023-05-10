#Functions made with the reference exercise to adapt
#This functions are Helpers for the implementation


from PIL import Image, ImageDraw

size = 1000



def coords_to_pixel(orig_x, orig_y, size):
    # Calculate the center of the picture
    center_x = size // 2
    center_y = size // 2

    # Calculate the pixel coordinates
    pixel_x = center_x + int(orig_x * (size / 2))
    pixel_y = center_y - int(orig_y * (size / 2))

    return pixel_x, pixel_y


def plot_squares(point_list):
    # Create a new image with a white background
    image = Image.new("RGB", (100, 100), "white")
    draw = ImageDraw.Draw(image)

    # Plot the squares for each point in the list
    for point in point_list:
        x, y = point
        # Calculate the top-left and bottom-right coordinates of the square
        top_left = (x - 1, y - 1)
        bottom_right = (x + 1, y + 1)
        # Draw a filled rectangle representing the square
        draw.rectangle([top_left, bottom_right], fill="black")

    return image