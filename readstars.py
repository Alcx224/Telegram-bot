from PIL import Image, ImageDraw
import os
size= 3000

#Transform coords to pixel coords
center_x = size // 2
center_y = size // 2


def plot_background():
    # Create a new image with a white background
    image = Image.new("RGB", (size, size), "black")
    return image


#Dictionary functions keyed to Henry Draper Numbers
def read_coords(file):
    hd_dict = {}      # Dictionary keyed on Henry Draper number with x and y coordinates
    magnitude_dict = {}  # Dictionary keyed on Henry Draper number with magnitudes
    name_dict = {}    # Dictionary keyed on star names with Henry Draper numbers

    for line in file:
        parts = line.split()
        hd_number = parts[3]
        x_coord = float(parts[0])
        y_coord = float(parts[1])
        magnitude = float(parts[4])

        x_coord = center_x + int(x_coord * (size / 2))
        y_coord = center_y - int(y_coord * (size / 2))
        # Store the x and y coordinates in hd_dict
        hd_dict[hd_number] = (x_coord, y_coord)

        # Store the magnitude in magnitude_dict
        magnitude_dict[hd_number] = magnitude

        # Check if star has a name
        if len(parts) > 6:
            star_names = " ".join(parts[6:])  # Merge the star names into a single string
            star_names = star_names.split(';')  # Split names by semicolon

            for name in star_names:
                if name.strip():  # Skip empty names
                    if name in name_dict:
                        name_dict[name].append(hd_number)
                    else:
                        name_dict[name] = [hd_number]

    return hd_dict, magnitude_dict, name_dict

#Dict test
'''hd_number = "432"
if hd_number in hd_dict:
    x, y = hd_dict[hd_number]
    print(f"Star {hd_number} is located at coordinates ({x}, {y})")
    magnitude = magnitude_dict[hd_number]
    print(f"Magnitude of star {hd_number} is {magnitude}")
    print(hd_dict)'''


def stars_plotting(hd_dict, magnitude_dict):
    picture = plot_background()
    draw1 = ImageDraw.Draw(picture)

    for hd_number, (x, y) in hd_dict.items():
        magnitude = magnitude_dict.get(hd_number, 0)  # Get the magnitude of the star

        # Calculate the size of the rectangle based on the magnitude
        star_size = round(10.0 / (magnitude + 2))

        # Calculate the top-left and bottom-right coordinates of the rectangle
        top_left = (x - star_size, y - star_size)
        bottom_right = (x + star_size, y + star_size)

        # Draw a filled rectangle representing the star
        draw1.rectangle([top_left, bottom_right], fill="white")

    return picture

def read_constellation_lines(file):
    constellation_dict = {}

    for line in file:
        parts = line.strip().split(",")
        star1 = parts[0]
        star2 = parts[1]

        if star1 in constellation_dict:
            constellation_dict[star1].append(star2)
        else:
            constellation_dict[star1] = [star2]

        if star2 in constellation_dict:
            constellation_dict[star2].append(star1)
        else:
            constellation_dict[star2] = [star1]

    return constellation_dict

def read_all_constellation_lines(folder_path, exclude_file):
    all_cons = {}

    for filename in os.listdir(folder_path):
        if filename != exclude_file: 
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                lines_dict = read_constellation_lines(file)
                all_cons.update(lines_dict)

    return all_cons

def plot_constellation_lines(picture, hd_dict, constellation_dict, name_dict, line_color):
    draw = ImageDraw.Draw(picture)

    for star, connected_stars in constellation_dict.items():
        if star in name_dict:
            hd_numbers = name_dict[star]
            for hd_number in hd_numbers:
                if hd_number in hd_dict:
                    x1, y1 = hd_dict[hd_number]
                    for connected_star in connected_stars:
                        if connected_star in name_dict:
                            connected_hd_numbers = name_dict[connected_star]
                            for connected_hd_number in connected_hd_numbers:
                                if connected_hd_number in hd_dict:
                                    x2, y2 = hd_dict[connected_hd_number]
                                    draw.line([(x1, y1), (x2, y2)], fill=line_color)

    return picture


