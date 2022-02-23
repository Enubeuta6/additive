from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.shortcuts import resolve_url
from django.utils import inspect
from django.utils.encoding import force_str

from Waysed import settings
from .models import *

class DataMixin():
    dbData = UserDataMeta.objects.all()

    def get_user_context(self, **kwargs):
        context = kwargs
        return context


    class AccessMixin:
        """
        Base access mixin. All other access mixins should extend this one.
        """

        login_url = None
        raise_exception = False
        redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth
        redirect_unauthenticated_users = False

        def __init__(self, *args, **kwargs):
            self._class_name = self.__class__.__name__
            super().__init__(*args, **kwargs)

        def get_login_url(self):
            """
            Override this method to customize the login_url.
            """
            login_url = self.login_url or settings.LOGIN_URL
            if not login_url:
                raise ImproperlyConfigured(
                    f"Define {self._class_name}.login_url or settings.LOGIN_URL or "
                    f"override {self._class_name}.get_login_url()."
                )

            return force_str(login_url)

        def get_redirect_field_name(self):
            """
            Override this method to customize the redirect_field_name.
            """
            if self.redirect_field_name is None:
                raise ImproperlyConfigured(
                    f"{self._class_name} is missing the redirect_field_name. "
                    f"Define {self._class_name}.redirect_field_name or "
                    f"override {self._class_name}.get_redirect_field_name()."
                )
            return self.redirect_field_name

        def handle_no_permission(self, request):
            """What should happen if the user doesn't have permission?"""
            if self.raise_exception:
                if (
                        self.redirect_unauthenticated_users
                        and not request.user.is_authenticated
                ):
                    return self.no_permissions_fail(request)
                else:
                    if inspect.isclass(self.raise_exception) and issubclass(
                            self.raise_exception, Exception
                    ):
                        raise self.raise_exception
                    if callable(self.raise_exception):
                        ret = self.raise_exception(request)
                        if isinstance(ret, (HttpResponse, StreamingHttpResponse)):
                            return ret
                    raise PermissionDenied

            return self.no_permissions_fail(request)

        def no_permissions_fail(self, request=None):
            """
            Called when the user has no permissions and no exception was raised.
            This should only return a valid HTTP response.
            By default we redirect to login.
            """
            return redirect_to_login(
                request.get_full_path(),
                self.get_login_url(),
                self.get_redirect_field_name(),
            )
class AnonymousRequiredMixin(AccessMixin):
    """
    Requires the user to be unauthenticated.
    NOTE:
        This should be the left-most mixin of a view.
    ## Example Usage
        class SomeView(AnonymousRequiredMixin, ListView):
            ...
            # required
            authenticated_redirect_url = "/accounts/profile/"
            ...
    """

    authenticated_redirect_url = settings.LOGIN_REDIRECT_URL

    def dispatch(self, request, *args, **kwargs):
        """Call the appropriate handler after guaranteeing anonymity"""
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_authenticated_redirect_url())
        return super().dispatch(request, *args, **kwargs)

    def get_authenticated_redirect_url(self):
        """Return the reversed authenticated redirect url."""
        if not self.authenticated_redirect_url:
            raise ImproperlyConfigured(
                f"{self._class_name} is missing an authenticated_redirect_url "
                f"url to redirect to. Define {self._class_name}.authenticated_redirect_url "
                f"or override {self._class_name}.get_authenticated_redirect_url()."
            )
        return resolve_url(self.authenticated_redirect_url)
