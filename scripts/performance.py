import cProfile

from markupy import View
from markupy.tag import Table, Tbody, Td, Th, Thead, Tr

rows = list(range(50_000))


def render() -> View:
    return Table[
        Thead[Tr[Th["Row #"]]],
        Tbody[(Tr(".row")[Td(dataValue=row)[row]] for row in rows)],
    ]


with cProfile.Profile() as pr:
    str(render())
    # Results can be wiewed with snakeviz
    # uvx snakeviz output.prof
    pr.dump_stats("output.prof")
    # pr.print_stats(sort="tottime")
