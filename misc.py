
class Config:
    verbose = False
    n_gpu_layers = -1
    n_threads = 16
    n_ctx = 1 << 9
    use_mmap = False

    @staticmethod
    def __call__(cls: object):
        return {key: getattr(cls, key)
                for key in sorted(dir(cls))
                if not key.startswith('__')}


@Config()
class Qwen14B5Q(Config):
    """9.900 GB"""
    repo_id = "Qwen/Qwen2.5-Coder-14B-Instruct-GGUF"
    filename = "qwen2.5-coder-14b-instruct-q5_0.gguf"


@Config()
class Qwen8(Config):
    """7.718 GB"""
    repo_id = "Qwen/Qwen2.5-Coder-7B-Instruct-GGUF"
    filename = "qwen2.5-coder-7b-instruct-q8_0.gguf"


@Config()
class Qwen2(Config):
    """3.254 GB"""
    repo_id = "Qwen/Qwen2.5-Coder-7B-Instruct-GGUF"
    filename = "qwen2.5-coder-7b-instruct-q2_k.gguf"


if __name__ == "__main__":
    from model import Model
    model = Model(Qwen14B5Q)

    input()
