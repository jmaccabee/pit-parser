from django.forms import ModelForm, TextInput

from parser_backend.models import ProcessedPitData


class AnnotationForm(ModelForm):
    class Meta:
        model = ProcessedPitData
        exclude = ["mango_product_file", "timeseries_id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        text_input_class = {
            "class": (
                "bg-gray-50 border border-gray-300 text-gray-900 "
                "text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 "
                "block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 "
                "dark:placeholder-gray-400 dark:text-white"
            )
        }
        for field, value in self.fields.items():
            if field == "dates_start_period":
                continue
            value.widget.attrs.update(text_input_class)
        self.fields["dates_start_period"].widget.attrs.update(
            {
                "class": (
                    "w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 "
                    "focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 "
                    "dark:focus:ring-blue-600 dark:ring-offset-gray-800 "
                    "dark:focus:ring-offset-gray-800"
                )
            }
        )
