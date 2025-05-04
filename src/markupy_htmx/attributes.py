from ._private import htmx as _htmx

get = _htmx.get
post = _htmx.post
delete = _htmx.delete
patch = _htmx.patch
put = _htmx.put
on = _htmx.on
push_url = _htmx.push_url
select = _htmx.select
select_oob = _htmx.select_oob
swap = _htmx.swap
swap_oob = _htmx.swap_oob
target = _htmx.target
trigger = _htmx.trigger
trigger_every_ms = _htmx.trigger_every_ms
vals = _htmx.vals
boost = _htmx.boost
confirm = _htmx.confirm
disable = _htmx.disable
disabled_elt = _htmx.disabled_elt
disinherit = _htmx.disinherit
encoding = _htmx.encoding
ext = _htmx.ext
headers = _htmx.headers
history = _htmx.history
history_elt = _htmx.history_elt
include = _htmx.include
indicator = _htmx.indicator
inherit = _htmx.inherit
params = _htmx.params
preserve = _htmx.preserve
prompt = _htmx.prompt
replace_url = _htmx.replace_url
request = _htmx.request
sync = _htmx.sync
validate = _htmx.validate

__all__ = [
    "get",
    "post",
    "delete",
    "patch",
    "put",
    "on",
    "push_url",
    "select",
    "select_oob",
    "swap",
    "swap_oob",
    "target",
    "trigger",
    "trigger_every_ms",
    "vals",
    "boost",
    "confirm",
    "disable",
    "disabled_elt",
    "disinherit",
    "encoding",
    "ext",
    "headers",
    "history",
    "history_elt",
    "include",
    "indicator",
    "inherit",
    "params",
    "preserve",
    "prompt",
    "replace_url",
    "request",
    "sync",
    "validate",
]
