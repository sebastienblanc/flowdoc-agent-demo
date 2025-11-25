FROM golang:1.24 AS builder
WORKDIR /app
COPY . .

RUN go mod tidy
RUN go mod download
RUN CGO_ENABLED=0 GOOS=linux go build -o documenter .

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/documenter .
ENTRYPOINT ["./documenter"]
