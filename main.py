from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Ellipse
from kivy.core.clipboard import Clipboard
from kivy.metrics import dp
import math

def wgs84_to_sk42(lon, lat):
    # Упрощенный математический алгоритм пересчета (Гаусса-Крюгера)
    # Зона 5 или 6 (Украина/Европа)
    zone = int(lon / 6 + 1)
    a = 6378245.0          # Красовский
    f = 1 / 298.3
    e2 = 2 * f - f**2
    
    lon0 = (zone * 6 - 3) * math.pi / 180
    lat_rad = lat * math.pi / 180
    lon_rad = lon * math.pi / 180
    
    l = lon_rad - lon0
    cos_lat = math.cos(lat_rad)
    sin_lat = math.sin(lat_rad)
    t = math.tan(lat_rad)
    eta2 = e2 * cos_lat**2
    N = a / math.sqrt(1 - e2 * sin_lat**2)
    
    # Очень упрощенно для теста (Север X, Восток Y)
    x = lat * 111132.0 
    y = zone * 1000000 + 500000 + (lon - (zone*6-3)) * 111320.0 * cos_lat
    return x, y

class MapScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.map_image = Image(source='https://tile.openstreetmap.org/10/512/512.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.map_image)
        self.points = []
        
        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'bottom': 1})
        btn_copy = Button(text="Копировать", background_color=(0, 0.7, 0, 1))
        btn_copy.bind(on_press=self.show_copy_popup)
        btn_reset = Button(text="Сброс", background_color=(0.7, 0, 0, 1))
        btn_reset.bind(on_press=self.reset_points)
        btn_layout.add_widget(btn_copy)
        btn_layout.add_widget(btn_reset)
        self.add_widget(btn_layout)

        self.bind(on_touch_down=self.on_tap)

    def on_tap(self, instance, touch):
        if touch.y < self.height * 0.1: return
        lon = 30.5 + (touch.x / self.width) * 0.5
        lat = 50.4 + (touch.y / self.height) * 0.5
        sk_x, sk_y = wgs84_to_sk42(lon, lat)
        self.points.append((sk_x, sk_y))
        with self.canvas.after:
            Color(1, 0, 0, 1)
            d = dp(20)
            Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d, d))

    def show_copy_popup(self, instance):
        text = "\n".join([f"{x:.0f} {y:.0f}" for x, y in self.points])
        content = BoxLayout(orientation='vertical')
        scroll = ScrollView()
        scroll.add_widget(Label(text=text or "Пусто", size_hint_y=None))
        content.add_widget(scroll)
        btn = Button(text="В буфер", size_hint_y=0.2)
        btn.bind(on_press=lambda x: Clipboard.copy(text))
        content.add_widget(btn)
        Popup(title="Координаты", content=content, size_hint=(0.8, 0.8)).open()

    def reset_points(self, instance):
        self.points = []
        self.canvas.after.clear()

class MapApp(App):
    def build(self): return MapScreen()

if __name__ == '__main__':
    MapApp().run()

