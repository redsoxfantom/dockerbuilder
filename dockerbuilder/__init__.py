import subprocess

def buildimage(context,dockerfile,imagename,should_delete,tags,dev_mode,dev_args):
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
        print("Container logs will be output below.\n"\
             F"Note that pressing 'ctrl-c' is not sufficient to kill the running container. You will need to run 'docker kill {imagename}'")
        docker = subprocess.call(runcmd)
            
        