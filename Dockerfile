FROM python:3.11.0a2-alpine
RUN apk add --no-cache git && pip install pygithub
RUN git clone https://github.com/aidan-moj/truffleHog.git
RUN cd truffleHog && pip install -e .
ADD ./massTruffle.py /root
RUN chmod u+x /root/massTruffle.py
ENTRYPOINT ["/root/massTruffle.py"]
WORKDIR /output
