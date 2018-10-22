FROM ncats/pca-core
MAINTAINER David Redmin <david.redmin@hq.dhs.gov>
ENV PCA_REPORTS_SRC="/usr/src/pca-reports"

USER root

# Install LaTeX packages
RUN apt-get update && apt-get -y install \
    texlive-xetex \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra

# Install our own fonts
COPY pca_report/assets/Fonts /usr/share/fonts/truetype/ncats
RUN fc-cache -fsv

WORKDIR ${PCA_REPORTS_SRC}
COPY . ${PCA_REPORTS_SRC}

RUN pip install --no-cache-dir .[dev]
RUN ln -snf ${PCA_REPORTS_SRC}/var/getenv /usr/local/bin

USER pca
WORKDIR ${PCA_HOME}
CMD ["getenv"]
