# NCATS: PCA Reports

The files needed reporting on Phishing Campaign Assessment (PCA) data.

## Configuration

The `pca-reports` library requires a configuration file.  If that file does not exist, it will be created when a PCA script attempts to read it.  You should then edit the file to ensure it is correct for your environment.  The default location for this file is `/etc/pca/pca.yml`.  An example configuration is below.

### `/etc/pca/pca.yml`
```
default-section: production-read

production-read:
  database-name: pca
  database-uri: mongodb://<MONGO_USERNAME>:<MONGO_PASSWORD>@host.docker.internal:27017/pca

production-write:
  database-name: pca
  database-uri: mongodb://<MONGO_USERNAME>:<MONGO_PASSWORD>@host.docker.internal:27017/pca
```

## Using PCA Commands with Docker
The PCA commands implemented in the docker container can be aliased into the host environment by using the procedure below.

Alias the container commands to the local environment:
```bash
eval "$(docker run ncats/pca-reports)"
```

To run a PCA command:
```bash
pca-report -h
```

### Caveats, and Gotchas

Whenever an aliased PCA command is executed, it will use the current working directory as its home volume.  This limits your ability to use absolute paths as parameters to commands, or relative paths that reference parent directories, e.g.; `../foo`.  That means all path parameters to a PCA command must be in the current working directory, or a subdirectory.  

| Do this?        | Command                                   | Reason  |
| ------------- |---------------------------------------------| --------|
| Yes           | `pca-import --customer CUST.json`           | parameter file is in the current directory |
| Yes           | `pca-import --customer sample/CUST.json`    | parameter file is in a sub-directory |
| NO!           | `pca-import --customer ../CUST.json`        | parameter file is in a parent directory |
| NO!           | `pca-import --customer /tmp/CUST.json`      | parameter file is an absolute path |

### Advanced configuration

By default, the container will look for your PCA configuration in `/etc/pca`.  This location can be changed by setting the `PCA_CONF_DIR` environment variable to point to your PCA configuration directory.  The commands will also attempt to run using the `ncats/pca-reports` image.  A different image can be used by setting the `PCA_REPORTS_IMAGE` environment variable to the image name.

Example:
```
export PCA_CONF_DIR=/private/etc/pca
export PCA_REPORTS_IMAGE=dhub.ncats.cyber.dhs.gov:5001/pca-reports
```

### Building the pca-reports container
To build the Docker container for pca-reports:

```bash
docker build -t ncats/pca-reports .
```

## Manual Installation
To manually install on your host system, run the following command from the pca-reports source directory:
`sudo pip install --no-cache-dir .`

## Development Installation
If you are developing the source, the following installation command will allow in-place editing with live updates to the libraries and command line utilities:
`sudo pip install --no-cache-dir -e .[dev]`
