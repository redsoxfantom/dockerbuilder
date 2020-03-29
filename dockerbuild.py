import sys
major = sys.version_info.major
minor = sys.version_info.minor
if major < 3 or (major == 3 and minor < 7):
    print("ERROR: Must be run with python 3.7 or higher")
    exit(1)

import subprocess
import json
import argparse
import os

with open("app/package.json") as f:
    package = json.load(f)
    version = package['version']

context = os.getcwd()
dockerfile = os.path.join(os.getcwd(),'Dockerfile')
should_delete = False
dev_mode = False
latest = False
tags = []
imagename = os.path.basename(os.getcwd())
dev_args = F"-i -t --rm --network host --name {imagename}"

parser = argparse.ArgumentParser(description="Build docker image")
parser.add_argument('--imagename',help=F"Name of docker image to create. If not specified, defaults to '{imagename}'")
parser.add_argument('--version',help=F"Version to tag the resulting Docker image with. If not specified, defaults to '{version}'")
parser.add_argument('--dockerfile',help=F"Path to the Dockerfile to use for building. If not specified, defaults to '{dockerfile}'")
parser.add_argument('--context',help=F"Path to the context to use when building. If not specified, defaults to '{context}'")
parser.add_argument('--dev',help="Creates a \"dev\" Docker image (image will be tagged with 'dev', image will be run in non-daemon mode)",action="store_true")
parser.add_argument('--dev_args',help=F"Arguments to pass to Docker when running in dev mode. Defaults to '{dev_args}'")
parser.add_argument('--delete',help="If a docker image with the same tag already exists, delete it",action="store_true")
parser.add_argument('--latest',help="Tag this image with 'latest'",action="store_true")
parser.add_argument('--tags',help="Comma separated list of tags to apply to the built image")
args = parser.parse_args()

if args.tags:
    tags = args.tags.split(",")
if args.imagename:
    imagename = args.imagename
if args.version:
    version = args.version
if args.dockerfile:
    dockerfile = args.dockerfile
if args.context:
    context = args.context
if args.dev:
    version="dev"
    dev_mode = True
if args.dev_args:
    dev_args = args.dev_args
if args.delete:
    should_delete = True
if args.latest:
    tags.append("latest")

if dev_mode:
    tags = ["dev"]
else:
    tags.append(version)

try:
    docker = subprocess.run(["docker","images"],capture_output=True)
    docker.check_returncode()
except:
    print("ERROR: 'dockerbuild.py' must be run by an account with access to the Docker daemon (root or a member of the 'docker' group)")
    exit(2)

print(F"Will create docker image '{imagename}' from Dockerfile '{dockerfile}' and context '{context}'")
if dev_mode:
    print("Will run created docker image in dev mode (image will be with 'dev' and will run in non-daemon mode)")
    if dev_args:
        print(F"Dev docker image will be run with the following args: {dev_args}")
else:
    print(F"Will tag the docker image with the following: {','.join(tags)}")

if should_delete:
    print("Will delete any docker images matching this image name and tags")
    for tag in tags:
        dockerimage = F"{imagename}:{tag}"
        docker = subprocess.run(["docker","images","-q",dockerimage],capture_output=True).stdout
        if docker:
            print(F"Deleting {dockerimage}")
            docker = subprocess.run(["docker","image","rm",dockerimage])
            docker.check_returncode()

dockertagslist = [["-t",F"{imagename}:{tag}"] for tag in tags]
dockertags = []
for dockertag in dockertagslist:
    for tag in dockertag:
        dockertags.append(tag)
buildcmd = ["docker","build","-f",dockerfile]
buildcmd.extend(dockertags)
buildcmd.append(context)
print(F"Building docker image ({' '.join(buildcmd)})")
docker = subprocess.run(buildcmd)
docker.check_returncode()

if dev_mode:
    runcmd = ["docker","run"]
    runcmd.extend(dev_args.split(" "))
    runcmd.append(F"{imagename}:dev")
    print(F"Running docker image ({' '.join(runcmd)})")
    subprocess.run(runcmd)
