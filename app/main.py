from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from audio_player import AudioVisualizerKivy


class MainApp(App):
    def build(self):
        # Create a layout
        layout = BoxLayout(orientation='vertical')

        # Create an instance of the AudioVisualizerKivy widget
        audio_visualizer = AudioVisualizerKivy(source_type='mic')

        # Add the visualizer widget to the layout
        layout.add_widget(audio_visualizer)

        # # Add another widget (e.g., a button) to the layout
        # layout.add_widget(Button(text="Stop Visualizer", on_press=self.stop_visualizer))

        return layout

    def stop_visualizer(self, instance):
        # Handle stopping the visualizer
        self.root.children[0].on_stop()  # Assuming the visualizer is the first widget in the layout


if __name__ == '__main__':
    MainApp().run()
