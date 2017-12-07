from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from user.models import User
from user.forms import UpdateUserForm


class EditProfileView(UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'edit_health_professional.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditProfileView, self).dispatch(*args, **kwargs)

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('edit_profile')