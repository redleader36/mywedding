from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from weddings.models import Invitation


class FriendsView(TemplateView):
    template_name = "friends.html"

    pin = None
    invitation = None

    def get(self, request, *args, **kwargs):
        # check if everything in place
        if 'pin_provided' not in request.session or 'logged_pin' not in request.session:
            return HttpResponseRedirect(reverse('pin1'))

        self.pin = request.session['logged_pin']

        invitation = self.check_pin(request.session['logged_pin'])

        if invitation == False:
            return HttpResponseRedirect(reverse('pin1'))

        self.invitation = invitation

        response = super(FriendsView, self).get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = super(FriendsView, self).get_context_data(**kwargs)
        context['invitation'] = self.invitation
        context['friends'] = self.invitation.friends.all()
        return context

    def check_pin(self, pin):
        try:
            return Invitation.objects.get(invite_code=pin)
        except Invitation.DoesNotExist:
            return False
