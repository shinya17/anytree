# -*- coding: utf-8 -*-
import six
from helper import eq_, eq_str

import anytree


def test_render_str():
    """Render string cast."""
    root = anytree.Node("root")
    s0 = anytree.Node("sub0", parent=root)
    anytree.Node("sub0B", parent=s0)
    anytree.Node("sub0A", parent=s0)
    anytree.Node("sub1", parent=root)
    r = anytree.RenderTree(root)

    expected = "\n".join(
        [
            "Node('/root')",
            "├── Node('/root/sub0')",
            "│   ├── Node('/root/sub0/sub0B')",
            "│   └── Node('/root/sub0/sub0A')",
            "└── Node('/root/sub1')",
        ]
    )
    eq_str(str(r), expected)

    r = anytree.RenderTree(root, childiter=lambda nodes: [n for n in nodes if len(n.name) < 5])

    expected = "\n".join(
        [
            "Node('/root')",
            "├── Node('/root/sub0')",
            "└── Node('/root/sub1')",
        ]
    )
    eq_str(str(r), expected)


def test_render_repr():
    """Render representation."""
    root = anytree.Node("root")
    anytree.Node("sub", parent=root)
    r = anytree.RenderTree(root)

    if six.PY2:
        expected = "RenderTree(Node('/root'), style=ContStyle(), " "childiter=<type 'list'>)"
    else:
        expected = "RenderTree(Node('/root'), style=ContStyle(), " "childiter=<class 'list'>)"
    eq_(repr(r), expected)


def test_render():
    """Rendering."""
    root = anytree.Node("root", lines=["c0fe", "c0de"])
    s0 = anytree.Node("sub0", parent=root, lines=["ha", "ba"])
    s0b = anytree.Node("sub0B", parent=s0, lines=["1", "2", "3"])
    s0a = anytree.Node("sub0A", parent=s0, lines=["a", "b"])
    s1 = anytree.Node("sub1", parent=root, lines=["Z"])

    r = anytree.RenderTree(root, style=anytree.DoubleStyle)
    result = [(pre, node) for pre, _, node in r]
    expected = [
        ("", root),
        ("╠══ ", s0),
        ("║   ╠══ ", s0b),
        ("║   ╚══ ", s0a),
        ("╚══ ", s1),
    ]
    eq_(result, expected)

    def multi(root):
        for pre, fill, node in anytree.RenderTree(root):
            yield "%s%s" % (pre, node.lines[0]), node
            for line in node.lines[1:]:
                yield "%s%s" % (fill, line), node

    result = list(multi(root))
    expected = [
        ("c0fe", root),
        ("c0de", root),
        ("├── ha", s0),
        ("│   ba", s0),
        ("│   ├── 1", s0b),
        ("│   │   2", s0b),
        ("│   │   3", s0b),
        ("│   └── a", s0a),
        ("│       b", s0a),
        ("└── Z", s1),
    ]
    eq_(result, expected)


def test_maxlevel():
    root = anytree.Node("root", lines=["c0fe", "c0de"])
    s0 = anytree.Node("sub0", parent=root, lines=["ha", "ba"])
    s0b = anytree.Node("sub0B", parent=s0, lines=["1", "2", "3"])
    s0a = anytree.Node("sub0A", parent=s0, lines=["a", "b"])
    s1 = anytree.Node("sub1", parent=root, lines=["Z"])

    r = anytree.RenderTree(root, maxlevel=2)
    result = [(pre, node) for pre, _, node in r]
    expected = [
        ("", root),
        ("├── ", s0),
        ("└── ", s1),
    ]
    print(expected)
    print(result)
    eq_(result, expected)


def test_asciistyle():
    style = anytree.AsciiStyle()
    eq_(style.vertical, "|   ")
    eq_(style.cont, "|-- ")
    eq_(style.end, "+-- ")


def test_contstyle():
    style = anytree.ContStyle()
    eq_(style.vertical, "\u2502   ")
    eq_(style.cont, "\u251c\u2500\u2500 ")
    eq_(style.end, "\u2514\u2500\u2500 ")


def test_controundstyle():
    style = anytree.ContRoundStyle()
    eq_(style.vertical, "\u2502   ")
    eq_(style.cont, "\u251c\u2500\u2500 ")
    eq_(style.end, "\u2570\u2500\u2500 ")


def test_doublestyle():
    style = anytree.DoubleStyle()
    eq_(style.vertical, "\u2551   ")
    eq_(style.cont, "\u2560\u2550\u2550 ")
    eq_(style.end, "\u255a\u2550\u2550 ")


def test_by_attr():
    """by attr."""
    root = anytree.Node("root", lines=["root"])
    s0 = anytree.Node("sub0", parent=root, lines=["su", "b0"])
    anytree.Node("sub0B", parent=s0, lines=["sub", "0B"])
    anytree.Node("sub0A", parent=s0)
    anytree.Node("sub1", parent=root, lines=["sub1"])
    eq_(anytree.RenderTree(root).by_attr(), "root\n├── sub0\n│   ├── sub0B\n│   └── sub0A\n└── sub1")
    eq_(anytree.RenderTree(root).by_attr("lines"), "root\n├── su\n│   b0\n│   ├── sub\n│   │   0B\n│   └── \n└── sub1")
    eq_(
        anytree.RenderTree(root).by_attr(lambda node: ":".join(node.name)),
        "r:o:o:t\n├── s:u:b:0\n│   ├── s:u:b:0:B\n│   └── s:u:b:0:A\n└── s:u:b:1",
    )
