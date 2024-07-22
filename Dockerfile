FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="noninteractive"

RUN apt-get update && apt-get upgrade -y && \
     apt-get install -y python3 wine64 libncurses5 gcc

RUN mkdir asfuzzer
COPY arch asfuzzer/arch
COPY AsFuzzer asfuzzer/AsFuzzer
COPY AsInferrer asfuzzer/AsInferrer
COPY bin asfuzzer/bin
COPY intel64 asfuzzer/intel64
COPY mutator asfuzzer/mutator
COPY fuzzer.py asfuzzer/fuzzer.py
COPY inferrer.py asfuzzer/inferrer.py
COPY gen.py asfuzzer/gen.py
COPY triage.py asfuzzer/triage.py


