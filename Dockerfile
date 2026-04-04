FROM public.ecr.aws/docker/library/python:3.10-slim
ENV LOG_LEVEL=INFO
WORKDIR /app
RUN useradd -m appuser
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src /app
COPY tests /app/tests
RUN chown -R appuser:appuser /app
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
RUN  python -m unittest discover -s tests -v
CMD ["python", "-m", "HiveBox"]
