FROM python:3.11.9-slim

RUN apt-get update

WORKDIR /src

COPY src/requirements.txt src/requirements.txt
RUN pip install -r src/requirements.txt

COPY src /src

ENV PORT 8080

EXPOSE $PORT

CMD ["bash"]