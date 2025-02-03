WARNING:Slept longer than interval because the interval between photos from the replayed dataset is longer. On the ISS, the actual interval may be closer to the value you have specified.
Traceback (most recent call last):
  File "/lib/python312.zip/_pyodide/_base.py", line 574, in eval_code_async
    await CodeRunner(
  File "/lib/python312.zip/_pyodide/_base.py", line 394, in run_async
    coroutine = eval(self.code, globals, locals)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "main.py", line 163, in <module>
    main(verbose=True)
  File "main.py", line 143, in main
    delta = time_delta(image_1, image_2)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "main.py", line 69, in time_delta
    results = execute_workers([
              ^^^^^^^^^^^^^^^^^
  File "main.py", line 34, in execute_workers
    worker.start()  # Start all threads
    ^^^^^^^^^^^^^^
  File "/lib/python312.zip/threading.py", line 992, in start
    _start_new_thread(self._bootstrap, ())
RuntimeError: can't start new thread
