import time


def time_cost(func):
    def new_func(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        runtime = end_time - start_time
        print(f"Function '{func.__name__}' ran in: {runtime:.4f} seconds")
        return result
    return new_func

'''
进如虚拟环境
.\.venv\Scripts\activate
退出
deactivate
'''