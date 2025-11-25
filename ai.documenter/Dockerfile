FROM golang:1.24 AS builder
WORKDIR /app
COPY . .
RUN go mod tidy
RUN go build -o documenter main.go

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/documenter .
ENTRYPOINT ["./documenter"]
