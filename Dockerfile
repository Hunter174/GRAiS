FROM python:3.10-slim AS base-image

# Install system dependencies for PyAudio, gcc, and graphics libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    libasound-dev \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    pulseaudio \
    gcc \
    libgl1-mesa-glx \
    libmtdev-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    xorg \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file first and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install PulseAudio for sound management
RUN apt-get update && apt-get install -y pulseaudio
