import sys

from ._private import HtmxAttributes

hx: HtmxAttributes = HtmxAttributes(__name__)
sys.modules[__name__] = hx

get = hx.get
post = hx.post
delete = hx.delete
patch = hx.patch
put = hx.put
on = hx.on
push_url = hx.push_url
select = hx.select
select_oob = hx.select_oob
swap = hx.swap
swap_oob = hx.swap_oob
target = hx.target
trigger = hx.trigger
trigger_every_ms = hx.trigger_every_ms
vals = hx.vals
boost = hx.boost
confirm = hx.confirm
disable = hx.disable
disabled_elt = hx.disabled_elt
disinherit = hx.disinherit
encoding = hx.encoding
ext = hx.ext
headers = hx.headers
history = hx.history
history_elt = hx.history_elt
include = hx.include
indicator = hx.indicator
inherit = hx.inherit
params = hx.params
preserve = hx.preserve
prompt = hx.prompt
replace_url = hx.replace_url
request = hx.request
sync = hx.sync
validate = hx.validate

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
