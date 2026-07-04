"""
utils/authproxy.py
-------------------
Authenticated proxy forwarding for Chrome / Selenium automation.

Chrome's --proxy-server flag cannot carry a username:password, so this
module starts a tiny LOCAL proxy that Chrome talks to with no auth at
all. That local proxy then authenticates to your real (upstream) proxy
on Chrome's behalf:

    Chrome --http--> 127.0.0.1:PORT (this module) --auth--> upstream proxy --> internet

It's built on top of `pproxy` (https://pypi.org/project/pproxy), a small,
pure-asyncio HTTP/HTTPS/SOCKS4/SOCKS5 tunnel library with no dependencies
of its own. We only use it as a library (no subprocess, no CLI, no
manual setup) so the whole project stays one Python program.

    pip install pproxy

Quick start
-----------
    from utils.authproxy import ProxyForwarder

    proxy = ProxyForwarder(host, port, username, password)
    proxy.start()
    options.add_argument(f"--proxy-server=http://{proxy.address}")
    driver = webdriver.Chrome(options=options)
    ...
    proxy.stop()

or as a context manager, which stops the forwarder automatically:

    with ProxyForwarder(host, port, username, password) as proxy:
        options.add_argument(f"--proxy-server=http://{proxy.address}")
        driver = webdriver.Chrome(options=options)
        ...

A SOCKS5 upstream works the same way, just pass scheme="socks5".
"""

from __future__ import annotations

import asyncio
import atexit
import socket
import threading
from typing import Optional

import pproxy

__all__ = ["ProxyForwarder", "start_proxy", "stop_proxy"]


def _free_local_port() -> int:
    """Ask the OS for an unused local TCP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _upstream_uri(host: str, port: int, username: Optional[str],
                   password: Optional[str], scheme: str) -> str:
    """
    Build a pproxy remote-server URI.

    NOTE: pproxy's URI dialect is {scheme}://{netloc}[#{username}:{password}]
    -- credentials for a plain http/socks proxy go in a '#' suffix, NOT in
    a user:pass@host netloc (that form is reserved for shadowsocks-style
    cipher@host addresses). Mixing these up is a common gotcha.
    """
    auth = f"#{username}:{password or ''}" if username else ""
    return f"{scheme}://{host}:{port}{auth}"


class ProxyForwarder:
    """
    Runs a local, unauthenticated proxy that forwards every request to
    an authenticated upstream proxy (HTTP, HTTPS, or SOCKS5).

    The forwarder owns a background thread with its own asyncio event
    loop, so start()/stop() are plain blocking calls -- nothing async
    leaks into the rest of your (presumably synchronous, Selenium-driven)
    code.
    """

    def __init__(self, host: str, port: int, username: str = None,
                 password: str = None, scheme: str = "http",
                 local_port: int = None, verbose=None):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._scheme = scheme  # "http" or "socks5"
        self._local_port = local_port
        self._verbose = verbose  # e.g. pass print for traffic logging

        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._handler = None
        self._args: Optional[dict] = None

        self.address: Optional[str] = None

    # ---- lifecycle -----------------------------------------------------

    def start(self) -> str:
        """Start the local forwarder. Returns 'host:port' for Chrome."""
        if self._thread is not None:
            return self.address  # already running, start() is idempotent

        local_port = self._local_port or _free_local_port()
        self.address = f"127.0.0.1:{local_port}"

        ready = threading.Event()
        startup_error: list = []

        def _run_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self._loop = loop
            try:
                server = pproxy.Server(f"http://127.0.0.1:{local_port}")
                remote = pproxy.Connection(_upstream_uri(
                    self._host, self._port, self._username,
                    self._password, self._scheme,
                ))
                self._args = dict(
                    rserver=[remote],
                    verbose=self._verbose or (lambda *args, **kwargs: None))
                self._handler = loop.run_until_complete(
                    server.start_server(self._args)
                )
            except Exception as exc:
                startup_error.append(exc)
                ready.set()
                return
            ready.set()
            try:
                loop.run_forever()
            finally:
                loop.run_until_complete(loop.shutdown_asyncgens())
                loop.close()

        self._thread = threading.Thread(target=_run_loop, daemon=True)
        self._thread.start()

        if not ready.wait(timeout=5):
            self._thread = None
            raise RuntimeError("Local proxy did not start within 5s")
        if startup_error:
            self._thread = None
            raise RuntimeError(
                f"Could not start local proxy on {self.address}: {startup_error[0]}"
            ) from startup_error[0]

        atexit.register(self.stop)  # safety net if the caller forgets to
        return self.address

    def stop(self) -> None:
        """Stop the local forwarder and release the port."""
        if self._thread is None or self._loop is None:
            return

        async def _close():
            if self._handler is not None:
                self._handler.close()
                await self._handler.wait_closed()

        try:
            future = asyncio.run_coroutine_threadsafe(_close(), self._loop)
            future.result(timeout=5)
        except Exception:
            pass  # best-effort -- we still want to tear the loop down below

        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join(timeout=5)
        self._thread = None
        self._loop = None
        self._handler = None

    def rotate(self, host: str, port: int, username: str = None,
               password: str = None, scheme: str = "http") -> None:
        """
        Swap the upstream proxy WITHOUT restarting the local listener, so
        Chrome keeps using the same local address (no driver restart).

        Connections opened after this call use the new upstream; anything
        already in flight finishes on the old one. For residential-pool
        rotation, call this between page loads/actions, not mid-request.
        """
        if self._args is None:
            raise RuntimeError("Call start() before rotate().")
        self._host, self._port = host, port
        self._username, self._password, self._scheme = username, password, scheme
        self._args["rserver"] = [pproxy.Connection(
            _upstream_uri(host, port, username, password, scheme)
        )]

    # ---- context manager -----------------------------------------------

    def __enter__(self) -> "ProxyForwarder":
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stop()


# ---- Phase-1-style functional API, for callers who'd rather not hold an
# object around -- both styles share the same ProxyForwarder underneath.

_active: dict[str, ProxyForwarder] = {}


def start_proxy(host: str, port: int, username: str = None,
                 password: str = None, scheme: str = "http") -> str:
    """Start a forwarder. Returns 'host:port' for --proxy-server."""
    forwarder = ProxyForwarder(host, port, username, password, scheme)
    address = forwarder.start()
    _active[address] = forwarder
    return address


def stop_proxy(address: str) -> None:
    """Stop a forwarder previously started with start_proxy()."""
    forwarder = _active.pop(address, None)
    if forwarder is not None:
        forwarder.stop()