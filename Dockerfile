FROM registry.access.redhat.com/ubi9/python-39
WORKDIR /opt/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the source afterwards to keep the cache
COPY . ./
RUN pip install --no-cache-dir .
CMD ["python", "-m", "cli.nfl_cli", "--help"]
