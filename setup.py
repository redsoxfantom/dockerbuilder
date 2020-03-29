import setuptools
import subprocess

version = "0.0.1+beta"
with open("VERSION") as f:
    version = f.read()

try:
    sha = subprocess.check_output(['git','rev-parse','--short','HEAD']).decode('ascii').strip()
    version = version + "+" + sha
except Exception:
    pass

package_short_desc = "CLI utility for quickly building / running docker images"
package_long_desc = package_short_desc
with open("README.md") as f:
    package_long_desc = f.read()

setuptools.setup(
    name="dockerbuilder-redsoxfantom",
    version=version,
    description=package_short_desc,
    long_description=package_long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/redsoxfantom/dockerbuilder",
    author="redsoxfantom",
    author_email="redsoxfantom@gmail.com",
    python_requires=">=3.7.0",
    packages=["dockerbuilder"]
)
