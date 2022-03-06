import datetime
import json
import redis
import os
import importlib.util
import time

USER_MODULE_FILE_PATH = '/opt/usermodule.py'


class Context:
    host = ''
    port = 1234
    input_key = ''
    output_key = ''
    last_execution = None
    env = {}

    def __init__(self, host: str, port: int, input_key=None, output_key=None):
        self.host = host
        self.port = port
        self.input_key = input_key
        self.output_key = output_key
        self.function_getmtime = os.path.getmtime(USER_MODULE_FILE_PATH)
        self.last_execution = None

    def update_last_exec_time(self):
        self.last_execution = datetime.datetime.now()


def main():
    global USER_MODULE_FILE_PATH

    REDIS_HOST = os.getenv('REDIS_HOST', "localhost")
    REDIS_PORT = int(os.getenv('REDIS_PORT', 9999))
    REDIS_INPUT_KEY = os.getenv('REDIS_INPUT_KEY', None)
    REDIS_OUTPUT_KEY = os.getenv('REDIS_OUTPUT_KEY', None)
    INTERVAL_TIME = int(os.getenv('INTERVAL', 5))

    # allow overriding the path to usermodule.py
    USER_MODULE_FILE_PATH = os.getenv('USER_MODULE_FILE_PATH', USER_MODULE_FILE_PATH)

    assert os.path.isfile(USER_MODULE_FILE_PATH)
    # import custom handler from /opt/usermodule.py
    spec = importlib.util.spec_from_file_location('usermodule', USER_MODULE_FILE_PATH)
    if not spec:
        print(f"Cannot load {USER_MODULE_FILE_PATH}")
        exit(1)
    usermodule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(usermodule)

    # connect to redis
    assert REDIS_INPUT_KEY
    assert REDIS_OUTPUT_KEY
    r_server = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset="utf-8", decode_responses=True)

    # main routine
    context = Context(host=REDIS_HOST, port=REDIS_PORT, input_key=REDIS_INPUT_KEY, output_key=REDIS_OUTPUT_KEY)

    # polling
    while True:
        try:
            data = r_server.get(REDIS_INPUT_KEY)
            data = json.loads(data)

            output = usermodule.handler(data, context)

            r_server.set(REDIS_OUTPUT_KEY, json.dumps(output))
        except Exception as e:
            print(f'ERROR when running serverless function: {e}')
            continue

        context.update_last_exec_time()
        time.sleep(INTERVAL_TIME)


if __name__ == '__main__':
    main()
