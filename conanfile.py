from jinja2 import Template
from conans.model import Generator
from conans import ConanFile

dot_graph_j2_template = Template("""\
digraph {
    {%- for src, dst in graph_edges %}
        "{{ src }}" -> "{{ dst }}"
    {%- endfor %}
}

""")

class dot_graph(Generator):

    def _node(self, name, version):
        return "{}/{}".format(name, version)

    @property
    def filename(self):
        return "conangraph.dot"

    @property
    def content(self):
        graph_edges = []

        src = self._node(self.conanfile.name, self.conanfile.version)
        for name in self.conanfile.requires.keys():
            dst = self._node(name, self.conanfile.deps_cpp_info[name].version)
            graph_edges.append((src, dst))
        for (name, _) in self.conanfile.build_requires.keys():
            self.conanfile.output.warn(name)
            dst = self._node(name, self.conanfile.deps_cpp_info[name].version)
            graph_edges.append((src, dst))

        for name, cpp_info in self.conanfile.deps_cpp_info.dependencies:
            src = self._node(name, cpp_info.version)
            for dep in cpp_info.public_deps:
                dst = self._node(dep, self.conanfile.deps_cpp_info[dep].version)
                graph_edges.append((src, dst))

        return dot_graph_j2_template.render(graph_edges=graph_edges)

class DotGraphPackage(ConanFile):
     name = "dot-graph-generator"
     version = "0.1.0"
     url = "https://github.com/markushedvall/conan-dot-graph-generator"
     license = "MIT"
