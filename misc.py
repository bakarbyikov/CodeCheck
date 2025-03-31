import sys

from loguru import logger

logger.remove()
logger.add(sys.stderr, level="TRACE")
logger.add("trace_long.log", level="TRACE")


class Config:
    verbose = False
    n_gpu_layers = -1
    n_threads = 16
    n_ctx = 1 << 11
    use_mmap = False
    
    repo_id = None
    filename = None

    @staticmethod
    def __call__(cls: object):
        return {key: getattr(cls, key)
                for key in sorted(dir(cls))
                if not key.startswith('__')}


@Config()
class Qwen_14B_Q5(Config):
    """9.900 GB"""
    repo_id = "Qwen/Qwen2.5-Coder-14B-Instruct-GGUF"
    filename = "qwen2.5-coder-14b-instruct-q5_0.gguf"


@Config()
class Qwen_7b_Q8(Config):
    """7.718 GB"""
    repo_id = "Qwen/Qwen2.5-Coder-7B-Instruct-GGUF"
    filename = "qwen2.5-coder-7b-instruct-q8_0.gguf"


@Config()
class Qwen_7B_q2(Config):
    """3.254 GB"""
    repo_id = "Qwen/Qwen2.5-Coder-7B-Instruct-GGUF"
    filename = "qwen2.5-coder-7b-instruct-q2_k.gguf"


@Config()
class Qwen_3B_Q8(Config):
    """3.557 GB"""
    repo_id = "Qwen/Qwen2.5-Coder-3B-Instruct-GGUF"
    filename = "qwen2.5-coder-3b-instruct-q8_0.gguf"


@Config()
class Coder_GRPO_3B_Q8(Config):
    """3.503 GB"""
    repo_id = "yasserrmd/Coder-GRPO-3B"
    filename = "unsloth.Q8_0.gguf"

@Config()
class Yandex_8B_Q4(Config):
    """~5 GB - half gpu"""
    n_gpu_layers = 21
    use_mmap = True
    repo_id = "yandex/YandexGPT-5-Lite-8B-instruct-GGUF"
    filename = "YandexGPT-5-Lite-8B-instruct-Q4_K_M.gguf"
    


if __name__ == "__main__":
    from model import Model
    model = Model(Qwen_3B_Q8)

    input()
