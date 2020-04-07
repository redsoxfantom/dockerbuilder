FROM python:3.7.7-slim

COPY . /dockerbuilder

WORKDIR /dockerbuilder 

RUN ["pip","install","."]