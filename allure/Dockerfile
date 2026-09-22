ARG ALLURE_VERSION=2.35.1
FROM openjdk:26-ea-jdk-slim AS builder
ARG ALLURE_VERSION
RUN apt-get update && apt-get install --no-install-recommends -y \
    wget=1.25.0-2 nginx=1.26.3-3+deb13u1 unzip=6.0-29 && \
    wget https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.zip -P /tmp/ && \
    unzip /tmp/allure-${ALLURE_VERSION}.zip -d /opt/ && \
    rm /tmp/allure-${ALLURE_VERSION}.zip && \
    apt-get remove -y wget unzip && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Add allure to PATH
ENV PATH="/opt/allure-${ALLURE_VERSION}/bin:${PATH}"

WORKDIR /app
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh && \
    mkdir -p /app/allure-results

ENTRYPOINT ["/app/entrypoint.sh"]