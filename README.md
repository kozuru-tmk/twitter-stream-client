## twitter_stream

### Installation

#### From Github

```
$ pip install git+https://github.com/kozuru-tmk/twitter_stream.git
```

#### Download and execute setup.py

```
$ git clone https://github.com/kozuru-tmk/twitter_stream.git
$ cd twitter_stream
$ python install setup.py
```

#### Download and copy to your project directory

```
$ git clone https://github.com/kozuru-tmk/twitter_stream.git
$ cp -a twitter_stream/twitter_stream /path/to/your-lib
$ PYTHONPATH=/path/to/your-lib python program-using-this-lib.py
```

Python 3.4 is supported.

### Execute example program

#### stream-api.py

0. Edit stream-api.py. Set your twitter application keys.
0. Execute!

```
$ python examples/stream-api.py --compressed --track tokyo
```
