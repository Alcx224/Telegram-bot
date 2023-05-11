from PIL import Image, ImageDraw
size= 5000

#Transform coords to pixel coords
center_x = size // 2
center_y = size // 2


def plot_background():
    # Create a new image with a white background
    image = Image.new("RGB", (size, size), "black")
    return image

picture = plot_background()


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
            star_names = "".join(parts[6:])  # Merge the split parts into a single string
            star_names = star_names.split(' ')  # Split 
            for name in star_names:
                if name in name_dict:
                    # Append the HD number to the existing entry
                    name_dict[name].append(hd_number)
                else:
                    # Create a new entry with the star name and HD number
                    name_dict[name] = [hd_number]
    return hd_dict, magnitude_dict, name_dict

with open("./constellations/stars.txt", "r") as file:
    hd_dict, magnitude_dict, name_dict = read_coords(file)

#Dict test
'''hd_number = "432"
if hd_number in hd_dict:
    x, y = hd_dict[hd_number]
    print(f"Star {hd_number} is located at coordinates ({x}, {y})")
    magnitude = magnitude_dict[hd_number]
    print(f"Magnitude of star {hd_number} is {magnitude}")
    print(hd_dict)'''


def stars_plotting(picture, hd_dict, magnitude_dict):
    draw = ImageDraw.Draw(picture)

    for hd_number, (x, y) in hd_dict.items():
        magnitude = magnitude_dict.get(hd_number, 0)  # Get the magnitude of the star

        # Calculate the size of the rectangle based on the magnitude
        star_size = round(10.0 / (magnitude + 2))

        # Calculate the top-left and bottom-right coordinates of the rectangle
        top_left = (x - star_size, y - star_size)
        bottom_right = (x + star_size, y + star_size)

        # Draw a filled rectangle representing the star
        draw.rectangle([top_left, bottom_right], fill="white")

    return picture
starsplot = stars_plotting(picture, hd_dict, magnitude_dict)


def read_constellation_lines(file):
    lines_dict = {}  # Dictionary keyed on star names with lines between stars

    for line in file:
        star1, star2 = line.strip().split(',')
        star1 = star1.strip()
        star2 = star2.strip()

        if star1 in lines_dict:
            lines_dict[star1].append(star2)
        else:
            lines_dict[star1] = [star2]

        if star2 in lines_dict:
            lines_dict[star2].append(star1)
        else:
            lines_dict[star2] = [star1]

    return lines_dict

with open("./constellations/Boyero.txt", "r") as file:
    lines_dict = read_constellation_lines(file)

def plot_constellations(starsplot, hd_dict, lines_dict, name_dict):
    draw2 = ImageDraw.Draw(starsplot)
    for star1, star2 in lines_dict.items():
        if star1 in name_dict:
            hd_numbers = name_dict[star1]
            if isinstance(hd_numbers, list):
                hd_number = hd_numbers[0]
            else:
                hd_number = hd_numbers

            if hd_number in hd_dict:
                x, y = hd_dict[hd_number]

                for connected_star in star2:
                    print(connected_star)
                    if connected_star in name_dict:
                        connected_hd_numbers = name_dict[connected_star]
                        if isinstance(connected_hd_numbers, list):
                            connected_hd_number = connected_hd_numbers[0]
                        else:
                            connected_hd_number = connected_hd_numbers

                        if connected_hd_number in hd_dict:
                            x1, y1 = hd_dict[connected_hd_number]

                            # Draw a line between the two stars
                            draw2.line([x, y, x1, y1], fill='white')

    return starsplot
finalplot = plot_constellations(starsplot, hd_dict, lines_dict, name_dict)
finalplot.show()