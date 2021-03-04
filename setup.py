"""
jupyter_cadquery_widgets setup
"""
import json
from pathlib import Path

from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    skip_if_exists,
)
import setuptools

HERE = Path(__file__).parent.resolve()

# The name of the project
name = "jupyter_cadquery_widgets"
py_path = HERE / name
lab_path = HERE / name / "labextension"
js_path = HERE / "lib"

# Representative files that should exist after a successful build
# jstargets = [
#     str(lab_path / "package.json"),
# ]

package_data_spec = {
    name: ["*"],
}

labext_name = "jupyter_cadquery"

data_files_spec = [
    # JupyterLab 3
    ("share/jupyter/labextensions/%s" % labext_name, str(lab_path), "**"),
    ("share/jupyter/labextensions/%s" % labext_name, str(HERE), "install.json"),
    # Jupyter Notebook
    ("etc/jupyter/nbconfig", str(HERE / "jupyter-config"), "**/*.json"),
    ("share/jupyter/nbextensions/jupyter_cadquery", str(py_path / "nbextension"), "**/*.js"),
    ("share/jupyter/nbextensions/jupyter_cadquery", str(py_path / "nbextension"), "**/*.js.map"),
]

cmdclass = create_cmdclass(
    "jsdeps", package_data_spec=package_data_spec, data_files_spec=data_files_spec
)

cmdclass["jsdeps"] = combine_commands(
    install_npm(
        path=str(js_path),
        npm=["yarn"],
        build_cmd="build:prod",
    ),
    ensure_targets(
        [
            str(py_path / "nbextension" / "extension.js"),
            str(py_path / "nbextension" / "index.js"),
        ]
    ),
)

long_description = (HERE / "README.md").read_text()

# Get the package info from package.json
pkg_json = json.loads((HERE / "package.json").read_bytes())

setup_args = dict(
    name=name,
    version=pkg_json["version"],
    url=pkg_json["homepage"],
    author=pkg_json["author"]["name"],
    author_email=pkg_json["author"]["email"],
    description=pkg_json["description"],
    license=pkg_json["license"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    cmdclass=cmdclass,
    packages=setuptools.find_packages(),
    install_requires=["jupyterlab~=3.0", "ipywidgets~=7.6"],
    extras_require={
        "dev": {
            "jupyter-packaging",
            "cookiecutter",
            "twine",
            "bumpversion",
            "black",
            "pylint",
            "pyYaml",
        }
    },
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.6",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Jupyter", "JupyterLab", "JupyterLab3"],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Jupyter",
    ],
)


if __name__ == "__main__":
    setuptools.setup(**setup_args)
