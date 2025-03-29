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
    """~4 GB"""
    repo_id = "Qwen/Qwen2.5-Coder-3B-Instruct-GGUF"
    filename = "qwen2.5-coder-3b-instruct-q8_0.gguf"


@Config()
class Coder_GRPO_3B_Q8(Config):
    """3.503 GB"""
    repo_id = "yasserrmd/Coder-GRPO-3B"
    filename = "unsloth.Q8_0.gguf"


if __name__ == "__main__":
    from model import Model
    model = Model(Coder_GRPO_3B_Q8)

    input()
