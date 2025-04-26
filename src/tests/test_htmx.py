from markupy import elements as el

from markupy_htmx import attributes as hx


def test_get() -> None:
    assert el.Input(hx.get("hello")) == """<input hx-get="hello">"""


def test_on() -> None:
    assert (
        el.Input(hx.on("htmx:beforeRequest", "alert('Making a request!')"))
        == """<input hx-on:htmx:before-request="alert(&#39;Making a request!&#39;)">"""
    )


def test_on_case() -> None:
    assert (
        el.Input(hx.on("htmx:noSSESourceError", ""))
        == el.Input(hx.on("htmx:no-sse-source-error", ""))
        == """<input hx-on:htmx:no-sse-source-error="">"""
    )


def test_select_oob() -> None:
    assert (
        el.Input(hx.select_oob("#hello"), hx.select_oob(("#alert", "afterbegin")))
        == el.Input(hx.select_oob("#hello", ("#alert", "afterbegin")))
        == """<input hx-select-oob="#hello, #alert:afterbegin">"""
    )


def test_target() -> None:
    assert el.Input(hx.target("closest tr")) == """<input hx-target="closest tr">"""
    assert el.Input(hx.target("#foo")) == """<input hx-target="#foo">"""


def test_trigger() -> None:
    assert (
        el.Input(
            hx.trigger(
                "input",
                changed=True,
                delay_ms=1000,
                from_selector="form input",
                target_selector=".row input",
            )
        )
        == """<input hx-trigger="input changed delay:1000ms from:(form input) target:(.row input)">"""
    )


def test_trigger_every() -> None:
    assert (
        el.Input(hx.trigger_every_ms(1000, filters="myConditional"))
        == """<input hx-trigger="every 1000ms [myConditional]">"""
    )


def test_trigger_multi() -> None:
    assert (
        el.Input(hx.trigger("load"), hx.trigger("click", delay_ms=1000))
        == """<input hx-trigger="load, click delay:1000ms">"""
    )


def test_vals() -> None:
    assert (
        el.Input(hx.vals({"myStr": "My Value", "anInt": 3, "aBool": True}))
        == """<input hx-vals="{&#34;myStr&#34;: &#34;My Value&#34;, &#34;anInt&#34;: 3, &#34;aBool&#34;: true}">"""
    )
    assert (
        el.Input(hx.vals("js:{myVal: calculateValue()}"))
        == """<input hx-vals="js:{myVal: calculateValue()}">"""
    )


def test_disabled_elt() -> None:
    assert (
        el.Input(hx.disabled_elt("a", "p"), hx.disabled_elt("i"))
        == """<input hx-disabled-elt="a, p, i">"""
    )


def test_disinherit() -> None:
    assert (
        el.Input(hx.disinherit("hx-confirm", "hx-boost"))
        == el.Input(hx.disinherit("hx-confirm"), hx.disinherit("hx-boost"))
        == """<input hx-disinherit="hx-confirm hx-boost">"""
    )


def test_ext() -> None:
    assert (
        el.Input(hx.ext("a", "b"))
        == el.Input(hx.ext("a"), hx.ext("b"))
        == """<input hx-ext="a, b">"""
    )


def test_ext_ignore() -> None:
    assert (
        el.Input(hx.ext("a", "b", ignore=True))
        == el.Input(hx.ext("a", ignore=True), hx.ext("b", ignore=True))
        == """<input hx-ext="ignore:a, ignore:b">"""
    )


def test_history() -> None:
    assert el.Input(hx.history(True)) == """<input>"""
    assert el.Input(hx.history(False)) == """<input hx-history="false">"""


def test_params() -> None:
    assert el.Input(hx.params("a", "b")) == """<input hx-params="a, b">"""
    assert (
        el.Input(hx.params("a", "b", exclude=True))
        == """<input hx-params="not a, b">"""
    )
