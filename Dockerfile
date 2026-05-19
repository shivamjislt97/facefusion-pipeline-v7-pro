FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04

ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility,video
ENV CUDA_DEVICE_ORDER=PCI_BUS_ID
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/workspace

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    ffmpeg git wget curl \
    libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6 \
    libgomp1 libopenblas-dev rclone \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY requirements.txt ./
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

COPY . /workspace/

RUN mkdir -p pipeline/logs workspace persistent outputs

COPY docker/healthcheck.sh /healthcheck.sh
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /healthcheck.sh /entrypoint.sh

HEALTHCHECK --interval=30s --timeout=15s --start-period=90s --retries=3 \
    CMD /healthcheck.sh

EXPOSE 7860

CMD ["/entrypoint.sh"]
