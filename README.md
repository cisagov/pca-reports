PCA Reports
=============

The files needed for reporting on a Phishing Campaign Assessment.  


Installation
------------
The following installation will allow in-place editing with live updates to all files:

sudo pip install -r requirements.txt

Configuration file:
The PCA tools will read `/etc/pca/pca.yml`
If that file does not exist, it will be created when a PCA script attempts to read it.  You should then edit the file to ensure it is correct for your environment.


Docker Goodies
--------------
To build the Docker container for pca-reports locally:
```bash
docker build -t ncats/pca-reports .
```

To build the Docker container for pca-reports in NCATS Docker hub:
```bash
docker build -t dhub.ncats.cyber.dhs.gov:5001/pca-reports .
```

Create aliases to the run commands inside a container (replace paths below as appropriate):
```bash
alias pca-import='docker run -it --rm --volume /private/etc/pca:/etc/pca --volume /tmp/pca:/home/pca dhub.ncats.cyber.dhs.gov:5001/pca-reports pca-import'
alias pca-report='docker run -it --rm --volume /private/etc/pca:/etc/pca --volume /tmp/pca:/home/pca dhub.ncats.cyber.dhs.gov:5001/pca-reports pca-report'
alias pca-tool='docker run -it --rm --volume /private/etc/pca:/etc/pca --volume /tmp/pca:/home/pca dhub.ncats.cyber.dhs.gov:5001/pca-reports pca-tool'
alias pca-template-preview='docker run -it --rm --volume /private/etc/pca:/etc/pca --volume /tmp/pca:/home/pca dhub.ncats.cyber.dhs.gov:5001/pca-reports pca-template-preview'
```

To run a command after creating aliases above and sourcing them in your shell:
```bash
pca-import -h
pca-tool -h
pca-report -h
pca-template-preview -h
```

To start a new pca-reports container and attach to a shell (replace paths below as appropriate):
```bash
docker run -it --volume /private/etc/pca:/etc/pca --volume /tmp/pca:/home/pca --entrypoint /bin/bash dhub.ncats.cyber.dhs.gov:5001/pca-reports
```
