import swapper
from django import forms
from django.db.models import Q
from wagtail.admin.forms.choosers import BaseFilterForm, LocaleFilterMixin
from wagtail.admin.ui.tables import TitleColumn
from wagtail.admin.views.generic.chooser import BaseChooseView, ChooseViewMixin, CreationFormMixin, \
    ChooseResultsViewMixin
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.models import TranslatableMixin
from django.utils.translation import gettext as _

from .conf import settings

# ----------------------------------------------------------
#
#   CONTACT CUSTOM CHOOSER
#
# ----------------------------------------------------------

class StreamformFilterMixin(forms.Form):

    q = forms.CharField(
        label=_("Search forms"),
        widget=forms.TextInput(attrs={"placeholder": _("Search")}),
        required=False,
    )

    def filter(self, objects):
        objects = super().filter(objects)
        search_query = self.cleaned_data.get("q")
        if search_query:
            objects = objects.filter(
                Q(title__icontains=search_query) |
                Q(site__icontains=search_query)
            )
            self.is_searching = True
            self.search_query = search_query
        return objects

class BaseStreamformChooser(BaseChooseView):
    """
    Base class for the staff member chooser views
    """

    @property
    def columns(self):
        return [
            TitleColumn(
                name="title",
                label=_("Title"),
                accessor="title",
                url_name=self.chosen_url_name,
                link_attrs={"data-chooser-modal-choice": True},
            ),
            TitleColumn(
                name="template_name",
                label=_("Template Name"),
                accessor="email",
                url_name=self.chosen_url_name,
                link_attrs={"data-chooser-modal-choice": True},
            ),
            TitleColumn(
                name="success_message",
                label=_("Success Message"),
                accessor="success_message",
                url_name=self.chosen_url_name,
                link_attrs={"data-chooser-modal-choice": True},
            ),
            TitleColumn(
                name="post_redirect_page",
                label=_("Redirect Page"),
                accessor="post_redirect_page",
                url_name=self.chosen_url_name,
                link_attrs={"data-chooser-modal-choice": True},
            ),
        ]

    def get_filter_form_class(self):
        bases = [StreamformFilterMixin, BaseFilterForm]

        i18n_enabled = getattr(settings, "WAGTAIL_I18N_ENABLED", False)
        if i18n_enabled and issubclass(self.model_class, TranslatableMixin):
            bases.insert(0, LocaleFilterMixin)

        return type(
            "FilterForm",
            tuple(bases),
            {},
        )

class StreamformChooseView(ChooseViewMixin, CreationFormMixin, BaseStreamformChooser):
    pass

class StreamformChooseResultsView(ChooseResultsViewMixin, CreationFormMixin, BaseStreamformChooser):
    pass


class StreamformChooserViewSet(ChooserViewSet):
    model = 'wagtailstreamforms.Form'

    choose_view_class = StreamformChooseView
    choose_results_view_class = StreamformChooseResultsView

    icon = "document"
    choose_one_text = _("Choose a form")
    choose_another_text = _("Choose another form")
    edit_item_text = _("Edit this form")

streamform_chooser_viewset = StreamformChooserViewSet("streamform_chooser")

