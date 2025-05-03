from collections.abc import Mapping
from json import dumps as _json_dumps
from re import sub as _re_sub
from typing import Any, Literal

from markupy import Attribute, attribute_handlers

COMMA_SEPARATED = {
    "hx-select-oob",
    "hx-trigger",
    "hx-disabled-elt",
    "hx-ext",
    "hx-params",
}

SPACE_SEPARATED = {"hx-disinherit", "hx-inherit"}


@attribute_handlers.register
def htmx_handler(old: Attribute | None, new: Attribute) -> Attribute | None:
    if old is not None and old.value is not None and new.value is not None:
        # Allow attributes to be set multiple times and values appended
        separator = None
        if new.name in COMMA_SEPARATED:
            separator = ", "
        elif new.name in SPACE_SEPARATED:
            separator = " "

        if separator is not None:
            new.value = f"{old.value}{separator}{new.value}"
            return new
    return None


InheritedAttributes = Literal[
    "*",
    "hx-boost",
    "hx-confirm",
    "hx-disabled",
    "hx-encoding",
    "hx-headers",
    "hx-include",
    "hx-indicator",
    "hx-params",
    "hx-preserve",
    "hx-prompt",
    "hx-push-url",
    "hx-replace-url",
    "hx-request",
    "hx-select",
    "hx-select-oob",
    "hx-swap",
    "hx-sync",
    "hx-target",
    "hx-vals",
]

Selector = (
    Literal[
        "closest …",
        "find …",
        "next",
        "next …",
        "previous",
        "previous …",
    ]
    | str
)

SelectorThis = Selector | Literal["this"]

TriggerSelector = Selector | Literal["document", "window"]


Swap = Literal[
    "innerHTML",
    "outerHTML",
    "textContent",
    "beforebegin",
    "afterbegin",
    "beforeend",
    "afterend",
    "delete",
    "none",
]

HtmxEvent = Literal[
    "htmx:abort",
    "htmx:afterOnLoad",
    "htmx:afterProcessNode",
    "htmx:afterRequest",
    "htmx:afterSettle",
    "htmx:afterSwap",
    "htmx:beforeCleanupElement",
    "htmx:beforeOnLoad",
    "htmx:beforeProcessNode",
    "htmx:beforeRequest",
    "htmx:beforeSwap",
    "htmx:beforeSend",
    "htmx:beforeTransition",
    "htmx:configRequest",
    "htmx:confirm",
    "htmx:historyCacheError",
    "htmx:historyCacheMiss",
    "htmx:historyCacheMissError",
    "htmx:historyCacheMissLoad",
    "htmx:historyRestore",
    "htmx:beforeHistorySave",
    "htmx:load",
    "htmx:noSSESourceError",
    "htmx:onLoadError",
    "htmx:oobAfterSwap",
    "htmx:oobBeforeSwap",
    "htmx:oobErrorNoTarget",
    "htmx:prompt",
    "htmx:pushedIntoHistory",
    "htmx:replacedInHistory",
    "htmx:responseError",
    "htmx:sendAbort",
    "htmx:sendError",
    "htmx:sseError",
    "htmx:sseOpen",
    "htmx:swapError",
    "htmx:targetError",
    "htmx:timeout",
    "htmx:validation:validate",
    "htmx:validation:failed",
    "htmx:validation:halted",
    "htmx:xhr:abort",
    "htmx:xhr:loadend",
    "htmx:xhr:loadstart",
    "htmx:xhr:progress",
]

HtmlEvent = Literal[
    # Mouse / pointer
    "click",
    "dblclick",
    "mousedown",
    "mouseup",
    "mouseover",
    "mouseout",
    "mouseenter",
    "mouseleave",
    "mousemove",
    "contextmenu",
    # Pointer‑device–agnostic (covers mouse, touch, pen)
    "pointerdown",
    "pointerup",
    "pointermove",
    "pointerenter",
    "pointerleave",
    "pointerover",
    "pointerout",
    "pointercancel",
    # Touch
    "touchstart",
    "touchmove",
    "touchend",
    "touchcancel",
    # Keyboard & focus
    "keydown",
    "keyup",
    "keypress",  # keypress = legacy but still common
    "focus",
    "blur",
    "focusin",
    "focusout",
    # Forms & input
    "input",
    "change",
    "beforeinput",
    "invalid",
    "submit",
    "reset",
    # Clipboard & drag‑and‑drop
    "copy",
    "cut",
    "paste",
    "dragstart",
    "drag",
    "dragenter",
    "dragover",
    "dragleave",
    "drop",
    "dragend",
    # Media & resource loading
    "load",
    "error",
    "play",
    "pause",
    "volumechange",
    "timeupdate",
    "ended",
    "seeking",
    "seeked",
    "waiting",
    # Window / document lifecycle
    "visibilitychange",
    "scroll",
    "resize",
    "beforeunload",
    "unload",
]

TriggerEvent = Literal["load", "revealed", "intersect"] | HtmlEvent

TopBottom = Literal["top", "bottom"]


class HtmxAttributes:
    def get(self, url: str) -> Attribute:
        return Attribute("hx-get", url)

    def post(self, url: str) -> Attribute:
        return Attribute("hx-post", url)

    def delete(self, url: str) -> Attribute:
        return Attribute("hx-delete", url)

    def patch(self, url: str) -> Attribute:
        return Attribute("hx-patch", url)

    def put(self, url: str) -> Attribute:
        return Attribute("hx-put", url)

    def on(
        self,
        event: str | HtmxEvent | HtmlEvent,
        value: str,
    ) -> Attribute:
        event = _re_sub(r"([a-z0-9])([A-Z])", r"\1-\2", event)
        event = _re_sub(r"([A-Z]+)([A-Z][a-z])", r"\1-\2", event)
        return Attribute(f"hx-on:{event.lower()}", value)

    def push_url(self, value: str | bool) -> Attribute:
        return Attribute(
            "hx-push-url", str(value).lower() if isinstance(value, bool) else value
        )

    def select(self, selector: str) -> Attribute:
        return Attribute("hx-select", selector)

    def select_oob(self, *selector: str | tuple[str, Swap]) -> Attribute:
        values: list[str] = []
        for v in selector:
            if isinstance(v, tuple):
                values.append(":".join(v))
            else:
                values.append(v)
        return Attribute("hx-select-oob", ", ".join(values))

    def swap(
        self,
        swap: Swap,
        transition: bool | None = None,
        swap_ms: int | None = None,
        settle_ms: int | None = None,
        ignore_title: bool | None = None,
        scroll: TopBottom | tuple[str, TopBottom] | None = None,
        show: TopBottom | tuple[str, TopBottom] | None = None,
        focus_scroll: bool | None = None,
    ) -> Attribute:
        values: list[str] = [swap]
        if transition is not None:
            values.append(f"transition:{str(transition).lower()}")
        if swap_ms is not None:
            values.append(f"swap:{swap_ms}ms")
        if settle_ms is not None:
            values.append(f"settle:{settle_ms}ms")
        if ignore_title is not None:
            values.append(f"ignoreTitle:{str(ignore_title).lower()}")
        if scroll is not None:
            if isinstance(scroll, tuple):
                values.append(f"scroll:{':'.join(scroll)}")
            else:
                values.append(f"scroll:{scroll}")
        if show is not None:
            if isinstance(show, tuple):
                values.append(f"show:{':'.join(show)}")
            else:
                values.append(f"show:{show}")
        if focus_scroll is not None:
            values.append(f"focus-scroll={str(focus_scroll).lower()}")
        return Attribute("hx-swap", " ".join(values))

    def swap_oob(
        self, swap: Swap | Literal[True], selector: str | None = None
    ) -> Attribute:
        values: list[str] = []
        if swap is True:
            values.append(str(swap).lower())
        else:
            values.append(swap)
        if selector is not None:
            values.append(selector)

        return Attribute("hx-swap-oob", ":".join(values))

    def target(self, selector: SelectorThis) -> Attribute:
        return Attribute("hx-target", selector)

    def trigger(
        self,
        event: TriggerEvent | str,
        *,
        filters: str | None = None,
        once: bool = False,
        changed: bool = False,
        delay_ms: int | None = None,
        throttle_ms: int | None = None,
        from_selector: TriggerSelector | None = None,
        target_selector: str | None = None,
        consume: bool = False,
        queue: Literal["first", "last", "all", "none"] | None = None,
        intersect_root: str | None = None,
        intersect_threshold: float | None = None,
    ) -> Attribute:
        values = [event]
        if filters is not None:
            values.append(f"[{filters}]")
        if once is True:
            values.append("once")
        if changed is True:
            values.append("changed")
        if delay_ms is not None:
            values.append(f"delay:{delay_ms}ms")
        if throttle_ms is not None:
            values.append(f"delay:{throttle_ms}ms")
        if from_selector is not None:
            values.append(f"from:({from_selector})")
        if target_selector is not None:
            values.append(f"target:({target_selector})")
        if consume is True:
            values.append("consume")
        if queue is not None:
            values.append(f"queue:{queue}")
        if intersect_root is not None:
            values.append(f"root:{intersect_root}")
        if intersect_threshold is not None:
            values.append(f"threshold:{intersect_threshold}")
        return Attribute("hx-trigger", " ".join(values))

    def trigger_every_ms(self, every_ms: int, filters: str | None = None) -> Attribute:
        return self.trigger(
            f"every {every_ms}ms",
            filters=filters,
        )

    def vals(self, value: str | Mapping[Any, Any]) -> Attribute:
        res = _json_dumps(value) if isinstance(value, Mapping) else value
        return Attribute("hx-vals", res)

    def boost(self, value: bool) -> Attribute:
        return Attribute("hx-boost", str(value).lower())

    def confirm(self, message: str) -> Attribute:
        return Attribute("hx-confirm", message)

    def disable(
        self,
    ) -> Attribute:
        return Attribute("hx-disable", True)

    def disabled_elt(self, *selector: SelectorThis) -> Attribute:
        return Attribute("hx-disabled-elt", ", ".join(selector))

    def disinherit(self, *attributes: InheritedAttributes) -> Attribute:
        return Attribute("hx-disinherit", " ".join(attributes))

    def encoding(
        self,
        encoding: Literal[
            "application/x-www-form-urlencoded",
            "multipart/form-data",
        ],
    ) -> Attribute:
        return Attribute("hx-encoding", encoding)

    def ext(self, *extension: str, ignore: bool = False) -> Attribute:
        value = ", ".join(map(lambda e: f"ignore:{e}" if ignore else e, extension))
        return Attribute("hx-ext", value)

    def headers(self, value: str | Mapping[Any, Any]) -> Attribute:
        res = _json_dumps(value) if isinstance(value, Mapping) else value
        return Attribute("hx-headers", res)

    def history(self, value: bool) -> Attribute:
        return Attribute("hx-history", "false" if value is False else None)

    def history_elt(self, value: bool = True) -> Attribute:
        return Attribute("hx-history-elt", value)

    def include(self, selector: SelectorThis) -> Attribute:
        return Attribute("hx-include", selector)

    def indicator(self, selector: str | Literal["closest …"]) -> Attribute:
        return Attribute("hx-indicator", selector)

    def inherit(self, *attributes: InheritedAttributes) -> Attribute:
        return Attribute("hx-inherit", " ".join(attributes))

    def params(
        self, *param: Literal["*", "none"] | str, exclude: bool = False
    ) -> Attribute:
        value = ", ".join(param)
        if exclude:
            value = f"not {value}"
        return Attribute("hx-params", value)

    def preserve(self, value: bool = True) -> Attribute:
        return Attribute("hx-preserve", value)

    def prompt(self, message: str) -> Attribute:
        return Attribute("hx-prompt", message)

    def replace_url(self, value: bool | str) -> Attribute:
        return Attribute(
            "hx-replace-url", str(value).lower() if isinstance(value, bool) else value
        )

    def request(
        self,
        timeout_ms: int | None = None,
        credentials: bool | None = None,
        no_headers: bool | None = None,
    ) -> Attribute:
        value = {}
        if timeout_ms is not None:
            value["timeout"] = timeout_ms
        if credentials is not None:
            value["credentials"] = credentials
        if no_headers is not None:
            value["noHeaders"] = no_headers
        return Attribute("hx-request", _json_dumps(value))

    def sync(
        self,
        selector: SelectorThis,
        strategy: None
        | Literal[
            "drop",
            "abort",
            "replace",
            "queue",
            "queue first",
            "queue last",
            "queue all",
        ],
    ) -> Attribute:
        value = f"{selector}:{strategy}" if strategy else selector
        return Attribute("hx-sync", value)

    def validate(self, value: bool = True) -> Attribute:
        return Attribute("hx-validate", str(value).lower())
