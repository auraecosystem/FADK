FROM golang:1.21
# Fadaka node container
COPY . /app
RUN make build
CMD ["./fadaka-node"]
#  node container
COPY . /app
RUN make build
CMD ["./web4assetchain"]
