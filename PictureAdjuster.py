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

    def __adjust(self) -> Image:
        pass

    @staticmethod  # means cant use self
    def __convert_to_sepia(red: int, green: int, blue: int) -> (int, int, int):
        pass

    @staticmethod
    def __convert_to_grayscale(red: int, green: int, blue: int) -> (int, int, int):
        pass

    @staticmethod
    def __convert_to_negative(red: int, green: int, blue: int) -> (int, int, int):
        pass

    @staticmethod
    def __convert_to_washout(red: int, green: int, blue: int) -> (int, int, int):
        pass

    def __convert_to_one_color(self, red: int, green: int, blue: int) -> (int, int, int):
        pass

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
            self.convert_method = None
            self.convert_method_name = None
        else:
            self.convert_method = self.__convert_map[convert_method]
            self.convert_method_name = None

    def __del_convert_method(self) -> None:
        self.__convert_method = None

    def __set_color_component(self, color_component: str) -> None:
        pass

    def __get_color_component(self) -> str:
        pass

    def __del_color_component(self) -> None:
        pass

    # Properties
    image = property(__get_img, __set_img, __del_img)
    convert_method = property(__get_convert_method, __set_convert_method, __del_convert_method)
    color_component = property(__get_color_component, __set_color_component, __del_color_component)

    # typically deletion means removig from mem in python
