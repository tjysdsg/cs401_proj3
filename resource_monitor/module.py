import numpy as np
from typing import Dict, Any


class Queue:  # more suitable than queue.Queue
    def __init__(self, maxsize: int):
        self.data = []
        self.maxsize = maxsize

    def append(self, x):
        if len(self.data) >= self.maxsize:
            del self.data[0]

        self.data.append(x)

    def front(self):
        return self.data[0]

    def avg(self, n_samples: int):
        assert 0 < n_samples <= self.maxsize

        curr_size = len(self.data)

        if n_samples >= curr_size:
            return np.mean(self.data)

        data = self.data[curr_size - n_samples:]
        return np.mean(data)


class CPUEnv:
    def __init__(self, n_cpus: int):
        self.n_cpus = n_cpus
        self.data = {i: Queue(maxsize=720) for i in range(n_cpus)}

    def get_cpu_data(self, idx: int) -> Queue:
        return self.data[idx]


def handler(data: dict, context: object) -> Dict[str, Any]:
    # assume this is called every 5 seconds, so 1 min moving average needs 12 data points, 1 hour needs 720

    ret = {}
    try:
        if getattr(context, 'cpu_env', None) is None:
            # find the number of cpus
            n_cpus = 0
            for i in range(9999):
                if f'cpu_percent-{i}' not in data:
                    n_cpus = i
                    break

            assert n_cpus > 0
            context.cpu_env = CPUEnv(n_cpus)

        cpu_env = context.cpu_env
        n_cpus = cpu_env.n_cpus

        for i in range(n_cpus):
            cpu_env.get_cpu_data(i).append(data[f'cpu_percent-{i}'])
            ret[f'cpu_{i}_1min_avg'] = cpu_env.get_cpu_data(i).avg(12)
            ret[f'cpu_{i}_1hr_avg'] = cpu_env.get_cpu_data(i).avg(720)
    except Exception as e:
        ret['error'] = str(e)

    return ret
