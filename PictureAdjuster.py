from PIL import Image


class PictureAdjuster:

    def __init__(self, img: Image = None):  # image has to be RGB
        if img is not None and img.mode != 'RGB':
            raise ValueError('img must either be an RGB image or None')

        self.__img = img
        self.__del_color_component = None
        self.__convert_method = None
        self.convert_method_name = None
        self.__adjust_img = None
        self.__convert_map = {
            'sepia': PictureAdjuster.__convert_to_sepia,
            'grayscale': PictureAdjuster.__convert_to_grayscale,
            'negative': PictureAdjuster.__convert_to_negative,
            'washout': PictureAdjuster.__convert_to_washout,
            'onecolor': PictureAdjuster.__convert_to_one_color,
        }

    # takes each pixel and makes modifications to them
    # classes are classes? a class itself is a class itself
    def __adjust(self) -> Image:
        if self.__img is None:
            return None
        if self.convert_method is None:
            return None
        if (self.convert_method is self.__convert_to_one_color and self.__color_component is None) or (self.convert_method is self):
            return None

        # self.__adjust_img = self.__img
        # The problem with this is that all it does is point back to the same
        # address as img is meaning it will change the img in files rather than making a copy
        self.__adjusted_img = self.__img.copy()
        pixels = self.__adjusted_img.load()
        width, height = self.__adjusted_img.size

        # loop over the pixels
        for y in range(height):
            for x in range(width):
                # read the pixel
                current_pixel = pixels[x, y]

                # process the pixel
                red, green, blue = current_pixel
                red, green, blue = self.__convert_method(red, green, blue)
                current_pixel = (red, green, blue)
                pixels[x, y] = current_pixel
        return self.__adjusted_img

    @staticmethod  # means cant use self
    def __convert_to_sepia(red: int, green: int, blue: int) -> (int, int, int):

        t_red = int(0.393 * red + 0.769 * green + 0.189 * blue)
        t_green = int(0.349 * red + 0.686 * green + 0.168 * blue)
        t_blue = int(0.272 * red + .534 * green + .131 * blue)

        t_red, t_green, t_blue = (255 if c > 255 else c for c in (t_red, t_green, t_blue))
        return t_red, t_green, t_blue

    @staticmethod
    def __convert_to_grayscale(red: int, green: int, blue: int) -> (int, int, int):
        gray = (red + green + blue) // 3
        return gray, gray, gray

    @staticmethod
    def __convert_to_negative(red: int, green: int, blue: int) -> (int, int, int):
        return (255 - c for c in (red, green, blue))

    @staticmethod
    def __convert_to_washout(red: int, green: int, blue: int) -> (int, int, int):
        max_c = max(red, green, blue)
        t_red, t_green, t_blue = (c + max_c for c in (red, green, blue))
        return (255 if c > 255 else c for c in (t_red, t_green, t_blue))

    def __convert_to_one_color(self, red: int, green: int, blue: int) -> (int, int, int):
        colors = [0, 0, 0]
        if self.__color_component == 'red':
            colors[0] =  red
        elif self.__color_component == 'green':
            colors[1] = green
        else:
            colors[2] = blue
        return tuple(colors)

    def __get_img(self) -> Image:
        return self.__adjust()

    def __set_img(self, img: Image) -> None:
        if img is None or img.size != 'RGB':
            raise ValueError('img must be an RGB image')
        self.__img = img

    def __del_img(self) -> None:
        self.__img = None

    def __get_convert_method(self) -> str:
        return self.convert_method_name

    def __set_convert_method(self, convert_method: str) -> None:
        if convert_method not in self.__convert_map.keys():
            self.__convert_method = None
            self.convert_method_name = None
        else:
            self.__convert_method = self.__convert_map[convert_method]
            self.convert_method_name = None

    def __del_convert_method(self) -> None:
        self.__convert_method = None

    def __set_color_component(self, color_component: str) -> None:
        if color_component not in ['red', 'green', 'blue']:
            self.__color_component = None
        else:
            self.__color_component = color_component

    def __get_color_component(self) -> str:
        return self.__color_component

    def __del_color_component(self) -> None:
        self.__color_component = None

    # Properties
    image = property(__get_img, __set_img, __del_img)
    convert_method = property(__get_convert_method, __set_convert_method, __del_convert_method)
    color_component = property(__get_color_component, __set_color_component, __del_color_component)

    # typically deletion means removing from mem in python
