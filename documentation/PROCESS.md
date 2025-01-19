0. `jutge-exec` scripts are installed in the images through a Git submodule. So images contain the following scripts: `jutge-submit`, `jutge-start`, `jutge-sanitize`, `jutge-somhi`, `jutge-kill-nobody` (compiled in the Docker build process).

1. The queue connects directly through SSH to a worker, and it runs there an image within which [launches `jutge-submit`](https://github.com/jutge-org/jutge-queue/blob/4c6dc8066477ce858ada93c525fd25d613b25ac1/src/services/queue.ts#L155)

    The full command is:

    ```bash
    docker run --rm -i --network none --cpus=1 --memory=1g
       jutgeorg/<imageid>
       jutge-submit jutge-run <image-id> <task_id>
    ``` 

    NOTE: It seems like `jutge-run` is not being used, right now, since `jutge-run` was just a wrapper for the Docker command which the queue issues directly. However, it might be convenient to launch a judging process?

2. `jutge-submit` does the "unboxing" of the submission:
    - Makes a directory on the queue for the `$name` sent (now it seems to be `jutge-run`!). This is unnecessary since all of it is run inside a Docker container which will disappear (`--rm`) option.
    - Changes to that directory.
    - Extracts a tar file from the standard input.
    - Changes permissions in the directory for security.
    - Sets a timeout of 320 secons (5 minutes and 20 seconds).
    - Launches `jutge-start`, a Python script.
    - After that, `jutge-sanitize` cleans up.
    - A `correction.tgz` for the `correction` folder is created and sent to the standard output.
    - Some cleanup is done.

3. `jutge-start` is a Python script which:
    - Sets resource limits (CORE = 0?, CPU = 300s)
    - Sets a `umask` of `0x077`.
    - Decompresses the three parts of the problem: `submission.tgz`, `problem.tgz`, and `driver.tgz` into folders with the same name.
    - Makes 2 directories: `solution`, and `correction`.
    - **Executes de driver**: 
        - Now it can only be a Python script called `driver/judge.py`. Here the `name` argument passed from above is still being passed down.
        - With Python, it pipes both stdout and stderr to `stdout.txt` and `stderr.txt`. 
        - Gets the return code of the process.
        - This execution will have as working directory the place where `.tar.gz` were decompressed. It now has this folders: `driver`, `submission`, `problem`, `solution`, and `correction`.
    - It compresses `correction.tgz` from the `correction` directory.
    - Flushes streams (stdout, stderr). Also closes them (?).

4. The driver starts the judging process...

We should make a single `jutge-exec` (Python or not) which deals with all of this in a single place. It can do what `jutge-submit` does directly, and also integrate `jutge-sanitize` and `jutge-somhi` as well. We then would have a single managing process inside the container, aside from the driver itself. The number of scripts and necessary names is confusing and error-prone.


