def config(cls: object):
    return {key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith('__')}


@config
class Qwen8gb:
    repo_id = "Qwen/Qwen2.5-Coder-7B-Instruct-GGUF"
    filename = "qwen2.5-coder-7b-instruct-q8_0.gguf"
    verbose = False
    n_gpu_layers = -1
    n_threads = 16
    n_ctx = 1 << 10
