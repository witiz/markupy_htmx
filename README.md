# markupy_htmx

## Project description

`markupy_htmx` is an extension for [`markupy`](https://markupy.witiz.com) that allows for a simpler HTMX attribute generation by enabling the following:

- Full coverage of HTMX attributes, all rewritten as convenient Python functions/helpers
- Static typing to improve reliability and error detection
- IDE autocomplete of existing attributes and for each of them, parameter types and values

## Installation

`markupy_htmx` can be installed via [PYPI](https://pypi.org/project/markupy_htmx/):

```sh
pip install markupy_htmx
```

Like its dependency `markupy`, it is targeting Python 3.10+ versions.


## Basic usage

All HTMX attributes are exposed via `markupy_htmx.attributes` that we recommend you alias to `hx` in order to call attributes with `hx.attr(...)`

```python
from markupy.elements import Button
from markupy_htmx import attributes as hx

el = Button(hx.post("/clicked"), hx.swap("outerHTML"))["Click me"]
print(el)
```

The generated HTML will be the following:

```html
<button hx-post="/clicked" hx-swap="outerHTML">Click Me</button>
```

## Advanced usage

As you saw above, most of the `markupy_htmx` attributes have exactly the same construct as their "native" counterpart.
Some attributes benefited from small adjustments, mostly to improve developer experience and ensure compatibility with Python.

### hx-on:* attribute

As opposed to the HTMX native attribute that expects the event as part of the attribute name, `markupy_htmx` expects the event as the very first argument of `hx.on()`:

```python
Button(hx.on("htmx:beforeRequest", "alert('Making a request!')"))
```

```html
<button hx-on:htmx:before-request="alert(&#39;Making a request!&#39;)"></button>
```

Several things to note here:

- The event name can be written both in it's original "camelCase" Javascript syntax or the adapted "kebab-case" syntax enforced by HTMX when written as part of the attribute name
- All valid HTMX events and standard HTML events will be autocompleted by your IDE for convenience, but you can as well type your own events
- The Javascript content is escaped by `markupy` when it is rendered as part of an attribute's value, but the code is interpreted normally by the browsers

### Multi-value attributes

Some HTMX attributes accept multiple values (either comma or space separated).
To make it more convenient for you to provide these values without having to remember the expected params or value separator, `markupy_htmx` allows for multiple definitions of the same attribute and will take care of the concatenation for you.

Here's the list of such attributes:

- hx-select-oob
- hx-trigger
- hx-disabled-elt
- hx-ext
- hx-params
- hx-disinherit
- hx-inherit

#### hx-select-oob

```python
from markupy.elements import Input
from markupy_htmx import attributes as hx

el1 = Input(hx.select_oob("#hello"), hx.select_oob(("#alert", "afterbegin")))
el2 = Input(hx.select_oob("#hello", ("#alert", "afterbegin")))
```

Both elements `el1` and `el2`are equivalent and will render as:

```html
<input hx-select-oob="#hello, #alert:afterbegin">
```

#### hx-trigger

```python
from markupy.elements import Button
from markupy_htmx import attributes as hx

Button(hx.trigger("load"), hx.trigger("click", delay_ms=1000))["Click"]
```

```html
<button hx-trigger="load, click delay:1000ms">Click</button>
```

Talking about the `hx-trigger` attribute, it has a special variant called `hx.trigger_every_ms()` that is used for polling. It's a dedicated method because it takes different params from the regular "event based" triggers:

```python
Button(hx.trigger_every_ms(1000, filters="myConditional"))
```

```html
<button hx-trigger="every 1000ms [myConditional]"></button>
```

### Python `dict` to JSON

Some attributes such as `hx-vals`, `hx-headers` or `hx-request` take JSON objects as arguments. With `markupy_htmx`, you can write them as `dict` and they will be properly converted (and escaped):

```python
Button(hx.vals({"myStr": "My Value", "anInt": 3, "aBool": True}))
```

### Boolean attributes

HTMX has a lot of boolean attributes and properties. All of them are mapped to Python `bool`:

```python
Body(hx.boost(True), hx.push_url(False))
```

Some boolean attributes can also omit a value and will take a default value:

```python
Div(hx.preserve())
Div(hx.disable())
```