from conans import ConanFile

_expected = """
digraph {
        "None/None" -> "boost/1.73.0"
        "None/None" -> "spdlog/1.6.1"
        "None/None" -> "dot-graph-generator/0.1.0"
        "None/None" -> "catch2/2.12.2"
        "boost/1.73.0" -> "zlib/1.2.11"
        "boost/1.73.0" -> "bzip2/1.0.8"
        "spdlog/1.6.1" -> "fmt/6.2.0"
}
"""

class TestPackageConan(ConanFile):
    generators = "dot_graph"
    requires = [
        ("boost/1.73.0"),
        ("spdlog/1.6.1", "private")
    ]
    build_requires = "catch2/2.12.2"

    def test(self):
        with open("conangraph.dot", "r") as file:
            data = file.read()
            assert data.strip() == _expected.strip()
