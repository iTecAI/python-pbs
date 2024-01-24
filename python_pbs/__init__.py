from .extensions import *
from .util.typed_wrapper import Attribute

c = pbs_connect(None)

attrs = Attribute.make_attrl([Attribute(name="enabled"), Attribute(name="state_count")])

attr = attrl()
attr.name = ""

print(
    pbs_statque(
        c,
        "",
        attrs,
        None,
    )
)
