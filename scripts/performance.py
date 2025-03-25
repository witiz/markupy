import cProfile

from markupy.tag import Table, Tbody, Td, Th, Thead, Tr

rows = list(range(50_000))


def render_markupy_attr() -> str:
    return str(
        Table[
            Thead[Tr[Th["Row #"]]],
            Tbody[(Tr(".row")[Td(dataValue=row)[row]] for row in rows)],
        ]
    )


with cProfile.Profile() as pr:
    render_markupy_attr()
    # Results can be wiewed with snakeviz
    # uvx snakeviz output.prof
    pr.dump_stats("output.prof")
    # pr.print_stats(sort="tottime")
