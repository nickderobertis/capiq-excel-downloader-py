import multiprocessing as mp

class TimeoutWrapper:

    def __init__(self, timeout, func, timeout_callback):
        self.timeout = timeout
        self.func = func
        self.timeout_callback = timeout_callback

    def __call__(self,  *func_args, timeout_callback_kwargs={},  **func_kwargs):

        with mp.Pool(1) as p:
            result_promise = p.apply_async(self.func, args=func_args, kwds=func_kwargs, error_callback=_raise_exception)

            try:
                result = result_promise.get(self.timeout)
                return result
            except mp.TimeoutError:
                # Run timeout callback outside of pool
                pass

        # code only reaches here in mp.TimeoutError
        return self.timeout_callback(**timeout_callback_kwargs)



def _raise_exception(exception: Exception):
    raise exception