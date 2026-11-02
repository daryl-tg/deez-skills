import urllib.request

from deezlib.superclanker import sources
from deezlib.superclanker.domain import utc_now

HEALTHZ = "http://127.0.0.1:31337/healthz"
PROBE_TIMEOUT_SECONDS = 2


def _read(urlopen):
    try:
        with urlopen(HEALTHZ, timeout=PROBE_TIMEOUT_SECONDS):
            pass
    except OSError:
        raise sources.PollFailed("om daemon unreachable") from None
    raise sources.PollFailed("om rooms read not implemented; see openapi.json")


def poll(store, policy, now=utc_now, urlopen=urllib.request.urlopen):
    return sources.record(store, policy, now, lambda: _read(urlopen))
