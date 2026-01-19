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
import os

# Пытаемся импортировать pyproj
try:
    from pyproj import Transformer
    PROJ_READY = True
except ImportError:
    PROJ_READY = False

class MapScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Основная карта (OSM)
        self.map_image = Image(
            source='https://tile.openstreetmap.org/10/512/512.png',
            allow_stretch=True,
            keep_ratio=False
        )
        self.add_widget(self.map_image)

        self.points = []
        self.mark_widgets = []

        # Кнопки
        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'bottom': 1})
        btn_copy = Button(text="Копировать", background_color=(0, 0.7, 0, 1))
        btn_copy.bind(on_press=self.show_copy_popup)
        
        btn_reset = Button(text="Сброс", background_color=(0.7, 0, 0, 1))
        btn_reset.bind(on_press=self.reset_points)
        
        btn_layout.add_widget(btn_copy)
        btn_layout.add_widget(btn_reset)
        self.add_widget(btn_layout)

        self.info_label = Label(
            text="Нажми на карту",
            size_hint=(1, 0.1),
            pos_hint={'top': 1},
            color=(1, 1, 0, 1)
        )
        self.add_widget(self.info_label)

        self.bind(on_touch_down=self.on_tap)

    def on_tap(self, instance, touch):
        if touch.y < self.height * 0.1: return # Не кликать на кнопки
        
        px_x = touch.x
        px_y = touch.y

        # Расчет координат
        lon = 30.5 + (touch.x / self.width) * 0.1
        lat = 50.4 + (touch.y / self.height) * 0.1
        
        sk_x, sk_y = 0, 0
        if PROJ_READY:
            try:
                zone = int((lon + 180) // 6) + 1
                transformer = Transformer.from_crs("EPSG:4326", f"EPSG:{28400 + zone}", always_xy=True)
                sk_y, sk_x = transformer.transform(lon, lat)
            except: pass

        self.points.append((sk_x, sk_y))

        with self.canvas.after:
            Color(1, 0, 0, 1)
            d = dp(15)
            Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d, d))

    def show_copy_popup(self, instance):
        output = ""
        for x, y in self.points:
            output += f"{x:.0f} {y:.0f}\n"
        
        content = BoxLayout(orientation='vertical')
        scroll = ScrollView()
        lab = Label(text=output or "Пусто", size_hint_y=None, halign='left')
        lab.bind(texture_size=lab.setter('size'))
        scroll.add_widget(lab)
        content.add_widget(scroll)
        
        btn = Button(text="Копировать всё", size_hint_y=0.2)
        btn.bind(on_press=lambda x: Clipboard.copy(output))
        content.add_widget(btn)
        
        popup = Popup(title="Координаты", content=content, size_hint=(0.8, 0.8))
        popup.open()

    def reset_points(self, instance):
        self.points = []
        self.canvas.after.clear()

class MapApp(App):
    def build(self):
        return MapScreen()

if __name__ == '__main__':
    MapApp().run()
