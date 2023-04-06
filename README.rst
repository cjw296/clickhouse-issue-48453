.. code-block:: bash

    $ cd vcs/git/clickhouse-issue-48453/
    $ python3.11 -m venv .venv
    $ pip install -r requirements.txt
    ...

    $ python reproducer.py --sleep 3
    2023.04.06 07:22:24.449001 [ 45 ] {} <Information> Application: Ready for connections.
    2023-04-06T07:22:27.485347: Attempting to execute a statement...
    [('INFORMATION_SCHEMA',), ('default',), ('information_schema',), ('sampledb',), ('system',)]
    (.venv)(master +) tweedledee:clickhouse-issue-48453 chris:

    $ python reproducer.py
    2023.04.06 07:22:31.367542 [ 45 ] {} <Information> Application: Ready for connections.
    2023-04-06T07:22:31.413540: Attempting to execute a statement...
    Error on socket shutdown: [Errno 57] Socket is not connected
    Traceback (most recent call last):
      File "/Users/chris/vcs/git/clickhouse-issue-48453/reproducer.py", line 60, in <module>
        main(parser.parse_args().sleep)
      File "/Users/chris/vcs/git/clickhouse-issue-48453/reproducer.py", line 54, in main
        print(client.execute('SHOW DATABASES'))
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...
    File "clickhouse_driver/bufferedreader.pyx", line 240, in clickhouse_driver.bufferedreader.BufferedSocketReader.read_into_buffer
    EOFError: Unexpected EOF while reading bytes
