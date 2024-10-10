FROM python:3.12-bullseye

WORKDIR /src
# RUN apt-get update && \
#     apt-get install -y curl && \
#     curl https://sh.rustup.rs -sSf | sh -s -- -y && \
#     . $HOME/.cargo/env && \
#     apt-get clean

# # Set environment variables to ensure Rust and Cargo are available
# ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app/ ./app

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.wsgi:g_app", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "debug"]

# CMD ["flask", "--app", "app", "run"]