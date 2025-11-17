ARG PYTHON_VERSION=3.12

FROM alpine as builder
ARG PYTHON_VERSION

# Install Python and build dependencies
RUN apk add --no-cache \
    python3~=${PYTHON_VERSION} \
    gcc \
    musl-dev \
    linux-headers \
    libffi-dev

# Install picows
RUN pip3 install --no-cache-dir picows

WORKDIR /usr/lib/python${PYTHON_VERSION}
RUN python -m compileall -o 2 .

# Move optimized .pyc files and clean up
RUN find . -name "*.cpython-*.opt-2.pyc" | awk '{print $1, $1}' | sed 's/__pycache__\///2' | sed 's/.cpython-[0-9]\{2,\}.opt-2//2' | xargs -n 2 mv
RUN find . -mindepth 1 | grep -v -E '^\./(encodings)([/.].*)?$' | xargs rm -rf
RUN find . -name "*.py" -delete
RUN find . -name "__pycache__" -exec rm -r {} +

FROM scratch
ARG PYTHON_VERSION

COPY --from=builder /usr/bin/python3 /
COPY --from=builder /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=builder /usr/lib/libpython${PYTHON_VERSION}.so.1.0 /usr/lib/libpython${PYTHON_VERSION}.so.1.0
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/ /usr/lib/python${PYTHON_VERSION}/

ENTRYPOINT ["/python3"]   
