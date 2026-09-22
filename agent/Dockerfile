FROM git.moevm.info/projects/cyp_test_lib_image:origins_restructuring_v1.0

RUN apt-get update && apt-get install -y \
    sshpass=1.10-0.1 && \
    apt-get clean

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh run_tests.py .

ENTRYPOINT ["/src/entrypoint.sh"]
