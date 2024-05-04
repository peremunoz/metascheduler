from enum import Enum


class ClusterMode(Enum):
    EXCLUSIVE = "exclusive"
    BEST_EFFORT = "best_effort"
    SHARED = "shared"
    DYNAMIC = "dynamic"
