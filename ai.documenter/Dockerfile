FROM golang:1.24 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -mod=vendor -o documenter main.go

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/documenter .
ENTRYPOINT ["./documenter"]
