from django.forms.widgets import FileInput
from django.utils.safestring import mark_safe

class MultipleFileInput(FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs['multiple'] = 'multiple'
        return super().render(name, value, attrs, renderer)
    
    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return files.get(name)