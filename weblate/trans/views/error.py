# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2019 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from __future__ import unicode_literals

import django.views.defaults
from django.conf import settings
from django.middleware.csrf import REASON_NO_CSRF_COOKIE, REASON_NO_REFERER
from django.utils.translation import ugettext as _

from weblate.trans.util import render


def bad_request(request, exception=None):
    """Error handler for bad request."""
    return render(request, "400.html", {"title": _("Bad Request")}, status=400)


def not_found(request, exception=None):
    """Error handler showing list of available projects."""
    return render(request, "404.html", {"title": _("Page Not Found")}, status=404)


def denied(request, exception=None):
    return render(request, "403.html", {"title": _("Permission Denied")}, status=403)


def csrf_failure(request, reason=""):
    return render(
        request,
        "403_csrf.html",
        {
            "title": _("Permission Denied"),
            "no_referer": reason == REASON_NO_REFERER,
            "no_cookie": reason == REASON_NO_CSRF_COOKIE,
        },
        status=403,
    )


def server_error(request):
    """Error handler for server errors."""
    try:
        if hasattr(settings, "RAVEN_CONFIG") and "public_dsn" in settings.RAVEN_CONFIG:
            sentry_dsn = settings.RAVEN_CONFIG["public_dsn"]
        else:
            sentry_dsn = None
        return render(
            request,
            "500.html",
            {"title": _("Internal Server Error"), "sentry_dsn": sentry_dsn},
            status=500,
        )
    except Exception:
        return django.views.defaults.server_error(request)
