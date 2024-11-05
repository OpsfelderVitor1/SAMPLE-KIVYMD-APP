from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from plyer import gps

class GPSApp(MDApp):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        self.label = MDLabel(text="Pressione o botão para obter a localização GPS", halign="center")
        layout.add_widget(self.label)
        
        button = MDRaisedButton(text="Obter Localização", pos_hint={"center_x": 0.5})
        button.bind(on_press=self.get_location)
        layout.add_widget(button)

        return layout

    def get_location(self, instance):
        try:
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            gps.start(minTime=1000, minDistance=1)
        except NotImplementedError:
            self.label.text = "O GPS não é suportado neste dispositivo"

    def on_location(self, **kwargs):
        latitude = kwargs.get('lat')
        longitude = kwargs.get('lon')
        
        if latitude and longitude:
            with open('localizacao.txt', 'w') as f:
                f.write(f'Latitude: {latitude}\nLongitude: {longitude}')
            self.label.text = f'Localização salva em localizacao.txt\nLatitude: {latitude}, Longitude: {longitude}'

    def on_status(self, stype, status):
        if status == 'provider-enabled':
            self.label.text = "GPS Ativado"
        elif status == 'provider-disabled':
            self.label.text = "GPS Desativado"

    def on_stop(self):
        gps.stop()

if __name__ == '__main__':
    GPSApp().run()
