import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView


class Note:
    def __init__(self, title, content, category):
        self.title = title
        self.content = content
        self.category = category


class NoteApp(App):
    def __init__(self, **kwargs):
        super(NoteApp, self).__init__(**kwargs)
        self.notes = []
        self.categories = ['General', 'Personal', 'Work']
        self.selected_category = 'General'

    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.category_spinner = Spinner(text='General', values=self.categories)
        self.category_spinner.bind(text=self.on_category_select)

        self.note_title_input = TextInput(hint_text='Enter title')
        self.note_content_input = TextInput(hint_text='Enter content', multiline=True)

        add_note_button = Button(text='Add Note')
        add_note_button.bind(on_press=self.add_note_popup)

        self.note_list_layout = BoxLayout(orientation='vertical')
        self.update_note_list()

        self.layout.add_widget(self.category_spinner)
        self.layout.add_widget(self.note_title_input)
        self.layout.add_widget(self.note_content_input)
        self.layout.add_widget(add_note_button)
        self.layout.add_widget(ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True))
        self.layout.add_widget(self.note_list_layout)

        return self.layout

    def add_note_popup(self, instance):
        popup_layout = BoxLayout(orientation='vertical')
        popup = Popup(title='Add Note', content=popup_layout, size_hint=(None, None), size=(300, 200))

        note_title_input = TextInput(hint_text='Enter title')
        note_content_input = TextInput(hint_text='Enter content', multiline=True)
        category_spinner = Spinner(text='General', values=self.categories)

        add_button = Button(text='Add')
        add_button.bind(on_press=lambda x: self.add_note(note_title_input.text, note_content_input.text,
                                                         category_spinner.text, popup))

        popup_layout.add_widget(note_title_input)
        popup_layout.add_widget(note_content_input)
        popup_layout.add_widget(category_spinner)
        popup_layout.add_widget(add_button)

        popup.open()

    def add_note(self, title, content, category, popup):
        if title.strip() == '' or content.strip() == '':
            self.show_error_popup('Error', 'Title and content cannot be empty.')
            return

        self.notes.append(Note(title, content, category))
        self.update_note_list()
        popup.dismiss()

    def delete_note(self, note):
        self.notes.remove(note)
        self.update_note_list()

    def update_note_list(self):
        self.note_list_layout.clear_widgets()
        for note in self.notes:
            note_button = Button(text=note.title)
            note_button.bind(on_press=lambda x, note=note: self.edit_note_popup(note))
            delete_button = Button(text='Delete')
            delete_button.bind(on_press=lambda x, note=note: self.delete_note_confirmation(note))
            note_layout = BoxLayout(orientation='horizontal')
            note_layout.add_widget(note_button)
            note_layout.add_widget(delete_button)
            self.note_list_layout.add_widget(note_layout)

    def edit_note_popup(self, note):
        popup_layout = BoxLayout(orientation='vertical')
        popup = Popup(title='Edit Note', content=popup_layout, size_hint=(None, None), size=(300, 200))

        note_title_input = TextInput(text=note.title, hint_text='Enter title')
        note_content_input = TextInput(text=note.content, hint_text='Enter content', multiline=True)
        category_spinner = Spinner(text=note.category, values=self.categories)

        save_button = Button(text='Save')
        save_button.bind(on_press=lambda x: self.save_edited_note(note, note_title_input.text,
                                                                  note_content_input.text,
                                                                  category_spinner.text, popup))

        popup_layout.add_widget(note_title_input)
        popup_layout.add_widget(note_content_input)
        popup_layout.add_widget(category_spinner)
        popup_layout.add_widget(save_button)

        popup.open()

    def save_edited_note(self, note, title, content, category, popup):
        if title.strip() == '' or content.strip() == '':
            self.show_error_popup('Error', 'Title and content cannot be empty.')
            return

        note.title = title
        note.content = content
        note.category = category
        self.update_note_list()
        popup.dismiss()

    def delete_note_confirmation(self, note):
        confirmation_popup = Popup(title='Delete Note', content=Label(text='Are you sure you want to delete this note?'),
                                   size_hint=(None, None), size=(300, 200))

        delete_button = Button(text='Delete')
        delete_button.bind(on_press=lambda x: self.delete_note_and_dismiss(note, confirmation_popup))

        cancel_button = Button(text='Cancel')
        cancel_button.bind(on_press=confirmation_popup.dismiss)

        confirmation_popup.content.add_widget(delete_button)
        confirmation_popup.content.add_widget(cancel_button)

        confirmation_popup.open()

    def delete_note_and_dismiss(self, note, popup):
        self.delete_note(note)
        popup.dismiss()

    def on_category_select(self, instance, text):
        self.selected_category = text

    def show_error_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(300, 200))
        popup.open()


if __name__ == '__main__':
    NoteApp().run()
