from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import FormView, UpdateView, View

from apps.evidence.models import UsageEvent

from .forms import UserProfileForm, UserRegistrationForm

User = get_user_model()


class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        user = form.save()
        UsageEvent.objects.create(user=user, event_type="USER_REGISTERED")
        self._send_verification_email(user)
        messages.success(
            self.request,
            "Registration successful. Check your email to activate your account.",
        )
        return super().form_valid(form)

    def _send_verification_email(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verification_url = self.request.build_absolute_uri(
            reverse("accounts:verify-email", kwargs={"uidb64": uid, "token": token})
        )
        message = render_to_string(
            "accounts/email_verification_email.txt",
            {
                "user": user,
                "verification_url": verification_url,
                "site_name": "Privatedec",
            },
        )
        send_mail(
            subject="Verify your Privatedec account",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )


class VerifyEmailView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        user = self._get_user(uidb64)
        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_email_verified = True
            user.save(update_fields=["is_active", "is_email_verified", "updated_at"])
            UsageEvent.objects.create(user=user, event_type="EMAIL_VERIFIED")
            messages.success(request, "Your account has been verified. You can now sign in.")
        else:
            messages.error(request, "The verification link is invalid or expired.")
        return HttpResponseRedirect(reverse("accounts:login"))

    def _get_user(self, uidb64):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
        except (TypeError, ValueError, OverflowError):
            return None
        return User.objects.filter(pk=user_id).first()


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated.")
        return super().form_valid(form)
