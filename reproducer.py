from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from time import sleep
from uuid import uuid1

import docker
from clickhouse_driver import Client as ClickhouseClient

CLICKHOUSE_CONFIG = str((Path(__file__).parent / 'config').absolute())


def main(wait_for_startup: float = 0):
    client = docker.from_env()
    password = str(uuid1())
    container = client.containers.run(
        'docker.io/clickhouse/clickhouse-server:latest',
        environment={
            'CLICKHOUSE_USER': 'clickhouseuser',
            'CLICKHOUSE_PASSWORD': password,
            'CLICKHOUSE_DB': 'sampledb',
            'CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT': '1',
            'CLICKHOUSE_LOG_LEVEL': 'TRACE',
        },
        ports={'9000/tcp': 0},
        detach=True,
        auto_remove=True,
        volumes={CLICKHOUSE_CONFIG: {'bind': '/etc/clickhouse-server/config.d/', 'mode': 'ro'}},
    )
    container = client.containers.get(container.id)
    port = int(container.ports[f'9000/tcp'][0]['HostPort'])

    starting = True
    while starting:
        log = container.logs()
        index = 0
        index = log.find(b'<Information> Application: Ready for connections.', index)
        if index < 0:
            sleep(0.01)
        else:
            starting = False
            print(log.split(b'\n')[-2].decode())

    client = ClickhouseClient(
        host='127.0.0.1',
        port=port,
        user='clickhouseuser',
        password=password
    )

    sleep(wait_for_startup)

    print(f'{datetime.utcnow().isoformat()}: Attempting to execute a statement...')
    print(client.execute('SHOW DATABASES'))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--sleep', type=float, default=0)
    main(parser.parse_args().sleep)
