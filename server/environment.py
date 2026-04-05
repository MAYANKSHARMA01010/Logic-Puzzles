"""Environment scaffold for your custom RL environment."""


class LogicGateRLEnv:
    """Implement your own reset/step/state logic here."""

    def __init__(self) -> None:
        pass

    def reset(self):
        raise NotImplementedError("Implement reset() in server/environment.py")

    def step(self, action):
        raise NotImplementedError("Implement step() in server/environment.py")
