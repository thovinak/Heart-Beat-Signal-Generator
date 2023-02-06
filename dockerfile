FROM python:3
LABEL App.Maintainer="Karthik Thovinakere"
LABEL App.eMail="thovinak@mcmaster.ca"
LABEL App.Name="Noise Generator"

ARG SHELL="/bin/bash"

#ENV SAVE_IMG=NULL
ENV IMG_DIR="/snapshots"
ENV t = "np.linspace(0, 10, 1000)"
ENV amplitude = "1"
ENV frequency = "1.25"
ENV plot_freq = "0"
ENV noise_level = "0.5"
#ENV DEBUG=NULL

VOLUME ${IMG_DIR}

# add curl for healthcheck
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip3 install --upgrade --no-cache-dir pip && \
    pip3 install --no-cache-dir -r requirements.txt
COPY main.py .

CMD ["python3", "main.py"]