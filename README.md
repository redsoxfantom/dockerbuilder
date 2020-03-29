# DockerBuilder

Python 3 CLI application to assist with building and running docker containers

# Usage
    python -m dockerbuilder [-h] [--imagename IMAGENAME] [--version VERSION] [--dockerfile   DOCKERFILE] [--context CONTEXT] [--dev] [--dev_args DEV_ARGS] [--delete] [--latest] [--tags TAGS]

`-h, --help`  
Show this help message and exit

`--imagename IMAGENAME`  
Name of docker image to create. If not specified, defaults to the name of the folder 

`--version VERSION`  
Version to tag the resulting Docker image with. If not specified, searches in current working directory for a file called "VERSION" an tags image with the contents of that file. If that isn't found, defaults to '0.0.1'

`--dockerfile DOCKERFILE`  
Path to the Dockerfile to use for building. If not specified, defaults to '/current/working/directory/Dockerfile'

`--context CONTEXT`  
Path to the context to use when building. If not specified, defaults to '/current/working/directory'

`--dev`  
Creates a "dev" Docker image (image will be tagged with `:dev`, image will run immediately after being build). Note that passing `--dev` causes the `--latest` and `--tags` parameters to be ignored 

`--dev_args DEV_ARGS`  
Arguments to pass to Docker when running in dev mode. Defaults to "`-i -t --rm --network host --name <imagename>`"

`--delete`  
If a docker image with the same tag already exists, delete it before building

`--latest`  
Tag this image with 'latest'. This is functionally equivalent to passing `--tags "latest"`
  
`--tags TAGS`  
Comma separated list of tags to apply to the built image
