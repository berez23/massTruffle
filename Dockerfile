FROM python:3-alpine
RUN apk add --no-cache git && pip install trufflehog pygithub
ADD ./massTruffle.py /root
RUN chmod u+x /root/massTruffle.py
ENTRYPOINT ["/root/massTruffle.py"]
WORKDIR /output
